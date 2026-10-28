from pages.util import money

# ---- Selectors ----------------------------------------------------------------
NAME = "h2.name"
PRICE = "h3.price-container"
ADD_TO_CART = "a.btn-success"
# -------------------------------------------------------------------------------


class ProductPage:
    def __init__(self, page, alerts):
        self.page = page
        self.alerts = alerts

    def name(self):
        return self.page.locator(NAME).inner_text().strip()

    def price(self):
        return money(self.page.locator(PRICE).inner_text())

    def add_to_cart(self):
        mark = self.alerts.mark()
        self.page.locator(ADD_TO_CART, has_text="Add to cart").click()
        assert self.alerts.wait_for("Product added", mark), (
            f"No 'Product added' alert appeared. Alerts seen: {self.alerts.messages[mark:]}"
        )
