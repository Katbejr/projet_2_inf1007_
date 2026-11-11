"""Tests du module donnees (premier test de mise en place)."""
import pytest

from exceptions import DonneeInvalideError


def test_exception_personnalisee_peut_etre_levee() -> None:
    """Vérifie que DonneeInvalideError hérite de Exception et se lève avec raise."""
    with pytest.raises(DonneeInvalideError):
        raise DonneeInvalideError("saisie invalide")
