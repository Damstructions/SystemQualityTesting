import re
from decimal import Decimal

from playwright.sync_api import TimeoutError as PWTimeout

from pages.util import money

# ---- Selectors ----------------------------------------------------------------
MODAL = "#orderModal"
FIELDS = {
    "name": "#name",
    "country": "#country",
    "city": "#city",
    "card": "#card",
    "month": "#month",
    "year": "#year",
}
MODAL_TOTAL = "#totalm"
CONFIRM_BOX = ".sweet-alert"
# -------------------------------------------------------------------------------

# Fake data for a public demo site
VALID_DETAILS = {
    "name": "Test Shopper",
    "country": "Australia",
    "city": "Sydney",
    "card": "4111111111111111",
    "month": "12",
    "year": "2030",
}


class CheckoutPage:
    """The 'Place Order' modal on the cart page."""

    def __init__(self, page):
        self.page = page

    def fill(self, **values):
        for key, value in values.items():
            self.page.locator(MODAL).locator(FIELDS[key]).fill(value)

    def fill_valid_details(self):
        self.fill(**VALID_DETAILS)

    def modal_total(self):
        return money(self.page.locator(MODAL_TOTAL).inner_text())

    def submit(self):
        self.page.locator(MODAL).get_by_role("button", name="Purchase").click()

    # ---- confirmation (a SweetAlert box, not a native alert) ----------------
    def confirmation_shown(self):
        try:
            self.page.locator(CONFIRM_BOX, has_text="Thank you for your purchase").wait_for(
                state="visible", timeout=10000
            )
            return True
        except PWTimeout:
            return False

    def confirmation_text(self):
        return self.page.locator(CONFIRM_BOX).inner_text()

    def confirmation_amount(self):
        m = re.search(r"Amount:\s*([\d,]+(?:\.\d+)?)", self.confirmation_text())
        assert m, f"No 'Amount:' line in confirmation: {self.confirmation_text()!r}"
        return Decimal(m.group(1).replace(",", ""))

    def confirm_ok(self):
        self.page.locator(CONFIRM_BOX).get_by_role("button", name="OK").click()
        self.page.wait_for_load_state("networkidle")
