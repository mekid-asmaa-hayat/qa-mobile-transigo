# 05 — Matrice d'appareils iOS / Android

## Principe de sélection
On ne teste pas « tous les téléphones » : on choisit selon **les statistiques d'usage réelles de l'application** (outil d'analytics) et **le risque** (petit écran, ancien OS, constructeur avec surcouche Android).

| Priorité | Appareil | OS | Pourquoi | Campagne |
|---|---|---|---|---|
| P1 | iPhone 13 | iOS 18 | Modèle iOS le plus utilisé par nos clients | Toutes |
| P1 | Google Pixel 7 | Android 15 | Android « pur », référence | Toutes |
| P1 | Samsung Galaxy A54 | Android 14 + One UI | 1er constructeur Android en France, surcouche | Bout en bout + MEP |
| P2 | iPhone SE (2e gén.) | iOS 17 | Petit écran 4,7", bouton Home, ancienne version d'iOS supportée | Parcours critiques |
| P2 | Android entrée de gamme (Redmi) | Android 12 | Faible mémoire : app tuée en arrière-plan | Interruptions |
| P3 | iPad | iPadOS 18 | Usage marginal — smoke test | MEP majeure |

## Ce qui change entre iOS et Android (et que je vérifie)
| Sujet | iOS | Android |
|---|---|---|
| Retour arrière | Geste de balayage depuis le bord | Bouton / geste retour système (CT-M04) |
| Lecteur d'écran | VoiceOver | TalkBack |
| Taille du texte | Dynamic Type | Taille de police + zoom d'affichage |
| Zone tactile minimale | 44 × 44 pt (Apple HIG) | 48 × 48 dp (Material Design) |
| Clavier | `inputmode` / `keyboardType` | idem, rendu différent selon le clavier installé |
| Permissions | Pop-up système unique | Permissions à la demande, « Refuser et ne plus demander » |
| App en arrière-plan | Suspension rapide | Peut être tuée par l'OS (mémoire) |
| Encoches / zones sûres | Dynamic Island, barre Home | Caméra perforée, barre de navigation |

## Dans ce dépôt
Les tests automatisés émulent **iPhone 13** (WebKit = moteur de Safari) et **Pixel 7** (Chromium) via les profils d'appareils Playwright, avec écran tactile, taille d'écran et user-agent réels. L'émulation **ne remplace pas** les devices réels pour les interruptions, les lecteurs d'écran et le réseau réel : ce sont les cas CT-M01 à CT-M12, exécutés manuellement (sur devices physiques ou une ferme de devices type BrowserStack / Sauce Labs).
