from playwright.sync_api import TimeoutError as PWTimeout

class HomePage:
    RESULT = ".product-thumb h4 a"

    def __init__(self, page, base_url):
        self.page, self.base_url = page, base_url

    def open(self):
        self.page.goto(self.base_url)

    def search(self, term):
        self.page.fill("input[name='search']", term)
        with self.page.expect_navigation():          # wait for the results page
            self.page.keyboard.press("Enter")

    def result_titles(self):
        try:
            self.page.wait_for_selector(self.RESULT, timeout=5000)
        except PWTimeout:
            return []                                # no results is a valid outcome
        return self.page.locator(self.RESULT).all_inner_texts()

    def no_results_message_visible(self):
        msg = self.page.get_by_text("no product", exact=False).first
        try:
            msg.wait_for(state="visible", timeout=5000)
            return True
        except PWTimeout:
            return False