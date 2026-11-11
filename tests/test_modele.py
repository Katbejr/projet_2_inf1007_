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
from donnees import JeuDeDonnees
from modele import Modele


def test_modele_bat_la_reference() -> None:
    """La régression a une MAE plus faible que la moyenne (cas usuel)."""
    jeu = JeuDeDonnees("donnees/Student_Performance.csv")
    jeu.nettoyer()
    X_train, X_test, y_train, y_test = jeu.separer()
    m = Modele()
    m.entrainer(X_train, y_train)
    resultats = m.evaluer(X_test, y_test)
    assert resultats["mae"] < resultats["mae_reference"]