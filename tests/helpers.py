"""Actions métier réutilisables (niveau « parcours utilisateur »)."""
from playwright.sync_api import Page, expect

ALICE = "alice@transigo.fr"   # plein tarif
BOB = "bob@transigo.fr"       # tarif réduit étudiant
PASSWORD = "Test1234!"

CARD_OK = {"number": "4111 1111 1111 1111", "expiry": "12/30", "cvv": "123"}
CARD_BAD_LUHN = {"number": "4111 1111 1111 1112", "expiry": "12/30", "cvv": "123"}
CARD_EXPIRED = {"number": "4111 1111 1111 1111", "expiry": "01/24", "cvv": "123"}
CARD_BAD_CVV = {"number": "4111 1111 1111 1111", "expiry": "12/30", "cvv": "12"}


def login(page: Page, email=ALICE, password=PASSWORD):
    page.goto("/#/login")
    page.locator("#email").fill(email)
    page.locator("#password").fill(password)
    page.locator("#login-btn").tap()
    expect(page.get_by_role("heading", name="Acheter un titre")).to_be_visible()


def _has_touch(page: Page) -> bool:
    return page.evaluate("() => 'ontouchstart' in window || navigator.maxTouchPoints > 0")


def tap(page: Page, selector: str):
    loc = page.locator(selector)
    if _has_touch(page):
        loc.tap()
    else:
        loc.click()


def add_to_cart(page: Page, product_id: str, qty: int):
    for _ in range(qty):
        page.locator(f'.product[data-id="{product_id}"] button[data-act="inc"]').tap()
    expect(page.get_by_test_id(f"qty-{product_id}")).to_have_text(str(qty))


def open_cart(page: Page):
    page.locator('nav.tabs a[data-tab="panier"]').tap()
    expect(page.get_by_test_id("cart-total")).to_be_visible()


def cart_total(page: Page) -> str:
    return page.get_by_test_id("cart-total").inner_text().replace(" ", " ")


def fill_card(page: Page, card: dict):
    page.locator("#go-pay").tap()
    page.locator("#cc-number").fill(card["number"])
    page.locator("#cc-exp").fill(card["expiry"])
    page.locator("#cc-cvv").fill(card["cvv"])


def buy(page: Page, items: dict, card=CARD_OK):
    for pid, qty in items.items():
        add_to_cart(page, pid, qty)
    open_cart(page)
    fill_card(page, card)
    page.locator("#pay-btn").tap()


def go(page: Page, route: str):
    page.evaluate(f"() => {{ location.hash = '#/{route}'; }}")
    page.wait_for_timeout(300)
