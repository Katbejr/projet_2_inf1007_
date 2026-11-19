"""Exceptions personnalisées du projet."""


# Erreur levée quand une saisie est invalide, pour afficher un message clair.
class DonneeInvalideError(Exception):
    """Levée quand une saisie ou une donnée ne respecte pas le format attendu."""


# Erreur levée quand le modèle sauvegardé est absent.
class ModeleIntrouvableError(Exception):
    """Levée quand le fichier du modèle ou des métadonnées est absent."""
