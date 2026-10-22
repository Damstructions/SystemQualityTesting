import re
from decimal import Decimal

# ---- Selectors: the only place to edit if the site markup differs ----------
QUANTITY_INPUT = "input[name='quantity']"                 # product page
ADD_TO_CART_BUTTON = "#button-cart"                       # product page
CART_ROWS = "#content form table tbody tr"                # one row per product
ROW_QUANTITY = "input[name^='quantity']"
ROW_UPDATE = "button[data-original-title='Update'], button[title='Update'], button[aria-label='Update']"
ROW_REMOVE = "button[data-original-title='Remove'], button[title='Remove'], a[title='Remove'], button[aria-label='Remove']"
TOTALS_ROWS = "#content table tr"
# -----------------------------------------------------------------------------

CART_PATH = "index.php?route=checkout/cart"
PRODUCT_PATH = "index.php?route=product/product&product_id={id}"

# Product ids read from the live home page
PRODUCT_IDS = {
    "iPhone": 40,
    "Canon EOS 5D": 30,
    "Nikon D300": 31,
    "iPod Shuffle": 34,
    "HTC Touch HD": 28,
}

MONEY = re.compile(r"\$([\d,]+\.\d{2})")


def amounts(text):
    """All dollar amounts in a piece of text, as Decimals."""
    return [Decimal(m.replace(",", "")) for m in MONEY.findall(text)]


class CartPage:
    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url

    # ---- navigation ---------------------------------------------------------
    def open(self):
        self.page.goto(self.base_url + CART_PATH)
        self.page.wait_for_load_state("domcontentloaded")

    def reload(self):
        self.page.reload()
        self.page.wait_for_load_state("domcontentloaded")

    def proceed_to_checkout(self):
        self.page.locator("#content").get_by_role("link", name="Checkout").first.click()
        self.page.wait_for_load_state("domcontentloaded")

    # ---- actions ------------------------------------------------------------
    def add_product(self, name, quantity=1):
        if name not in PRODUCT_IDS:
            raise ValueError(f"Unknown product '{name}'. Add its id to PRODUCT_IDS.")
        self.page.goto(self.base_url + PRODUCT_PATH.format(id=PRODUCT_IDS[name]))
        self.page.fill(QUANTITY_INPUT, str(quantity))
        with self.page.expect_response(
            lambda r: r.request.method == "POST" and "cart" in r.url and "add" in r.url
        ) as resp:
            self.page.click(ADD_TO_CART_BUTTON)
        assert resp.value.ok, f"Add to cart failed with HTTP {resp.value.status}"

    def update_quantity(self, name, quantity):
        row = self._row(name)
        row.locator(ROW_QUANTITY).fill(str(quantity))
        row.locator(ROW_UPDATE).first.click()
        self.page.wait_for_load_state("networkidle")

    def remove(self, name):
        self._row(name).locator(ROW_REMOVE).first.click()
        self.page.wait_for_load_state("networkidle")

    # ---- reading state ------------------------------------------------------
    def _row(self, name):
        row = self.page.locator(CART_ROWS, has_text=name).first
        row.wait_for(state="visible", timeout=10000)
        return row

    def is_empty_message_visible(self):
        msg = self.page.get_by_text("Your shopping cart is empty", exact=False).first
        msg.wait_for(state="visible", timeout=10000)
        return msg.is_visible()

    def contains(self, name):
        return self.page.locator(CART_ROWS, has_text=name).count() > 0

    def quantity_of(self, name):
        return int(self._row(name).locator(ROW_QUANTITY).input_value())

    def unit_price(self, name):
        return amounts(self._row(name).inner_text())[0]

    def line_total(self, name):
        return amounts(self._row(name).inner_text())[-1]

    def line_item_count(self):
        self.page.locator(CART_ROWS).first.wait_for(state="visible", timeout=10000)
        return self.page.locator(CART_ROWS).count()

    def all_line_totals(self):
        rows = self.page.locator(CART_ROWS)
        return [amounts(rows.nth(i).inner_text())[-1] for i in range(rows.count())]

    def sub_total(self):
        row = self.page.locator(TOTALS_ROWS, has_text=re.compile(r"Sub-Total")).last
        row.wait_for(state="visible", timeout=10000)
        return amounts(row.inner_text())[-1]
