# À faire — Projet 2 (d'après l'énoncé)

## Étape 0 — mise en place
- [x] Structure de dossiers, README, requirements.txt, workflow CI, premier test
- [x] Créer le dépôt GitHub public, y inviter Alex, premier push, CI verte
- [x] Licence du jeu de données notée dans le README

## Volet 1 — données (`src/donnees.py`)
- [x] Validations A (domaine) et B (jeu de données) avec l'auxiliaire
- [x] `JeuDeDonnees.inspecter` : types, valeurs manquantes (0), doublons (127), aberrantes
- [x] `JeuDeDonnees.nettoyer` : doublons + encodage Yes/No
- [x] Graphique d'exploration enregistré avec `savefig`

## Volet 2 — modèle (`src/modele.py`)
- [ ] Validation C : cible, métrique, modèle
- [x] `separer` (graine fixée), référence `DummyRegressor`
- [x] `Modele.entrainer`, `evaluer`, `predire`, `sauvegarder`, `charger`
- [x] `mae_numpy` (vectorisé) + test comparé à scikit-learn
- [x] Décorateur `chronometre`
- [x] Graphique « prédit contre réel » + limites (données probablement synthétiques)

## Volet 3 — interface (`src/interface.py`)
- [ ] Validation D : technologie + maquette papier
- [x] `VariableNumerique.valider`, `VariableCategorielle.valider`
- [x] Formulaire construit à partir des métadonnées JSON
- [x] Bouton Prédire + messages clairs (aucun traceback)
- [x] Graphique Matplotlib intégré
- [x] Historique CSV consultable

## Qualité
- [ ] Docstrings + annotations partout
- [x] ≥ 8 tests (usuel, limite, erreur), `pytest.approx`
- [x] Couverture notée dans le README
- [x] DECISIONS.md et JOURNAL_IA.md (≥ 5 entrées, dont une vérification qui change une décision)
- [ ] Cloner dans un dossier neuf : installation, lancement, CI verte
