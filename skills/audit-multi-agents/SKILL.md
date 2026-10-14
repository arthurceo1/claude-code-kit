---
name: audit-multi-agents
description: "Mener un audit ou un check-up large (produit, dossier, infra, coûts, sécurité, données) en 3 à 6 angles confiés en parallèle à des sous-agents general-purpose en lecture seule qui écrivent chacun leur rapport sur disque, puis contre-vérification des points critiques, synthèse par un advisor à contexte neuf (modèle fort), un seul livrable daté dans docs/AAAA-MM/ fusionné avec l'audit précédent du même sujet, une fiche mémoire, 5 constats et des décisions numérotées pour l'utilisateur. À lancer dès que l'utilisateur dit « audit », « check-up », « de A à Z », « passe tout en revue », « lance des agents en parallèle ». PAS pour relire un diff avant push (voir pousser-en-prod)."
---

# Audit multi-agents : des angles en parallèle, un seul livrable

Pourquoi : 24 audits multi-agents en un mois, 154 rapports empilés à la racine d'un dossier, et
5 agents lancés en `Explore` qui n'ont pas pu écrire leur rapport (130 Ko réémis à la main).

## 1. Cadrer avant de lancer
- La question en une phrase, le périmètre (repos, dossiers, bases, période) et le hors champ.
- L'audit précédent du même sujet : `grep -i <mot> <dossier docs>/INDEX.md`, les fiches mémoire
  `audit-*`. En relever les constats encore ouverts (pas tout le fichier) : ils sont à revérifier.
- Personne d'autre dessus (si ton lanceur liste les sessions ouvertes).
- 3 à 6 angles qui ne se recouvrent pas. Au-delà : deux audits.

## 2. Lancer les angles, tous dans le même message
- `subagent_type: "general-purpose"`, jamais `Explore` : il n'a aucun outil d'écriture et ne peut
  pas poser son rapport.
- Modèle écrit dans chaque appel (sans lui, c'est le modèle intermédiaire) : `sonnet` par défaut,
  `opus` pour l'angle sécurité ou un angle de jugement.
- Rapports dans `<dossier docs>/AAAA-MM/<sujet>-AAAA-MM-JJ/<angle>.md`.
- À coller tel quel dans chaque prompt, après la question, le périmètre et l'angle :
  > Lecture seule. Tu n'écris QUE dans <chemin du rapport>, avec l'outil Write, section par
  > section au fil de l'eau : une coupure ne doit pas tout perdre. Jamais `git stash`,
  > `stash pop`, `reset --hard`, `clean`, `checkout`, commit ni push ; pour lire une autre
  > branche : `git show <ref>:<fichier>`. Aucune écriture en base, en prod ni dans un repo.
  > Sorties Bash coupées (`head`, `tail`, `-q`). Pas de `tsc`, de build ni de suite de tests hors
  > de la file d'attente des jobs lourds. Chaque constat porte sa preuve : fichier:ligne, commande
  > et sortie, requête ou URL. Sépare le constaté du supposé. Rends un résumé de 40 lignes au plus.
- Gros volume (logs, milliers de fichiers, grosses tables) : un échantillon d'abord.

## 3. Contre-vérifier les points critiques
- Critique = argent, sécurité ou secret, mineurs, perte de données, prod en panne.
- Chacun est rejoué avant la synthèse (sa commande, sa ligne, sa requête), par toi ou par un 2e
  agent : confirmé, corrigé ou retiré.
- Le parent ne lit que les résumés et ces preuves, jamais les rapports entiers.
- Agent coupé : reprendre son rapport là où il s'arrête (skill `reprise-apres-coupure`), pas
  tout l'angle.

## 4. Synthèse par un advisor à contexte neuf
- Un sous-agent `general-purpose` avec `model: "opus"`, qui lit lui-même sur disque les rapports
  et l'audit précédent (les chemins dans le prompt, pas le contenu).
- Il écrit le livrable unique `<dossier docs>/AAAA-MM/<sujet>-AAAA-MM-JJ.md` : la réponse en 3
  lignes ; les constats par gravité, chacun avec sa preuve et le lien vers son rapport d'angle ;
  le statut de chaque constat de l'audit précédent (résolu, toujours ouvert, nouveau) ; les
  décisions numérotées avec options et reco.
- L'audit précédent reçoit en première ligne « Remplacé par <chemin du nouveau> », sans être
  supprimé : des fiches mémoire pointent vers lui.

## 5. Mémoire
- Une seule fiche par sujet : mettre à jour celle de l'audit précédent (décisions, points
  critiques, chemin du livrable), sinon en créer une, avec sa ligne dans `MEMORY.md`.

## 6. Message à l'utilisateur
- La réponse en 1 à 2 lignes, puis les 5 constats qui comptent (une ligne chacun), puis le
  chemin du livrable.
- En fin de message, sous le titre « Décisions pour toi » : décisions numérotées, options en
  puces, ta reco en une ligne.
- Les correctifs viennent après, sur décision de l'utilisateur, par `pousser-en-prod`.

## À quoi ressemble « fait »
- Un rapport par angle dans `docs/AAAA-MM/<sujet>-AAAA-MM-JJ/`, un seul livrable daté à côté,
  rien à la racine.
- Chaque constat a sa preuve ; chaque point critique est confirmé, corrigé ou retiré.
- Audit précédent fusionné (statut de ses constats) et marqué « Remplacé par » ; fiche mémoire à
  jour.
- Message : 5 constats, puis décisions numérotées en fin.
