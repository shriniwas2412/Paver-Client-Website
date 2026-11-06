# Google Business Profile — setup guide for Satyam Pavers

**Recommendation: yes, create it.** For searches like "paver blocks near me" or "paver blocks Bhopal", Google shows the map pack (3 businesses with a map) *above* normal results. Local competitors only have thin IndiaMART/Justdial listings with 1–2 reviews, so a complete, well-reviewed profile can reach the top quickly.

You must create and verify it yourself at <https://business.google.com>. It needs your Google account, and Google verifies by video, phone or postcard.

## Make two profiles (one per real location)

| | Profile 1 | Profile 2 |
|---|---|---|
| Business name | Satyam Pavers | Satyam Pavers — Mandideep Factory |
| Address | Kanha Building, Plot No. 190, near Hotel Kanha, near Sargam Cinema, Zone-II, Maharana Pratap Nagar, Bhopal, Madhya Pradesh 462011 | Suveesha Engineers & Industries Pvt. Ltd., Industrial Area, Mandideep, Raisen district, Madhya Pradesh 462046 *(confirm the exact plot/sector and PIN)* |
| Website link | https://shriniwas2412.github.io/Paver-Client-Website/paver-blocks-bhopal/ | https://shriniwas2412.github.io/Paver-Client-Website/paver-blocks-mandideep/ |
| Phone | +91 91711 10110 | +91 91711 10110 |
| Primary category | Concrete product supplier | Concrete product supplier |
| Extra categories | Paving materials supplier, Building materials supplier, Landscaping supply store | Concrete factory (or Manufacturer), Paving materials supplier |
| Service areas | Bhopal, Mandideep, Obedullaganj, Raisen, Sehore, Vidisha, Narmadapuram, Indore | same |

Rules:
- Write the name, address and phone **exactly** as they appear on the website. Any difference weakens ranking.
- Google only allows a second profile if the factory has its own signage and staff during working hours. If it doesn't, create only Profile 1 and mention the factory in the description.
- Fill in real **opening hours**. They aren't on the website yet; send them to me and I'll add them to the site and its schema too.

## Description (750 characters max). Paste this:

> Satyam Pavers makes concrete paver blocks, interlocking tiles, paver tiles and kerb stones at our own factory in Mandideep, near Bhopal. Choose from 13 ranges — zig-zag, I-shape, rectangular, square, cosmic, Combo 5, hexagon 3D tiles, slate finish, anti-skid, cobble stone, speckled finish, paver tiles and kerb stones — in 60, 80 and 100 mm for gardens, home driveways, colony roads, parking and factory yards. Buy factory-direct with colour-matched batches and truck delivery across Bhopal, Raisen, Sehore, Vidisha, Narmadapuram and Indore. Visit our sales office in MP Nagar or send an enquiry on WhatsApp.

## Products section
Add each of the 13 products with the photo and the short description from its product page. Use the **"Learn more"** button linked to that product page. Leave the price field empty.

## Photos to upload (aim for 20+, then add some every month)
1. Logo (`assets/brand/logo-512.png`) and a cover photo (factory or a finished driveway)
2. Outside of the MP Nagar office with the signboard, daytime
3. Inside the office display
4. Factory gate and signboard at Mandideep
5. Production line, moulds, curing yard, stacked pallets
6. Each product close-up (one per range, per colour)
7. **Finished projects**: driveways, colony roads, parking areas you supplied, with the area name in the photo title
8. Trucks loading or delivering

## First 5 posts (one a week)
1. "13 paver ranges made in Mandideep": link to /products/
2. "Which thickness for your driveway? 60 vs 80 vs 100 mm": link to the home page load guide
3. "Monsoon-ready: anti-skid pavers for ramps and poolsides": link to /products/anti-skid-paver-blocks/
4. "Kerb stones for colony roads": link to /products/kerb-stones/
5. A recent project photo + "Send enquiry" button

## Reviews (this matters most for ranking)
- After every delivery, send the customer your review link (GBP → "Ask for reviews" → copy link) on WhatsApp.
- Reply to every review within 2 days, mentioning the product and area (e.g., "Thanks for choosing our grey zig-zag pavers for your Kolar Road driveway").
- Never buy reviews or post fake ones. Google removes them and can suspend the profile.

## Use the same NAP everywhere else
Use the same name, address and phone on: IndiaMART, Justdial, TradeIndia, Bing Places (it feeds ChatGPT/Copilot answers), Apple Business Connect, Facebook and Instagram. Once these exist, send me the links and I'll add them to the site's `sameAs` schema.

## After launch
- Add the site to **Google Search Console** and **Bing Webmaster Tools** and submit `sitemap.xml`. Send me the verification meta tags and I'll add them.
- If you buy a custom domain (e.g., satyampavers.in, recommended), tell me. One line in `tools/build.py` (`SITE_URL`) updates every page.
