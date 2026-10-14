#!/usr/bin/env python3
"""Garde-fous git pour toutes les sessions Claude Code (hook PreToolUse/Bash).

Règles (voir ~/.claude/CLAUDE.md) :
  1. JAMAIS git stash / pop / drop / apply / push / save / store / clear
     (pile globale au dépôt, partagée entre sessions parallèles ; incident réel
     du 01/08/2026 : un pop a ramené le travail d'une autre session, 22 fichiers
     en conflit). Autorisés : stash create / list / show.
  2. JAMAIS git reset --hard ni git clean -f* sans accord explicite de l'utilisateur.
  3. JAMAIS de push forcé (-f, --force*, refspec +src:dst) sans accord de l'utilisateur.
  4. Typecheck vert obligatoire avant tout git push sur les repos mappés
     (voir TYPECHECK_MAP). Échappatoire d'urgence, avec accord de l'utilisateur :
     préfixer la commande de GIT_GUARD_TYPECHECK=0 (vraie assignation, pas du
     texte cité).

Analyse (v3, durcie après revue croisée gpt-5.5 du 03/08/2026) :
  - les continuations backslash-newline sont jointes AVANT découpe ;
  - découpe en segments sur | ; & \n UNIQUEMENT hors quotes (un message de
    commit contenant "; git stash" ne crée plus de faux segment) ;
  - chaque segment est tokenisé (shlex) ; on saute assignations VAR=x,
    wrappers (env/time/nohup/...) et leurs flags, et mots-clés shell
    (if/then/while/...) pour trouver la commande effective ;
  - les règles ne s'appliquent que si cette commande est `git`, avec récursion
    dans les payloads `bash -c` / `-lc` ;
  - jugement par TOKENS (un texte cité ne déclenche rien) ;
  - segment intokenisable (quote non fermée résiduelle) contenant `git` :
    analyse texte grossière, côté blocage (fail-safe).

Threat model : l'usage ACCIDENTEL par un agent de bonne foi. Un contournement
volontairement obfusqué reste possible (couvert en partie par permissions.deny) ;
ce n'est pas l'objectif de ce garde.

Contrat hook : exit 0 = autorisé, exit 2 = bloqué (stderr montré à l'agent).
Erreur interne du script = autorisé (un garde cassé ne doit pas bloquer tout
Bash) ; mais tout échec à LANCER le typecheck sur un repo mappé = bloqué.
"""
import json
import os
import re
import shlex
import subprocess
import sys

WRAPPERS = ("env", "time", "nohup", "command", "exec", "caffeinate")
SHELLS = ("bash", "sh", "zsh", "dash", "ksh")
SHELL_KEYWORDS = ("if", "then", "else", "elif", "fi", "while", "until", "do", "done", "!", "{", "(")
GIT_GLOBAL_OPTS_WITH_ARG = ("-C", "-c", "--git-dir", "--work-tree", "--exec-path")

TYPECHECK_MAP = [
    # (motif cherché dans l'URL du remote origin, args passés à node_modules/.bin/tsc,
    #  description affichée). À PERSONNALISER : une ligne par repo où le typecheck
    #  doit être vert avant tout push. Laisser la liste vide désactive cette règle,
    #  les gardes git (stash/reset/clean/force) continuent de s'appliquer.
    # ("mon-repo", ["--noEmit"], "tsc --noEmit"),
    # ("mon-monorepo", ["--noEmit", "-p", "apps/web/tsconfig.json"],
    #  "tsc --noEmit -p apps/web/tsconfig.json"),
]

TSC_TIMEOUT = 360  # secondes ; fail-closed au-delà

STASH_MSG = (
    "BLOQUÉ par le garde-fou git (règle du setup, non négociable) : `git stash` est "
    "interdit sur ces repos. La pile de stash est GLOBALE au dépôt et partagée entre "
    "les sessions parallèles : un pop peut rendre le travail d'une AUTRE session "
    "(incident réel du 01/08/2026, 22 fichiers en conflit). À la place : commite tôt "
    "(quitte à réécrire), travaille dans un worktree dédié (`git worktree add`), ou "
    "utilise `git stash create` (fabrique un commit sans toucher la pile)."
)
RESET_MSG = (
    "BLOQUÉ par le garde-fou git : `git reset --hard` est interdit sans accord "
    "explicite d'l'utilisateur (chemins partagés entre sessions parallèles, perte de travail "
    "possible). Alternatives : `git restore <fichier>` ciblé, ou un worktree jetable. "
    "Si c'est vraiment nécessaire, demande d'abord à l'utilisateur."
)
CLEAN_MSG = (
    "BLOQUÉ par le garde-fou git : `git clean -f` est interdit sans accord explicite "
    "d'l'utilisateur (supprime des fichiers non suivis qui peuvent appartenir à une autre "
    "session parallèle). `git clean -n` (dry-run) est autorisé ; pour le reste, "
    "demande à l'utilisateur."
)
FORCE_MSG = (
    "BLOQUÉ par le garde-fou git : push forcé interdit sans accord explicite de l'utilisateur "
    "(réécriture d'historique sur un repo partagé entre sessions). Ça inclut -f, "
    "--force*, les options courtes groupées contenant f, et les refspecs +src:dst. "
    "Demande à l'utilisateur avant."
)

# Positionné pendant l'analyse si l'échappatoire GIT_GUARD_TYPECHECK=0 apparaît
# comme VRAIE assignation en préfixe de commande (pas du texte cité).
HATCH = {"active": False}


def deny(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(2)


def allow_with_message(msg):
    print(json.dumps({"systemMessage": msg}))
    sys.exit(0)


def split_segments(cmd):
    """Découpe sur | ; & et retours ligne, HORS quotes. Les continuations
    backslash-newline ont déjà été jointes par l'appelant."""
    segs, buf, quote, esc = [], [], None, False
    for ch in cmd:
        if esc:
            buf.append(ch)
            esc = False
            continue
        if ch == "\\" and quote != "'":
            esc = True
            buf.append(ch)
            continue
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
        elif ch in ("'", '"'):
            quote = ch
            buf.append(ch)
        elif ch in "|;&\n":
            segs.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    segs.append("".join(buf))
    return [s for s in (x.strip() for x in segs) if s]


def git_token_lists(segment, depth=0):
    """[(kind, payload)] où kind = 'tokens' (payload = tokens depuis git) ou
    'raw' (fallback texte). Saute assignations, wrappers + leurs flags, et
    mots-clés shell ; récurse dans bash -c / -lc."""
    out = []
    if depth > 4:
        return out
    try:
        tokens = shlex.split(segment, posix=True)
    except ValueError:
        if re.search(r"\bgit\b", segment):
            out.append(("raw", segment))
        return out
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", t):
            if t == "GIT_GUARD_TYPECHECK=0":
                HATCH["active"] = True
            i += 1
        elif t in WRAPPERS:
            i += 1
            while i < len(tokens) and tokens[i].startswith("-"):
                i += 1
        elif t in SHELL_KEYWORDS:
            i += 1
        else:
            break
    if i >= len(tokens):
        return out
    head = os.path.basename(tokens[i])
    if head == "git":
        out.append(("tokens", tokens[i:]))
    elif head in SHELLS:
        for j in range(i + 1, len(tokens) - 1):
            # -c exact ou groupé (-lc, -xc...) : le payload est le token suivant.
            if tokens[j] == "-c" or (re.match(r"^-[a-zA-Z]+$", tokens[j]) and "c" in tokens[j]):
                for sub in split_segments(tokens[j + 1]):
                    out.extend(git_token_lists(sub, depth + 1))
    return out


def git_subcommand(tokens):
    """(sous-commande, tokens restants, valeur de -C éventuelle)."""
    i, c_dir = 1, None
    while i < len(tokens):
        t = tokens[i]
        if t in GIT_GLOBAL_OPTS_WITH_ARG:
            if t == "-C" and i + 1 < len(tokens):
                c_dir = tokens[i + 1]
            i += 2
            continue
        if t.startswith("-"):
            i += 1
            continue
        return t, tokens[i + 1:], c_dir
    return "", [], c_dir


def check_tokens(tokens):
    sub, rest, _ = git_subcommand(tokens)
    if sub == "stash":
        action = rest[0] if rest and not rest[0].startswith("-") else ""
        if action not in ("create", "list", "show"):
            deny(STASH_MSG)
    elif sub == "reset":
        if "--hard" in rest:
            deny(RESET_MSG)
    elif sub == "clean":
        for t in rest:
            if t == "--force" or (re.match(r"^-[a-zA-Z]+$", t) and "f" in t):
                deny(CLEAN_MSG)
    elif sub == "push":
        for t in rest:
            if t in ("--force", "--force-with-lease", "--force-if-includes") or t.startswith("--force-with-lease="):
                deny(FORCE_MSG)
            if re.match(r"^-[a-zA-Z]+$", t) and "f" in t:  # -f, -uf, -fu...
                deny(FORCE_MSG)
            if t.startswith("+") and len(t) > 1:  # refspec forcée +src:dst
                deny(FORCE_MSG)


def check_raw(segment):
    """Fallback texte pour segments intokenisables : grossier, côté blocage."""
    opts = r"(?:-C\s+\S+\s+|-c\s+\S+\s+|--git-dir=\S+\s+|--work-tree=\S+\s+)*"
    m = re.search(r"\bgit\s+" + opts + r"stash\b\s*(\S*)", segment)
    if m and m.group(1) not in ("create", "list", "show"):
        deny(STASH_MSG)
    if re.search(r"\bgit\s+" + opts + r"reset\b[^\n]*--hard", segment):
        deny(RESET_MSG)
    m = re.search(r"\bgit\s+" + opts + r"clean\b([^\n]*)", segment)
    if m and re.search(r"(?:^|\s)-{1,2}(?:force|[a-zA-Z]*f)", m.group(1)):
        deny(CLEAN_MSG)
    if re.search(r"\bgit\s+" + opts + r"push\b", segment) and (
        re.search(r"(?:^|\s)--force(?:-with-lease|-if-includes)?\b", segment)
        or re.search(r"(?:^|\s)-[a-zA-Z]*f\b", segment)
    ):
        deny(FORCE_MSG)


def push_c_dirs(entries):
    """Les valeurs -C des commandes git push détectées (prioritaires pour
    identifier le repo à typechecker)."""
    dirs = []
    for kind, payload in entries:
        if kind == "tokens":
            sub, _, c_dir = git_subcommand(payload)
            if sub == "push" and c_dir:
                dirs.append(c_dir)
    return dirs


def has_push(entries):
    for kind, payload in entries:
        if kind == "tokens":
            if git_subcommand(payload)[0] == "push":
                return True
        elif re.search(r"\bgit\b[^\n]*\bpush\b", payload):
            return True
    return False


def find_repo_dir(cmd, cwd, priority_dirs):
    dirs = []
    for d in priority_dirs:
        if not os.path.isabs(d) and cwd:
            d = os.path.join(cwd, d)
        d = os.path.expanduser(d)
        if os.path.isdir(d):
            dirs.append(d)
    m = re.search(r"\bcd\s+(?:\"([^\"]+)\"|'([^']+)'|(\S+))", cmd)
    if m:
        target = os.path.expanduser(os.path.expandvars(m.group(1) or m.group(2) or m.group(3)))
        if os.path.isdir(target):
            dirs.append(target)
    if cwd and os.path.isdir(cwd):
        dirs.append(cwd)
    for d in dirs:
        try:
            url = subprocess.run(
                ["git", "-C", d, "remote", "get-url", "origin"],
                capture_output=True, text=True, timeout=10,
            )
            if url.returncode == 0:
                top = subprocess.run(
                    ["git", "-C", d, "rev-parse", "--show-toplevel"],
                    capture_output=True, text=True, timeout=10,
                )
                if top.returncode == 0:
                    return url.stdout.strip(), top.stdout.strip()
        except Exception:
            continue
    return None, None


def check_typecheck_gate(cmd, cwd, priority_dirs):
    if os.environ.get("GIT_GUARD_TYPECHECK") == "0" or HATCH["active"]:
        allow_with_message(
            "⚠️ Garde typecheck désactivé explicitement (GIT_GUARD_TYPECHECK=0) pour ce push."
        )
    origin, toplevel = find_repo_dir(cmd, cwd, priority_dirs)
    if not origin:
        return
    for pattern, tsc_args, desc in TYPECHECK_MAP:
        if pattern in origin:
            tsc_bin = os.path.join(toplevel, "node_modules", ".bin", "tsc")
            if not os.path.exists(tsc_bin):
                # Trade-off assumé (revue du 03/08, finding 5) : un worktree sans
                # node_modules ne peut pas typechecker ; exiger un npm ci de
                # plusieurs minutes pousserait vers l'échappatoire permanente.
                # Le CI GitHub (typecheck.yml) rattrape ce cas après push.
                allow_with_message(
                    "⚠️ Garde typecheck sauté : node_modules absent de " + toplevel
                    + " (worktree sans install ?). Le CI GitHub vérifiera après push."
                )
            try:
                res = subprocess.run(
                    [tsc_bin] + tsc_args, cwd=toplevel,
                    capture_output=True, text=True, timeout=TSC_TIMEOUT,
                )
            except subprocess.TimeoutExpired:
                deny(
                    "BLOQUÉ : le typecheck (" + desc + ") n'a pas fini en " + str(TSC_TIMEOUT)
                    + "s dans " + toplevel + ". Lance-le à la main, vérifie qu'il est vert, "
                    "puis relance le push (ou GIT_GUARD_TYPECHECK=0 avec l'accord de l'utilisateur)."
                )
            except Exception as e:
                # FileNotFoundError, PermissionError... : fail-closed, jamais
                # d'allow silencieux quand le garde ne peut pas vérifier.
                deny(
                    "BLOQUÉ : impossible de LANCER le typecheck (" + desc + ") dans "
                    + toplevel + " : " + repr(e) + ". Vérifie l'environnement, lance le "
                    "typecheck à la main, puis relance le push."
                )
            out = (res.stdout or "") + "\n" + (res.stderr or "")
            # Les erreurs dans .next/ sont des artefacts de build périmés (ex :
            # .next/types/validator.ts référençant une route supprimée depuis le
            # dernier build). Vercel rebuilde de zéro et reste le filet pour la
            # conformance des routes ; on ne juge que le code source.
            err_lines = [
                l for l in out.splitlines()
                if "error TS" in l and not re.match(r"(?:.*/)?\.next/", l.strip())
            ]
            if err_lines:
                deny(
                    "BLOQUÉ : typecheck ROUGE (" + desc + ") dans " + toplevel + ". "
                    "Règle d'l'utilisateur : on ne pousse jamais du code qui ne typecheck pas. "
                    "Corrige d'abord :\n" + "\n".join(err_lines[-25:])
                )
            if res.returncode != 0 and "error TS" not in out:
                deny(
                    "BLOQUÉ : le typecheck (" + desc + ") a échoué sans erreur TS lisible "
                    "dans " + toplevel + " (le garde ne peut pas vérifier). Détail :\n"
                    + "\n".join(out.strip().splitlines()[-15:])
                )
            return
    # repo non mappé : pas de gate


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    cmd = (data.get("tool_input") or {}).get("command") or ""
    if "git" not in cmd:
        sys.exit(0)
    # Continuations backslash-newline : le shell les joint, nous aussi (revue
    # 03/08, finding 1 : sinon `git reset \\\n --hard` échappe au découpage).
    cmd_joined = re.sub(r"\\\n\s*", " ", cmd)
    entries = []
    for segment in split_segments(cmd_joined):
        entries.extend(git_token_lists(segment))
    for kind, payload in entries:
        if kind == "tokens":
            check_tokens(payload)
        else:
            check_raw(payload)
    if has_push(entries):
        check_typecheck_gate(cmd_joined, data.get("cwd") or "", push_c_dirs(entries))
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        # Un garde cassé ne doit jamais bloquer tout Bash : on autorise.
        sys.exit(0)
