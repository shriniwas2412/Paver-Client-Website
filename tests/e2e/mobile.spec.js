// Key pages on a phone: no sideways scroll, quick-action bar visible. Saves a screenshot of each.
const { test, expect } = require("@playwright/test");

const pages = ["", "uses/paver-blocks-for-driveway/", "guides/paver-block-price-bhopal/", "hi/", "hi/products/zig-zag-paver-blocks/", "paver-blocks-indore/", "contact/"];
for (const p of pages) {
  test(`mobile /${p}`, async ({ page }, info) => {
    await page.goto(p);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    expect(overflow).toBeLessThanOrEqual(0);
    await expect(page.locator("nav.mbar")).toBeVisible();
    await page.screenshot({ path: info.outputPath("page.png"), fullPage: false });
  });
}
