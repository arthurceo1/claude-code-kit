---
name: first-principles
description: Reconstruire un coût ou une architecture depuis son plancher physique au lieu de le comparer à l'existant. À lancer quand la question est "pourquoi c'est si cher / si lent", "ça devrait coûter combien", avant un gros chantier d'infra, ou face à un prix fournisseur qui semble subi. PAS pour un debug, un fix, une revue de code (voir /code-review) ni un nettoyage (voir /simplify).
---

# Plancher théorique

Le réflexe par défaut compare un coût à sa valeur d'hier. Ce skill le compare à
son minimum physique. L'écart entre les deux est la seule marge réelle.

## 1. Vérifier le chiffre de départ (non négociable)

Un plancher calculé sous un numérateur faux ne vaut rien, et ici le numérateur
est faux une fois sur deux :
- **Mesuré ou estimé ?** Une estimation encore allumée alors que la mesure
  existe fausse tout le calcul (cas vécu : coût vision au P&L).
- **Bonne unité ?** Compter les requêtes quand la facture est aux octets donne
  un audit entièrement à côté (cas vécu : egress Supabase).
- **Bonne fenêtre ?** Un pic mensuel lu sur une journée calme ne dit rien.

Si le chiffre n'est pas mesuré, la première livraison est la mesure, pas l'analyse.

## 2. Décomposer jusqu'à l'incompressible

Lister ce qui est réellement payé : GPU-secondes, octets sortis, tokens, appels
API, heures humaines. Pour chaque poste, une seule question : **loi physique ou
habitude héritée ?** Un prix fournisseur, un forfait, un "on a toujours fait
comme ça" ne sont jamais des lois.

## 3. Poser le plancher, calculer le ratio

Plancher = ces postes incompressibles au prix spot, sans surcouche.
Ratio = coût réel ÷ plancher.
- Ratio sous 2 : le sujet est déjà serré. S'arrêter là et le dire.
- Ratio au-dessus de 5 : c'est du process, pas de la matière. Ça vaut un chantier.

## 4. Reconstruire, dans cet ordre

Supprimer, puis simplifier, puis accélérer, puis automatiser. Une étape
supprimée ne coûte rien et ne casse jamais. Avant de proposer une suppression,
vérifier qu'elle ne portait pas une garantie silencieuse (auth, idempotence,
retenue, trace de paie).

## Sortie

Style de sortie du CLAUDE.md global, sans exception : le chiffre réel, le plancher,
le ratio, une ligne par piste, la reco en une ligne. Pas de trace de
raisonnement, pas de section "hypothèses challengées". Une hypothèse dont dépend
le résultat = une puce, avec le test qui la trancherait.
