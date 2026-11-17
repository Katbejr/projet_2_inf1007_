# Projet 2 INF1007 — Prédire la performance d'un étudiant

Application qui estime l'indice de performance d'un étudiant (10 à 100) à partir de ses habitudes d'étude, avec une interface graphique.

**Équipe :** Alex Le · Joud Katbe · Mohamed Dahmani

📽️ **Support de la présentation orale : [PRESENTATION.md](PRESENTATION.md)** (plan minuté, démo, schémas de conception, questions probables).

🏗️ **Architecture du projet : [ARCHITECTURE.md](ARCHITECTURE.md)** (programmes, modules, classes, parcours d'une prédiction, fichiers échangés).

## Jeu de données
- Nom : Student Performance (Multiple Linear Regression)
- Source : https://www.kaggle.com/datasets/nikhil7280/student-performance-multiple-linear-regression
- Licence : libre de partage et d’utilisation (« Anyone is free to share and use the data », page Kaggle) ; compatible avec un usage éducatif et la redistribution dans ce dépôt public
- 10 000 lignes, 5 caractéristiques (4 numériques, 1 catégorielle), cible : `Performance Index` (régression)
- Fichier : `donnees/Student_Performance.csv`

## Installation et lancement
Depuis la racine du dépôt :
```bash
pip install -r requirements.txt
```
```bash
python src/entrainement.py
```
```bash
python src/main.py
```
`entrainement.py` s'exécute **une seule fois** : il produit les graphiques dans `figures/`, puis enregistre le modèle (`modeles/modele.joblib`) et ses métadonnées (`modeles/metadonnees.json` : colonnes, intervalles des variables numériques, valeurs des catégories, encodage, métriques). `main.py` recharge ce modèle sans le ré-entraîner et construit le formulaire à partir des métadonnées.

L'interface utilise Tkinter, inclus avec Python. Sous Linux, il peut falloir l'installer à part (`sudo apt install python3-tk`).

## Tests et couverture
```bash
pytest -v
coverage run -m pytest && coverage report
```
Couverture (logique dans `src/`, hors `interface.py` et `main.py`, voir `.coveragerc`) : **96 %**, avec 29 tests.

| Module | Couverture |
|---|---|
| `donnees.py` | 97 % |
| `modele.py` | 97 % |
| `graphiques.py` | 98 % |
| `entrainement.py` | 85 % (le bloc `if __name__ == "__main__"` n'est pas testé) |
| `exceptions.py` | 100 % |

## Structure du code
| Fichier | Rôle |
|---|---|
| `src/donnees.py` | Chemins, lecture, nettoyage, classes de variables, métadonnées, historique |
| `src/modele.py` | Entraînement (chronométré), évaluation, sauvegarde, chargement, prédiction |
| `src/graphiques.py` | Graphiques d'exploration et « prédit contre réel » (`savefig`) |
| `src/entrainement.py` | Script à lancer une fois : entraîne, évalue et sauvegarde le modèle |
| `src/exceptions.py` | Exceptions personnalisées |
| `src/interface.py` | Interface graphique |
| `src/main.py` | Point d'entrée |
| `donnees/` | Jeu de données (CSV) |
| `modeles/` | Modèle sauvegardé + métadonnées JSON (générés, non versionnés) |
| `figures/` | `exploration.png` et `predit_contre_reel.png` |
| `docs/captures/` | Captures de l'interface (plan B de la démo) |
| `PRESENTATION.md` | Support de la présentation orale |
| `ARCHITECTURE.md` | Architecture détaillée (schémas) |

## Résultats du modèle
Régression linéaire multiple, évaluée sur l'ensemble de test (30 %, soit 3 000 lignes, `random_state=42`) :

| Modèle | MAE (points d'indice) | R² |
|---|---|---|
| Référence (`DummyRegressor`, moyenne) | 16,24 | -0,001 |
| Régression linéaire | **1,61** | **0,989** |

Le modèle se trompe en moyenne de 1,6 point sur 100, soit 10 fois moins que la référence (voir `figures/predit_contre_reel.png`).

**Limites :** un R² aussi élevé suggère que le jeu est synthétique, généré à partir d'une formule presque linéaire. Le modèle ne vaut donc que pour des données semblables, et pas pour de vrais étudiants. Les saisies sont limitées aux intervalles observés : hors de ces intervalles, le modèle extrapolerait. Enfin, 127 doublons sont conservés (voir DECISIONS.md).

## Outil du chapitre 7
- **Décorateur** `chronometre` (`src/modele.py`) : il enveloppe `Modele.entrainer` pour mesurer la durée de l'entraînement sans modifier la méthode. La durée est enregistrée dans les métadonnées (`duree_entrainement_s`).
- **Lambda** comme clé de tri dans `decrire_variables` (`src/donnees.py`) : `sorted(..., key=lambda v: v.lower())` ordonne les valeurs des catégories sans tenir compte de la casse.

## Documentation consultée
- pandas : [`read_csv`](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html), [`Series.map`](https://pandas.pydata.org/docs/reference/api/pandas.Series.map.html), [`DataFrame.duplicated`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.duplicated.html)
- scikit-learn : [`train_test_split`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html), [`LinearRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html), [`DummyRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyRegressor.html), [persistance des modèles (joblib)](https://scikit-learn.org/stable/model_persistence.html)
- Tkinter : [`tkinter`](https://docs.python.org/3/library/tkinter.html), [`tkinter.ttk`](https://docs.python.org/3/library/tkinter.ttk.html)
- Matplotlib : [Embedding in Tk](https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html), [`Figure.savefig`](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html)
