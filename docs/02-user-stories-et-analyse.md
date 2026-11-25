# 02 — User Stories, critères d'acceptation et analyse QA

Les US ci-dessous ont été analysées en **Backlog Refinement** avant le Sprint 12. Pour chacune : critères d'acceptation en Gherkin, risques identifiés et **questions remontées au PO / BA** (la réponse obtenue est indiquée).

---

## US-01 — Connexion
**En tant que** voyageur inscrit, **je veux** me connecter avec mon e-mail et mon mot de passe **afin d'**accéder à mes titres.

```gherkin
Scénario: Connexion réussie
  Étant donné un compte actif "alice@transigo.fr"
  Quand je saisis un mot de passe correct et que je valide
  Alors j'arrive sur l'écran "Acheter un titre" et mon nom est affiché

Scénario: Mot de passe erroné
  Quand je saisis un mot de passe incorrect
  Alors le message "Identifiants incorrects" est affiché
  Et aucune session n'est ouverte
```
❓ *Le message doit-il préciser si c'est l'e-mail ou le mot de passe qui est faux ?* → **Non** (sécurité : ne pas révéler l'existence d'un compte).
❓ *Le gestionnaire de mots de passe iOS/Android doit-il pouvoir pré-remplir ?* → **Oui** → attributs `autocomplete` vérifiés.

## US-02 — Choisir ses titres
**En tant que** voyageur, **je veux** choisir des titres et leur quantité **afin de** préparer mon achat.

```gherkin
Scénario: Ajuster la quantité
  Étant donné que je suis sur le catalogue
  Quand j'appuie 3 fois sur "+" puis 1 fois sur "−" pour le ticket unitaire
  Alors la quantité affichée est 2 et le badge du panier indique (2)
```
⚠️ Risque UX/accessibilité : boutons « + / − » sous forme d'icônes → **nom accessible obligatoire** pour VoiceOver/TalkBack, zone tactile ≥ 44 pt / 48 dp.
❓ *Quantité maximale ?* → **20 par titre** (limite anti-fraude).

## US-03 — Tarification (plein tarif / tarif réduit)
**En tant qu'**étudiant, **je veux** bénéficier automatiquement de -50 % **afin de** payer le bon prix.

```gherkin
Règle: la réduction de 50 % s'applique à chaque unité des titres éligibles

Plan du scénario: Calcul du total
  Étant donné l'utilisateur <profil>
  Quand j'ajoute <quantité> <titre>
  Alors le total du panier est <total>

  Exemples:
    | profil | titre            | quantité | total   |
    | Alice  | Ticket unitaire  | 2        | 4,20 €  |
    | Bob    | Ticket unitaire  | 1        | 1,05 €  |
    | Bob    | Ticket unitaire  | 3        | 3,15 €  |
    | Bob    | Pass journée     | 1        | 8,65 €  |
```
❓ *Le pass journée est-il réductible ?* → **Non** (règle tarifaire autorité organisatrice) — ajouté aux critères, il ne l'était pas initialement.
❓ *Règle d'arrondi ?* → **Au centime, arrondi commercial (half-up), par ligne**.
💡 Technique : **partitions d'équivalence + valeurs limites** (quantité 1 / >1 / 20, titre éligible / non éligible).

## US-04 — Payer par carte
**En tant que** voyageur, **je veux** payer par carte bancaire **afin d'**obtenir mes titres immédiatement.

```gherkin
Scénario: Paiement accepté
  Étant donné un panier non vide et une carte valide
  Quand je confirme le paiement
  Alors une seule commande est créée et je suis redirigé vers "Mes billets"

Scénario: Carte refusée
  Quand je saisis une carte <cas>
  Alors le message <message> est affiché et aucune commande n'est créée
  Exemples:
    | cas                    | message                     |
    | numéro invalide (Luhn) | Numéro de carte invalide    |
    | expirée (01/24)        | Carte expirée               |
    | cryptogramme 2 chiffres| Cryptogramme invalide       |

Scénario: Double appui sur "Confirmer"
  Quand j'appuie deux fois rapidement sur "Confirmer le paiement"
  Alors une seule commande est créée et un seul débit est effectué
```
⚠️ Risque mobile majeur : **double tap / réseau lent / retry automatique** → exigence d'idempotence remontée en atelier, **ajoutée aux critères d'acceptation**.
❓ *Clavier attendu sur le numéro de carte ?* → **Pavé numérique** sur iOS et Android.

## US-05 — Présenter mes billets (y compris hors ligne)
**En tant que** voyageur, **je veux** afficher mes billets avec QR code **même sans réseau** **afin de** les présenter au contrôleur dans le métro.

```gherkin
Scénario: Consultation hors ligne
  Étant donné que j'ai acheté 1 billet et ouvert "Mes billets" en ligne
  Quand je perds le réseau et que j'actualise
  Alors mon billet reste affiché avec son QR code
  Et un bandeau indique "Hors ligne — billets enregistrés sur ce téléphone"
```
❓ *Durée de conservation hors ligne ?* → **Jusqu'à la date de validité du titre**.
❓ *Luminosité de l'écran forcée au maximum à l'affichage du QR ?* → **Oui, à tester sur device réel** (CT-M09).

## US-06 — Déconnexion et sécurité de session
**En tant que** voyageur, **je veux** me déconnecter **afin qu'**aucune personne utilisant mon téléphone ne voie mes billets.

```gherkin
Scénario: Déconnexion
  Étant donné que je suis connecté et que j'ai des billets
  Quand je me déconnecte puis que j'essaie d'ouvrir "Mes billets"
  Alors je suis renvoyé à l'écran de connexion et aucun billet n'est visible

Scénario: Session expirée
  Étant donné que mon jeton a expiré côté serveur
  Quand j'effectue une action
  Alors je suis renvoyé à l'écran de connexion, sans message technique
```
❓ *Contradiction avec US-05 ?* (billets hors ligne vs effacement à la déconnexion) → **Arbitrage PO** : le cache est **effacé à la déconnexion volontaire**, conservé en cas de simple perte réseau.

---

## Synthèse de l'analyse
- **9 questions** remontées au PO/BA avant développement, **4 critères d'acceptation ajoutés** (pass non réductible, idempotence, clavier numérique, effacement du cache à la déconnexion).
- Ces ajouts correspondent précisément à des zones où des anomalies ont ensuite été détectées (BUG-001, 003, 005, 008) : l'analyse amont permet de **tester ce qui compte**, et pas seulement le chemin nominal.
