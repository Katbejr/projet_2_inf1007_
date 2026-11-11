"""Exceptions personnalisées du projet."""


class DonneeInvalideError(Exception):
    """Levée quand une saisie ou une donnée ne respecte pas le format attendu."""


class ModeleIntrouvableError(Exception):
    """Levée quand le fichier du modèle ou des métadonnées est absent."""
