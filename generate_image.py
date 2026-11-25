#!/usr/bin/env python3
"""Draw a newspaper front page summing up Wednesday 25 November 2026.

Everything is drawn in code with Pillow: no photos, no external images.
Output: entry.png, 1024x1024, under 1 MiB.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (22, 22, 22)
RED = (163, 18, 18)
NAVY = (28, 61, 110)
BLUE = (43, 98, 168)
GOLD = (201, 148, 28)
GREY = (90, 90, 88)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, fnt, max_w):
    """Greedy word wrap by measured width."""
    lines, cur = [], ""
    for word in text.split():
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


def para(text, fnt, x, y, max_w, leading, color=INK):
    for line in wrap(text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(x0, y, x1, width=2, color=INK):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


def star(cx, cy, r, color):
    pts = []
    import math
    for i in range(10):
        ang = math.pi * i / 5 - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)


def flame(cx, base_y, h, w):
    d.polygon(
        [(cx - w, base_y), (cx - w * 0.4, base_y - h * 0.7),
         (cx, base_y - h), (cx + w * 0.4, base_y - h * 0.65),
         (cx + w, base_y)],
        fill=(232, 116, 24))
    d.polygon(
        [(cx - w * 0.55, base_y), (cx - w * 0.2, base_y - h * 0.45),
         (cx, base_y - h * 0.62), (cx + w * 0.2, base_y - h * 0.4),
         (cx + w * 0.55, base_y)],
        fill=(245, 196, 66))


# ---------------------------------------------------------------- masthead
d.text((W // 2, 26), "THE WORLD TODAY", font=font(SERIF_B, 62),
       fill=INK, anchor="ma")
rule(36, 104, W - 36, 3)
d.text((W // 2, 112), "WEDNESDAY, 25 NOVEMBER 2026",
       font=font(SANS_B, 30), fill=RED, anchor="ma")
d.text((W // 2, 148), "ONE DAY  •  ONE PAGE  •  SIX STORIES FROM AROUND THE GLOBE",
       font=font(SANS, 16), fill=GREY, anchor="ma")
rule(36, 178, W - 36, 2)

# ---------------------------------------------------------------- lead story
LX, LW = 36, 500
d.text((LX, 196), "STRAIT OF HORMUZ", font=font(SANS_B, 24), fill=RED)
y = 226
y = para("TANKERS HIT MINES IN HORMUZ",
         font(SERIF_B, 40), LX, y, LW, 48)
y += 8
y = para("Two oil tankers struck naval mines early on Wednesday and caught "
         "fire in the Strait of Hormuz, Iran's Revolutionary Guards Navy said.",
         font(SANS, 19), LX, y, LW, 26)
y += 8
y = para("The tankers were not named. It follows a string of attacks on "
         "shipping in the vital oil waterway.",
         font(SANS, 19), LX, y, LW, 26)

# Lead illustration: burning tankers at sea (code-drawn)
IX, IY, IW, IH = 560, 196, 428, 262
d.rectangle([IX, IY, IX + IW, IY + IH], outline=INK, width=3)
# sky
d.rectangle([IX + 3, IY + 3, IX + IW - 3, IY + 110], fill=(196, 220, 235))
d.ellipse([IX + 330, IY + 18, IX + 372, IY + 60], fill=(250, 226, 130))
# sea
d.rectangle([IX + 3, IY + 110, IX + IW - 3, IY + IH - 3], fill=(24, 74, 120))
for wx in range(IX + 20, IX + IW - 20, 46):
    d.arc([wx, IY + 150, wx + 34, IY + 168], 180, 360, fill=(210, 228, 240), width=3)
    d.arc([wx + 12, IY + 205, wx + 46, IY + 223], 180, 360, fill=(210, 228, 240), width=3)
# spiky mine in the water
mx, my = IX + 60, IY + 200
for ang in range(0, 360, 45):
    import math
    x2 = mx + 26 * math.cos(math.radians(ang))
    y2 = my + 26 * math.sin(math.radians(ang))
    d.line([(mx, my), (x2, y2)], fill=(30, 30, 30), width=4)
d.ellipse([mx - 15, my - 15, mx + 15, my + 15], fill=(30, 30, 30))
# tanker 1 (left, burning)
t1x, t1y = IX + 90, IY + 118
d.rectangle([t1x, t1y, t1x + 150, t1y + 34], fill=(18, 18, 18))
d.rectangle([t1x, t1y + 34, t1x + 150, t1y + 44], fill=(150, 30, 30))
d.rectangle([t1x + 105, t1y - 26, t1x + 135, t1y], fill=(240, 240, 235))
flame(t1x + 55, t1y, 52, 30)
flame(t1x + 95, t1y, 40, 22)
d.ellipse([t1x + 30, t1y - 78, t1x + 70, t1y - 38], fill=(120, 120, 118))
d.ellipse([t1x + 60, t1y - 96, t1x + 104, t1y - 52], fill=(150, 150, 148))
# tanker 2 (right, listing, smoke)
t2x, t2y = IX + 265, IY + 132
d.polygon([(t2x, t2y), (t2x + 140, t2y + 10), (t2x + 140, t2y + 40),
           (t2x, t2y + 34)], fill=(18, 18, 18))
d.polygon([(t2x, t2y + 34), (t2x + 140, t2y + 40), (t2x + 140, t2y + 48),
           (t2x, t2y + 42)], fill=(150, 30, 30))
d.rectangle([t2x + 18, t2y - 18, t2x + 44, t2y], fill=(240, 240, 235))
d.ellipse([t2x + 90, t2y - 62, t2x + 128, t2y - 24], fill=(120, 120, 118))
d.ellipse([t2x + 110, t2y - 84, t2x + 152, t2y - 42], fill=(150, 150, 148))
d.text((IX + IW // 2, IY + IH - 26), "THE STRAIT OF HORMUZ",
       font=font(SANS_B, 15), fill=(255, 255, 255), anchor="ma")

rule(36, 482, W - 36, 2)

# ---------------------------------------------------------------- middle row: two cards
def card(x, y, w, h, kicker, headline, body, art):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    d.text((x + 14, y + 10), kicker, font=font(SANS_B, 19), fill=RED)
    tw = w - 28 - 150  # text column left of the art panel
    yy = y + 38
    yy = para(headline, font(SERIF_B, 24), x + 14, yy, tw, 28)
    yy += 4
    para(body, font(SANS, 15), x + 14, yy, tw, 19)
    art(x, y, w, h)


def art_rocket(x, y, w, h):
    # night-sky panel at the top-right of the card
    px, py, pw, ph = x + w - 150, y + 12, 136, 118
    d.rectangle([px, py, px + pw, py + ph], fill=(16, 24, 54))
    for sx, sy, sr in [(px + 18, py + 18, 2), (px + 60, py + 12, 2),
                       (px + 105, py + 26, 3), (px + 30, py + 55, 2),
                       (px + 118, py + 70, 2), (px + 82, py + 44, 2)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 255, 255))
    # earth arc: a thin sliver at the very bottom of the panel
    d.ellipse([px, py + ph - 20, px + pw, py + ph + 40], fill=(43, 98, 168))
    d.ellipse([px, py + ph - 20, px + pw, py + ph + 40], outline=(120, 190, 230), width=2)
    # hide the part of the arc that spills below the panel, restore its edge
    d.rectangle([px, py + ph, px + pw, py + ph + 42], fill=PAPER)
    d.rectangle([px, py, px + pw, py + ph], outline=INK, width=2)
    # rocket (nose drawn after the body so it stays visible)
    rx = px + pw // 2
    d.rectangle([rx - 13, py + 44, rx + 13, py + 72], fill=(245, 245, 240))
    d.polygon([(rx - 13, py + 44), (rx + 13, py + 44), (rx, py + 28)], fill=(200, 40, 40))
    d.ellipse([rx - 6, py + 50, rx + 6, py + 62], fill=(43, 98, 168), outline=INK)
    d.polygon([(rx - 13, py + 60), (rx - 26, py + 78), (rx - 13, py + 72)], fill=(200, 40, 40))
    d.polygon([(rx + 13, py + 60), (rx + 26, py + 78), (rx + 13, py + 72)], fill=(200, 40, 40))
    d.polygon([(rx - 8, py + 72), (rx + 8, py + 72), (rx, py + 96)], fill=(245, 160, 40))


def art_treaty(x, y, w, h):
    px, py, pw, ph = x + w - 150, y + 12, 136, 118
    # document
    d.rectangle([px + 8, py + 6, px + pw - 8, py + ph - 6], fill=(255, 255, 255), outline=INK, width=2)
    for i, ly in enumerate(range(py + 22, py + 66, 12)):
        d.line([(px + 20, ly), (px + pw - 24, ly)], fill=(120, 120, 120), width=2)
    d.ellipse([px + pw // 2 - 16, py + 74, px + pw // 2 + 16, py + 106],
              fill=RED, outline=GOLD, width=3)
    # two small flags above the document corners
    d.rectangle([px + 2, py + 2, px + 42, py + 20], fill=NAVY, outline=INK)
    star(px + 22, py + 11, 6, (255, 255, 255))
    d.rectangle([px + pw - 42, py + 2, px + pw - 2, py + 20], fill=(0, 110, 80), outline=INK)
    d.polygon([(px + pw - 42, py + 20), (px + pw - 2, py + 2), (px + pw - 2, py + 20)],
              fill=(0, 90, 160))
    star(px + pw - 22, py + 11, 5, (245, 196, 66))


card(36, 498, 466, 216, "SPACE  •  CHINA",
     "Pakistan's first astronaut reaches orbit",
     "Shenzhou-24 docked with Tiangong about three hours after launching. "
     "Muhammad Zeeshan Ali, 40, is the first Pakistani in orbit.",
     art_rocket)
card(522, 498, 466, 216, "PACIFIC  •  CANBERRA",
     "Solomons sign landmark treaty with Australia",
     "Wale and Albanese signed a treaty making Australia the Solomons' "
     "'primary security partner' — no foreign base, A$740m over a decade.",
     art_treaty)

# ---------------------------------------------------------------- bottom row: three cards
def mini(x, y, w, h, kicker, headline, body, art):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    d.text((x + 12, y + 9), kicker, font=font(SANS_B, 16), fill=RED)
    yy = para(headline, font(SERIF_B, 22), x + 12, y + 32, w - 24, 26)
    yy += 2
    para(body, font(SANS, 15), x + 12, yy, w - 24, 20)
    art(x, y, w, h)


def art_ukraine(x, y, w, h):
    by = y + h - 30
    d.rectangle([x + 2, by, x + w - 2, by + 14], fill=(43, 98, 168))
    d.rectangle([x + 2, by + 14, x + w - 2, y + h - 2], fill=(245, 196, 66))
    star(x + w - 26, by + 14, 7, (200, 40, 40))


def art_gaza(x, y, w, h):
    by = y + h - 30
    d.rectangle([x + 2, by, x + w - 2, y + h - 2], fill=(232, 190, 150))
    for bx, bh in [(x + 14, 16), (x + 40, 22), (x + 68, 13), (x + 200, 18), (x + 232, 14)]:
        d.rectangle([bx, y + h - 2 - bh, bx + 20, y + h - 2], fill=(70, 60, 55))


def art_merz(x, y, w, h):
    by = y + h - 30
    d.rectangle([x + 2, by, x + w - 2, by + 9], fill=(20, 20, 20))
    d.rectangle([x + 2, by + 9, x + w - 2, by + 18], fill=(200, 40, 40))
    d.rectangle([x + 2, by + 18, x + w - 2, y + h - 2], fill=(245, 196, 66))


mini(36, 726, 300, 210, "UKRAINE",
     "Overnight strikes kill 3, wound 15",
     "A drone hit a bus in Kharkiv, killing one and injuring seven. "
     "One more died near Kyiv.",
     art_ukraine)
mini(362, 726, 300, 210, "GAZA",
     "Strike kills Hamas security chief and family",
     "A pre-dawn strike killed Muhammad Abu al-Awf, 47, his wife and two "
     "daughters, 13 and 15.",
     art_gaza)
mini(688, 726, 300, 210, "GERMANY",
     "Merz: Europe will 'show Russia its limits'",
     "Merz defended a 2027 defence budget of €139.4bn, up €31.2bn: "
     "'Russia wants more than Ukraine.'",
     art_merz)

# ---------------------------------------------------------------- ticker
d.rectangle([0, 946, W, H], fill=(22, 22, 22))
ticker = "HORMUZ: 2 TANKERS HIT MINES  •  SHENZHOU-24 DOCKS  •  SOLOMONS TREATY SIGNED  •  KYIV: 3 KILLED OVERNIGHT"
tsize = 17
while d.textlength(ticker, font=font(SANS_B, tsize)) > W - 40 and tsize > 10:
    tsize -= 1
d.text((W // 2, 962), ticker, font=font(SANS_B, tsize), fill=(255, 255, 255), anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png")
