#!/usr/bin/env python3
"""Rappel de compaction pour toutes les sessions Claude Code (hook Stop).

Pourquoi (mesuré le 22/09/2026) :
  Avec la fenêtre de contexte à 1 million, la compaction automatique ne se
  déclenche plus qu'aux alentours de 950k, contre ~180k du temps de la fenêtre
  200k. Le garde-fou existe donc toujours, mais 5 fois plus haut. Résultat
  mesuré sur les sessions mesurées : 6 conversations tournaient entre 805k et
  986k avec ZÉRO compaction, chaque message y coûtant jusqu'à 19 fois le prix
  d'un message dans une session neuve (51k).

Ce que fait ce hook :
  À la FIN d'une réponse (événement Stop, jamais au milieu d'une action), il lit
  le contexte réellement consommé dans le transcript et affiche un rappel quand
  on franchit un palier. Il ne compacte rien tout seul, il ne bloque rien, et
  il n'injecte AUCUN texte dans le contexte (le message est affiché à l'écran,
  pas ajouté à la conversation) : son coût en tokens est donc nul.

Règle de l'utilisateur : compacter à la fin d'un sujet, jamais en plein milieu. Le hook
se contente donc de signaler ; c'est l'utilisateur qui juge si le sujet est terminé.

Défensif par construction : toute anomalie (stdin vide, JSON illisible,
transcript absent) se termine par un exit 0 silencieux. Ce hook ne doit jamais
empêcher une réponse d'aboutir.
"""

import json
import os
import sys
import tempfile

# 60 % d'une fenêtre de 1M. Ajustable sans toucher au code.
SEUIL = int(os.environ.get("CONTEXT_GUARD_SEUIL", "600000"))
PALIER = 100_000  # on réalerte tous les 100k au-dessus du seuil


def contexte_actuel(transcript):
    """Dernier contexte connu du transcript, en tokens. 0 si illisible."""
    try:
        taille = os.path.getsize(transcript)
    except OSError:
        return 0
    # On ne lit que la fin du fichier : un transcript peut peser des dizaines de Mo.
    debut = max(0, taille - 2_000_000)
    try:
        with open(transcript, "rb") as fh:
            fh.seek(debut)
            lignes = fh.read().decode("utf-8", "ignore").splitlines()
    except OSError:
        return 0

    for ligne in reversed(lignes):
        if '"usage"' not in ligne:
            continue
        try:
            usage = (json.loads(ligne).get("message") or {}).get("usage")
        except (ValueError, AttributeError):
            continue
        if not isinstance(usage, dict):
            continue
        total = (
            (usage.get("cache_read_input_tokens") or 0)
            + (usage.get("cache_creation_input_tokens") or 0)
            + (usage.get("input_tokens") or 0)
        )
        if total:
            return total
    return 0


def deja_signale(session_id, palier):
    """Vrai si ce palier a déjà été annoncé pour cette session."""
    if not session_id:
        return False
    marqueur = os.path.join(
        tempfile.gettempdir(), f"claude-ctx-guard-{session_id[:16]}"
    )
    try:
        with open(marqueur) as fh:
            if int(fh.read().strip() or 0) >= palier:
                return True
    except (OSError, ValueError):
        pass
    try:
        with open(marqueur, "w") as fh:
            fh.write(str(palier))
    except OSError:
        pass
    return False


def main():
    try:
        entree = json.load(sys.stdin)
    except (ValueError, OSError):
        return

    transcript = entree.get("transcript_path")
    if not transcript or not os.path.exists(transcript):
        return

    contexte = contexte_actuel(transcript)
    if contexte < SEUIL:
        return

    palier = (contexte // PALIER) * PALIER
    if deja_signale(entree.get("session_id", ""), palier):
        return

    pct = contexte * 100 // 1_000_000
    cout = max(1, contexte // 51_000)
    message = (
        f"⚠️  Contexte à {contexte // 1000}k ({pct} %). "
        f"Chaque message ici coûte environ {cout}× celui d'une session neuve. "
        f"Si ton sujet est terminé : /compact, ou ouvre une session fraîche."
    )

    # stderr s'affiche dans le terminal ; systemMessage s'affiche dans l'UI.
    # Aucun des deux n'entre dans le contexte de la conversation.
    print(message, file=sys.stderr)
    print(json.dumps({"systemMessage": message}))


if __name__ == "__main__":
    try:
        main()
    except Exception:  # un garde-fou ne doit jamais casser une session
        pass
    sys.exit(0)
