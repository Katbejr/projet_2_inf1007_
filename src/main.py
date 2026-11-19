"""Point d'entrée de l'application : charge le modèle sauvegardé, puis ouvre l'interface.

Le modèle n'est pas ré-entraîné ici : lancer d'abord `python src/entrainement.py`.
"""
import sys

from donnees import CHEMIN_HISTORIQUE, DOSSIER_MODELES, variables_depuis_metadonnees
from exceptions import DonneeInvalideError, ModeleIntrouvableError
from interface import Application
from modele import Modele


# Charge le modèle sauvegardé, crée les variables et lance l'interface.
def main() -> None:
    """Charge le modèle et ses métadonnées, construit les variables et lance l'interface."""
    try:
        modele = Modele.charger(DOSSIER_MODELES)
        variables = variables_depuis_metadonnees(modele.metadonnees)
    except ModeleIntrouvableError as erreur:
        print(f"{erreur}\nLancez d'abord : python src/entrainement.py")
        sys.exit(1)
    except (DonneeInvalideError, KeyError) as erreur:
        print(f"Métadonnées invalides ({erreur}). Relancez : python src/entrainement.py")
        sys.exit(1)
    Application(modele, variables, CHEMIN_HISTORIQUE).lancer()


if __name__ == "__main__":
    main()
