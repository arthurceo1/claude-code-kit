---
name: verifier-en-vrai
description: "Vérifier un changement visible dans un vrai navigateur avant de dire « fini » : Chromium sans interface, preview ou prod, compte de test du projet, état modifié déclenché, 0 erreur console, 0 réponse 4xx/5xx, mobile 412 px sans débordement, capture jointe. À lancer dès que l'utilisateur dit « vérifie en vrai », « regarde la page », « teste en vrai », avant tout « fini » ou « c'est en ligne » sur un changement visible (page, écran, composant, e-mail HTML, PDF), et à l'étape 5 de pousser-en-prod."
---

# Vérifier en vrai : regarder la page, pas le code

Pourquoi : des lots testés au jsdom et relus sont partis en ligne avec des boutons superposés,
trouvés à l'œil en 10 minutes. jsdom ne calcule pas la mise en page ; un test vert n'est pas une
page qui s'affiche.

## 1. Cible
- Preview du commit (Vercel READY) ou la prod une fois le vrai déploiement constaté
  (`pousser-en-prod`, étape 4).
- Un serveur de dev sous le bac à sable est souvent inutilisable (ports, limites de fichiers) :
  préférer la preview ; pour un fichier local (HTML, build statique), un petit serveur Node sur
  `127.0.0.1` lancé et arrêté dans le script.

## 2. Navigateur
- `playwright-core` + `chromium-headless-shell` installés UNE fois, dans un dossier durable (le
  dossier temporaire se vide tout seul) :
  `npm i --prefix <dossier durable> playwright-core` puis
  `node <dossier durable>/node_modules/playwright-core/cli.js install chromium-headless-shell`.
  Toujours `--prefix` : sans lui, npm remonte au premier `node_modules` qu'il trouve et
  désinstalle ce qui ne figure pas dans son `package.json` (vécu).
- Flags testés sous un bac à sable macOS :
  `['--no-sandbox', '--disable-gpu', '--single-process', '--no-zygote', '--disable-software-rasterizer', '--disable-gpu-rasterization', '--disable-accelerated-2d-canvas']`
  (les 3 derniers évitent un plantage à l'initialisation GL).
- Derrière un proxy : le passer à `chromium.launch({ proxy })` depuis `HTTPS_PROXY` (sinon
  `ERR_NAME_NOT_RESOLVED`).
- Avec `--single-process` : jamais `browser.newContext()` ; un `launch` par largeur,
  `browser.newPage({ viewport })` ; fermer la page ferme le navigateur.
- Sortie du script dans un fichier, lue en filtrant le bruit système sans conséquence.

## 3. Compte de test
- Celui du projet, noté dans son `CLAUDE.md` (où trouver l'identifiant, jamais le mot de passe en
  clair). Jamais le compte de l'utilisateur ni celui d'un vrai client.
- Pas de compte noté : vérifier la partie publique, puis une question à l'utilisateur, et
  l'inscrire dans le `CLAUDE.md` du projet.
- Ce que le test crée en prod est supprimé à la fin, lignes laissées comprises (supprimer un
  compte ne retire pas un réglage posé sur son rôle).

## 4. Déclencher l'état modifié
- Aller jusqu'à l'écran exact que le diff change (clic, formulaire, filtre, cas vide, cas
  d'erreur, langue), pas seulement la page d'accueil.

## 5. Contrôles, à 412 px puis à 1440 px
- 0 erreur console : `page.on('console')` de type `error`, et `page.on('pageerror')`.
- 0 réponse 4xx/5xx : `page.on('response')` ; un 401 ou un 404 attendu se justifie en une ligne.
- 0 débordement à 412 px : `document.documentElement.scrollWidth - innerWidth` vaut 0 ; aucun
  bouton coupé, superposé ou masqué.
- Capture PNG de l'état modifié à chaque largeur, regardée (outil Read), une image à la fois.

## 6. Rendre compte
- Les chemins des captures et les trois chiffres : erreurs console, réponses 4xx/5xx,
  débordement.
- Ce qui n'a pas pu être vu : « non vérifiable parce que … », avec l'URL exacte et quoi regarder.

## À quoi ressemble « fait »
- Capture de l'état modifié à 412 et 1440 px, regardée.
- 0 erreur console, 0 réponse 4xx/5xx, 0 débordement à 412 px.
- Ou la phrase « non vérifiable parce que … » avec l'URL et quoi regarder.
