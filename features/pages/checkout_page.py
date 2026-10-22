import re
import time

# ---- Selectors: the only place to edit if the site markup differs ----------
VALIDATION_ERRORS = ".text-danger, .invalid-feedback, .alert-danger"
# -----------------------------------------------------------------------------

CHECKOUT_PATH = "index.php?route=checkout/checkout"

# Fake data for a demo site. The email is unique per run.
GUEST = {
    "First Name": "Test",
    "Last Name": "Shopper",
    "Telephone": "0400000000",
    "Address 1": "1 Test Street",
    "City": "Sydney",
    "Post Code": "2000",
}


class CheckoutPage:
    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url

    def open(self):
        self.page.goto(self.base_url + CHECKOUT_PATH)
        self.page.wait_for_load_state("domcontentloaded")

    # The checkout is a step-by-step accordion: only the open step's
    # "Continue" button is visible, so the first visible match is the right one.
    def click_continue(self):
        self.page.get_by_role("button", name="Continue").first.click()
        self.page.wait_for_load_state("networkidle")

    def choose_guest(self):
        self.page.get_by_label("Guest Checkout").check()
        self.click_continue()

    def fill_billing_details(self):
        email = f"qa.tester+{int(time.time())}@example.com"
        for label, value in GUEST.items():
            self.page.get_by_label(label).fill(value)
        self.page.get_by_label("E-Mail").fill(email)
        self.page.get_by_label("Country").select_option(label="Australia")
        region = self.page.get_by_label("Region")
        region.locator("option").nth(1).wait_for(state="attached", timeout=10000)
        region.select_option(index=1)
        self.click_continue()

    def accept_terms_and_continue(self):
        # shipping method step, then payment method step with the terms box
        self.click_continue()
        self.page.get_by_role("checkbox", name=re.compile("terms", re.I)).check()
        self.click_continue()

    def confirm_order(self):
        self.page.get_by_role("button", name=re.compile("Confirm Order", re.I)).click()

    # ---- reading state ------------------------------------------------------
    def current_url(self):
        return self.page.url

    def validation_errors_visible(self):
        err = self.page.locator(VALIDATION_ERRORS).first
        err.wait_for(state="visible", timeout=5000)
        return err.is_visible()

    def order_placed(self):
        msg = self.page.get_by_text("Your order has been placed", exact=False).first
        msg.wait_for(state="visible", timeout=20000)
        return msg.is_visible()
