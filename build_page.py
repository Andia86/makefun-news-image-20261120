#!/usr/bin/env python3
"""Draw the one-page broadsheet for the news of Friday 20 November 2026.

The page follows the classic two-tier broadsheet layout:

* a masthead and a large date line that name the day outright,
* eleven illustrated story cards (numbered 1-11) with a small flat
  drawing, a region tag, a serif headline and one line of summary,
* a bottom band holding a world map with numbered pins on the left
  and the remaining twenty-nine stories (12-40) as a numbered list
  on the right,
* a footer that says when every story was reported and names the
  wires and papers each item was checked against.

Every story below was reported on Friday 20 November 2026 and is
listed with its source in NEWS_SOURCES.md.  The drawing uses only
the Python standard library plus Pillow, fixed fonts and fixed
geometry: no clock, no randomness, no network, so two runs of this
program produce byte-identical PNG files.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas

SIZE = 1024
MARGIN = 26
WIDTH = SIZE - 2 * MARGIN

PAPER = (247, 243, 233)
CARD_BG = (255, 252, 244)
CARD_EDGE = (198, 186, 158)
NAVY = (20, 38, 74)
RED = (176, 32, 50)
INK = (28, 28, 30)
GREY = (96, 92, 84)
LAND = (216, 205, 178)
SEA = (238, 233, 218)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF_BOLD = str(FONT_DIR / "DejaVuSerif-Bold.ttf")
SERIF = str(FONT_DIR / "DejaVuSerif.ttf")
SANS = str(FONT_DIR / "DejaVuSans.ttf")
SANS_BOLD = str(FONT_DIR / "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- stories
# Each card: (region tag, headline, one-line summary, source line, icon key)
# Every item was reported on Friday 20 November 2026; NEWS_SOURCES.md
# carries the per-story source list.

CARDS = [
    (
        "THE HAGUE · WORLD COURT",
        "World Court: Myanmar committed genocide",
        "ICJ rules 9-6, a first in 80 years; reparations and a safe "
        "Rohingya return ordered.",
        "CNN · REUTERS",
        "scales",
    ),
    (
        "SHENZHEN · APEC SUMMIT",
        "Trump, Xi and Putin hold first trilateral talks",
        "Three leaders meet at APEC, talk nuclear risks, issue a "
        "joint \u201cpeace declaration\u201d.",
        "LE MONDE · AFP",
        "flags",
    ),
    (
        "CLIMATE · COP31 SUMMIT",
        "Fossil-fuel exit dropped from COP31 deal",
        "Near-final text scrubs the fossil-fuel transition; Pacific "
        "delegates cry outrage.",
        "DAWN · UN NEWS",
        "flame",
    ),
    (
        "STRAIT OF HORMUZ · ENERGY",
        "Iran widens tanker war as oil slides",
        "Two tankers burn after mine strikes east of Hormuz, Iran "
        "says; US war cost put over $48bn.",
        "JAPAN TIMES · DAWN",
        "tanker",
    ),
    (
        "UKRAINE · WAR",
        "Ukraine strikes Crimea Bridge again",
        "Putin rules out sea and energy truce; missiles hit Kyiv, "
        "damage two embassies.",
        "JAPAN TIMES · GT DAILY",
        "bridge",
    ),
    (
        "WALL STREET · MARKETS",
        "Anthropic's record IPO stuns Wall Street",
        "Shares open +34%, close +17% at $97.17 \u2014 largest IPO "
        "ever, raising ~$81bn.",
        "REUTERS · WSJ",
        "chart",
    ),
    (
        "GAZA · MIDDLE EAST",
        "Israel ends rare Gaza ground operation",
        "Troops pull back past the \u201cYellow Line\u201d; Shelter Cluster "
        "counts ~64,000 tents waiting.",
        "BANGKOK POST · SCOOP",
        "tent",
    ),
    (
        "BRUSSELS · EUROPE",
        "EU and UK seek reset at Brussels summit",
        "Youth mobility scheme leads the agenda at Burnham's "
        "post-Brexit reset talks.",
        "BBC · BANGKOK POST",
        "stars",
    ),
    (
        "EUROPE · PROTESTS",
        "Europe's youth take to the streets",
        "Coordinated protests over living costs; Stiglitz: the "
        "young are right to be worried.",
        "BANGKOK POST",
        "crowd",
    ),
    (
        "DEEP SPACE · NASA",
        "Voyager 1 nears one light-day from Earth",
        "Humanity's farthest probe phones home from almost a "
        "light-day away.",
        "MANILA TIMES · BANGKOK POST",
        "satellite",
    ),
    (
        "SCIENCE · SPACE",
        "Potatoes grown in moon soil",
        "Scientists report a successful crop raised in lunar "
        "regolith.",
        "DAWN",
        "sprout",
    ),
]

# Stories 12-40: headline only, sources live in NEWS_SOURCES.md.
LISTED = [
    "UK: 1,000+ drones for Ukraine",
    "Europe ready for Russia talks",
    "US sells deep-sea mining leases",
    "Meta rethinks 2030 climate goal",
    "Somalia expels UAE ambassador",
    "Bangladesh deploys paramilitary",
    "Georgia gas blast kills six",
    "Genoa airport halted by drones",
    "Istanbul mayor barred from 2028",
    "Haiti raid: at least 34 killed",
    "Florida's 20th execution of 2026",
    "UN: antibiotics failing patients",
    "AI reshapes e-government: UN",
    "Association needs no permit: UN",
    "Trump pardons Rose posthumously",
    "California probes Nvidia chips",
    "Saudi downs two Houthi drones",
    "French tower fire kills one",
    "5.6 quake near New Caledonia",
    "Cyclone Xavier in S. Pacific",
    "Van Gogh sells for record $190.4m",
    "Quarter of children in war zones",
    "Bukele eyes third term",
    "Spain PM admits mistakes",
    "Musk: GOP spending \u201cfoolish\u201d",
    "Judge tosses student visa rules",
    "Kushner cites Russia guarantees",
    "Trump too busy to meet Kim",
    "Fiona the hippo dies in Ohio",
]

DATE_LINE = "FRIDAY 20 NOVEMBER 2026"
COUNT_LINE = "40 STORIES · 6 REGIONS · ONE PAGE"
CHECK_LINE = "EVERY STORY CHECKED AGAINST ITS SOURCE"
FOOTER = (
    "Every story was reported on Friday 20 November 2026; disputed claims "
    "are attributed. Sources: Reuters, AP, AFP, BBC, CNN, Dawn, The Japan "
    "Times, Bangkok Post, Le Monde, UN News. Original drawings."
)


# ---------------------------------------------------------------- text help

def wrap(draw, text, fnt, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_lines(draw, text, path, start_size, max_width, max_lines, min_size=9):
    """Shrink a font from start_size until text wraps within max_lines."""
    size = start_size
    while size > min_size:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_width)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = font(path, min_size)
    return fnt, wrap(draw, text, fnt, max_width)


# ---------------------------------------------------------------- world map
# Coarse equirectangular continent outlines as (lon, lat) point lists,
# drawn flat in the broadsheet style.  Deliberately simplified shapes.

CONTINENTS = [
    # North America
    [(-166, 68), (-150, 70), (-135, 69), (-125, 71), (-110, 68), (-95, 69),
     (-86, 66), (-82, 62), (-79, 58), (-77, 52), (-72, 48), (-66, 45),
     (-69, 44), (-71, 41), (-74, 39), (-76, 35), (-79, 33), (-80, 27),
     (-82, 24), (-85, 21), (-88, 21), (-91, 19), (-94, 17), (-97, 16),
     (-95, 15), (-90, 14), (-86, 13), (-83, 9), (-79, 9), (-84, 12),
     (-90, 14), (-97, 16), (-102, 18), (-105, 20), (-109, 23), (-113, 27),
     (-116, 32), (-121, 34), (-123, 40), (-124, 47), (-129, 53),
     (-135, 58), (-150, 60), (-160, 61)],
    # South America
    [(-79, 9), (-75, 11), (-71, 12), (-64, 11), (-58, 8), (-52, 6),
     (-50, 1), (-44, -3), (-38, -5), (-39, -10), (-40, -16), (-41, -22),
     (-48, -26), (-53, -33), (-58, -37), (-62, -39), (-65, -43),
     (-66, -48), (-68, -52), (-70, -54), (-73, -51), (-74, -44),
     (-73, -34), (-71, -27), (-70, -20), (-72, -17), (-76, -14),
     (-79, -8), (-81, -4), (-80, 1), (-77, 4), (-78, 7)],
    # Africa
    [(-17, 15), (-16, 20), (-13, 27), (-9, 31), (-6, 35), (-1, 35),
     (5, 37), (10, 37), (15, 32), (22, 33), (30, 31), (33, 28),
     (36, 24), (39, 21), (41, 16), (43, 12), (47, 11), (51, 11),
     (49, 6), (45, 0), (41, -6), (40, -13), (37, -19), (35, -24),
     (33, -27), (29, -31), (24, -34), (19, -35), (17, -32), (15, -27),
     (13, -19), (12, -11), (10, -4), (9, 2), (5, 4), (-1, 5), (-7, 5),
     (-12, 8), (-16, 12)],
    # Madagascar
    [(44, -12), (47, -13), (50, -17), (49, -21), (46, -24), (45, -25),
     (44, -21), (43, -17)],
    # Europe
    [(-9, 37), (-9, 43), (-3, 44), (-1, 46), (-4, 48), (-1, 50),
     (2, 51), (4, 52), (6, 53), (8, 55), (8, 57), (13, 56), (18, 56),
     (21, 56), (24, 58), (27, 59), (30, 60), (28, 63), (24, 66),
     (19, 69), (13, 68), (7, 63), (5, 60), (3, 58), (-2, 57), (-4, 55),
     (-6, 58), (-8, 54), (-6, 52), (-4, 50), (-2, 49), (0, 46),
     (3, 43), (6, 43), (9, 44), (12, 44), (14, 42), (16, 40),
     (18, 40), (20, 38), (23, 37), (26, 38), (28, 41), (24, 42),
     (19, 43), (14, 45), (10, 44), (6, 43), (3, 42), (0, 39),
     (-1, 38), (-3, 37)],
    # Britain
    [(-5, 50), (-3, 51), (-2, 53), (-3, 55), (-4, 57), (-6, 58),
     (-8, 55), (-7, 53), (-6, 51)],
    # Asia (with Arabia and India)
    [(30, 60), (40, 64), (50, 68), (65, 70), (80, 73), (95, 76),
     (110, 74), (125, 73), (140, 72), (155, 70), (170, 67), (178, 65),
     (178, 62), (168, 61), (160, 58), (158, 52), (150, 50), (143, 49),
     (141, 45), (140, 40), (136, 35), (130, 33), (127, 37), (123, 38),
     (121, 34), (122, 29), (118, 25), (112, 22), (108, 19), (106, 10),
     (104, 6), (101, 7), (99, 12), (96, 16), (93, 20), (90, 22),
     (87, 21), (84, 19), (81, 15), (79, 10), (77, 8), (74, 13),
     (72, 19), (69, 22), (64, 25), (59, 25), (57, 26), (53, 26),
     (51, 24), (55, 24), (58, 23), (57, 19), (54, 16), (48, 14),
     (44, 12), (42, 14), (39, 19), (36, 26), (34, 29), (35, 33),
     (33, 36), (29, 36), (27, 37), (30, 41), (33, 44), (38, 46),
     (44, 48), (48, 51), (46, 55), (42, 58), (36, 60)],
    # Japan
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (142, 44),
     (144, 44), (142, 41), (140, 38), (138, 35), (135, 34), (132, 33)],
    # Indonesia and New Guinea
    [(95, 5), (100, 0), (105, -3), (110, -4), (115, -3), (120, -4),
     (125, -2), (130, -3), (136, -2), (141, -3), (146, -6), (150, -9),
     (147, -10), (142, -8), (137, -6), (132, -5), (127, -6), (120, -8),
     (113, -8), (106, -6), (99, -3)],
    # Australia
    [(113, -22), (114, -28), (115, -33), (118, -35), (124, -33),
     (129, -32), (133, -32), (136, -35), (139, -37), (142, -38),
     (146, -39), (150, -37), (153, -31), (153, -26), (150, -23),
     (146, -19), (143, -15), (142, -11), (141, -14), (139, -17),
     (136, -15), (135, -12), (132, -11), (129, -13), (126, -14),
     (122, -17), (118, -20)],
    # New Zealand
    [(167, -45), (170, -43), (172, -41), (174, -39), (176, -37),
     (175, -37), (173, -40), (170, -44), (168, -46)],
]

# (story number, lon, lat) — numbered pins for card stories,
# plain dots for listed stories.
PINS_NUMBERED = [
    (1, 4.9, 52.1), (2, 114.1, 22.5), (4, 56.5, 26.5), (5, 31.5, 49.0),
    (6, -74.0, 40.7), (7, 34.3, 31.4), (8, 4.35, 50.85), (9, 10.0, 48.5),
]
# Pixel nudges so near-coincident datelines stay readable (The Hague
# sits almost on top of Brussels at this scale).
PIN_OFFSETS = {1: (-10, -10), 8: (6, 7)}
PINS_DOTS = [
    (90.4, 23.8), (45.3, 2.0), (29.0, 41.0), (-72.3, 18.5),
    (165.0, -21.5), (8.9, 44.4), (-84.0, 30.4), (44.8, 41.7),
]


def draw_map(draw, x0, y0, w, h):
    """Flat world map in the panel, with story pins."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA)

    def project(lon, lat):
        px = x0 + (lon + 180.0) / 360.0 * w
        py = y0 + (84.0 - lat) / 168.0 * h
        return px, py

    for outline in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in outline]
        draw.polygon(pts, fill=LAND, outline=NAVY, width=1)

    for lon, lat in PINS_DOTS:
        px, py = project(lon, lat)
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=NAVY)

    pin_font = font(SANS_BOLD, 10)
    for number, lon, lat in PINS_NUMBERED:
        px, py = project(lon, lat)
        ox, oy = PIN_OFFSETS.get(number, (0, 0))
        px, py = px + ox, py + oy
        r = 8
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                     outline=(255, 255, 255), width=1)
        label = str(number)
        tw = draw.textlength(label, font=pin_font)
        draw.text((px - tw / 2, py - 6), label, font=pin_font,
                  fill=(255, 255, 255))


# ---------------------------------------------------------------- icons
# Small flat glyphs drawn with primitives in a square box (x, y, size).

def _line(draw, pts, fill=NAVY, width=3):
    draw.line(pts, fill=fill, width=width, joint="curve")


def icon_scales(draw, x, y, s):
    cx = x + s / 2
    _line(draw, [(cx, y + 4), (cx, y + s - 6)])
    _line(draw, [(x + 6, y + 10), (x + s - 6, y + 10)])
    for side in (-1, 1):
        px = cx + side * (s / 2 - 8)
        _line(draw, [(px, y + 10), (px - 7, y + s - 16)], width=2)
        _line(draw, [(px, y + 10), (px + 7, y + s - 16)], width=2)
        draw.arc([px - 9, y + s - 24, px + 9, y + s - 6], 0, 180,
                 fill=RED, width=3)
    draw.ellipse([cx - 4, y, cx + 4, y + 8], fill=RED)


def icon_flags(draw, x, y, s):
    for i, colour in enumerate((RED, NAVY, RED)):
        px = x + 8 + i * (s - 16) / 2
        _line(draw, [(px, y + s - 4), (px, y + 6)], width=2)
        draw.polygon([(px, y + 6), (px + 13, y + 11), (px, y + 16)],
                     fill=colour)


def icon_flame(draw, x, y, s):
    cx = x + s / 2
    flame = [(cx, y + 2), (cx + 11, y + s * 0.45), (cx + 13, y + s - 8),
             (cx + 4, y + s - 2), (cx - 4, y + s - 2), (cx - 13, y + s - 8),
             (cx - 10, y + s * 0.42), (cx - 3, y + s * 0.30)]
    draw.polygon(flame, fill=RED)
    inner = [(cx, y + s * 0.42), (cx + 6, y + s * 0.66),
             (cx + 5, y + s - 8), (cx - 5, y + s - 8),
             (cx - 6, y + s * 0.64)]
    draw.polygon(inner, fill=(247, 190, 60))


def icon_tanker(draw, x, y, s):
    hull = [(x + 3, y + s * 0.55), (x + s - 3, y + s * 0.55),
            (x + s - 10, y + s * 0.78), (x + 10, y + s * 0.78)]
    draw.polygon(hull, fill=NAVY)
    draw.rectangle([x + s * 0.62, y + s * 0.32, x + s * 0.78, y + s * 0.55],
                   fill=RED)
    _line(draw, [(x + 8, y + s * 0.45), (x + s * 0.60, y + s * 0.45)],
          width=3)
    for i in range(3):
        wx = x + 6 + i * (s - 12) / 2
        draw.arc([wx, y + s * 0.82, wx + (s - 12) / 2, y + s * 0.98],
                 0, 180, fill=NAVY, width=2)


def icon_bridge(draw, x, y, s):
    deck = y + s * 0.72
    _line(draw, [(x + 2, deck), (x + s - 2, deck)], width=3)
    for tx in (x + s * 0.28, x + s * 0.72):
        _line(draw, [(tx, y + 8), (tx, deck)], width=3)
    draw.arc([x + 2, y + 8, x + s * 0.56, deck + 6], 180, 330,
             fill=RED, width=2)
    draw.arc([x + s * 0.44, y + 8, x + s - 2, deck + 6], 210, 360,
             fill=RED, width=2)
    draw.arc([x + s * 0.22, y - 6, x + s * 0.78, deck - 8], 0, 180,
             fill=RED, width=2)


def icon_chart(draw, x, y, s):
    _line(draw, [(x + 6, y + 4), (x + 6, y + s - 6)], width=2)
    _line(draw, [(x + 6, y + s - 6), (x + s - 3, y + s - 6)], width=2)
    pts = [(x + 10, y + s * 0.68), (x + s * 0.38, y + s * 0.52),
           (x + s * 0.58, y + s * 0.58), (x + s - 8, y + s * 0.22)]
    _line(draw, pts, fill=RED, width=3)
    draw.polygon([(x + s - 8, y + s * 0.22), (x + s - 16, y + s * 0.24),
                  (x + s - 9, y + s * 0.32)], fill=RED)


def icon_tent(draw, x, y, s):
    apex = (x + s / 2, y + 6)
    draw.polygon([apex, (x + 3, y + s - 6), (x + s - 3, y + s - 6)],
                 outline=NAVY, width=3)
    draw.polygon([(x + s / 2, y + s * 0.52), (x + s * 0.36, y + s - 6),
                  (x + s * 0.64, y + s - 6)], fill=RED)
    _line(draw, [(x + 2, y + s - 3), (x + s - 2, y + s - 3)], width=2)


def icon_stars(draw, x, y, s):
    import math
    cx, cy = x + s / 2, y + s / 2
    for i in range(8):
        ang = 2 * math.pi * i / 8
        px, py = cx + 17 * math.cos(ang), cy + 17 * math.sin(ang)
        draw.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=NAVY)
    star = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        r = 9 if i % 2 == 0 else 4
        star.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(star, fill=RED)


def icon_frame(draw, x, y, s):
    draw.rectangle([x + 5, y + 5, x + s - 5, y + s - 5], outline=NAVY,
                   width=3)
    draw.rectangle([x + 11, y + 11, x + s - 11, y + s - 11],
                   outline=RED, width=2)
    _line(draw, [(x + 13, y + s - 13), (x + s * 0.42, y + s * 0.45),
                 (x + s * 0.58, y + s * 0.62), (x + s * 0.72, y + s * 0.5),
                 (x + s - 13, y + s - 13)], fill=NAVY, width=2)
    draw.ellipse([x + s * 0.60, y + 15, x + s * 0.60 + 7, y + 22],
                 fill=RED)


def icon_satellite(draw, x, y, s):
    draw.rectangle([x + s * 0.40, y + s * 0.36, x + s * 0.60, y + s * 0.58],
                   fill=NAVY)
    draw.rectangle([x + 4, y + s * 0.30, x + s * 0.34, y + s * 0.52],
                   outline=RED, width=3)
    draw.rectangle([x + s * 0.66, y + s * 0.42, x + s - 4, y + s * 0.64],
                   outline=RED, width=3)
    _line(draw, [(x + s / 2, y + s * 0.58), (x + s / 2, y + s * 0.74)],
          width=2)
    draw.arc([x + s * 0.36, y + s * 0.62, x + s * 0.64, y + s * 0.94],
             300, 60, fill=NAVY, width=2)
    draw.arc([x + s * 0.30, y + s * 0.56, x + s * 0.70, y + s - 2],
             300, 60, fill=NAVY, width=2)


def icon_crowd(draw, x, y, s):
    heads = [(0.28, 0.40, 6), (0.52, 0.30, 7), (0.74, 0.42, 6)]
    for i, (fx, fy, r) in enumerate(heads):
        cx, cy = x + s * fx, y + s * fy
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=RED if i == 1 else NAVY)
        draw.arc([cx - r - 3, cy + r - 2, cx + r + 3, cy + r + 12],
                 180, 360, fill=RED if i == 1 else NAVY, width=3)
    _line(draw, [(x + 6, y + s - 4), (x + s - 6, y + s - 4)], width=2)


def icon_sprout(draw, x, y, s):
    cx = x + s / 2
    _line(draw, [(cx, y + s - 8), (cx, y + s * 0.34)], width=3)
    draw.polygon([(cx, y + s * 0.40), (cx - 15, y + s * 0.30),
                  (cx - 16, y + s * 0.12), (cx - 2, y + s * 0.16)],
                 fill=RED)
    draw.polygon([(cx, y + s * 0.34), (cx + 15, y + s * 0.22),
                  (cx + 16, y + 4), (cx + 2, y + 10)], fill=NAVY)
    _line(draw, [(x + 6, y + s - 5), (x + s - 6, y + s - 5)], width=2)


ICONS = {
    "scales": icon_scales, "flags": icon_flags, "flame": icon_flame,
    "tanker": icon_tanker, "bridge": icon_bridge, "chart": icon_chart,
    "tent": icon_tent, "stars": icon_stars, "frame": icon_frame,
    "satellite": icon_satellite, "sprout": icon_sprout,
    "crowd": icon_crowd,
}


# ---------------------------------------------------------------- layout

def draw_card(draw, x, y, w, h, number, card):
    tag, headline, summary, src, icon = card
    draw.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=CARD_EDGE,
                   width=1)
    # number chip
    r = 13
    cx, cy = x + 12 + r, y + 10 + r
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    num_font = font(SANS_BOLD, 14)
    label = str(number)
    tw = draw.textlength(label, font=num_font)
    draw.text((cx - tw / 2, cy - 8), label, font=num_font,
              fill=(255, 255, 255))
    # icon
    ICONS[icon](draw, x + 8, y + 44, 46)
    # text column
    tx = x + 64
    tw_max = x + w - 10 - tx
    draw.text((tx, y + 9), tag, font=font(SANS_BOLD, 10), fill=RED)
    h_font, h_lines = fit_lines(draw, headline, SERIF_BOLD, 16, tw_max, 2)
    hy = y + 24
    for line in h_lines:
        draw.text((tx, hy), line, font=h_font, fill=INK)
        hy += 17
    s_font, s_lines = fit_lines(draw, summary, SANS, 11, tw_max, 2)
    sy = max(hy + 2, y + 60)
    for line in s_lines:
        draw.text((tx, sy), line, font=s_font, fill=INK)
        sy += 13
    draw.text((tx, y + h - 15), f"{src} \u2713 20 NOV 2026",
              font=font(SANS_BOLD, 8), fill=GREY)


def draw_list_panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=CARD_EDGE,
                   width=1)
    draw.text((x + 14, y + 12), "ALSO IN THE DAY \u2014 STORIES 12\u201340",
              font=font(SANS_BOLD, 13), fill=NAVY)
    col_w = (w - 28 - 16) // 2
    columns = [(LISTED[:15], 12), (LISTED[15:], 27)]
    for idx, (items, first_no) in enumerate(columns):
        cx = x + 14 + idx * (col_w + 16)
        cy = y + 38
        for j, headline in enumerate(items):
            no = first_no + j
            draw.text((cx, cy), str(no), font=font(SANS_BOLD, 11), fill=RED)
            lines = wrap(draw, headline, font(SANS, 11), col_w - 24)
            ly = cy
            for line in lines:
                draw.text((cx + 24, ly), line, font=font(SANS, 11), fill=INK)
                ly += 13
            cy = ly + 4


def build():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(img)

    # masthead
    draw.rectangle([MARGIN, MARGIN, MARGIN + WIDTH, MARGIN + 58],
                   fill=NAVY)
    title_font = font(SERIF_BOLD, 32)
    title = "THE DAY IN WORLD NEWS"
    tw = draw.textlength(title, font=title_font)
    draw.text((MARGIN + (WIDTH - tw) / 2, MARGIN + 12), title,
              font=title_font, fill=(247, 243, 233))
    draw.rectangle([MARGIN, MARGIN + 62, MARGIN + WIDTH, MARGIN + 66],
                   fill=RED)

    # date band
    d_font, _ = fit_lines(draw, DATE_LINE, SERIF_BOLD, 37, 640, 1)
    draw.text((MARGIN, 102), DATE_LINE, font=d_font, fill=NAVY)
    count_font = font(SANS_BOLD, 15)
    cw = draw.textlength(COUNT_LINE, font=count_font)
    draw.text((MARGIN + WIDTH - cw, 104), COUNT_LINE, font=count_font,
              fill=RED)
    check_font = font(SANS, 11)
    kw = draw.textlength(CHECK_LINE, font=check_font)
    draw.text((MARGIN + WIDTH - kw, 128), CHECK_LINE, font=check_font,
              fill=GREY)
    draw.line([MARGIN, 156, MARGIN + WIDTH, 156], fill=GREY, width=1)

    # story cards: 3 columns x 4 rows, the last cell is a brief panel
    col_w, card_h, gap_x, gap_y = 314, 104, 15, 10
    top = 168
    for i, card in enumerate(CARDS):
        row, col = divmod(i, 3)
        x = MARGIN + col * (col_w + gap_x)
        y = top + row * (card_h + gap_y)
        draw_card(draw, x, y, col_w, card_h, i + 1, card)
    bx = MARGIN + 2 * (col_w + gap_x)
    by = top + 3 * (card_h + gap_y)
    draw.rectangle([bx, by, bx + col_w, by + card_h], fill=NAVY)
    brief_font = font(SERIF_BOLD, 17)
    draw.text((bx + 16, by + 14), "THE DAY IN BRIEF",
              font=brief_font, fill=(247, 243, 233))
    for j, line in enumerate(wrap(
            draw, "Twenty-nine more stories from every region of the "
                  "world, listed below.", font(SANS, 11), col_w - 32)):
        draw.text((bx + 16, by + 44 + j * 14), line, font=font(SANS, 11),
                  fill=(247, 243, 233))

    # bottom band: map + list
    band_y, band_h = 626, 332
    map_w = 452
    draw.rectangle([MARGIN, band_y, MARGIN + map_w, band_y + band_h],
                   fill=(252, 250, 242), outline=CARD_EDGE, width=1)
    draw.text((MARGIN + 14, band_y + 12), "WHERE IT HAPPENED",
              font=font(SANS_BOLD, 13), fill=NAVY)
    draw_map(draw, MARGIN + 14, band_y + 36, map_w - 28, band_h - 78)
    draw.text((MARGIN + 14, band_y + band_h - 30),
              "Red pins: the numbered stories. Dots: further datelines.",
              font=font(SANS, 10), fill=GREY)
    draw_list_panel(draw, MARGIN + map_w + 14, band_y,
                    WIDTH - map_w - 14, band_h)

    # footer
    draw.line([MARGIN, 970, MARGIN + WIDTH, 970], fill=GREY, width=1)
    f_lines = wrap(draw, FOOTER, font(SANS, 10), WIDTH - 40)
    for j, line in enumerate(f_lines):
        lw = draw.textlength(line, font=font(SANS, 10))
        draw.text((MARGIN + (WIDTH - lw) / 2, 978 + j * 13), line,
                  font=font(SANS, 10), fill=GREY)

    return img


def main():
    import hashlib
    out = Path(__file__).resolve().parent / "entry.png"
    img = build()
    img.save(out, format="PNG")
    data = out.read_bytes()
    print(f"wrote {out} ({len(data)} bytes) "
          f"sha256={hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
