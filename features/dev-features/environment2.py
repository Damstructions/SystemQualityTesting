import os
import re
import sys

# behave does not put this directory on the import path, so do it here
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from playwright.sync_api import sync_playwright  # noqa: E402

from cert_date import chrome_args_for_date_only  # noqa: E402
from pages.account_page import AccountPage  # noqa: E402

# Configure with environment variables, e.g. (PowerShell):
#   $env:BASE_URL="https://opencart.abstracta.us/"; $env:HEADLESS="1"; behave features/dev-features
BASE_URL = os.getenv("BASE_URL", "https://opencart.abstracta.us/")
HEADLESS = os.getenv("HEADLESS", "0") == "1"
SLOW_MO = int(os.getenv("SLOW_MO", "0"))


def before_all(context):
    context.base_url = BASE_URL.rstrip("/") + "/"
    context.pw = sync_playwright().start()
    # Ignore a date error only after the trust store has accepted the chain
    # and the leaf name matches the host. Other certificate failures stay in force.
    context.browser = context.pw.chromium.launch(
        channel="chrome",
        headless=HEADLESS,
        slow_mo=SLOW_MO,
        args=chrome_args_for_date_only(context.base_url),
    )
    os.makedirs("screenshots", exist_ok=True)


def before_scenario(context, scenario):
    # A new browser context per scenario = a new empty cookie jar
    context.browser_context = context.browser.new_context(locale="en-AU")
    page = context.browser_context.new_page()
    page.set_default_timeout(20000)
    context.page = page
    context.account = AccountPage(page, context.base_url)


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
