# Definition of Ready / Definition of Done — volet qualité

## Definition of Ready (une US peut entrer dans le sprint si…)
- [ ] Valeur métier claire (« En tant que… je veux… afin de… »)
- [ ] Critères d'acceptation rédigés en Gherkin, **testables** et relus par le testeur
- [ ] Règles de gestion explicites (calculs, arrondis, limites, messages d'erreur)
- [ ] Maquettes UX disponibles pour iOS **et** Android (états vide, erreur, chargement, hors ligne)
- [ ] Exigences d'accessibilité identifiées (libellés lecteur d'écran, contrastes)
- [ ] Jeux de données de test identifiés
- [ ] Dépendances (API, prestataire de paiement) connues

## Definition of Done (une US est terminée si…)
- [ ] Code revu, tests unitaires verts en CI
- [ ] Déployée en QUALIF sur iOS et Android
- [ ] **Tous les critères d'acceptation vérifiés** par le testeur sur les 2 OS
- [ ] Aucune anomalie Bloquante / Critique / Majeure ouverte sur l'US
- [ ] Cas de test ajoutés au cahier de recette et, si pertinent, à la suite de non-régression automatisée
- [ ] Contrôle d'accessibilité automatique OK
- [ ] Documentation fonctionnelle Confluence mise à jour
- [ ] Démontrée et acceptée par le PO en Sprint Review
