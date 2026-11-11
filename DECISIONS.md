# Fiche de décisions

| Choix | Options envisagées | Choix retenu et justification | Validé par l'auxiliaire (date) |
|---|---|---|---|
| Domaine | Finance, automobile (prix des voitures d'occasion), éducation | Éducation. [Votre raison : ex. sujet qui nous concerne comme étudiants.] Un utilisateur peut estimer l'effet de ses habitudes (heures d'étude, sommeil, exercices) sur sa performance. | |
| Jeu de données | CarDekho (Car details v3), Student Performance | Student Performance (Kaggle) : 10 000 lignes, 5 caractéristiques (4 numériques, 1 catégorielle), cible numérique claire, licence libre (« Anyone is free to share and use the data »), aucune donnée personnelle. [Pourquoi pas CarDekho : à compléter.] | |
| Doublons | Supprimer, conserver | Conservés (127 lignes). Les entrées n'ont que 64 800 combinaisons possibles ; ~730 répétitions sont attendues par hasard sur 10 000 lignes et 792 sont observées : ce sont vraisemblablement des étudiants distincts. Limite : une même ligne peut se trouver en entraînement et en test (1,3 % des données). | |
| Encodage | `.map`, `get_dummies` | `Extracurricular Activities` encodée Yes → 1, No → 0 avec `.map` : variable binaire, une seule colonne suffit. | |
| Séparation | 80/20, 70/30 | 70/30 avec `random_state=42` : 3 000 lignes de test donnent une mesure d'erreur plus stable, et 7 000 lignes suffisent largement pour une régression linéaire. Graine fixée pour la reproductibilité. | |
| Cible et métrique | MAE, RMSE, R² | `Performance Index` (régression, 10 à 100). Métrique principale : MAE, lisible directement en points d'indice (« le modèle se trompe en moyenne de X points »). R² en complément. | |
| Référence | Moyenne, médiane | `DummyRegressor(strategy="mean")` : prédit toujours la moyenne ; point de comparaison exigé. | |
| Modèle | Régression linéaire multiple, forêt aléatoire, deux régressions (une par valeur d'activité parascolaire) | Régression linéaire multiple : simple, coefficients interprétables, adaptée à une cible numérique. Deux régressions séparées seront comparées sur le même ensemble de test ; [choix final à compléter selon la MAE]. | |
| Technologie d'interface | Tkinter, Streamlit | [À compléter après la validation D, avec la maquette papier.] | |