"""Lecture, nettoyage des données, classes de variables et historique."""
import csv
import os

import pandas as pd

COLONNE_CIBLE = "Performance Index"
NUMERIQUES = ["Hours Studied", "Previous Scores", "Sleep Hours",
              "Sample Question Papers Practiced"]
CATEGORIELLES = ["Extracurricular Activities"]


class JeuDeDonnees:
    """Charge le CSV et prépare les données pour le modèle."""

    def __init__(self, chemin: str) -> None:
        # TODO (toi) : vérifier os.path.exists(chemin), sinon lever une exception
        self._chemin = chemin
        self._df = pd.read_csv(chemin)

    def inspecter(self) -> dict:
        """Renvoie un résumé : nombre de lignes, types, valeurs manquantes, doublons."""
        raise NotImplementedError

    def nettoyer(self) -> None:
        """Supprime doublons / lignes invalides et encode « Yes »/« No » en 1/0."""
        raise NotImplementedError

    def separer(self, taille_test: float = 0.2, graine: int = 42):
        """Renvoie X_train, X_test, y_train, y_test (train_test_split, graine fixée)."""
        raise NotImplementedError

    @property
    def df(self) -> pd.DataFrame:
        return self._df.copy()

    def __len__(self) -> int:
        return len(self._df)
# ---------------------------------------------------------------------------
# Classes de variables (ch. 9 à 11 : héritage, polymorphisme, encapsulation)
# Chaque variable valide la saisie de l'utilisateur à sa façon.
# ---------------------------------------------------------------------------
from abc import ABC, abstractmethod

from exceptions import DonneeInvalideError


class Variable(ABC):
    """Classe parente abstraite : une caractéristique d'entrée du modèle."""

    def __init__(self, nom: str) -> None:
        self._nom = nom

    @property
    def nom(self) -> str:
        """Nom de la colonne (lecture seule)."""
        return self._nom

    @abstractmethod
    def valider(self, saisie: str):
        """Convertit et valide une saisie texte.

        Reçoit : la saisie brute (str) venant de l'interface.
        Renvoie : la valeur convertie, prête pour le modèle.
        Échoue : lève DonneeInvalideError si la saisie est invalide.
        """

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._nom!r})"


class VariableNumerique(Variable):
    """Variable numérique bornée par un intervalle [minimum, maximum]."""

    def __init__(self, nom: str, minimum: float, maximum: float) -> None:
        super().__init__(nom)
        self._minimum = minimum
        self._maximum = maximum

    def valider(self, saisie: str) -> float:
        # TODO (toi) :
        # 1. saisie vide (après .strip()) -> raise DonneeInvalideError(...)
        # 2. convertir avec float() dans un try / except ValueError
        #    -> raise DonneeInvalideError(...) si non numérique
        # 3. hors de [self._minimum, self._maximum] -> raise DonneeInvalideError(...)
        # 4. return la valeur
        raise NotImplementedError


class VariableCategorielle(Variable):
    """Variable catégorielle : la saisie doit faire partie des valeurs permises."""

    def __init__(self, nom: str, valeurs: list[str]) -> None:
        super().__init__(nom)
        self._valeurs = list(valeurs)

    @property
    def valeurs(self) -> list[str]:
        """Valeurs possibles (pour remplir la liste déroulante)."""
        return list(self._valeurs)

    def valider(self, saisie: str) -> str:
        # TODO (toi) : saisie absente de self._valeurs -> raise DonneeInvalideError(...)
        #              sinon return saisie
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Historique des prédictions (ch. 5 : os, with, vérifier l'existence)
# ---------------------------------------------------------------------------
def ajouter_historique(chemin: str, ligne: dict) -> None:
    """Ajoute une prédiction (dict) à la fin du fichier CSV d'historique.

    Crée le fichier avec l'en-tête s'il n'existe pas encore.
    """
    # TODO (toi) : os.path.exists(chemin) ; with open(chemin, "a", newline="", encoding="utf-8") ;
    #              csv.DictWriter, writeheader() seulement si le fichier est nouveau
    raise NotImplementedError


def lire_historique(chemin: str) -> list[dict]:
    """Renvoie la liste des prédictions passées ([] si le fichier n'existe pas)."""
    # TODO (toi) : with open(...) + csv.DictReader
    raise NotImplementedError
