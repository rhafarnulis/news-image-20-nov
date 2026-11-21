#!/usr/bin/env python3
"""Draw the front page for Friday 20 November 2026.

Every shape and line of text is drawn with PIL on a blank canvas.
No external images, no network, no copied artwork.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
CW = W - 2 * MARGIN  # 952

PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (163, 29, 29)
BLUE = (31, 58, 95)
GREY = (90, 86, 76)
LIGHT_RULE = (180, 172, 150)
DUSK_TOP = (24, 38, 74)
DUSK_MID = (64, 68, 110)
DUSK_LOW = (214, 122, 62)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def serif(size, bold=True):
    name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    return ImageFont.truetype(FONT_DIR + name, size)


def sans(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(FONT_DIR + name, size)


def text_w(draw, text, font):
    return draw.textbbox((0, 0), text, font=font)[2]


def wrap(draw, text, font, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if text_w(draw, trial, font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, max_w, text, font, fill=INK, leading=None):
    """Draw a wrapped paragraph; return the y just below it."""
    lh = leading if leading is not None else int(font.size * 1.32)
    for line in wrap(draw, text, font, max_w):
        draw.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def headline(draw, x, y, max_w, text, font, fill=INK, leading=None):
    lh = leading if leading is not None else int(font.size * 1.12)
    for line in wrap(draw, text, font, max_w):
        draw.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def rule(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text):
    f = sans(15, bold=True)
    draw.text((x, y), text, font=f, fill=RED)
    return y + 22


def starburst(draw, cx, cy, r_outer, r_inner, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_outer if i % 2 == 0 else r_inner
        ang = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- skyline art
def draw_kyiv_art(draw, x0, y0, x1, y1):
    """Dusk skyline with missile arcs and flashes, all drawn shapes."""
    draw.rectangle([x0, y0, x1, y1], fill=DUSK_TOP)
    # horizon glow bands
    for i, col in enumerate((DUSK_MID, (150, 96, 84), DUSK_LOW)):
        band_y = y1 - 66 + i * 22
        draw.rectangle([x0, band_y, x1, band_y + 22], fill=col)
    # missile arcs (white dotted trails)
    for (sx, sy, ex, ey) in ((x0 + 30, y0 + 130, x0 + 150, y0 + 34),
                             (x0 + 330, y0 + 142, x0 + 240, y0 + 48),
                             (x0 + 190, y0 + 150, x0 + 120, y0 + 78)):
        steps = 24
        for t in range(steps + 1):
            u = t / steps
            px = sx + (ex - sx) * u
            py = sy + (ey - sy) * u - 36 * math.sin(math.pi * u)
            if t % 2 == 0:
                draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255))
        draw.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(255, 220, 120))
    # skyline silhouettes
    rng = [(0, 78, 46), (48, 108, 60), (110, 66, 34), (146, 126, 52),
           (200, 82, 40), (242, 116, 58), (302, 72, 44), (348, 100, 20)]
    base = y1
    for (dx, bh, bw) in rng:
        draw.rectangle([x0 + dx, base - bh, x0 + dx + bw, base], fill=(18, 22, 40))
    # lit windows
    for (dx, bh, bw) in rng:
        for wy in range(base - bh + 10, base - 8, 16):
            for wx in range(x0 + dx + 6, x0 + dx + bw - 6, 12):
                if (wx * 7 + wy * 13) % 5 < 2:
                    draw.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 196, 90))
    # explosion flashes above the skyline
    starburst(draw, x0 + 128, y0 + 44, 20, 8, 8, (255, 214, 90))
    starburst(draw, x0 + 128, y0 + 44, 11, 5, 8, (255, 120, 40))
    starburst(draw, x0 + 296, y0 + 30, 15, 6, 8, (255, 214, 90))
    starburst(draw, x0 + 296, y0 + 30, 8, 4, 8, (255, 120, 40))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 232, 240))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=3)
    draw.ellipse([cx - int(r * 0.55), cy - r, cx + int(r * 0.55), cy + r],
                 outline=BLUE, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=BLUE, width=2)
    draw.arc([cx - r, cy - int(r * 0.55), cx + r, cy + int(r * 0.55)],
             0, 360, fill=BLUE, width=2)
    # land blobs
    draw.ellipse([cx - r + 8, cy - r + 12, cx - 6, cy - 2], fill=(96, 150, 96))
    draw.ellipse([cx + 2, cy + 2, cx + r - 6, cy + r - 10], fill=(96, 150, 96))


def draw_chart(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=LIGHT_RULE)
    pts = [(x0 + 14 + i * (x1 - x0 - 28) / 5,
            y0 + 18 + (i * i) * (y1 - y0 - 36) / 25) for i in range(6)]
    draw.line(pts, fill=RED, width=4)
    for (px, py) in pts:
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    ex, ey = pts[-1]
    draw.polygon([(ex, ey + 12), (ex - 12, ey - 4), (ex + 2, ey - 2)], fill=RED)


def draw_eu_uk(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=LIGHT_RULE)
    cx, cy, r = (x0 + x1) // 2, (y0 + y1) // 2, 30
    draw.ellipse([cx - r - 22, cy - r, cx - r + 36, cy + r], fill=(0, 51, 153))
    for k in range(12):
        ang = 2 * math.pi * k / 12
        sx = cx - 22 + 17 * math.cos(ang)
        sy = cy + 17 * math.sin(ang)
        starburst(draw, sx, sy, 4, 2, 5, (255, 204, 0))
    draw.ellipse([cx + r - 36, cy - r, cx + r + 22, cy + r], fill=(255, 255, 255),
                 outline=INK, width=2)
    draw.text((cx + r - 22, cy - 12), "UK", font=sans(18, bold=True), fill=INK)


def draw_cyclone(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(226, 238, 244), outline=LIGHT_RULE)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for r in (9, 18, 27, 36):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=200 + 260,
                 fill=BLUE, width=4)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    for i in range(6):
        rx = x0 + 12 + i * 13
        draw.line([(rx, y1 - 10), (rx - 4, y1 - 22)], fill=BLUE, width=2)


# ------------------------------------------------------------------- the page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    mast = serif(56)
    title = "THE WORLD IN ONE DAY"
    tw = text_w(d, title, mast)
    d.text(((W - tw) / 2, 20), title, font=mast, fill=INK)
    rule(d, MARGIN, W - MARGIN, 88, fill=INK, width=3)
    rule(d, MARGIN, W - MARGIN, 93, fill=INK, width=1)
    date_f = sans(18, bold=True)
    date = "FRIDAY  ·  20 NOVEMBER 2026"
    dw = text_w(d, date, date_f)
    d.text(((W - dw) / 2, 100), date, font=date_f, fill=RED)
    sub_f = sans(14)
    sub = "One day. One page. The news that mattered."
    sw = text_w(d, sub, sub_f)
    d.text(((W - sw) / 2, 124), sub, font=sub_f, fill=GREY)
    rule(d, MARGIN, W - MARGIN, 146, fill=INK, width=2)

    # ---- lead story: Kyiv
    y = 158
    y = kicker(d, MARGIN, y, "KYIV, UKRAINE  —  OVERNIGHT")
    y = headline(d, MARGIN, y, CW,
                 "RUSSIA RAINS MISSILES ON KYIV HOURS AFTER PEACE SUMMIT",
                 serif(40), leading=45)
    y += 6
    body_y = y
    text_wd = 560
    art_x0, art_y0 = MARGIN + 584, body_y
    art_x1, art_y1 = W - MARGIN, body_y + 168
    y2 = para(d, MARGIN, body_y, text_wd,
              "More than 110 missiles and 400 drones struck Ukraine "
              "overnight, killing at least eight people, hitting three "
              "bridges across the Dnipro and cutting power across Kyiv "
              "— hours after President Putin left the Shenzhen summit "
              "with Mr Trump and Mr Xi.",
              sans(18), leading=24)
    y2 = para(d, MARGIN, y2 + 6, text_wd,
              "Poland said three objects, a cruise missile among them, "
              "crossed into its airspace. Kyiv called it one of the "
              "largest attacks of the war; Moscow said it hit military "
              "and energy sites.",
              sans(18), leading=24)
    draw_kyiv_art(d, art_x0, art_y0, art_x1, art_y1)
    cap_f = sans(13)
    d.text((art_x0, art_y1 + 6),
           "Kyiv's skyline under fire overnight. (Illustration)",
           font=cap_f, fill=GREY)
    rule(d, MARGIN, W - MARGIN, 496, fill=INK, width=2)

    # ---- second row: COP31 | markets
    col_w = (CW - 20) // 2
    x2 = MARGIN + col_w + 20
    deck_w = col_w - 110
    y = 510
    y = kicker(d, MARGIN, y, "ANTALYA, TURKEY  —  CLIMATE")
    y = headline(d, MARGIN, y, col_w,
                 "COP31 DRAFT DROPS FOSSIL FUELS", serif(26), leading=29)
    para(d, MARGIN, y + 4, deck_w,
         "The final-day draft strips out every mention of phasing "
         "out fossil fuels and drops a $120bn adaptation-finance "
         "target, angering vulnerable nations as talks run into "
         "overtime.",
         sans(16), leading=21)
    draw_globe(d, MARGIN + col_w - 48, 606, 40)

    y = 510
    y = kicker(d, x2, y, "NEW YORK  —  MARKETS")
    y = headline(d, x2, y, col_w,
                 "ANTHROPIC SLIDES ON DAY TWO AS AI ROUT SPREADS",
                 serif(26), leading=29)
    para(d, x2, y + 4, deck_w,
         "Shares in Anthropic fell about a tenth a day after its "
         "record listing, as the AI sell-off swept Asia: Tokyo's "
         "Nikkei fell 5.1% and Seoul's Kospi 5.2%, with Wall "
         "Street set for a seventh straight fall.",
         sans(16), leading=21)
    draw_chart(d, x2 + col_w - 92, 600, x2 + col_w, 680)
    rule(d, MARGIN, W - MARGIN, 716, fill=INK, width=2)

    # ---- third row: EU-UK | cyclone
    y = 730
    y = kicker(d, MARGIN, y, "BRUSSELS  —  EUROPE")
    y = headline(d, MARGIN, y, col_w,
                 "UK AND EU SEAL RESET DEAL AT SECOND SUMMIT",
                 serif(26), leading=29)
    para(d, MARGIN, y + 4, deck_w,
         "Britain and the EU signed deals on food checks, linked "
         "carbon markets and a youth scheme for 100,000 under-32s. "
         "London says the package adds 0.5% to GDP.",
         sans(16), leading=21)
    draw_eu_uk(d, MARGIN + col_w - 92, 786, MARGIN + col_w, 866)

    y = 730
    y = kicker(d, x2, y, "ODISHA, INDIA  —  WEATHER")
    y = headline(d, x2, y, col_w,
                 "CYCLONE AKVAN HITS ODISHA COAST", serif(26), leading=29)
    para(d, x2, y + 4, deck_w,
         "The storm came ashore near Gopalpur with winds gusting "
         "to 90 km/h, after 300,000 people were moved to "
         "shelters. No deaths were reported.",
         sans(16), leading=21)
    draw_cyclone(d, x2 + col_w - 92, 786, x2 + col_w, 866)
    rule(d, MARGIN, W - MARGIN, 902, fill=INK, width=2)

    # ---- in brief
    y = 916
    bf = sans(15, bold=True)
    d.text((MARGIN, y), "IN BRIEF", font=bf, fill=RED)
    y += 26
    bw = (CW - 20) // 2
    para(d, MARGIN, y, bw,
         "HORMUZ — A tanker caught fire after a projectile struck "
         "it near Oman; no casualties. Iran said it hit a mine.",
         sans(16), leading=21)
    para(d, x2, y, bw,
         "MERCURY — BepiColombo reaches Mercury after eight years "
         "and six billion miles; orbit burn set for Saturday.",
         sans(16), leading=21)
    rule(d, MARGIN, W - MARGIN, 1000, fill=INK, width=1)
    tick = sans(13)
    ticker = ("THURSDAY'S CLOSE:  S&P 500 7,176  ▼ 2.0%, a sixth straight fall  ·  "
              "Brent $90.05  ▲ 0.7%  ·  Gold ▼ 4.2%")
    tw = text_w(d, ticker, tick)
    d.text(((W - tw) / 2, 1006), ticker, font=tick, fill=GREY)
    return img


if __name__ == "__main__":
    page = build()
    page.save("entry.png", optimize=True)
    print("saved entry.png", page.size)
