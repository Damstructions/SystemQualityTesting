const { expect } = require("@playwright/test");

async function addIPhone(page) {
  await page.goto("index.php?route=product/product&product_id=40");

  await expect(page.locator("#content h1")).toHaveText("iPhone");

  await page.locator("#button-cart").click();

  await expect(page.locator(".alert-success")).toContainText("iPhone");
}

function cartRow(page, productName) {
  return page
    .locator("#content form table tbody tr")
    .filter({ hasText: productName });
}

function convertPriceToNumber(priceText) {
  return Number(priceText.replace(/[^0-9.]/g, ""));
}

module.exports = {
  addIPhone,
  cartRow,
  convertPriceToNumber,
};
