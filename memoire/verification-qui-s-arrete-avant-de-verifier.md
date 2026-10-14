---
name: verification-qui-s-arrete-avant-de-verifier
description: "Une vérification qui échoue TÔT, sur une étape annexe, se lit comme une vérification qui passe. Vécu le 18/08/2026 : `next build` mourait sur les polices Google avant de compiler, et « erreur seulement sur les polices » a été pris pour un feu vert pendant toute une journée."
metadata:
  type: reference
---

<!--
CETTE FICHE EST UN EXEMPLE RÉEL, gardée telle quelle parce que c'est le format qui compte.
Ce qui en fait une bonne fiche :
  1. Le `name` est un slug qui DIT la leçon, pas le projet ni la date.
  2. La `description` porte la leçon complète : c'est elle qui sert à décider, plus tard, si la
     fiche est pertinente. Une description du genre "notes sur le build" ne se rappellera jamais.
  3. Le corps raconte le cas concret, puis GÉNÉRALISE en une règle qu'on peut appliquer ailleurs.
  4. Il finit par un signe d'alerte reconnaissable dans une future session.
  5. `type` : user (qui est l'utilisateur) | feedback (comment il veut qu'on bosse) |
     project (chantier en cours) | reference (leçon technique durable).
  6. Les liens vers d'autres fiches s'écrivent [[nom-de-la-fiche]], sans .md.
-->

Le 18/08/2026 au matin, une panne de production (trois exports non-async dans un fichier
`"use server"`, qui vident le module entier). Parade posée dans la foulée, écrite dans chaque
brief d'agent : **lancer `npx next build` avant tout push.**

Cette parade n'a jamais rien vérifié. Le bundler télécharge les polices Google depuis sa couche
Rust, qui ignore les variables de proxy de la machine : le build échouait sur `next/font`
**avant d'avoir compilé une seule ligne**. Trois agents successifs ont rapporté « build propre,
il ne s'arrête que sur les 2 polices Google ». Personne ne mentait : la phrase décrivait
exactement ce qui s'affichait.

**La règle : une vérification qui s'interrompt avant son objet ne rend pas un résultat partiel,
elle rend un résultat VIDE, et un résultat vide se lit spontanément comme « rien à signaler ».**
Le test à se poser sur tout garde-fou : *est-ce que je l'ai déjà vu échouer pour la bonne
raison ?* S'il n'a jamais été mis à l'épreuve en lui donnant le défaut qu'il est censé attraper,
son vert ne vaut rien.

**Signe d'alerte concret :** une erreur récurrente qu'on a appris à qualifier d'« attendue » et à
sauter mentalement (ici, la ligne sur les polices). C'est précisément là que la vérification
s'arrête, donc l'endroit d'où plus rien n'est vérifié.
