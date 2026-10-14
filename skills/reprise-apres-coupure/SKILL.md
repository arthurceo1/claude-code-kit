---
name: reprise-apres-coupure
description: "Reprendre un travail interrompu sans rien refaire ni rien perdre, quand une session ou des sous-agents ont été coupés (limite de compte, changement de compte ou de machine, machine figée ou redémarrée) : journal et mémoire du chantier, inventaire git et disque, dernière étape commitée de chaque agent, vérification qu'aucune autre session ne fait déjà le travail, relance de ce qui manque seulement avec commit après chaque étape, bilan repris / fait / perdu. À lancer dès que l'utilisateur dit « reprends », « continue », « on a été coupés », « t'en étais où »."
---

# Reprise après coupure : l'état réel d'abord, la relance ensuite

Pourquoi : 94 coupures en cinq semaines, dont 50 relances. Un chantier entier a été refait en
doublon d'une autre session ; une autre fois, l'historique visible après un changement de compte
avait 13 heures de retard sur le disque.

## 1. Ce qui était en cours
- `head -n 15 ~/.claude/session-log.md` : les entrées récentes sont EN HAUT (un `tail` lit les
  plus anciennes). Pour le chantier : `grep -m 8 -i "<projet ou sujet>" ~/.claude/session-log.md`.
- La fiche mémoire du chantier (lien dans `MEMORY.md`) et sa « prochaine étape ».
- Après un changement de compte ou de machine, l'historique visible peut être périmé. Si le
  disque est en avance, lire le transcript le plus gros de la session
  (`find ~/.claude/projects -name '<session-id>.jsonl' -exec ls -lS {} + | head -3`) et en
  extraire, par un petit script, les messages de l'utilisateur postérieurs au dernier horodatage
  visible.

## 2. Inventaire, en lecture seule
Pour chaque repo du chantier :
- `git worktree list` ; `git branch -vv | head -30` (commits non poussés : `ahead`) ;
  `git log --oneline -10 <branche du chantier>`.
- `git status --short | head -30` dans chaque worktree du chantier.
- Rapports et sorties partiels : `ls -lt` du dossier cité par le journal ou la fiche.
- Ce qui a été poussé est-il en ligne (statut du déploiement) ?
- Jamais `git stash`, `stash pop`, `reset --hard` ni `clean` pour y voir clair : ces commandes
  touchent le travail des autres sessions.
- Worktree ou fichiers dans le dossier temporaire : il se vide tout seul en quelques jours ; ce
  qui n'y était ni commité ni copié ailleurs est peut-être perdu.

## 3. Personne d'autre dessus
- Si ton lanceur liste les sessions ouvertes : regarder celles du même projet ou sujet.
- Une autre session avance sur ce chantier : ne rien toucher, le dire à l'utilisateur.
- Worktree modifié récemment sans session connue : le laisser, demander.

## 4. Où s'est arrêté chaque agent coupé
- Sa dernière étape = son dernier commit, ou la dernière section écrite de son rapport. Ce qu'il
  a annoncé sans l'écrire est perdu.
- Ses fichiers modifiés non commités : les relire ; s'ils tiennent, les commiter (tests et
  typecheck refaits) ; sinon les mettre de côté par un commit sur une branche jetable, jamais par
  stash.

## 5. Relancer seulement ce qui manque
- Agent coupé dans cette session (nom ou identifiant dans l'historique) : le reprendre par
  message depuis son transcript, contexte intact. Sinon un agent neuf (`general-purpose` s'il
  doit écrire un fichier).
- Dans chaque prompt de relance : ce qui est déjà fait (commits, sections), ce qui reste,
  « commit après chaque étape » (ou « écris ton rapport section par section »), et « jamais de
  git stash ».
- Coupures en série par limite de compte : moins d'agents à la fois, morceaux plus petits.
- Ce qui doit partir en prod repart par `pousser-en-prod` : une revue faite avant la coupure ne
  couvre que le diff qu'elle a lu.

## 6. Bilan
- À l'utilisateur, trois lignes : repris (en cours), fait (avec commit ou fichier), perdu (et
  s'il faut le refaire).
- Le même bilan dans la fiche mémoire du chantier et dans l'entrée du journal.

## À quoi ressemble « fait »
- Liste repris / fait / perdu écrite, chaque « fait » avec son commit ou son fichier.
- Rien de commité ou d'écrit n'a été refait ; aucun doublon avec une autre session.
- Chaque agent relancé a reçu « commit après chaque étape ».
