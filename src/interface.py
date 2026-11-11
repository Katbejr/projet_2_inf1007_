"""Interface graphique : appelle la logique du projet, ne la contient pas.

Technologie à faire approuver (validation D) avant de coder : Tkinter, Streamlit, etc.
"""
from donnees import Variable, ajouter_historique, lire_historique
from exceptions import DonneeInvalideError
from modele import Modele


class Application:
    """Fenêtre principale. Composition : contient le Modele et la liste des Variable."""

    def __init__(self, modele: Modele, variables: list[Variable], chemin_historique: str) -> None:
        self._modele = modele
        self._variables = variables
        self._chemin_historique = chemin_historique

    def construire_formulaire(self) -> None:
        """Un champ par variable : champ texte (numérique) ou liste déroulante (catégorielle)."""
        raise NotImplementedError

    def predire(self) -> None:
        """Bouton « Prédire » : valide chaque saisie (try / except DonneeInvalideError),
        affiche un message clair en cas d'erreur, sinon la prédiction en langage simple,
        puis l'ajoute à l'historique."""
        raise NotImplementedError

    def afficher_graphique(self) -> None:
        """Graphique Matplotlib intégré (titre, axes, légende)."""
        raise NotImplementedError

    def afficher_historique(self) -> None:
        """Montre les prédictions passées (lire_historique)."""
        raise NotImplementedError
