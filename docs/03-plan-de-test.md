# 03 — Plan de test — Sprint 12 (v1.4.0)

## Périmètre
| Dans le périmètre | Hors périmètre |
|---|---|
| US-01 à US-06 (connexion, catalogue, tarification, paiement, billets, session) | Back-office de tarification |
| Non-régression des parcours existants | Tests de charge / performance serveur (équipe dédiée) |
| Spécificités mobiles iOS / Android | Tests de sécurité intrusifs (pentest annuel) |
| Accessibilité (RGAA 4.1 niveau AA) | Validation physique du QR par les valideurs (recette métier exploitant) |

## Couverture : 35 cas de test
| Bloc | Cas | Mode | Exécution |
|---|---|---|---|
| Connexion / session | CT-01, 02, 14, 15, 23 | Automatisé | iOS + Android |
| Catalogue / panier / tarifs | CT-03 à 07 | Automatisé | iOS + Android |
| Paiement | CT-08 à 12, 16 | Automatisé | iOS + Android |
| Hors ligne | CT-13 | Automatisé | iOS + Android |
| Ergonomie mobile | CT-17, 21, 22 | Automatisé | iOS + Android |
| Accessibilité | CT-18, 19, 20 | Automatisé (axe-core) | iOS + Android |
| Interruptions, gestes système, lecteurs d'écran, réseau réel | CT-M01 à CT-M12 | **Manuel sur device réel** | voir matrice |

Traçabilité exigences ↔ tests : onglet « Cas de test » du [cahier de recette](cahier-de-recette.xlsx) et colonne *User Story* des rapports.

## Environnements
| Env. | Usage | Données |
|---|---|---|
| QUALIF | Recette fonctionnelle et bout en bout | Jeux de données maîtrisés, réinitialisables ([04](04-jeux-de-donnees.md)) |
| PREPROD | Vérification finale avant MEP, smoke test | Copie anonymisée |

## Planning dans le sprint (2 semaines)
| Jour | Activité QA |
|---|---|
| J1 | Sprint Planning : estimation de l'effort de test dans chaque US, identification des risques |
| J1–J3 | Rédaction / mise à jour des cas de test et des jeux de données |
| J3–J8 | Recette au fil de l'eau des US livrées ; anomalies créées dans JIRA le jour même |
| J8 | **Campagne 1** complète (bout en bout + non-régression + mobile) |
| J9 | Vérification des correctifs |
| J9 | **Campagne 2** (re-test + non-régression complète) → décision GO / NO-GO |
| J10 | Sprint Review (démo + bilan qualité) ; Rétrospective |

## Techniques de conception utilisées
- **Partitions d'équivalence et valeurs limites** : tarifs, quantités (1 / >1 / 20), dates d'expiration (mois courant / passé).
- **Tables de décision** : profil × éligibilité du titre → réduction.
- **Tests de transition d'états** : session (connecté → expiré → déconnecté), réseau (en ligne → hors ligne → en ligne).
- **Test exploratoire** en sessions de 45 min sur device réel (chartes : « interrompre le paiement », « utiliser l'app d'une seule main », « VoiceOver uniquement »).
