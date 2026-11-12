"""Entraînement, évaluation, sauvegarde et prédiction du modèle."""
import json
import os

import joblib
import numpy as np
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from exceptions import ModeleIntrouvableError


def mae_numpy(y_vrai: np.ndarray, y_predit: np.ndarray) -> float:
    """Erreur absolue moyenne calculée avec NumPy, sans boucle (ch. 12).

    Un test vérifiera qu'elle égale sklearn.metrics.mean_absolute_error.
    """
    # TODO (toi) : une seule ligne avec np.abs et np.mean
    return float(np.mean(np.abs(np.asarray(y_vrai) - np.asarray(y_predit))))

class Modele:
    """Enveloppe le modèle scikit-learn, sa référence et ses métadonnées."""

    FICHIER_MODELE = "modele.joblib"
    FICHIER_META = "metadonnees.json"

    def __init__(self, estimateur=None) -> None:
        self._estimateur = estimateur if estimateur is not None else LinearRegression()
        self._reference = DummyRegressor(strategy="mean")
        self._metadonnees: dict = {}

    def entrainer(self, X_train, y_train) -> None:
        """Entraîne le modèle ET la référence sur l'ensemble d'entraînement."""
        self.X_train =X_train
        self.y_train = y_train
        self._estimateur.fit(X_train, y_train)
        self._reference.fit(X_train, y_train)
    def evaluer(self, X_test, y_test) -> dict:
        """Note le modèle et la référence sur l'ensemble de test (aucun fit ici).
        
                Renvoie {"mae": ..., "r2": ..., "mae_reference": ..., "r2_reference": ...}.
                """
        # TODO (toi) : reprendre la logique de regression_lineaire.py
        pred_modele = self._estimateur.predict(X_test)
        pred_reference = self._reference.predict(X_test)
        return {
            "mae": mae_numpy(y_test, pred_modele),
            "r2": float(r2_score(y_test, pred_modele)),
            "mae_reference": mae_numpy(y_test, pred_reference),
            "r2_reference": float(r2_score(y_test, pred_reference)),
        }


    def predire(self, X) -> np.ndarray:
        """Renvoie les indices de performance prédits pour les lignes de X."""
        return self._estimateur.predict(X)

    def sauvegarder(self, dossier: str, metadonnees: dict) -> None:
        """Écrit le modèle (joblib) et les métadonnées (JSON) dans `dossier`.

        Métadonnées attendues : colonnes, valeurs des catégories,
        intervalles des numériques, métrique obtenue.
        """
        # TODO (toi) : os.path.join ; joblib.dump ; with open(..., "w", encoding="utf-8") + json.dump
        os.makedirs(dossier, exist_ok=True)
        chemin_modele = os.path.join(dossier, self.FICHIER_MODELE)
        chemin_meta = os.path.join(dossier, self.FICHIER_META)
        joblib.dump(self._estimateur, chemin_modele)

        with open(chemin_meta, "w", encoding="utf-8") as f:
            json.dump(metadonnees, f, indent=2, ensure_ascii=False)

        self._metadonnees = dict(metadonnees)

                                   
    @classmethod
    def charger(cls, dossier: str) -> "Modele":
        """Recharge un modèle sauvegardé.

        Échoue : ModeleIntrouvableError si un des deux fichiers est absent.
        """
        chemin_modele = os.path.join(dossier, cls.FICHIER_MODELE)
        chemin_meta = os.path.join(dossier, cls.FICHIER_META)

        if not os.path.exists(chemin_modele):
            raise ModeleIntrouvableError(f"Modèle introuvable : {chemin_modele}")
        if not os.path.exists(chemin_meta):
            raise ModeleIntrouvableError(f"Métadonnées introuvables : {chemin_meta}")

        estimateur = joblib.load(chemin_modele)
        with open(chemin_meta, encoding="utf-8") as f:
            metadonnees = json.load(f)

        modele = cls(estimateur)
        modele._estimateur = metadonnees
        return modele

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