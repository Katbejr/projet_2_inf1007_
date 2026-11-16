"""Tests du module donnees."""
import pytest

from donnees import (
    JeuDeDonnees,
    VariableCategorielle,
    VariableNumerique,
    ajouter_historique,
    lire_historique,
    variables_depuis_metadonnees,
)
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
    """70 % entraînement, 30 % test, cible retirée de X (cas usuel)."""
    jeu = JeuDeDonnees(CHEMIN)
    jeu.nettoyer()
    X_train, X_test, y_train, y_test = jeu.separer()
    assert len(X_train) == 7000 and len(X_test) == 3000
    assert "Performance Index" not in X_train.columns


def test_numerique_valide() -> None:
    """Saisie numérique dans l'intervalle (cas usuel)."""
    v = VariableNumerique("Sleep Hours", 4, 9)
    assert v.valider("7") == pytest.approx(7.0)


def test_numerique_borne_exacte() -> None:
    """Borne maximale acceptée (cas limite)."""
    v = VariableNumerique("Sleep Hours", 4, 9)
    assert v.valider("9") == pytest.approx(9.0)


@pytest.mark.parametrize("saisie", ["", "   ", "abc", "12"])
def test_numerique_invalide(saisie: str) -> None:
    """Vide, espaces, texte ou hors intervalle : erreur (cas d'erreur)."""
    v = VariableNumerique("Sleep Hours", 4, 9)
    with pytest.raises(DonneeInvalideError):
        v.valider(saisie)


def test_categorielle_valide() -> None:
    """Valeur permise acceptée (cas usuel)."""
    v = VariableCategorielle("Extracurricular Activities", ["Yes", "No"])
    assert v.valider("Yes") == "Yes"


@pytest.mark.parametrize("saisie", ["", "Oui", "yes"])
def test_categorielle_invalide(saisie: str) -> None:
    """Vide, autre langue ou mauvaise casse : erreur (cas d'erreur)."""
    v = VariableCategorielle("Extracurricular Activities", ["Yes", "No"])
    with pytest.raises(DonneeInvalideError):
        v.valider(saisie)


def test_historique_ajoute_puis_relit(tmp_path) -> None:
    """Deux ajouts puis relecture : en-tête unique, deux lignes (cas usuel)."""
    chemin = str(tmp_path / "historique.csv")
    assert lire_historique(chemin) == []
    ajouter_historique(chemin, {"heures": 7, "prediction": 72.5})
    ajouter_historique(chemin, {"heures": 3, "prediction": 41.0})
    lignes = lire_historique(chemin)
    assert len(lignes) == 2
    assert lignes[0]["prediction"] == "72.5"


def test_variables_depuis_metadonnees() -> None:
    """Une Variable du bon type par colonne, dans l'ordre (cas usuel)."""
    meta = {
        "colonnes": ["Sleep Hours", "Extracurricular Activities"],
        "numeriques": {"Sleep Hours": [4.0, 9.0]},
        "categorielles": {"Extracurricular Activities": ["No", "Yes"]},
    }
    variables = variables_depuis_metadonnees(meta)
    assert isinstance(variables[0], VariableNumerique)
    assert variables[0].maximum == pytest.approx(9.0)
    assert isinstance(variables[1], VariableCategorielle)
    assert variables[1].valeurs == ["No", "Yes"]


def test_variables_colonne_non_decrite_leve_erreur() -> None:
    """Colonne absente des métadonnées : DonneeInvalideError (cas d'erreur)."""
    meta = {"colonnes": ["Inconnue"], "numeriques": {}, "categorielles": {}}
    with pytest.raises(DonneeInvalideError):
        variables_depuis_metadonnees(meta)
