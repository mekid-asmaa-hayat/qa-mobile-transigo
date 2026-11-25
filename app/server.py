"""
TransiGo — application mobile de démonstration (achat de titres de transport).

⚠️ Application FICTIVE créée uniquement comme terrain d'exercice QA.
Elle contient des défauts injectés volontairement, activés par la variable
d'environnement APP_DEFECTS=on (valeur par défaut). APP_DEFECTS=off = version corrigée.

Lancement :  python app/server.py   puis ouvrir http://localhost:5050 en vue mobile.
"""
import os
import secrets
import threading
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from flask import Flask, jsonify, render_template, request

DEFECTS = os.environ.get("APP_DEFECTS", "on").lower() == "on"

app = Flask(__name__)
_lock = threading.Lock()

USERS = {
    "alice@transigo.fr": {"password": "Test1234!", "name": "Alice Martin", "reduced": False},
    "bob@transigo.fr": {"password": "Test1234!", "name": "Bob Leroy (étudiant)", "reduced": True},
}

CATALOGUE = [
    {"id": "T1", "label": "Ticket unitaire", "price": "2.10", "reducible": True},
    {"id": "C10", "label": "Carnet 10 tickets", "price": "17.35", "reducible": True},
    {"id": "PJ", "label": "Pass journée", "price": "8.65", "reducible": False},
]
PRODUCTS = {p["id"]: p for p in CATALOGUE}

STATE = {}


def reset_state():
    with _lock:
        STATE.clear()
        STATE.update({"tokens": {}, "orders": [], "idempotency": {}, "seq": 0})


reset_state()


def money(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def current_user():
    auth = request.headers.get("Authorization", "")
    token = auth.replace("Bearer ", "")
    return STATE["tokens"].get(token)


def quote(items, user):
    lines, total = [], Decimal("0")
    for it in items:
        product = PRODUCTS.get(it.get("id"))
        qty = int(it.get("qty", 0))
        if not product or qty < 1 or qty > 20:
            raise ValueError("Article ou quantité invalide")
        price = Decimal(product["price"])
        line = price * qty
        if USERS[user]["reduced"] and product["reducible"]:
            if DEFECTS:
                # [DEFECT BUG-001] la réduction de 50 % n'est appliquée qu'à une seule unité
                line = price * qty - price * Decimal("0.5")
            else:
                line = price * qty * Decimal("0.5")
        total += line
        lines.append({"id": product["id"], "label": product["label"], "qty": qty, "amount": money(line)})
    return lines, money(total)


def luhn_ok(number: str) -> bool:
    digits = [int(d) for d in number]
    checksum = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0


def validate_card(card):
    number = (card.get("number") or "").replace(" ", "")
    expiry = card.get("expiry") or ""
    cvv = card.get("cvv") or ""
    if not (number.isdigit() and len(number) == 16 and luhn_ok(number)):
        return "Numéro de carte invalide"
    if len(expiry) != 5 or expiry[2] != "/" or not (expiry[:2] + expiry[3:]).isdigit():
        return "Date d'expiration invalide (MM/AA)"
    month, year = int(expiry[:2]), 2000 + int(expiry[3:])
    if not 1 <= month <= 12:
        return "Date d'expiration invalide (MM/AA)"
    if not DEFECTS:
        today = date.today()
        if (year, month) < (today.year, today.month):
            return "Carte expirée"
    # [DEFECT BUG-004] en version défectueuse, aucune vérification de date passée
    if not (cvv.isdigit() and len(cvv) == 3):
        return "Cryptogramme invalide"
    return None


@app.get("/")
def index():
    return render_template("index.html", defects=DEFECTS)


@app.post("/api/login")
def login():
    data = request.get_json(force=True)
    user = USERS.get((data.get("email") or "").strip().lower())
    if not user or user["password"] != data.get("password"):
        return jsonify(error="Identifiants incorrects"), 401
    token = secrets.token_hex(16)
    STATE["tokens"][token] = data["email"].strip().lower()
    return jsonify(token=token, name=user["name"], reduced=user["reduced"])


@app.post("/api/logout")
def logout():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    STATE["tokens"].pop(token, None)
    return jsonify(ok=True)


@app.get("/api/catalogue")
def catalogue():
    return jsonify(CATALOGUE)


@app.post("/api/quote")
def api_quote():
    user = current_user()
    if not user:
        return jsonify(error="Session expirée"), 401
    try:
        lines, total = quote(request.get_json(force=True).get("items", []), user)
    except ValueError as exc:
        return jsonify(error=str(exc)), 400
    return jsonify(lines=lines, total=total)


@app.post("/api/orders")
def create_order():
    user = current_user()
    if not user:
        return jsonify(error="Session expirée"), 401
    data = request.get_json(force=True)
    key = data.get("idempotency_key")
    with _lock:
        if not DEFECTS and key and key in STATE["idempotency"]:
            return jsonify(STATE["idempotency"][key]), 200
        # [DEFECT BUG-003] en version défectueuse la clé d'idempotence est ignorée
        error = validate_card(data.get("card", {}))
        if error:
            return jsonify(error=error), 422
        try:
            lines, total = quote(data.get("items", []), user)
        except ValueError as exc:
            return jsonify(error=str(exc)), 400
        STATE["seq"] += 1
        order_id = f"CMD-{STATE['seq']:05d}"
        tickets = []
        for line in lines:
            for n in range(line["qty"]):
                tickets.append({"ref": f"{order_id}-{line['id']}-{n + 1}", "label": line["label"]})
        order = {"id": order_id, "user": user, "total": total, "lines": lines, "tickets": tickets}
        STATE["orders"].append(order)
        if key:
            STATE["idempotency"][key] = order
    return jsonify(order), 201


@app.get("/api/tickets")
def tickets():
    user = current_user()
    if not user:
        return jsonify(error="Session expirée"), 401
    result = [t for o in STATE["orders"] if o["user"] == user for t in o["tickets"]]
    return jsonify(result)


# --- Endpoints réservés aux tests (jeux de données) ---------------------------
@app.post("/test/reset")
def test_reset():
    reset_state()
    return jsonify(ok=True, defects=DEFECTS)


@app.get("/test/orders")
def test_orders():
    return jsonify(STATE["orders"])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    print(f"TransiGo démo — APP_DEFECTS={'on' if DEFECTS else 'off'} — http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
