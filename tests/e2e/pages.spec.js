// SEO basics on every page in the sitemap, plus a link check across the whole site.
const { test, expect } = require("@playwright/test");
const { sitemapPaths, SITE_URL } = require("./helpers");

const paths = sitemapPaths();
test.describe.configure({ mode: "parallel" });

for (const p of paths) {
  test(`page /${p}`, async ({ page }) => {
    const res = await page.goto(p);
    expect(res.status()).toBe(200);
    await expect(page.locator("h1")).toHaveCount(1);
    expect((await page.title()).length).toBeGreaterThan(10);
    const desc = await page.locator('meta[name="description"]').getAttribute("content");
    expect(desc && desc.length).toBeGreaterThan(50);
    expect(await page.locator('link[rel="canonical"]').getAttribute("href")).toBe(SITE_URL + p);
    // every JSON-LD block parses and has a @graph
    for (const raw of await page.locator('script[type="application/ld+json"]').allTextContents()) {
      const data = JSON.parse(raw);
      expect(Array.isArray(data["@graph"])).toBeTruthy();
    }
    // hreflang pairs point back at each other
    const alts = await page.locator('link[rel="alternate"][hreflang]').evaluateAll(ls => ls.map(l => [l.hreflang, l.href]));
    if (alts.length) {
      expect(alts.map(a => a[0]).sort()).toEqual(["en-IN", "hi-IN", "x-default"]);
      expect(alts.some(a => a[1] === SITE_URL + p)).toBeTruthy();
    }
    // images have alt text
    expect(await page.locator("img:not([alt])").count()).toBe(0);
    // external links opened in a new tab carry rel=noopener
    expect(await page.locator('a[target="_blank"]:not([rel*="noopener"])').count()).toBe(0);
  });
}

test("every internal link resolves", async ({ page, request }) => {
  const seen = new Set();
  for (const p of paths) {
    await page.goto(p);
    const hrefs = await page.locator("a[href]").evaluateAll(as => as.map(a => a.href));
    for (const h of hrefs) {
      const u = new URL(h);
      if (u.origin === new URL(page.url()).origin) seen.add(u.pathname);
    }
  }
  const broken = [];
  for (const pathname of seen) {
    const r = await request.get(pathname);
    if (r.status() !== 200) broken.push(`${pathname} → ${r.status()}`);
  }
  expect(broken).toEqual([]);
});
