# Sprint 12 — Contribution QA aux rituels Agile

## Backlog Refinement (avant le sprint)
- Relecture des US-01 à US-06 en atelier « 3 Amigos » (PO, dev, QA).
- 9 questions remontées, **4 critères d'acceptation ajoutés** (voir [02-user-stories-et-analyse.md](../02-user-stories-et-analyse.md)).
- US-04 (paiement) jugée « non prête » tant que le comportement en double appui n'était pas défini → passée « Ready » après ajout du critère d'idempotence.

## Sprint Planning
- Effort de test intégré à l'estimation de chaque US (ex. US-05 hors ligne : +3 points pour les tests sur device réel).
- Risques partagés avec l'équipe : paiement et hors ligne testés en premier.

## Daily (exemples de points QA)
- *J4* : « US-03 testée : KO sur le tarif réduit en quantité > 1, BUG-001 créé et assigné, je reteste dès la livraison. »
- *J6* : « Bloqué sur US-05 : build Android QUALIF non installable → vu avec le dev, nouveau build à midi. »
- *J8* : « Campagne 1 terminée : 30/46 OK, 8 anomalies dont 2 bloquantes. Je propose de prioriser BUG-002 et BUG-003. »

## Sprint Review — bilan qualité présenté au PO
| Indicateur | Campagne 1 | Campagne 2 |
|---|---|---|
| Exécutions automatisées OK | 30 / 46 | **46 / 46** |
| Anomalies ouvertes (B/C/Ma/Mi) | 2 / 2 / 2 / 2 | **0** |
| Décision | 🔴 NO-GO | 🟢 **GO** |
| Cas manuels device réel | 12 conçus | à exécuter sur devices avant MEP |

Démonstration du parcours achat → billet hors ligne sur iPhone et Android.

## Rétrospective — actions côté qualité
| Constat | Action |
|---|---|
| 4 anomalies sur 8 portaient sur des critères ajoutés en refinement | ✅ Continuer les 3 Amigos ; ajouter une case « cas limites » au template d'US |
| BUG-003 (double débit) trouvé tard (J8) | Automatiser le test d'idempotence dès la livraison de l'API |
| Accessibilité vérifiée uniquement en fin de sprint | Lancer l'audit axe-core dans la CI à chaque merge |
