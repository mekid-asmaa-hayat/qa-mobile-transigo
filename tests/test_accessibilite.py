"""
Accessibilité numérique (RGAA 4.1 / WCAG 2.1 AA) — contrôles automatiques avec axe-core.
Les contrôles automatiques couvrent ~30-40 % des critères : ils complètent, sans les remplacer,
les tests manuels VoiceOver / TalkBack du cahier de recette (CT-M06, CT-M07).
"""
from axe_playwright_python.sync_playwright import Axe

from helpers import add_to_cart, login, open_cart

axe = Axe()
BLOCKING = {"critical", "serious"}


def blocking_violations(page):
    results = axe.run(page)
    return [f"{v['id']} ({v['impact']}) x{len(v['nodes'])} : {v['help']}"
            for v in results.response["violations"] if v["impact"] in BLOCKING]


def test_ct18_accessibilite_catalogue(page):
    """CT-18 — US-02 : l'écran d'achat n'a aucune violation critique/sérieuse (ex. boutons sans nom pour VoiceOver/TalkBack)."""
    login(page)
    violations = blocking_violations(page)
    assert not violations, "\n".join(violations)


def test_ct19_accessibilite_connexion_paiement_billets(page):
    """CT-19 — Écrans connexion, paiement et billets sans violation critique/sérieuse."""
    found = {}
    page.goto("/#/login")
    page.locator("#email").wait_for()
    found["connexion"] = blocking_violations(page)
    login(page)
    add_to_cart(page, "T1", 1)
    open_cart(page)
    page.locator("#go-pay").tap()
    page.locator("#cc-number").wait_for()
    found["paiement"] = blocking_violations(page)
    page.locator("#cc-number").fill("4111 1111 1111 1111"); page.locator("#cc-exp").fill("12/30"); page.locator("#cc-cvv").fill("123")
    page.locator("#pay-btn").tap()
    page.get_by_test_id("ticket").first.wait_for()
    found["billets"] = blocking_violations(page)
    problems = {k: v for k, v in found.items() if v}
    assert not problems, problems


def test_ct20_accessibilite_mode_sombre(make_context):
    """CT-20 — Mode sombre système : contrastes conformes sur connexion et panier."""
    page = make_context(color_scheme="dark").new_page()
    page.goto("/#/login")
    page.locator("#email").wait_for()
    v1 = blocking_violations(page)
    login(page)
    add_to_cart(page, "PJ", 1)
    open_cart(page)
    v2 = blocking_violations(page)
    assert not (v1 or v2), {"connexion": v1, "panier": v2}
