#!/usr/bin/env python3
"""Draw "THE WORLD ON ONE PAGE" — Wednesday 25 November 2026.

A dense newspaper front page in the style of the 24 Nov rank-1 winner:
35 stories, all from Wednesday 25 November 2026, region counts up front,
a big-numbers strip, three illustrated hero leads, eight secondary stories,
a pin map, a 24-item ALSO list and a red DATE CHECK strip.

Everything is drawn with Pillow from the numbers and headlines below —
no photos, no external assets, no network, no randomness, no clock.
Running this script twice writes byte-identical PNGs.

    python3 draw.py            # writes entry.png next to this file
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---- palette (cream newsprint, ink black, one red accent) ----
CREAM = (247, 242, 230)
PAPER = (239, 232, 214)
INK = (22, 21, 19)
RED = (169, 50, 38)
SEA = (207, 224, 232)
LAND = (232, 217, 168)
LAND2 = (220, 198, 132)
GREY = (110, 106, 96)
DARK = (28, 43, 74)          # night sky for the rocket panel
WHITE = (255, 255, 255)

REGION = {
    "EUROPE": (31, 78, 121),
    "MIDDLE EAST": (176, 58, 46),
    "ASIA": (123, 45, 139),
    "AFRICA": (46, 125, 50),
    "AMERICAS": (15, 118, 110),
    "OCEANIA": (194, 112, 30),
    "GLOBAL": (85, 85, 85),
}

FD = "/usr/share/fonts/truetype"
SERIF_B = f"{FD}/liberation/LiberationSerif-Bold.ttf"
SERIF = f"{FD}/liberation/LiberationSerif-Regular.ttf"
SERIF_I = f"{FD}/liberation/LiberationSerif-Italic.ttf"
SANS_B = f"{FD}/liberation/LiberationSans-Bold.ttf"
SANS = f"{FD}/liberation/LiberationSans-Regular.ttf"
SANS_I = f"{FD}/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_size(d, text, path, start, max_w):
    """Largest font size (from `start` down) at which `text` fits max_w."""
    size = start
    while size > 8:
        f = font(path, size)
        if d.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, 8)


def centered(d, y, text, f, fill=INK, x0=0, x1=W):
    w = d.textlength(text, font=f)
    d.text(((x0 + x1 - w) / 2, y), text, font=f, fill=fill)


def para(d, x, y, text, f, max_w, lh, fill=INK):
    """Draw wrapped paragraph; returns the y just below the last line."""
    for line in wrap(d, text, f, max_w):
        d.text((x, y), line, font=f, fill=fill)
        y += lh
    return y


def rule(d, y, x0=12, x1=1012, width=1, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

# =====================================================================
# Masthead
# =====================================================================
d.text((12, 8), "THE WORLD ON ONE PAGE", font=font(SANS_B, 15), fill=INK)
centered(d, 9, "DAY 329 OF 2026", font(SANS_B, 13), fill=RED)
right = "EVERY STORY DATED WEDNESDAY 25 NOV"
d.text((1012 - d.textlength(right, font=font(SANS_B, 13)), 9), right,
       font=font(SANS_B, 13), fill=INK)
rule(d, 27, width=1)

# =====================================================================
# Headline
# =====================================================================
headline = "Wednesday 25 November 2026"
hf = fit_size(d, headline, SERIF_B, 60, 990)
centered(d, 34, headline, hf)
rule(d, 98, width=2)

# =====================================================================
# Region banner
# =====================================================================
banner = ("35 STORIES, ALL FROM WEDNESDAY 25 NOV \u00b7 EUROPE 6 \u00b7 "
          "MIDDLE EAST 5 \u00b7 ASIA 9 \u00b7 AFRICA 4 \u00b7 AMERICAS 7 \u00b7 "
          "OCEANIA 2 \u00b7 GLOBAL 2")
centered(d, 104, banner, font(SANS_B, 14))
rule(d, 124, width=1)

# =====================================================================
# Ticker: the three hero teasers, red diamonds between them
# =====================================================================
tick = ("Drones hit two refineries 800 km inside Russia  \u25c6  "
        "Asian stocks rout as KOSPI falls 6%  \u25c6  "
        "First foreign astronaut reaches Tiangong")
centered(d, 130, tick, font(SERIF_I, 15))
rule(d, 150, width=1)

# =====================================================================
# Big-numbers row: six figures, six captions
# =====================================================================
bignums = [
    ("2", "Russian refineries\nhit overnight"),
    ("800 km", "how deep the\nstrikes reached"),
    ("\u22126%", "KOSPI's fall on\ntariff fears"),
    ("1st", "foreign astronaut\non Tiangong"),
    ("50", "Boeing 737-8 jets\nfor Xiamen"),
    ("4,000 kg", "of explosives\ndestroyed in Iowa"),
]
col_w = 1000 / 6
for i, (num, cap) in enumerate(bignums):
    cx = 12 + i * col_w
    nf = fit_size(d, num, SERIF_B, 30, col_w - 12)
    centered(d, 156, num, nf, x0=cx, x1=cx + col_w)
    for j, line in enumerate(cap.split("\n")):
        centered(d, 190 + j * 12, line, font(SANS, 10), fill=GREY,
                 x0=cx, x1=cx + col_w)
rule(d, 218, width=1)

# =====================================================================
# Hero panels: three illustrated leads (maps drawn in code)
# =====================================================================
HX = [12, 351, 690]          # hero column x starts
HW = 322                     # hero column width
MAP_Y0, MAP_Y1 = 224, 350    # map art box

def flame(dx, x, y, r=7):
    """A small red/orange flame marker."""
    dx.ellipse([x - r, y - r, x + r, y + r], fill=RED)
    dx.ellipse([x - r * 0.55, y - r * 0.45, x + r * 0.55, y + r * 0.6],
               fill=(255, 176, 66))

def dot(dx, x, y, r=4, fill=INK):
    dx.ellipse([x - r, y - r, x + r, y + r], fill=fill)
    dx.ellipse([x - r, y - r, x + r, y + r], outline=WHITE, width=1)

# --- Hero 1: Samara refineries (western Russia) ---
x0 = HX[0]
d.rectangle([x0, MAP_Y0, x0 + HW, MAP_Y1], fill=LAND, outline=INK, width=1)
d.polygon([(x0, 300), (x0, MAP_Y1), (95, MAP_Y1), (75, 302)], fill=SEA)
d.polygon([(x0, 292), (110, 282), (140, 320), (100, MAP_Y1), (x0, MAP_Y1)],
          fill=LAND2, outline=(120, 100, 40))
d.line([(x0, 292), (110, 282), (140, 320)], fill=(120, 100, 40), width=1)
d.text((x0 + 8, MAP_Y0 + 6), "POLAND", font=font(SANS_B, 10), fill=GREY)
d.text((x0 + 14, 318), "UKRAINE", font=font(SANS_B, 10), fill=GREY)
d.text((x0 + 150, MAP_Y0 + 8), "RUSSIA", font=font(SANS_B, 13), fill=GREY)
dot(d, x0 + 238, 258)
d.text((x0 + 246, 252), "Moscow", font=font(SANS, 10), fill=INK)
# dashed drone path from the Ukrainian border to Samara
for t in range(0, 21):
    px = 150 + t * 7
    py = 332 - t * 2
    if t % 2 == 0:
        d.ellipse([x0 + px - 2, py - 2, x0 + px + 2, py + 2], fill=RED)
flame(d, x0 + 282, 292)
flame(d, x0 + 300, 302)
d.text((x0 + 258, 312), "Syzran", font=font(SANS, 9), fill=INK)
d.text((x0 + 292, 322), "Kuibyshev", font=font(SANS, 9), fill=INK)
d.rectangle([x0 + 176, 330, x0 + 318, 347], fill=WHITE, outline=RED, width=1)
d.text((x0 + 182, 333), "2 REFINERIES HIT", font=font(SANS_B, 11), fill=RED)

# --- Hero 2: Korea-Japan markets (plunging chart over a map) ---
x0 = HX[1]
d.rectangle([x0, MAP_Y0, x0 + HW, MAP_Y1], fill=SEA, outline=INK, width=1)
d.polygon([(x0 + 78, 268), (x0 + 92, 252), (x0 + 104, 268), (x0 + 112, 300),
           (x0 + 96, 336), (x0 + 80, 320), (x0 + 72, 292)], fill=LAND,
          outline=(120, 100, 40))
d.polygon([(x0 + 210, 240), (x0 + 222, 236), (x0 + 228, 258), (x0 + 220, 282),
           (x0 + 206, 268)], fill=LAND, outline=(120, 100, 40))
d.polygon([(x0 + 238, 292), (x0 + 250, 288), (x0 + 254, 312), (x0 + 242, 330),
           (x0 + 232, 312)], fill=LAND, outline=(120, 100, 40))
d.polygon([(x0 + 258, 330), (x0 + 268, 326), (x0 + 270, 342), (x0 + 258, 348)],
          fill=LAND, outline=(120, 100, 40))
for gy in (262, 292, 322):
    d.line([(x0 + 6, gy), (x0 + HW - 6, gy)], fill=(255, 255, 255), width=1)
chart = [(x0 + 150, 250), (x0 + 190, 262), (x0 + 230, 282),
         (x0 + 270, 312), (x0 + 305, 334)]
d.line(chart, fill=RED, width=3)
d.polygon([(x0 + 305, 334), (x0 + 293, 326), (x0 + 295, 340)], fill=RED)
dot(d, x0 + 92, 282, r=4)
d.text((x0 + 100, 276), "SEOUL", font=font(SANS_B, 10), fill=INK)
d.text((x0 + 216, 300), "TOKYO", font=font(SANS_B, 10), fill=INK)
d.text((x0 + 10, 228), "KOSPI \u22126.0%", font=font(SANS_B, 14), fill=RED)
d.text((x0 + 10, 246), "NIKKEI \u22123.3%", font=font(SANS_B, 11), fill=INK)

# --- Hero 3: Shenzhou-24 (night sky, rocket, Earth arc) ---
# Drawn on its own layer so the Earth arc is clipped to the panel.
x0 = HX[2]
layer = Image.new("RGBA", (HW, MAP_Y1 - MAP_Y0), (0, 0, 0, 0))
ld = ImageDraw.Draw(layer)
ld.rectangle([0, 0, HW, MAP_Y1 - MAP_Y0], fill=DARK)
for sx, sy in [(20, 14), (60, 34), (110, 10), (160, 24), (210, 8), (260, 32),
               (300, 14), (40, 76), (140, 94), (240, 92), (290, 72),
               (180, 58)]:
    ld.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=WHITE)
ld.ellipse([-40, 96, 360, 206], fill=(58, 110, 165))
ld.ellipse([80, 106, 130, 128], fill=(74, 140, 90))
ld.ellipse([220, 111, 270, 128], fill=(74, 140, 90))
for t in range(0, 15):
    px = 90 + t * 10
    py = 116 - t * 3
    ld.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 220, 130))
rx, ry = 235, 46
ld.polygon([(rx - 7, ry + 26), (rx - 10, ry + 44), (rx + 10, ry + 44),
            (rx + 7, ry + 26)], fill=(255, 140, 40))
ld.polygon([(rx - 9, ry - 26), (rx + 9, ry - 26), (rx + 6, ry + 28),
            (rx - 6, ry + 28)], fill=WHITE, outline=(200, 200, 200))
ld.polygon([(rx - 9, ry - 26), (rx, ry - 40), (rx + 9, ry - 26)], fill=RED)
ld.ellipse([rx - 3, ry - 6, rx + 3, ry], fill=(58, 110, 165))
ld.ellipse([272, 8, 314, 50], fill=RED)
ld.text((284, 22), "1st", font=font(SANS_B, 15), fill=WHITE)
ld.text((10, 76), "SHENZHOU-24", font=font(SANS_B, 10), fill=(255, 220, 130))
ld.text((10, 94), "JIUQUAN", font=font(SANS_B, 10), fill=WHITE)
ld.text((180, 8), "TIANGONG", font=font(SANS_B, 10), fill=WHITE)
img.paste(layer, (x0, MAP_Y0), layer)
d.rectangle([x0, MAP_Y0, x0 + HW, MAP_Y1], outline=INK, width=1)

# --- Hero text blocks: tag bar, headline, body, source ---
heroes = [
    ("EUROPE \u00b7 WAR", "1", "SAMARA, RUSSIA",
     "Drones hit two refineries 800 km inside Russia",
     "Ukrainian long-range drones struck the Syzran and Kuibyshev "
     "refineries in Samara overnight, setting both ablaze; video shows "
     "air defences firing. The plants sit ~800 km from Ukraine's border. "
     "Neither Kyiv nor Moscow has confirmed the strikes; Putin vowed "
     "retaliation.",
     "KYIV INDEPENDENT \u00b7 INDEPENDENT \u00b7 H.UA"),
    ("ASIA \u00b7 MARKETS", "2", "SEOUL / TOKYO",
     "Asian stocks rout as KOSPI falls 6%",
     "Asia-Pacific shares sold off hard on US tariff fears ahead of USTR "
     "chief Greer's report: KOSPI \u22126.0% to 4,705, Taiwan \u22124.7%, "
     "Nikkei \u22123.3% to 56,710. Brent crude fell to $90.09. Worst day "
     "for Seoul and Taipei since April's tariff shock.",
     "REUTERS MORNING BID"),
    ("ASIA \u00b7 SPACE", "3", "JIUQUAN, CHINA",
     "First foreign astronaut reaches Tiangong",
     "China launched Shenzhou-24 at 00:18 UTC from Jiuquan, carrying Tang "
     "Hongbo, Wu Yi and Pakistani Muhammad Zeeshan Ali, 40 \u2014 the "
     "first foreign astronaut ever to visit Tiangong. He stays 5\u201310 "
     "days running experiments; docking is planned today.",
     "REUTERS \u00b7 XINHUA"),
]
for i, (tag, num, place, head, body, src) in enumerate(heroes):
    x0 = HX[i]
    tagcol = REGION["EUROPE"] if i == 0 else REGION["ASIA"]
    tw = d.textlength(tag, font=font(SANS_B, 10)) + 12
    d.rectangle([x0, 354, x0 + tw, 370], fill=tagcol)
    d.text((x0 + 6, 357), tag, font=font(SANS_B, 10), fill=WHITE)
    nx = x0 + tw + 6
    d.ellipse([nx, 354, nx + 16, 370], fill=RED)
    d.text((nx + 5, 356), num, font=font(SANS_B, 11), fill=WHITE)
    d.text((nx + 22, 357), place, font=font(SANS_B, 10), fill=INK)
    y = 376
    for line in wrap(d, head, font(SERIF_B, 20), HW)[:2]:
        d.text((x0, y), line, font=font(SERIF_B, 20), fill=INK)
        y += 23
    y += 4
    for line in wrap(d, body, font(SANS, 11), HW)[:5]:
        d.text((x0, y), line, font=font(SANS, 11), fill=INK)
        y += 13
    d.text((x0, y + 2), src, font=font(SANS, 9), fill=(122, 46, 34))

# =====================================================================
# Secondary featured stories (4-11): two rows of four
# =====================================================================
secondary = [
    ("2", "KILLED", "Russian strike kills 2 in Odesa",
     "Strike hits cars and buildings; a Kyiv tower is ablaze after drone debris."),
    ("20", "STILL HELD", "Supermarket siege in Cartagena",
     "30 held at first, 10 freed; police negotiate as ~20 remain inside."),
    ("5%", "MAX FINES", "Australia passes duty of care",
     "Big tech faces fines up to 5% of global revenue; users 16+ can sue."),
    ("5", "CITIES", "Coalition hits Hodeidah",
     "Saudi-led strikes overnight after a Houthi drone hit a Riyadh tower."),
    ("2", "DEMANDS", "Qatar urges Hormuz reopened",
     "Doha calls for shipping routes restored and US\u2013Iran talks resumed."),
    ("2", "CANDIDATES", "VP deadline day in Indonesia",
     "Prabowo must name two VP candidates today; none confirmed yet."),
    ("4,000 kg", "EXPLOSIVES", "Army destroys explosives",
     "4,000 kg of unstable lead azide blown up at an Iowa plant today."),
    ("50", "JETS", "Xiamen orders 50 Boeing jets",
     "China Southern unit agrees to buy 50 Boeing 737-8 aircraft."),
]
SX = [12, 263, 514, 765]
for row in range(2):
    y0 = 508 + row * 100
    for col in range(4):
        num, cap, head, body = secondary[row * 4 + col]
        x0 = SX[col]
        nf = fit_size(d, num, SERIF_B, 22, 58)
        centered(d, y0 + 2, num, nf, x0=x0, x1=x0 + 58)
        centered(d, y0 + 30, cap, font(SANS_B, 8), x0=x0, x1=x0 + 58)
        tx = x0 + 66
        y = y0 + 2
        for line in wrap(d, head, font(SANS_B, 12), 177)[:2]:
            d.text((tx, y), line, font=font(SANS_B, 12), fill=INK)
            y += 15
        for line in wrap(d, body, font(SANS, 10), 177)[:3]:
            d.text((tx, y), line, font=font(SANS, 10), fill=INK)
            y += 12
    if row == 0:
        rule(d, 604, width=1)
for vx in (259, 510, 761):
    d.line([(vx, 508), (vx, 700)], fill=GREY, width=1)
rule(d, 702, width=1)

# =====================================================================
# Bottom: world map with numbered pins + ALSO list
# =====================================================================
# --- world map (left) ---
d.rectangle([12, 706, 352, 930], fill=SEA, outline=INK, width=1)
d.rectangle([12, 706, 352, 724], fill=INK)
d.text((18, 709), "WHERE IT HAPPENED", font=font(SANS_B, 11), fill=WHITE)
d.text((200, 710), "pins carry the story numbers",
       font=font(SANS, 9), fill=(200, 200, 200))
d.polygon([(28, 780), (40, 748), (70, 738), (105, 744), (118, 766),
           (108, 792), (88, 812), (64, 806), (44, 792), (30, 776)],
          fill=LAND, outline=(120, 100, 40))
d.polygon([(100, 838), (118, 832), (132, 846), (126, 876), (114, 898),
           (104, 872), (98, 852)], fill=LAND, outline=(120, 100, 40))
d.polygon([(168, 752), (184, 742), (198, 750), (194, 768), (180, 774),
           (170, 762)], fill=LAND, outline=(120, 100, 40))
d.polygon([(172, 792), (196, 786), (210, 800), (206, 830), (192, 852),
           (180, 830), (170, 808)], fill=LAND, outline=(120, 100, 40))
d.polygon([(204, 742), (258, 732), (306, 742), (320, 766), (298, 788),
           (268, 792), (240, 784), (216, 768), (206, 754)],
          fill=LAND, outline=(120, 100, 40))
d.polygon([(272, 868), (296, 862), (306, 880), (292, 894), (276, 886)],
          fill=LAND, outline=(120, 100, 40))
dot(d, 108, 732, r=3, fill=LAND)
dot(d, 172, 748, r=2, fill=LAND)
dot(d, 312, 772, r=2, fill=LAND)
dot(d, 316, 782, r=2, fill=LAND)

def pin(n, x, y, region):
    col = REGION[region]
    d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=col, outline=WHITE, width=1)
    t = str(n)
    f = font(SANS_B, 8 if n < 10 else 7)
    d.text((x - d.textlength(t, font=f) / 2, y - 5), t, font=f, fill=WHITE)

pins = [
    (1, 268, 762, "EUROPE"), (4, 232, 782, "EUROPE"),
    (12, 236, 790, "EUROPE"), (13, 228, 772, "EUROPE"),
    (14, 206, 752, "EUROPE"), (15, 242, 776, "EUROPE"),
    (7, 218, 828, "MIDDLE EAST"), (8, 232, 822, "MIDDLE EAST"),
    (16, 210, 806, "MIDDLE EAST"), (17, 222, 836, "MIDDLE EAST"),
    (18, 236, 812, "MIDDLE EAST"),
    (2, 302, 792, "ASIA"), (3, 288, 782, "ASIA"), (9, 292, 868, "ASIA"),
    (11, 304, 812, "ASIA"), (19, 266, 806, "ASIA"), (20, 276, 812, "ASIA"),
    (21, 268, 796, "ASIA"), (22, 302, 842, "ASIA"), (23, 300, 802, "ASIA"),
    (24, 200, 822, "AFRICA"), (25, 186, 824, "AFRICA"),
    (26, 192, 814, "AFRICA"), (27, 178, 848, "AFRICA"),
    (5, 78, 842, "AMERICAS"), (10, 58, 782, "AMERICAS"),
    (28, 88, 776, "AMERICAS"), (29, 68, 792, "AMERICAS"),
    (30, 42, 790, "AMERICAS"), (31, 90, 768, "AMERICAS"),
    (32, 94, 772, "AMERICAS"),
    (6, 318, 898, "OCEANIA"), (33, 310, 894, "OCEANIA"),
    (34, 290, 816, "GLOBAL"), (35, 150, 758, "GLOBAL"),
]
for n, x, y, region in pins:
    pin(n, x, y, region)

# --- ALSO list (right): 24 items in two columns ---
also = [
    "Zaporizhzhia toll rises: 2 killed, 44 wounded",
    "Dymer toll rises to 12 as rescued woman dies",
    "Latvia: invasion may hit tipping point in 2027",
    "Ukraine: 161 clashes in a day; 1,848 troops lost",
    "US envoy not certain Israel aid ends this year",
    "Britain sanctions Houthis and four officials",
    "Iran medicine shortage leaves patients hunting",
    "India: SP offers Congress 26 seats in UP polls",
    "Bangladesh launches mass typhoid vaccination",
    "Indian Army hunts scores missing after flood",
    "Mayon stays at Alert Level 3; 6 quakes",
    "Shanghai party pledges loyalty after Chen probe",
    "Libya: two soldiers die after Russian ship attack",
    "Libya frozen conflict risks fresh instability",
    "Erdo\u011fan plans first Libya trip in 15 years",
    "Cameroon separatist leader in Norway court",
    "Trump pardons turkeys Freedom and Feathers",
    "Police clear 12,000 from Don Toliver concert",
    "Thomas Markle formally charged in California",
    "ICE detains Princeton PhD student Eva Yi Xie",
    "US envoy: Australia law will limit free speech",
    "Australia apologises to LGBTQ veterans",
    "Laos graduates from least-developed status",
    "EU and Canada plan closer AI collaboration",
]
d.rectangle([360, 706, 1012, 724], fill=INK)
d.text((366, 709), "ALSO ON WEDNESDAY 25 NOV",
       font=font(SANS_B, 11), fill=WHITE)


def trim(d, text, f, max_w):
    if d.textlength(text, font=f) <= max_w:
        return text
    while text and d.textlength(text + "\u2026", font=f) > max_w:
        text = text[:-1]
    return text + "\u2026"


for k, item in enumerate(also):
    n = 12 + k
    col = 0 if k < 12 else 1
    x0 = 368 + col * 316
    y = 730 + (k % 12) * 17
    nf = font(SANS_B, 10)
    d.text((x0, y), f"{n}", font=nf, fill=RED)
    d.text((x0 + 22, y), trim(d, item, font(SANS, 10), 288),
           font=font(SANS, 10), fill=INK)

# =====================================================================
# DATE CHECK strip + footer
# =====================================================================
d.rectangle([12, 936, 1012, 988], outline=RED, width=2)
dc = ("DATE CHECK  Left out as other days' news \u2014 Tue 24 Nov: Houthi "
      "drone hits Riyadh tower, 11 hurt \u00b7 Huawei convicted in Brooklyn "
      "\u00b7 Chen Jining probe \u00b7 Senegal AFCON title restored \u00b7 "
      "Shein $100M FTC deal \u00b7 Baghdad takes Kurdish oilfields \u00b7 "
      "Malaysia to send 6,500 Rohingya back \u00b7 Hanoi blast kills 6 \u00b7 "
      "Dow tops 50,000. Mon 23 Nov: COP31 collapse \u00b7 Villavicencio "
      "car bomb. Sun 22 Nov: Merkury sunk; Dymer strike.")
y = 942
for line in wrap(d, dc, font(SANS, 10), 976)[:3]:
    if line.startswith("DATE CHECK"):
        d.text((20, y), "DATE CHECK", font=font(SANS_B, 10), fill=RED)
        d.text((20 + d.textlength("DATE CHECK  ", font=font(SANS_B, 10)), y),
               line[len("DATE CHECK  "):], font=font(SANS, 10), fill=INK)
    else:
        d.text((20, y), line, font=font(SANS, 10), fill=INK)
    y += 14

centered(d, 996,
         "Every story here happened or was first reported on Wednesday "
         "25 November 2026, as the named outlets reported it. Maps and "
         "drawings are original vector art.",
         font(SERIF_I, 10), fill=GREY)

# =====================================================================
# Save (deterministic: no timestamps, no randomness anywhere above)
# =====================================================================
import os
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print(f"wrote {out} ({os.path.getsize(out)} bytes, {img.size[0]}x{img.size[1]})")
