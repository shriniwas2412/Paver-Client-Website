# Gemini product images: reference, prompt, output

Use Gemini (gemini.google.com or Google AI Studio) with the image model.
For each row: start a **new chat**, attach the reference photo from `reference/gemini-refs/`, paste the prompt, download the result, rename it to the output name and put it in `assets/img/generated/`.

Paste this **style line** at the end of every prompt so all images match the 5 Canva ones:

> Clean professional catalogue product photo. Keep the exact same shape, proportions, edge profile, surface texture and colour as the block in the reference photo — do not invent a different design. Three-quarter view on a plain light warm-grey seamless studio background, soft natural daylight from the upper left, soft contact shadow, sharp focus, realistic concrete material. No text, no logo, no people, no other objects. Landscape 4:3.

| # | Reference photo | Prompt (then add the style line) | Save as |
|---|---|---|---|
| 1 | `hexagon-grey.jpg` | A single grey concrete hexagon paver tile with three grooved faces whose parallel grooves form a 3D cube illusion, lying almost flat, seen slightly from above. | `hexagon.png` |
| 2 | `slate-grey.jpg` | A grey concrete paver slab with a moulded natural-slate surface of soft ripples and veins, one slab lying flat with a second leaning behind it. | `slate.png` |
| 3 | `antiskid-stack.jpg` | A neat stack of three grey rectangular concrete anti-skid paver blocks with a fine leather-grain grip surface on top. | `antiskid.png` |
| 4 | `cobble-beige.jpg` | Three chunky beige concrete cobble stones with rough split-face sides and a slightly uneven top, grouped together. | `cobble.png` |
| 5 | `speckled-slab.jpg` | A grey concrete paver block with a smooth face scattered with small stone chips like terrazzo, one block lying flat. | `speckled.png` |
| 6 | `kerb-lineup.jpg` | A row of three grey concrete kerb stones of different heights standing side by side, showing their smooth faces and chamfered top edge. | `curved.png` |
| 7 | `tile-yellow.jpg` | A yellow 300 × 300 mm concrete paver tile with a moulded brick-weave pattern of grooves on its face, lying almost flat. | `tiles.png` |

Optional redo (Canva's version lost some texture):

| # | Reference photo | Prompt (then add the style line) | Save as |
|---|---|---|---|
| 8 | `ishape-red.jpg` | Two red I-shape (dumbbell) interlocking concrete paver blocks locked together, with the scattered dash-pattern grip texture on the top face clearly visible. | `ishape.png` |

Still needed (the site shows a "Photo coming soon" tile for Cosmic until this exists):

| # | Reference photo | Prompt (then add the style line) | Save as |
|---|---|---|---|
| 9 | `reference/photos/cosmic-red.webp` | Two red cosmic interlocking concrete paver blocks, each with curved wave-like edges, locked together, lying flat, seen slightly from above. | `cosmic.png` |

Optional: Zig-zag, rectangular and square currently use licensed stock photos. To replace them with your own product shots, use `zigzag-red.webp`, `rect-grey.webp` and `square-grey.webp` from `reference/photos/` and save as `zigzag.png`, `rectangular.png`, `square.png`.

Then run `python3 tools/build.py`.

## Tips
- If Gemini changes the shape, reply: *"Keep the block exactly as in my photo — same outline and texture. Only change the background and lighting."*
- If it adds text or extra objects, reply: *"Remove everything except the block."*
- Download the full-size image (not a screenshot).
- Raw photos are never published; the generated image is labelled "Product image" on the site.

## Better results: "laid on site" prompts (use these instead)
Single-block catalogue shots tend to look fake. Gemini is far better at **blocks already laid at a real site**, and these sell better too (it's what Basant Betons does). Attach the reference photo and paste:

> Photorealistic photo of a newly paved [AREA] in Bhopal, India, laid with [COLOUR] [BLOCK NAME] concrete paver blocks exactly like the block in the reference photo — same shape, joints and surface texture. Eye-level view, late-afternoon sun, crisp joints filled with sand, clean concrete kerb edge, a little greenery. No people, no text, no logos, no watermark. Landscape 16:10, high detail.

| Block | [AREA] | Save as |
|---|---|---|
| Cosmic (red + yellow) | driveway in front of a modern Indian house | `cosmic.png` |
| Zig-zag (grey with red bands) | housing-society internal road | `zigzag.png` |
| I-shape (grey) | factory loading yard with a parked truck | `ishape.png` |
| Rectangular herringbone (grey/red) | home porch and car parking | `rectangular.png` |
| Hexagon 3D tile | terrace of an apartment | `hexagon.png` |

If the shape comes out wrong, reply: *"Use exactly the block shape from my photo; change nothing about the block."*
