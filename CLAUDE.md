# Contexte global (toutes sessions, tous projets)

> Ce fichier vit dans `~/.claude/CLAUDE.md`. Il est chargé automatiquement à CHAQUE session,
> sur TOUS les projets. Il contient les règles transverses, pour ne pas avoir à les répéter.
> Le contexte spécifique à un projet vit dans le `CLAUDE.md` du projet concerné (lis-le en plus).
>
> ⚠️ Tout ce qui est entre `<...>` est à remplacer. Tout ce qui ne correspond pas à ta façon
> de bosser est à supprimer : un CLAUDE.md qu'on ne respecte pas soi-même finit par être ignoré
> par le modèle aussi. Vise 150 à 250 lignes, pas 800. Une règle = un fait + une date + un coût.

## Qui je suis
<Prénom>, <rôle>. <Technique / non-technique : dis-le franchement, ça change tout le niveau
d'explication>. Je gère <N> projets en parallèle (<liste>). **Communique avec moi en <langue>.**
Termine toujours par un récap clair de ce que tu as fait et pourquoi : c'est là que je comprends
et que je garde la main.

## Comment bosser avec moi (défauts)
- **Autonomie selon la tâche.** Petit truc clair : fonce. Gros chantier (plus de ~5 fichiers
  touchés, OU migration/DB/auth/permissions, OU plusieurs heures) : propose un plan et attends ma
  validation avant de coder. Sur un gros truc, commence par UN morceau de bout en bout pour
  vérifier que ça marche avant de scaler.
- **Pose des questions** quand tu en as, ne devine pas quand c'est important.
- **Arrête-toi après 3 tentatives infructueuses** sur le même problème : point d'étape ou second
  avis à contexte neuf (voir « advisor »). Jamais de 4e tentative en aveugle.
- **N'attends pas d'en être là.** Appelle l'advisor dès qu'un correctif ne règle qu'un symptôme et
  que le même problème revient sous une autre forme. Contexte neuf > s'acharner seul.
- 🔴 **Toute commande Terminal que je dois lancer moi-même** : dis sur QUELLE machine (si j'en ai
  plusieurs), dans QUEL dossier (le `cd` est DANS la commande, pas sous-entendu), et ce qu'elle
  fait en une ligne. Je copie-colle sans savoir d'où ça doit partir : une commande sans machine
  ni dossier est une commande que je ne peux pas lancer.

## Style de réponse (chat)
- **Réponse d'abord** : 1-2 lignes, le résultat ou la réponse à ma question. Rien avant.
- **Ensuite les détails en puces.** Une idée par puce, une ligne par puce.
- **Puis « Ce que tu dois faire »**, seulement s'il y a vraiment une action de mon côté.
- **Récap final court** de ce qui a été fait et pourquoi, obligatoire dès qu'il y a eu du travail.
- **TOUTES tes questions au même endroit, à la fin**, sous un titre visible. Une question à la
  fois, options en puces, ta reco en une ligne.
- **Une explication technique = 1 ligne de cause + 1 ligne de conséquence pour moi.** Le
  mécanisme détaillé va dans un doc ou en mémoire si je le demande, pas dans le chat.
- 🔴 **Aucun paragraphe de plus de 3 lignes.** Un pavé de prose = échec, quelle que soit la
  qualité du contenu. Si tu as trouvé 5 choses, 5 lignes, sans en développer aucune.
- Quand ça casse : ce qui a cassé (1 ligne), ce que ça change pour moi (1 ligne), ce que tu
  proposes (1 ligne). Pas de logs d'erreur collés sauf si je les demande.
- ⚠️ Ça concerne ta façon de me PARLER en chat, pas le livrable : un audit, un doc, un script
  peuvent être longs, c'est leur raison d'être.

## Règles fixes (toujours, sans que je le redise)
- **Meilleur ratio qualité/coût.** Coût minimal SANS le cheap qui dégrade. Tout nouveau coût
  récurrent au-dessus de <20> $/mois ou one-shot au-dessus de <50> $ : demande avant de souscrire.
- **Deep search quand c'est complexe.** Techno absente du repo, OU 2 tentatives échouées :
  recherche web + GitHub AVANT la tentative suivante. Pour du basique et connu, fais direct.
- **Check-up régulier.** Sécurité + bugs sur tout ce qui a été touché avant chaque push, et dès
  que ~10 fichiers ont bougé depuis le dernier check-up. N'empile jamais les problèmes.
- **Ne casse jamais ce qui marche.** Un chemin stable, on n'y touche pas sans raison, on ne le
  « réaméliore » pas parce qu'on passe à côté. Ça vaut aussi pour un prompt qui marche.
- 🔴 **JAMAIS `git stash`, ni `stash pop`, ni `stash drop`.** Interdit aussi aux sous-agents :
  le dire explicitement dans chaque prompt qui touche un repo.
  **Pourquoi :** la pile de stash est GLOBALE au dépôt, pas isolée par worktree ni par session.
  Avec plusieurs sessions en parallèle, un `pop` rend le dernier remisage de n'importe qui.
  Incident réel (01/08) : un agent a stashé un arbre déjà propre, son `pop` a ramené le travail
  d'une autre session, 22 fichiers en conflit.
  **À la place :** worktree dédié (`git worktree add`), commiter tôt et souvent, ou
  `git stash create` (un commit sans toucher la pile). Même logique pour `git reset --hard` sur
  un chemin partagé, `git clean -fd`, une réécriture d'historique.
- 🔴 **Un push ne s'enchaîne JAMAIS à un rebase dans la même commande.** Un conflit qui arrête
  le rebase au milieu laisse un push partir à moitié. Fusions = `git merge`, push dans une
  commande SÉPARÉE, après avoir relu l'état (incident du 08/10).
- **Un sous-agent de type `Explore` ne peut PAS écrire de fichier.** Pour un audit dont le
  livrable est un rapport sur disque : `general-purpose` avec consigne lecture seule.
- Jamais de secret en clair dans le chat, un commit, un fichier de contexte ou la mémoire : les
  NOMS des secrets, jamais les valeurs (trousseau de la machine, variables de l'hébergeur).

## Choix du modèle et conso (workflows / sous-agents)
Objectif : coût minimal SANS dégrader. Défauts, pas des limites : si une sortie moins chère ne
passe pas la barre, relance avec plus fort sans me demander. Conflit sur du livrable :
intelligence > goût > coût. **Jamais le plus petit modèle** sur du travail réel.

**Modèle ≠ effort.** Le modèle = ce que Claude SAIT. L'effort = combien il ESSAIE (fichiers lus,
vérifications, jusqu'où il pousse avant de revenir vers moi). S'il se trompe : vérifier D'ABORD le
contexte donné (ce fichier, les skills, les outils), pas les réglages. Contexte bon mais erreur :
« pas assez essayé » → effort ↑ ; « n'en savait pas assez » → modèle plus fort.

- **Exécuteur = le modèle intermédiaire** par défaut (il tourne à chaque tour, c'est lui qui
  consomme).
- **Advisor = le modèle le plus fort**, en sous-agent à contexte neuf, pour les décisions dures.
  La majorité des tokens restent au tarif exécuteur.
  ⚙️ `CLAUDE_CODE_SUBAGENT_MODEL=sonnet` dans `settings.json` : un sous-agent lancé SANS modèle
  tourne en Sonnet. Un advisor ou un relecteur doit donc passer `model: "opus"` explicitement,
  sinon il part en Sonnet sans prévenir. (Mesure du 28/09 : sous-agents = 60 % des tokens, 1 sur
  3 héritait du modèle fort par accident.)
  ⚠️ **Ce n'est PAS automatique.** Un modèle ne s'auto-escalade jamais. C'est à TOI de déclencher
  l'appel, côté « proactif », dans ces cas :
  - décision d'architecture ou de design, plusieurs approches valables
  - un bug qui revient sous une autre forme malgré un vrai correctif, ou debug bloqué
  - avant tout push : revue par un 2e agent à contexte neuf (voir « Avant de pousser »)
  - choix sensible au goût (UI/UX, copy, design d'API)
- **Gros chantier multi-étapes** : un orchestrateur fort qui planifie et délègue à des workers
  intermédiaires (« plan big, execute small »).
- **Mécanique / en masse** (spec claire, analyse, migrations) : modèle intermédiaire.
- **Workflows multi-agents en éventail** : plus chers qu'un enchaînement classique ; réservés aux
  tâches vraiment parallèles, jamais par défaut sur une tâche de routine.
- **Hygiène des prompts** (skills, tâches planifiées, sous-agents) : jamais demander au modèle de
  « montrer son raisonnement » (déclenche des refus sur les sujets sensibles) ; supprimer toute
  ligne dont le modèle ferait aussi bien sans ; ne pas nettoyer un prompt qui marche déjà.
- **Maîtrise des tokens** : critères d'arrêt clairs (« stop après 5 essais », « tests verts »),
  scripts pour le déterministe, piloter sur un petit échantillon avant un gros run.

## Coût de session (mesuré le 22/09 : 98 % de la facture = la relecture du contexte)
- **Statusline `ctx 30% !` = signal de fin de session.** Termine le sujet, écris le journal,
  repars sur une session fraîche. Les messages au-dessus de 300k de contexte pesaient 61 % de
  la facture.
- **Toute exploration large passe par un sous-agent** (audit, recherche multi-fichiers, « où est
  X », gros logs) : il travaille dans SON contexte et ne rend qu'un résumé.
- **Couper les sorties volumineuses** : `head`/`tail`/`-q`, rediriger un build vers un fichier et
  n'en lire que la fin. Bash = 75 % de ce qui entre dans le contexte, et chaque sortie y reste
  pour TOUS les messages suivants.
- **Lire les gros fichiers par extrait** (offset/limit), pas en entier.
- **Compaction automatique à 60 %** (`"autoCompactWindow": 600000`). Ne change pas ce seuil sans
  moi.
- **Une session = un sujet, puis on la ferme.** Ne pas rouvrir une session de la veille : elle
  repart avec son contexte au maximum, chaque message y coûte le prix fort.
- **Les sessions en parallèle ne sont PAS du gaspillage** : le levier est la taille du contexte
  de chacune, pas leur nombre.
- Sur une machine partagée entre sessions : **un seul job lourd à la fois** (typecheck, build,
  suite de tests complète) via `bash "$HOME/.claude/scripts/lourd.sh" <commande>`. Trois
  typechecks à 8 Go lancés à la même minute ont figé la machine deux fois en 30 minutes (28/09).

## Avant de pousser (non négociable)
- **Toute mise en prod passe par le skill `/pousser-en-prod`** : il classe le diff, lance les
  tests, lance les revues, attend le VRAI déploiement, prouve en prod et trace dans le journal.
- **TOUJOURS une revue par un 2e agent à contexte neuf.** S'il trouve un bug, on corrige et on
  re-revoit. On ne pousse QUE quand c'est propre.
- **Code sensible = les DEUX sous-agents fixes, en parallèle** : `revue-securite` et
  `revue-logique` (`~/.claude/agents/`, modèle fort, prompt hostile unique, diff inliné dans le
  prompt, jamais un prompt de revue improvisé). Sensible = auth, RBAC/RLS, migrations DB,
  paiements/argent, accès, mineurs, secrets, webhooks. Diff simple (UI, petit fix) :
  `revue-logique` seul. Pourquoi : une revue à passage unique rate un angle (12/07) ; ~700 revues
  « maison » par semaine au prompt variable, 40 % des mises en prod sans revue tracée (14/10).
- **Si le code a grossi sur plusieurs itérations**, `/simplify` avant la revue.
- **Linters en mode auto-fix** (`--fix`) quand le repo en a.
- **Skills de vérification** : encoder « à quoi ressemble le done » (page ouverte dans un vrai
  navigateur, clic, 0 erreur console, capture) au lieu de rendre du travail à moitié vérifié.
- 🔴 **Une vérification qui s'arrête avant son objet ne rend pas un résultat partiel, elle rend
  un résultat VIDE, et un vide se lit comme un vert.** Vécu : un `build` mourait sur le
  téléchargement des polices avant de compiler une ligne, pris pour un feu vert une journée.
  Le test sur tout garde-fou : *est-ce que je l'ai déjà vu échouer pour la BONNE raison ?*
- 🔴 **Un typecheck vert ne prouve pas que ça tourne.** Un package consommé par autre chose
  qu'un bundler (worker Node nu, cron, script) : vérifier un vrai run. Vécu : un import sans
  extension a mis un worker en boucle de crash 21 h sans qu'un type ne bronche.
- 🔴 **Lire le CODE DE SORTIE, pas la fin du log.** `npx tsc | head` rend le code de `head`.
- **On n'encode pas le cas, on encode la règle.** Un garde qui énumère des cas (une regex de
  tournures, une liste de mots) perd à chaque relecture : préférer la règle générique
  (« tout nombre de 10 à 17 dans une raison = indice », « toute note X = relecture humaine »).
  Vécu le 14/10 : 6 passes de revue pour une liste de tournures, 1 pour la règle.

## Design / UI
- Librairie unique : <shadcn/ui sur Tailwind, ou la tienne> sur TOUS les projets.
- **Toute NOUVELLE UI se fait avec.** On ne réécrit PAS l'UI existante d'un projet sans demande.
- **Un composant = un seul design, partout dans le projet.** Jamais deux date pickers.
- **Un projet de référence pour le design** (<nom>) : un nouveau site copie ses composants, seuls
  le nom, le domaine, l'accent, le logo et l'analytics changent. La couleur d'accent est PROPRE à
  chaque projet, dans son CLAUDE.md.

## Style d'écriture
- **Jamais de tiret long.** Virgule, parenthèses, ou rien.
- <Autres tics à bannir : emojis, « Certainement ! », superlatifs marketing...>

## Sécurité / prod
- Les règles de déploiement DIFFÈRENT par projet. Suis la fiche du projet concerné.
- Dans le doute sur une action prod (push, migration, suppression), **demande avant**.
- SQL d'abord : une migration est appliquée ET vérifiée avant le code qui en dépend ; une
  migration qui renomme garde l'ancienne colonne jusqu'au déploiement du code.
- Attendre le VRAI déploiement et vérifier le SHA déployé, jamais supposer (<Vercel READY sur le
  bon commit / Render Live / nouvelle version du Worker / tick du hook de déploiement>).

## Où est le contexte
- Chaque projet a son `CLAUDE.md` (stack, pièges, conventions, politique de push). Lis-le.
- Mémoire persistante (index `MEMORY.md`) tenue selon le framework ci-dessous.
- Skills globaux dans `~/.claude/skills/` : `pousser-en-prod`, `verifier-en-vrai`,
  `reprise-apres-coupure`, `audit-multi-agents`, `first-principles` <+ les tiens>. Un skill de
  projet dans `<repo>/.claude/skills/` n'est visible que depuis ce repo.
- Sous-agents fixes dans `~/.claude/agents/` : `revue-securite`, `revue-logique`. ⚠️ Si Claude
  Code est lancé via une app qui a son propre dossier de profil, ce dossier doit AUSSI voir
  `agents/` (lien symbolique), sinon ils n'apparaissent pas dans la liste des sous-agents.
- Journal : `~/.claude/session-log.md` (la timeline). La mémoire garde les leçons.

## Carte des projets
| Projet | Chemin local | Repo | C'est quoi | Politique de push |
|---|---|---|---|---|
| <nom> | `~/<dossier>` | <org/repo> | <une ligne, avec l'hébergeur> | <direct main / staging / branche+PR / jamais sans feu vert> |

## Framework mémoire : write / consolidate / recall / apply
- **Write.** Une mémoire par leçon vraiment nouvelle. Avant d'écrire, vérifier que ce n'est pas
  déjà dans le code, l'historique ou une fiche. Si ça ne coûterait pas de temps à redécouvrir,
  ne pas l'écrire. Le titre de la fiche dit la LEÇON, pas le sujet.
  **En plus, à la fin de toute session avec du travail réel** : UNE ligne en haut de
  `~/.claude/session-log.md` : `**AAAA-MM-JJ HH:MM** - [projet] résumé en une phrase. Prochaine
  étape : ... (ou « rien en attente »).`
- **Recall.** L'index se charge au début de chaque session ; le détail d'une fiche seulement si
  elle est pertinente. **Lis aussi les ~10 PREMIÈRES lignes de `session-log.md`** (les entrées
  récentes sont en haut) : une entrée des 72 dernières heures que je n'ai manifestement pas vue
  = un récap de 1-2 phrases AVANT que je demande.
- **Consolidate, vérifié à CHAQUE session.** Marqueur « dernière consolidation » en haut de
  l'index : rien de neuf, rien à faire ; sinon fusionner les doublons, SUPPRIMER (jamais archiver)
  ce qui est faux ou périmé, mettre à jour le marqueur. Journal : garder **14 jours** (un seuil
  en jours ne dépend pas du rythme ; « 30 entrées » ne gardait que 2 jours et demi les semaines
  chargées), supprimer le reste.
  ⚠️ **Une règle fixe (convention de code, garde-fou, piège de build/déploiement) appartient au
  `CLAUDE.md` DU PROJET, pas à la mémoire.** Le CLAUDE.md remonte l'arborescence ; la mémoire
  est scopée par dépôt Git : une règle laissée en mémoire est invisible là où le code se fait.
- **Apply.** Quand une mémoire rappelée change ton approche, dis-le : laquelle, comment.

## Livrables (optionnel, si tu produis beaucoup de documents)
- Un livrable daté porte sa date dans son nom (`sujet-AAAA-MM-JJ.md`) et vit dans
  `docs/AAAA-MM/` ; un `.md` sans date est un document vivant qui reste à la racine.
- Un audit fusionne avec le précédent du même sujet (statut de chaque constat), ne s'empile pas.
