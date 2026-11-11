# What we need from Satyam Pavers

The site is built so these sections stay **hidden until real details are filled in**. Nothing is invented. When the client sends any of the items below, fill in the matching setting near the top of `tools/build.py` ("trust facts") and run `python3 tools/build.py`.

| Ask the client for | Setting in `tools/build.py` | Where it shows up |
|---|---|---|
| Office and factory opening hours | `HOURS` | Footer, plus `openingHoursSpecification` in the LocalBusiness schema (Google Maps and search results) |
| Year the business started | `YEARS` | Footer ("Making paver blocks since …") and `foundingDate` in the schema |
| GST number | `GSTIN` | Footer and `taxID` in the schema |
| Sales email address | `EMAIL` | Footer, plus a "Send by email" button on every enquiry form |
| Google Business Profile, IndiaMART, Justdial, Facebook and Instagram links | `SAME_AS` | `sameAs` in the schema, which ties the listings to the site |
| Google review link (GBP → "Ask for reviews") | `GBP_REVIEW_URL` | A "Review us on Google" link under the reviews |
| Google reviews, copied word for word, with the reviewer's name and area | `REVIEWS` | Home page and Bhopal page (English and Hindi) |
| 5–10 finished sites: photo, site name, area of Bhopal, block used, sq ft, year | `PROJECTS` (put the photos in `assets/img/projects/`) | A new `/projects/` page, a home-page strip and a sitemap entry |
| GA4 or Microsoft Clarity ID | `ANALYTICS` | Loads tracking. Call, WhatsApp, enquiry and call-back clicks are already reported as events |
| Custom domain (e.g. satyampavers.in) | `SITE_URL` | Every canonical, sitemap and schema URL |

Example values:

```python
YEARS = 2009
HOURS = {"office": [(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "10:00", "19:00")]}
REVIEWS = [dict(name="R. Sharma", place="Awadhpuri, Bhopal", text="Exact words from Google", rating=5)]
PROJECTS = [dict(site="Green Valley Society", place="Kolar Road, Bhopal", product="zigzag", sqft=12000, year=2025,
                 photo="assets/img/projects/green-valley.webp", note="80 mm grey with red bands")]
```

## Still worth asking
- Does the factory make **grass pavers**, reflective blocks or L-shape blocks? Each one could get its own product page.
- **Test reports** (compressive strength, water absorption) per grade, with lab name and date. With these the site can state IS 15658 compliance.
- Does Satyam Pavers offer **laying**, or supply only? The price guide currently says laying is a separate cost and doesn't claim either way.

## Not checked in this round
- **Lighthouse scores.** Node on the build Mac is the Intel (x64) build, so Lighthouse won't launch Chrome. After deploying, run each key page through https://pagespeed.web.dev.
- **CSP.** GitHub Pages can't send security headers. The site sets a referrer policy by meta tag; a Content-Security-Policy needs a host that allows headers (for example Cloudflare Pages) or a custom domain behind Cloudflare.
