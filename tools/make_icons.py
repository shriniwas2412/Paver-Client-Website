#!/usr/bin/env python3
"""Draws the PNG icons from the logo mark (two interlocking zig-zag pavers). Run from the repo root."""
from PIL import Image, ImageDraw
A = [(6,14),(14,6),(22,14),(30,6),(38,14),(38,30),(30,38),(22,30),(14,38),(6,30)]
B = [(x+20, y+20) for x, y in A]
def icon(size, bg="#151412", pad=0.14):
    img = Image.new("RGBA", (size*4, size*4), bg)
    d = ImageDraw.Draw(img)
    k = size*4*(1-2*pad)/52; o = size*4*pad - 6*k
    for poly, col in ((A, "#C4553A"), (B, "#D99A22")):
        d.polygon([(o+x*k, o+y*k) for x, y in poly], fill=col)
    return img.resize((size, size), Image.LANCZOS)
for name, size in [("favicon-32", 32), ("apple-touch-icon", 180), ("logo-192", 192), ("logo-512", 512)]:
    icon(size).save(f"assets/brand/{name}.png")
