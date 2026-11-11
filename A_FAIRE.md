# À faire — Projet 2 (d'après l'énoncé)

## Étape 0 — mise en place
- [x] Structure de dossiers, README, requirements.txt, workflow CI, premier test
- [ ] Créer le dépôt GitHub public, y inviter Alex, premier push, CI verte
- [ ] Licence du jeu de données notée dans le README

## Volet 1 — données (`src/donnees.py`)
- [ ] Validations A (domaine) et B (jeu de données) avec l'auxiliaire
- [ ] `JeuDeDonnees.inspecter` : types, valeurs manquantes (0), doublons (127), aberrantes
- [ ] `JeuDeDonnees.nettoyer` : doublons + encodage Yes/No
- [ ] Graphique d'exploration enregistré avec `savefig`

## Volet 2 — modèle (`src/modele.py`)
- [ ] Validation C : cible, métrique, modèle
- [ ] `separer` (graine fixée), référence `DummyRegressor`
- [ ] `Modele.entrainer`, `evaluer`, `predire`, `sauvegarder`, `charger`
- [ ] `mae_numpy` (vectorisé) + test comparé à scikit-learn
- [ ] Décorateur `chronometre`
- [ ] Graphique « prédit contre réel » + limites (données probablement synthétiques)

## Volet 3 — interface (`src/interface.py`)
- [ ] Validation D : technologie + maquette papier
- [ ] `VariableNumerique.valider`, `VariableCategorielle.valider`
- [ ] Formulaire construit à partir des métadonnées JSON
- [ ] Bouton Prédire + messages clairs (aucun traceback)
- [ ] Graphique Matplotlib intégré
- [ ] Historique CSV consultable

## Qualité
- [ ] Docstrings + annotations partout
- [ ] ≥ 8 tests (usuel, limite, erreur), `pytest.approx`
- [ ] Couverture notée dans le README
- [ ] DECISIONS.md et JOURNAL_IA.md (≥ 5 entrées, dont une vérification qui change une décision)
- [ ] Cloner dans un dossier neuf : installation, lancement, CI verte
