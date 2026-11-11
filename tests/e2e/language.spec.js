// The Hindi button goes to the matching page when one exists, and translates labels in place otherwise.
const { test, expect } = require("@playwright/test");

test("Bhopal page ⇄ Hindi page", async ({ page }) => {
  await page.goto("paver-blocks-bhopal/");
  await expect(page.locator("html")).toHaveAttribute("lang", "en");
  await page.locator("#langBtn").click();
  await expect(page).toHaveURL(/\/hi\/$/);
  await expect(page.locator("html")).toHaveAttribute("lang", "hi");
  await expect(page.locator("h1")).toHaveText("भोपाल में पेवर ब्लॉक");
  await page.locator("#langBtn").click();
  await expect(page).toHaveURL(/\/paver-blocks-bhopal\/$/);
});

test("Hindi product page pairs with the English one", async ({ page }) => {
  await page.goto("hi/products/zig-zag-paver-blocks/");
  await page.locator("#langBtn").click();
  await expect(page).toHaveURL(/\/products\/zig-zag-paver-blocks\/$/);
  await expect(page.locator("h1")).toHaveText("Zig-Zag (Uni) Interlocking Paver Blocks");
});

test("page without a Hindi twin translates labels in place", async ({ page }) => {
  await page.goto("contact/");
  await page.locator("#langBtn").click();
  await expect(page).toHaveURL(/\/contact\/$/);
  await expect(page.locator('nav.menu a[data-i18n="nav.products"]')).toHaveText("उत्पाद");
});
