"""
Socle d'exécution des tests mobiles TransiGo.

- Lance l'application de démo (APP_DEFECTS=on|off hérité de l'environnement).
- Paramètre chaque test sur deux profils d'appareils :
    ios     -> iPhone 13 (moteur WebKit = Safari) ; IOS_ENGINE=chromium pour forcer Chrome en local
    android -> Pixel 7 (moteur Chromium = Chrome Android)
- Remet les données de test à zéro avant chaque test (tests indépendants).
- Capture une preuve d'écran à chaque échec (reports/captures/).
"""
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PORT = int(os.environ.get("PORT", 5057))
BASE_URL = f"http://127.0.0.1:{PORT}"
CAPTURES = ROOT / "reports" / "captures"

DEVICES = {
    "ios": {"descriptor": "iPhone 13", "engine": os.environ.get("IOS_ENGINE", "webkit"), "min_touch": 44},
    "android": {"descriptor": "Pixel 7", "engine": "chromium", "min_touch": 48},
}


@pytest.fixture(scope="session")
def server():
    env = {**os.environ, "PORT": str(PORT)}
    proc = subprocess.Popen([sys.executable, str(ROOT / "app" / "server.py")], env=env,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(50):
        try:
            requests.post(f"{BASE_URL}/test/reset", timeout=1)
            break
        except requests.ConnectionError:
            time.sleep(0.2)
    else:
        proc.kill()
        raise RuntimeError("L'application n'a pas démarré")
    yield BASE_URL
    proc.terminate()


@pytest.fixture(scope="session")
def pw():
    with sync_playwright() as p:
        yield p


_browsers = {}


def get_browser(pw, engine):
    if engine not in _browsers:
        kwargs = {}
        if engine == "chromium" and os.environ.get("PW_CHANNEL"):
            kwargs["channel"] = os.environ["PW_CHANNEL"]
        _browsers[engine] = getattr(pw, engine).launch(**kwargs)
    return _browsers[engine]


@pytest.fixture(params=list(DEVICES), ids=list(DEVICES))
def device(request):
    return request.param


@pytest.fixture
def make_context(pw, server, device):
    """Fabrique de contextes navigateur émulant l'appareil (overrides possibles : viewport, color_scheme...)."""
    contexts = []
    spec = DEVICES[device]

    def _make(**overrides):
        descriptor = dict(pw.devices[spec["descriptor"]])
        descriptor.pop("default_browser_type", None)
        descriptor.update(overrides)
        ctx = get_browser(pw, spec["engine"]).new_context(base_url=server, locale="fr-FR", **descriptor)
        contexts.append(ctx)
        return ctx

    yield _make
    for ctx in contexts:
        ctx.close()


@pytest.fixture
def page(make_context, request, device):
    ctx = make_context()
    pg = ctx.new_page()
    yield pg
    rep = getattr(request.node, "rep_call", None)
    if rep is not None and rep.failed:
        CAPTURES.mkdir(parents=True, exist_ok=True)
        try:
            pg.screenshot(path=str(CAPTURES / f"{request.node.originalname}-{device}.png"), full_page=True)
        except Exception:
            pass


@pytest.fixture(autouse=True)
def reset_data(server):
    requests.post(f"{server}/test/reset", timeout=5)


@pytest.fixture
def min_touch(device):
    return DEVICES[device]["min_touch"]


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


def pytest_sessionfinish(session, exitstatus):
    for b in _browsers.values():
        try:
            b.close()
        except Exception:
            pass
