"""Entraînement, évaluation, sauvegarde et prédiction du modèle."""
import json
import os
import time
from functools import wraps

import joblib
import numpy as np
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression

from exceptions import ModeleIntrouvableError


def chronometre(fonction):
    """Décorateur (outil du ch. 7) : affiche la durée d'exécution de la fonction."""
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        # TODO (toi) : debut = time.perf_counter() ; resultat = fonction(...) ;
        #              afficher la durée ; return resultat
        raise NotImplementedError
    return enveloppe


def mae_numpy(y_vrai: np.ndarray, y_predit: np.ndarray) -> float:
    """Erreur absolue moyenne calculée avec NumPy, sans boucle (ch. 12).

    Un test vérifiera qu'elle égale sklearn.metrics.mean_absolute_error.
    """
    # TODO (toi) : une seule ligne avec np.abs et np.mean
    raise NotImplementedError


class Modele:
    """Enveloppe le modèle scikit-learn, sa référence et ses métadonnées."""

    FICHIER_MODELE = "modele.joblib"
    FICHIER_META = "metadonnees.json"

    def __init__(self, estimateur=None) -> None:
        self._estimateur = estimateur if estimateur is not None else LinearRegression()
        self._reference = DummyRegressor(strategy="mean")
        self._metadonnees: dict = {}

    @chronometre
    def entrainer(self, X_train, y_train) -> None:
        """Entraîne le modèle ET la référence sur l'ensemble d'entraînement."""
        # TODO (toi) : .fit() sur self._estimateur et self._reference
        raise NotImplementedError

    def evaluer(self, X_test, y_test) -> dict:
        """Renvoie {"mae": ..., "r2": ..., "mae_reference": ..., "r2_reference": ...}."""
        # TODO (toi) : reprendre la logique de regression_lineaire.py
        raise NotImplementedError

    def predire(self, X) -> np.ndarray:
        """Renvoie les indices de performance prédits pour les lignes de X."""
        raise NotImplementedError

    def sauvegarder(self, dossier: str, metadonnees: dict) -> None:
        """Écrit le modèle (joblib) et les métadonnées (JSON) dans `dossier`.

        Métadonnées attendues : colonnes, valeurs des catégories,
        intervalles des numériques, métrique obtenue.
        """
        # TODO (toi) : os.path.join ; joblib.dump ; with open(..., "w", encoding="utf-8") + json.dump
        raise NotImplementedError

    @classmethod
    def charger(cls, dossier: str) -> "Modele":
        """Recharge un modèle sauvegardé.

        Échoue : ModeleIntrouvableError si un des deux fichiers est absent.
        """
        # TODO (toi) : vérifier os.path.exists AVANT d'ouvrir ; joblib.load ; json.load
        raise NotImplementedError

    @property
    def metadonnees(self) -> dict:
        return dict(self._metadonnees)

    def __repr__(self) -> str:
        return f"Modele({type(self._estimateur).__name__})"
class ModeleParGroupe:
    """Deux régressions : une par valeur d'« Extracurricular Activities »."""

    def __init__(self) -> None:
        self._modeles = {0: Modele(), 1: Modele()}   # composition

    def entrainer(self, X_train, y_train) -> None:
        # pour chaque groupe g (0 et 1) :
        #   masque = X_train[col] == g
        #   entraîner self._modeles[g] sur X_train[masque] (sans la colonne) et y_train[masque]
        ...

    def predire(self, X):
        # pour chaque ligne, utiliser le modèle de son groupe
        ...