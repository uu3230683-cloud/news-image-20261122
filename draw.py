#!/usr/bin/env python3
"""Draw the 22 November 2026 world-news front page (1024x1024 PNG).

One image summing up Sunday 22 November 2026: six verified stories,
each with a flat pictogram, a headline and a one-line summary, plus a
masthead naming the day and a footer ticker of smaller stories.
Run: python3 draw.py  ->  writes entry.png next to this file.
Only Pillow is needed, and only at build time; main.py (the entrypoint)
is stdlib-only and just copies entry.png into the output directory.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (246, 241, 231)
INK = (25, 25, 25)
RED = (164, 31, 31)
BLUE = (23, 69, 107)
TEAL = (15, 92, 77)
GOLD = (176, 124, 30)
GREY = (90, 90, 88)
LIGHT = (255, 255, 255)
ORANGE = (214, 96, 20)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, leading):
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180.0 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def pic_globe(d, x, y, s):
    """Earth with a crack: the climate talks that broke apart."""
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=4)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=BLUE, width=3)
    d.line([(cx - r, cy), (cx + r, cy)], fill=BLUE, width=3)
    d.ellipse([cx - r + 8, cy - r + 14, cx - r + 34, cy - r + 34], fill=TEAL)
    d.ellipse([cx + 6, cy + 8, cx + 34, cy + 30], fill=TEAL)
    d.ellipse([cx - 20, cy + r - 30, cx + 4, cy + r - 10], fill=TEAL)
    crack = [(cx - 6, cy - r + 2), (cx + 8, cy - r // 2), (cx - 10, cy),
             (cx + 10, cy + r // 2), (cx - 4, cy + r - 2)]
    d.line(crack, fill=RED, width=5, joint="curve")


def pic_scales(d, x, y, s):
    """Scales of justice: the world court's genocide ruling."""
    cx = x + s // 2
    top = y + 8
    d.line([(cx, top), (cx, y + s - 14)], fill=INK, width=5)
    d.line([(x + 10, top + 12), (x + s - 10, top + 12)], fill=INK, width=5)
    d.line([(cx - 16, top + 2), (cx + 16, top + 2)], fill=INK, width=4)
    for sx in (x + 10, x + s - 10):
        d.line([(sx, top + 12), (sx - 18, y + s - 42)], fill=INK, width=3)
        d.line([(sx, top + 12), (sx + 18, y + s - 42)], fill=INK, width=3)
        d.arc([sx - 20, y + s - 46, sx + 20, y + s - 14], 0, 180, fill=GOLD, width=4)
    d.line([(cx - 26, y + s - 12), (cx + 26, y + s - 12)], fill=INK, width=5)


def pic_fire(d, x, y, s):
    """Factory with flames and smoke: the Banten candy-factory fire."""
    base = y + s - 16
    d.rectangle([x + 8, base - 44, x + s - 34, base], fill=GREY)
    d.rectangle([x + s - 30, base - 66, x + s - 16, base], fill=GREY)
    for wx in range(x + 16, x + s - 40, 18):
        d.rectangle([wx, base - 36, wx + 10, base - 22], fill=LIGHT)
    d.ellipse([x + s - 32, base - 82, x + s - 14, base - 64], fill=(200, 200, 200))
    d.ellipse([x + s - 38, base - 98, x + s - 18, base - 78], fill=(215, 215, 215))
    flame = [(x + 22, base - 40), (x + 34, base - 78), (x + 44, base - 52),
             (x + 56, base - 86), (x + 68, base - 44), (x + 58, base - 40)]
    d.polygon(flame, fill=ORANGE)
    inner = [(x + 34, base - 40), (x + 42, base - 62), (x + 50, base - 40)]
    d.polygon(inner, fill=(240, 200, 40))


def pic_badge(d, x, y, s):
    """A sheriff's star: the cartel boss captured in Sinaloa."""
    cx, cy = x + s // 2, y + s // 2 - 6
    d.polygon(star_points(cx, cy, s // 2 - 4, s // 5), fill=GOLD)
    d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=BLUE)
    d.polygon(star_points(cx, cy, 11, 5), fill=LIGHT)
    d.arc([x + 12, y + s - 26, x + 44, y + s - 2], 0, 360, fill=INK, width=4)
    d.arc([x + s - 44, y + s - 26, x + s - 12, y + s - 2], 0, 360, fill=INK, width=4)
    d.line([(x + 44, y + s - 14), (x + s - 44, y + s - 14)], fill=INK, width=4)


def pic_building(d, x, y, s):
    """Apartment block, top sheared off, blast star above it."""
    bx, bw = x + 14, s - 28
    top = y + 34
    jag = [(bx, top + 14), (bx + bw // 4, top), (bx + bw // 2, top + 12),
           (bx + 3 * bw // 4, top + 2), (bx + bw, top + 14)]
    d.polygon(jag + [(bx + bw, y + s - 10), (bx, y + s - 10)], fill=(120, 120, 118))
    for r in range(3):
        for c in range(4):
            wx = bx + 8 + c * (bw // 4)
            wy = top + 26 + r * 24
            d.rectangle([wx, wy, wx + 14, wy + 14], fill=(255, 220, 120)
                        if (r + c) % 3 == 0 else LIGHT)
    bx2, by2 = x + s // 2, y + 16
    d.polygon(star_points(bx2, by2, 20, 8, n=8, rot=0), fill=RED)


def pic_ship(d, x, y, s):
    """Oil tanker on waves with a spiked mine: the Hormuz attacks."""
    base = y + s - 34
    d.polygon([(x + 6, base - 26), (x + s - 6, base - 26), (x + s - 16, base),
               (x + 16, base)], fill=INK)
    for i, col in enumerate((RED, BLUE, TEAL)):
        cx0 = x + 16 + i * 26
        d.rectangle([cx0, base - 46, cx0 + 22, base - 26], fill=col)
    d.rectangle([x + s - 30, base - 52, x + s - 12, base - 26], fill=GREY)
    for wy in (base + 8, base + 20):
        for k in range(4):
            wx = x + 6 + k * 26
            d.arc([wx, wy - 8, wx + 24, wy + 8], 180, 360, fill=BLUE, width=3)
    mx, my = x + s - 26, y + 14
    d.polygon(star_points(mx, my, 16, 7, n=8, rot=0), fill=INK)
    d.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=INK)


PICS = {
    "globe": pic_globe,
    "scales": pic_scales,
    "fire": pic_fire,
    "badge": pic_badge,
    "building": pic_building,
    "ship": pic_ship,
}


def kicker_head_body(d, x, y, w, story, head_size=27, body_size=19):
    """Draw one story cell: kicker, headline, summary. Returns bottom y."""
    kf = font(SANS_B, 15)
    hf = font(SANS_B, head_size)
    bf = font(SANS, body_size)
    d.text((x, y), story["kicker"], font=kf, fill=story.get("color", RED))
    y += 22
    lines = wrap(d, story["headline"], hf, w)
    y = text_block(d, x, y, lines, hf, INK, head_size + 5)
    y += 4
    lines = wrap(d, story["body"], bf, w)
    y = text_block(d, x, y, lines, bf, (60, 60, 60), body_size + 5)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Top rules and masthead naming the day.
    d.rectangle([0, 0, W, 10], fill=RED)
    d.text((W // 2, 26), "THE WORLD IN ONE DAY", font=font(SERIF_B, 56),
           fill=INK, anchor="ma")
    d.text((W // 2, 96), "SUNDAY  \u2022  22 NOVEMBER 2026",
           font=font(SANS_B, 32), fill=RED, anchor="ma")
    d.line([(16, 148), (W - 16, 148)], fill=INK, width=3)
    d.line([(16, 154), (W - 16, 154)], fill=INK, width=1)

    # Lead story: COP31 collapse.
    lead = {
        "kicker": "CLIMATE  \u2022  ANTALYA, T\u00dcRKIYE",
        "headline": "COP31 COLLAPSES: NO DEAL ON CLIMATE",
        "body": ("UN climate talks end after two days of overtime with no "
                 "agreement, as the fight over fossil fuels splits the world."),
    }
    ly = 172
    d.rectangle([16, ly, W - 16, ly + 196], outline=INK, width=2)
    d.rectangle([16, ly, W - 16, ly + 196], fill=(255, 252, 244))
    d.rectangle([16, ly, W - 16, ly + 196], outline=INK, width=2)
    PICS["globe"](d, 34, ly + 18, 160)
    d.line([(214, ly + 14), (214, ly + 182)], fill=(200, 195, 180), width=2)
    kicker_head_body(d, 234, ly + 16, W - 234 - 28, lead, head_size=33, body_size=21)

    # Four stories in a 2x2 grid.
    grid = [
        {"pic": "scales", "kicker": "WORLD COURT  \u2022  THE HAGUE",
         "headline": "MYANMAR GUILTY OF GENOCIDE",
         "body": ("The International Court of Justice rules Myanmar committed "
                  "genocide against its Rohingya minority.")},
        {"pic": "fire", "kicker": "DISASTER  \u2022  BANTEN, INDONESIA",
         "headline": "CANDY FACTORY FIRE KILLS 3",
         "body": ("A blaze at a confectionery factory kills three workers; "
                  "dozens are still missing in the wreckage.")},
        {"pic": "badge", "kicker": "MEXICO  \u2022  SINALOA",
         "headline": "\u2018EL CHAPO ISIDRO\u2019 CAPTURED",
         "body": ("Mexican troops seize cartel boss Fausto Isidro Meza Flores "
                  "in a raid backed by US intelligence; four soldiers killed.")},
        {"pic": "building", "kicker": "WAR IN UKRAINE  \u2022  KYIV",
         "headline": "MISSILE HITS KYIV APARTMENT BLOCK",
         "body": ("A Russian strike kills three and buries others as Ukraine "
                  "fights to keep the winter cold outside.")},
    ]
    gx, gy, cw, ch, gap = 16, 384, 488, 200, 16
    for i, story in enumerate(grid):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        d.rectangle([cx, cy, cx + cw, cy + ch], outline=INK, width=2)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=(255, 252, 244))
        d.rectangle([cx, cy, cx + cw, cy + ch], outline=INK, width=2)
        PICS[story["pic"]](d, cx + 12, cy + 22, 128)
        d.line([(cx + 152, cy + 12), (cx + 152, cy + ch - 12)],
               fill=(200, 195, 180), width=2)
        kicker_head_body(d, cx + 166, cy + 14, cw - 182, story,
                         head_size=24, body_size=18)

    # Bottom banner: Hormuz tankers.
    by = 812
    hormuz = {
        "kicker": "GULF  \u2022  STRAIT OF HORMUZ",
        "headline": "TANKERS HIT NEAR HORMUZ",
        "body": ("Iran says two supertankers struck mines east of the strait; "
                 "Trump says he may strike Iran again after the new year."),
    }
    d.rectangle([16, by, W - 16, by + 132], outline=INK, width=2)
    d.rectangle([16, by, W - 16, by + 132], fill=(238, 240, 244))
    d.rectangle([16, by, W - 16, by + 132], outline=INK, width=2)
    PICS["ship"](d, 34, by + 14, 104)
    d.line([(154, by + 10), (154, by + 122)], fill=(200, 195, 180), width=2)
    kicker_head_body(d, 172, by + 10, W - 172 - 28, hormuz,
                     head_size=24, body_size=18)

    # Footer ticker of smaller stories, and the day restated.
    fy = 958
    d.line([(16, fy), (W - 16, fy)], fill=INK, width=2)
    tf = font(SANS_B, 15)
    ticker = ("ALSO:  Delta outage delays 1,600+ flights  \u2022  Ukraine drones "
              "sink Russian warship off Libya  \u2022  Tree felled in Norway")
    d.text((16, fy + 10), ticker, font=tf, fill=INK)
    d.text((W // 2, H - 24), "Sunday 22 November 2026 \u2014 the day in one image",
           font=font(SANS, 15), fill=GREY, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
