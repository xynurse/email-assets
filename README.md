# email-assets

Images for email signatures, linked by raw GitHub URL.

## Originals

- `michael-thorn.JPG`: headshot illustration, white ground.
- `BSCC_Logo.png`: Byron Sportsmen and Conservation Club logo.

## Skapa Health theme (`skapa/`)

Versions in the Skapa Health house style (navy `#00203C`, blue `#0068C8`,
mist `#D6E8F8`, paper `#F3F7FB`). PNGs are rendered at 2x for sharp display.

| File | Use | Display size |
|---|---|---|
| `skapa-logo-horizontal-color.png` | Signature logo on light backgrounds (default) | 26–60px tall |
| `skapa-logo-horizontal-white.png` | Same, on navy or dark backgrounds | 26–60px tall |
| `skapa-logo-stacked-{color,white}.png` | Square spaces, banners | 60–120px tall |
| `skapa-icon-{color,white}.png` | Glyph alone: avatars, small spaces | 16–64px tall |
| `michael-thorn-skapa-{mist,paper,navy}.jpg` | Headshot on a Skapa ground, square | 80–150px |
| `michael-thorn-skapa-{mist,paper,navy}-circle.png` | Same, circle crop, transparent corners | 80–150px |
| `signature.html` | Paste-ready signature using the assets above | |

`src/` holds the official vector marks. To regenerate the PNGs and JPGs:

```bash
pip install playwright pillow numpy
python3 skapa/build.py   # set CHROMIUM_PATH to use a specific Chromium binary
```
