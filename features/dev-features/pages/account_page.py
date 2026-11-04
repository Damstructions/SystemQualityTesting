import re
from urllib.parse import urlsplit

# ---- Selectors ----------------------------------------------------------------
EMAIL = "#input-email"
PASSWORD = "#input-password"
SUBMIT = "#content input[type='submit']"
CONTENT_HEADING = "#content h2"
LOGOUT_LINK = "#column-right a[href*='route=account/logout']"
HEADER_LOGOUT = "#top-links .dropdown-menu a[href*='route=account/logout']"
HEADER_LOGIN = "#top-links .dropdown-menu a[href*='route=account/login']"
LOGGED_OFF = "You have been logged off your account"
STORE_HOST = "opencart.abstracta.us"
# -------------------------------------------------------------------------------


class AccountPage:
    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url.rstrip("/") + "/"

    def _open(self, route):
        self.page.goto(self.base_url + route)

    def open_login(self):
        self._open("index.php?route=account/login")
        self.page.locator(EMAIL).wait_for(state="visible")

    def login(self, email, password):
        self.open_login()
        self.page.locator(EMAIL).fill(email)
        self.page.locator(PASSWORD).fill(password)
        self.page.locator(SUBMIT).click()
        self.page.wait_for_url(re.compile(r"route=account/account"))

    def logout_from_my_account(self):
        link = self.page.locator(LOGOUT_LINK)
        link.wait_for(state="visible")
        link.click()
        self.page.wait_for_url(re.compile(r"route=account/logout"))

    def logon_feedback_shown(self):
        heading = self.page.locator(CONTENT_HEADING).first.inner_text().strip()
        return (
            "route=account/account" in self.page.url
            and heading == "My Account"
            and self.page.locator(HEADER_LOGOUT).count() == 1
        )

    def logout_feedback_shown(self):
        message = self.page.get_by_text(LOGGED_OFF).is_visible()
        return "route=account/logout" in self.page.url and message and self.header_is_logged_out()

    def header_is_logged_out(self):
        return (
            self.page.locator(HEADER_LOGOUT).count() == 0
            and self.page.locator(HEADER_LOGIN).count() == 1
        )

    def shows_no_logon_sign(self):
        on_login = "route=account/login" in self.page.url
        no_account_heading = self.page.locator(CONTENT_HEADING, has_text="My Account").count() == 0
        return on_login and no_account_heading and self.header_is_logged_out()

    def session_cookie(self, browser_context):
        for cookie in browser_context.cookies():
            if cookie["name"] == "OCSESSID":
                return cookie["value"]
        raise AssertionError("Login did not store OCSESSID")

    def delete_chrome_cookies_and_site_data(self, browser_context):
        """Clear this site's cookies before the next navigation.

        Storage.clearDataForOrigin removes the host-only session cookie and
        leaves Domain cookies such as language and currency. Those remaining
        cookies are deleted from Chrome's cookie store as well.
        """
        parts = urlsplit(self.page.url)
        origin = f"{parts.scheme}://{parts.netloc}"
        client = browser_context.new_cdp_session(self.page)
        try:
            client.send("Storage.clearDataForOrigin", {"origin": origin, "storageTypes": "all"})
            held = client.send("Network.getAllCookies")
            for cookie in held["cookies"]:
                domain = cookie.get("domain", "")
                if not domain.endswith(STORE_HOST):
                    continue
                client.send(
                    "Network.deleteCookies",
                    {"name": cookie["name"], "domain": domain, "path": cookie.get("path", "/")},
                )
        finally:
            client.detach()

    def reload(self):
        self.page.reload(wait_until="domcontentloaded")
