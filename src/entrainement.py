"""Entraîne le modèle UNE fois et le sauvegarde (avec ses métadonnées JSON).

Lancement : python src/entrainement.py
L'application (main.py) recharge ensuite le modèle sans le ré-entraîner.
"""
import os

from donnees import (CHEMIN_DONNEES, DOSSIER_FIGURES, DOSSIER_MODELES,
                     JeuDeDonnees, decrire_variables)
from graphiques import graphique_exploration, graphique_predit_reel
from modele import Modele


def entrainer_et_sauvegarder(chemin_donnees: str, dossier_modeles: str,
                             dossier_figures: str) -> dict:
    """Explore, entraîne, évalue puis sauvegarde le modèle.

    Reçoit : le CSV source, le dossier du modèle et celui des figures.
    Renvoie : les métriques {"mae", "r2", "mae_reference", "r2_reference"}.
    Échoue : FileNotFoundError si le CSV est absent.
    """
    jeu = JeuDeDonnees(chemin_donnees)
    description = decrire_variables(jeu.df)          # avant l'encodage Yes/No
    graphique_exploration(jeu.df, os.path.join(dossier_figures, "exploration.png"))

    jeu.nettoyer()
    X_train, X_test, y_train, y_test = jeu.separer()
    modele = Modele()
    modele.entrainer(X_train, y_train)
    metriques = modele.evaluer(X_test, y_test)
    graphique_predit_reel(y_test, modele.predire(X_test),
                          os.path.join(dossier_figures, "predit_contre_reel.png"))

    metadonnees = dict(description)
    metadonnees["encodage"] = {"Extracurricular Activities": {"Yes": 1, "No": 0}}
    metadonnees["cible"] = "Performance Index"
    metadonnees["metriques"] = {cle: round(valeur, 4) for cle, valeur in metriques.items()}
    metadonnees["duree_entrainement_s"] = round(Modele.entrainer.derniere_duree, 4)
    modele.sauvegarder(dossier_modeles, metadonnees)
    return metriques


if __name__ == "__main__":
    resultats = entrainer_et_sauvegarder(CHEMIN_DONNEES, DOSSIER_MODELES, DOSSIER_FIGURES)
    print(f"MAE modèle     : {resultats['mae']:.2f} points (R² = {resultats['r2']:.3f})")
    print(f"MAE référence  : {resultats['mae_reference']:.2f} points "
          f"(R² = {resultats['r2_reference']:.3f})")
    print(f"Modèle sauvegardé dans {DOSSIER_MODELES}")
