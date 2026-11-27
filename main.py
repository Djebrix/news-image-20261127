#!/usr/bin/env python3
"""THE WORLD IN ONE DAY - Friday, 27 November 2026.

A newspaper front page drawn with pure stdlib Python. No fonts, no
images, no network: every pixel is computed here and encoded to PNG
with zlib (stdlib). Deterministic: same input, same bytes, every run.
"""
import os
import struct
import zlib

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (18, 18, 18)
RED = (178, 34, 34)
BLUE = (28, 68, 128)
GREY = (110, 105, 95)
LIGHT = (232, 226, 212)
GOLD = (176, 132, 30)

# ---------------------------------------------------------------- 5x7 font
# Each glyph: 7 strings of 5 chars, '#' = ink.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '$': ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    '*': ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    '|': ("00100", "00100", "00100", "00100", "00100", "00100", "00100"),
}


def glyph(ch):
    return FONT.get(ch.upper(), FONT['?'])


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def put(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.put(xx, yy, c)

    def hline(self, x, y, w, c, t=1):
        self.rect(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.rect(x, y, t, h, c)

    def line(self, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.put(x0, y0, c)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c, fill=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill and d <= r * r:
                    self.put(xx, yy, c)
                elif not fill and abs(d - r * r) <= r:
                    self.put(xx, yy, c)

    def text(self, x, y, s, scale, c):
        cx = x
        for ch in s:
            g = glyph(ch)
            for row in range(7):
                for col in range(5):
                    if g[row][col] == '1':
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, c)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale):
        return len(s) * 6 * scale - scale

    def centre(self, y, s, scale, c, x0=0, x1=None):
        x1 = self.w if x1 is None else x1
        w = self.text_w(s, scale)
        self.text(x0 + (x1 - x0 - w) // 2, y, s, scale, c)

    def wrap(self, x, y, s, scale, c, max_w, lh=None):
        lh = lh or 9 * scale
        words, line, yy = s.split(), "", y
        for wd in words:
            trial = (line + " " + wd).strip()
            if self.text_w(trial, scale) <= max_w or not line:
                line = trial
            else:
                self.text(x, yy, line, scale, c)
                yy += lh
                line = wd
        if line:
            self.text(x, yy, line, scale, c)
        return yy + lh


# ---------------------------------------------------------------- pictograms
def pic_drone(cv, x, y, s, c):
    # quadcopter silhouette over a blast star
    cv.rect(x + 8 * s // 10, y + 4 * s // 10, 14 * s // 10, 3 * s // 10, c)
    for dx in (-2, 16):
        cv.circle(x + dx * s // 10 + 2 * s // 10, y + 4 * s // 10, 3 * s // 10, c)
        cv.hline(x + (dx - 3) * s // 10, y + 2 * s // 10, 10 * s // 10, c, 2)
    for dx, dy in ((-3, 9), (22, 9), (4, 12), (15, 12), (9, 15)):
        cv.line(x + 10 * s // 10, y + 6 * s // 10,
                x + dx * s // 10, y + dy * s // 10, RED)


def pic_storm(cv, x, y, s, c):
    cv.circle(x + 8 * s // 10, y + 5 * s // 10, 6 * s // 10, c)
    cv.circle(x + 16 * s // 10, y + 4 * s // 10, 7 * s // 10, c)
    cv.circle(x + 23 * s // 10, y + 6 * s // 10, 5 * s // 10, c)
    cv.rect(x + 3 * s // 10, y + 6 * s // 10, 24 * s // 10, 5 * s // 10, c)
    for dx in (4, 11, 18, 25):
        cv.line(x + dx * s // 10, y + 13 * s // 10,
                x + (dx - 2) * s // 10, y + 19 * s // 10, BLUE)


def pic_chess(cv, x, y, s, c):
    for r in range(4):
        for col in range(4):
            if (r + col) % 2 == 0:
                cv.rect(x + col * 7 * s // 10, y + r * 7 * s // 10,
                        7 * s // 10, 7 * s // 10, c)
    cv.rect(x + 2 * s // 10, y - 6 * s // 10, 5 * s // 10, 6 * s // 10, RED)
    cv.rect(x + 21 * s // 10, y + 22 * s // 10, 5 * s // 10, 6 * s // 10, BLUE)


def pic_blast(cv, x, y, s, c):
    cx, cy = x + 14 * s // 10, y + 12 * s // 10
    for dx, dy in ((0, -12), (9, -9), (12, 0), (9, 9), (0, 12),
                   (-9, 9), (-12, 0), (-9, -9), (4, -11), (-4, 11)):
        cv.line(cx, cy, cx + dx * s // 10, cy + dy * s // 10, RED)
    cv.circle(cx, cy, 5 * s // 10, GOLD)


def pic_parliament(cv, x, y, s, c):
    cv.rect(x + 2 * s // 10, y + 2 * s // 10, 24 * s // 10, 4 * s // 10, c)
    for i in range(5):
        cv.rect(x + (3 + i * 5) * s // 10, y + 6 * s // 10, 2 * s // 10,
                12 * s // 10, c)
    cv.rect(x + 1 * s // 10, y + 18 * s // 10, 26 * s // 10, 3 * s // 10, c)
    cv.rect(x + 11 * s // 10, y - 4 * s // 10, 6 * s // 10, 6 * s // 10, RED)


def pic_chart(cv, x, y, s, c):
    cv.hline(x, y + 20 * s // 10, 28 * s // 10, c, 2)
    cv.vline(x, y, 20 * s // 10, c, 2)
    pts = [(2, 17), (8, 14), (13, 15), (18, 8), (24, 3)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        cv.line(x + ax * s // 10, y + ay * s // 10,
                x + bx * s // 10, y + by * s // 10, (34, 139, 34))
    cv.line(x + 24 * s // 10, y + 3 * s // 10, x + 20 * s // 10,
            y + 3 * s // 10, (34, 139, 34))
    cv.line(x + 24 * s // 10, y + 3 * s // 10, x + 24 * s // 10,
            y + 7 * s // 10, (34, 139, 34))


def pic_tower(cv, x, y, s, c):
    cv.rect(x + 4 * s // 10, y + 8 * s // 10, 6 * s // 10, 13 * s // 10, c)
    cv.rect(x + 14 * s // 10, y + 4 * s // 10, 8 * s // 10, 17 * s // 10, c)
    cv.rect(x + 22 * s // 10, y + 12 * s // 10, 5 * s // 10, 9 * s // 10, c)
    for dx, dy in ((7, -4), (10, -7), (6, -8)):
        cv.line(x + dx * s // 10, y + 4 * s // 10,
                x + (dx + 2) * s // 10, y + dy * s // 10, RED)
    cv.circle(x + 8 * s // 10, y + 2 * s // 10, 2 * s // 10, GOLD)


def pic_stars(cv, x, y, s, c):
    import math
    cx, cy, r = x + 14 * s // 10, y + 11 * s // 10, 10 * s // 10
    for i in range(12):
        a = 2 * math.pi * i / 12 - math.pi / 2
        cv.circle(int(cx + r * math.cos(a)), int(cy + r * math.sin(a)),
                  2 * s // 10, GOLD)
    cv.rect(x + 9 * s // 10, y + 8 * s // 10, 10 * s // 10, 6 * s // 10, BLUE)


def pic_drone_small(cv, x, y, s, c):
    pic_drone(cv, x, y, s, c)


PICS = {
    'drone': pic_drone, 'storm': pic_storm, 'chess': pic_chess,
    'blast': pic_blast, 'parliament': pic_parliament, 'chart': pic_chart,
    'tower': pic_tower, 'stars': pic_stars, 'drone2': pic_drone_small,
}

# ---------------------------------------------------------------- stories
# (kicker, headline, body, pictogram) — all verified 27 Nov 2026.
STORIES = [
    ("GULF CRISIS",
     "DRONE STRIKE IN KUWAIT KILLS TWO ITALIANS",
     "Two Rheinmetall technicians died at a Kuwaiti air-defence station. "
     "Kuwait and Italy blame Iran; Tehran denies any role.",
     "drone"),
    ("USA",
     "THANKSGIVING STORM CUTS POWER TO 900,000",
     "A nor'easter flooded the Northeast, forced the first-ever postponement "
     "of the Macy's parade and cancelled 400+ flights.",
     "storm"),
    ("UKRAINE",
     "RUSSIA FIRES 155 DRONES OVERNIGHT",
     "Kyiv says 110 were downed, with hits at 27 sites. Zelensky tells the "
     "BBC the US is too focused on the Middle East.",
     "drone2"),
    ("GAZA",
     "ISRAELI STRIKES KILL NINE IN GAZA",
     "Among the dead is a Hamas-appointed deputy education minister. Israel's "
     "defence minister threatens a new offensive.",
     "blast"),
    ("EUROPE",
     "EU SUMMIT ENDS WITH NO DEAL ON 45BN LOAN",
     "Leaders split over Ukraine funding and the long-term budget. Germany "
     "threatens a veto; a decision slips to December.",
     "stars"),
    ("NEW ZEALAND",
     "HUNG PARLIAMENT: 65-65 DEADLOCK",
     "The final count strips Luxon's coalition of its majority. Newcomer "
     "Opportunity, with 7 seats, now holds the balance.",
     "parliament"),
    ("MARKETS",
     "CHINA STOCKS SOAR IN BEST DAY IN 2 YEARS",
     "Shanghai +3.7%, CSI 300 +4.2%, STAR 50 +15% after Beijing vows stronger "
     "state support for the market.",
     "chart"),
    ("THAILAND",
     "BANGKOK REFINERY BLAST INJURES NINE",
     "An explosion at Bangchak's Phra Khanong plant sent black smoke over the "
     "city. Production is shut; three are critical.",
     "tower"),
    ("CHESS",
     "GUKESH-SINDAROV: GAME 3 DRAWN IN 60 MOVES",
     "A marathon third game in Geneva ends level. The world title match "
     "stands at 1.5-1.5; Game 4 is on Saturday.",
     "chess"),
]


def draw_page(cv):
    cv.rect(0, 0, W, H, PAPER)
    cv.rect(0, 0, W, 6, RED)
    # masthead
    cv.centre(26, "THE WORLD IN ONE DAY", 7, INK)
    cv.hline(48, 108, W - 96, INK, 3)
    cv.centre(122, "FRIDAY, 27 NOVEMBER 2026", 3, RED)
    cv.centre(152, "NINE STORIES FROM ONE DAY ON EARTH", 2, GREY)
    cv.hline(48, 182, W - 96, INK, 2)

    # lead story, full width
    lx, ly, lw = 48, 200, W - 96
    cv.rect(lx, ly, lw, 196, LIGHT)
    cv.rect(lx, ly, lw, 196, INK)  # border via thin frame below
    cv.rect(lx + 2, ly + 2, lw - 4, 192, LIGHT)
    k, h, b, pic = STORIES[0]
    cv.text(lx + 20, ly + 16, "LEAD  |  " + k, 2, RED)
    cv.wrap(lx + 20, ly + 44, h, 4, INK, 560, lh=38)
    cv.wrap(lx + 20, ly + 128, b, 2, INK, 560, lh=20)
    PICS[pic](cv, lx + 640, ly + 34, 8, INK)
    cv.text(lx + 640, ly + 168, "KUWAIT  |  2 DEAD", 2, RED)

    # grid: remaining 8 stories, 2 columns x 4 rows
    gx, gy = 48, 420
    cw, ch, gap = 452, 130, 24
    for i, (k, h, b, pic) in enumerate(STORIES[1:]):
        x = gx + (i % 2) * (cw + gap)
        y = gy + (i // 2) * (ch + 10)
        cv.rect(x, y, cw, ch, PAPER)
        cv.hline(x, y, cw, INK, 2)
        cv.text(x + 8, y + 10, k, 2, RED)
        cv.wrap(x + 8, y + 34, h, 2, INK, 330, lh=20)
        cv.wrap(x + 8, y + 78, b, 1, INK, 330, lh=13)
        PICS[pic](cv, x + 352, y + 36, 9, INK)

    # footer
    fy = 420 + 4 * 130 + 3 * 10 + 12
    cv.hline(48, fy, W - 96, INK, 2)
    cv.centre(fy + 10, "SOURCES: UPI - REUTERS - BBC - AAP - CHEMORBIS - SPORTSKEEDA", 1, GREY)


def png_bytes(cv):
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * stride:(y + 1) * stride]

    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    cv = Canvas(W, H, PAPER)
    draw_page(cv)
    data = png_bytes(cv)
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print(f"wrote {path} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
