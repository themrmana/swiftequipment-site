"""Turn the supplied Swift Equipment Ltd logo PDF into web assets.

Page 1 of the source PDF is the black wordmark on white, page 2 the same mark
reversed out of black. Only page 1 is needed: it is vector, so everything here
is a crop and a recolour of it.

Produces, in assets/img/:
    logo.svg          full wordmark, black, cropped to the ink
    logo-white.svg    the same, white, for dark backgrounds
    logo-inline.svg   the same with fill="currentColor", inlined into the page
    favicon.svg       the italic S alone, reversed out of a dark rounded square
    icon-180.png      apple-touch-icon
    icon-512.png      PWA / large icon
    og.png            1200x630 social card

Run:  python tools/make_logo_assets.py
"""

import pathlib
import re

import fitz  # PyMuPDF
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
IMG = HERE.parent / "assets" / "img"
SRC = IMG / "Swift_Equipment_Ltd_Logo.pdf"

PAD = 2.0          # points of breathing room around the cropped ink
INK = "#0b0d10"    # page background, kept in step with --ink in site.css
S_PATHS = (0, 1)   # the two drawings that make up the italic S

BODY = re.compile(r"<svg[^>]*>(.*)</svg>", re.S)
VIEWBOX = re.compile(r'viewBox="0 0 ([\d.]+) ([\d.]+)"')


def bbox(page, indices=None):
    """Union rect of the page's vector drawings, or just the ones named."""
    drawings = page.get_drawings()
    if indices is not None:
        drawings = [drawings[i] for i in indices]
    box = fitz.Rect()
    for d in drawings:
        box |= d["rect"]
    if box.is_empty:
        raise SystemExit("no vector drawings found: has the logo changed?")
    return box


def cropped(doc_path, indices=None, pad=PAD):
    """Reopen the PDF cropped to the chosen ink, returning (page, rect)."""
    doc = fitz.open(doc_path)
    page = doc[0]
    box = bbox(page, indices)
    box = fitz.Rect(box.x0 - pad, box.y0 - pad, box.x1 + pad, box.y1 + pad) & page.rect
    page.set_cropbox(box)
    return doc, page, box


def recolour(svg, colour):
    """The exported paths carry no fill, so they inherit it from the group."""
    out, n = re.subn(r"<g clip-path=", f'<g fill="{colour}" clip-path=', svg, count=1)
    if not n:
        raise SystemExit("no clip group to colour: PyMuPDF output has changed")
    return out


def white_on(pix, size, bg, radius=None, inset=0.0):
    """Paint a rendered pixmap white and centre it on a coloured tile."""
    mark = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)
    white = Image.new("RGBA", mark.size, (255, 255, 255, 255))
    white.putalpha(mark.getchannel("A"))

    w, h = size
    tile = Image.new("RGBA", size, (0, 0, 0, 0))
    if radius:
        mask = Image.new("L", size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius, fill=255)
        tile.paste(Image.new("RGBA", size, bg), mask=mask)
    else:
        tile.paste(Image.new("RGBA", size, bg))

    room_w, room_h = w * (1 - 2 * inset), h * (1 - 2 * inset)
    scale = min(room_w / white.width, room_h / white.height)
    white = white.resize(
        (max(1, round(white.width * scale)), max(1, round(white.height * scale))),
        Image.LANCZOS,
    )
    tile.alpha_composite(white, ((w - white.width) // 2, (h - white.height) // 2))
    return tile


def main():
    # --- full wordmark -----------------------------------------------------
    doc, page, box = cropped(SRC)
    svg = page.get_svg_image(text_as_path=True)

    (IMG / "logo.svg").write_text(recolour(svg, "#0b0d10"), encoding="utf-8")
    (IMG / "logo-white.svg").write_text(recolour(svg, "#ffffff"), encoding="utf-8")
    (IMG / "logo-inline.svg").write_text(recolour(svg, "currentColor"), encoding="utf-8")

    # --- social card -------------------------------------------------------
    card = page.get_pixmap(matrix=fitz.Matrix(3, 3), alpha=True)
    white_on(card, (1200, 630), INK, inset=0.14).convert("RGB").save(IMG / "og.png")

    # --- the S, for the icons ---------------------------------------------
    sdoc, spage, sbox = cropped(SRC, S_PATHS, pad=0.0)
    ssvg = spage.get_svg_image(text_as_path=True)
    body = BODY.search(recolour(ssvg, "#ffffff")).group(1)
    vw, vh = (float(v) for v in VIEWBOX.search(ssvg).groups())

    side, room = 64.0, 40.0
    scale = min(room / vw, room / vh)
    dx, dy = (side - vw * scale) / 2, (side - vh * scale) / 2
    (IMG / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n'
        f'<rect width="64" height="64" rx="14" fill="{INK}"/>\n'
        f'<g transform="translate({dx:.4f} {dy:.4f}) scale({scale:.6f})">{body}</g>\n'
        "</svg>\n",
        encoding="utf-8",
    )

    icon = spage.get_pixmap(matrix=fitz.Matrix(8, 8), alpha=True)
    white_on(icon, (180, 180), INK, radius=40, inset=0.22).save(IMG / "icon-180.png")
    white_on(icon, (512, 512), INK, radius=114, inset=0.22).save(IMG / "icon-512.png")

    print(f"wordmark  {box}  aspect {box.width / box.height:.4f}")
    print(f"S         {sbox}  aspect {sbox.width / sbox.height:.4f}")
    for f in sorted(IMG.iterdir()):
        print(f"  {f.name:22} {f.stat().st_size:>9,} bytes")


if __name__ == "__main__":
    main()
