---
name: pousser-en-prod
description: Mettre du code en prod sur n'importe quel projet avec la recette unique : classer le diff, tests, revue par sous-agents fixes (revue-logique seul, ou revue-securite + revue-logique en parallèle si le diff est sensible), SQL avant le code, attendre le vrai déploiement, contrôle en prod, trace dans le journal. À lancer dès que l'utilisateur dit « pousse », « go prod », « mets en ligne », « déploie », ou avant tout merge ou migration vers la prod.
---

# Pousser en prod : une seule recette, tracée

Pourquoi ce skill : sans recette unique, les revues dérivent vers des prompts improvisés
(mesuré : ~700 sous-agents « maison » par semaine au prompt variable, et 40 % des mises en prod
d'une semaine sans aucune revue tracée).

## 0. Avant tout
- Lire la règle de push du projet dans son `CLAUDE.md` (direct `main` / staging seulement /
  branche + PR / jamais sans feu vert).
- Travailler dans un worktree. **Jamais `git stash`, `stash pop`, `reset --hard`, `clean`** : la
  pile de stash est partagée entre sessions.
- Aucun secret dans le diff (`git diff | grep -iE 'key|token|secret|password'` : chaque hit
  s'explique ou se retire).

## 1. Classer le diff
Sensible si une ligne touche : auth ou session, RBAC/RLS/permissions, migration ou fonction SQL,
argent (paie, prix, solde, taux, paiement), mineurs ou modération, secrets, webhooks ou crons,
suppression de données. Sinon : simple (UI, copy, petit fix, test).

## 2. Vérifier avant de relire
- Typecheck du projet (machine partagée : via `bash "$HOME/.claude/scripts/lourd.sh" …`, jamais
  deux jobs lourds en parallèle).
- Tests liés au diff, puis la suite complète si le projet la joue au push. Lire le CODE DE
  SORTIE, pas la fin du log.
- Linter en mode `--fix` s'il existe.
- Si le code a grossi sur plusieurs itérations : `/simplify` d'abord.

## 3. Relire, par les sous-agents fixes (jamais un prompt improvisé)
- **Diff simple** : un sous-agent `revue-logique` (contexte neuf, modèle fort).
- **Diff sensible** : `revue-securite` ET `revue-logique` lancés en parallèle, dans le même
  message.
- Dans le prompt : le projet, la règle de push, ce que le diff est censé faire en 3 lignes, et
  le diff lui-même (inliné : `git diff <base>...HEAD`), plus la liste des fichiers touchés. Rien
  d'autre.
- Chaque défaut rendu est vérifié dans le code avant d'agir : confirmé (on corrige), écarté (une
  ligne de raison). Correctif non trivial = nouvelle passe des mêmes agents.
- Après 2 passes qui trouvent « encore un cas » du même type : changer de règle (générique) au
  lieu d'allonger la liste, sinon la revue ne converge pas.
- On ne pousse QUE quand les deux listes sont vides ou entièrement écartées avec raison.

## 4. Pousser dans le bon ordre
- SQL d'abord : migration appliquée et vérifiée (corps de la fonction, droits, `search_path`)
  AVANT le code qui en dépend ; une migration qui renomme garde l'ancienne colonne jusqu'au
  déploiement du code.
- Push séparé de tout rebase (un push enchaîné à un rebase pousse un rebase à moitié).
- Attendre le VRAI déploiement : Vercel = statut READY sur le bon commit ; Render = « Live » ;
  Cloudflare = nouvelle version du Worker ; déploiement par hook = attendre le tick (un commit
  vide ou un « Redeploy » peut être sauté).

## 5. Contrôler en prod
- Une preuve par changement : URL en 200, requête SQL qui montre la nouvelle valeur, ligne de
  log du cron, capture. Changement visible = skill `verifier-en-vrai`.
- Ce qui n'a pas pu être vérifié est écrit noir sur blanc (« non vérifié : … »), jamais passé
  sous silence.

## 6. Tracer
- Entrée dans `~/.claude/session-log.md` (en haut) : projet, commit, « revue-logique » ou
  « revue-securite + revue-logique », nombre de défauts confirmés / écartés, preuve en prod,
  prochaine étape.
- Récap à l'utilisateur : ce qui est en ligne, ce qui a été corrigé grâce aux revues, ce qui
  reste non vérifié.

## À quoi ressemble « fait »
- Typecheck et tests verts avec code de sortie lu.
- Revues tracées avec leur angle, aucun défaut ouvert.
- Déploiement constaté sur le bon commit.
- Une preuve en prod par changement, ou la mention « non vérifié » explicite.
- Ligne de journal écrite.
