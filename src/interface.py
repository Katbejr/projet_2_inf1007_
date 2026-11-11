"""Interface graphique : appelle la logique du projet, ne la contient pas.

Technologie à faire approuver (validation D) avant de coder : Tkinter, Streamlit, etc.
"""
import tkinter as tk
from tkinter import messagebox, ttk

from donnees import (Variable, VariableCategorielle, ajouter_historique,
                     lire_historique)
from exceptions import DonneeInvalideError
from modele import Modele
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

ENCODAGE = {"Yes": 1, "No": 0}        
VARIABLE_GRAPHIQUE = "Hours Studied"  

class Application:
    """Fenêtre principale. Composition : contient le Modele et la liste des Variable."""

    def __init__(self, modele: Modele, variables: list[Variable], chemin_historique: str) -> None:
        self._modele = modele
        self._variables = variables
        self._chemin_historique = chemin_historique
        self._champs: dict = {}

        self._fenetre = tk.Tk()
        self._fenetre.title("Prédiction de la performance d'un étudiant")

        self._cadre_formulaire = ttk.Frame(self._fenetre, padding=10)
        self._cadre_formulaire.grid(row=0, column=0, sticky="n")
        self._cadre_graphique = ttk.Frame(self._fenetre, padding=10)
        self._cadre_graphique.grid(row=0, column=1)

        self._resultat = tk.StringVar(value="Remplissez le formulaire puis cliquez sur Predire.")
        self.construire_formulaire()
        self._creer_graphique()

    def lancer(self) -> None:
        """Ouvre la fenêtre et attend les actions de l'utilisateur."""
        self._fenetre.mainloop()

    def construire_formulaire(self) -> None:
        """Un champ par variable : champ texte (numérique) ou liste déroulante (catégorielle)."""
        raise NotImplementedError
    

    def predire(self) -> None:
        """Bouton « Prédire » : valide chaque saisie (try / except DonneeInvalideError),
        affiche un message clair en cas d'erreur, sinon la prédiction en langage simple,
        puis l'ajoute à l'historique."""
        raise NotImplementedError

    def creer_graphique(self) -> None:
        
        raise NotImplementedError

    def afficher_graphique(self) -> None:
        """Graphique Matplotlib intégré (titre, axes, légende)."""


        raise NotImplementedError

    def afficher_historique(self) -> None:
        """Montre les prédictions passées (lire_historique)."""


        raise NotImplementedError
