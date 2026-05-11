"""
Render the Camp Hyde icon at 1024x1024 to a PNG.
Then image_to_ico.py packs it into a multi-resolution ICO.

Aesthetic: 1970s risograph camp pennant — cherry + cyan + canary on cream,
chunky Cooper Black "CH" monogram with triple offset shadow (ink → cyan → cherry).
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random
from pathlib import Path

SIZE = 1024  # 4x oversample, will downscale via ICO sizes
OUT = Path(__file__).resolve().parent.parent / "icon-source.png"

# Riso palette
CHERRY = (230, 57, 70, 255)
CHERRY_DARK = (185, 42, 53, 255)
CYAN = (16, 152, 199, 255)
CANARY = (244, 211, 94, 255)
CREAM = (244, 237, 210, 255)
INK = (11, 20, 24, 255)

img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# ── Rounded stamp base ─────────────────────────────────────────
pad = 24
stamp_box = (pad, pad, SIZE - pad, SIZE - pad)
radius = 80
d.rounded_rectangle(stamp_box, radius=radius, fill=CREAM, outline=INK, width=18)

# Inner subtle border (riso double-rule)
inner_pad = pad + 36
d.rounded_rectangle(
    (inner_pad, inner_pad, SIZE - inner_pad, SIZE - inner_pad),
    radius=radius - 28,
    outline=INK,
    width=4,
)

# ── Sunburst behind the monogram ───────────────────────────────
# Big canary sun + radiating spokes
cx, cy = SIZE // 2, SIZE // 2 + 30
sun_r = 280

# 12 rays
for i in range(12):
    angle = (i * 30) * math.pi / 180
    ray_inner = sun_r - 20
    ray_outer = sun_r + 130
    # Each ray is a chunky line
    x1 = cx + math.cos(angle) * ray_inner
    y1 = cy + math.sin(angle) * ray_inner
    x2 = cx + math.cos(angle) * ray_outer
    y2 = cy + math.sin(angle) * ray_outer
    d.line([(x1, y1), (x2, y2)], fill=CANARY, width=46)

# Sun disc (canary, drawn after rays so it sits clean over them)
d.ellipse(
    (cx - sun_r, cy - sun_r, cx + sun_r, cy + sun_r),
    fill=CANARY,
    outline=INK,
    width=10,
)

# ── Halftone dots scattered on cream margin ────────────────────
random.seed(1976)
for _ in range(140):
    px = random.randint(pad + 30, SIZE - pad - 30)
    py = random.randint(pad + 30, SIZE - pad - 30)
    # Skip if inside the sun area
    if math.hypot(px - cx, py - cy) < sun_r + 60:
        continue
    color = random.choice([CHERRY, CYAN])
    radius_d = random.choice([5, 6, 7, 8])
    # Light opacity dots
    dot_color = (*color[:3], 90)
    d.ellipse((px - radius_d, py - radius_d, px + radius_d, py + radius_d), fill=dot_color)

# ── "CH" monogram with triple-offset shadow ───────────────────
# Cooper Black, italic-ish (we'll use the upright version since COOPBL.TTF
# has the chunky 1970s shape and that's the riso vibe).
FONT_PATH = "C:/Windows/Fonts/COOPBL.TTF"
font_size = 580
font = ImageFont.truetype(FONT_PATH, font_size)

text = "CH"

# Measure
bbox = d.textbbox((0, 0), text, font=font)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
tx = (SIZE - tw) // 2 - bbox[0]
ty = (SIZE - th) // 2 - bbox[1] - 10  # nudge up slightly

# Triple-shadow stamp:  ink (back), cyan (middle), cherry (front)
SHADOW_INK = 36
SHADOW_CYAN = 20

# Ink (back)
d.text((tx + SHADOW_INK, ty + SHADOW_INK), text, font=font, fill=INK)
# Cyan
d.text((tx + SHADOW_CYAN, ty + SHADOW_CYAN), text, font=font, fill=CYAN)
# Cherry (front)
d.text((tx, ty), text, font=font, fill=CHERRY)

# ── Slight rotation for the hand-stamped feel ─────────────────
# Apply a small rotation to the whole composition so it feels stuck on slightly off
final = img.rotate(-2.5, resample=Image.BICUBIC, expand=False, fillcolor=(0, 0, 0, 0))

# Save
final.save(OUT, "PNG")
print(f"Rendered: {OUT}")
