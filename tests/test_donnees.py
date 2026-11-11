"""Tests du module donnees (premier test de mise en place)."""
import pytest

from exceptions import DonneeInvalideError


def test_nettoyer_encode_yes_no() -> None:
    jeu = JeuDeDonnees("donnees/Student_Performance.csv")
    jeu.nettoyer()
    valeurs = set(jeu.df["Extracurricular Activities"].unique())
    assert valeurs == {0, 1}
