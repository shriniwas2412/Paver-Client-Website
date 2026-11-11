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

# ---------- trust facts: fill these only with verified details from the client ----------
# Every section below renders only when its value is filled in, so nothing made-up ever goes live.
# docs/client-inputs.md lists what to ask the client for.
EMAIL = ""              # e.g. "sales@satyampavers.in"; adds a "Send by email" option to the enquiry form
YEARS = None            # year the business started, e.g. 2009; shown in the footer and Organization schema
GSTIN = ""              # shown in the footer
HOURS = {}              # per location id: [(["Monday", ..., "Saturday"], "10:00", "19:00")]
SAME_AS = []            # profile URLs: Google Business Profile, IndiaMART, Justdial, Facebook, Instagram
GBP_REVIEW_URL = ""     # Google Business Profile "Ask for reviews" link
ANALYTICS = {"ga4": "", "clarity": ""}   # e.g. {"ga4": "G-XXXXXXX"}; no tracking script loads while empty
# Real supplied projects: dict(site="Green Valley Society", place="Kolar Road, Bhopal", product="zigzag", sqft=12000,
#   year=2025, photo="assets/img/projects/green-valley.webp", note="80 mm grey with red bands")
PROJECTS = []
# Real Google reviews, copied word for word: dict(name="R. Sharma", place="Awadhpuri, Bhopal", text="...", rating=5)
REVIEWS = []

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
  dict(id="diamond", slug="diamond-paver-blocks", code="DM", name="Diamond", full="Diamond Paver Blocks", alt="Rhombus-shaped paver", uses=["walk","drive"], c="red",
       desc="Diamond-shaped blocks that lock edge to edge in a crisp lattice. Two colours laid in alternate rows give a striking pattern for entrances and plazas.",
       size="On request", thick=[60,80], per=None, load="Foot to light", patterns=["diamond"],
       best=["Entrances and forecourts","Plazas and mall walkways","Society and temple courtyards"],
       answer="Diamond paver blocks are rhombus-shaped concrete blocks that lock edge to edge in a lattice. They come in 60 and 80 mm and suit entrances, forecourts, plazas and courtyards, laid in one colour or in two-colour rows."),
  dict(id="cosmic", slug="cosmic-paver-blocks", code="CS", name="Cosmic", full="Cosmic Paver Blocks", alt="Curved three-arm interlocking paver", uses=["walk","drive"], c="yellow", lay="Interlocking, laid in flowing rows",
       desc="Three curved arms lock into each other for a flowing, decorative floor. The dotted face gives a sure grip underfoot.",
       size="On request", thick=[60,80], per=None, load="Foot to light", patterns=["cosmic"],
       best=["Temple and school courtyards","Society walkways","Decorative driveways"],
       answer="Cosmic paver blocks have three curved arms that lock together in flowing rows. The dotted face gives grip underfoot. They come in 60 and 80 mm, in red and yellow, for courtyards, walkways and decorative driveways."),
  dict(id="hexagon", slug="hexagon-3d-paver-tiles", code="HX", name="Hexagon Tile", full="Hexagon 3D-Cube Paver Tiles", alt="Grooved 3D-cube hexagon tile", uses=["walk"], c="grey", lay="Hexagon grid (3D-cube effect)",
       desc="A hexagon with three grooved faces that read as a 3D cube when laid. The honeycomb layout spreads foot traffic evenly, so it suits wide walkways, parks and plazas as well as terraces and lobbies.",
       size="On request", thick=[], per=None, load="Foot traffic", patterns=["hex"],
       best=["Wide walkways, parks and plazas","Building entrances and lobbies","Terraces and feature pathways"],
       answer="Hexagon 3D-cube paver tiles have three grooved faces that read as a cube when laid together in a honeycomb. They suit wide walkways, parks, plazas, building entrances and terraces with foot traffic."),
  dict(id="slate", slug="slate-finish-paver-slabs", code="SL", name="Slate Finish Slab", full="Slate Finish Paver Slabs", alt="Natural slate texture", uses=["walk"], c="grey", lay="Grid or staggered",
       desc="A moulded natural-slate face with soft ripples and veins. Looks like split stone for a fraction of the cost.",
       size="On request", thick=[], per=None, load="Foot traffic", patterns=["slab"],
       best=["Garden paths and patios","Poolside decks","Farmhouse and villa landscaping"],
       answer="Slate finish paver slabs have a moulded natural-slate face with ripples and veins, in grey and black. They give a split-stone look for garden paths, patios and poolsides."),
  dict(id="antiskid", slug="anti-skid-paver-blocks", code="AS", name="Anti-Skid Block", full="Anti-Skid Paver Blocks", alt="Leather-grain grip surface", uses=["walk","drive"], c="grey", lay="Stretcher bond or grid",
       desc="A fine leather-grain face that stays grippy when wet. Made for ramps, steps, poolsides and monsoon walkways.",
       size="On request", thick=[], per=None, load="Foot to light", patterns=["grip"],
       best=["Ramps and steps","Poolsides","Hospital and school walkways"],
       answer="Anti-skid paver blocks have a fine leather-grain face that stays grippy when wet. They are made for ramps, steps, poolsides and walkways that see heavy monsoon rain."),
  dict(id="cobble", slug="cobble-stone-pavers", code="CB", name="Cobble Stone", full="Cobble Stone Pavers", alt="Rough split-face cobble", uses=["walk","drive"], c="yellow", lay="Random rows or fan arcs",
       desc="Chunky cobbles with a rough split face for heritage driveways, courtyards, tree surrounds and landscape edging.",
       size="On request", thick=[], per=None, load="Foot to light", patterns=["cobble"],
       best=["Heritage-style driveways","Tree surrounds and edging","Hotel and resort courtyards"],
       answer="Cobble stone pavers are chunky concrete cobbles with a rough split face, in beige and black. They suit heritage-style driveways, courtyards, tree surrounds and landscape edging."),
  dict(id="speckled", slug="speckled-finish-paver-blocks", code="SP", name="Speckled Finish Block", full="Speckled Finish Paver Blocks", alt="Exposed-chip terrazzo look", uses=["walk"], c="grey", lay="Grid or staggered",
       desc="A smooth face scattered with stone chips, like terrazzo. A refined finish for lobbies, terraces and clubhouse paths.",
       size="On request", thick=[], per=None, load="Foot traffic", patterns=["slabst"],
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
PATTERN_NAMES = {"cosmic": "Interlocking", "cobble": "Random rows", "slab": "Grid", "slabst": "Staggered", "grip": "Stretcher bond", "diamond": "Diamond", "hex": "Honeycomb", "herringbone":"Herringbone","bond":"Running bond","basket":"Basket weave","stack":"Stack bond","zig":"Stretcher","ishape":"Stretcher","grid":"Grid","staggered":"Staggered","combo5":"Random modular","tiles":"Grid"}
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
def view_of(p, c, root, card=False):
    if card and not p.get("noRender") and c in RENDER_COLOURS:
        return root + f'assets/img/laid/{p["id"]}-{c}.webp', False, f'{p["name"]} pattern in {COLOURS[c].lower()}'
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
            "hasMap": maps_link(l), "areaServed": AREAS, **hours_schema(l)}
def hours_schema(l):
    h = HOURS.get(l["id"])
    return {"openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": days, "opens": o, "closes": c} for days, o, c in h]} if h else {}
def org_schema():
    o = {"@type": "Organization", "@id": ORG_ID, "name": BRAND, "legalName": LEGAL, "url": SITE_URL,
            "logo": SITE_URL + "assets/brand/logo-512.png", "telephone": CONTACT["tel"],
            "contactPoint": {"@type": "ContactPoint", "telephone": CONTACT["tel"], "contactType": "sales", "areaServed": "IN", "availableLanguage": ["en", "hi"]},
            "address": {"@type": "PostalAddress", "streetAddress": LOCATIONS[0]["street"], "addressLocality": LOCATIONS[0]["locality"],
                        "addressRegion": "Madhya Pradesh", "postalCode": LOCATIONS[0]["pin"], "addressCountry": "IN"},
            "description": "Manufacturer of concrete paver blocks, kerb stones and paver tiles in Mandideep, supplying malls, stadiums, schools, hospitals, factories, housing societies, petrol pumps and homes across Bhopal and central Madhya Pradesh."}
    if SAME_AS: o["sameAs"] = SAME_AS
    if YEARS: o["foundingDate"] = str(YEARS)
    if EMAIL: o["email"] = EMAIL
    if GSTIN: o["taxID"] = GSTIN
    return o
def ld(graph): return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + "</script>"
def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE_URL + u} for i, (n, u) in enumerate(items)]}

# ---------- page shell ----------
FONTS = "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Barlow+Condensed:wght@500;600;700&family=Mukta:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap"
# English path -> Hindi path, for pages that exist in both languages (hreflang links and the language button use it)
HI_PRODUCTS = ["zigzag", "ishape", "rectangular", "curved"]
HI_PAIRS = {"paver-blocks-bhopal/": "hi/", "products/": "hi/products/", "guides/paver-block-price-bhopal/": "hi/guides/paver-block-price-bhopal/",
            **{f"products/{s}/": f"hi/products/{s}/" for s in ("zig-zag-paver-blocks", "i-shape-paver-blocks", "rectangular-paver-blocks", "kerb-stones")}}
def analytics_tags():
    out = ""
    if ANALYTICS.get("ga4"):
        g = e(ANALYTICS["ga4"])
        out += f'<script async src="https://www.googletagmanager.com/gtag/js?id={g}"></script>\n<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{g}");</script>\n'
    if ANALYTICS.get("clarity"):
        c = e(ANALYTICS["clarity"])
        out += f'<script>(function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y)}})(window,document,"clarity","script","{c}");</script>\n'
    return out
def head(root, path, title, desc, img="assets/img/scenes/hero.webp", schema="", extra="", lang="en"):
    url = SITE_URL + path
    en_path = next((k for k, v in HI_PAIRS.items() if v == path), path) if lang == "hi" else path
    hi_path = HI_PAIRS.get(en_path)
    alt_attr, alts = "", ""
    if hi_path is not None:
        alts = (f'<link rel="alternate" hreflang="en-IN" href="{SITE_URL}{en_path}">\n<link rel="alternate" hreflang="hi-IN" href="{SITE_URL}{hi_path}">\n'
                f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}{en_path}">\n')
        alt_attr = f' data-alt="{root}{hi_path if lang == "en" else en_path}"'
    return f'''<!DOCTYPE html>
<html lang="{lang}" data-root="{root}"{alt_attr}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
{alts}<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="theme-color" content="#151412">
<meta name="geo.region" content="IN-MP"><meta name="geo.placename" content="Bhopal">
<meta property="og:type" content="website"><meta property="og:site_name" content="{BRAND}"><meta property="og:locale" content="{"hi_IN" if lang == "hi" else "en_IN"}">
<meta property="og:url" content="{url}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE_URL}{img}"><meta property="og:image:alt" content="{e(title)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{root}assets/brand/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{root}assets/brand/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{root}assets/brand/apple-touch-icon.png">
<link rel="manifest" href="{root}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="{FONTS}"></noscript>
<link rel="stylesheet" href="{root}assets/css/site.css?v={VER}">
{extra}{schema}{analytics_tags()}
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
      <a href="{root}products/" data-i18n="nav.products">Products</a>
      <a href="{root}#studio" data-i18n="nav.studio">Pattern studio</a>
      <a href="{root}#load" data-i18n="nav.load">Load guide</a>
      <a href="{root}#desk" id="navDesk">Home guide</a>
      <a href="{root}paver-blocks-bhopal/" data-i18n="nav.bhopal">Bhopal</a>
      <a href="{root}paver-blocks-mandideep/" data-i18n="nav.mandideep">Mandideep</a>
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
    use_links = "".join(f'<li><a href="{root}uses/{u["slug"]}/">{e(u["short"])}</a></li>' for u in USES)
    guide_links = "".join(f'<li><a href="{root}{g["slug"]}/">{e(g["h1"])}</a></li>' for g in GUIDES)
    hours = "".join(f'<li>{e(l["role"])} hours: ' + "; ".join(f'{days[0][:3]}–{days[-1][:3]} {o}–{c}' if len(days) > 1 else f'{days[0][:3]} {o}–{c}' for days, o, c in HOURS[l["id"]]) + '</li>' for l in LOCATIONS if HOURS.get(l["id"]))
    facts = " ".join(x for x in [f"Making paver blocks since {YEARS}." if YEARS else "", f"GSTIN {e(GSTIN)}." if GSTIN else ""] if x)
    email = f'<li>Email: <a href="mailto:{e(EMAIL)}">{e(EMAIL)}</a></li>' if EMAIL else ""
    return f'''<footer><div class="wrap">
  <div><b class="foot-brand"><svg width="28" height="28" aria-hidden="true"><use href="#logo"/></svg>{BRAND}</b><p style="margin-top:8px;max-width:30em">Concrete paver blocks, kerb stones and paver tiles, made in Mandideep for Bhopal, Indore and central Madhya Pradesh.</p>
    <p style="margin-top:14px"><a class="btn btn-primary" href="{root}contact/">Send enquiry</a></p>
    <p style="margin-top:14px"><a href="{root}hi/" lang="hi">हिंदी में पढ़ें: भोपाल में पेवर ब्लॉक</a></p></div>
  <div><h4>Products</h4><ul>{prods}<li><a href="{root}products/">All products →</a></li></ul>
    <h4 style="margin-top:20px">By use</h4><ul>{use_links}</ul></div>
  <div><h4>Visit us</h4><ul>{locs}{hours}<li><a href="{root}paver-blocks-bhopal/">Paver blocks in Bhopal</a></li><li><a href="{root}paver-blocks-mandideep/">Paver blocks in Mandideep</a></li><li><a href="{root}contact/">Contact &amp; enquiry</a></li><li><a href="{root}tools/paver-calculator/">Paver block calculator</a></li><li>Delivery: {area_links}</li><li class="num">Mobile: <a href="tel:{CONTACT["tel"]}">{CONTACT["display"]}</a></li>{email}</ul>
    <h4 style="margin-top:20px">Guides</h4><ul>{guide_links}</ul></div>
  <div class="legal">{BRAND} is a brand of {e(LEGAL)}, Madhya Pradesh. {facts} Sizes and block counts are typical values; colours of real blocks vary slightly in shade. Page updated {TODAY}.</div>
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
    src, real, cap = view_of(p, p["c"], root, card=True)
    href = f'{root}products/{p["slug"]}/'
    tag = "" if p["size"] == "On request" else f'<span class="tag">{e(p["size"])}</span>'
    dots = "".join(f'<button type="button" class="dot sm" id="dot-{p["id"]}-{c}" data-p="{p["id"]}" data-c="{c}" aria-label="{COLOURS[c]}" title="{COLOURS[c]}" aria-pressed="{str(c == p["c"]).lower()}" style="background:{HEX[c]}"></button>' for c in colours_of(p)) if interactive else ""
    cmp = f'<button type="button" class="cmp" id="cmp-{p["id"]}" data-cmp="{p["id"]}" aria-pressed="false"><b>✓</b>Compare</button>' if interactive else ""
    return (f'<article class="p" data-uses="{" ".join(p["uses"])}">'
            f'<a class="ph" href="{href}" aria-label="{e(p["full"])}: sizes and details"><img id="img-{p["id"]}" src="{src}" alt="{e(cap)}" loading="{"eager" if i < 3 else "lazy"}" width="800" height="1000">{tag}</a>'
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

def enquiry_form(root, product="", city="", message="", hi=False):
    opts = "".join(f'<option{" selected" if p["full"] == product else ""}>{e(p["full"])}</option>' for p in PRODUCTS)
    T = (dict(h="पूछताछ भेजें", note="आपकी पूछताछ WhatsApp में लिखी हुई खुलेगी। वहाँ भेजें दबाने तक कुछ नहीं जाता।", name="आपका नाम", phone="मोबाइल नंबर",
              product="ब्लॉक", unsure="पता नहीं — आप सुझाइए", area="एरिया (लगभग वर्ग फ़ुट)", city="साइट की जगह", ph_city="जैसे कोलार रोड, भोपाल",
              msg="और कुछ", ph_msg="मोटाई, रंग, कब तक चाहिए…", send="पूछताछ भेजें") if hi else
         dict(h="Send enquiry", note="Your enquiry opens in WhatsApp, typed in and ready. Nothing is sent until you press send there.", name="Your name", phone="Mobile number",
              product="Product", unsure="Not sure yet — please suggest", area="Area in sq ft (approx.)", city="Site location", ph_city="e.g. Kolar Road, Bhopal",
              msg="Anything else", ph_msg="Thickness, colour, timeline…", send="Send enquiry"))
    return f'''<form class="form enq" novalidate{' data-lang="hi"' if hi else ''}>
  <div><div class="label" style="color:var(--ink)">{T["h"]}</div><p class="note">{T["note"]}</p></div>
  <label>{T["name"]}<input name="name" autocomplete="name" required></label>
  <label>{T["phone"]}<input name="phone" type="tel" autocomplete="tel" inputmode="tel" required></label>
  <label>{T["product"]}<select name="product"><option value="">{T["unsure"]}</option>{opts}</select></label>
  <label>{T["area"]}<input name="area" type="number" min="1" inputmode="numeric"></label>
  <label>{T["city"]}<input name="city" value="{e(city)}" placeholder="{T["ph_city"]}"></label>
  <label>{T["msg"]}<input name="message" value="{e(message)}" placeholder="{T["ph_msg"]}"></label>
  <button class="btn btn-wa" type="submit"><svg><use href="#wa"/></svg>{T["send"]}</button>
  <div class="enq-done" role="status" tabindex="-1" hidden></div>
</form>'''

def callback_form(topic, hi=False):
    """One-field 'call me back' request. It goes through the same WhatsApp flow as the enquiry form."""
    h, p, b, n = (("कॉल बैक चाहिए?", "मोबाइल नंबर", "मुझे कॉल करें", "नंबर छोड़िए, हमारी सेल्स टीम आपको कॉल करेगी।") if hi else
                  ("Rather talk it through?", "Your mobile number", "Call me back", "Leave your number and our sales team will call you."))
    return f'''<form class="form enq cb" data-kind="callback" novalidate{' data-lang="hi"' if hi else ''}>
  <div><div class="label" style="color:var(--ink)">{h}</div><p class="note">{n}</p></div>
  <input type="hidden" name="product" value="{e(topic)}">
  <div class="cb-row"><label class="sr">{p}<input name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="{p}" required></label>
  <button class="btn btn-ink" type="submit"><svg><use href="#phone"/></svg>{b}</button></div>
  <div class="enq-done" role="status" tabindex="-1" hidden></div>
</form>'''

# ---------- delivery-town pages ----------
SERVICE_AREAS = [
  dict(name="Obedullaganj", slug="paver-blocks-obedullaganj", km=12, note="Obedullaganj is the nearest town to our factory, so small orders and urgent top-ups are easy to arrange.", popular=["zigzag", "rectangular", "curved"]),
  dict(name="Raisen", slug="paver-blocks-raisen", km=50, note="Mandideep is in Raisen district, and we supply homes, colonies and government-style works across the district.", popular=["ishape", "zigzag", "curved"]),
  dict(name="Narmadapuram", slug="paver-blocks-narmadapuram", km=55, note="Trucks run straight down NH-46 from Mandideep to Narmadapuram, Itarsi-side sites included.", popular=["zigzag", "cobble", "curved"]),
  dict(name="Sehore", slug="paver-blocks-sehore", km=65, note="For Sehore town and the Bhopal–Sehore road belt, we plan full-truck deliveries that match your site schedule.", popular=["rectangular", "zigzag", "tiles"]),
  dict(name="Vidisha", slug="paver-blocks-vidisha", km=85, note="For Vidisha we usually deliver in full truckloads, so larger driveways, colony roads and campus jobs work best.", popular=["ishape", "rectangular", "curved"]),
  dict(name="Indore", slug="paver-blocks-indore", km=215, note="Indore orders travel by full truckload along the Bhopal–Indore highway via Sehore and Dewas, so they suit colony roads, factory and warehouse yards, campuses and larger driveways. Tell us your quantity and we plan the trucks around your site schedule.", popular=["zigzag", "ishape", "curved"]),
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
  <div class="row2" style="margin-top:20px"><a class="btn btn-primary" href="#enquiry">Send enquiry</a><a class="link" href="../products/">See all 14 ranges</a></div>
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

# ---------- pages by use (what will drive on the floor) ----------
# Build-up numbers match the home-page load guide (assets/js/site.js LOADS): block + 30 mm sand + compacted stone sub-base.
USES = [
  dict(slug="paver-blocks-for-driveway", short="Home driveways", h1="Paver blocks for a home driveway",
       title="Paver Blocks for Driveway in Bhopal | Thickness & Pattern — Satyam Pavers",
       desc="Which paver block for a home driveway: 60 or 80 mm, zig-zag or rectangular in herringbone, how deep to dig and how many blocks you need. Made in Mandideep.",
       label="Homeowners · cars and SUVs", img="onsite/zigzag", img_alt="Zig-zag paver blocks laid on a driveway",
       answer="For a home driveway, use 60 mm interlocking blocks if a car parks there now and then, and 80 mm for daily cars and SUVs. Zig-zag (uni) blocks, or rectangular blocks laid in herringbone, hold best under turning wheels. Dig about 300 mm, build a 200 mm compacted stone base with 30 mm of sand on top, and fix kerb stones along the open edges.",
       build=dict(mm="60 / 80 mm", grade="M35–M40", base="150–200 mm", dig="240–310 mm"),
       picks=[("zigzag", "60 or 80 mm. Locks on every side; the most popular driveway block in Bhopal."), ("rectangular", "80 mm in herringbone. A classic look that takes turning cars."),
              ("combo5", "60 or 80 mm. A random, stone-like look for villas and farmhouses."), ("curved", "Kerb stones along the open edges stop blocks spreading.")],
       body=[("Pattern", "Lay rectangular blocks in herringbone (at 45° or 90°) on a driveway: the zig-zag joints spread the push from turning and braking wheels. Avoid stack bond, where long straight joints let blocks creep."),
             ("Slope and drainage", "Give the driveway a fall of about 1 in 60 away from the house, towards the gate or a drain. Water that stands on the sand bed through Bhopal's monsoon is what makes driveways sink."),
             ("Colours", "Grey hides tyre marks best. A border of red or yellow blocks frames the drive and marks the edges at night. Ask for one batch for the whole drive so the shade matches.")],
       faqs=[("Is 60 mm enough for a car driveway?", "Yes, for a home driveway where one car parks and drives slowly, as long as the stone base is built and compacted properly. Choose 80 mm for SUVs, daily use, or if delivery trucks or water tankers will come in."),
             ("How many blocks do I need for a 20 × 30 ft driveway?", "A 20 × 30 ft driveway is 600 sq ft. That is about 2,460 zig-zag blocks or about 2,900 rectangular blocks, including 5% extra for cutting at the edges."),
             ("Can paver blocks be laid over my old concrete driveway?", "Only if the old slab is sound and already slopes so water runs off. Lay a 25–30 mm sand bed on it, fix kerbs at the edges and leave a drainage path at the low end. If the slab is cracked or sinking, break it out and build a proper stone base."),
             ("How soon can I drive on a new paver driveway?", "As soon as the blocks are compacted and the joints are filled with sand. Unlike a concrete slab, there is no curing time to wait for.")]),
  dict(slug="parking-paver-blocks", short="Car parks", h1="Paver blocks for parking areas",
       title="Parking Paver Blocks in Bhopal | Car Park Paving — Satyam Pavers",
       desc="Paver blocks for car parks at shops, hospitals, offices and societies: 80 or 100 mm zig-zag and I-shape blocks, bay marking in coloured blocks, base depth and block count.",
       label="Shops, hospitals, offices, societies", img="stock/zigzag-parking", img_alt="Zig-zag pavers in a parking bay",
       answer="For a car park, use 80 mm zig-zag (uni) or I-shape (Behaton) interlocking blocks on a 200 mm compacted stone base. Where buses, trucks or delivery vans come in, step up to 100 mm. Mark bays and walkways in a contrasting colour of block instead of paint, so the markings never wear off.",
       build=dict(mm="80 / 100 mm", grade="M35–M50", base="200–250 mm", dig="310–380 mm"),
       picks=[("zigzag", "80 mm for cars, 100 mm where vans and trucks come in."), ("ishape", "80 or 100 mm. Spreads wheel loads; a favourite for large car parks."),
              ("rectangular", "80 mm in herringbone for smaller parking courts."), ("curved", "Kerbs round islands, medians and the paved edge.")],
       body=[("Mark bays in block, not paint", "Lay bay lines, arrows and walkways in yellow or red blocks against a grey field. The colour runs right through each block, so the markings last as long as the floor."),
             ("Drainage", "Give the car park a fall of about 1 in 60 towards drains. A car park that holds water loses its joint sand first, and the blocks start to rock."),
             ("Repairs without patches", "When a cable or drain line under the car park needs work, lift the blocks, fix it and lay the same blocks back. There is no patch of new concrete to show where you dug.")],
       faqs=[("Which thickness is right for a car park?", "80 mm for cars and SUVs. 100 mm if buses, delivery trucks or water tankers use it, even now and then."),
             ("How many blocks for a 5,000 sq ft car park?", "About 20,500 zig-zag blocks or about 18,900 I-shape blocks, including 5% extra for cutting at the edges."),
             ("Can you supply a large car park in phases?", "Yes. Large orders are made to schedule at our Mandideep plant and sent by the truckload as each section of your site is ready, colour-matched across batches."),
             ("Can bay lines be made in a different colour?", "Yes. Order a few hundred blocks in yellow or red alongside the grey, and lay them as lines and arrows. Tell us the layout and we will work out the split.")]),
  dict(slug="society-road-paver-blocks", short="Society & colony roads", h1="Paver blocks for society and colony roads",
       title="Paver Blocks for Society & Colony Roads | Bhopal — Satyam Pavers",
       desc="Paver blocks for housing-society and colony internal roads and footpaths: 80 mm I-shape and zig-zag, kerb stones, base depth, and phased supply for builders.",
       label="Builders · housing societies · colonies", img="onsite/society-road", img_alt="Society road paved with grey zig-zag pavers and red bands",
       answer="For colony and society internal roads, use 80 mm I-shape (Behaton) or zig-zag interlocking blocks on a 200–250 mm compacted stone base, with kerb stones on both edges. Footpaths beside the road can be 60 mm. Builders can order phase by phase, with colour matched across batches.",
       build=dict(mm="80 mm (roads) · 60 mm (footpaths)", grade="M35–M40", base="200–250 mm", dig="310–360 mm"),
       picks=[("ishape", "80 mm. Locks on four sides and spreads wheel loads along the road."), ("zigzag", "80 mm. The other favourite for colony roads; strong under braking."),
              ("rectangular", "60 mm for footpaths, laid in running bond."), ("curved", "Kerb stones on both edges of every road; curved kerbs at corners.")],
       body=[("Kerbs first", "Set kerb stones on a concrete bed along both edges before any block is laid. Without them the blocks slowly spread sideways under wheels and the road opens up at the edges."),
             ("Bands at gates and junctions", "A band of red or yellow blocks across the road at gates, speed breakers and junctions slows traffic and marks crossings without paint."),
             ("Services under the road", "Water, sewer and cable lines under a paver road can be reached by lifting the blocks and laying the same ones back. With a concrete road the cut stays visible for good."),
             ("Phased supply for builders", "Send your total quantity and phase plan. We make to schedule at Mandideep and send full truckloads as each phase is ready, from matched batches so the shade stays even across the colony.")],
       faqs=[("Which paver block is best for a society road?", "80 mm I-shape (Behaton) or zig-zag (uni) interlocking blocks. Both lock on all sides and spread car loads. Use 100 mm where buses, school vans or construction trucks run daily."),
             ("Why do I need kerb stones?", "Kerbs hold the edge of the paving. Without them the outer blocks move outwards under wheels and the joints open up across the road."),
             ("Can we get the whole colony in one shade?", "Yes. Tell us the total quantity at the start and we plan production so every phase comes from matched batches."),
             ("Do you give a supply plan for builders?", "Yes. Send the road and footpath areas and your phase dates, and our team sends a supply plan with block counts, kerb lengths and delivery dates.")]),
  dict(slug="petrol-pump-paver-blocks", short="Petrol pumps", h1="Paver blocks for petrol pumps",
       title="Paver Blocks for Petrol Pumps | Heavy-Duty 100 mm — Satyam Pavers",
       desc="Heavy-duty paver blocks for petrol pump forecourts: 100 mm zig-zag and I-shape blocks, M40–M50 grade, base depth, oil stains, and paving in phases while the pump stays open.",
       label="Fuel stations · forecourts · tanker areas", img="stock/zigzag-laid", img_alt="Grey zig-zag paving with red bands",
       answer="Petrol pump forecourts carry tankers, trucks and braking cars, so use 100 mm zig-zag (uni) or I-shape (Behaton) interlocking blocks, grade M40–M50, on a 250 mm compacted stone base, with kerb stones round the islands and edges. Oil drips can be cleaned off, and a stained or damaged block can be lifted and swapped.",
       build=dict(mm="100 mm", grade="M40–M50", base="250 mm", dig="about 380 mm"),
       picks=[("zigzag", "100 mm. The standard forecourt block; wavy joints resist braking wheels."), ("ishape", "100 mm. Spreads tanker loads; good for the unloading bay."),
              ("antiskid", "For the walkway to the shop and air point; grippy when wet."), ("curved", "Kerbs round fuel islands, medians and the forecourt edge.")],
       body=[("The tanker bay", "The spot where the tanker stands to unload takes the heaviest load on the site. Use 100 mm blocks there and give it the full stone base, even if the car lanes are lighter."),
             ("Oil and fuel stains", "Soak fresh spills with sawdust or cement powder, then scrub with detergent and warm water. A block that stays badly stained can be lifted and replaced with one from the same batch."),
             ("Keep the pump open", "Paving can go in section by section. Each section takes traffic as soon as it is compacted and the joints are filled, so part of the forecourt can stay open while the rest is laid.")],
       faqs=[("Which paver thickness for a petrol pump?", "100 mm, grade M40–M50, on a 250 mm compacted stone base. Tankers and trucks turn and brake on a forecourt every day, so thinner blocks wear and rut."),
             ("Will diesel and oil damage paver blocks?", "Spills stain concrete but do not weaken a well-made block. Clean fresh spills quickly; a breathable concrete sealer makes cleaning easier."),
             ("Can the forecourt be paved without closing the pump?", "Yes. Lay it section by section; each section can be used once it is compacted and the joints are filled."),
             ("How many blocks for a 10,000 sq ft forecourt?", "About 41,000 zig-zag blocks or about 37,800 I-shape blocks, including 5% extra for cutting. Send your drawing and we will confirm the count and kerb length.")]),
  dict(slug="factory-yard-paver-blocks", short="Factory & warehouse yards", h1="Heavy-duty paver blocks for factory yards",
       title="Heavy Duty Paver Blocks for Factory & Warehouse Yards — Satyam Pavers",
       desc="Heavy-duty 100 mm I-shape and zig-zag paver blocks for factory yards, warehouses, loading bays and truck roads in Mandideep, Govindpura and Bhopal. M50 for forklifts.",
       label="Factories · warehouses · loading bays", img="onsite/ishape", img_alt="I-shape paver blocks laid on site",
       answer="For factory yards, warehouses and loading bays, use 100 mm I-shape (Behaton) interlocking blocks, grade M50 where forklifts and containers run, on a 250–300 mm compacted stone base. 100 mm zig-zag suits truck roads. Pavers take point loads from forklift wheels and container legs, and can be lifted when underground services need work.",
       build=dict(mm="100 mm", grade="M40–M50", base="250–300 mm", dig="380–430 mm"),
       picks=[("ishape", "100 mm, M50. The heavy-duty choice for forklifts, containers and loading bays."), ("zigzag", "100 mm. Truck roads and turning areas, laid in herringbone."),
              ("curved", "Kerbs along roads, loading-bay edges and green areas.")],
       body=[("Close to Mandideep and Govindpura", "Our factory is in Mandideep industrial area itself, so units in Mandideep and Obedullaganj get the shortest delivery runs, and Govindpura and other Bhopal industrial areas are a short trip up NH-46."),
             ("Forklifts and point loads", "Forklift wheels and container legs press on a small area. A 100 mm M50 block on a well-compacted 300 mm base spreads that load; a thinner block or a weak base lets it punch down and rock."),
             ("Plan the yard in zones", "Pave forklift aisles and loading bays in 100 mm M50, truck roads in 100 mm, and staff walkways in 60 mm. Zoning keeps the cost in the places that carry the load.")],
       faqs=[("Which paver block for forklifts?", "100 mm I-shape (Behaton) blocks in M50 grade on a 300 mm compacted stone base. Ask your site engineer to confirm the base for your soil."),
             ("Are paver blocks better than a concrete floor for a yard?", "For outdoor yards, usually yes: pavers do not crack across the whole surface, drain at the joints, and can be lifted to reach cables and pipes. Indoor warehouse floors that need to be dead flat for racking are usually concrete."),
             ("How are the blocks checked?", "Sample blocks are checked for size, strength and water absorption before dispatch. Ask us for the details for the grade you order."),
             ("Can you supply a large yard on a schedule?", "Yes. Send the area and the dates, and we make to schedule and deliver by the truckload as each zone is ready.")]),
]
def uses_for(pid): return [u for u in USES if any(i == pid for i, _ in u["picks"])]

def build_use(u):
    root = "../../"
    url = f'uses/{u["slug"]}/'
    b = u["build"]
    rows = "".join(f'<tr><th scope="row">{k}</th><td>{e(v)}</td></tr>' for k, v in [("Block thickness", b["mm"]), ("Strength grade", b["grade"]), ("Bedding sand", "25–30 mm"), ("Stone sub-base (compacted)", b["base"]), ("Total dig depth (approx.)", b["dig"])])
    picks = "".join(f'<li><a class="link" href="{root}products/{P(i)["slug"]}/">{e(P(i)["full"])}</a><br><span class="note" style="font-size:.92rem">{e(t)}</span></li>' for i, t in u["picks"])
    cards = "".join(card(P(i), root, 9, interactive=False) for i, _ in u["picks"][:3])
    secs = "".join(f'<h2 class="h2" style="margin-top:40px">{e(h)}</h2><p style="margin-top:10px;max-width:68ch">{e(t)}</p>' for h, t in u["body"])
    others = " · ".join(f'<a class="link" href="{root}uses/{x["slug"]}/">{e(x["short"])}</a>' for x in USES if x is not u)
    graph = [org_schema(), {"@type": "Service", "name": u["h1"], "serviceType": "Concrete paver block supply", "description": u["answer"], "provider": {"@id": ORG_ID},
              "areaServed": [{"@type": "City", "name": a} for a in AREAS]},
             crumbs([("Home", ""), (u["h1"], url)]), faq_schema(u["faqs"])]
    main = f'''<main id="main"><section><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{root}">Home</a> / <span>{e(u["h1"])}</span></nav>
  <div class="prod">
    <figure class="gal"><img src="{root}assets/img/{u["img"]}.webp" alt="{e(u["img_alt"])}" width="1100" height="825" fetchpriority="high"></figure>
    <div class="prod-info">
      <div class="label">{e(u["label"])}</div>
      <h1 class="h1">{e(u["h1"])}</h1>
      <p class="answer">{e(u["answer"])}</p>
      <div class="row2"><a class="btn btn-primary" href="#enquiry">Send enquiry</a><a class="link" href="{root}tools/paver-calculator/">Count your blocks</a></div>
    </div>
  </div>
  <div class="prod-cols">
    <div><h2 class="h2">Build-up</h2><div class="tbl" style="margin-top:14px"><table class="spec"><tbody>{rows}</tbody></table></div>
      <p class="note" style="margin-top:8px">Typical build-up. Your site engineer confirms the sub-base for your soil. See the <a href="{root}#load">load guide</a> and <a href="{root}guides/how-to-lay-paver-blocks/">how to lay paver blocks</a>.</p></div>
    <div><h2 class="h2">Blocks we suggest</h2><ul class="asklist" style="margin-top:14px">{picks}</ul></div>
  </div>
  {secs}
  <h2 class="h2" style="margin-top:56px">Suggested blocks</h2>
  <div class="products" style="margin-top:20px">{cards}</div>
  <div class="prod-cols" style="margin-top:56px" id="enquiry">
    <div>{enquiry_form(root, message="For: " + u["short"].lower())}</div>
    <div><h2 class="h2">Questions</h2><div class="faq" style="margin-top:16px">{faq_html(u["faqs"])}</div>
      <div style="margin-top:24px">{callback_form(u["h1"])}</div>
      <p style="margin-top:20px">Other uses: {others}</p></div>
  </div>
</div></section></main>
'''
    write(url + "index.html", head(root, url, u["title"], u["desc"], img=f'assets/img/{u["img"]}.webp', schema=ld(graph)) + header(root) + main + footer(root))

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
  dict(slug="guides/paver-block-price-bhopal", title="Paver Block Price in Bhopal: What Decides the Cost | Satyam Pavers", h1="Paver block price in Bhopal: what decides the cost",
       desc="What decides the price of paver blocks in Bhopal: thickness, shape, colour, finish, quantity and delivery. How to compare quotes and get an exact rate in one message.",
       answer="The price of paver blocks in Bhopal depends on six things: thickness, shape, colour, surface finish, quantity and delivery distance. Laying is a separate cost from supply. Send us your area, block, thickness, colour and site location, and we reply the same working day with factory-direct terms for your order.",
       howto=False, enquiry=True,
       steps=[("Thickness", "Thickness moves the price most, because it sets how much concrete goes into each block. 60 mm costs least, then 80 mm, then 100 mm. Buy the thickness your load needs and no more: 60 mm for paths and light driveways, 80 mm for daily cars and colony roads, 100 mm for trucks and forklifts."),
              ("Shape and coverage", "Quotes come per block or per square foot. Always compare per square foot: a zig-zag block covers more ground than a rectangular one, so you need fewer of them (about 3.9 against 4.6 per sq ft)."),
              ("Colour and finish", "Grey blocks have no added pigment and are usually the lowest-priced. Red, yellow, black and other colours have pigment mixed through the block, which adds to the cost. Decorative faces such as slate, cobble, speckled and anti-skid cost more than plain blocks."),
              ("Quantity", "Larger orders get better terms, because making and delivering by the full truckload spreads the cost over more blocks. Builders paving a whole colony can fix terms once for phased delivery."),
              ("Delivery distance and site access", "Our factory is in Mandideep, about 25 km from Bhopal. Sites in Bhopal, Mandideep and Obedullaganj are the shortest runs; Raisen, Sehore, Vidisha, Narmadapuram and Indore are further. Narrow lanes where a truck cannot reach the site add handling."),
              ("Supply and laying are separate", "The supply price covers blocks delivered to your site. Laying adds labour, sand, the stone sub-base, kerb stones and compaction, and depends on how much digging your site needs. When you compare quotes, compare supply with supply and laying with laying."),
              ("Watch out for very cheap blocks", "A block much cheaper than the rest is often thinner than stated, cured for too short a time or low in cement. Check the thickness with a tape, look for clean, sharp edges and even colour, and ask which strength grade it is made to."),
              ("Get an exact rate in one message", "Send the area in square feet, the block (or what will drive on it), thickness, colour, site location and when you need it. That is everything we need to quote. Use the enquiry form below or WhatsApp.")],
       faqs=[("What is the price of paver blocks per sq ft in Bhopal?", "It depends on thickness, shape, colour, finish, quantity and site location, so we quote for each order. Send those details and we reply with factory-direct terms the same working day."),
             ("Are grey paver blocks cheaper than coloured ones?", "Usually, yes. Grey blocks have no added pigment; red, yellow and black blocks carry the cost of the pigment mixed through them."),
             ("Is delivery included in the price?", "The terms we send are for delivery to your site location, so you can compare them directly with other quotes."),
             ("Why buy from the factory instead of a dealer?", "We make the blocks at our own Mandideep plant and sell from our MP Nagar office, with no dealer margin in between. Your order comes from matched batches, so the shade stays even across the floor.")],
       hi=dict(title="भोपाल में पेवर ब्लॉक का रेट: क़ीमत किन बातों पर तय होती है | सत्यम पेवर्स", h1="भोपाल में पेवर ब्लॉक का रेट किन बातों पर तय होता है",
               desc="भोपाल में पेवर ब्लॉक का रेट मोटाई, आकार, रंग, फ़िनिश, मात्रा और डिलीवरी पर निर्भर करता है। कोटेशन की तुलना कैसे करें और एक मैसेज में सही रेट कैसे पाएँ।",
               answer="भोपाल में पेवर ब्लॉक का रेट छह बातों पर तय होता है: मोटाई, आकार, रंग, सतह की फ़िनिश, मात्रा और साइट की दूरी। बिछाई (लेइंग) का खर्च सप्लाई से अलग होता है। अपना एरिया, ब्लॉक, मोटाई, रंग और साइट की जगह भेजिए — हम उसी कामकाजी दिन फैक्ट्री-डायरेक्ट रेट भेजते हैं।",
               steps=[("मोटाई", "रेट पर सबसे ज़्यादा असर मोटाई का होता है, क्योंकि इसी से तय होता है कि हर ब्लॉक में कितना कंक्रीट लगेगा। 60 mm सबसे सस्ता, फिर 80 mm, फिर 100 mm। उतनी ही मोटाई लें जितनी ज़रूरत है: पैदल रास्ते और हल्के ड्राइववे के लिए 60 mm, रोज़ की कारों और कॉलोनी की सड़कों के लिए 80 mm, ट्रक और फ़ोर्कलिफ़्ट के लिए 100 mm।"),
                      ("आकार और कवरेज", "रेट प्रति ब्लॉक या प्रति वर्ग फ़ुट बताया जाता है। तुलना हमेशा प्रति वर्ग फ़ुट करें: ज़िग-ज़ैग ब्लॉक रेक्टैंगुलर से ज़्यादा जगह ढकता है, इसलिए कम ब्लॉक लगते हैं (लगभग 3.9 बनाम 4.6 प्रति वर्ग फ़ुट)।"),
                      ("रंग और फ़िनिश", "ग्रे ब्लॉक में अलग से रंग नहीं मिलाया जाता, इसलिए वह आम तौर पर सबसे किफ़ायती होता है। लाल, पीले और काले ब्लॉक में रंग पूरे ब्लॉक में मिला होता है, जिससे क़ीमत बढ़ती है। स्लेट, कोबल, स्पेकल्ड और एंटी-स्किड जैसी डिज़ाइनर सतहें सादे ब्लॉक से महँगी होती हैं।"),
                      ("मात्रा", "बड़े ऑर्डर पर बेहतर रेट मिलता है, क्योंकि पूरे ट्रक के हिसाब से बनाने और भेजने में खर्च ज़्यादा ब्लॉकों पर बँट जाता है। पूरी कॉलोनी बनाने वाले बिल्डर चरणों में डिलीवरी के लिए एक बार में रेट तय कर सकते हैं।"),
                      ("दूरी और साइट तक पहुँच", "हमारी फैक्ट्री मंडीदीप में है, भोपाल से लगभग 25 km। भोपाल, मंडीदीप और ओबेदुल्लागंज सबसे पास हैं; रायसेन, सीहोर, विदिशा, नर्मदापुरम और इंदौर दूर हैं। जहाँ ट्रक साइट तक न पहुँच सके, वहाँ ढुलाई का खर्च बढ़ता है।"),
                      ("सप्लाई और बिछाई अलग हैं", "सप्लाई रेट में साइट तक पहुँचाए गए ब्लॉक आते हैं। बिछाई में मज़दूरी, रेत, गिट्टी का बेस, कर्ब स्टोन और कॉम्पैक्शन जुड़ते हैं, जो आपकी साइट की खुदाई पर निर्भर है। कोटेशन मिलाते समय सप्लाई की तुलना सप्लाई से और बिछाई की बिछाई से करें।"),
                      ("बहुत सस्ते ब्लॉक से सावधान", "जो ब्लॉक बाक़ी से बहुत सस्ता हो, वह अक्सर बताई गई मोटाई से पतला, कम दिन क्योरिंग वाला या कम सीमेंट वाला होता है। टेप से मोटाई नापें, साफ़ और सीधे किनारे और एक जैसा रंग देखें, और पूछें कि ब्लॉक किस स्ट्रेंथ ग्रेड का है।"),
                      ("एक मैसेज में सही रेट", "एरिया (वर्ग फ़ुट), ब्लॉक (या उस पर क्या चलेगा), मोटाई, रंग, साइट की जगह और कब तक चाहिए — बस इतना भेजिए। नीचे दिया फ़ॉर्म या WhatsApp इस्तेमाल करें।")],
               faqs=[("भोपाल में पेवर ब्लॉक का रेट प्रति वर्ग फ़ुट क्या है?", "रेट मोटाई, आकार, रंग, फ़िनिश, मात्रा और साइट की जगह पर निर्भर है, इसलिए हम हर ऑर्डर के लिए अलग रेट देते हैं। ये जानकारी भेजिए, उसी कामकाजी दिन जवाब मिलेगा।"),
                     ("क्या ग्रे पेवर ब्लॉक रंगीन ब्लॉक से सस्ते होते हैं?", "आम तौर पर हाँ। ग्रे ब्लॉक में अलग से रंग नहीं मिलाया जाता; लाल, पीले और काले ब्लॉक में रंग का खर्च जुड़ता है।"),
                     ("क्या डिलीवरी रेट में शामिल है?", "हम जो रेट भेजते हैं वह आपकी साइट तक डिलीवरी के साथ होता है, ताकि आप दूसरे कोटेशन से सीधे तुलना कर सकें।"),
                     ("डीलर की जगह फैक्ट्री से क्यों ख़रीदें?", "ब्लॉक हमारी अपनी मंडीदीप फैक्ट्री में बनते हैं और एमपी नगर कार्यालय से बिकते हैं — बीच में डीलर का मार्जिन नहीं। पूरा ऑर्डर मिलते-जुलते बैच से आता है, इसलिए फ़र्श का रंग एक जैसा रहता है।")])),
  dict(slug="guides/60mm-vs-80mm-vs-100mm-paver-blocks", title="60 mm vs 80 mm vs 100 mm Paver Blocks: Which Thickness? | Satyam Pavers", h1="60 mm vs 80 mm vs 100 mm paver blocks",
       desc="Which paver block thickness do you need? 60 mm for paths and light driveways, 80 mm for cars and colony roads, 100 mm for trucks and forklifts, with grade, base and dig depth.",
       answer="Use 60 mm paver blocks for footpaths, gardens, terraces and home driveways with light car use; 80 mm for daily cars, SUVs, colony roads and car parks; and 100 mm for buses, trucks, petrol pumps, factory yards and forklifts. The stone base under the block matters as much as its thickness.",
       howto=False,
       table=("Thickness at a glance", ["Thickness", "Use it for", "Strength grade", "Stone sub-base", "Dig depth (approx.)"],
              [["60 mm", "Footpaths, gardens, terraces, two-wheelers, light home driveways", "M30–M35", "100–150 mm", "190–240 mm"],
               ["80 mm", "Daily cars and SUVs, colony roads, car parks", "M35–M40", "200 mm", "about 310 mm"],
               ["100 mm", "Buses, trucks, petrol pumps, factory roads", "M40–M50", "250 mm", "about 380 mm"],
               ["100 mm, M50", "Forklifts, loading bays, container yards", "M50", "300 mm", "about 430 mm"]]),
       steps=[("Why thicker blocks carry more", "A thicker block is stiffer and locks deeper into its neighbours, so a wheel load spreads over a wider area of base instead of pushing single blocks down. That is why ruts show first on thin blocks under heavy wheels."),
              ("The base matters as much", "An 80 mm block on a poor base sinks sooner than a 60 mm block on a well-compacted one. Build the stone sub-base in compacted layers and fix kerbs at the edges; a thicker block will not rescue a weak base."),
              ("When to step up a size", "Go one thickness up if delivery trucks, water tankers or construction vehicles will use the floor even now and then, or where cars turn sharply in one spot, such as at a gate."),
              ("Which shapes come in which thickness", "Zig-zag, I-shape and rectangular blocks come in 60, 80 and 100 mm. Square, Combo 5, diamond and cosmic blocks come in 60 and 80 mm. Decorative finishes such as slate, speckled and hexagon tiles are made for foot traffic.")],
       faqs=[("Is 60 mm paver block enough for cars?", "For a home driveway with light, slow car use on a good base, yes. For daily cars, SUVs or colony roads, use 80 mm."),
             ("Which thickness for a petrol pump or truck yard?", "100 mm, grade M40–M50, on a 250 mm compacted stone base. Use M50 on a 300 mm base where forklifts or containers run.")]),
  dict(slug="guides/paver-blocks-vs-tiles-vs-concrete-driveway", title="Paver Blocks vs Concrete vs Tiles for a Driveway | Satyam Pavers", h1="Paver blocks vs concrete vs tiles for a driveway",
       desc="Paver blocks, a concrete slab, Kota stone or tiles for your driveway? Load, grip in the rain, drainage, cracks, repairs and looks compared for Indian homes.",
       answer="For a driveway that cars use every day, interlocking paver blocks are usually the best long-term choice: they carry car loads, let some rainwater through the joints, and can be repaired block by block. A concrete slab cracks across and has to be broken out to repair. Kota stone and ceramic or vitrified tiles suit covered porches with foot traffic; on an open driveway they get slippery in the rain and crack under wheels.",
       howto=False,
       table=("Side by side", ["", "Paver blocks", "Concrete slab", "Kota stone", "Ceramic / vitrified tiles"],
              [["Takes car loads", "Yes (60–80 mm)", "Yes, if reinforced", "Thin slabs crack", "Not made for cars"],
               ["Grip when wet", "Good; anti-skid face available", "Good if brushed", "Slippery when polished", "Slippery"],
               ["Rainwater", "Some drains through joints", "Runs off", "Runs off", "Runs off"],
               ["Cracks", "Joints take up movement", "Cracks across the slab", "Slabs crack", "Tiles crack and come loose"],
               ["Repairs", "Lift and re-lay the same blocks", "Break out and re-cast", "Replace the slab", "Replace tiles; hard to match"],
               ["Ready for cars", "As soon as compacted and jointed", "After curing, a week or more", "After the mortar sets", "After the mortar sets"],
               ["Look", "Many shapes, colours, patterns", "Plain grey", "Natural stone", "Many designs"]]),
       steps=[("When paver blocks are the right choice", "Anywhere cars drive, where pipes or cables run underneath, and where monsoon rain stands on the surface. Pavers also let you change the look later by re-laying in a new pattern."),
              ("When a concrete slab makes sense", "For a narrow utility strip or a trolley ramp where a perfectly smooth surface matters. Build it reinforced, with expansion joints, and cure it properly before use."),
              ("Kota stone and tiles", "Kota stone with a rough finish suits verandahs, steps and covered porches. Ceramic and vitrified tiles belong indoors and on covered porches; on an open driveway they get slippery in rain and crack under car wheels."),
              ("A mixed design works well", "Many Bhopal homes pave the driveway in 80 mm zig-zag or rectangular blocks, use paver tiles or Kota stone on the covered porch, and finish the edges with kerb stones.")],
       faqs=[("Are paver blocks cheaper than a concrete driveway?", "The first cost is often similar. Over the years pavers usually cost less, because a damaged patch is lifted and re-laid instead of breaking out the slab."),
             ("Can I use tiles on my driveway?", "Not on an open driveway that cars use. Tiles are slippery when wet and crack under wheels. Use 300 × 300 mm concrete paver tiles or Kota stone on a covered porch instead.")]),
]
def guide_table(t):
    cap, heads, rows = t
    th = "".join(f'<th scope="col">{e(h)}</th>' for h in heads)
    body = "".join("<tr>" + "".join(f'<th scope="row">{e(c)}</th>' if i == 0 else f"<td>{e(c)}</td>" for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<h2 class="h2" style="margin-top:40px">{e(cap)}</h2><div class="tbl" style="margin-top:14px"><table class="spec"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'

def build_guide(g, hi=False):
    root = "../../../" if hi else "../../"
    G = dict(g, **g["hi"]) if hi else g
    url = ("hi/" if hi else "") + g["slug"] + "/"
    steps = "".join(f'<li><h2 class="h2" style="font-size:1.5rem">{e(h)}</h2><p>{e(t)}</p></li>' for h, t in G["steps"])
    faqs = G.get("faqs", [])
    graph = [org_schema(), crumbs([("Home", ""), (G["h1"], url)]),
             {"@type": "Article", "headline": G["h1"], "description": G["desc"], "inLanguage": "hi-IN" if hi else "en-IN", "dateModified": TODAY,
              "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID}, "mainEntityOfPage": SITE_URL + url}]
    if g["howto"]:
        graph.append({"@type": "HowTo", "name": G["h1"], "description": G["answer"], "step": [{"@type": "HowToStep", "position": i + 1, "name": h, "text": t} for i, (h, t) in enumerate(G["steps"])]})
    if faqs: graph.append(faq_schema(faqs))
    table = guide_table(g["table"]) if g.get("table") and not hi else ""
    faq = f'<h2 class="h2" style="margin-top:48px">{"सवाल-जवाब" if hi else "Questions"}</h2><div class="faq" style="margin-top:16px;display:block">{faq_html(faqs)}</div>' if faqs else ""
    others = " · ".join(f'<a class="link" href="{root}{x["slug"]}/">{e(x["h1"])}</a>' for x in GUIDES if x is not g)
    if hi:
        more = f'<p style="margin-top:32px">और पढ़ें: <a class="link" href="{root}hi/">भोपाल में पेवर ब्लॉक</a> · <a class="link" href="{root}hi/products/">सभी ब्लॉक</a> · <a class="link" href="{root}{g["slug"]}/" lang="en">Read in English</a></p>'
    else:
        uses = " · ".join(f'<a class="link" href="{root}uses/{u["slug"]}/">{e(u["short"])}</a>' for u in USES)
        more = f'<p style="margin-top:32px">Not sure which thickness you need? See the <a class="link" href="{root}#load">load guide</a>.</p><p style="margin-top:12px">Pavers by use: {uses}</p><p style="margin-top:12px">More guides: {others}</p>'
    tail = (f'<div style="margin-top:40px" id="enquiry">{enquiry_form(root, hi=hi)}</div>' if g.get("enquiry") else
            f'<div class="row2" style="margin-top:24px"><a class="btn btn-primary" href="{root}contact/">Send enquiry</a><a class="link" href="{root}products/">See all 14 ranges</a></div>')
    main = f'''<main id="main"><section><div class="wrap" style="max-width:820px">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{root}{"hi/" if hi else ""}">{"होम" if hi else "Home"}</a> / <span>{e(G["h1"])}</span></nav>
  <div class="label">{"गाइड" if hi else "Guide"}</div>
  <h1 class="h1">{e(G["h1"])}</h1>
  <p class="answer">{e(G["answer"])}</p>
  {table}
  <ol class="guide-steps">{steps}</ol>
  {faq}
  {more}
  {tail}
</div></section></main>
'''
    write(url + "index.html", head(root, url, G["title"], G["desc"], schema=ld(graph), lang="hi" if hi else "en") + header(root) + main + footer(root))

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
    trust = projects_strip("") + (f'<section><div class="wrap">{reviews_html("")}</div></section>' if REVIEWS else "")
    body = body.replace("<!-- VISIT -->", trust + "\n  <!-- VISIT -->", 1)
    graph = [org_schema(), {"@type": "WebSite", "@id": SITE_URL + "#website", "name": BRAND, "url": SITE_URL, "publisher": {"@id": ORG_ID}, "inLanguage": "en-IN"}] + [loc_schema(l) for l in LOCATIONS] + [faq_schema(FAQ),
             {"@type": "ItemList", "name": "Satyam Pavers products", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE_URL + "products/" + p["slug"] + "/", "name": p["full"]} for i, p in enumerate(PRODUCTS)]}]
    page = head("", "", "Paver Block Manufacturer in Bhopal & Mandideep | Satyam Pavers",
                "Concrete paver blocks, interlocking tiles and kerb stones made in Mandideep for Bhopal. 14 ranges, 60–100 mm. Design your floor online and send an enquiry.",
                schema=ld(graph), extra='<link rel="preload" as="image" href="assets/img/scenes/hero.webp" fetchpriority="high">\n')
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
  <p class="answer">{BRAND} makes 14 ranges of concrete paving at its Mandideep factory near Bhopal: interlocking paver blocks (zig-zag, I-shape, rectangular, square, diamond, cosmic, Combo 5), decorative finishes (slate, anti-skid, cobble, speckled, hexagon 3D tiles), concrete paver tiles and kerb stones, in 60, 80 and 100 mm for foot traffic up to heavy vehicles.</p></div></div>
  <div class="products">{cards}</div>
  <h2 class="h2" style="margin-top:64px">Size and thickness at a glance</h2>
  <div class="tbl" style="margin-top:16px"><table class="spec"><thead><tr><th>Product</th><th>Size</th><th>Thickness</th><th>Load</th></tr></thead><tbody>{rows}</tbody></table></div>
  <p class="note" style="margin-top:8px">Typical values. Confirm the exact size and thickness for your order with our team.</p>
</div></section></main>
'''
    write("products/index.html", head(root, "products/", "Paver Block Types & Sizes | Interlocking Tiles, Kerb Stones — Satyam Pavers",
          "All 14 Satyam Pavers ranges: zig-zag, I-shape, rectangular, square, diamond, cosmic, hexagon, slate, anti-skid, cobble, paver tiles and kerb stones. Sizes, thickness and uses.", schema=ld(graph)) + header(root) + main + footer(root))

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
    ul = uses_for(p["id"])
    uses_links = ('<p class="note" style="margin-top:10px">Used for: ' + " · ".join(f'<a href="{root}uses/{u["slug"]}/">{e(u["short"])}</a>' for u in ul) + '</p>') if ul else ""
    hi_link = f' · <a href="{root}hi/products/{p["slug"]}/" lang="hi">हिंदी में पढ़ें</a>' if p["id"] in HI_PRODUCTS else ""
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
      <p class="note" style="margin-top:14px">Not sure about thickness? See the <a href="{root}#load">load guide</a>.</p>
      {uses_links}
      <p class="note" style="margin-top:10px">Pricing: <a href="{root}guides/paver-block-price-bhopal/">what decides the price of paver blocks</a>{hi_link}</p>
      <div style="margin-top:20px">{callback_form(p["full"])}</div></div>
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

# ---------- trust blocks: render only when real data has been filled in at the top of this file ----------
def uses_block(root):
    links = "".join(f'<li><a class="link" href="{root}uses/{u["slug"]}/">{e(u["h1"])}</a></li>' for u in USES)
    return f'<h2 class="h2" style="margin-top:40px">Pavers by use</h2><ul class="asklist" style="margin-top:14px">{links}</ul>'

def reviews_html(root, hi=False):
    if not REVIEWS: return ""
    items = "".join(f'<figure class="review"><div class="stars" aria-label="{r.get("rating", 5)} out of 5">{"★" * int(r.get("rating", 5))}</div><blockquote>{e(r["text"])}</blockquote>'
                    f'<figcaption><b>{e(r["name"])}</b> · {e(r["place"])}</figcaption></figure>' for r in REVIEWS)
    more = f'<a class="link" href="{e(GBP_REVIEW_URL)}" target="_blank" rel="noopener">{"Google पर रिव्यू लिखें" if hi else "Review us on Google"}</a>' if GBP_REVIEW_URL else ""
    return f'''<section class="reviews" style="margin-top:56px"><div class="label">{"ग्राहकों की राय" if hi else "Reviews from Google"}</div>
  <h2 class="h2">{"ग्राहक क्या कहते हैं" if hi else "What customers say"}</h2><div class="review-grid">{items}</div><p style="margin-top:14px">{more}</p></section>'''

def project_card(pr, root):
    p = P(pr["product"])
    img = f'<img src="{root}{pr["photo"]}" alt="{e(p["name"])} paver blocks at {e(pr["site"])}, {e(pr["place"])}" loading="lazy" width="1200" height="900">' if pr.get("photo") else ""
    facts = " · ".join(x for x in [f'{pr["sqft"]:,} sq ft' if pr.get("sqft") else "", str(pr["year"]) if pr.get("year") else ""] if x)
    return (f'<article class="project">{img}<div class="project-body"><div class="label">{e(pr["place"])}</div><h3>{e(pr["site"])}</h3>'
            f'<p><a href="{root}products/{p["slug"]}/">{e(p["full"])}</a>{" · " + e(pr["note"]) if pr.get("note") else ""}</p><p class="note">{facts}</p></div></article>')

def projects_strip(root):
    if not PROJECTS: return ""
    return f'''<section id="projects"><div class="wrap"><div class="head"><div><div class="label">Projects</div><h2>Sites we have supplied</h2></div></div>
  <div class="project-grid">{"".join(project_card(pr, root) for pr in PROJECTS[:3])}</div>
  <p style="margin-top:20px"><a class="link" href="{root}projects/">See all projects</a></p></div></section>'''

def build_projects():
    if not PROJECTS: return
    root = "../"
    graph = [org_schema(), crumbs([("Home", ""), ("Projects", "projects/")]), {"@type": "CollectionPage", "name": "Satyam Pavers projects", "url": SITE_URL + "projects/", "about": {"@id": ORG_ID}}]
    main = f'''<main id="main"><section><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a> / <span>Projects</span></nav>
  <div class="label">Projects</div><h1 class="h1">Paver projects in Bhopal and nearby</h1>
  <p class="answer">Driveways, colony roads, car parks and yards paved with {BRAND} blocks, made at our Mandideep factory.</p>
  <div class="project-grid" style="margin-top:28px">{"".join(project_card(pr, root) for pr in PROJECTS)}</div>
  {reviews_html(root)}
</div></section></main>
'''
    write("projects/index.html", head(root, "projects/", "Paver Block Projects in Bhopal | Satyam Pavers", "Driveways, colony roads, car parks and factory yards in Bhopal and nearby paved with Satyam Pavers blocks from our Mandideep factory.", schema=ld(graph)) + header(root) + main + footer(root))

# ---------- Hindi pages (real pages Google can index; the JS toggle only translates the shared labels) ----------
HI_NAMES = {"rectangular": "रेक्टैंगुलर पेवर ब्लॉक", "zigzag": "ज़िग-ज़ैग (यूनी) पेवर ब्लॉक", "ishape": "आई-शेप (बेहटन) पेवर ब्लॉक", "square": "स्क्वेयर पेवर ब्लॉक",
            "combo5": "कॉम्बो 5 सीरीज़ पेवर सेट", "diamond": "डायमंड पेवर ब्लॉक", "cosmic": "कॉस्मिक पेवर ब्लॉक", "hexagon": "हेक्सागन 3D पेवर टाइल्स",
            "slate": "स्लेट फ़िनिश पेवर स्लैब", "antiskid": "एंटी-स्किड पेवर ब्लॉक", "cobble": "कोबल स्टोन पेवर", "speckled": "स्पेकल्ड फ़िनिश पेवर ब्लॉक",
            "curved": "कंक्रीट कर्ब स्टोन", "tiles": "कंक्रीट पेवर टाइल्स"}
HI_LOAD = {"Foot to heavy": "पैदल से भारी वाहन तक", "Cars to heavy": "कार से भारी वाहन तक", "Cars to very heavy": "कार से बहुत भारी वाहन तक",
           "Foot to light": "पैदल से हल्के वाहन तक", "Foot traffic": "पैदल आवाजाही", "Edging": "किनारे के लिए"}
HI_COLOURS = {"grey": "ग्रे", "red": "लाल", "yellow": "पीला", "orange": "नारंगी", "black": "काला", "brown": "भूरा", "beige": "बेज"}
HI_COPY = {
  "zigzag": dict(full="ज़िग-ज़ैग (यूनी) इंटरलॉकिंग पेवर ब्लॉक",
       answer="ज़िग-ज़ैग पेवर ब्लॉक, जिन्हें यूनी पेवर भी कहते हैं, 225 × 112 mm के इंटरलॉकिंग कंक्रीट ब्लॉक हैं जिनके लहरदार किनारे चारों ओर से अगले ब्लॉक में फँस जाते हैं। ये 60, 80 और 100 mm मोटाई में और ग्रे, लाल, काले, भूरे व पीले रंग में बनते हैं। एक वर्ग फ़ुट में लगभग 3.9 ब्लॉक लगते हैं।",
       desc="भोपाल में सबसे ज़्यादा लगने वाला ब्लॉक। ब्रेक लगाने और गाड़ी मोड़ने पर भी फ़र्श अपनी जगह टिका रहता है, इसलिए ड्राइववे, पार्किंग और पेट्रोल पंप के लिए यही पहली पसंद है।",
       best=["घर के ड्राइववे और सोसाइटी की सड़कें", "पेट्रोल पंप और पार्किंग", "इंडस्ट्रियल यार्ड और सड़कें (100 mm)"]),
  "ishape": dict(full="आई-शेप (बेहटन / डंबल) पेवर ब्लॉक",
       answer="आई-शेप पेवर ब्लॉक, जिन्हें बेहटन या डंबल पेवर भी कहते हैं, 200 × 165 mm के इंटरलॉकिंग ब्लॉक हैं जो गाड़ियों का भार पूरे फ़र्श पर फैला देते हैं। 80 और 100 mm के ब्लॉक ट्रक यार्ड, बस स्टैंड और गोदामों के लिए हैं; 60 mm घर के ड्राइववे के लिए। एक वर्ग फ़ुट में लगभग 3.6 ब्लॉक लगते हैं।",
       desc="साइट पर इसे बेहटन या डंबल ब्लॉक कहते हैं। चारों तरफ़ से जुड़कर यह सोसाइटी की सड़कों से लेकर ट्रक यार्ड तक भार बाँट देता है।",
       best=["सोसाइटी की अंदरूनी सड़कें और फ़ुटपाथ", "कमर्शियल वॉकवे और पार्किंग", "ट्रक यार्ड और गोदाम (100 mm)"]),
  "rectangular": dict(full="रेक्टैंगुलर पेवर ब्लॉक",
       answer="रेक्टैंगुलर पेवर ब्लॉक 200 × 100 mm के कंक्रीट ब्लॉक हैं, जो 60, 80 और 100 mm मोटाई में बनते हैं। हेरिंगबोन पैटर्न में बिछाने पर ये मुड़ती गाड़ियों का भार झेलते हैं; रनिंग बॉन्ड या बास्केट वीव में ये रास्तों और आँगन के लिए अच्छे हैं। एक वर्ग फ़ुट में लगभग 4.6 ब्लॉक लगते हैं।",
       desc="सादा और हर काम का ब्लॉक। ड्राइववे के लिए हेरिंगबोन, रास्तों के लिए रनिंग बॉन्ड और आँगन के लिए बास्केट वीव।",
       best=["घर के ड्राइववे और पोर्च", "कॉलोनी की सड़कें और कार पार्क", "फैक्ट्री यार्ड (100 mm)"]),
  "curved": dict(full="कंक्रीट कर्ब स्टोन",
       answer="कंक्रीट कर्ब स्टोन सड़क, ड्राइववे, पार्किंग, डिवाइडर और गार्डन बेड के किनारे लगते हैं और पेवर ब्लॉक को अपनी जगह थामे रखते हैं। ये सीधे और घुमावदार दोनों प्रोफ़ाइल में बनते हैं और रनिंग फ़ुट के हिसाब से दिए जाते हैं।",
       desc="कर्ब के बिना किनारे के ब्लॉक गाड़ियों के दबाव से बाहर खिसकने लगते हैं। हर सड़क और ड्राइववे के खुले किनारे पर कर्ब लगाएँ।",
       best=["सड़क और कॉलोनी के किनारे", "ड्राइववे और पार्किंग के किनारे", "गोल चक्कर, डिवाइडर और गार्डन बेड"]),
}
HI_DELIVERY = "हाँ। मंडीदीप फैक्ट्री से भोपाल, ओबेदुल्लागंज, रायसेन, सीहोर, विदिशा, नर्मदापुरम और इंदौर तक ट्रक से डिलीवरी होती है। डिलीवरी की तारीख़ ऑर्डर के साथ तय होती है।"
def hi_size(p): return {"On request": "पूछें", "Set of 5 blocks": "5 ब्लॉक का सेट"}.get(p["size"], p["size"])
def hi_thick(p): return " / ".join(map(str, p["thick"])) + " mm" if p["thick"] else "पूछें"
def hi_href(p, root): return f'{root}hi/products/{p["slug"]}/' if p["id"] in HI_PRODUCTS else f'{root}products/{p["slug"]}/'

def hi_card(p, root):
    src, _, cap = view_of(p, p["c"], root, card=True)
    href = hi_href(p, root)
    return (f'<article class="p"><a class="ph" href="{href}" aria-label="{e(HI_NAMES[p["id"]])}"><img src="{src}" alt="{e(HI_NAMES[p["id"]])}" loading="lazy" width="800" height="1000"></a>'
            f'<div class="row"><h3><a href="{href}" style="text-decoration:none">{e(HI_NAMES[p["id"]])}</a></h3></div>'
            f'<div class="sub">{e(HI_LOAD[p["load"]])} · {e(hi_thick(p))}</div></article>')

def hi_product_faq(p):
    out = []
    if p["thick"]:
        out.append((f'{HI_NAMES[p["id"]]} की कितनी मोटाई चाहिए?', f'ये {hi_thick(p)} मोटाई में बनते हैं। पैदल रास्तों के लिए सबसे पतला, कारों के लिए बीच वाला, और ट्रक या फ़ोर्कलिफ़्ट के लिए {p["thick"][-1]} mm लें। आपकी साइट के लिए सही ग्रेड हमारी टीम बताएगी।'))
    if p.get("per"):
        out.append(("कितने ब्लॉक लगेंगे?", f'एक वर्ग फ़ुट में लगभग {p["per"]} ब्लॉक, और किनारों की कटाई के लिए लगभग 5% ज़्यादा। 1,000 वर्ग फ़ुट के लिए लगभग {round(1000 * 1.05 * p["per"]):,} ब्लॉक।'))
    out.append(("रेट कैसे पता करें?", "अपना एरिया (वर्ग फ़ुट), मोटाई, रंग और साइट की जगह भेजें। हमारी टीम उसी कामकाजी दिन फैक्ट्री-डायरेक्ट रेट भेजती है।"))
    out.append(("क्या आप मेरी साइट तक डिलीवरी करते हैं?", HI_DELIVERY))
    return out

def build_hi_product(p):
    root = "../../../"
    H = HI_COPY[p["id"]]
    url = f'hi/products/{p["slug"]}/'
    ims = images_of(p)
    src, cap = ((root + f'assets/img/{ims[0]["f"]}.webp', ims[0]["cap"]) if ims else (root + f'assets/img/laid/{p["id"]}-{p["c"]}.webp', p["full"]))
    spec = [("आकार", hi_size(p)), ("मोटाई", hi_thick(p)), ("कवरेज", f'लगभग {p["per"]} ब्लॉक प्रति वर्ग फ़ुट' if p.get("per") else ("रनिंग फ़ुट के हिसाब से" if p["id"] == "curved" else "पूछें")),
            ("भार", HI_LOAD[p["load"]]), ("रंग", ", ".join(HI_COLOURS[c] for c in colours_of(p))), ("कहाँ बनता है", "हमारी मंडीदीप फैक्ट्री, भोपाल के पास")]
    rows = "".join(f'<tr><th scope="row">{k}</th><td>{e(v)}</td></tr>' for k, v in spec)
    best = "".join(f"<li>{e(b)}</li>" for b in H["best"])
    faqs = hi_product_faq(p)
    rel = "".join(hi_card(P(i), root) for i in HI_PRODUCTS if i != p["id"])
    wa = e(wa_link(f'Hello Satyam Pavers, I would like to enquire about {p["full"]}.'))
    graph = [org_schema(), crumbs([("होम", "hi/"), ("उत्पाद", "hi/products/"), (H["full"], url)]),
             {"@type": "Product", "name": H["full"], "alternateName": p["full"], "description": H["answer"], "sku": "SP-" + p["code"], "image": SITE_URL + src[len(root):],
              "brand": {"@type": "Brand", "name": BRAND}, "manufacturer": {"@id": ORG_ID}, "category": "Concrete paving", "material": "Concrete", "inLanguage": "hi-IN"},
             faq_schema(faqs)]
    main = f'''<main id="main"><section><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{root}hi/">होम</a> / <a href="{root}hi/products/">उत्पाद</a> / <span>{e(H["full"])}</span></nav>
  <div class="prod">
    <figure class="gal"><img src="{src}" alt="{e(H["full"])}" width="1100" height="825" fetchpriority="high"></figure>
    <div class="prod-info">
      <div class="label">सत्यम पेवर्स · मंडीदीप में निर्मित</div>
      <h1 class="h1">{e(H["full"])}</h1>
      <p class="answer">{e(H["answer"])}</p>
      <p>{e(H["desc"])}</p>
      <div class="row2"><a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener"><svg><use href="#wa"/></svg>WhatsApp पर पूछें</a><a class="link" href="{root}products/{p["slug"]}/" lang="en">Read in English</a></div>
    </div>
  </div>
  <div class="prod-cols">
    <div><h2 class="h2">स्पेसिफ़िकेशन</h2><div class="tbl" style="margin-top:14px"><table class="spec"><tbody>{rows}</tbody></table></div>
      <p class="note" style="margin-top:8px">ये सामान्य माप हैं। अपने ऑर्डर का सही साइज़, ग्रेड और स्टॉक हमारी टीम से पक्का करें।</p></div>
    <div><h2 class="h2">कहाँ सबसे अच्छा</h2><ul class="asklist" style="margin-top:14px">{best}</ul>
      <p class="note" style="margin-top:14px">रेट किन बातों पर तय होता है, पढ़ें: <a href="{root}hi/guides/paver-block-price-bhopal/">भोपाल में पेवर ब्लॉक का रेट</a></p></div>
  </div>
  <div class="prod-cols" style="margin-top:56px" id="enquiry">
    <div>{enquiry_form(root, product=p["full"], hi=True)}</div>
    <div><h2 class="h2">सवाल-जवाब</h2><div class="faq" style="margin-top:16px;display:block">{faq_html(faqs)}</div>
      <div style="margin-top:24px">{callback_form(p["full"], hi=True)}</div></div>
  </div>
  <h2 class="h2" style="margin-top:56px">और ब्लॉक</h2>
  <div class="products" style="margin-top:20px">{rel}</div>
</div></section></main>
'''
    title = f'{H["full"]} भोपाल | साइज़, मोटाई और रंग — सत्यम पेवर्स'
    desc = f'{H["full"]}: {hi_size(p)}, {hi_thick(p)}। मंडीदीप फैक्ट्री में बने, भोपाल और आसपास डिलीवरी। रेट के लिए आज ही पूछताछ भेजें।'
    write(url + "index.html", head(root, url, title, desc, img=src[len(root):], schema=ld(graph), lang="hi") + header(root) + main + footer(root))

def build_hi_products():
    root = "../../"
    rows = "".join(f'<tr><td><a href="{hi_href(p, root)}">{e(HI_NAMES[p["id"]])}</a></td><td class="mono">{e(hi_size(p))}</td><td class="mono">{e(hi_thick(p))}</td><td>{e(HI_LOAD[p["load"]])}</td></tr>' for p in PRODUCTS)
    cards = "".join(hi_card(P(i), root) for i in HI_PRODUCTS)
    graph = [org_schema(), crumbs([("होम", "hi/"), ("उत्पाद", "hi/products/")]),
             {"@type": "CollectionPage", "name": "पेवर ब्लॉक, टाइल्स और कर्ब स्टोन", "url": SITE_URL + "hi/products/", "inLanguage": "hi-IN", "about": {"@id": ORG_ID}}]
    main = f'''<main id="main"><section><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{root}hi/">होम</a> / <span>उत्पाद</span></nav>
  <div class="label">कैटलॉग</div><h1 class="h1">पेवर ब्लॉक, टाइल्स और कर्ब स्टोन</h1>
  <p class="answer">सत्यम पेवर्स अपनी मंडीदीप फैक्ट्री में कंक्रीट पेविंग की 14 रेंज बनाता है: इंटरलॉकिंग पेवर ब्लॉक (ज़िग-ज़ैग, आई-शेप, रेक्टैंगुलर, स्क्वेयर, डायमंड, कॉस्मिक, कॉम्बो 5), डिज़ाइनर फ़िनिश (स्लेट, एंटी-स्किड, कोबल, स्पेकल्ड, हेक्सागन 3D टाइल्स), पेवर टाइल्स और कर्ब स्टोन — 60, 80 और 100 mm में, पैदल रास्तों से लेकर भारी वाहनों तक।</p>
  <h2 class="h2" style="margin-top:40px">सबसे ज़्यादा माँगे जाने वाले</h2>
  <div class="products" style="margin-top:20px">{cards}</div>
  <h2 class="h2" style="margin-top:56px">सभी 14 रेंज: साइज़ और मोटाई</h2>
  <div class="tbl" style="margin-top:16px"><table class="spec"><thead><tr><th>ब्लॉक</th><th>साइज़</th><th>मोटाई</th><th>भार</th></tr></thead><tbody>{rows}</tbody></table></div>
  <p class="note" style="margin-top:8px">ये सामान्य माप हैं। ऑर्डर का सही साइज़ और मोटाई हमारी टीम से पक्का करें। <a href="{root}products/" lang="en">English catalogue</a></p>
  <div class="prod-cols" style="margin-top:56px"><div>{enquiry_form(root, hi=True)}</div>
    <div><h2 class="h2">रेट जानना है?</h2><p style="margin-top:10px">पढ़ें <a class="link" href="{root}hi/guides/paver-block-price-bhopal/">भोपाल में पेवर ब्लॉक का रेट किन बातों पर तय होता है</a>, या सीधे फ़ॉर्म भरें।</p>
      <p style="margin-top:14px">कॉल करें: <a class="num" href="tel:{CONTACT["tel"]}"><b>{CONTACT["display"]}</b></a></p></div></div>
</div></section></main>
'''
    write("hi/products/index.html", head(root, "hi/products/", "पेवर ब्लॉक के प्रकार और साइज़ | इंटरलॉकिंग टाइल्स, कर्ब स्टोन — सत्यम पेवर्स",
          "सत्यम पेवर्स की सभी 14 रेंज: ज़िग-ज़ैग, आई-शेप, रेक्टैंगुलर, स्क्वेयर, डायमंड, कॉस्मिक, हेक्सागन, स्लेट, एंटी-स्किड, कोबल, पेवर टाइल्स और कर्ब स्टोन। साइज़, मोटाई और उपयोग।",
          schema=ld(graph), lang="hi") + header(root) + main + footer(root))

HI_BHOPAL_FAQ = [
  ("भोपाल में पेवर ब्लॉक का रेट क्या है?", "रेट मोटाई, आकार, रंग, मात्रा और साइट की दूरी पर निर्भर करता है, इसलिए हम हर ऑर्डर के लिए अलग रेट देते हैं। एरिया, ब्लॉक, मोटाई, रंग और साइट की जगह भेजिए — उसी कामकाजी दिन जवाब मिलेगा।"),
  ("एक वर्ग फ़ुट में कितने पेवर ब्लॉक लगते हैं?", "लगभग 4.6 रेक्टैंगुलर, 3.9 ज़िग-ज़ैग, 3.6 आई-शेप या 2.3 स्क्वेयर ब्लॉक। किनारों की कटाई के लिए लगभग 5% ज़्यादा जोड़ें।"),
  ("कार के ड्राइववे के लिए कितनी मोटाई चाहिए?", "कभी-कभार कार वाले घर के ड्राइववे के लिए 60 mm काफ़ी है। रोज़ की कारों, एसयूवी और कॉलोनी की सड़कों के लिए 80 mm सुरक्षित है। ट्रक और फ़ोर्कलिफ़्ट के लिए 100 mm लें।"),
  ("क्या रंग फीका पड़ता है?", "रंग कंक्रीट में ही मिला होता है, ऊपर पेंट नहीं होता, इसलिए पूरे ब्लॉक में रहता है। धूप में सालों बाद हर कंक्रीट पेवर थोड़ा हल्का होता है; साल में एक-दो बार धोने से चमक बनी रहती है।"),
  ("क्या भोपाल के बाहर डिलीवरी होती है?", HI_DELIVERY),
  ("क्या ऑर्डर से पहले ब्लॉक देख सकते हैं?", "हाँ। एमपी नगर के बिक्री कार्यालय या मंडीदीप फैक्ट्री आइए। पहले पूछताछ भेज दें ताकि आपके पसंद के ब्लॉक के सैंपल तैयार रहें।"),
]
def build_hi_bhopal():
    root = "../"
    l = LOCATIONS[0]
    secs = [("कौन-सा ब्लॉक किस काम का", None),
            ("कितनी मोटाई चाहिए", "60 mm: पैदल रास्ते, बगीचे, छत और हल्के ड्राइववे। 80 mm: रोज़ की कारें, एसयूवी, कॉलोनी की सड़कें और पार्किंग। 100 mm: ट्रक, बस, पेट्रोल पंप, फैक्ट्री यार्ड और फ़ोर्कलिफ़्ट। ब्लॉक के नीचे दबाकर बनाया गया गिट्टी का बेस उतना ही ज़रूरी है जितनी मोटाई।"),
            ("भोपाल में कहाँ-कहाँ डिलीवरी", "पूरे शहर में — कोलार रोड, नर्मदापुरम रोड, अयोध्या बायपास, बावड़िया कलाँ, मिसरोद, कटारा हिल्स, बैरागढ़, गोविंदपुरा, अवधपुरी, शाहपुरा, अरेरा कॉलोनी और पुराना शहर। बड़े ऑर्डर फैक्ट्री से सीधे ट्रक द्वारा आपकी साइट पर जाते हैं।"),
            ("फैक्ट्री से सीधे क्यों", "बीच में कोई डीलर नहीं, एक ही बैच के मिलते-जुलते रंग, और मंडीदीप फैक्ट्री से लोड हुए ट्रक सीधे आपकी साइट तक। बिल्डरों के लिए साइट के शेड्यूल के हिसाब से चरणों में सप्लाई।")]
    picks = [("zigzag", "ड्राइववे, पार्किंग और पेट्रोल पंप"), ("ishape", "सोसाइटी की सड़कें, फ़ुटपाथ और ट्रक यार्ड"), ("rectangular", "पोर्च, आँगन और हेरिंगबोन ड्राइववे"), ("curved", "सड़क, ड्राइववे और गार्डन के किनारे")]
    pick_list = "".join(f'<li><a class="link" href="{hi_href(P(i), root)}">{e(HI_NAMES[i])}</a> — {e(t)}</li>' for i, t in picks)
    body = "".join(f'<h2 class="h2" style="margin-top:40px">{e(h)}</h2>' + (f'<ul class="asklist" style="margin-top:14px">{pick_list}</ul>' if t is None else f'<p style="margin-top:10px;max-width:68ch">{e(t)}</p>') for h, t in secs)
    cards = "".join(hi_card(P(i), root) for i in HI_PRODUCTS[:3])
    graph = [org_schema(), loc_schema(l),
             crumbs([("होम", "hi/")]), faq_schema(HI_BHOPAL_FAQ),
             {"@type": "WebPage", "url": SITE_URL + "hi/", "name": "भोपाल में पेवर ब्लॉक", "inLanguage": "hi-IN", "about": {"@id": SITE_URL + l["slug"] + "/#place"}}]
    main = f'''<main id="main"><section><div class="wrap">
  <div class="prod">
    <div class="prod-info" style="padding:0">
      <div class="label">सत्यम पेवर्स · मंडीदीप में निर्मित</div>
      <h1 class="h1">भोपाल में पेवर ब्लॉक</h1>
      <p class="answer">सत्यम पेवर्स इंटरलॉकिंग पेवर ब्लॉक, पेवर टाइल्स और कर्ब स्टोन अपनी मंडीदीप फैक्ट्री में बनाता है और भोपाल में कहीं भी सीधे आपकी साइट तक पहुँचाता है। हमारा बिक्री कार्यालय कान्हा बिल्डिंग, प्लॉट नं. 190, ज़ोन-II, एमपी नगर में होटल कान्हा और सरगम सिनेमा के पास है।</p>
      <address class="addr"><b>बिक्री कार्यालय</b><br>कान्हा बिल्डिंग, प्लॉट नं. 190, होटल कान्हा के पास, सरगम सिनेमा के पास, ज़ोन-II, महाराणा प्रताप नगर, भोपाल, मध्य प्रदेश {l["pin"]}<br>मोबाइल: <a href="tel:{CONTACT["tel"]}">{CONTACT["display"]}</a></address>
      <div class="row2"><a class="btn btn-primary" href="#enquiry">पूछताछ भेजें</a><a class="btn btn-ink" href="{maps_link(l)}" target="_blank" rel="noopener">रास्ता देखें</a><a class="link" href="{root}paver-blocks-bhopal/" lang="en">Read in English</a></div>
    </div>
    <iframe class="map" title="नक्शा: सत्यम पेवर्स, एमपी नगर" src="{maps_embed(l)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div>
  {body}
  <h2 class="h2" style="margin-top:56px">लोकप्रिय ब्लॉक</h2>
  <div class="products" style="margin-top:20px">{cards}</div>
  <p style="margin-top:20px"><a class="link" href="{root}hi/products/">सभी 14 रेंज देखें</a> · <a class="link" href="{root}hi/guides/paver-block-price-bhopal/">रेट किन बातों पर तय होता है</a></p>
  {reviews_html(root, hi=True)}
  <div class="prod-cols" style="margin-top:56px" id="enquiry">
    <div>{enquiry_form(root, city="भोपाल", hi=True)}</div>
    <div><h2 class="h2">सवाल-जवाब</h2><div class="faq" style="margin-top:16px;display:block">{faq_html(HI_BHOPAL_FAQ)}</div>
      <div style="margin-top:24px">{callback_form("Paver blocks, Bhopal", hi=True)}</div></div>
  </div>
</div></section></main>
'''
    write("hi/index.html", head(root, "hi/", "भोपाल में पेवर ब्लॉक | इंटरलॉकिंग टाइल्स और कर्ब स्टोन — सत्यम पेवर्स",
          "भोपाल में पेवर ब्लॉक, इंटरलॉकिंग टाइल्स और कर्ब स्टोन। मंडीदीप की अपनी फैक्ट्री में बने, एमपी नगर बिक्री कार्यालय से। रेट के लिए आज ही पूछताछ भेजें।",
          img="assets/img/onsite/society-road.webp", schema=ld(graph), lang="hi") + header(root) + main + footer(root))

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
  {uses_block(root) if l["id"] == "office" else ""}
  {'<p style="margin-top:16px"><a class="link" href="../hi/" lang="hi">यह पेज हिंदी में पढ़ें →</a></p>' if l["id"] == "office" else ""}
  <figure class="scene"><img src="{root}assets/img/{c["img"] if "/" in c["img"] else "stock/" + c["img"]}.webp" alt="{e(c["img_alt"])}" loading="lazy" width="1200" height="900"></figure>
  {reviews_html(root) if l["id"] == "office" else ""}
  <h2 class="h2" style="margin-top:56px">Popular blocks</h2>
  <div class="products" style="margin-top:20px">{cards}</div>
  <div class="prod-cols" style="margin-top:56px">
    <div>{enquiry_form(root, city=l["city"])}</div>
    <div><h2 class="h2">Our other location</h2><div class="places">{place_html(other, root)}</div><p style="margin-top:20px"><a class="link" href="../products/">See all 14 product ranges</a></p></div>
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
    urls = ([("", "1.0"), ("products/", "0.9")] + [("products/" + p["slug"] + "/", "0.8") for p in PRODUCTS] + [(l["slug"] + "/", "0.9") for l in LOCATIONS]
            + [("uses/" + u["slug"] + "/", "0.8") for u in USES] + [(a["slug"] + "/", "0.7") for a in SERVICE_AREAS] + [(g["slug"] + "/", "0.7") for g in GUIDES]
            + [("tools/paver-calculator/", "0.7"), ("contact/", "0.7")] + ([("projects/", "0.8")] if PROJECTS else []) + [(v, "0.7") for v in HI_PAIRS.values()])
    def alts(u):
        en = next((k for k, v in HI_PAIRS.items() if v == u), u)
        if en not in HI_PAIRS: return ""
        return "".join(f'<xhtml:link rel="alternate" hreflang="{h}" href="{SITE_URL}{x}"/>' for h, x in (("en-IN", en), ("hi-IN", HI_PAIRS[en]), ("x-default", en)))
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "".join(f"  <url><loc>{SITE_URL}{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority>{alts(u)}</url>\n" for u, pr in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /src/\nAllow: /tools/paver-calculator/\nDisallow: /tools/\nDisallow: /docs/\nDisallow: /tests/\n\n# AI search crawlers are welcome\nUser-agent: OAI-SearchBot\nAllow: /\nUser-agent: Claude-SearchBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n")
    lines = [f"# {BRAND}", "", f"> {BRAND} ({LEGAL}) manufactures concrete paver blocks, interlocking tiles, paver tiles and kerb stones at its factory in Mandideep, Madhya Pradesh, and sells from a sales office in MP Nagar, Bhopal. It supplies shopping malls, schools and colleges, factories and warehouses, housing societies, petrol pumps and homes, and delivers across Bhopal, Raisen, Sehore, Vidisha, Narmadapuram and Indore. Prices are given on enquiry only.", "",
             "## Locations"] + [f"- [{l['role']}]({SITE_URL}{l['slug']}/): {addr_line(l)}" for l in LOCATIONS] + ["", "## Products"] + \
            [f"- [{p['full']}]({SITE_URL}products/{p['slug']}/): {p['answer']}" for p in PRODUCTS] + ["", "## Pavers by use"] + [f"- [{u['h1']}]({SITE_URL}uses/{u['slug']}/): {u['answer']}" for u in USES] + ["", "## Delivery areas"] + [f"- [Paver blocks in {a['name']}]({SITE_URL}{a['slug']}/): delivered from Mandideep, about {a['km']} km" for a in SERVICE_AREAS] + \
            ["", "## Guides"] + [f"- [{g['h1']}]({SITE_URL}{g['slug']}/): {g['answer']}" for g in GUIDES] + ["", f"- [Paver block calculator]({SITE_URL}tools/paver-calculator/): estimates block count from area, with 5% wastage.", "", "## Common questions"] + [f"- Q: {q}\n  A: {a}" for q, a in FAQ] + \
            ["", "## Hindi pages", f"- [भोपाल में पेवर ब्लॉक]({SITE_URL}hi/)", f"- [पेवर ब्लॉक के प्रकार]({SITE_URL}hi/products/)", f"- [भोपाल में पेवर ब्लॉक का रेट]({SITE_URL}hi/guides/paver-block-price-bhopal/)"] + \
            ["", "## Contact", f"- [Send an enquiry]({SITE_URL}contact/): enquiry form and WhatsApp, mobile {CONTACT['display']}", f"- {BRAND} is a brand of {LEGAL}.", ""]
    write("llms.txt", "\n".join(lines))
    write("site.webmanifest", json.dumps({"name": BRAND, "short_name": BRAND, "start_url": "./", "display": "standalone", "background_color": "#F2F1ED", "theme_color": "#151412",
                                          "icons": [{"src": "assets/brand/logo-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "assets/brand/logo-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=1))
    data = {"products": PRODUCTS, "photos": {p["id"]: images_of(p) for p in PRODUCTS}, "colours": {p["id"]: colours_of(p) for p in PRODUCTS}}
    write("assets/js/data.js", "/* generated by tools/build.py — edit the data there */\nwindow.SP_CONTACT = " + json.dumps(dict(CONTACT, email=EMAIL)) + ";\nwindow.SP_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n")

if __name__ == "__main__":
    import_generated(); build_home(); build_products_index()
    for i, p in enumerate(PRODUCTS): build_product(p, i)
    for l in LOCATIONS: build_location(l)
    for a in SERVICE_AREAS: build_area(a)
    for a in USES: build_use(a)
    for g in GUIDES:
        build_guide(g)
        if g.get("hi"): build_guide(g, hi=True)
    build_hi_bhopal(); build_hi_products()
    for i in HI_PRODUCTS: build_hi_product(P(i))
    build_projects(); build_calc()
    build_contact(); build_404(); build_meta()
    print("built", 6 + len(PRODUCTS) + len(SERVICE_AREAS) + len(USES) + len(GUIDES) + len(HI_PAIRS) + (1 if PROJECTS else 0), "pages")
