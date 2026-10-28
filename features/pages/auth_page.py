# ---- Selectors ----------------------------------------------------------------
SIGNUP_LINK = "#signin2"
LOGIN_LINK = "#login2"
SIGNUP_MODAL = "#signInModal"
LOGIN_MODAL = "#logInModal"
WELCOME = "#nameofuser"
# -------------------------------------------------------------------------------


class AuthPage:
    def __init__(self, page, alerts):
        self.page = page
        self.alerts = alerts

    def sign_up(self, username, password):
        mark = self.alerts.mark()
        self.page.locator(SIGNUP_LINK).click()
        self.page.locator(SIGNUP_MODAL).locator("#sign-username").wait_for(state="visible")
        self.page.fill("#sign-username", username)
        self.page.fill("#sign-password", password)
        self.page.locator(SIGNUP_MODAL).get_by_role("button", name="Sign up").click()
        return mark

    def log_in(self, username, password):
        mark = self.alerts.mark()
        self.page.locator(LOGIN_LINK).click()
        self.page.locator(LOGIN_MODAL).locator("#loginusername").wait_for(state="visible")
        self.page.fill("#loginusername", username)
        self.page.fill("#loginpassword", password)
        self.page.locator(LOGIN_MODAL).get_by_role("button", name="Log in").click()
        return mark

    def welcome_text(self):
        loc = self.page.locator(WELCOME)
        loc.wait_for(state="visible")
        return loc.inner_text().strip()
