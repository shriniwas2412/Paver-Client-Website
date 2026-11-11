const fs = require("fs");
const path = require("path");
const ROOT = path.join(__dirname, "..", "..");
const SITE_URL = "https://shriniwas2412.github.io/Paver-Client-Website/";
/** Every page in sitemap.xml, as a path relative to the site root (e.g. "products/"). */
function sitemapPaths() {
  const xml = fs.readFileSync(path.join(ROOT, "sitemap.xml"), "utf8");
  return [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1].replace(SITE_URL, ""));
}
module.exports = { sitemapPaths, SITE_URL };
