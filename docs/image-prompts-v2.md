# Image prompts v2: real-site photos for Satyam Pavers

Replaces the studio prompts in `gemini-prompts.md`. Gemini looks far more real with **blocks laid on a real site**, described as a photograph, with our real block photo attached.

## How to use

1. **One image per chat.** A new chat each time stops blocks bleeding over.
2. **Attach the listed reference photo first**, then paste the prompt.
3. **Aspect ratio:** 16:9 for `hero.png` and 4:3 for the rest. Also set the app's ratio picker if it has one.
4. **Iterate in the same chat**, one change per follow-up, ending with *"Keep everything else exactly the same."* After 3–4 failed tries, start fresh.
5. **Shape fidelity:** prompts spell out each outline in words. Keep the camera at standing height; steep close-ups warp patterns.
6. **Avoiding the AI look:** every prompt asks for sand joints, dust, slight shade variation, matte concrete, natural daylight, a normal lens and a believable Bhopal setting, with no text or faces.
7. Save full-size to `assets/img/generated/<name>`, then run `python3 tools/build.py`.

**Our blocks:** coloured blocks have a ~10 mm coloured top layer over a grey body, slight chamfers, and muted matte colours (brick-red, ochre-yellow, cement grey, charcoal).

---

## Prompts

### hero.png (16:9) — attach `reference/photos/zigzag-grey.webp` + `zigzag-red.webp`
> 35 mm photo of a freshly paved driveway in front of a two-storey house in a Bhopal residential colony, India. The paving is the zig-zag concrete block in the photos, a rectangle with two V-notches along each long side. Laid in interlocking rows, mostly cement grey with two bands of muted brick-red. Sand-filled joints, light dust, a faint tyre mark, slight shade variation. Behind are a plastered boundary wall, a black MS sliding gate and bougainvillea. Soft morning side light. Standing eye height. No text, no people. 16:9 landscape.

### cosmic.png — attach `reference/photos/cosmic-red.webp` + `cosmic-yellow.webp`
> 35 mm photo of a home driveway in Bhopal, India, paved with the cosmic concrete paver in the photos. It is a curved triangle with three concave sides and three rounded lobes. Face: raised diamond-knurled border around a field of small round dimples. The blocks interlock in rows, alternating muted brick-red and ochre-yellow, with grey sand in the joints, a little dust and a few faded blocks. A compound wall and gate show at the edge. Overcast daylight, standing height. No text or people. 4:3.

### zigzag.png — attach `reference/gemini-refs/zigzag-red.jpg`
> 35 mm photo of a car parking area in Bhopal paved with the zig-zag (uni) paver in the photo. Rectangle with two V-notches per long side, matte brick-red face with scattered raised dashes, chamfered edges. The blocks are laid in a 90° herringbone pattern with a cement-grey border course and a concrete kerb. There is sand in the joints and a faint oil stain. Late-afternoon sun throws neem-tree shadows. Standing height. No text or people. 4:3.

### ishape.png — attach `reference/gemini-refs/ishape-red.jpg`
> 35 mm photo of the internal road of a Bhopal housing society, paved with the I-shape (Behaton/dumbbell) paver in the photo. Each block is a capital "I": wide ends, waisted middle, chamfered corners, matte face with scattered dashes. The blocks are laid in interlocking rows of cement grey, with a brick-red edge band and concrete kerbs. Apartment blocks, young neem trees and a distant hatchback line the road; sand joints, light tyre wear. Hazy morning light, eye level. No signs, no people. 4:3 landscape.

### rectangular.png — attach `reference/photos/rect-grey.webp`
> 35 mm photo of a house porch and car-parking area in Bhopal, paved with the rectangular 200 × 100 mm concrete paver in the photo. It has a sandy matte face, small pores and a slight chamfer. The blocks are laid in a 45° herringbone of cement grey with a brick-red soldier-course border, with sand joints and light dust near a steel gate. Soft late-afternoon light, standing height. No text or people. 4:3.

### square.png — attach `reference/photos/square-grey.webp`
> 35 mm photo of a bungalow courtyard path in Bhopal, paved with the 200 × 200 mm square concrete paver in the photo. It has a flat, mottled matte grey face, tiny pores and a small chamfer. The blocks are laid in a straight grid with thin sand joints, a few a shade darker than the rest. Lawn and a plastered wall alongside. Diffused daylight, standing height looking 45° down. No text or people. 4:3.

### combo5.png — attach `reference/photos/rect-grey.webp`
> 35 mm photo of a farmhouse courtyard near Bhopal, paved with a five-size concrete paver set: five rectangle and square sizes mixed randomly like natural stone. Blocks have the sandy matte face and chamfer of the attached block, in ochre-yellow and cement grey. Sand joints, slight shade variation. Dappled neem shade, a charpai at the edge. Morning light, standing height. No text or people. 4:3.

### hexagon.png — attach `reference/gemini-refs/hexagon-grey.jpg`
> 35 mm photo of an apartment rooftop terrace in Bhopal, floored with the grey hexagon concrete tile in the photo. Each hexagon has three diamond faces of parallel grooves, each running a different way, so the honeycomb floor reads as 3D cubes. Thin joints, dust in the grooves, faint water marks. A parapet wall, a water-tank stand and potted plants are in frame. Overcast light, standing height looking 45° down. No text or people. 4:3.

### slate.png — attach `reference/gemini-refs/slate-grey.jpg`
> 35 mm photo of a bungalow garden walkway in Bhopal, paved with the slate-finish concrete slab in the photo. Square slabs with a charcoal-grey face moulded with soft diagonal ripples and veins like split slate, small pores and slightly rough edges. Staggered grid, sand joints, grass and a low hedge either side. Low morning side light picks out the texture. Knee height. No text or people. 4:3.

### antiskid.png — attach `reference/gemini-refs/antiskid-stack.jpg`
> 35 mm photo of a gentle vehicle ramp at a small Indian clinic entrance, paved with the grey anti-skid block in the photo. Rectangular blocks with a fine raised leather-grain face, laid in stretcher bond, with concrete kerbs and a steel handrail. The surface is damp after monsoon rain, with water in the joints. Overcast light, eye height from the foot of the ramp. No text, no signs, no people. 4:3 landscape.

### cobble.png — attach `reference/gemini-refs/cobble-beige.jpg`
> 35 mm photo of a curved farmhouse driveway near Bhopal, paved with the beige-grey concrete cobble in the photo. The cobbles are chunky, with rough split-rock sides and a slightly uneven top. Laid in fan arcs with wide sand joints and a few grass tufts. Behind: a neem tree, brick boundary wall, black gate. Warm late-afternoon sun, standing height. No text or people. 4:3.

### speckled.png — attach `reference/gemini-refs/speckled-slab.jpg`
> 35 mm photo of a clubhouse entrance path in a Bhopal housing society, paved with the speckled concrete block in the photo. The face is charcoal, densely packed with small rounded light and dark stone chips like terrazzo, over a light grey body. Grid layout, fine joints, a little dust and a few leaves. Door frame and potted palms soft-focus at the edge. Soft daylight, standing height. No text or people. 4:3.

### curved.png — attach `reference/gemini-refs/kerb-lineup.jpg`
> 35 mm photo of a new colony road in Bhopal edged with the plain cement-grey precast kerb stones in the photo. The kerbs have a smooth face and a chamfered top edge. The kerb line curves round a corner past a tree ring, separating black asphalt from a grey paver footpath; mortar joints, light dust, a fallen neem leaf. Morning sun, standing height looking along the kerb. No text or people. 4:3.

### tiles.png — attach `reference/gemini-refs/tile-yellow.jpg`
> 35 mm photo of a house terrace in Bhopal laid with the 300 × 300 mm ochre-yellow concrete paver tile in the photo. Moulded brick-weave face: rectangles split by recessed grooves, smooth panels alternating with pebbled ones. Laid in a grid on mortar with thin grey joints and light dust in the grooves. Parapet wall, clothes line, potted plants. Clear morning light, standing height looking 45° down. No text or people. 4:3.

### factory.png — attach `reference/photos/zigzag-grey.webp`
> 35 mm photo of the open curing yard of a concrete paver factory in Mandideep, Madhya Pradesh. Wooden pallets stacked chest-high with grey and brick-red zig-zag paver blocks, like the attached photo, stand in rows on a dusty concrete floor. Some plastic-wrapped, some damp from curing. Behind: a tin-roof shed, block-making machine, forklift and an Indian tipper truck. Bright hazy afternoon light, eye height. No logos, no writing, no faces. 4:3 landscape.

### office.png — attach `reference/photos/showroom-wide.webp`
> 35 mm photo of a paver manufacturer's sales office display in Bhopal, matching the attached photo. Sample pavers and kerb stones in grey, red, yellow and black stand in a row against a plain white wall on a grey stone floor; a small table with two plastic chairs to one side. Light scuffs on the wall. Window daylight plus a tube light. Standing height. No posters, no text, no people. 4:3 landscape.

---

## Fix-up follow-ups (same chat)

- **Wrong shape:** *"Make every block exactly the outline in my photo: [e.g. capital-I with waisted middle]. Keep everything else exactly the same."*
- **Plastic look:** *"Make the concrete matte and porous with fine sand texture and tiny pits, no shine. Phone-photo look, slight grain."*
- **Too perfect:** *"Add realistic wear: sand in the joints, light dust, a faint tyre mark, a few blocks a shade lighter. Keep the layout."*
- **Warped pattern:** *"Make the pattern regular with straight, even joints, in correct perspective from standing height."*
- **Extra objects:** *"Remove the [object] and continue the same paving there. Change nothing else."*
- **Text appears:** *"Remove all text, letters, numbers and logos. Leave those surfaces plain."*

*Sources: [Google Cloud – Ultimate Nano Banana prompting guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana), [Gemini API image generation docs](https://ai.google.dev/gemini-api/docs/image-generation).*
