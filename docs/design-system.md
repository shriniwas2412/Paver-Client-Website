# Satyam Pavers design rules

Set with the ui-ux-pro-max design-system search ("construction materials manufacturer B2B premium", spacious density, subtle motion) and its trust-and-authority landing pattern: hero → proof (sectors and scale) → products → clear enquiry path.

## Layout
- Mobile first: design at 375px, then 768px and 1280px. Most visitors are on phones.
- Section rhythm: 96px vertical padding on desktop, 64px on phone. 16–20px side gutter. Container max 1240px.
- Section header: label (small caps), serif h2, lede at most 60ch.
- Home order: hero → trust bar → catalogue → sectors → large-projects band → applications → studio → load guide → desks → process → enquiry → visit → FAQ.

## Product cards
- Every range uses one rendered pattern tile from `assets/img/laid/<id>-<colour>.webp` (800×1000, same scale, light and seed), shown in a 4:5 frame.
- Card body: title row, two-line clamped subtitle, actions pinned to the bottom, so all cards align.
- Phone: 2-column grid, one Enquire action; Compare and Details are hidden (the whole tile opens the product).
- Photos (on-site, studio, stock) appear only on product pages, in fixed frames at capped sizes. They are never shown large.

## Type and colour
- Serif display (Fraunces) for headings, sans for body at 16–17px with a line height of 1.5–1.6.
- Dark basalt `--hero`, laterite accent for primary actions, marigold for labels on dark backgrounds. Body contrast is at least 4.5:1.

## Motion
- Reveal on scroll with a small offset; hover lift on cards for pointer devices only; everything off under `prefers-reduced-motion`.

## Content rules
- No prices, one phone number (+91 91711 10110), no invented client names, no raw factory photos.
