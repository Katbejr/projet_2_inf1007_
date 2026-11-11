"""Tests du module donnees."""
import pytest

from donnees import JeuDeDonnees
from exceptions import DonneeInvalideError

CHEMIN = "donnees/Student_Performance.csv"


def test_exception_personnalisee_peut_etre_levee() -> None:
    """DonneeInvalideError hérite de Exception et se lève avec raise."""
    with pytest.raises(DonneeInvalideError):
        raise DonneeInvalideError("saisie invalide")


def test_fichier_absent_leve_erreur() -> None:
    """Un chemin inexistant lève FileNotFoundError (cas d'erreur)."""
    with pytest.raises(FileNotFoundError):
        JeuDeDonnees("inexistant.csv")


def test_inspecter_compte_lignes_et_doublons() -> None:
    """Le résumé compte 10 000 lignes et 127 doublons (cas usuel)."""
    resume = JeuDeDonnees(CHEMIN).inspecter()
    assert resume["nb_lignes"] == 10000
    assert resume["doublons"] == 127


def test_nettoyer_deux_fois_reste_0_1() -> None:
    """Appeler nettoyer() deux fois ne détruit pas l'encodage (cas limite)."""
    jeu = JeuDeDonnees(CHEMIN)
    jeu.nettoyer()
    jeu.nettoyer()
    assert set(jeu.df["Extracurricular Activities"].unique()) == {0, 1}


def test_separer_tailles() -> None:
    """80 % entraînement, 20 % test, cible retirée de X (cas usuel)."""
    jeu = JeuDeDonnees(CHEMIN)
    jeu.nettoyer()
    X_train, X_test, y_train, y_test = jeu.separer()
    assert len(X_train) == 8000 and len(X_test) == 2000
    assert "Performance Index" not in X_train.columns
