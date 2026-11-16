"""Entraînement, évaluation, sauvegarde et prédiction du modèle."""
import functools
import json
import os
import time
from typing import Any, Callable

import joblib
import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from exceptions import ModeleIntrouvableError


def chronometre(fonction: Callable) -> Callable:
    """Décorateur (ch. 7) : mesure la durée d'exécution de `fonction`.

    Reçoit : la fonction à chronométrer.
    Renvoie : une fonction enveloppe qui renvoie le même résultat ; la durée
    du dernier appel (en secondes) est conservée dans `enveloppe.derniere_duree`.
    """
    @functools.wraps(fonction)
    def enveloppe(*args: Any, **kwargs: Any) -> Any:
        """Appelle `fonction`, mémorise sa durée et renvoie son résultat."""
        debut = time.perf_counter()
        resultat = fonction(*args, **kwargs)
        enveloppe.derniere_duree = time.perf_counter() - debut
        return resultat

    enveloppe.derniere_duree = 0.0
    return enveloppe


def mae_numpy(y_vrai: np.ndarray, y_predit: np.ndarray) -> float:
    """Erreur absolue moyenne calculée avec NumPy, sans boucle (ch. 12).

    Un test vérifiera qu'elle égale sklearn.metrics.mean_absolute_error.
    """
    return float(np.mean(np.abs(np.asarray(y_vrai) - np.asarray(y_predit))))

def formuler_resultat(indice: float, mae: float | None = None) -> str:
    """Phrase lisible par un non-informaticien pour une prédiction.

    Reçoit : l'indice prédit et, si connue, l'erreur moyenne (MAE) du modèle,
    utilisée comme indice de confiance.
    Renvoie : par exemple « Indice de performance estimé : 72 sur 100
    (marge d'erreur moyenne du modèle : ± 1,6 point) ».
    """
    indice = min(max(indice, 0.0), 100.0)  # l'indice est défini sur [0, 100]
    phrase = f"Indice de performance estimé : {indice:.0f} sur 100"
    if mae is not None:
        marge = f"{mae:.1f}".replace(".", ",")
        phrase += f"\n(marge d'erreur moyenne du modèle : ± {marge} point)"
    return phrase


class Modele:
    """Enveloppe le modèle scikit-learn, sa référence et ses métadonnées."""

    FICHIER_MODELE = "modele.joblib"
    FICHIER_META = "metadonnees.json"

    def __init__(self, estimateur: Any = None) -> None:
        """Reçoit un estimateur scikit-learn (LinearRegression par défaut).

        La référence (DummyRegressor, moyenne) est créée ici ; les métadonnées
        sont remplies par sauvegarder() ou charger().
        """
        self._estimateur = estimateur if estimateur is not None else LinearRegression()
        self._reference = DummyRegressor(strategy="mean")
        self._metadonnees: dict = {}

    @chronometre
    def entrainer(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        """Entraîne le modèle ET la référence sur l'ensemble d'entraînement.

        Chronométré : la durée est lisible dans Modele.entrainer.derniere_duree.
        """
        self._estimateur.fit(X_train, y_train)
        self._reference.fit(X_train, y_train)

    def evaluer(self, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
        """Note le modèle et la référence sur l'ensemble de test (aucun fit ici).
        
                Renvoie {"mae": ..., "r2": ..., "mae_reference": ..., "r2_reference": ...}.
                """
        pred_modele = self._estimateur.predict(X_test)
        pred_reference = self._reference.predict(X_test)
        return {
            "mae": mae_numpy(y_test, pred_modele),
            "r2": float(r2_score(y_test, pred_modele)),
            "mae_reference": mae_numpy(y_test, pred_reference),
            "r2_reference": float(r2_score(y_test, pred_reference)),
        }


    def predire(self, X: pd.DataFrame) -> np.ndarray:
        """Renvoie les indices de performance prédits pour les lignes de X."""
        return self._estimateur.predict(X)

    def sauvegarder(self, dossier: str, metadonnees: dict) -> None:
        """Écrit le modèle (joblib) et les métadonnées (JSON) dans `dossier`.

        Métadonnées attendues : colonnes, valeurs des catégories,
        intervalles des numériques, métrique obtenue.
        """
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
        modele._metadonnees = metadonnees
        return modele

    @property
    def metadonnees(self) -> dict:
        """Copie des métadonnées (vide tant que le modèle n'est ni sauvegardé ni chargé)."""
        return dict(self._metadonnees)

    def __repr__(self) -> str:
        """Représentation lisible, par exemple Modele(LinearRegression)."""
        return f"Modele({type(self._estimateur).__name__})"


class ModeleParGroupe:
    """Deux régressions : une par valeur d'« Extracurricular Activities »."""
    COLONNE = "Extracurricular Activities"

    def __init__(self) -> None:
        """Crée un Modele par groupe (0 = sans activité, 1 = avec) : composition."""
        self._modeles = {0: Modele(), 1: Modele()}

    def entrainer(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        """Entraîne chaque Modele sur les lignes de son groupe, sans la colonne de groupe.

        Échoue : KeyError si la colonne de groupe est absente de X_train.
        """
        for groupe, modele in self._modeles.items():
            masque = X_train[self.COLONNE] == groupe
            modele.entrainer(X_train[masque].drop(columns=[self.COLONNE]), y_train[masque])

    def predire(self, X: pd.DataFrame) -> np.ndarray:
        """Prédit chaque ligne avec le Modele de son groupe.

        Renvoie : un tableau NumPy de même longueur que X.
        Échoue : KeyError si la colonne de groupe est absente de X.
        """
        predictions = np.empty(len(X))
        for groupe, modele in self._modeles.items():
            masque = (X[self.COLONNE] == groupe).to_numpy()
            if masque.any():
                predictions[masque] = modele.predire(X[masque].drop(columns=[self.COLONNE]))
        return predictions

    def evaluer(self, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
        """Renvoie {"mae": ..., "r2": ...} sur l'ensemble de test (aucun fit ici)."""
        predictions = self.predire(X_test)
        return {
            "mae": mae_numpy(y_test, predictions),
            "r2": float(r2_score(y_test, predictions)),
        }

    def __repr__(self) -> str:
        """Représentation lisible du modèle composé."""
        return "ModeleParGroupe(2 x Modele(LinearRegression))"
