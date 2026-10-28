import os
import re
import sys

# behave does not put features/ on the import path, so do it here
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from playwright.sync_api import sync_playwright  # noqa: E402

from pages.alerts import Alerts  # noqa: E402
from pages.auth_page import AuthPage  # noqa: E402
from pages.cart_page import CartPage  # noqa: E402
from pages.checkout_page import CheckoutPage  # noqa: E402
from pages.home_page import HomePage  # noqa: E402
from pages.product_page import ProductPage  # noqa: E402

# Configure with environment variables, e.g. (PowerShell):
#   $env:BASE_URL="https://www.demoblaze.com/"; $env:HEADLESS="1"; behave
BASE_URL = os.getenv("BASE_URL", "https://www.demoblaze.com/")
HEADLESS = os.getenv("HEADLESS", "0") == "1"
SLOW_MO = int(os.getenv("SLOW_MO", "0"))


def before_all(context):
    context.base_url = BASE_URL.rstrip("/") + "/"
    context.pw = sync_playwright().start()
    context.browser = context.pw.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
    os.makedirs("screenshots", exist_ok=True)


def before_scenario(context, scenario):
    # A new browser context per scenario = new cookies = an empty cart
    context.browser_context = context.browser.new_context()
    page = context.browser_context.new_page()
    page.set_default_timeout(10000)
    context.page = page

    # Demoblaze reports results with native JavaScript alert() boxes
    context.alerts = Alerts(page)

    context.home = HomePage(page, context.base_url)
    context.product = ProductPage(page, context.alerts)
    context.cart = CartPage(page, context.base_url)
    context.checkout = CheckoutPage(page)
    context.auth = AuthPage(page, context.alerts)

    context.prices = {}  # product name -> price seen on its product page


def after_scenario(context, scenario):
    status = str(getattr(scenario.status, "name", scenario.status)).lower()
    if status in ("failed", "error"):
        safe = re.sub(r"[^\w\-]+", "_", scenario.name)[:80]
        try:
            context.page.screenshot(path=os.path.join("screenshots", f"{safe}.png"))
        except Exception:
            pass
    context.browser_context.close()


def after_all(context):
    context.browser.close()
    context.pw.stop()
