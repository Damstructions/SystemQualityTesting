class TestSignUpDialog:
    """T015 / F17 DemoBlaze Sign-up validation and dismiss"""

    def test_empty_sign_up_is_rejected(self, store):
        store.open_signup()
        store.fill_signup("", "")
        message = store.submit_signup()
        assert "Please fill out Username and Password." in message
        assert "show" in (store.signup_modal().get_attribute("class") or "")
        assert store.page.locator("#login2").is_visible()

    def test_existing_username_is_rejected(self, store):
        username = store.unique_username("exist")
        first = store.sign_up(username, "Passw0rd!QA")
        assert "Sign up successful." in first
        store.close_signup()

        second = store.sign_up(username, "Passw0rd!QA")
        assert "This user already exist." in second
        assert store.page.locator("#login2").is_visible()
        assert not store.page.locator("#logout2").is_visible()

    def test_close_does_not_create_a_session(self, store):
        store.open_signup()
        store.fill_signup(store.unique_username("close"), "Passw0rd!QA")
        store.close_signup()

        assert store.page.locator("#login2").is_visible()
        assert store.page.locator("#signin2").is_visible()
        assert "Welcome" not in store.page.locator("#nameofuser").inner_text()
