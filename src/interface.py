"""Interface graphique Tkinter : appelle la logique du projet, ne la contient pas.

Le formulaire est construit à partir des Variable recréées depuis les métadonnées
du modèle sauvegardé ; le graphique Matplotlib est intégré avec FigureCanvasTkAgg.
"""
import csv

import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk

from donnees import (Variable, VariableCategorielle, ajouter_historique,
                     lire_historique)
from exceptions import DonneeInvalideError
from modele import Modele, formuler_resultat
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

VARIABLE_GRAPHIQUE = "Hours Studied"  

class Application:
    """Fenêtre principale. Composition : contient le Modele et la liste des Variable."""

    def __init__(self, modele: Modele, variables: list[Variable], chemin_historique: str) -> None:
        """Reçoit le modèle chargé, ses variables d'entrée et le chemin de l'historique CSV.

        Crée la fenêtre, le formulaire et la zone du graphique (sans l'afficher : voir lancer()).
        """
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

        self._resultat = tk.StringVar(value="Remplissez le formulaire puis cliquez sur Prédire.")
        self.construire_formulaire()
        self.creer_graphique()

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
            if variable.aide():
                ttk.Label(self._cadre_formulaire, text=variable.aide(),
                          foreground="gray").grid(row=numero, column=2, sticky="w")

        ttk.Label(self._cadre_formulaire, textvariable=self._resultat,
                  wraplength=300).grid(
            row=len(self._variables) + 1, column=0, columnspan=3, pady=10)

        ttk.Button(self._cadre_formulaire, text="Prédire",
                   command=self.predire).grid(
            row=len(self._variables), column=0, columnspan=3, pady=10)
        ttk.Button(self._cadre_formulaire, text="Voir l'historique",
                   command=self.afficher_historique).grid(
            row=len(self._variables) + 2, column=0, columnspan=3, pady=5)
    

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
        encodage = self._modele.metadonnees.get("encodage", {})  # ex. Yes -> 1, No -> 0
        for nom, valeur in valeurs.items():
            if nom in encodage:
                ligne[nom] = encodage[nom][valeur]
        X = pd.DataFrame([ligne])
        indice = self._modele.predire(X)[0]
        mae = self._modele.metadonnees.get("metriques", {}).get("mae")
        self._resultat.set(formuler_resultat(float(indice), mae))
        self.afficher_graphique(ligne, indice)
        ligne["Indice estimé"] = round(float(indice), 1)
        try:
            ajouter_historique(self._chemin_historique, ligne)
        except OSError as erreur:
            messagebox.showwarning(
                "Historique", f"La prédiction n'a pas pu être enregistrée : {erreur}")

    def creer_graphique(self) -> None:
        """Crée la figure Matplotlib vide et l'intègre dans la fenêtre Tkinter."""
        self._figure = Figure(figsize=(5, 3.8))
        self._axes = self._figure.add_subplot(111)
        self._canevas = FigureCanvasTkAgg(self._figure, master=self._cadre_graphique)
        self._canevas.get_tk_widget().pack()
        self._axes.set_title("Le graphique apparaîtra après une prédiction", fontsize=11)
        self._canevas.draw()

    def afficher_graphique(self, ligne: dict, indice: float) -> None:
        """Graphique Matplotlib intégré (titre, axes, légende)."""
        heures = list(range(1, 10))
        X = pd.DataFrame([ligne] * len(heures))
        X[VARIABLE_GRAPHIQUE] = heures
        predictions = self._modele.predire(X)

        self._axes.clear()
        self._axes.plot(heures, predictions, marker="o", label="Prédiction du modèle")
        self._axes.scatter([ligne[VARIABLE_GRAPHIQUE]], [indice],
                           color="red", zorder=3, label="Votre cas")
        self._axes.set_title("Effet des heures d'étude sur l'indice", fontsize=11)
        self._axes.set_xlabel("Heures d'étude par semaine")
        self._axes.set_ylabel("Indice de performance estimé")
        self._axes.legend()
        self._figure.tight_layout()
        self._canevas.draw()

    def afficher_historique(self) -> None:
        """Montre les prédictions passées (lire_historique)."""


        fenetre = tk.Toplevel(self._fenetre)
        fenetre.title("Historique des prédictions")
        try:
            lignes = lire_historique(self._chemin_historique)
        except (OSError, csv.Error) as erreur:
            ttk.Label(fenetre, text=f"Historique illisible : {erreur}").pack(padx=20, pady=20)
            return
        if not lignes:
            ttk.Label(fenetre, text="Aucune prédiction pour l'instant.").pack(padx=20, pady=20)
            return
        for ligne in lignes:
            texte = ", ".join(f"{cle} : {valeur}" for cle, valeur in ligne.items())
            ttk.Label(fenetre, text=texte).pack(anchor="w", padx=10, pady=2)