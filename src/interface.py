"""Interface graphique : appelle la logique du projet, ne la contient pas.

Technologie à faire approuver (validation D) avant de coder : Tkinter, Streamlit, etc.
"""
import pandas as pd
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
        #self._creer_graphique() #activer plus tard
        

    def lancer(self) -> None:
        """Ouvre la fenêtre et attend les actions de l'utilisateur."""
        self._fenetre.mainloop()

    def construire_formulaire(self) -> None:
        """Un champ par variable : champ texte (numérique) ou liste déroulante (catégorielle)."""
        for numero, variable in enumerate(self._variables):
            ttk.Label(self._cadre_formulaire, text=variable.nom).grid(
                row=numero, column=0, sticky="w", pady=4)
            if isinstance(variable, VariableCategorielle):
                champ = ttk.Combobox(self._cadre_formulaire,
                                     values=variable.valeurs, state="readonly")
                champ.current(0)
            else:
                champ = ttk.Entry(self._cadre_formulaire)
            champ.grid(row=numero, column=1, padx=8, pady=4)
            self._champs[variable.nom] = champ

        ttk.Label(self._cadre_formulaire, textvariable=self._resultat,
                  wraplength=300).grid(
            row=len(self._variables) + 1, column=0, columnspan=2, pady=10)

        ttk.Button(self._cadre_formulaire, text="Prédire",
                   command=self.predire).grid(
            row=len(self._variables), column=0, columnspan=2, pady=10)
    

    def predire(self) -> None:
        """Bouton « Prédire » : valide chaque saisie (try / except DonneeInvalideError),
        affiche un message clair en cas d'erreur, sinon la prédiction en langage simple,
        puis l'ajoute à l'historique."""
        valeurs = {}
        try:
            for variable in self._variables:
                saisie = self._champs[variable.nom].get()
                valeurs[variable.nom] = variable.valider(saisie)
        except DonneeInvalideError as erreur:
            messagebox.showerror("Saisie invalide", str(erreur))
            return
        ligne = dict(valeurs)
        for nom, valeur in valeurs.items():
            if valeur in ENCODAGE:
                ligne[nom] = ENCODAGE[valeur]
        X = pd.DataFrame([ligne])
        indice = self._modele.predire(X)[0]
        self._resultat.set(f"Indice de performance estimé : {indice:.0f} sur 100")
        

    def creer_graphique(self) -> None:
        
        raise NotImplementedError

    def afficher_graphique(self) -> None:
        """Graphique Matplotlib intégré (titre, axes, légende)."""


        raise NotImplementedError

    def afficher_historique(self) -> None:
        """Montre les prédictions passées (lire_historique)."""


        raise NotImplementedError
