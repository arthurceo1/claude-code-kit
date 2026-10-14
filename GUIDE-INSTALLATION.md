# Kit de démarrage Claude Code (v2)

Structure de travail rodée sur ~7 mois et une quinzaine de projets en parallèle. Tout est
copiable tel quel, tout est modifiable. Ce n'est pas une config magique : c'est du contexte écrit
une fois pour ne plus le répéter, plus quelques garde-fous qui bloquent les erreurs qu'un agent
commet vraiment.

## La règle qui explique tout le reste

**Une session oublie tout. Le système doit se souvenir.** Quand Claude se trompe, la question
n'est jamais « comment reformuler mon prompt » mais « où cette leçon aurait-elle dû être écrite
pour que ça ne puisse pas arriver ? ». Cinq endroits, du plus mou au plus dur :

| Endroit | Force | Pour quoi |
|---|---|---|
| Le prompt de la session | nulle, meurt avec la session | rien de ce qu'on veut garder |
| La mémoire | rappelée quand c'est pertinent | une leçon datée, un audit, une décision |
| `CLAUDE.md` | chargé à chaque session du projet | une convention permanente |
| Un skill | chargé quand la tâche correspond | un rituel, une procédure, une définition de « fait » |
| Un hook, une règle de lint, un test | **impossible à ignorer** | tout ce qui coûte de l'argent ou ouvre un accès |

**Règle de promotion :** un problème qui arrive une deuxième fois descend d'une ligne. Un
problème qui coûte de l'argent va directement en bas. Et on n'encode jamais le cas : on encode
la règle.

Contexte bon mais erreur quand même ? Deux cas seulement : il n'a « pas assez essayé » (pas assez
lu, pas vérifié) → monter l'effort ; il « n'en savait pas assez » → monter le modèle.

## Ce qu'il y a dans le kit

| Fichier | Où le mettre | À quoi ça sert |
|---|---|---|
| `CLAUDE.md` | `~/.claude/CLAUDE.md` | Règles transverses, chargées à CHAQUE session, sur tous les projets |
| `CLAUDE-projet.template.md` | `<repo>/CLAUDE.md` | Contexte d'UN projet (stack, pièges, conventions, politique de push) |
| `output-styles/style-perso.md` | `~/.claude/output-styles/` | Force le format de réponse (le plus gros gain de confort au quotidien) |
| `agents/revue-securite.md`, `agents/revue-logique.md` | `~/.claude/agents/` | Les deux relecteurs fixes à contexte neuf, appelés avant tout push |
| `skills/pousser-en-prod/SKILL.md` | `~/.claude/skills/pousser-en-prod/` | La recette unique de mise en prod, tracée |
| `skills/verifier-en-vrai/SKILL.md` | `~/.claude/skills/verifier-en-vrai/` | « Fait » = une capture dans un vrai navigateur, 0 erreur console |
| `skills/reprise-apres-coupure/SKILL.md` | `~/.claude/skills/reprise-apres-coupure/` | Reprendre un chantier coupé sans rien refaire ni rien perdre |
| `skills/audit-multi-agents/SKILL.md` | `~/.claude/skills/audit-multi-agents/` | Un audit en 3 à 6 angles parallèles, un seul livrable daté |
| `skills/first-principles/SKILL.md` | `~/.claude/skills/first-principles/` | Recalculer un coût depuis son plancher physique |
| `hooks/git_guard.py` | `~/.claude/hooks/` | Bloque `git stash` / `reset --hard` / `clean -f` / push forcé, et le push si le typecheck n'est pas vert |
| `hooks/context_guard.py` | `~/.claude/hooks/` | Rappel à l'écran quand le contexte dépasse 60 % (coût zéro en tokens) |
| `statusline.sh` | `~/.claude/` | Barre d'état : dossier, modèle, contexte en %, coût de la session |
| `scripts/lourd.sh` | `~/.claude/scripts/` | Un seul job lourd (typecheck, build, suite de tests) à la fois sur la machine |
| `memoire/MEMORY.md` + 2 fiches d'exemple | dossier mémoire (voir plus bas) | Index des leçons et le format d'une bonne fiche |
| `session-log.md` | `~/.claude/` | Journal : une ligne par session, les plus récentes en haut |
| `settings.json` | `~/.claude/settings.json` | Branche tout : style, hooks, deny-list, statusline, variables, compaction |

Ce qui est volontairement ABSENT (trop lié à mes projets, disponible sur demande) : le skill de
lancement d'un nouveau produit, le skill « nouveau site au design de référence » (copie exacte des
composants d'un projet de référence, seul l'accent change), le skill SEO/GEO par site, le skill de
livrable visuel (deck, carte, PDF, vidéo depuis une source HTML), le skill d'aspiration de site.

## Installation (une heure, dans cet ordre, chaque étape utile seule)

1. **CLAUDE.md global** (le seul vraiment obligatoire)
   ```bash
   cp CLAUDE.md ~/.claude/CLAUDE.md
   ```
   Puis le remplir : tout ce qui est entre `<...>` est à remplacer, tout ce qui ne correspond pas
   à ta façon de bosser est à SUPPRIMER. Vise 150 à 250 lignes. Un CLAUDE.md de 800 lignes que
   personne ne respecte se fait ignorer par le modèle aussi.

2. **Le style de sortie**
   ```bash
   cp output-styles/style-perso.md ~/.claude/output-styles/
   ```
   Puis choisir ce style dans `/config` (ou `"outputStyle"` dans settings.json). C'est ce qui
   empêche les pavés de prose.

3. **`settings.json`** : FUSIONNER avec l'existant, bloc par bloc (`env`, `autoCompactWindow`,
   `permissions.deny`, `hooks`, `statusLine`). Le mode `bypassPermissions` (plus aucune question)
   n'a de sens QUE si la deny-list et le hook git sont en place ; sinon garde le mode par défaut.

4. **Les hooks**
   ```bash
   mkdir -p ~/.claude/hooks && cp hooks/*.py ~/.claude/hooks/ && chmod +x ~/.claude/hooks/*.py
   ```
   Ouvrir `git_guard.py` et remplir `TYPECHECK_MAP` (une ligne par repo où le typecheck doit être
   vert avant push ; liste vide = les gardes git marchent quand même). `context_guard.py` n'a
   rien à régler (seuil par défaut 600k = 60 % d'une fenêtre d'un million).

5. **La statusline** (`jq` requis : `brew install jq`)
   ```bash
   cp statusline.sh ~/.claude/ && chmod +x ~/.claude/statusline.sh
   ```

6. **Les sous-agents**
   ```bash
   mkdir -p ~/.claude/agents && cp agents/*.md ~/.claude/agents/
   ```
   ⚠️ Si tu lances Claude Code via une app qui a son propre dossier de profil (et non `~/.claude`
   directement), ce profil doit voir `agents/` (lien symbolique), comme il voit déjà `skills/` et
   `CLAUDE.md`. Sinon les deux relecteurs n'apparaissent jamais dans la liste des sous-agents, et
   on finit par recopier leur prompt à la main : vécu le 14/10, pendant un mois sans le savoir.
   Vérifier : `/agents` doit lister `revue-securite` et `revue-logique`.

7. **Les skills**
   ```bash
   cp -R skills/* ~/.claude/skills/
   ```
   Vérifier qu'en tapant `/` dans une session, `pousser-en-prod` est proposé.

8. **La mémoire et le journal**
   Claude Code gère son dossier mémoire tout seul, scopé par dépôt, chemin indiqué dans le prompt
   système de la session. Le trouver :
   ```bash
   ls ~/.claude/projects/
   ```
   Copier `memoire/MEMORY.md` dedans s'il n'existe pas, et laisser Claude écrire les fiches.
   `session-log.md` va dans `~/.claude/`. La discipline (quoi écrire, quoi supprimer) est déjà
   dans le CLAUDE.md, section « Framework mémoire ».

9. **Un CLAUDE.md par projet**
   ```bash
   cp CLAUDE-projet.template.md /chemin/vers/le/repo/CLAUDE.md
   ```
   Ou ouvrir Claude Code dans le repo et lancer `/init`, puis corriger à la main.
   ⚠️ Les CLAUDE.md se CUMULENT en remontant l'arborescence : le global + celui du dossier parent
   + celui du repo. Ne recopie pas les règles globales dans chaque projet.

10. **La file d'attente des jobs lourds** (seulement si plusieurs sessions partagent une machine)
    ```bash
    mkdir -p ~/.claude/scripts && cp scripts/lourd.sh ~/.claude/scripts/ && chmod +x ~/.claude/scripts/lourd.sh
    ```
    Puis, dans chaque CLAUDE.md de projet, la commande de typecheck s'écrit
    `bash "$HOME/.claude/scripts/lourd.sh" npx tsc --noEmit`.

## Les 8 erreurs de structure qui coûtent le plus cher

1. **Tout mettre dans le CLAUDE.md.** Il est rechargé à chaque session : chaque ligne inutile est
   payée à chaque fois, et noie les lignes qui comptent. Le durable va dans le CLAUDE.md, le
   ponctuel (résultat d'un audit, état d'un chantier) va en mémoire.
2. **Mettre une règle de code en mémoire au lieu du CLAUDE.md du projet.** Le CLAUDE.md remonte
   les dossiers, la mémoire est scopée par dépôt : une règle laissée en mémoire est invisible
   pile là où le code se fait.
3. **Écrire des mémoires sans jamais consolider.** Au bout de 2 mois l'index fait 150 lignes de
   doublons et de leçons périmées, et le rappel devient du bruit.
4. **Croire que le modèle s'escalade tout seul.** Une session lancée sur un modèle intermédiaire
   y reste du début à la fin. L'appel à un modèle plus fort, en sous-agent à contexte neuf, doit
   être déclenché explicitement (décision d'archi, bug qui revient, revue avant push).
5. **Prendre un « ça passe » pour une preuve.** Une vérification qui s'interrompt avant son objet
   rend un résultat vide, et un vide se lit comme un vert. Demander la preuve concrète (la
   commande lancée, son code de sortie, la capture, le test qui échouerait si le bug revenait).
6. **Relire avec un prompt improvisé.** Chaque revue « maison » a un prompt différent, donc une
   qualité différente, et aucune trace. Deux relecteurs fixes, un seul prompt, un seul skill qui
   les appelle.
7. **Encoder le cas au lieu de la règle.** Un garde qui énumère (liste de mots, regex de
   tournures) ne converge jamais sous revue : chaque passe trouve un cas de plus. Après deux
   passes du même type, changer de règle, pas allonger la liste.
8. **Rouvrir la session d'hier.** Elle repart avec son contexte au maximum et chaque message y
   coûte jusqu'à 19 fois le prix d'un message dans une session neuve. Un sujet, une session, puis
   on ferme.

## Ce qui n'est PAS dans ce kit et qui compte quand même

- **Les worktrees** (`git worktree add`) dès que plusieurs sessions tournent sur le même repo.
  Deux sessions dans le même dossier se marchent dessus sans prévenir.
- **`/simplify`** quand le code a grossi sur plusieurs itérations, avant la revue.
- **Les règles de lint maison et les tests qui lisent le code source** (pour verrouiller une
  règle métier à un seul endroit) : c'est de l'organisation de code, pas de la configuration.
  Le guide long « How We Work With Claude Code » (en anglais, sur demande) couvre ces sujets.
