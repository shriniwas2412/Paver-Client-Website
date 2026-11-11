// Calculator: blocks per m² (from tools/build.py CALC) × area × 1.05 wastage, rounded up.
const { test, expect } = require("@playwright/test");

const cases = [
  { label: "Rectangular 200×100 mm", l: 20, w: 10, u: "ft", sqm: 200 * 0.0929, perSqm: 50 },
  { label: "Zig-Zag (Uni) interlocking", l: 20, w: 30, u: "ft", sqm: 600 * 0.0929, perSqm: 40 },
  { label: "I-Shape (Behaton)", l: 10, w: 5, u: "m", sqm: 50, perSqm: 39 },
];
for (const c of cases) {
  test(`calculator: ${c.label} ${c.l}×${c.w} ${c.u}`, async ({ page }) => {
    await page.goto("tools/paver-calculator/");
    const f = page.locator("#calc");
    await f.locator('[name="b"]').selectOption({ label: c.label });
    await f.locator('[name="u"]').selectOption(c.u);
    await f.locator('[name="l"]').fill(String(c.l));
    await f.locator('[name="w"]').fill(String(c.w));
    const n = Math.ceil(c.sqm * c.perSqm * 1.05);
    await expect(page.locator("#c-blocks")).toHaveText(n.toLocaleString("en-IN"));
    await expect(page.locator("#c-sqft")).toHaveText(String(Math.round(c.sqm * 10.764)));
    const wa = decodeURIComponent(await page.locator("#c-wa").getAttribute("href"));
    expect(wa).toContain(`I need about ${n} ${c.label} blocks`);
  });
}
