#!/bin/bash
# Un seul job LOURD à la fois sur le machine partagée (tsc, next build, vitest complet).
#
# Pourquoi : le 28/09/2026 le mini (16 Go) a manqué de mémoire deux fois en
# 30 minutes. Cause mesurée dans le journal des commandes : trois sessions en
# parallèle ont chacune lancé un `tsc --noEmit` d'un gros projet avec
# --max-old-space-size=8192, plus des vitest, à la même minute. Force Quit
# affichait 38 Go pour le lanceur, qui compte tout ce qu'il a lancé.
#
# Usage (les variables d'env passent) :
#   NODE_OPTIONS=--max-old-space-size=8192 bash "$HOME/.claude/scripts/lourd.sh" npx tsc --noEmit -p tsconfig.json
#   bash "$HOME/.claude/scripts/lourd.sh" bash -c 'cd X && npx vitest run'
#
# Les autres attendent leur tour (30 min max, puis code 75). Le verrou est
# dans /tmp/claude-<uid>, partagé par toutes les sessions et tous les comptes.

LOCK="/tmp/claude-$(id -u)/lourd.lock"
WAIT="${LOURD_WAIT:-1800}"
mkdir -p "$(dirname "$LOCK")"

if [ "$#" -eq 0 ]; then
  echo "usage: lourd.sh <commande...>" >&2
  exit 64
fi

# Tente sans attendre, pour dire qu'on attend quand c'est le cas.
if /usr/bin/lockf -k -t 0 "$LOCK" true 2>/dev/null; then
  :
else
  echo "[lourd] un autre job lourd tourne, en attente de mon tour (max ${WAIT}s)..." >&2
fi
exec /usr/bin/lockf -k -t "$WAIT" "$LOCK" "$@"
