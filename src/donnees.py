"""Lecture, nettoyage des données, classes de variables et historique."""
import csv
import os

import pandas as pd
from sklearn.model_selection import train_test_split

COLONNE_CIBLE = "Performance Index"
NUMERIQUES = ["Hours Studied", "Previous Scores", "Sleep Hours",
              "Sample Question Papers Practiced"]
CATEGORIELLES = ["Extracurricular Activities"]

# Bornes logiques (min, max) pour repérer les valeurs aberrantes
BORNES = {
    "Hours Studied": (0, 24),
    "Previous Scores": (0, 100),
    "Sleep Hours": (0, 24),
    "Sample Question Papers Practiced": (0, 100),
    "Performance Index": (0, 100),
}


class JeuDeDonnees:
    """Charge le CSV et prépare les données pour le modèle."""

    def __init__(self, chemin: str) -> None:
        if not os.path.exists(chemin):
            raise FileNotFoundError(f"Fichier introuvable : {chemin}")
        self._chemin = chemin
        self._df = pd.read_csv(chemin)

    def inspecter(self) -> dict:
        """Renvoie un résumé : nombre de lignes, types, valeurs manquantes,
        doublons et valeurs aberrantes (hors des bornes logiques)."""
        df = self._df
        aberrantes = {}
        for col, (mini, maxi) in BORNES.items():
            aberrantes[col] = int(((df[col] < mini) | (df[col] > maxi)).sum())
        return {
            "nb_lignes": len(df),
            "types": df.dtypes.astype(str).to_dict(),
            "manquantes": df.isna().sum().to_dict(),
            "doublons": int(df.duplicated().sum()),
            "aberrantes": aberrantes,
        }

    def nettoyer(self) -> None:
        """Encode « Yes »/« No » en 1/0.

        Les doublons sont conservés (voir DECISIONS.md).
        Sans effet si la colonne est déjà encodée.
        """
        col = CATEGORIELLES[0]
        if self._df[col].dtype != object:
            return
        self._df[col] = self._df[col].map({"Yes": 1, "No": 0})

    def separer(self, taille_test: float = 0.3, graine: int = 42) -> tuple:
        """Renvoie X_train, X_test, y_train, y_test (train_test_split, graine fixée).

        Appeler nettoyer() avant, pour que toutes les colonnes soient numériques.
        """
        y = self._df[COLONNE_CIBLE]
        X = self._df.drop(columns=[COLONNE_CIBLE])
        return train_test_split(X, y, test_size=taille_test, random_state=graine)

    @property
    def df(self) -> pd.DataFrame:
        """Copie du tableau (lecture seule)."""
        return self._df.copy()

    def __len__(self) -> int:
        """Nombre de lignes du jeu de données."""
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
        """Convertit la saisie en nombre et vérifie qu'elle est dans [minimum, maximum].

        Échoue : DonneeInvalideError si vide, non numérique ou hors intervalle.
        """
        if not saisie.strip():
            raise DonneeInvalideError(f"{self.nom} : la saisie est vide.")
        try:
            valeur = float(saisie)
        except ValueError:
            raise DonneeInvalideError(f"{self.nom} : « {saisie} » n'est pas un nombre.")
        if not self._minimum <= valeur <= self._maximum:
            raise DonneeInvalideError(
                f"{self.nom} : doit être entre {self._minimum} et {self._maximum}."
            )
        return valeur
            


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
        """Vérifie que la saisie fait partie des valeurs permises.

        Échoue : DonneeInvalideError si la valeur n'est pas dans la liste.
        """
        if saisie not in self._valeurs:
            raise DonneeInvalideError(
                f"{self.nom} : choisir parmi {', '.join(self._valeurs)}."
            )
        return saisie

# ---------------------------------------------------------------------------
# Historique des prédictions (ch. 5 : os, with, vérifier l'existence)
# ---------------------------------------------------------------------------
def ajouter_historique(chemin: str, ligne: dict) -> None:
    """Ajoute une prédiction (dict) à la fin du fichier CSV d'historique.

    Crée le fichier avec l'en-tête s'il n'existe pas encore.
    """
    nouveau = not os.path.exists(chemin)
    with open(chemin, "a", newline="", encoding="utf-8") as f:
        ecrivain = csv.DictWriter(f, fieldnames=list(ligne.keys()))
        if nouveau:
            ecrivain.writeheader()
        ecrivain.writerow(ligne)


def lire_historique(chemin: str) -> list[dict]:
    """Renvoie la liste des prédictions passées ([] si le fichier n'existe pas)."""
    if not os.path.exists(chemin):
        return []
    with open(chemin, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
