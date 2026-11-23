"""Front-page image engine for news-image-20261123.

Pure-stdlib drawing: a small RGB canvas, a 5x7 pixel font, a handful of
shape primitives and a minimal PNG encoder (zlib + struct, filter 0).
No network, no clock, no randomness: the same data always renders the
same bytes, so repeated runs are byte-identical.

Layout (1024 x 1024): masthead, hero (COP31 collapse), two-card row A
(NATO council / peace plan), three-card row B (markets / Sparta II /
Mexico), Iran band, two-line ticker.
"""

import math
import struct
import zlib

W = 1024
H = 1024

# ---------------------------------------------------------------- font: 5x7
# Each glyph is 7 rows of 5 bits, "1" = ink. Uppercase + digits + the
# punctuation the front page needs. Anything unknown renders blank.

FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "\u2014": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "\u2022": ("00000", "00000", "01100", "01100", "01100", "00000", "00000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "*": ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    ">": ("10000", "01000", "00100", "00010", "00100", "01000", "10000"),
    "<": ("00001", "00010", "00100", "01000", "00100", "00010", "00001"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "@": ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
}

BLANK = ("00000",) * 7
CHAR_W = 5
CHAR_H = 7


def text_width(text, scale):
    """Pixel width of text at the given scale (1px gap between glyphs)."""
    n = len(text)
    if n == 0:
        return 0
    return n * (CHAR_W * scale + scale) - scale


def wrap_text(text, max_width, scale):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    for raw in text.split("\n"):
        words = raw.split(" ")
        line = ""
        for word in words:
            trial = word if not line else line + " " + word
            if text_width(trial, scale) <= max_width or not line:
                line = trial
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


# ------------------------------------------------------------------ canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def _idx(self, x, y):
        return (y * self.w + x) * 3

    def set_pixel(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = self._idx(x, y)
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            i = self._idx(x0, yy)
            self.px[i:i + len(row)] = row

    def outline_rect(self, x, y, w, h, color, t=1):
        self.fill_rect(x, y, w, t, color)
        self.fill_rect(x, y + h - t, w, t, color)
        self.fill_rect(x, y, t, h, color)
        self.fill_rect(x + w - t, y, t, h, color)

    def hline(self, x, y, length, color, t=1):
        self.fill_rect(x, y, length, t, color)

    def vline(self, x, y, length, color, t=1):
        self.fill_rect(x, y, t, length, color)

    def line(self, x0, y0, x1, y1, color, t=1):
        """Bresenham line; thickness t draws a small square brush."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            self.fill_rect(x - t // 2, y - t // 2, t, t, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def polyline(self, points, color, t=1):
        for (ax, ay), (bx, by) in zip(points, points[1:]):
            self.line(ax, ay, bx, by, color, t)

    def fill_circle(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            half = int(math.sqrt(max(0, r * r - dy * dy)))
            self.fill_rect(cx - half, cy + dy, half * 2 + 1, 1, color)

    def circle(self, cx, cy, r, color, t=1):
        for rr in range(r - t + 1, r + 1):
            x = 0
            y = rr
            d = 1 - rr
            while x <= y:
                for px, py in ((cx + x, cy + y), (cx - x, cy + y),
                               (cx + x, cy - y), (cx - x, cy - y),
                               (cx + y, cy + x), (cx - y, cy + x),
                               (cx + y, cy - x), (cx - y, cy - x)):
                    self.set_pixel(px, py, color)
                if d < 0:
                    d += 2 * x + 3
                else:
                    d += 2 * (x - y) + 5
                    y -= 1
                x += 1

    def fill_poly(self, points, color):
        """Scanline polygon fill (even-odd)."""
        if len(points) < 3:
            return
        ys = [p[1] for p in points]
        for y in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            n = len(points)
            for i in range(n):
                (x0, y0), (x1, y1) = points[i], points[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
                    xs.append(x)
            xs.sort()
            for j in range(0, len(xs) - 1, 2):
                xa = max(0, int(math.ceil(xs[j])))
                xb = min(self.w - 1, int(math.floor(xs[j + 1])))
                if xb >= xa:
                    self.fill_rect(xa, y, xb - xa + 1, 1, color)

    def star(self, cx, cy, r_outer, r_inner, color):
        pts = []
        for k in range(10):
            r = r_outer if k % 2 == 0 else r_inner
            ang = -math.pi / 2 + k * math.pi / 5
            pts.append((int(cx + r * math.cos(ang)),
                        int(cy + r * math.sin(ang))))
        self.fill_poly(pts, color)

    # ------------------------------------------------------------- text
    def draw_glyph(self, ch, x, y, scale, color):
        glyph = FONT.get(ch, BLANK)
        for row_i, row in enumerate(glyph):
            for col_i, bit in enumerate(row):
                if bit == "1":
                    self.fill_rect(x + col_i * scale, y + row_i * scale,
                                   scale, scale, color)

    def draw_text(self, text, x, y, scale, color):
        text = text.upper()
        cx = x
        for ch in text:
            self.draw_glyph(ch, cx, y, scale, color)
            cx += (CHAR_W + 1) * scale
        return cx - x - scale if text else 0

    def draw_text_centered(self, text, cx, y, scale, color):
        w = text_width(text.upper(), scale)
        self.draw_text(text, cx - w // 2, y, scale, color)
        return w

    def draw_text_block(self, text, x, y, max_width, scale, color,
                        line_gap=4):
        lines = wrap_text(text, max_width, scale)
        for i, ln in enumerate(lines):
            self.draw_text(ln, x, y + i * (CHAR_H * scale + line_gap),
                           scale, color)
        return len(lines)


# -------------------------------------------------------------------- PNG
def encode_png(canvas):
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)  # filter: none
        start = y * stride
        raw += canvas.px[start:start + stride]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", comp) + chunk(b"IEND", b""))


# ------------------------------------------------------------------ layout
CREAM = (245, 239, 224)
PAPER = (253, 251, 245)
INK = (24, 24, 24)
GREY = (64, 64, 64)
DARK = (30, 30, 30)
HERO_BG = (28, 44, 38)
YELLOW = (242, 197, 49)
DIM_YELLOW = (201, 162, 39)
WHITE = (255, 255, 255)
BAND_RED = (110, 31, 26)
TICKER_BG = (26, 26, 26)
GLOBE_SEA = (58, 110, 82)
GLOBE_LAND = (34, 74, 52)


def _card(c, x, y, w, h, accent):
    c.fill_rect(x, y, w, h, PAPER)
    c.outline_rect(x, y, w, h, DARK, 2)
    c.fill_rect(x, y, w, 8, accent)


def _draw_chart(c, x0, y0):
    c.hline(x0, y0 + 42, 296, (180, 180, 170), 2)
    c.vline(x0, y0, 42, (180, 180, 170), 2)
    pts = [(x0 + 12, y0 + 8), (x0 + 66, y0 + 14), (x0 + 116, y0 + 6),
           (x0 + 166, y0 + 22), (x0 + 216, y0 + 28), (x0 + 266, y0 + 40)]
    c.polyline(pts, (178, 44, 44), 3)
    for px, py in pts:
        c.fill_circle(px, py, 3, (178, 44, 44))


def _draw_ship(c, x0, y0):
    # hull + containers + flame + smoke, centred on x0
    c.fill_poly([(x0 - 68, y0 + 24), (x0 + 68, y0 + 24),
                 (x0 + 52, y0 + 40), (x0 - 52, y0 + 40)], (58, 58, 58))
    for dx, col in ((-48, (140, 60, 50)), (-20, (60, 90, 120)),
                    (8, (90, 110, 60))):
        c.fill_rect(x0 + dx, y0 + 10, 24, 14, col)
    c.fill_poly([(x0 - 12, y0 + 10), (x0, y0 - 8), (x0 + 12, y0 + 10)],
                (232, 120, 40))
    c.fill_poly([(x0 - 6, y0 + 10), (x0, y0 - 2), (x0 + 6, y0 + 10)],
                (242, 197, 49))


def render(data):
    c = Canvas(W, H, CREAM)
    mh = data["masthead"]

    # ---------------------------------------------------------- masthead
    c.draw_text_centered(mh["title"], W // 2, 14, 6, INK)
    c.draw_text_centered(mh["date"], W // 2, 62, 3, INK)
    c.draw_text_centered(mh["kicker"], W // 2, 88, 2, GREY)
    c.fill_rect(0, 106, W, 2, DARK)

    # -------------------------------------------------------------- hero
    hero = data["hero"]
    c.fill_rect(0, 108, W, 352, HERO_BG)
    c.draw_text(hero["label"], 32, 122, 2, YELLOW)
    c.draw_text(hero["line1"], 32, 146, 7, WHITE)
    c.draw_text(hero["line2"], 32, 206, 7, YELLOW)
    for i, sub in enumerate(hero["subs"]):
        y = 272 + i * 20
        c.fill_rect(32, y + 3, 8, 8, YELLOW)
        c.draw_text(sub, 48, y, 2, WHITE)
    # cracked globe + dim sun, right side
    c.fill_circle(800, 258, 105, GLOBE_SEA)
    c.fill_poly([(740, 200), (790, 190), (810, 220), (780, 250),
                 (745, 240)], GLOBE_LAND)
    c.fill_poly([(820, 280), (860, 270), (875, 300), (840, 320),
                 (815, 305)], GLOBE_LAND)
    c.fill_poly([(760, 300), (790, 295), (800, 320), (770, 325)],
                GLOBE_LAND)
    c.circle(800, 258, 105, (20, 30, 26), 3)
    c.polyline([(762, 168), (792, 196), (772, 228), (806, 256),
                (782, 292), (812, 330), (796, 356)], YELLOW, 4)
    c.fill_circle(918, 166, 26, DIM_YELLOW)
    for k in range(8):
        ang = k * math.pi / 4
        c.line(int(918 + 32 * math.cos(ang)), int(166 + 32 * math.sin(ang)),
               int(918 + 42 * math.cos(ang)), int(166 + 42 * math.sin(ang)),
               DIM_YELLOW, 3)
    # strip
    c.fill_rect(0, 420, W, 32, YELLOW)
    c.draw_text_centered(hero["strip"], W // 2, 428, 3, HERO_BG)

    # ------------------------------------------------------------- row A
    for card, x in zip(data["row_a"], (8, 516)):
        accent = card["accent"]
        _card(c, x, 460, 500, 168, accent)
        c.draw_text(card["kicker"], x + 20, 478, 2, accent)
        c.draw_text(card["head"][0], x + 20, 500, 4, INK)
        c.draw_text(card["head"][1], x + 20, 530, 4, INK)
        for i, sub in enumerate(card["subs"]):
            c.draw_text(sub, x + 20, 566 + i * 20, 2, GREY)
    # small shield on the NATO card, top right
    c.polyline([(468, 482), (496, 482), (496, 502), (482, 518),
                (468, 502), (468, 482)], (31, 78, 121), 2)
    c.fill_poly([(482, 488), (486, 496), (482, 504), (478, 496)],
                (31, 78, 121))

    # ------------------------------------------------------------- row B
    for card, x, w in zip(data["row_b"], (8, 344, 680), (328, 328, 336)):
        accent = card["accent"]
        _card(c, x, 628, w, 168, accent)
        c.draw_text(card["kicker"], x + 16, 646, 2, accent)
        c.draw_text(card["head"], x + 16, 670, 3, INK)
        for i, sub in enumerate(card["subs"]):
            c.draw_text(sub, x + 16, 702 + i * 20, 2, GREY)
        if card["graphic"] == "chart":
            _draw_chart(c, x + 16, 742)
        elif card["graphic"] == "ship":
            _draw_ship(c, x + w // 2, 748)
        elif card["graphic"] == "star":
            c.star(x + w // 2, 766, 24, 10, DIM_YELLOW)

    # ------------------------------------------------------------ Iran band
    band = data["band"]
    c.fill_rect(0, 796, W, 92, BAND_RED)
    c.draw_text_centered(band["line1"], W // 2, 812, 4, WHITE)
    c.draw_text_centered(band["line2"], W // 2, 856, 2, (232, 220, 210))

    # -------------------------------------------------------------- ticker
    c.fill_rect(0, 888, W, 136, TICKER_BG)
    c.fill_rect(0, 888, W, 3, YELLOW)
    c.draw_text_centered(data["ticker"][0], W // 2, 918, 3, WHITE)
    c.draw_text_centered(data["ticker"][1], W // 2, 964, 3, WHITE)

    return c
