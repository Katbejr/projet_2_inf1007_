"""Point d'entrée de l'application."""
from donnees import CATEGORIELLES, JeuDeDonnees, VariableCategorielle, VariableNumerique
from interface import Application
from modele import Modele

CHEMIN_DONNEES = "donnees/Student_Performance.csv"
CHEMIN_HISTORIQUE = "historique.csv"

def main() -> None:
    """Lance l'application (l'interface sera branchée plus tard)."""
    variables = [
        VariableNumerique("Hours Studied", 1, 9),
        VariableNumerique("Previous Scores", 40, 99),
        VariableCategorielle("Extracurricular Activities", ["Yes", "No"]),
        VariableNumerique("Sleep Hours", 4, 9),
        VariableNumerique("Sample Question Papers Practiced", 0, 9),
    ]
    app=Application(None, variables, CHEMIN_HISTORIQUE)
    app.lancer()
    print("Projet 2 INF1007 : application en construction.")


if __name__ == "__main__":
    main()
