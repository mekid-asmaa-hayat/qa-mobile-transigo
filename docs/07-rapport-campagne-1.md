# Rapport de campagne — Campagne 1 — Sprint 12 (recette initiale)

- **Version testée** : v1.4.0-rc1 — APP_DEFECTS=on
- **Date d'exécution** : 25/11/2026
- **Environnement** : émulation d'appareils Playwright — profil iOS exécuté sur Chromium (WebKit indisponible sur le poste ; WebKit exécuté en CI), profil Android sur Chromium
- **Périmètre** : tests automatisés de recette (23 cas) × 2 profils d'appareils (iOS — iPhone 13 / Android — Pixel 7). Les 12 cas manuels sur device réel sont suivis dans le cahier de recette.

## Synthèse

| Indicateur | Valeur |
|---|---|
| Cas de test automatisés | 23 |
| Exécutions (cas × appareil) | 46 |
| Exécutions OK | 30 / 46 (65 %) |
| Cas de test OK sur les 2 OS | 15 / 23 |
| Anomalies ouvertes | 8 (Bloquant 2, Critique 2, Majeur 2, Mineur 2) |

## Décision : 🔴 **NO-GO** — mise en production refusée en l'état

Règle appliquée (cf. stratégie de recette §7) : **0 anomalie Bloquante, Critique ou Majeure ouverte** ; les Mineures sont acceptées si un contournement existe et qu'elles sont planifiées au sprint suivant.

## Résultats détaillés

| Cas | User Story | Intitulé | iOS | Android | Anomalie |
|---|---|---|---|---|---|
| CT-01 | US-01 | connexion valide | ✅ OK | ✅ OK |  |
| CT-02 | US-01 | connexion mot de passe errone | ✅ OK | ✅ OK |  |
| CT-03 | US-02 | quantites et compteur panier | ✅ OK | ✅ OK |  |
| CT-04 | US-03 | total plein tarif | ✅ OK | ✅ OK |  |
| CT-05 | US-03 | tarif reduit quantite 1 | ✅ OK | ✅ OK |  |
| CT-06 | US-03 | tarif reduit quantite multiple | ❌ KO | ❌ KO | [BUG-001](anomalies/BUG-001.md) (Critique) |
| CT-07 | US-03 | pass journee non reductible | ✅ OK | ✅ OK |  |
| CT-08 | US-04/05 | paiement nominal billets emis | ✅ OK | ✅ OK |  |
| CT-09 | US-04 | carte numero invalide | ✅ OK | ✅ OK |  |
| CT-10 | US-04 | carte expiree | ❌ KO | ❌ KO | [BUG-004](anomalies/BUG-004.md) (Critique) |
| CT-11 | US-04 | cryptogramme invalide | ✅ OK | ✅ OK |  |
| CT-12 | US-04 | double tap paiement | ❌ KO | ❌ KO | [BUG-003](anomalies/BUG-003.md) (Bloquant) |
| CT-13 | US-05 | billets consultables hors ligne | ❌ KO | ❌ KO | [BUG-002](anomalies/BUG-002.md) (Bloquant) |
| CT-14 | US-06 | deconnexion protege les billets | ❌ KO | ❌ KO | [BUG-005](anomalies/BUG-005.md) (Majeur) |
| CT-15 | US-06 | session expiree | ✅ OK | ✅ OK |  |
| CT-16 | US-04 | clavier numerique carte | ❌ KO | ❌ KO | [BUG-008](anomalies/BUG-008.md) (Mineur) |
| CT-17 | Transverse | zones tactiles | ❌ KO | ❌ KO | [BUG-007](anomalies/BUG-007.md) (Mineur) |
| CT-18 | US-02 | accessibilite catalogue | ❌ KO | ❌ KO | [BUG-006](anomalies/BUG-006.md) (Majeur) |
| CT-19 | Transverse | accessibilite connexion paiement billets | ✅ OK | ✅ OK |  |
| CT-20 | Transverse | accessibilite mode sombre | ✅ OK | ✅ OK |  |
| CT-21 | Transverse | orientation paysage | ✅ OK | ✅ OK |  |
| CT-22 | Transverse | petit ecran 320px | ✅ OK | ✅ OK |  |
| CT-23 | US-06 | isolation donnees utilisateurs | ✅ OK | ✅ OK |  |

_Rapport généré automatiquement par `tools/generate_report.py` à partir du fichier JUnit de la campagne._
