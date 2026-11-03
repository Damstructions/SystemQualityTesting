import time


class StorePage:
    """DemoBlaze helpers for sign-up, log-in, log-out and catalogue paging."""

    def __init__(self, page):
        self.page = page
        self.alerts = []
        page.on("dialog", self._accept_dialog)

    def _accept_dialog(self, dialog):
        self.alerts.append(dialog.message)
        dialog.accept()

    def last_alert(self):
        return self.alerts[-1] if self.alerts else ""

    def wait_for_alert(self, mark, timeout=8000):
        waited = 0
        while waited <= timeout:
            if len(self.alerts) > mark:
                return self.alerts[-1]
            self.page.wait_for_timeout(100)
            waited += 100
        raise AssertionError("No native alert appeared")

    def product_titles(self):
        return [text.strip() for text in self.page.locator("#tbodyid .card-title a").all_inner_texts()]

    def wait_for_catalogue(self):
        self.page.locator("#tbodyid .card-title a").first.wait_for(state="visible")

    def wait_until_titles_change(self, old_titles):
        for _ in range(100):
            now = self.product_titles()
            if now and now != old_titles:
                return now
            self.page.wait_for_timeout(100)
        raise AssertionError("The product list did not change")

    def go_to_next_page(self):
        old = self.product_titles()
        self.page.locator("#next2").click()
        return self.wait_until_titles_change(old)

    def go_to_previous_page(self):
        old = self.product_titles()
        self.page.locator("#prev2").click()
        return self.wait_until_titles_change(old)

    def unique_username(self, prefix="zy"):
        return f"{prefix}_{int(time.time() * 1000)}"

    def dismiss_backdrops(self):
        self.page.evaluate(
            """() => {
                document.querySelectorAll('.modal-backdrop').forEach((el) => el.remove());
                document.body.classList.remove('modal-open');
            }"""
        )

    def open_signup(self):
        self.dismiss_backdrops()
        self.page.locator("#signin2").click(force=True)
        self.page.locator("#signInModal.show").wait_for(state="visible")
        self.page.locator("#sign-username").wait_for(state="visible")

    def signup_modal(self):
        return self.page.locator("#signInModal")

    def fill_signup(self, username, password):
        self.page.fill("#sign-username", "")
        self.page.fill("#sign-password", "")
        self.page.fill("#sign-username", username)
        self.page.fill("#sign-password", password)

    def submit_signup(self):
        mark = len(self.alerts)
        self.signup_modal().locator("button.btn-primary", has_text="Sign up").click(force=True)
        return self.wait_for_alert(mark)

    def sign_up(self, username, password):
        self.open_signup()
        self.fill_signup(username, password)
        return self.submit_signup()

    def close_signup(self):
        self.signup_modal().locator(".modal-footer button.btn-secondary", has_text="Close").click(force=True)
        self.page.wait_for_timeout(400)
        if "show" in (self.signup_modal().get_attribute("class") or ""):
            self.signup_modal().locator(".modal-header button.close").click(force=True)
            self.page.wait_for_timeout(400)
        self.dismiss_backdrops()

    def open_login(self):
        self.dismiss_backdrops()
        self.page.locator("#login2").click(force=True)
        self.page.locator("#logInModal.show").wait_for(state="visible")
        self.page.locator("#loginusername").wait_for(state="visible")

    def log_in(self, username, password):
        self.open_login()
        self.page.fill("#loginusername", username)
        self.page.fill("#loginpassword", password)
        self.page.locator("#logInModal button.btn-primary", has_text="Log in").click(force=True)
        self.page.locator("#nameofuser").wait_for(state="visible")

    def welcome_text(self):
        loc = self.page.locator("#nameofuser")
        loc.wait_for(state="visible")
        return loc.inner_text().strip()

    def log_out(self):
        self.page.locator("#logout2").click()
        self.page.locator("#login2").wait_for(state="visible")

    def register_and_login(self, username=None, password="Passw0rd!QA"):
        username = username or self.unique_username()
        message = self.sign_up(username, password)
        if "successful" not in message.lower():
            raise AssertionError("Sign up failed: %s" % message)
        self.close_signup()
        self.log_in(username, password)
        return username
