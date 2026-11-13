"""Tests du module modele.

Tests prévus (au moins 8 au total dans le projet, cas usuel / limite / erreur) :
- mae_numpy == sklearn mean_absolute_error (pytest.approx)
- mae_numpy vaut 0 quand prédit == réel (cas limite)
- evaluer : le modèle fait mieux que la référence
- charger un dossier vide -> pytest.raises(ModeleIntrouvableError)
- sauvegarder puis charger redonne les mêmes prédictions (tmp_path)
Dans test_donnees.py :
- VariableNumerique : saisie valide, vide, non numérique, hors intervalle, bornes exactes
- VariableCategorielle : valeur permise / non permise

Écris chaque test seulement quand la fonction testée est codée : la CI doit rester verte.
"""
import numpy as np
import pytest
from sklearn.exceptions import NotFittedError
from sklearn.metrics import mean_absolute_error

from donnees import JeuDeDonnees
from modele import Modele, mae_numpy, ModeleParGroupe


CHEMIN = "donnees/Student_Performance.csv"

@pytest.fixture
def donnees_separees() -> tuple:
    """Jeu nettoyé puis séparé : X_train, X_test, y_train, y_test."""
    jeu = JeuDeDonnees(CHEMIN)
    jeu.nettoyer()
    return jeu.separer()

def test_mae_numpy_egale_sklearn() -> None:
    """mae_numpy donne le même résultat que scikit-learn (cas usuel)."""
    y_vrai = np.array([50.0, 70.0, 90.0, 30.0])
    y_predit = np.array([55.0, 65.0, 92.0, 20.0])
    assert mae_numpy(y_vrai, y_predit) == pytest.approx(
        mean_absolute_error(y_vrai, y_predit)
    )

def test_mae_numpy_zero_si_predictions_parfaites() -> None:
    """Prédit == réel : l'erreur vaut 0 (cas limite)."""
    y = np.array([10.0, 55.5, 100.0])
    assert mae_numpy(y, y) == pytest.approx(0.0)

def test_modele_bat_la_reference() -> None:
    """La régression a une MAE plus faible que la moyenne (cas usuel)."""
    jeu = JeuDeDonnees("donnees/Student_Performance.csv")
    jeu.nettoyer()
    X_train, X_test, y_train, y_test = jeu.separer()
    m = Modele()
    m.entrainer(X_train, y_train)
    resultats = m.evaluer(X_test, y_test)
    assert resultats["mae"] < resultats["mae_reference"]

def test_modele_par_groupe_comparable() -> None:
    """Les deux approches donnent une erreur proche (cas usuel)."""
    jeu = JeuDeDonnees("donnees/Student_Performance.csv")
    jeu.nettoyer()
    X_train, X_test, y_train, y_test = jeu.separer()

    unique = Modele()
    unique.entrainer(X_train, y_train)
    groupe = ModeleParGroupe()
    groupe.entrainer(X_train, y_train)

    mae_unique = unique.evaluer(X_test, y_test)["mae"]
    mae_groupe = groupe.evaluer(X_test, y_test)["mae"]
    assert len(groupe.predire(X_test)) == len(X_test)
    assert mae_groupe == pytest.approx(mae_unique, abs=1.0)