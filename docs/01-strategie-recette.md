# 01 — Stratégie de recette — TransiGo mobile (iOS / Android)

> Contexte : évolution « Achat et présentation de titres de transport » livrée au **Sprint 12** (v1.4.0).
> Équipe Scrum : 1 PO, 1 Business Analyst, 1 UX Designer, 3 développeurs mobiles, 1 testeur fonctionnel (moi).

## 1. Objectifs
1. Vérifier la **conformité** des développements aux User Stories et à leurs critères d'acceptation.
2. Garantir la **fiabilité des parcours critiques** sur iOS **et** Android avant mise en production.
3. Couvrir les **spécificités mobiles** : réseau instable, interruptions, orientation, tailles d'écran, clavier, gestes système.
4. Vérifier l'**accessibilité numérique** (RGAA 4.1 / WCAG 2.1 AA) — obligation légale pour un service de transport public.
5. Fournir au PO une **décision GO / NO-GO argumentée** et chiffrée.

## 2. Analyse de risques (priorisation de l'effort de test)

| # | Risque | Impact | Probabilité | Criticité | Réponse de test |
|---|---|---|---|---|---|
| R1 | Montant facturé erroné (tarifs réduits, quantités) | Financier + image + juridique | Moyenne | 🔴 Élevée | Tests aux limites de tarification (CT-04 à CT-07) |
| R2 | **Double débit** (double tap, réseau lent, retry) | Financier + réclamations | Élevée sur mobile | 🔴 Élevée | CT-12, CT-M11 |
| R3 | Billet **non affichable sans réseau** (métro, zone blanche) → amende client | Client verbalisé | Élevée | 🔴 Élevée | CT-13, CT-M10 |
| R4 | Billet émis sans paiement valide | Perte de recettes | Faible | 🟠 Moyenne | CT-09 à CT-11 |
| R5 | Données visibles après déconnexion (téléphone prêté/partagé) | RGPD + fraude | Moyenne | 🟠 Moyenne | CT-14, CT-23 |
| R6 | Parcours inutilisable avec VoiceOver / TalkBack | Exclusion + non-conformité RGAA | Moyenne | 🟠 Moyenne | CT-18 à CT-20, CT-M06/07 |
| R7 | Comportement différent iOS / Android (clavier, retour, gestes) | Parcours bloqué sur un OS | Moyenne | 🟠 Moyenne | Exécution systématique sur les 2 OS + CT-M04/05 |
| R8 | Affichage cassé (petit écran, paysage, police agrandie) | Ergonomie | Moyenne | 🟡 Faible | CT-21, CT-22, CT-M08 |

## 3. Niveaux et types de tests

| Type | Qui | Quand | Outillage |
|---|---|---|---|
| Tests unitaires / d'API | Développeurs | En continu | CI |
| **Recette fonctionnelle des US** | Testeur | Dès qu'une US passe « Prête à tester » | Cahier de recette, JIRA |
| **Tests de bout en bout** (connexion → achat → billet) | Testeur | Fin de sprint, environnement de qualification | Playwright (émulation iOS/Android) + devices réels |
| **Tests de non-régression** | Testeur (automatisés) | Avant chaque mise en production | Suite automatisée en CI (46 exécutions, ~1 min) |
| Tests spécifiques mobiles | Testeur | Fin de sprint | Devices réels (cas CT-M01 à CT-M12) |
| Accessibilité | Testeur + UX | Fin de sprint | axe-core (auto) + VoiceOver / TalkBack (manuel) |
| Vérification des correctifs | Testeur | À chaque correctif livré | Re-test du cas KO + non-régression |

## 4. Approche « shift-left » (qualité dès la conception)
- Participation au **Backlog Refinement** et aux ateliers de conception (« 3 Amigos » PO / Dev / QA) : chaque US est relue avec la question *« comment je vais la tester ? »*. → voir [02-user-stories-et-analyse.md](02-user-stories-et-analyse.md), 9 questions remontées au PO avant développement.
- Critères d'acceptation rédigés en **Gherkin** (Étant donné / Quand / Alors) → directement transformables en cas de test.
- **Definition of Ready** incluant « critères d'acceptation testables + jeux de données identifiés » → [agile/definition-of-ready-done.md](agile/definition-of-ready-done.md).

## 5. Matrice d'appareils
Voir [05-matrice-appareils.md](05-matrice-appareils.md). Principe : **1 iOS récent + 1 Android récent** systématiquement, élargi aux appareils « à risque » (petit écran, ancien OS) pour les parcours critiques.

## 6. Gestion des anomalies
- **JIRA** : anomalies détectées en recette (avant production), rattachées à l'US et au sprint.
- **ServiceNow (SNOW)** : incidents remontés **en production** par le support ; le testeur qualifie l'incident, le reproduit, crée l'anomalie JIRA liée, puis valide le correctif. → exemple [anomalies/SNOW-INC0012874.md](anomalies/SNOW-INC0012874.md).

| Sévérité | Définition | Délai de correction attendu |
|---|---|---|
| **Bloquant** | Parcours critique impossible ou perte financière directe, sans contournement | Immédiat — bloque la MEP |
| **Critique** | Résultat faux sur une fonction cœur (montant, émission de billet) | Avant MEP |
| **Majeur** | Fonction dégradée, contournement possible ; non-conformité réglementaire (RGPD, RGAA) | Avant MEP |
| **Mineur** | Gêne ergonomique, contournement simple | Sprint suivant |

Cycle de vie : *Ouverte → Qualifiée → En correction → Livrée en recette → Vérifiée (fermée) / Réouverte*.

## 7. Critères d'entrée et de sortie

**Entrée en recette** : build installable sur iOS et Android en environnement de qualification ; US au statut « Prête à tester » ; jeux de données disponibles ; tests unitaires verts.

**Sortie (GO MEP)** :
- 100 % des cas de test **critiques** exécutés sur iOS et Android ;
- **0 anomalie Bloquante, Critique ou Majeure ouverte** ;
- anomalies Mineures acceptées par le PO avec contournement et planification ;
- suite de non-régression automatisée 100 % verte.

## 8. Livrables
Plan de test, cahier de recette (Excel), rapports de campagne, fiches d'anomalies, export JIRA, compte rendu de Sprint Review.
