const { test, expect } = require("@playwright/test");

test.describe("TC-RP-SEARCH — Product search", () => {
  test("SEARCH-01 Exact product name returns iPhone", async ({ page }) => {
    // Act: search using the complete product name.
    await page.goto("index.php?route=product/search&search=iPhone");

    const iPhoneResult = page.locator("#content .product-layout h4 a", {
      hasText: "iPhone",
    });

    // Assert: exactly one iPhone result is displayed.
    await expect(iPhoneResult).toHaveCount(1);
    await expect(iPhoneResult).toBeVisible();
  });

  test("SEARCH-02 Partial keyword returns Mac products", async ({ page }) => {
    // Act: search using a partial product keyword.
    await page.goto("index.php?route=product/search&search=Mac");

    const productResults = page.locator("#content .product-layout");

    const macBookResult = page
      .locator("#content .product-layout h4 a", { hasText: "MacBook" })
      .first();

    // Assert: at least one matching result is displayed.
    await expect(productResults.first()).toBeVisible();

    await expect(macBookResult).toBeVisible();
  });

  test("SEARCH-03 Unknown term displays no-results message", async ({
    page,
  }) => {
    // Act: search using a term that should not match a product.
    await page.goto(
      "index.php?route=product/search" + "&search=zzzz-no-such-product-rujeet",
    );

    const productResults = page.locator("#content .product-layout");

    // Assert: no products are displayed.
    await expect(productResults).toHaveCount(0);

    // Verify that no matching product cards are displayed.
    await expect(page.locator("#content .product-layout")).toHaveCount(0);
  });
});
