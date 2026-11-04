const { expect } = require("@playwright/test");

async function register(page, email, password) {
  await page.goto("index.php?route=account/register");

  await page.locator("#input-firstname").fill("Rujeet");
  await page.locator("#input-lastname").fill("Prajapati");
  await page.locator("#input-email").fill(email);
  await page.locator("#input-telephone").fill("0400000000");
  await page.locator("#input-password").fill(password);
  await page.locator("#input-confirm").fill(password);

  await page.locator("input[name='newsletter'][value='0']").check();

  await page.locator("input[name='agree']").check();

  await page.locator("#content input[type='submit']").click();

  await expect(page).toHaveURL(/route=account\/success/);
}

async function logout(page) {
  await page.goto("index.php?route=account/logout");

  await expect(
    page.getByText("You have been logged off your account"),
  ).toBeVisible();
}

async function login(page, email, password) {
  await page.goto("index.php?route=account/login");

  await page.locator("#input-email").fill(email);
  await page.locator("#input-password").fill(password);

  await page.locator("#content input[type='submit']").click();
}

module.exports = {
  register,
  logout,
  login,
};
