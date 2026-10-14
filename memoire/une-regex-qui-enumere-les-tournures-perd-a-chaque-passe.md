---
name: une-regex-qui-enumere-les-tournures-perd-a-chaque-passe
description: "Un garde qui ÉNUMÈRE des cas (liste de mots, regex de tournures) ne converge jamais sous revue : chaque passe trouve une tournure de plus. Vécu le 14/10/2026 : 6 passes de revue sur un filtre « mineur » ; la règle générique (« tout nombre de 10 à 17 dans une raison = indice ») a tenu en une passe."
metadata:
  type: reference
---

<!--
DEUXIÈME FICHE D'EXEMPLE, réelle elle aussi. Ce qu'elle montre en plus de la première :
  1. La leçon vient d'une BOUCLE (6 passes), pas d'un incident unique : c'est le motif qui compte.
  2. Le corps donne le signe d'alerte qui permet de reconnaître la situation la prochaine fois.
  3. Le lien [[...]] relie deux leçons de la même famille (un garde qui ne garde pas).
-->

Un filtre devait reconnaître « un âge sous 18 ans » dans une raison écrite par un modèle.
Version 1 : `minor|under 18|underage`. Chaque relecture a trouvé une tournure absente
(« age: 16 », « less than 18 », « just turned 17 », « born 2010 », « 16F », « 11th grade »...).
Six passes de revue, treize défauts, tous de la même famille.

Ce qui a mis fin à la série : abandonner l'énumération pour une règle sur la FORME (« tout nombre
isolé de 10 à 17 dans une raison de modération est un indice ») et lire la SOURCE (la raison
écrite par le modèle) plutôt que sa conclusion (le verdict), qui dépendait de l'ancienne regex.

**La règle : quand une 2e passe de revue trouve « encore un cas » du même type, le défaut n'est
pas la liste, c'est le fait d'avoir une liste. Changer de règle, pas allonger.**

**Signe d'alerte concret :** un correctif qui ajoute une alternative à une regex ou un mot à une
liste. Une fois, ça passe ; deux fois, c'est la forme du garde qui est fausse. Voir
[[verification-qui-s-arrete-avant-de-verifier]].
