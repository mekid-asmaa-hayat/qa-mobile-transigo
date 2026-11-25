# 06 — Cas de test manuels spécifiques mobile (devices réels)

Ces cas ne peuvent pas être automatisés de manière fiable en émulation : ils demandent un **téléphone physique**. Ils sont conçus et intégrés au cahier de recette ; dans ce projet de démonstration ils sont au statut **« Non exécuté — device réel requis »** (je ne présente pas de résultat que je n'ai pas obtenu).

| Cas | Titre | Étapes | Résultat attendu | OS |
|---|---|---|---|---|
| CT-M01 | Appel entrant pendant le paiement | 1. Remplir la carte 2. Recevoir un appel (2e téléphone) 3. Raccrocher, revenir dans l'app | Formulaire conservé (sauf CVV), **aucun paiement en double**, aucun plantage | iOS + Android |
| CT-M02 | Passage en arrière-plan pendant le paiement | 1. Appuyer sur « Confirmer » 2. Aller immédiatement sur l'écran d'accueil 3. Revenir après 30 s | La commande est soit confirmée soit clairement en échec ; billets affichés si payés | iOS + Android |
| CT-M03 | Notification par-dessus le QR code | Afficher un billet, recevoir une notification | Le QR reste lisible après disparition de la bannière | iOS + Android |
| CT-M04 | Bouton retour Android après paiement | Payer, puis appui sur retour système | Pas de retour sur l'écran de paiement pré-rempli, **pas de 2e paiement possible** | Android |
| CT-M05 | Geste retour iOS après paiement | Payer, puis balayage depuis le bord gauche | Idem CT-M04 | iOS |
| CT-M06 | Parcours d'achat complet avec VoiceOver | Écran éteint (rideau d'écran), réaliser un achat | Chaque élément est annoncé avec un nom clair (« Augmenter la quantité de Ticket unitaire »), ordre de lecture logique, montant total annoncé | iOS |
| CT-M07 | Parcours d'achat complet avec TalkBack | Idem CT-M06 | Idem | Android |
| CT-M08 | Police agrandie (Dynamic Type max / police 200 %) | Activer la plus grande taille, parcourir l'app | Aucun texte tronqué ou superposé, boutons toujours utilisables | iOS + Android |
| CT-M09 | Présentation du QR au contrôle | Afficher un billet, luminosité système au minimum | Luminosité poussée au max automatiquement, QR lu par le terminal du contrôleur | iOS + Android |
| CT-M10 | Mode avion réel puis redémarrage de l'app | Acheter, activer le mode avion, tuer l'app, la relancer | Billets affichés depuis le stockage local avec bandeau hors ligne | iOS + Android |
| CT-M11 | Réseau dégradé (3G / perte pendant la requête) | Network Link Conditioner (iOS) / profil réseau (Android), payer | Indicateur de chargement, message clair en cas d'échec, **jamais de double débit** au réessai | iOS + Android |
| CT-M12 | Mise à jour de l'application | Installer v1.3, acheter, mettre à jour en v1.4 | Session et billets conservés après mise à jour | iOS + Android |

## Charte de test exploratoire (exemple)
> **Explorer** le paiement **avec** des interruptions (appels, notifications, verrouillage, changement d'app, perte réseau) **pour découvrir** des doubles débits, pertes de panier ou états incohérents.
> Durée : 45 min · Appareils : iPhone SE + Galaxy A54 · Notes de session et anomalies dans JIRA (label `exploratoire`).
