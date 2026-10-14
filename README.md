# Claude Code Kit

Une configuration Claude Code complète, prête à copier : le `CLAUDE.md` global, un modèle de
`CLAUDE.md` par projet, un style de réponse, deux relecteurs fixes (sous-agents), cinq skills,
deux hooks, une barre d'état, la mémoire et le journal. Rodée sur ~7 mois, une quinzaine de
projets, plusieurs sessions en parallèle, par un fondateur non-technique.

Aucune information personnelle, aucune donnée business : uniquement de la structure et des
règles, avec des `<...>` à remplacer par les tiennes.

## Télécharger

- Tout d'un coup : **[claude-code-kit.zip](../../archive/refs/heads/main.zip)** (le bouton vert
  « Code » puis « Download ZIP » fait la même chose).
- Un seul fichier qui contient tout : [`KIT-COMPLET.md`](KIT-COMPLET.md) (à coller à Claude).

## Installation en une phrase (à copier-coller dans Claude Code)

Dézippe le kit, ouvre Claude Code dans le dossier dézippé, et colle ceci :

```
Ce dossier est un kit de configuration Claude Code (lis GUIDE-INSTALLATION.md d'abord).
Installe-le chez moi : copie chaque fichier à sa destination (~/.claude/CLAUDE.md,
~/.claude/output-styles/, ~/.claude/agents/, ~/.claude/skills/, ~/.claude/hooks/,
~/.claude/statusline.sh, ~/.claude/scripts/lourd.sh, ~/.claude/session-log.md, et
memoire/MEMORY.md dans mon dossier mémoire). Si un fichier existe déjà, ne l'écrase pas :
propose une fusion section par section, surtout pour settings.json (fusionne env,
autoCompactWindow, permissions.deny, hooks, statusLine avec ce que j'ai). Rends exécutables
les .py et .sh. Ensuite, pose-moi les questions nécessaires pour remplir les <...> de
~/.claude/CLAUDE.md (qui je suis, ma langue, mes projets avec leur politique de push, mes
seuils de coût) et la TYPECHECK_MAP de hooks/git_guard.py. Termine en vérifiant que
revue-securite et revue-logique apparaissent dans /agents et que pousser-en-prod apparaît
dans la liste des skills, puis fais-moi un récap de ce qui est installé et de ce qui reste
à personnaliser.
```

Si tu as déjà une configuration, remplace « Installe-le chez moi » par « Compare-le à ma
configuration actuelle et propose-moi, point par point, ce qui vaut la peine d'être adopté ».

## Ce qu'il y a dedans

| Dossier / fichier | Destination | Rôle |
|---|---|---|
| `CLAUDE.md` | `~/.claude/CLAUDE.md` | Règles transverses, chargées à chaque session |
| `CLAUDE-projet.template.md` | `<repo>/CLAUDE.md` | Contexte d'un projet (stack, pièges, politique de push) |
| `output-styles/style-perso.md` | `~/.claude/output-styles/` | Réponse d'abord, puces, questions à la fin, jamais de pavés |
| `agents/` | `~/.claude/agents/` | `revue-securite` et `revue-logique`, les deux relecteurs à contexte neuf |
| `skills/` | `~/.claude/skills/` | `pousser-en-prod`, `verifier-en-vrai`, `reprise-apres-coupure`, `audit-multi-agents`, `first-principles` |
| `hooks/` | `~/.claude/hooks/` | `git_guard.py` (stash, reset, clean, push forcé, typecheck avant push) et `context_guard.py` (rappel à 60 % de contexte) |
| `statusline.sh` | `~/.claude/` | Dossier, modèle, contexte en %, coût de la session (`jq` requis) |
| `scripts/lourd.sh` | `~/.claude/scripts/` | Un seul job lourd à la fois sur une machine partagée |
| `memoire/` | ton dossier mémoire | Index + deux fiches d'exemple (le format compte plus que le contenu) |
| `session-log.md` | `~/.claude/` | Journal : une ligne par session, les récentes en haut, 14 jours |
| `settings.json` | `~/.claude/settings.json` | À FUSIONNER : style, variables, compaction, deny-list, hooks, statusline |
| `GUIDE-INSTALLATION.md` | à lire | L'ordre d'installation, les 8 erreurs qui coûtent le plus cher |
| `KIT-COMPLET.md` | à coller à Claude | Tout le kit en un seul fichier |

## Si tu as déjà reçu le guide « How We Work With Claude Code »

Le guide explique le pourquoi ; ce kit est le quoi, à jour d'octobre 2026. Ce qui a changé
depuis le guide : la revue croisée par un autre modèle est remplacée par deux sous-agents
Claude fixes, la mise en prod est un seul skill tracé, le coût d'une session a été mesuré
(98 % = la relecture du contexte, d'où la barre d'état, le hook de contexte et la compaction
automatique), et le journal se garde 14 jours. Le détail est en tête de `KIT-COMPLET.md`.

## Licence

Fais-en ce que tu veux. Si tu l'améliores, renvoie l'ascenseur.
