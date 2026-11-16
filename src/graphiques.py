"""Graphiques enregistrés avec savefig (ch. 13) : exploration et évaluation.

On utilise matplotlib.figure.Figure directement (sans pyplot) : aucune fenêtre
n'est ouverte, ce qui fonctionne aussi dans la CI.
"""
import os

import numpy as np
import pandas as pd
from matplotlib.figure import Figure

from donnees import COLONNE_CIBLE


def graphique_exploration(df: pd.DataFrame, chemin: str) -> None:
    """Enregistre deux graphiques d'exploration dans `chemin` (PNG).

    À gauche : distribution de la cible. À droite : cible selon les notes
    antérieures, la caractéristique la plus liée à la performance.
    Échoue : KeyError si une colonne attendue est absente.
    """
    figure = Figure(figsize=(11, 4.5))
    gauche, droite = figure.subplots(1, 2)

    gauche.hist(df[COLONNE_CIBLE], bins=30, color="tab:blue", edgecolor="white")
    gauche.set_title("Distribution de l'indice de performance")
    gauche.set_xlabel("Indice de performance")
    gauche.set_ylabel("Nombre d'étudiants")

    nuage = droite.scatter(df["Previous Scores"], df[COLONNE_CIBLE],
                           c=df["Hours Studied"], cmap="viridis", s=6, alpha=0.6)
    droite.set_title("Indice selon les notes antérieures")
    droite.set_xlabel("Notes antérieures (Previous Scores)")
    droite.set_ylabel("Indice de performance")
    figure.colorbar(nuage, ax=droite, label="Heures d'étude par jour")

    figure.tight_layout()
    _enregistrer(figure, chemin)


def graphique_predit_reel(y_reel: np.ndarray, y_predit: np.ndarray, chemin: str) -> None:
    """Enregistre le graphique « prédit contre réel » dans `chemin` (PNG).

    Les points proches de la diagonale sont bien prédits.
    Échoue : ValueError si les deux tableaux n'ont pas la même longueur.
    """
    y_reel = np.asarray(y_reel)
    y_predit = np.asarray(y_predit)
    if y_reel.shape != y_predit.shape:
        raise ValueError("y_reel et y_predit doivent avoir la même longueur.")

    figure = Figure(figsize=(5.5, 5))
    axes = figure.subplots()
    axes.scatter(y_reel, y_predit, s=6, alpha=0.5, label="Étudiants du test")
    bornes = [min(y_reel.min(), y_predit.min()), max(y_reel.max(), y_predit.max())]
    axes.plot(bornes, bornes, color="red", label="Prédiction parfaite")
    axes.set_title("Indice prédit contre indice réel (ensemble de test)")
    axes.set_xlabel("Indice réel")
    axes.set_ylabel("Indice prédit")
    axes.legend()
    figure.tight_layout()
    _enregistrer(figure, chemin)


def _enregistrer(figure: Figure, chemin: str) -> None:
    """Crée le dossier au besoin puis enregistre la figure (savefig)."""
    dossier = os.path.dirname(chemin)
    if dossier:
        os.makedirs(dossier, exist_ok=True)
    figure.savefig(chemin, dpi=120)
