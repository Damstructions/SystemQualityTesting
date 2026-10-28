import re
from decimal import Decimal

from pages.util import money

# ---- Selectors ----------------------------------------------------------------
NAV_CART = "#cartur"
ROWS = "#tbodyid tr.success"
TOTAL = "#totalp"
PLACE_ORDER = "button"          # matched by its visible text below
# -------------------------------------------------------------------------------


class CartPage:
    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url

    def _settle(self):
        self.page.wait_for_load_state("load")
        self.page.wait_for_load_state("networkidle")

    def open(self):
        # Use the nav link, as a shopper would, so the site's cart cookie is in place
        self.page.locator(NAV_CART).click()
        self.page.wait_for_url(re.compile(r"cart\.html"))
        self._settle()

    def reload(self):
        self.page.reload()
        self._settle()

    # ---- reading state ------------------------------------------------------
    def count(self):
        return self.page.locator(ROWS).count()

    def items(self):
        """[{'title': ..., 'price': Decimal}] for every row. Waits for rows to load."""
        self.page.locator(ROWS).first.wait_for(state="visible")
        self._settle()
        rows = self.page.locator(ROWS)
        out = []
        for i in range(rows.count()):
            cells = rows.nth(i).locator("td")
            out.append(
                {
                    "title": cells.nth(1).inner_text().strip(),
                    "price": money(cells.nth(2).inner_text()),
                }
            )
        return out

    def is_empty(self):
        self._settle()
        return self.count() == 0

    def total(self):
        """The cart total shown on the page. Waits until it has been filled in."""
        self.page.wait_for_function(
            "() => { const e = document.querySelector('#totalp');"
            " return e && e.innerText.trim() !== ''; }"
        )
        return money(self.page.locator(TOTAL).inner_text())

    # ---- actions ------------------------------------------------------------
    def delete(self, title):
        row = self.page.locator(ROWS, has_text=title).first
        row.wait_for(state="visible")
        row.locator("a", has_text="Delete").click()
        row.wait_for(state="detached")
        self._settle()

    def place_order(self):
        self.page.locator(PLACE_ORDER, has_text="Place Order").click()
        self.page.locator("#orderModal").wait_for(state="visible")
