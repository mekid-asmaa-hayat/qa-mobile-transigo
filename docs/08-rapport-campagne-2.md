# Rapport de campagne — Campagne 2 — Sprint 12 (vérification des correctifs + non-régression)

- **Version testée** : v1.4.0-rc2 — APP_DEFECTS=off
- **Date d'exécution** : 25/11/2026
- **Environnement** : émulation d'appareils Playwright — profil iOS exécuté sur Chromium (WebKit indisponible sur le poste ; WebKit exécuté en CI), profil Android sur Chromium
- **Périmètre** : tests automatisés de recette (23 cas) × 2 profils d'appareils (iOS — iPhone 13 / Android — Pixel 7). Les 12 cas manuels sur device réel sont suivis dans le cahier de recette.

## Synthèse

| Indicateur | Valeur |
|---|---|
| Cas de test automatisés | 23 |
| Exécutions (cas × appareil) | 46 |
| Exécutions OK | 46 / 46 (100 %) |
| Cas de test OK sur les 2 OS | 23 / 23 |
| Anomalies ouvertes | 0 (Bloquant 0, Critique 0, Majeur 0, Mineur 0) |

## Décision : 🟢 **GO** — mise en production recommandée

Règle appliquée (cf. stratégie de recette §7) : **0 anomalie Bloquante, Critique ou Majeure ouverte** ; les Mineures sont acceptées si un contournement existe et qu'elles sont planifiées au sprint suivant.

## Résultats détaillés

| Cas | User Story | Intitulé | iOS | Android | Anomalie |
|---|---|---|---|---|---|
| CT-01 | US-01 | connexion valide | ✅ OK | ✅ OK |  |
| CT-02 | US-01 | connexion mot de passe errone | ✅ OK | ✅ OK |  |
| CT-03 | US-02 | quantites et compteur panier | ✅ OK | ✅ OK |  |
| CT-04 | US-03 | total plein tarif | ✅ OK | ✅ OK |  |
| CT-05 | US-03 | tarif reduit quantite 1 | ✅ OK | ✅ OK |  |
| CT-06 | US-03 | tarif reduit quantite multiple | ✅ OK | ✅ OK |  |
| CT-07 | US-03 | pass journee non reductible | ✅ OK | ✅ OK |  |
| CT-08 | US-04/05 | paiement nominal billets emis | ✅ OK | ✅ OK |  |
| CT-09 | US-04 | carte numero invalide | ✅ OK | ✅ OK |  |
| CT-10 | US-04 | carte expiree | ✅ OK | ✅ OK |  |
| CT-11 | US-04 | cryptogramme invalide | ✅ OK | ✅ OK |  |
| CT-12 | US-04 | double tap paiement | ✅ OK | ✅ OK |  |
| CT-13 | US-05 | billets consultables hors ligne | ✅ OK | ✅ OK |  |
| CT-14 | US-06 | deconnexion protege les billets | ✅ OK | ✅ OK |  |
| CT-15 | US-06 | session expiree | ✅ OK | ✅ OK |  |
| CT-16 | US-04 | clavier numerique carte | ✅ OK | ✅ OK |  |
| CT-17 | Transverse | zones tactiles | ✅ OK | ✅ OK |  |
| CT-18 | US-02 | accessibilite catalogue | ✅ OK | ✅ OK |  |
| CT-19 | Transverse | accessibilite connexion paiement billets | ✅ OK | ✅ OK |  |
| CT-20 | Transverse | accessibilite mode sombre | ✅ OK | ✅ OK |  |
| CT-21 | Transverse | orientation paysage | ✅ OK | ✅ OK |  |
| CT-22 | Transverse | petit ecran 320px | ✅ OK | ✅ OK |  |
| CT-23 | US-06 | isolation donnees utilisateurs | ✅ OK | ✅ OK |  |

_Rapport généré automatiquement par `tools/generate_report.py` à partir du fichier JUnit de la campagne._
