# <Nom du projet> : contexte projet (lu à chaque session ouverte dans ce dossier)

> Chargé EN PLUS du `~/.claude/CLAUDE.md` global : ne recopie pas les règles globales ici.
> Les règles de ce fichier priment pour CE projet (si la politique de push diffère du global,
> le dire en toutes lettres). Plafond : 150 lignes. L'historique jour par jour va dans `docs/`.
> Une règle fixe du projet va ICI, avec son « Pourquoi », jamais en mémoire : la mémoire n'est
> pas vue depuis ce dépôt.

## Identité
- **C'est quoi** : <une phrase : ce que fait le produit, pour qui>. Pas de plaquette marketing.
- **Public ou interne** : <public, indexé / interne : noindex + protection>.
- **URL** : prod <https://domaine>, preview <https://...>, admin <https://... ou « aucun »>.
- **Dépôt** : `<org/repo>`, dossier local `<chemin absolu>`, branche de prod `<main>`.
- **Hébergeur** : <Vercel projet X / Render service Y / Cloudflare Worker Z / serveur maison>.
- **Base** : <aucune / Supabase `nom`, région / Postgres chez ...>. 🔴 <base de PROD en lecture
  seule, et ce que ça casse si on écrit dedans>.
- **Comptes et services** : domaine <...>, e-mails <...>, OAuth <...>, mesure <...>.
- **Coût mensuel** : <total> = <ligne par ligne>. Tout ajout au-delà du seuil du global : accord
  avant.
- **Qui touche à quoi** : <Prénom = rôle, périmètre>. ⚠️ <ce qu'on ne touche pas sans lui>.

## Stack et commandes
- <Framework, langage, ORM, UI>. Versions : celles de `package.json`, jamais recopiées ici.
- Typecheck : `<npx tsc --noEmit -p ...>` (⚠️ <piège : le script `lint` est cassé, la commande
  doit tourner depuis tel dossier...>). Sur une machine partagée : via `lourd.sh`.
- Tests : `<commande>`. Ce qui doit être vert avant de pousser : <liés au diff / suite complète>.
- Build : `<commande>`. <Ce que seul un vrai build attrape dans ce projet.>
- Lancer en local : <commande>, ou « impossible sous le bac à sable, vérifier sur la preview ».
- Migrations : <dossier, convention de nom, qui les applique, RLS sur chaque table>. 🔴 Un
  fichier SQL dans le dépôt n'est pas une migration appliquée : appliquer ET vérifier en base.
- Déploiement : <au push / par hook toutes les N minutes / à la main>. Preuve du déploiement :
  <statut READY sur le SHA / « Live » / version du Worker>.
- Compte de test pour `verifier-en-vrai` : <où est l'identifiant ; jamais le mot de passe ici>.

## Conventions
- **Politique de push** : <direct `main` = prod / staging seulement, `main` sur « go prod »
  explicite / branche + PR / jamais sans feu vert>. <Cette ligne prime sur le global.>
- **Auteur des commits** : <nom et e-mail attendus par l'hébergeur, s'il bloque les autres>.
- **Langue** : <chat en ... ; code, commits et texte produit en ...>.
- **Design** : <librairie, thème, accent propre à ce projet, composants imposés (un seul date
  picker, un seul modal)>. Détail : `DESIGN.md` s'il existe.
- **Definition of done** : <tests verts ; capture dans un vrai navigateur pour toute UI ; ce
  fichier à jour si un geste d'exploitation change ; récap>.

## Garde-fous propres à ce projet
> Format : la règle, puis « Pourquoi » en une ligne (une règle sans son pourquoi saute au premier
> qui la trouve gênante). Un 🔴 = non négociable, ça coûte de l'argent ou ouvre un accès.
- 🔴 <Règle>. **Pourquoi :** <l'incident qui l'a créée, daté, en une ligne.>
- ⚠️ <Piège de build ou de déploiement déjà payé une fois, et sa parade.>

## État / avancement (5 lignes maximum, datées ; l'ancien part dans `docs/`)
- <AAAA-MM-JJ> : <ce qui est en ligne, ce qui reste, la prochaine étape>.

## 🔴 ouverts (un par ligne, toujours qui + quand ; une ligne refermée est SUPPRIMÉE, pas barrée)
- 🔴 <quoi> · **qui** : <Prénom / Claude> · **quand** : <AAAA-MM-JJ> · **preuve attendue** : <...>.

## Pièges du projet
> Seulement ce qui a déjà fait perdre du temps ICI, un par ligne, avec sa parade.
- <symptôme> → <parade>.

## Où est le contexte
- `docs/` : plans, audits, historique daté. `README.md` : 5 lignes qui renvoient ici.
- Mémoire : fiche `<slug>-...` (elle pointe ici, elle ne recopie pas l'état).
- Secrets : les NOMS seulement, jamais les valeurs : trousseau `<fournisseur>-<projet>-<usage>`,
  variables de l'hébergeur.
