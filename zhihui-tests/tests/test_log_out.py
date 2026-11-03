class TestLogOut:
    """T014 / F16 DemoBlaze Log Out"""

    def test_logout_returns_to_guest_navigation(self, store):
        username = store.register_and_login()
        assert username in store.welcome_text()
        assert store.page.locator("#logout2").is_visible()

        store.log_out()

        assert store.page.locator("#login2").is_visible()
        assert store.page.locator("#signin2").is_visible()
        assert not store.page.locator("#logout2").is_visible()
        assert username not in store.page.locator("#nameofuser").inner_text()

    def test_logout_survives_refresh(self, store):
        store.register_and_login()
        store.log_out()
        store.page.reload()
        store.page.wait_for_selector("#nava")

        assert store.page.locator("#login2").is_visible()
        assert not store.page.locator("#logout2").is_visible()
        assert "Welcome" not in store.page.locator("#nameofuser").inner_text()

    def test_logout_does_not_keep_welcome_on_home(self, store):
        username = store.register_and_login()
        store.log_out()
        store.page.locator(".navbar-nav a.nav-link", has_text="Home").click()
        store.wait_for_catalogue()

        assert store.page.locator("#login2").is_visible()
        assert store.product_titles()
        assert username not in store.page.locator("#nameofuser").inner_text()
