"""
Parcours fonctionnels — connexion, panier, tarification, paiement.
Chaque test porte l'identifiant du cas de test du cahier de recette (CT-xx).
"""
import requests
from playwright.sync_api import expect

from helpers import (ALICE, BOB, CARD_BAD_CVV, CARD_BAD_LUHN, CARD_EXPIRED, CARD_OK,
                     add_to_cart, buy, cart_total, fill_card, login, open_cart)


def test_ct01_connexion_valide(page):
    """CT-01 — US-01 : un utilisateur inscrit se connecte et arrive sur le catalogue."""
    login(page, ALICE)
    expect(page.locator("#user-name")).to_have_text("Alice Martin")
    expect(page.locator("nav.tabs")).to_be_visible()


def test_ct02_connexion_mot_de_passe_errone(page):
    """CT-02 — US-01 : mot de passe erroné -> message explicite, aucune session ouverte."""
    page.goto("/#/login")
    page.locator("#email").fill(ALICE)
    page.locator("#password").fill("mauvais")
    page.locator("#login-btn").tap()
    expect(page.get_by_role("alert")).to_have_text("Identifiants incorrects")
    assert page.evaluate("() => localStorage.getItem('tg_token')") is None


def test_ct03_quantites_et_compteur_panier(page):
    """CT-03 — US-02 : +/- mettent à jour la quantité et le compteur du panier."""
    login(page)
    add_to_cart(page, "T1", 3)
    page.locator('.product[data-id="T1"] button[data-act="dec"]').tap()
    expect(page.get_by_test_id("qty-T1")).to_have_text("2")
    expect(page.locator("#cart-count")).to_have_text("(2)")


def test_ct04_total_plein_tarif(page):
    """CT-04 — US-03 : Alice (plein tarif) 2 tickets + 1 pass journée = 4,20 + 8,65 = 12,85 €."""
    login(page, ALICE)
    add_to_cart(page, "T1", 2)
    add_to_cart(page, "PJ", 1)
    open_cart(page)
    assert cart_total(page) == "12,85 €"


def test_ct05_tarif_reduit_quantite_1(page):
    """CT-05 — US-03 : Bob (étudiant -50 %) 1 ticket = 1,05 €."""
    login(page, BOB)
    add_to_cart(page, "T1", 1)
    open_cart(page)
    assert cart_total(page) == "1,05 €"


def test_ct06_tarif_reduit_quantite_multiple(page):
    """CT-06 — US-03 : Bob 3 tickets -> la réduction s'applique à CHAQUE ticket : 3 x 1,05 = 3,15 €."""
    login(page, BOB)
    add_to_cart(page, "T1", 3)
    open_cart(page)
    assert cart_total(page) == "3,15 €", f"Total affiché : {cart_total(page)}"


def test_ct07_pass_journee_non_reductible(page):
    """CT-07 — US-03 : le pass journée n'est pas éligible à la réduction (8,65 € pour Bob)."""
    login(page, BOB)
    add_to_cart(page, "PJ", 1)
    open_cart(page)
    assert cart_total(page) == "8,65 €"


def test_ct08_paiement_nominal_billets_emis(page):
    """CT-08 — US-04/05 : paiement valide -> confirmation + 1 billet avec QR par titre acheté."""
    login(page)
    buy(page, {"T1": 2})
    expect(page.get_by_text("Paiement accepté")).to_be_visible()
    expect(page.get_by_test_id("ticket")).to_have_count(2)
    expect(page.get_by_role("img", name="QR code du billet").first).to_be_visible()


def test_ct09_carte_numero_invalide(page):
    """CT-09 — US-04 : numéro de carte ne respectant pas Luhn -> refus, aucun billet."""
    login(page)
    add_to_cart(page, "T1", 1)
    open_cart(page)
    fill_card(page, CARD_BAD_LUHN)
    page.locator("#pay-btn").tap()
    expect(page.locator("#pay-error")).to_have_text("Numéro de carte invalide")


def test_ct10_carte_expiree(page, server):
    """CT-10 — US-04 : carte expirée (01/24) -> paiement refusé, aucune commande créée."""
    login(page)
    add_to_cart(page, "T1", 1)
    open_cart(page)
    fill_card(page, CARD_EXPIRED)
    page.locator("#pay-btn").tap()
    page.wait_for_timeout(500)
    orders = requests.get(f"{server}/test/orders").json()
    assert orders == [], f"{len(orders)} commande(s) créée(s) avec une carte expirée"
    expect(page.locator("#pay-error")).to_have_text("Carte expirée")


def test_ct11_cryptogramme_invalide(page):
    """CT-11 — US-04 : cryptogramme à 2 chiffres -> refus."""
    login(page)
    add_to_cart(page, "T1", 1)
    open_cart(page)
    fill_card(page, CARD_BAD_CVV)
    page.locator("#pay-btn").tap()
    expect(page.locator("#pay-error")).to_have_text("Cryptogramme invalide")


def test_ct12_double_tap_paiement(page, server):
    """CT-12 — US-04 : un double tap sur « Confirmer » ne doit créer qu'UNE commande (pas de double débit)."""
    login(page)
    add_to_cart(page, "T1", 1)
    open_cart(page)
    fill_card(page, CARD_OK)
    page.evaluate("() => { const b = document.getElementById('pay-btn'); b.click(); b.click(); }")
    page.wait_for_timeout(1500)
    orders = requests.get(f"{server}/test/orders").json()
    assert len(orders) == 1, f"{len(orders)} commandes créées pour un seul achat"
