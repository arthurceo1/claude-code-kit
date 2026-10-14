#!/bin/sh
# Statusline Claude Code : contexte utilise + cout de la session.
# Claude Code envoie un JSON sur stdin. On lit 3 champs, rien de plus.
# Tout champ absent est affiche "-", jamais d'erreur a l'ecran.

json=$(cat)

pct=$(printf '%s' "$json" | jq -r '.context_window.used_percentage // empty' 2>/dev/null)
cost=$(printf '%s' "$json" | jq -r '.cost.total_cost_usd // empty' 2>/dev/null)
model=$(printf '%s' "$json" | jq -r '.model.display_name // empty' 2>/dev/null)
dir=$(printf '%s' "$json" | jq -r '.workspace.current_dir // .cwd // empty' 2>/dev/null)

# contexte : arrondi a l'entier, avec un marqueur quand ca chauffe
if [ -n "$pct" ]; then
    p=$(printf '%.0f' "$pct" 2>/dev/null || echo "$pct")
    case "$p" in
        ''|*[!0-9]*) ctx="ctx ${pct}%" ;;
        *) if [ "$p" -ge 50 ]; then ctx="ctx ${p}% !!"
           elif [ "$p" -ge 30 ]; then ctx="ctx ${p}% !"
           else ctx="ctx ${p}%"; fi ;;
    esac
else
    ctx="ctx -"
fi

if [ -n "$cost" ]; then
    c=$(printf '$%.2f' "$cost" 2>/dev/null || echo "\$$cost")
else
    c="\$-"
fi

[ -n "$dir" ] && dir=$(basename "$dir") || dir="-"
[ -n "$model" ] || model="-"

printf '%s | %s | %s | %s' "$dir" "$model" "$ctx" "$c"
