#!/usr/bin/env python3
"""Builds the static Satyam Pavers site.

All business facts (contact, locations, products, FAQs) live in this file, so the
phone number and addresses are written in exactly one place. Run from the repo root:

    python3 tools/build.py

It writes index.html, products/*/index.html, the location and contact pages,
assets/js/data.js, sitemap.xml, robots.txt and llms.txt. Home page markup comes
from src/home.html.
"""
import html, json, os, datetime

SITE_URL = "https://shriniwas2412.github.io/Paver-Client-Website/"  # change when a custom domain is added
TODAY = datetime.date.today().isoformat()
BRAND = "Satyam Pavers"
LEGAL = "Suveesha Engineers & Industries Pvt. Ltd."

# ---------- contact: the only place the number is written ----------
CONTACT = {"display": "+91 91711 10110", "tel": "+919171110110", "wa": "919171110110"}

LOCATIONS = [
    {"id": "office", "slug": "paver-blocks-bhopal", "role": "Sales office", "name": "Satyam Pavers — Sales Office, MP Nagar",
     "street": "Kanha Building, Plot No. 190, near Hotel Kanha, near Sargam Cinema, Zone-II",
     "locality": "Maharana Pratap Nagar, Bhopal", "city": "Bhopal", "pin": "462011",
     "maps": "Kanha Building, Plot No. 190, Zone-II, MP Nagar, Bhopal 462011"},
    {"id": "factory", "slug": "paver-blocks-mandideep", "role": "Factory", "name": "Satyam Pavers — Factory, Mandideep (Suveesha Engineers & Industries)",
     "street": "Suveesha Engineers & Industries Pvt. Ltd., Industrial Area",
     "locality": "Mandideep, Raisen district", "city": "Mandideep", "pin": "462046",
     "maps": "Suveesha Engineers & Industries, Mandideep, Madhya Pradesh"},
]
def addr_line(l): return f'{l["street"]}, {l["locality"]}, Madhya Pradesh {l["pin"]}'

AREAS = ["Bhopal", "Mandideep", "Obedullaganj", "Raisen", "Sehore", "Vidisha", "Narmadapuram", "Indore"]

# ---------- products (sizes and counts are typical values; confirm with the factory) ----------
PRODUCTS = [
  dict(id="rectangular", slug="rectangular-paver-blocks", code="RC", name="Rectangular", full="Rectangular Paver Blocks", alt="Brick-shaped paver", uses=["walk","drive","heavy"], c="grey",
       desc="Classic and versatile. Herringbone for driveways that take turning cars, running bond for paths, basket weave for courtyards.",
       size="200 × 100 mm", thick=[60,80,100], per=4.6, load="Foot to heavy", patterns=["herringbone","bond","basket","stack"],
       best=["Home driveways and porches","Colony roads and car parks","Factory yards (100 mm)"],
       answer="Rectangular paver blocks are 200 × 100 mm concrete blocks made in 60, 80 and 100 mm thickness. Laid in herringbone they handle cars and turning wheels; laid in running bond or basket weave they suit paths and courtyards. About 4.6 blocks cover one square foot."),
  dict(id="zigzag", slug="zig-zag-paver-blocks", code="ZZ", name="Zig-Zag", full="Zig-Zag (Uni) Interlocking Paver Blocks", alt="Interlocking wave paver, also called a uni paver", uses=["drive","heavy"], c="red",
       desc="Also sold as the uni paver, and the most popular block in Bhopal. Wavy edges lock into the next block on every side, so the surface stays put under braking and turning wheels.",
       size="225 × 112 mm", thick=[60,80,100], per=3.9, load="Cars to heavy", patterns=["zig"],
       best=["Home driveways and society roads","Petrol pumps and parking areas","Industrial yards and roads (100 mm)"],
       answer="Zig-zag paver blocks, also called uni pavers, are 225 × 112 mm interlocking concrete blocks with wavy edges that lock on all sides. They come in 60, 80 and 100 mm and in grey, red, black, brown and yellow. About 3.9 blocks cover one square foot."),
  dict(id="ishape", slug="i-shape-paver-blocks", code="IS", name="I-Shape", full="I-Shape (Behaton / Dumbbell) Paver Blocks", alt="Dumbbell interlocking paver, also called a Behaton paver", uses=["drive","heavy"], c="grey",
       desc="Known on site as the Behaton or dumbbell block. The I profile locks into its neighbours on four sides and spreads wheel loads, from society roads to truck yards.",
       size="200 × 165 mm", thick=[60,80,100], per=3.6, load="Cars to very heavy", patterns=["ishape"],
       best=["Society internal roads and footpaths","Commercial walkways and parking","Truck yards and warehouses (100 mm)"],
       answer="I-shape paver blocks, also called Behaton or dumbbell pavers, are 200 × 165 mm interlocking blocks that spread wheel loads across the floor. In 80 and 100 mm they suit truck yards, bus stands and warehouses; 60 mm suits home driveways. About 3.6 blocks cover one square foot."),
  dict(id="square", slug="square-paver-blocks", code="SQ", name="Square", full="Square Paver Blocks", alt="Plain square paver", uses=["walk","drive"], c="grey",
       desc="Clean and symmetrical. A calm surface for paths, courtyards and terraces, laid in a grid or staggered.",
       size="200 × 200 mm", thick=[60,80], per=2.3, load="Foot to light", patterns=["grid","staggered"],
       best=["Courtyards and terraces","Garden paths","Light-traffic driveways (80 mm)"],
       answer="Square paver blocks are 200 × 200 mm concrete blocks in 60 and 80 mm thickness, laid in a grid or staggered. They suit courtyards, terraces and garden paths. About 2.3 blocks cover one square foot."),
  dict(id="combo5", slug="combo-5-series-pavers", code="C5", name="Combo 5 Series", full="Combo 5 Series Paver Set", alt="Five-piece paver set", uses=["walk","drive"], c="yellow",
       desc="Five block sizes laid together for a random, stone-like look. Mix two colours for a richer finish.",
       size="Set of 5 blocks", thick=[60,80], per=None, perSet=2, load="Foot to light", patterns=["combo5"],
       best=["Garden and villa driveways","Clubhouse and resort paths","Courtyards with a natural-stone look"],
       answer="The Combo 5 Series is a set of five block sizes laid together for a random, natural-stone look. It comes in 60 and 80 mm; one set covers about 2 square feet. Mixing two colours gives a richer finish."),
  dict(id="cosmic", slug="cosmic-paver-blocks", code="CS", name="Cosmic", full="Cosmic Paver Blocks", alt="Curved three-arm interlocking paver", uses=["walk","drive"], c="yellow", noRender=True, lay="Interlocking, laid in flowing rows",
       desc="Three curved arms lock into each other for a flowing, decorative floor. The dotted face gives a sure grip underfoot.",
       size="On request", thick=[60,80], per=None, load="Foot to light", patterns=[],
       best=["Temple and school courtyards","Society walkways","Decorative driveways"],
       answer="Cosmic paver blocks have three curved arms that lock together in flowing rows. The dotted face gives grip underfoot. They come in 60 and 80 mm, in red and yellow, for courtyards, walkways and decorative driveways."),
  dict(id="hexagon", slug="hexagon-3d-paver-tiles", code="HX", name="Hexagon Tile", full="Hexagon 3D-Cube Paver Tiles", alt="Grooved 3D-cube hexagon tile", uses=["walk"], c="grey", noRender=True, lay="Hexagon grid (3D-cube effect)",
       desc="A hexagon with three grooved faces that read as a 3D cube when laid. The honeycomb layout spreads foot traffic evenly, so it suits wide walkways, parks and plazas as well as terraces and lobbies.",
       size="On request", thick=[], per=None, load="Foot traffic", patterns=[],
       best=["Wide walkways, parks and plazas","Building entrances and lobbies","Terraces and feature pathways"],
       answer="Hexagon 3D-cube paver tiles have three grooved faces that read as a cube when laid together in a honeycomb. They suit wide walkways, parks, plazas, building entrances and terraces with foot traffic."),
  dict(id="slate", slug="slate-finish-paver-slabs", code="SL", name="Slate Finish Slab", full="Slate Finish Paver Slabs", alt="Natural slate texture", uses=["walk"], c="grey", noRender=True, lay="Grid or staggered",
       desc="A moulded natural-slate face with soft ripples and veins. Looks like split stone for a fraction of the cost.",
       size="On request", thick=[], per=None, load="Foot traffic", patterns=[],
       best=["Garden paths and patios","Poolside decks","Farmhouse and villa landscaping"],
       answer="Slate finish paver slabs have a moulded natural-slate face with ripples and veins, in grey and black. They give a split-stone look for garden paths, patios and poolsides."),
  dict(id="antiskid", slug="anti-skid-paver-blocks", code="AS", name="Anti-Skid Block", full="Anti-Skid Paver Blocks", alt="Leather-grain grip surface", uses=["walk","drive"], c="grey", noRender=True, lay="Stretcher bond or grid",
       desc="A fine leather-grain face that stays grippy when wet. Made for ramps, steps, poolsides and monsoon walkways.",
       size="On request", thick=[], per=None, load="Foot to light", patterns=[],
       best=["Ramps and steps","Poolsides","Hospital and school walkways"],
       answer="Anti-skid paver blocks have a fine leather-grain face that stays grippy when wet. They are made for ramps, steps, poolsides and walkways that see heavy monsoon rain."),
  dict(id="cobble", slug="cobble-stone-pavers", code="CB", name="Cobble Stone", full="Cobble Stone Pavers", alt="Rough split-face cobble", uses=["walk","drive"], c="beige", noRender=True, lay="Random rows or fan arcs",
       desc="Chunky cobbles with a rough split face for heritage driveways, courtyards, tree surrounds and landscape edging.",
       size="On request", thick=[], per=None, load="Foot to light", patterns=[],
       best=["Heritage-style driveways","Tree surrounds and edging","Hotel and resort courtyards"],
       answer="Cobble stone pavers are chunky concrete cobbles with a rough split face, in beige and black. They suit heritage-style driveways, courtyards, tree surrounds and landscape edging."),
  dict(id="speckled", slug="speckled-finish-paver-blocks", code="SP", name="Speckled Finish Block", full="Speckled Finish Paver Blocks", alt="Exposed-chip terrazzo look", uses=["walk"], c="grey", noRender=True, lay="Grid or staggered",
       desc="A smooth face scattered with stone chips, like terrazzo. A refined finish for lobbies, terraces and clubhouse paths.",
       size="On request", thick=[], per=None, load="Foot traffic", patterns=[],
       best=["Lobbies and porches","Terraces","Clubhouse paths"],
       answer="Speckled finish paver blocks have a smooth face scattered with stone chips, like terrazzo. They suit lobbies, porches, terraces and clubhouse paths."),
  dict(id="curved", slug="kerb-stones", code="CK", name="Kerb Stones", full="Concrete Kerb Stones", alt="Straight and curved kerbs", uses=["edge"], c="grey",
       desc="Kerbs hold the paving in place and give it a clean edge along roads, driveways, roundabouts, tree rings and garden beds.",
       size="On request", thick=[], per=None, load="Edging", patterns=[],
       best=["Road and colony edges","Driveway and parking edges","Roundabouts, medians and garden beds"],
       answer="Concrete kerb stones edge roads, driveways, parking areas, medians and garden beds, and hold paver blocks in place. They are made in straight and curved profiles and are supplied by the running foot."),
  dict(id="tiles", slug="paver-tiles", code="PT", name="Paver Tiles", full="Concrete Paver Tiles", alt="Textured paving tile", uses=["walk"], c="yellow",
       desc="Flat tiles with a moulded face, from brick-weave to rock-face, laid on mortar for a neat finished surface.",
       size="300 × 300 mm", thick=[25,30], per=1.0, load="Foot traffic", patterns=["tiles"],
       best=["Terraces and parking sheds","Footpaths","Building surrounds"],
       answer="Concrete paver tiles are 300 × 300 mm flat tiles, 25 or 30 mm thick, laid on mortar. Faces include brick-weave, four-square and nine-square rock-face, in yellow, red and grey. One tile covers about one square foot."),
]
# colours seen in the factory's own photos (used for colour lists only; the raw photos are not published)
PHOTOS = {
  "rectangular":[{"f":"rect-grey","c":"grey","cap":"Grey rectangular blocks"}],
  "zigzag":[{"f":"zigzag-grey","c":"grey","cap":"Grey zig-zag, 60 mm"},{"f":"zigzag-red","c":"red","cap":"Red zig-zag with grip face"},{"f":"zigzag-blackbrown","c":"black","cap":"Black and brown zig-zag"}],
  "ishape":[{"f":"ishape-red","c":"red","cap":"Red I-shape with grip face"}],
  "square":[{"f":"square-grey","c":"grey","cap":"Grey square block"}],
  "slate":[{"f":"slate-grey","c":"grey","cap":"Grey slate-finish slab"},{"f":"slate-black","c":"black","cap":"Black slate-finish slab, close-up"}],
  "antiskid":[{"f":"antiskid-stack","c":"grey","cap":"Grey anti-skid blocks"},{"f":"antiskid-pair","c":"black","cap":"Black and grey anti-skid blocks"}],
  "cobble":[{"f":"cobble-beige","c":"beige","cap":"Beige split-face cobble"},{"f":"cobble-black","c":"black","cap":"Black split-face cobble"}],
  "speckled":[{"f":"speckled-slab","c":"grey","cap":"Speckled finish block"}],
  "cosmic":[{"f":"cosmic-yellow","c":"yellow","cap":"Yellow cosmic paver"},{"f":"cosmic-red","c":"red","cap":"Red cosmic paver"}],
  "hexagon":[{"f":"hexagon-grey","c":"grey","cap":"Grooved hexagon tile"},{"f":"hexagon-stack","c":"grey","cap":"Hexagon tile with grey blocks"}],
  "curved":[{"f":"kerb-closeup","c":"grey","cap":"Kerb stone, 200 mm"},{"f":"kerb-lineup","c":"grey","cap":"Kerb stone range"}],
  "tiles":[{"f":"tile-yellow","c":"yellow","cap":"Yellow brick-weave tile"},{"f":"tile-red","c":"red","cap":"Red four-square rock-face tile"},{"f":"tile-rockface","c":"grey","cap":"Grey nine-square rock-face tile"}],
}
COLOURS = {"grey":"Grey","red":"Red","yellow":"Yellow","orange":"Orange","black":"Black","brown":"Brown","beige":"Beige"}
HEX = {"grey":"#85837D","red":"#9E4732","yellow":"#C79B4B","orange":"#BF6B3D","black":"#2B2A28","brown":"#4A2A22","beige":"#C9B9A0"}
RENDER_COLOURS = ["grey","red","yellow","orange"]
PATTERN_NAMES = {"herringbone":"Herringbone","bond":"Running bond","basket":"Basket weave","stack":"Stack bond","zig":"Stretcher","ishape":"Stretcher","grid":"Grid","staggered":"Staggered","combo5":"Random modular","tiles":"Grid"}
USE_NAMES = {"walk":"Walkways","drive":"Driveways","heavy":"Heavy duty","edge":"Edging"}

FAQ = [
  ("How do I get the price of paver blocks in Bhopal?", "Send an enquiry with your area in square feet, the block you like, its thickness and colour, and your site location. Our sales team replies the same working day with factory-direct terms for your quantity, with no dealer in between."),
  ("Which thickness do I need for a car driveway?", "60 mm works for a home driveway with occasional car use. 80 mm is the safer choice for daily cars, SUVs and colony roads. For trucks and forklifts, use 100 mm. The load guide above shows the full build-up."),
  ("How many paver blocks are in one square foot?", "About 4.6 rectangular blocks, 3.9 zig-zag blocks, 3.6 I-shape blocks or 2.3 square blocks per sq ft. Add about 5% for cutting at the edges. The pattern studio and enquiry form work this out for you."),
  ("Do you deliver outside Bhopal?", "Yes. We deliver from our Mandideep factory to Bhopal, Obedullaganj, Raisen, Sehore, Vidisha, Narmadapuram and Indore. The delivery date depends on quantity and stock and is confirmed with your order."),
  ("What are uni pavers and Behaton pavers?", "They are trade names for two interlocking shapes. A uni paver is the zig-zag block: the most popular choice for driveways, parking, petrol pumps and industrial yards because its wavy edges resist braking and turning wheels. A Behaton (I-shape or dumbbell) paver suits society internal roads, footpaths and commercial walkways. Hexagon pavers form a honeycomb that suits wide walkways, parks and plazas."),
  ("Will the colour fade?", "The pigment is mixed into the concrete, so the colour runs through the block rather than sitting on top as paint. All concrete pavers lighten slightly over years of sun; washing them once or twice a year keeps them bright."),
  ("Can I see the blocks before I order?", "Yes. Visit our sales office in MP Nagar, Bhopal, or our factory in Mandideep. Send an enquiry first and we will keep samples of the blocks you want ready, or send sample blocks for your architect or site engineer."),
  ("Are pavers better than a concrete slab for a driveway?", "Pavers let rainwater drain through the joints, do not crack across the whole surface, and can be lifted and re-laid if a pipe or cable needs work. A cracked slab has to be broken out."),
]

# licensed stock photos (Unsplash licence: free commercial use, no attribution required; credited in docs/image-credits.md)
STOCK = {
  "zigzag":[{"f":"stock/zigzag-laid","c":"grey","cap":"Grey zig-zag paving with red bands"},{"f":"stock/zigzag-parking","c":"grey","cap":"Zig-zag pavers in a parking bay"}],
  "ishape":[{"f":"stock/ishape-laid","c":"grey","cap":"Grey I-shape (Behaton) pavers laid"}],
  "rectangular":[{"f":"stock/rectangular-laid","c":"grey","cap":"Rectangular pavers in stretcher bond"},{"f":"stock/rectangular-terrace","c":"grey","cap":"Rectangular pavers on a garden terrace"}],
  "square":[{"f":"stock/square-grass","c":"grey","cap":"Square pavers with grass joints"}],
  "hexagon":[{"f":"stock/hexagon-walkway","c":"grey","cap":"Hexagon pavers in a honeycomb park walkway"},{"f":"stock/hexagon-closeup","c":"black","cap":"Dark hexagon paving, close-up"}],
}
GEN_COLOUR = {"hexagon":"grey","slate":"grey","antiskid":"grey","cobble":"beige","speckled":"grey","curved":"grey","ishape":"red","tiles":"yellow","zigzag":"grey","rectangular":"grey","square":"grey","cosmic":"red"}
ONSITE_DIR = "assets/img/onsite/"   # AI-generated "laid on site" views made from the owner's prompts (docs/image-prompts-v2.md)
ONSITE_COLOUR = {"cosmic":"red","zigzag":"red","ishape":"grey","rectangular":"grey","square":"grey","combo5":"yellow","hexagon":"grey","slate":"black","cobble":"grey","speckled":"grey","curved":"grey"}
def images_of(p):
    """Published pictures of a product: laid-on-site view first, then the studio product image, then stock photos."""
    out = []
    if os.path.exists(ONSITE_DIR + p["id"] + ".webp"):
        out.append({"f": "onsite/" + p["id"], "c": ONSITE_COLOUR.get(p["id"], p["c"]), "cap": p["full"] + " laid on site", "kind": "onsite"})
    if os.path.exists(GEN_DIR + p["id"] + ".webp"):
        out.append({"f": "generated/" + p["id"], "c": GEN_COLOUR.get(p["id"], p["c"]), "cap": p["full"], "kind": "gen"})
    out += [dict(x, kind="stock") for x in STOCK.get(p["id"], [])]
    return out

# ---------- generated product images ----------
# Drop a downloaded image named after the product id (e.g. zigzag.png, ishape.jpg) into
# assets/img/generated/; the build converts it to a 1200 px WebP and uses it as the
# product's main picture.
GEN_DIR = "assets/img/generated/"
def import_generated():
    from PIL import Image
    for f in os.listdir(GEN_DIR):
        name, ext = os.path.splitext(f)
        if ext.lower() in (".png", ".jpg", ".jpeg") and any(p["id"] == name for p in PRODUCTS):
            im = Image.open(GEN_DIR + f).convert("RGB")
            # cards are 4:3: extend a wide image with ground texture sampled from its own corners
            # (no mirroring, which would ghost the block), and cover the generator's corner watermark
            im = fill_ground(im)
            im.thumbnail((1200, 1200))
            im.save(GEN_DIR + name + ".webp", "WEBP", quality=84, method=6); os.remove(GEN_DIR + f)
def fill_ground(im):
    """Make a wide image 4:3 by extending its (already out-of-focus) ground above and below,
    and hide the generator's sparkle watermark in the bottom-right corner."""
    from PIL import Image, ImageFilter
    import numpy as np
    w, h = im.size
    ww, wh = int(w * .06), int(h * .08)                    # watermark corner: cover with the ground just left of it
    im.paste(im.crop((w - 2 * ww, h - wh, w - ww, h)).transpose(Image.FLIP_LEFT_RIGHT), (w - ww, h - wh))
    th = round(w * 3 / 4)
    if th <= h: return im
    pt = (th - h) // 2; pb = th - h - pt; band = max(8, h // 40); feather = h // 20
    rng = np.random.default_rng(7)
    def extend(strip, height):
        ext = strip.resize((w, height + feather), Image.BILINEAR).filter(ImageFilter.GaussianBlur(h / 60))
        a = np.asarray(ext).astype(np.float32); a += rng.normal(0, 4, a.shape[:2])[..., None]   # keep a little grain
        return Image.fromarray(np.clip(a, 0, 255).astype("uint8"))
    top = extend(im.crop((0, 0, w, band)), pt); bot = extend(im.crop((0, h - band, w, h)), pb)
    out = Image.new("RGB", (w, th)); out.paste(top, (0, 0)); out.paste(bot, (0, pt + h - feather))
    ramp = np.linspace(0, 255, feather).astype("uint8")
    mask = Image.new("L", (w, h), 255); m = np.asarray(mask).copy()
    m[:feather] = ramp[:, None]; m[h - feather:] = ramp[::-1][:, None]
    out.paste(im, (0, pt), Image.fromarray(m))
    return out

def gen_of(p, root):
    return root + GEN_DIR + p["id"] + ".webp" if os.path.exists(GEN_DIR + p["id"] + ".webp") else None

# ---------- helpers ----------
def _ver():
    """Short content hash for asset URLs, so browsers and GitHub Pages never serve a stale script or stylesheet."""
    import hashlib
    h = hashlib.md5()
    for f in ("assets/css/site.css", "assets/js/site.js", "tools/build.py"): h.update(open(f, "rb").read())
    return h.hexdigest()[:8]
VER = _ver()
KIND = {False: "Laid preview", "gen": "Product image", "stock": "Photo", "onsite": "Laid example"}
e = html.escape
def P(i): return next(p for p in PRODUCTS if p["id"] == i)
def colours_of(p):
    cs = [] if p.get("noRender") else list(RENDER_COLOURS)
    for x in PHOTOS.get(p["id"], []):
        if x["c"] not in cs: cs.append(x["c"])
    return cs
def view_of(p, c, root):
    ims = images_of(p)
    ph = (ims[0] if ims and c == p["c"] else None) or next((x for x in ims if x["c"] == c), None) or (ims[0] if ims and p.get("noRender") else None)
    if ph: return root + f'assets/img/{ph["f"]}.webp', ph["kind"], ph["cap"]
    if p.get("noRender"): return root + "assets/img/stock/placeholder.webp", False, p["full"]
    return root + f'assets/img/laid/{p["id"]}-{c}.webp', False, f'{p["name"]} laid in {COLOURS[c].lower()}'
def per_text(p):
    if p.get("per"): return f'≈ {p["per"]}'
    if p.get("perSet"): return f'1 set per {p["perSet"]} sq ft'
    return "Sold by running foot" if p["id"] == "curved" else "Ask us"
def thick_text(p): return " / ".join(map(str, p["thick"])) + " mm" if p["thick"] else "On request"
def wa_link(msg):
    from urllib.parse import quote
    return f'https://wa.me/{CONTACT["wa"]}?text={quote(msg)}'
def maps_link(l):
    from urllib.parse import quote_plus
    return "https://www.google.com/maps/search/?api=1&query=" + quote_plus(l["maps"])
def maps_embed(l):
    from urllib.parse import quote_plus
    return "https://maps.google.com/maps?q=" + quote_plus(l["maps"]) + "&output=embed"

def write(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    open(path, "w").write(text)

# ---------- schema ----------
ORG_ID = SITE_URL + "#organization"
def loc_schema(l):
    return {"@type": ["LocalBusiness", "HomeAndConstructionBusiness"], "@id": SITE_URL + l["slug"] + "/#place",
            "name": l["name"], "url": SITE_URL + l["slug"] + "/", "telephone": CONTACT["tel"],
            "image": SITE_URL + "assets/img/onsite/" + ("society-road" if l["id"] == "office" else "factory") + ".webp", "branchOf": {"@id": ORG_ID},
            "knowsAbout": ["paver blocks", "interlocking tiles", "kerb stones", "paver tiles"],
            "address": {"@type": "PostalAddress", "streetAddress": l["street"], "addressLocality": l["locality"],
                        "addressRegion": "Madhya Pradesh", "postalCode": l["pin"], "addressCountry": "IN"},
            "hasMap": maps_link(l), "areaServed": AREAS}
def org_schema():
    return {"@type": "Organization", "@id": ORG_ID, "name": BRAND, "legalName": LEGAL, "url": SITE_URL,
            "logo": SITE_URL + "assets/brand/logo-512.png", "telephone": CONTACT["tel"],
            "contactPoint": {"@type": "ContactPoint", "telephone": CONTACT["tel"], "contactType": "sales", "areaServed": "IN", "availableLanguage": ["en", "hi"]},
            "address": loc_schema(LOCATIONS[0])["address"],
            "description": "Manufacturer of concrete paver blocks, kerb stones and paver tiles in Mandideep, supplying malls, schools, factories, housing societies, petrol pumps and homes across Bhopal and central Madhya Pradesh."}
def ld(graph): return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + "</script>"
def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE_URL + u} for i, (n, u) in enumerate(items)]}

# ---------- page shell ----------
def head(root, path, title, desc, img="assets/img/scenes/hero.webp", schema="", extra=""):
    url = SITE_URL + path
    return f'''<!DOCTYPE html>
<html lang="en" data-root="{root}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#151412">
<meta name="geo.region" content="IN-MP"><meta name="geo.placename" content="Bhopal">
<meta property="og:type" content="website"><meta property="og:site_name" content="{BRAND}"><meta property="og:locale" content="en_IN">
<meta property="og:url" content="{url}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE_URL}{img}"><meta property="og:image:alt" content="{e(title)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{root}assets/brand/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{root}assets/brand/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{root}assets/brand/apple-touch-icon.png">
<link rel="manifest" href="{root}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Barlow+Condensed:wght@500;600;700&family=Mukta:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="{root}assets/css/site.css?v={VER}">
{extra}{schema}
<script src="{root}assets/js/data.js?v={VER}" defer></script>
<script src="{root}assets/js/site.js?v={VER}" defer></script>
</head>
<body>
'''

ICONS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="wa" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.6.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></symbol>
  <symbol id="phone" viewBox="0 0 24 24"><path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></symbol>
  <symbol id="sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4.5" fill="none" stroke="currentColor" stroke-width="2"/><path stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></symbol>
  <symbol id="moon" viewBox="0 0 24 24"><path fill="currentColor" d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z"/></symbol>
  <symbol id="logo" viewBox="0 0 64 64"><path d="M6 14l8-8 8 8 8-8 8 8v16l-8 8-8-8-8 8-8-8z" fill="#C4553A"/><path d="M26 34l8-8 8 8 8-8 8 8v16l-8 8-8-8-8 8-8-8z" fill="#D99A22"/></symbol>
</svg>
'''

def header(root):
    return ICONS + f'''<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap">
    <a class="brand" href="{root or './'}" aria-label="{BRAND}, home">
      <svg width="34" height="34" aria-hidden="true"><use href="#logo"/></svg>
      <span><b>{BRAND}</b><small>Paver blocks · Kerb stones</small></span>
    </a>
    <nav class="menu" aria-label="Main">
      <a href="{root}products/">Products</a>
      <a href="{root}#studio" data-i18n="nav.studio">Pattern studio</a>
      <a href="{root}#load" data-i18n="nav.load">Load guide</a>
      <a href="{root}#desk" id="navDesk">Home guide</a>
      <a href="{root}paver-blocks-bhopal/">Bhopal</a>
      <a href="{root}paver-blocks-mandideep/">Mandideep</a>
    </nav>
    <div class="tools">
      <button class="icon-btn" type="button" id="langBtn" aria-label="Switch language to Hindi">हिं</button>
      <button class="icon-btn" type="button" id="themeBtn" aria-label="Switch to dark mode"><svg><use href="#moon"/></svg></button>
      <a class="btn btn-primary" href="{root}contact/" data-i18n="nav.quote">Send enquiry</a>
      <button class="icon-btn menu-btn" type="button" id="menuBtn" aria-label="Open menu" aria-haspopup="dialog"><svg viewBox="0 0 24 24"><path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
    </div>
  </div>
</header>
'''

def footer(root):
    locs = "".join(f'<li><b>{e(l["role"])}:</b> {e(addr_line(l))}</li>' for l in LOCATIONS)
    prods = "".join(f'<li><a href="{root}products/{p["slug"]}/">{e(p["full"])}</a></li>' for p in PRODUCTS[:8])
    wa = e(wa_link("Hello Satyam Pavers, I would like to send an enquiry about paver blocks."))
    area_links = " · ".join(f'<a href="{root}{a["slug"]}/">{a["name"]}</a>' for a in SERVICE_AREAS)
    return f'''<footer><div class="wrap">
  <div><b class="foot-brand"><svg width="28" height="28" aria-hidden="true"><use href="#logo"/></svg>{BRAND}</b><p style="margin-top:8px;max-width:30em">Concrete paver blocks, kerb stones and paver tiles, made in Mandideep for Bhopal, Indore and central Madhya Pradesh.</p>
    <p style="margin-top:14px"><a class="btn btn-primary" href="{root}contact/">Send enquiry</a></p></div>
  <div><h4>Products</h4><ul>{prods}<li><a href="{root}products/">All products →</a></li></ul></div>
  <div><h4>Visit us</h4><ul>{locs}<li><a href="{root}paver-blocks-bhopal/">Paver blocks in Bhopal</a></li><li><a href="{root}paver-blocks-mandideep/">Paver blocks in Mandideep</a></li><li><a href="{root}contact/">Contact &amp; enquiry</a></li><li><a href="{root}tools/paver-calculator/">Paver block calculator</a></li><li><a href="{root}guides/how-to-lay-paver-blocks/">How to lay paver blocks</a></li><li><a href="{root}guides/paver-block-maintenance/">Paver care guide</a></li><li>Delivery: {area_links}</li><li class="num">Mobile: <a href="tel:{CONTACT["tel"]}">{CONTACT["display"]}</a></li></ul></div>
  <div class="legal">{BRAND} is a brand of {e(LEGAL)}, Madhya Pradesh. Sizes and block counts are typical values; colours of real blocks vary slightly in shade. Page updated {TODAY}.</div>
</div></footer>

<a class="float-wa" href="{wa}" target="_blank" rel="noopener" aria-label="Send enquiry on WhatsApp"><svg><use href="#wa"/></svg></a>
<nav class="mbar" aria-label="Quick actions">
  <a href="tel:{CONTACT["tel"]}"><svg><use href="#phone"/></svg><span data-i18n="bar.call">Call</span></a>
  <a href="{wa}" target="_blank" rel="noopener"><svg><use href="#wa"/></svg>WhatsApp</a>
  <a class="go" href="{root}contact/" data-i18n="bar.quote">Enquiry</a>
</nav>
<div class="toast" id="toast" role="status" hidden></div>

<dialog class="sheet" id="menu" aria-label="Menu">
  <div class="sheet-head"><span class="label">Menu</span><button class="d-close" type="button" data-close aria-label="Close menu">×</button></div>
  <nav class="sheet-nav" aria-label="Sections">
    <a href="{root}products/">Products</a>
    <a href="{root}#studio" data-i18n="nav.studio">Pattern studio</a>
    <a href="{root}#load" data-i18n="nav.load">Load guide</a>
    <a href="{root}#desk" id="navDesk2">Home guide</a>
    <a href="{root}paver-blocks-bhopal/">Bhopal office</a>
    <a href="{root}paver-blocks-mandideep/">Mandideep factory</a>
    <a href="{root}contact/" data-i18n="nav.quote">Send enquiry</a>
    <a href="{root}guides/how-to-lay-paver-blocks/">Laying guide</a>
    <a href="{root}#faq">FAQ</a>
  </nav>
  <div class="sheet-block">
    <span class="label" data-i18n="mode.label">I am a</span>
    <div class="seg seg-full" role="group" aria-label="Who are you?" id="modeSeg2">
      <button type="button" id="mode2-home" data-mode="home" aria-pressed="true" data-i18n="mode.home">Homeowner</button>
      <button type="button" id="mode2-builder" data-mode="builder" aria-pressed="false" data-i18n="mode.builder">Builder</button>
      <button type="button" id="mode2-architect" data-mode="architect" aria-pressed="false" data-i18n="mode.architect">Architect</button>
    </div>
  </div>
  <div class="sheet-block sheet-row">
    <button type="button" class="btn btn-line" id="themeBtn2">Dark mode</button>
    <button type="button" class="btn btn-line" id="langBtn2">हिंदी</button>
  </div>
  <div class="sheet-block">
    <a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener"><svg><use href="#wa"/></svg>Send enquiry on WhatsApp</a>
  </div>
</dialog>
</body>
</html>
'''

# ---------- shared blocks ----------
def card(p, root, i=0, interactive=True):
    src, real, cap = view_of(p, p["c"], root)
    href = f'{root}products/{p["slug"]}/'
    dots = "".join(f'<button type="button" class="dot sm" id="dot-{p["id"]}-{c}" data-p="{p["id"]}" data-c="{c}" aria-label="{COLOURS[c]}" title="{COLOURS[c]}" aria-pressed="{str(c == p["c"]).lower()}" style="background:{HEX[c]}"></button>' for c in colours_of(p)) if interactive else ""
    cmp = f'<button type="button" class="cmp" id="cmp-{p["id"]}" data-cmp="{p["id"]}" aria-pressed="false"><b>✓</b>Compare</button>' if interactive else ""
    return (f'<article class="p" data-uses="{" ".join(p["uses"])}">'
            f'<a class="ph" href="{href}" aria-label="{e(p["full"])}: sizes and details"><img id="img-{p["id"]}" src="{src}" alt="{e(cap)}" loading="{"eager" if i < 3 else "lazy"}" width="1100" height="825"><span class="tag">{e(p["size"])}</span><span class="kind{" real" if real else ""}" id="kind-{p["id"]}">{KIND[real]}</span></a>'
            f'<div class="row"><h3><a href="{href}" style="text-decoration:none">{e(p["name"])}</a></h3><div class="dots">{dots}</div></div>'
            f'<div class="sub">{e(p["alt"])} · {e(p["load"])}</div>'
            f'<div class="actions"><a class="link" href="{href}">Details</a><a class="ask" id="ask-{p["id"]}" href="{e(wa_link("Hello Satyam Pavers, I would like to enquire about " + p["name"] + " (" + COLOURS[p["c"]].lower() + ")."))}" target="_blank" rel="noopener"><svg><use href="#wa"/></svg>Enquire</a>{cmp}</div>'
            '</article>')

def faq_html(items, open_first=True):
    return "".join(f'<details{" open" if open_first and i == 0 else ""}><summary>{e(q)}</summary><p>{e(a)}</p></details>' for i, (q, a) in enumerate(items))
def faq_schema(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def place_html(l, root):
    return (f'<div class="place"><div><h3>{e(l["role"])}</h3><p>{e(addr_line(l))}</p></div>'
            f'<div class="row2"><a class="link" href="{root}{l["slug"]}/">About this location</a><a class="link" href="{maps_link(l)}" target="_blank" rel="noopener">Directions</a></div></div>')

def enquiry_form(root, product="", city=""):
    opts = "".join(f'<option{" selected" if p["full"] == product else ""}>{e(p["full"])}</option>' for p in PRODUCTS)
    return f'''<form class="form enq" novalidate>
  <div><div class="label" style="color:var(--ink)">Send enquiry</div><p class="note">Your enquiry opens in WhatsApp, typed in and ready. Nothing is sent until you press send there.</p></div>
  <label>Your name<input name="name" autocomplete="name" required></label>
  <label>Mobile number<input name="phone" type="tel" autocomplete="tel" inputmode="tel" required></label>
  <label>Product<select name="product"><option value="">Not sure yet — please suggest</option>{opts}</select></label>
  <label>Area in sq ft (approx.)<input name="area" type="number" min="1" inputmode="numeric"></label>
  <label>Site location<input name="city" value="{e(city)}" placeholder="e.g. Kolar Road, Bhopal"></label>
  <label>Anything else<input name="message" placeholder="Thickness, colour, timeline…"></label>
  <button class="btn btn-wa" type="submit"><svg><use href="#wa"/></svg>Send enquiry</button>
</form>'''

# ---------- delivery-town pages ----------
SERVICE_AREAS = [
  dict(name="Obedullaganj", slug="paver-blocks-obedullaganj", km=12, note="Obedullaganj is the nearest town to our factory, so small orders and urgent top-ups are easy to arrange.", popular=["zigzag", "rectangular", "curved"]),
  dict(name="Raisen", slug="paver-blocks-raisen", km=50, note="Mandideep is in Raisen district, and we supply homes, colonies and government-style works across the district.", popular=["ishape", "zigzag", "curved"]),
  dict(name="Narmadapuram", slug="paver-blocks-narmadapuram", km=55, note="Trucks run straight down NH-46 from Mandideep to Narmadapuram, Itarsi-side sites included.", popular=["zigzag", "cobble", "curved"]),
  dict(name="Sehore", slug="paver-blocks-sehore", km=65, note="For Sehore town and the Bhopal–Sehore road belt, we plan full-truck deliveries that match your site schedule.", popular=["rectangular", "zigzag", "tiles"]),
  dict(name="Vidisha", slug="paver-blocks-vidisha", km=85, note="For Vidisha we usually deliver in full truckloads, so larger driveways, colony roads and campus jobs work best.", popular=["ishape", "rectangular", "curved"]),
]
def build_area(a):
    root = "../"
    n = a["name"]
    faqs = [(f"Do you deliver paver blocks to {n}?", f"Yes. We deliver to {n} by truck from our factory in Mandideep, about {a['km']} km away. The delivery date is confirmed with your order and depends on quantity and stock."),
            (f"How do I get the price of paver blocks in {n}?", f"Send an enquiry with your area in square feet, the block, thickness and colour, and your site location in {n}. Delivery to {n} is included in the terms we send for your quantity."),
            (f"Which paver block is best for {n} colony roads and driveways?", "Use 80 mm zig-zag (uni) or I-shape (Behaton) blocks for colony roads and daily car use, 60 mm for light home driveways, and 100 mm where trucks drive. Finish the edges with kerb stones.")]
    cards = "".join(card(P(i), root, 9, interactive=False) for i in a["popular"])
    graph = [org_schema(), {"@type": "Service", "name": f"Paver block supply in {n}", "serviceType": "Concrete paver block and kerb stone supply",
              "provider": {"@id": ORG_ID}, "areaServed": {"@type": "City", "name": n, "containedInPlace": {"@type": "State", "name": "Madhya Pradesh"}}},
             crumbs([("Home", ""), (f"Paver blocks in {n}", a["slug"] + "/")]), faq_schema(faqs)]
    main = f'''<main id="main"><section><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a> / <span>Paver blocks in {e(n)}</span></nav>
  <div class="label">Delivery area · {a["km"]} km from our factory</div>
  <h1 class="h1">Paver blocks in {e(n)}</h1>
  <p class="answer">Satyam Pavers delivers concrete paver blocks, interlocking tiles and kerb stones to {e(n)} from our factory in Mandideep, about {a["km"]} km away. {e(a["note"])}</p>
  <div class="row2" style="margin-top:20px"><a class="btn btn-primary" href="#enquiry">Send enquiry</a><a class="link" href="../products/">See all 13 ranges</a></div>
  <h2 class="h2" style="margin-top:56px">Popular in {e(n)}</h2>
  <div class="products" style="margin-top:20px">{cards}</div>
  <div class="prod-cols" style="margin-top:56px" id="enquiry">
    <div>{enquiry_form(root, city=n)}</div>
    <div><h2 class="h2">Questions from {e(n)}</h2><div class="faq" style="margin-top:16px">{faq_html(faqs)}</div>
      <p style="margin-top:20px">Made at our <a class="link" href="../paver-blocks-mandideep/">Mandideep factory</a> · Sales office in <a class="link" href="../paver-blocks-bhopal/">MP Nagar, Bhopal</a></p></div>
  </div>
</div></section></main>
'''
    write(a["slug"] + "/index.html", head(root, a["slug"] + "/", f"Paver Blocks in {n} | Delivered from Mandideep — Satyam Pavers",
          f"Paver blocks, interlocking tiles and kerb stones delivered to {n} from our Mandideep factory, {a['km']} km away. Send an enquiry for factory-direct terms.",
          img="assets/img/stock/colony-road.webp", schema=ld(graph)) + header(root) + main + footer(root))

# ---------- guides ----------
GUIDES = [
  dict(slug="guides/how-to-lay-paver-blocks", title="How to Lay Paver Blocks: Step-by-Step Guide | Satyam Pavers", h1="How to lay paver blocks",
       desc="Step-by-step guide to laying interlocking paver blocks: excavation depth, sub-base, sand bed, kerbs, laying pattern, compaction and joint sand.",
       answer="A paver floor lasts when the ground under it is right. Dig to the depth your load needs, build a compacted stone sub-base, spread a thin even sand bed, fix kerbs at the edges, lay the blocks in pattern, compact them and brush sand into the joints.",
       howto=True,
       steps=[("Mark and dig", "Mark the area with a slope of about 1 in 60 away from the house for drainage. Dig 200–250 mm for footpaths, 300 mm for car driveways and 400 mm or more where trucks drive, and compact the soil."),
              ("Build the sub-base", "Lay crushed stone (GSB or WMM) in layers of about 100 mm and compact each layer with a plate compactor or roller: 100 mm for walkways, 150 mm for driveways, 250 mm or more for heavy-duty yards."),
              ("Fix the kerbs", "Set kerb stones on a concrete bed along every open edge before laying. Kerbs stop the blocks from spreading sideways under wheels."),
              ("Spread the sand bed", "Spread 25–30 mm of coarse sharp sand and screed it level. Do not walk on it or compact it before the blocks go down."),
              ("Lay the blocks", "Start from a straight edge or kerb and lay in your chosen pattern, tight against each other, working off the laid blocks. Use herringbone where cars turn. Cut edge pieces with a block cutter."),
              ("Compact and fill the joints", "Run a plate compactor over the blocks two or three times, brush dry fine sand into the joints and compact again until the joints are full. The floor can take foot traffic at once and cars after the joints are filled.")]),
  dict(slug="guides/paver-block-maintenance", title="Paver Block Maintenance & Cleaning Guide | Satyam Pavers", h1="Paver block care and maintenance",
       desc="How to clean paver blocks, remove oil stains and weeds, refill joints, fix a sunken patch and keep your paving looking new through the monsoon.",
       answer="Paver blocks need little care: sweep regularly, wash once or twice a year, top up joint sand when it washes out, and lift and re-lay any patch that sinks. Unlike a concrete slab, a paver floor can always be repaired block by block.",
       howto=False,
       steps=[("Regular cleaning", "Sweep weekly and wash with water and a stiff broom. A pressure washer is fine on a low setting held at an angle, then refill any joint sand it removes."),
              ("Oil and tyre stains", "Soak fresh oil with sawdust or cement powder, then scrub with detergent and warm water. Older stains respond to a concrete degreaser. Avoid acid cleaners, which etch the surface."),
              ("Weeds and moss", "Pull weeds and refill the joint with dry sand: full joints leave weeds no room. In shady damp spots, scrub moss off with a mild bleach solution and rinse well."),
              ("Joint sand", "Check the joints after every monsoon and brush in fresh dry sand where it has washed out. Full joints keep the blocks locked together."),
              ("Sunken or broken blocks", "Lift the blocks in the low area, add and level sand underneath, and re-lay the same blocks. Replace a broken block with one from the same colour batch."),
              ("Sealing (optional)", "A breathable concrete sealer deepens the colour and resists stains. Apply it on clean, dry paving, and re-apply every two to three years.")]),
]
def build_guide(g):
    root = "../../"
    steps = "".join(f'<li><h2 class="h2" style="font-size:1.5rem">{e(h)}</h2><p>{e(t)}</p></li>' for h, t in g["steps"])
    graph = [org_schema(), crumbs([("Home", ""), (g["h1"], g["slug"] + "/")])]
    if g["howto"]:
        graph.append({"@type": "HowTo", "name": g["h1"], "description": g["answer"], "step": [{"@type": "HowToStep", "position": i + 1, "name": h, "text": t} for i, (h, t) in enumerate(g["steps"])]})
    other = next(x for x in GUIDES if x is not g)
    main = f'''<main id="main"><section><div class="wrap" style="max-width:820px">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{root}">Home</a> / <span>{e(g["h1"])}</span></nav>
  <div class="label">Guide</div>
  <h1 class="h1">{e(g["h1"])}</h1>
  <p class="answer">{e(g["answer"])}</p>
  <ol class="guide-steps">{steps}</ol>
  <p style="margin-top:32px">Not sure which thickness you need? See the <a class="link" href="{root}#load">load guide</a> · Also read: <a class="link" href="{root}{other["slug"]}/">{e(other["h1"])}</a></p>
  <div class="row2" style="margin-top:24px"><a class="btn btn-primary" href="{root}contact/">Send enquiry</a><a class="link" href="{root}products/">See all 13 ranges</a></div>
</div></section></main>
'''
    write(g["slug"] + "/index.html", head(root, g["slug"] + "/", g["title"], g["desc"], schema=ld(graph)) + header(root) + main + footer(root))

# ---------- calculator ----------
CALC = [("Rectangular 200×100 mm", 50), ("Zig-Zag (Uni) interlocking", 40), ("I-Shape (Behaton)", 39), ("Square 200×200 mm", 25), ("Cosmic interlocking", 36), ("Paver tiles 300×300 mm", 11)]
def build_calc():
    root, slug = "../../", "tools/paver-calculator"
    opts = "".join(f'<option value="{n}">{e(t)}</option>' for t, n in CALC)
    graph = [org_schema(), crumbs([("Home", ""), ("Paver block calculator", slug + "/")]),
             {"@type": "WebApplication", "name": "Paver block quantity calculator", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "isAccessibleForFree": True}]
    main = f'''<main id="main"><section><div class="wrap" style="max-width:820px">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{root}">Home</a> / <span>Paver block calculator</span></nav>
  <div class="label">Tool</div>
  <h1 class="h1">Paver block quantity calculator</h1>
  <p class="answer">Enter your area to see roughly how many paver blocks you need, with 5% extra for cutting and breakage. Send the result to us on WhatsApp and we will confirm the exact count and delivery.</p>
  <form class="form" id="calc" data-wa="{CONTACT["wa"]}" style="margin-top:28px;display:grid;gap:16px;max-width:520px">
    <label>Block type<select name="b">{opts}</select></label>
    <label>Length<input name="l" type="number" min="0" step="0.1" inputmode="decimal" value="20"></label>
    <label>Width<input name="w" type="number" min="0" step="0.1" inputmode="decimal" value="10"></label>
    <label>Unit<select name="u"><option value="ft">Feet</option><option value="m">Metres</option></select></label>
  </form>
  <div class="calc-out" aria-live="polite"><div><b id="c-blocks">–</b><span>blocks (approx.)</span></div><div><b id="c-sqft">–</b><span>sq ft</span></div><div><b id="c-sqm">–</b><span>sq m</span></div></div>
  <div class="row2" style="margin-top:20px"><a class="btn btn-primary" id="c-wa" href="#" target="_blank" rel="noopener">Send on WhatsApp</a><a class="link" href="{root}guides/how-to-lay-paver-blocks/">How to lay paver blocks</a></div>
  <p class="muted" style="margin-top:24px;font-size:.9rem">Counts vary slightly with block thickness and pattern. Kerb stones are counted by running length, so tell us the edge length in your message.</p>
</div></section></main>
<script>(()=>{{const f=document.getElementById("calc"),$=i=>document.getElementById(i);function run(){{const l=+f.l.value||0,w=+f.w.value||0,m=f.u.value==="m"?l*w:l*w*0.0929,n=Math.ceil(m*+f.b.value*1.05);$("c-sqm").textContent=m.toFixed(1);$("c-sqft").textContent=Math.round(m*10.764);$("c-blocks").textContent=n.toLocaleString("en-IN");$("c-wa").href="https://wa.me/"+f.dataset.wa+"?text="+encodeURIComponent("Hello Satyam Pavers, I need about "+n+" "+f.b.selectedOptions[0].text+" blocks for "+Math.round(m*10.764)+" sq ft. Please confirm.")}}f.addEventListener("input",run);run()}})()</script>
'''
    write(slug + "/index.html", head(root, slug + "/", "Paver Block Calculator: How Many Blocks Do I Need? | Satyam Pavers", "Free paver block quantity calculator. Enter length and width in feet or metres to estimate how many interlocking paver blocks you need, with wastage.", schema=ld(graph)) + header(root) + main + footer(root))

# ---------- pages ----------
def build_home():
    body = open("src/home.html").read()
    body = body.replace('<main id="home">', '<main id="main">', 1)
    body = body.replace("{{GRID}}", "".join(card(p, "", i) for i, p in enumerate(sorted(PRODUCTS, key=lambda p: not (images_of(p) or not p.get("noRender"))))))
    body = body.replace("{{PLACES}}", "".join(place_html(l, "") for l in LOCATIONS))
    body = body.replace("{{FAQ}}", faq_html(FAQ))
    graph = [org_schema(), {"@type": "WebSite", "@id": SITE_URL + "#website", "name": BRAND, "url": SITE_URL, "publisher": {"@id": ORG_ID}, "inLanguage": "en-IN"}] + [loc_schema(l) for l in LOCATIONS] + [faq_schema(FAQ),
             {"@type": "ItemList", "name": "Satyam Pavers products", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE_URL + "products/" + p["slug"] + "/", "name": p["full"]} for i, p in enumerate(PRODUCTS)]}]
    page = head("", "", "Paver Block Manufacturer in Bhopal & Mandideep | Satyam Pavers",
                "Concrete paver blocks, interlocking tiles and kerb stones made in Mandideep for Bhopal. 13 ranges, 60–100 mm. Design your floor online and send an enquiry.",
                schema=ld(graph), extra='<link rel="preload" as="image" href="assets/img/scenes/hero.webp">\n')
    write("index.html", page + header("") + body + footer(""))

def build_products_index():
    root = "../"
    cards = "".join(card(p, root, i, interactive=False) for i, p in enumerate(PRODUCTS))
    rows = "".join(f'<tr><td><a href="{p["slug"]}/">{e(p["full"])}</a></td><td class="mono">{e(p["size"])}</td><td class="mono">{thick_text(p)}</td><td>{e(p["load"])}</td></tr>' for p in PRODUCTS)
    graph = [org_schema(), crumbs([("Home", ""), ("Products", "products/")]),
             {"@type": "CollectionPage", "name": "Paver blocks, tiles and kerb stones", "url": SITE_URL + "products/", "about": {"@id": ORG_ID}}]
    main = f'''<main id="main"><section><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a> / <span>Products</span></nav>
  <div class="head"><div><div class="label">Catalogue</div><h1 class="h1">Paver blocks, tiles &amp; kerb stones</h1>
  <p class="answer">{BRAND} makes 13 ranges of concrete paving at its Mandideep factory near Bhopal: interlocking paver blocks (zig-zag, I-shape, rectangular, square, cosmic, Combo 5), decorative finishes (slate, anti-skid, cobble, speckled, hexagon 3D tiles), concrete paver tiles and kerb stones, in 60, 80 and 100 mm for foot traffic up to heavy vehicles.</p></div></div>
  <div class="products">{cards}</div>
  <h2 class="h2" style="margin-top:64px">Size and thickness at a glance</h2>
  <div class="tbl" style="margin-top:16px"><table class="spec"><thead><tr><th>Product</th><th>Size</th><th>Thickness</th><th>Load</th></tr></thead><tbody>{rows}</tbody></table></div>
  <p class="note" style="margin-top:8px">Typical values. Confirm the exact size and thickness for your order with our team.</p>
</div></section></main>
'''
    write("products/index.html", head(root, "products/", "Paver Block Types & Sizes | Interlocking Tiles, Kerb Stones — Satyam Pavers",
          "All 13 Satyam Pavers ranges: zig-zag, I-shape, rectangular, square, cosmic, hexagon, slate, anti-skid, cobble, paver tiles and kerb stones. Sizes, thickness and uses.", schema=ld(graph)) + header(root) + main + footer(root))

def product_faq(p):
    out = []
    if p["thick"]:
        out.append((f'What thickness of {p["name"].lower()} should I use?',
                    f'{p["full"]} come in {thick_text(p)}. Use the thinnest option for foot traffic, the middle one for cars, and {p["thick"][-1]} mm where trucks or forklifts drive. Our team confirms the right grade for your site.'))
    if p.get("per") or p.get("perSet"):
        cov = f'about {p["per"]} blocks per square foot' if p.get("per") else f'one set per {p["perSet"]} square feet'
        out.append((f'How many {p["name"].lower()} blocks do I need?', f'Plan on {cov}, plus about 5% for cutting at the edges. For 1,000 sq ft that is roughly ' + (f'{round(1000*1.05*p["per"]):,} blocks.' if p.get("per") else f'{round(1000*1.05/p["perSet"]):,} sets.')))
    out.append((f'Which colours are available?', f'{p["full"]} are made in ' + ", ".join(COLOURS[c].lower() for c in colours_of(p)) + '. Ask us about other colours for larger orders.'))
    out.append((f'Do you deliver {p["name"].lower()} to my site?', 'Yes. We deliver from our Mandideep factory across Bhopal, Obedullaganj, Raisen, Sehore, Vidisha, Narmadapuram and Indore. The delivery date is confirmed with your order.'))
    return out

def build_product(p, idx):
    root = "../../"
    gallery = [(root + f'assets/img/{x["f"]}.webp', x["cap"], x["kind"]) for x in images_of(p)]
    if not p.get("noRender"):
        gallery += [(root + f'assets/img/laid/{p["id"]}-{c}.webp', f'{p["name"]} laid in {COLOURS[c].lower()} (preview)', False) for c in RENDER_COLOURS]
    if not gallery: gallery = [(root + "assets/img/stock/placeholder.webp", p["full"], False)]
    main_img = gallery[0]
    thumbs = "".join(f'<figure class="pg"><img src="{s}" alt="{e(c)}" loading="lazy" width="1100" height="825"><figcaption>{KIND[r]} · {e(c)}</figcaption></figure>' for s, c, r in gallery[1:])
    spec = [("Size", p["size"]), ("Thickness", thick_text(p)), ("Coverage", per_text(p) + (" blocks per sq ft" if p.get("per") else "")),
            ("Load", p["load"]), ("Laying patterns", ", ".join(PATTERN_NAMES[k] for k in p["patterns"]) or ("Straight runs and curves" if p["id"] == "curved" else p.get("lay", "Ask us"))),
            ("Colours", ", ".join(COLOURS[c] for c in colours_of(p))), ("Made at", "Our factory in Mandideep, near Bhopal")]
    spec_rows = "".join(f'<tr><th scope="row">{k}</th><td>{e(v)}</td></tr>' for k, v in spec)
    best = "".join(f"<li>{e(b)}</li>" for b in p["best"])
    faqs = product_faq(p)
    related = [q for q in PRODUCTS if q["id"] != p["id"] and set(q["uses"]) & set(p["uses"])][:3] or PRODUCTS[:3]
    rel = "".join(card(q, root, 9, interactive=False) for q in related)
    studio = f'<a class="link" href="{root}#studio">Try it in the pattern studio</a>' if p["patterns"] else ""
    wa = e(wa_link(f'Hello Satyam Pavers, I would like to enquire about {p["full"]}.'))
    url = f'products/{p["slug"]}/'
    graph = [org_schema(), crumbs([("Home", ""), ("Products", "products/"), (p["full"], url)]),
             {"@type": "Product", "@id": SITE_URL + url + "#product", "name": p["full"], "description": p["answer"], "sku": "SP-" + p["code"],
              "image": [SITE_URL + s[len(root):] for s, _, _ in gallery], "brand": {"@type": "Brand", "name": BRAND}, "manufacturer": {"@id": ORG_ID},
              "category": "Concrete paving", "material": "Concrete",
              "additionalProperty": [{"@type": "PropertyValue", "name": k, "value": v} for k, v in spec[:5]]},
             faq_schema(faqs)]
    title = f'{p["full"]} in Bhopal | Sizes, Thickness & Colours — {BRAND}'
    if len(title) > 70: title = f'{p["full"]} in Bhopal — {BRAND}'
    desc = f'{p["full"]} made in Mandideep for Bhopal: {p["size"]}, {thick_text(p)}, {", ".join(COLOURS[c].lower() for c in colours_of(p)[:4])}. {p["load"]} use. Send an enquiry today.'
    main = f'''<main id="main"><section><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{root}">Home</a> / <a href="{root}products/">Products</a> / <span>{e(p["full"])}</span></nav>
  <div class="prod">
    <figure class="gal"><img src="{main_img[0]}" alt="{e(main_img[1])}" width="1100" height="825" fetchpriority="high"><figcaption>{KIND[main_img[2]]} · {e(main_img[1])}</figcaption></figure>
    <div class="prod-info">
      <div class="label">{e(p["alt"])}</div>
      <h1 class="h1">{e(p["full"])}</h1>
      <p class="answer">{e(p["answer"])}</p>
      <p>{e(p["desc"])}</p>
      <div class="row2"><a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener"><svg><use href="#wa"/></svg>Send enquiry</a>{studio}</div>
    </div>
  </div>
  <div class="prod-cols">
    <div><h2 class="h2">Specifications</h2><div class="tbl" style="margin-top:14px"><table class="spec"><tbody>{spec_rows}</tbody></table></div>
      <p class="note" style="margin-top:8px">Typical values. Confirm exact size, grade and stock for your order.</p></div>
    <div><h2 class="h2">Where it works best</h2><ul class="asklist" style="margin-top:14px">{best}</ul>
      <p class="note" style="margin-top:14px">Not sure about thickness? See the <a href="{root}#load">load guide</a>.</p></div>
  </div>
  {f'<div class="pgs">{thumbs}</div>' if thumbs else ''}
  <div class="faq" style="margin-top:72px"><div><div class="label">FAQ</div><h2 class="h2">{e(p["name"])} questions</h2></div><div>{faq_html(faqs)}</div></div>
  <h2 class="h2" style="margin-top:72px">Related products</h2>
  <div class="products" style="margin-top:20px">{rel}</div>
</div></section>
<div class="final"><div class="wrap"><div><div class="label">Send enquiry</div><h2>Need {e(p["name"].lower())} for your site?</h2><p style="color:var(--hero-muted);margin-top:8px">Tell us your area, thickness and colour. We reply the same working day.</p></div>
  <div class="phone"><a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener"><svg><use href="#wa"/></svg>Send enquiry on WhatsApp</a><a class="btn btn-line" href="{root}contact/">Enquiry form</a></div></div></div>
</main>
'''
    write(url + "index.html", head(root, url, title, desc[:160], img=main_img[0][len(root):], schema=ld(graph)) + header(root) + main + footer(root))

LOC_COPY = {
  "office": dict(
    title="Paver Blocks in Bhopal | Sales Office, MP Nagar — Satyam Pavers",
    desc="Buy paver blocks, interlocking tiles and kerb stones in Bhopal. Visit our sales office at Kanha Building, Zone-II, MP Nagar, or send an enquiry.",
    h1="Paver blocks in Bhopal", img="onsite/society-road", img_alt="Society road paved with grey zig-zag pavers and red bands",
    answer="Satyam Pavers' Bhopal sales office is in Kanha Building, Plot No. 190, Zone-II, MP Nagar, near Hotel Kanha and Sargam Cinema. Homeowners, builders and architects come here to choose blocks, plan quantities and arrange delivery from our Mandideep factory to any site in Bhopal.",
    body=[("What you can do at the MP Nagar office", "Compare blocks, colours and finishes, get a block count for your area, and plan delivery dates for your site. Architects can collect sample blocks for client meetings."),
          ("Areas we deliver to in Bhopal", "Every part of the city, including Kolar Road, Narmadapuram Road, Ayodhya Bypass, Bawadia Kalan, Misrod, Katara Hills, Bairagarh, Govindpura, Awadhpuri, Shahpura, Arera Colony and the old city. Larger orders go straight from the factory to your site by truck."),
          ("भोपाल में पेवर ब्लॉक", "सत्यम पेवर्स का बिक्री कार्यालय कान्हा बिल्डिंग, प्लॉट नं. 190, ज़ोन-II, एमपी नगर, भोपाल में है। इंटरलॉकिंग पेवर ब्लॉक, पेवर टाइल्स और कर्ब स्टोन हमारी मंडीदीप फैक्ट्री से सीधे आपकी साइट तक पहुँचाए जाते हैं। रेट और उपलब्धता के लिए एन्क्वायरी भेजें।"),
          ("Popular in Bhopal", "Zig-zag (uni) pavers for driveways, parking and petrol pumps, I-shape (Behaton) pavers for society roads and footpaths, grey and red rectangular blocks for porches, and kerb stones to finish society roads.")]),
  "factory": dict(
    title="Paver Block Manufacturer in Mandideep | Factory — Satyam Pavers",
    desc="Satyam Pavers makes concrete paver blocks and kerb stones at the Suveesha Engineers & Industries factory in Mandideep, near Bhopal. Factory-direct supply.",
    h1="Paver block factory in Mandideep", img="onsite/factory", img_alt="Pallets of cured paver blocks in a factory yard",
    answer="Satyam Pavers blocks are made at the Suveesha Engineers & Industries factory in Mandideep industrial area, about 25 km from Bhopal. Buying factory-direct means no dealer in between, batches that match in colour, and trucks loaded at the factory for your site.",
    body=[("How our blocks are made", "Cement, stone dust, grit and pigment are weighed for every batch. Vibration and pressure pack the mix into steel moulds, the blocks are kept moist while they cure, and sample blocks are checked for size, strength and water absorption before dispatch."),
          ("How to reach the factory", "Mandideep is about 25 km south-east of Bhopal on NH-46, the Bhopal–Narmadapuram road, past Misrod. Send an enquiry before you visit so samples of the blocks you want are ready and the right person is at the gate."),
          ("Delivery from Mandideep", "Obedullaganj is about 12 km away, Bhopal 25 km, Raisen 50 km, Narmadapuram 55 km, Sehore 65 km, Vidisha 85 km and Indore 215 km. Dispatch dates are confirmed with each order."),
          ("For builders and contractors", "Phased delivery that follows your site schedule, colour matched across batches, and kerbs and edging to finish colony roads. Send your project quantity for a supply plan.")]),
}

def build_location(l):
    root = "../"
    c = LOC_COPY[l["id"]]
    other = next(x for x in LOCATIONS if x is not l)
    secs = "".join(f'<h2 class="h2" style="margin-top:40px">{e(h)}</h2><p style="margin-top:10px;max-width:68ch">{e(t)}</p>' for h, t in c["body"])
    cards = "".join(card(P(i), root, 9, interactive=False) for i in (["zigzag", "ishape", "curved"] if l["id"] == "office" else ["rectangular", "square", "tiles"]))
    graph = [org_schema(), loc_schema(l), crumbs([("Home", ""), (c["h1"], l["slug"] + "/")])]
    main = f'''<main id="main"><section><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a> / <span>{e(c["h1"])}</span></nav>
  <div class="prod">
    <div class="prod-info" style="padding:0">
      <div class="label">{e(l["role"])}</div>
      <h1 class="h1">{e(c["h1"])}</h1>
      <p class="answer">{e(c["answer"])}</p>
      <address class="addr"><b>{e(l["name"])}</b><br>{e(addr_line(l))}<br>Mobile: <a href="tel:{CONTACT["tel"]}">{CONTACT["display"]}</a></address>
      <div class="row2"><a class="btn btn-ink" href="{maps_link(l)}" target="_blank" rel="noopener">Get directions</a><a class="link" href="../contact/">Send enquiry</a></div>
    </div>
    <iframe class="map" title="Map: {e(l["name"])}" src="{maps_embed(l)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div>
  {secs}
  <figure class="scene"><img src="{root}assets/img/{c["img"] if "/" in c["img"] else "stock/" + c["img"]}.webp" alt="{e(c["img_alt"])}" loading="lazy" width="1200" height="900"></figure>
  <h2 class="h2" style="margin-top:56px">Popular blocks</h2>
  <div class="products" style="margin-top:20px">{cards}</div>
  <div class="prod-cols" style="margin-top:56px">
    <div>{enquiry_form(root, city=l["city"])}</div>
    <div><h2 class="h2">Our other location</h2><div class="places">{place_html(other, root)}</div><p style="margin-top:20px"><a class="link" href="../products/">See all 13 product ranges</a></p></div>
  </div>
</div></section></main>
'''
    write(l["slug"] + "/index.html", head(root, l["slug"] + "/", c["title"], c["desc"], img=f'assets/img/{c["img"] if "/" in c["img"] else "stock/" + c["img"]}.webp', schema=ld(graph)) + header(root) + main + footer(root))

def build_contact():
    root = "../"
    places = "".join(f'<div class="loc-card"><div class="label">{e(l["role"])}</div><h2 class="h2" style="font-size:1.8rem">{e(l["name"])}</h2><address class="addr">{e(addr_line(l))}</address><div class="row2"><a class="link" href="{maps_link(l)}" target="_blank" rel="noopener">Directions</a><a class="link" href="../{l["slug"]}/">Location page</a></div><iframe class="map" title="Map: {e(l["name"])}" src="{maps_embed(l)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>' for l in LOCATIONS)
    graph = [org_schema()] + [loc_schema(l) for l in LOCATIONS] + [crumbs([("Home", ""), ("Contact", "contact/")]), {"@type": "ContactPage", "url": SITE_URL + "contact/", "name": "Contact Satyam Pavers"}]
    main = f'''<main id="main"><section><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a> / <span>Contact</span></nav>
  <div class="prod-cols" style="margin-top:0;align-items:start">
    <div><div class="label">Contact</div><h1 class="h1">Send an enquiry</h1>
      <p class="answer">Tell us what you are paving, the area in square feet and your site location. Our sales team replies the same working day on WhatsApp or by phone.</p>
      <p style="margin-top:16px">Prefer to call? <a class="num" href="tel:{CONTACT["tel"]}"><b>{CONTACT["display"]}</b></a> <button type="button" class="copy-btn" data-copy>Copy number</button></p></div>
    <div>{enquiry_form(root)}</div>
  </div>
  <div class="locs">{places}</div>
</div></section></main>
'''
    write("contact/index.html", head(root, "contact/", "Contact Satyam Pavers | Paver Block Enquiry, Bhopal & Mandideep",
          "Send an enquiry for paver blocks and kerb stones. Sales office: Kanha Building, Zone-II, MP Nagar, Bhopal. Factory: Mandideep.", schema=ld(graph)) + header(root) + main + footer(root))

def build_404():
    root = "/Paver-Client-Website/"
    main = f'<main id="main"><section><div class="wrap"><h1 class="h1">Page not found</h1><p class="answer">This page has moved. Try our <a href="{root}products/">products</a> or <a href="{root}contact/">send an enquiry</a>.</p></div></section></main>'
    page = head(root, "404.html", "Page not found — Satyam Pavers", "This page could not be found.").replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
    write("404.html", page + header(root) + main + footer(root))

def build_meta():
    urls = [("", "1.0"), ("products/", "0.9")] + [("products/" + p["slug"] + "/", "0.8") for p in PRODUCTS] + [(l["slug"] + "/", "0.9") for l in LOCATIONS] + [(a["slug"] + "/", "0.7") for a in SERVICE_AREAS] + [(g["slug"] + "/", "0.7") for g in GUIDES] + [("tools/paver-calculator/", "0.7")] + [("contact/", "0.7")]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE_URL}{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for u, pr in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /src/\nDisallow: /tools/\nDisallow: /docs/\n\n# AI search crawlers are welcome\nUser-agent: OAI-SearchBot\nAllow: /\nUser-agent: Claude-SearchBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n")
    lines = [f"# {BRAND}", "", f"> {BRAND} ({LEGAL}) manufactures concrete paver blocks, interlocking tiles, paver tiles and kerb stones at its factory in Mandideep, Madhya Pradesh, and sells from a sales office in MP Nagar, Bhopal. It supplies shopping malls, schools and colleges, factories and warehouses, housing societies, petrol pumps and homes, and delivers across Bhopal, Raisen, Sehore, Vidisha, Narmadapuram and Indore. Prices are given on enquiry only.", "",
             "## Locations"] + [f"- [{l['role']}]({SITE_URL}{l['slug']}/): {addr_line(l)}" for l in LOCATIONS] + ["", "## Products"] + \
            [f"- [{p['full']}]({SITE_URL}products/{p['slug']}/): {p['answer']}" for p in PRODUCTS] + ["", "## Delivery areas"] + [f"- [Paver blocks in {a['name']}]({SITE_URL}{a['slug']}/): delivered from Mandideep, about {a['km']} km" for a in SERVICE_AREAS] + \
            ["", "## Guides"] + [f"- [{g['h1']}]({SITE_URL}{g['slug']}/): {g['answer']}" for g in GUIDES] + ["", f"- [Paver block calculator]({SITE_URL}tools/paver-calculator/): estimates block count from area, with 5% wastage.", "", "## Common questions"] + [f"- Q: {q}\n  A: {a}" for q, a in FAQ] + \
            ["", "## Contact", f"- [Send an enquiry]({SITE_URL}contact/): enquiry form and WhatsApp, mobile {CONTACT['display']}", f"- {BRAND} is a brand of {LEGAL}.", ""]
    write("llms.txt", "\n".join(lines))
    write("site.webmanifest", json.dumps({"name": BRAND, "short_name": BRAND, "start_url": "./", "display": "standalone", "background_color": "#F2F1ED", "theme_color": "#151412",
                                          "icons": [{"src": "assets/brand/logo-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "assets/brand/logo-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=1))
    data = {"products": PRODUCTS, "photos": {p["id"]: images_of(p) for p in PRODUCTS}, "colours": {p["id"]: colours_of(p) for p in PRODUCTS}}
    write("assets/js/data.js", "/* generated by tools/build.py — edit the data there */\nwindow.SP_CONTACT = " + json.dumps(CONTACT) + ";\nwindow.SP_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n")

if __name__ == "__main__":
    import_generated(); build_home(); build_products_index()
    for i, p in enumerate(PRODUCTS): build_product(p, i)
    for l in LOCATIONS: build_location(l)
    for a in SERVICE_AREAS: build_area(a)
    for g in GUIDES: build_guide(g)
    build_calc()
    build_contact(); build_404(); build_meta()
    print("built", 6 + len(PRODUCTS) + len(SERVICE_AREAS) + len(GUIDES) + 1, "pages")
