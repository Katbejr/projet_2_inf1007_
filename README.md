# Projet 2 INF1007 — Prédire la performance d'un étudiant

Application qui estime l'indice de performance d'un étudiant (10 à 100) à partir de ses habitudes d'étude, avec une interface graphique.

**Équipe :** Alex · Joud Katbe · Mohamed Dahmani

## Jeu de données
- Nom : Student Performance (Multiple Linear Regression)
- Source : https://www.kaggle.com/datasets/nikhil7280/student-performance-multiple-linear-regression
- Licence : libre de partage et d’utilisation (« Anyone is free to share and use the data », page Kaggle) ; compatible avec un usage éducatif et la redistribution dans ce dépôt public
- 10 000 lignes, 5 caractéristiques (4 numériques, 1 catégorielle), cible : `Performance Index` (régression)
- Fichier : `donnees/Student_Performance.csv`

## Installation et lancement
```bash
pip install -r requirements.txt
python src/main.py
```

## Tests et couverture
```bash
pytest -v
coverage run -m pytest && coverage report
```
Couverture : _à compléter_

## Structure du code
| Fichier | Rôle |
|---|---|
| `src/donnees.py` | Lecture, nettoyage, classes de variables, historique |
| `src/modele.py` | Entraînement, évaluation, sauvegarde, prédiction |
| `src/exceptions.py` | Exceptions personnalisées |
| `src/interface.py` | Interface graphique |
| `src/main.py` | Point d'entrée |
| `donnees/` | Jeu de données (CSV) |
| `modeles/` | Modèle sauvegardé + métadonnées JSON |

## Résultats du modèle
_Métrique et comparaison avec la référence : à compléter._

## Outil du chapitre 7
_À compléter (ex. : le décorateur `chronometre` mesure la durée de l'entraînement)._

## Documentation consultée
- _pandas : à compléter_
- _scikit-learn : à compléter_
- _interface graphique : à compléter_
