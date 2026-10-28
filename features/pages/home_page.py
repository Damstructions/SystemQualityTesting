from pages.util import exact

# ---- Selectors: the only place to edit if the site markup differs ----------
TITLES = "#tbodyid .card-title a"
CATEGORY_LINKS = "a.list-group-item"
NEXT_BUTTON = "#next2"
# -----------------------------------------------------------------------------


class HomePage:
    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url

    def open(self):
        self.page.goto(self.base_url)
        self.page.locator(TITLES).first.wait_for(state="visible")

    def titles(self):
        return [t.strip() for t in self.page.locator(TITLES).all_inner_texts()]

    def _wait_until_list_changes(self, old_titles):
        # The list is replaced via AJAX, so poll until it differs from before
        for _ in range(100):
            now = self.titles()
            if now and now != old_titles:
                return
            self.page.wait_for_timeout(100)
        raise AssertionError("The product list did not change after the click")

    def select_category(self, name):
        old = self.titles()
        self.page.locator(CATEGORY_LINKS, has_text=exact(name)).click()
        self._wait_until_list_changes(old)

    def next_page(self):
        old = self.titles()
        self.page.locator(NEXT_BUTTON).click()
        self._wait_until_list_changes(old)

    def _link(self, name):
        return self.page.locator(TITLES).filter(has_text=exact(name))

    def open_product(self, name):
        """Open a product from the current list, trying the next page if needed."""
        if self._link(name).count() == 0 and self.page.locator(NEXT_BUTTON).is_visible():
            self.next_page()
        assert self._link(name).count() > 0, f"Product '{name}' was not found"
        self._link(name).first.click()
        self.page.locator("h2.name").wait_for(state="visible")
