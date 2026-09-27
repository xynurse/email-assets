"""Build the Skapa Health email assets.

Rasterizes the official SVG marks in src/ to transparent PNGs (email clients
do not render SVG) and makes Skapa-ground versions of the headshot.

    pip install playwright pillow numpy
    python3 skapa/build.py

Set CHROMIUM_PATH to use a specific Chromium binary.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "src")

MIST = (0xD6, 0xE8, 0xF8)
PAPER = (0xF3, 0xF7, 0xFB)
NAVY = (0x00, 0x20, 0x3C)

# (svg name, output height in px). Heights are 2x the intended display size
# so the marks stay sharp on retina screens.
LOGOS = [
    ("skapa-logo-horizontal-color", 120),  # display at 60px tall
    ("skapa-logo-horizontal-white", 120),
    ("skapa-logo-stacked-color", 240),     # display at 120px tall
    ("skapa-logo-stacked-white", 240),
    ("skapa-icon-color", 128),             # display at 64px tall
    ("skapa-icon-white", 128),
]


def rasterize_logos():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            executable_path=os.environ.get("CHROMIUM_PATH") or None
        )
        page = browser.new_page()
        for name, h in LOGOS:
            svg = open(os.path.join(SRC, name + ".svg")).read()
            page.set_content(
                "<style>html,body{margin:0;background:transparent}"
                f"img{{display:block;height:{h}px}}</style>"
                f"<img src='data:image/svg+xml;base64,{__import__('base64').b64encode(svg.encode()).decode()}'>"
            )
            page.wait_for_timeout(100)
            page.locator("img").screenshot(
                path=os.path.join(HERE, name + ".png"), omit_background=True
            )
        browser.close()


def background_mask(img):
    """Alpha mask (0-255) of the near-white backdrop connected to the top edge."""
    probe = img.convert("RGB").copy()
    w, _ = probe.size
    key = (255, 0, 255)
    for x in range(0, w, 16):
        if min(probe.getpixel((x, 0))) > 235:
            ImageDraw.floodfill(probe, (x, 0), key, thresh=40)
    a = np.array(probe)
    mask = (a[..., 0] == 255) & (a[..., 1] == 0) & (a[..., 2] == 255)
    m = Image.fromarray((mask * 255).astype(np.uint8))
    # Soften the cut so the illustration's outline blends into the new ground.
    return m.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.2))


def headshots():
    src = Image.open(os.path.join(ROOT, "michael-thorn.JPG")).convert("RGB")
    mask = background_mask(src)
    size = 600  # display at 120-150px

    for name, ground in (("mist", MIST), ("paper", PAPER), ("navy", NAVY)):
        bg = Image.new("RGB", src.size, ground)
        out = Image.composite(bg, src, mask).resize((size, size), Image.LANCZOS)

        out.save(os.path.join(HERE, f"michael-thorn-skapa-{name}.jpg"), quality=90)

        # Circle crop with transparent corners, drawn at 4x for a clean edge.
        big = Image.new("L", (size * 4, size * 4), 0)
        ImageDraw.Draw(big).ellipse((0, 0, size * 4 - 1, size * 4 - 1), fill=255)
        circle = out.convert("RGBA")
        circle.putalpha(big.resize((size, size), Image.LANCZOS))
        circle.save(os.path.join(HERE, f"michael-thorn-skapa-{name}-circle.png"))


if __name__ == "__main__":
    rasterize_logos()
    headshots()
    print("done")
