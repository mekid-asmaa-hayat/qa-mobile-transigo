"""
Spécificités mobiles — hors ligne, session sur téléphone partagé, clavier, zones tactiles,
orientation, petits écrans, isolation des données.
"""
import requests
from playwright.sync_api import expect

from helpers import ALICE, BOB, add_to_cart, buy, go, login, open_cart


def test_ct13_billets_consultables_hors_ligne(page):
    """CT-13 — US-05 : en zone blanche (métro), les billets déjà achetés restent affichables."""
    login(page)
    buy(page, {"T1": 1})
    expect(page.get_by_test_id("ticket")).to_have_count(1)
    page.context.set_offline(True)
    page.locator("#refresh").tap()
    expect(page.get_by_test_id("offline-banner")).to_be_visible()
    expect(page.get_by_test_id("ticket")).to_have_count(1)


def test_ct14_deconnexion_protege_les_billets(page):
    """CT-14 — US-06 : après déconnexion, plus aucun billet n'est visible (téléphone prêté/partagé)."""
    login(page)
    buy(page, {"T1": 2})
    expect(page.get_by_test_id("ticket")).to_have_count(2)
    page.locator('nav.tabs a[data-tab="compte"]').tap()
    page.locator("#logout").tap()
    expect(page.locator("#login-form")).to_be_visible()
    go(page, "billets")
    expect(page.get_by_test_id("ticket")).to_have_count(0)
    expect(page.locator("#login-form")).to_be_visible()


def test_ct15_session_expiree(page):
    """CT-15 — US-06 : jeton expiré côté serveur -> retour à l'écran de connexion sans plantage."""
    login(page)
    page.evaluate("() => localStorage.setItem('tg_token', 'jeton-expire')")
    add_to_cart(page, "T1", 1)
    page.locator('nav.tabs a[data-tab="panier"]').tap()
    expect(page.locator("#login-form")).to_be_visible()


def test_ct16_clavier_numerique_carte(page):
    """CT-16 — US-04 : le champ numéro de carte ouvre le pavé numérique (inputmode) et propose l'autoremplissage."""
    login(page)
    add_to_cart(page, "T1", 1)
    open_cart(page)
    page.locator("#go-pay").tap()
    field = page.locator("#cc-number")
    assert field.get_attribute("inputmode") == "numeric", "Clavier alphabétique proposé pour un numéro de carte"
    assert field.get_attribute("autocomplete") == "cc-number"


def test_ct17_zones_tactiles(page, min_touch):
    """CT-17 — Ergonomie : zones tactiles >= 44 pt (Apple HIG) / 48 dp (Material Design)."""
    login(page)
    too_small = []
    for btn in page.locator("main button, nav.tabs a").all():
        box = btn.bounding_box()
        if box and (box["width"] < min_touch or box["height"] < min_touch):
            too_small.append(f"{btn.get_attribute('data-act') or btn.inner_text()} {box['width']:.0f}x{box['height']:.0f}")
    assert not too_small, f"Zones tactiles < {min_touch}px : {too_small}"


def test_ct21_orientation_paysage(make_context, device):
    """CT-21 — Rotation de l'écran : en paysage, le bouton de paiement reste atteignable et non masqué."""
    ctx = make_context(viewport={"width": 844, "height": 390} if device == "ios" else {"width": 915, "height": 412})
    page = ctx.new_page()
    login(page)
    add_to_cart(page, "T1", 1)
    open_cart(page)
    btn = page.locator("#go-pay")
    btn.scroll_into_view_if_needed()
    expect(btn).to_be_in_viewport()
    # la barre d'onglets fixe ne doit pas recouvrir le bouton
    covered = page.evaluate("""() => { const b = document.getElementById('go-pay').getBoundingClientRect();
        const el = document.elementFromPoint(b.left + b.width/2, b.top + b.height/2); return !el || !el.closest('#go-pay'); }""")
    assert not covered, "Le bouton Payer est recouvert en mode paysage"


def test_ct22_petit_ecran_320px(make_context):
    """CT-22 — Petits écrans (320 px, ex. iPhone SE 1re gén.) : aucun défilement horizontal sur les écrans du parcours."""
    ctx = make_context(viewport={"width": 320, "height": 568})
    page = ctx.new_page()
    overflow = []

    def check(name):
        w = page.evaluate("() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]")
        if w[0] > w[1]:
            overflow.append(f"{name} ({w[0]}px > {w[1]}px)")

    page.goto("/#/login"); check("connexion")
    login(page); check("catalogue")
    add_to_cart(page, "C10", 2); add_to_cart(page, "PJ", 1)
    open_cart(page); check("panier")
    page.locator("#go-pay").tap(); check("paiement")
    page.locator("#cc-number").fill("4111 1111 1111 1111"); page.locator("#cc-exp").fill("12/30"); page.locator("#cc-cvv").fill("123")
    page.locator("#pay-btn").tap(); page.get_by_test_id("ticket").first.wait_for(); check("billets")
    assert not overflow, f"Débordement horizontal : {overflow}"


def test_ct23_isolation_donnees_utilisateurs(page, server):
    """CT-23 — Confidentialité : Bob ne voit jamais les billets d'Alice."""
    login(page, ALICE)
    buy(page, {"T1": 1})
    expect(page.get_by_test_id("ticket")).to_have_count(1)
    page.locator('nav.tabs a[data-tab="compte"]').tap()
    page.locator("#logout").tap()
    login(page, BOB)
    page.locator('nav.tabs a[data-tab="billets"]').tap()
    expect(page.get_by_text("Aucun billet pour le moment.")).to_be_visible()
