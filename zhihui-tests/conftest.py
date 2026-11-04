from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from pages.store_page import StorePage

BASE_URL = "https://www.demoblaze.com/"
EVIDENCE_DIR = Path(__file__).parent / "evidence"


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        launched = playwright.chromium.launch(headless=True)
        yield launched
        launched.close()


@pytest.fixture
def page(browser, request):
    context = browser.new_context(viewport={"width": 1440, "height": 900}, locale="en-US")
    page = context.new_page()
    page.set_default_timeout(20_000)
    page.set_default_navigation_timeout(45_000)
    page.goto(BASE_URL)
    page.wait_for_selector("#nava")
    yield page
    scenario = request.node.name.replace("/", "_")
    EVIDENCE_DIR.mkdir(exist_ok=True)
    try:
        page.screenshot(path=str(EVIDENCE_DIR / f"{scenario}.png"), full_page=True, timeout=10_000)
    except Exception:
        page.screenshot(path=str(EVIDENCE_DIR / f"{scenario}.png"), timeout=10_000)
    context.close()


@pytest.fixture
def store(page):
    return StorePage(page)
