const { test, expect } = require("@playwright/test");

const { PASSWORD, uniqueEmail } = require("../helpers/test-data");

const { register, logout, login } = require("../helpers/account");

test.describe("TC-RP-LOGIN — Customer login", () => {
  test("LOGIN-01 Valid credentials open My Account", async ({ page }) => {
    const email = uniqueEmail();

    // Arrange: create an independent test account.
    await register(page, email, PASSWORD);
    await logout(page);

    // Act: log in using valid credentials.
    await login(page, email, PASSWORD);

    // Assert: the customer account page is displayed.
    await expect(page).toHaveURL(/route=account\/account/);

    await expect(page.locator("#content h2").first()).toHaveText("My Account");

    await expect(
      page.locator("#column-right a[href*='route=account/logout']"),
    ).toBeVisible();
  });

  test("LOGIN-02 Incorrect password is rejected", async ({ page }) => {
    const email = uniqueEmail();

    // Arrange: create a valid account and sign out.
    await register(page, email, PASSWORD);
    await logout(page);

    // Act: attempt login using an incorrect password.
    await login(page, email, "IncorrectPassword99!");

    // Assert: login is rejected with a warning.
    await expect(page).toHaveURL(/route=account\/login/);

    await expect(page.locator("#account-login .alert-danger")).toContainText(
      "No match for E-Mail Address and/or Password",
    );
  });

  test("LOGIN-03 Unregistered email is rejected", async ({ page }) => {
    const unregisteredEmail = uniqueEmail();

    // Act: attempt login with an email that was never registered.
    await login(page, unregisteredEmail, PASSWORD);

    // Assert: access is rejected.
    await expect(page).toHaveURL(/route=account\/login/);

    await expect(page.locator("#account-login .alert-danger")).toContainText(
      "No match for E-Mail Address and/or Password",
    );
  });
});
