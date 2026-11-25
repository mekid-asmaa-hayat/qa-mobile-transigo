# 04 — Jeux de données de test

Données **fictives**, réinitialisées avant chaque test automatisé (`POST /test/reset`) pour garantir des tests indépendants et rejouables.

## Comptes
| Id | Compte | Mot de passe | Profil | Utilisé par |
|---|---|---|---|---|
| JDD-U1 | alice@transigo.fr | Test1234! | Plein tarif | CT-01..04, 08..17, 23 |
| JDD-U2 | bob@transigo.fr | Test1234! | Étudiant -50 % | CT-05..07, 23 |
| JDD-U3 | alice@transigo.fr | `mauvais` | Mot de passe erroné | CT-02 |

## Catalogue (référentiel tarifaire)
| Code | Titre | Prix | Réductible |
|---|---|---|---|
| T1 | Ticket unitaire | 2,10 € | Oui |
| C10 | Carnet 10 tickets | 17,35 € | Oui |
| PJ | Pass journée | 8,65 € | **Non** |

## Cartes bancaires (numéros de test, jamais de vraies cartes)
| Id | Numéro | Expiration | CVV | Résultat attendu |
|---|---|---|---|---|
| JDD-C1 | 4111 1111 1111 1111 | 12/30 | 123 | Accepté |
| JDD-C2 | 4111 1111 1111 1112 | 12/30 | 123 | Refus — Luhn |
| JDD-C3 | 4111 1111 1111 1111 | 01/24 | 123 | Refus — carte expirée |
| JDD-C4 | 4111 1111 1111 1111 | 12/30 | 12 | Refus — cryptogramme |

## Résultats attendus de tarification (oracle de test)
| Profil | Panier | Calcul | Total attendu |
|---|---|---|---|
| Alice | 2 × T1 + 1 × PJ | 4,20 + 8,65 | **12,85 €** |
| Bob | 1 × T1 | 2,10 × 50 % | **1,05 €** |
| Bob | 3 × T1 | 3 × 1,05 | **3,15 €** |
| Bob | 1 × PJ | non réductible | **8,65 €** |

## Conditions d'environnement simulées
| Id | Condition | Comment |
|---|---|---|
| JDD-E1 | Hors ligne | `context.set_offline(True)` / mode avion sur device |
| JDD-E2 | Jeton expiré | jeton invalide injecté dans le stockage local |
| JDD-E3 | Mode sombre | `color_scheme="dark"` / réglage système |
| JDD-E4 | Paysage | viewport 844×390 (iPhone 13) / 915×412 (Pixel 7) |
| JDD-E5 | Petit écran | viewport 320×568 |
