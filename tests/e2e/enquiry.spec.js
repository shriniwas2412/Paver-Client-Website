// Enquiry and call-back forms build the right WhatsApp message and always show the fallback panel.
const { test, expect } = require("@playwright/test");

async function stubOpen(page) {
  await page.addInitScript(() => { window.__opened = []; window.open = u => { window.__opened.push(u); return null; }; });
}

test("enquiry form needs name and mobile", async ({ page }) => {
  await stubOpen(page);
  await page.goto("contact/");
  await page.locator("form.enq button[type=submit]").click();
  await expect(page.locator("#toast")).toHaveText(/name and mobile/);
  await expect(page.locator(".enq-done")).toBeHidden();
});

test("enquiry form opens WhatsApp and shows the fallback panel", async ({ page }) => {
  await stubOpen(page);
  await page.goto("contact/");
  const f = page.locator("form.enq");
  await f.locator('[name="name"]').fill("Test Buyer");
  await f.locator('[name="phone"]').fill("9000000000");
  await f.locator('[name="product"]').selectOption({ label: "Zig-Zag (Uni) Interlocking Paver Blocks" });
  await f.locator('[name="area"]').fill("600");
  await f.locator('[name="city"]').fill("Kolar Road, Bhopal");
  await f.locator("button[type=submit]").click();
  const opened = await page.evaluate(() => window.__opened);
  expect(opened).toHaveLength(1);
  const text = decodeURIComponent(new URL(opened[0]).searchParams.get("text"));
  expect(text).toContain("Name: Test Buyer");
  expect(text).toContain("Mobile: 9000000000");
  expect(text).toContain("Product: Zig-Zag (Uni) Interlocking Paver Blocks");
  expect(text).toContain("Area (sq ft): 600");
  expect(text).toContain("Site location: Kolar Road, Bhopal");
  const panel = f.locator(".enq-done");
  await expect(panel).toBeVisible();
  await expect(panel.locator("pre")).toContainText("Name: Test Buyer");
  await expect(panel.getByRole("link", { name: "Open WhatsApp" })).toHaveAttribute("href", opened[0]);
  await expect(panel.locator('a[href^="tel:"]')).toBeVisible();
  await expect(panel.getByRole("button", { name: "Copy message" })).toBeVisible();
});

test("call-back form on a product page", async ({ page }) => {
  await stubOpen(page);
  await page.goto("products/zig-zag-paver-blocks/");
  const f = page.locator("form.cb");
  await f.locator('[name="phone"]').fill("9000000001");
  await f.locator("button[type=submit]").click();
  const text = decodeURIComponent(new URL((await page.evaluate(() => window.__opened))[0]).searchParams.get("text"));
  expect(text).toBe("Hello Satyam Pavers, please call me back about Zig-Zag (Uni) Interlocking Paver Blocks.\nMobile: 9000000001");
  await expect(f.locator(".enq-done")).toBeVisible();
});

test("Hindi form shows Hindi fallback text", async ({ page }) => {
  await stubOpen(page);
  await page.goto("hi/");
  const f = page.locator("form.enq:not(.cb)");
  await f.locator('[name="name"]').fill("परीक्षण");
  await f.locator('[name="phone"]').fill("9000000002");
  await f.locator("button[type=submit]").click();
  await expect(f.locator(".enq-done")).toContainText("आपकी पूछताछ तैयार है");
});
