const { test, expect } = require("@playwright/test");

const { addIPhone, cartRow, convertPriceToNumber } = require("../helpers/cart");

test.describe("TC-RP-CART — Shopping cart", () => {
  test("CART-01 Adding iPhone creates one cart line", async ({ page }) => {
    // Act: add an iPhone and open the shopping cart.
    await addIPhone(page);

    await page.goto("index.php?route=checkout/cart");

    const iPhoneRow = cartRow(page, "iPhone");
    const quantityInput = iPhoneRow.locator("input[name^='quantity']");

    // Assert: one iPhone is present with quantity one.
    await expect(iPhoneRow).toHaveCount(1);
    await expect(quantityInput).toHaveValue("1");
  });

  test("CART-02 Updating quantity to two doubles line total", async ({
    page,
  }) => {
    // Arrange: add one iPhone and record its unit price.
    await addIPhone(page);

    await page.goto("index.php?route=checkout/cart");

    let iPhoneRow = cartRow(page, "iPhone");

    const unitPriceText = await iPhoneRow.locator("td").nth(4).innerText();

    const unitPrice = convertPriceToNumber(unitPriceText);

    // Act: update the product quantity from one to two.
    await iPhoneRow.locator("input[name^='quantity']").fill("2");

    await iPhoneRow.locator("button[data-original-title='Update']").click();

    // Locate the refreshed cart row after the update.
    iPhoneRow = cartRow(page, "iPhone");

    // Assert: quantity is two.
    await expect(iPhoneRow.locator("input[name^='quantity']")).toHaveValue("2");

    const lineTotalText = await iPhoneRow.locator("td").nth(5).innerText();

    const lineTotal = convertPriceToNumber(lineTotalText);

    // Assert: line total equals unit price multiplied by two.
    expect(lineTotal).toBeCloseTo(unitPrice * 2, 2);
  });

  test("CART-03 Removing only product produces empty cart", async ({
    page,
  }) => {
    // Arrange: add an iPhone and open the cart.
    await addIPhone(page);

    await page.goto("index.php?route=checkout/cart");

    const iPhoneRow = cartRow(page, "iPhone");

    // Act: remove the product.
    await iPhoneRow.locator("button[data-original-title='Remove']").click();

    // Assert: the product disappears and the cart is empty.
    await expect(cartRow(page, "iPhone")).toHaveCount(0);

    await expect(page.locator("#content")).toContainText(
      "Your shopping cart is empty!",
    );
  });
});
