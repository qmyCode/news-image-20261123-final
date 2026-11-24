"""Illustrated scenes: 3 mains + 12 cards. Every scene = layered background, 2+ subjects, data layer."""
import math

from gfx import ellipse_pts

WHITE = (255, 255, 255)
INK = (16, 28, 52)
RED = (190, 36, 36)
GREEN = (30, 150, 70)
GOLD = (232, 182, 40)
FIRE = (255, 140, 30)
WARM = (250, 205, 100)


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t + 0.5) for i in range(3))


class Off:
    """Drawing proxy with an origin offset and a clip rectangle."""

    def __init__(self, c, x, y, w, h, ty=0):
        c.clip(x, y, x + w, y + h)
        self.c, self.x, self.y, self.w, self.h = c, x, y + ty, w, h - ty
        self.seed = 12345

    def rnd(self):
        self.seed = (self.seed * 1103515245 + 12345) & 0x7FFFFFFF
        return self.seed / 0x7FFFFFFF

    def done(self):
        self.c.unclip()

    def rect(self, x0, y0, x1, y1, col, a=1.0):
        self.c.rect(self.x + x0, self.y + y0, self.x + x1, self.y + y1, col, a)

    def vgrad(self, x0, y0, x1, y1, c0, c1):
        self.c.vgrad(self.x + x0, self.y + y0, self.x + x1, self.y + y1, c0, c1)

    def frame(self, x0, y0, x1, y1, col, t=1, a=1.0):
        self.c.frame(self.x + x0, self.y + y0, self.x + x1, self.y + y1, col, t, a)

    def poly(self, pts, col, a=1.0):
        self.c.poly([(self.x + p[0], self.y + p[1]) for p in pts], col, a)

    def circle(self, cx, cy, r, col, a=1.0):
        self.c.circle(self.x + cx, self.y + cy, r, col, a)

    def ellipse(self, cx, cy, rx, ry, col, a=1.0):
        self.c.ellipse(self.x + cx, self.y + cy, rx, ry, col, a)

    def ring(self, cx, cy, r, t, col, a=1.0):
        self.c.ring(self.x + cx, self.y + cy, r, t, col, a)

    def arc(self, cx, cy, r, a0, a1, t, col, a=1.0):
        self.c.arc(self.x + cx, self.y + cy, r, a0, a1, t, col, a)

    def line(self, x0, y0, x1, y1, t, col, a=1.0):
        self.c.line(self.x + x0, self.y + y0, self.x + x1, self.y + y1, t, col, a)

    def dline(self, x0, y0, x1, y1, t, col, a=1.0, dash=4, gap=3):
        self.c.dline(self.x + x0, self.y + y0, self.x + x1, self.y + y1, t, col, a, dash, gap)

    def polyline(self, pts, t, col, a=1.0):
        self.c.polyline([(self.x + p[0], self.y + p[1]) for p in pts], t, col, a)

    def glow(self, cx, cy, r, col, a=0.5):
        self.c.glow(self.x + cx, self.y + cy, r, col, a)

    def cone(self, x, y, tx0, tx1, ty, col, a=0.2):
        self.c.cone(self.x + x, self.y + y, self.x + tx0, self.x + tx1, self.y + ty, col, a)

    def text(self, x, y, s, font, size, col, anchor="l", a=1.0, sp=0.0):
        return self.c.text(self.x + x, self.y + y, s, font, size, col, anchor, a, sp)

    def label(self, x, y, s, font, size, fg, bg, pad=2, anchor="l", a=1.0):
        w = self.c.tw(s, font, size)
        x0 = x if anchor == "l" else (x - w / 2 if anchor == "c" else x - w)
        self.rect(x0 - pad, y - size - pad + 1, x0 + w + pad, y + pad + 1, bg, a)
        self.text(x0, y, s, font, size, fg)

    def stars(self, n, x0, y0, x1, y1, col=(255, 255, 240)):
        for _ in range(n):
            sx = x0 + self.rnd() * (x1 - x0)
            sy = y0 + self.rnd() * (y1 - y0)
            self.rect(sx, sy, sx + 1 + (self.rnd() > 0.85), sy + 1, col, 0.4 + 0.5 * self.rnd())

    def windows(self, x0, y0, cols, rows, dx, dy, ww, wh, lit, dark, p=0.55):
        for r in range(rows):
            for k in range(cols):
                col = lit if self.rnd() < p else dark
                self.rect(x0 + k * dx, y0 + r * dy, x0 + k * dx + ww, y0 + r * dy + wh, col)

    def person(self, x, y, s, body, head=(240, 200, 160), helmet=None):
        """Small standing figure, feet at (x, y)."""
        self.rect(x - 1.2 * s, y - 7 * s, x + 1.2 * s, y, body)
        self.rect(x - 1.8 * s, y - 7.5 * s, x + 1.8 * s, y - 4.5 * s, body)
        self.circle(x, y - 9 * s, 1.5 * s, head)
        if helmet:
            self.poly([(x - 1.8 * s, y - 9.3 * s), (x, y - 11.6 * s), (x + 1.8 * s, y - 9.3 * s)], helmet)


def flag3(o, x, y, w, h, cols, vert=False):
    n = len(cols)
    for i, col in enumerate(cols):
        if vert:
            o.rect(x + w * i / n, y, x + w * (i + 1) / n, y + h, col)
        else:
            o.rect(x, y + h * i / n, x + w, y + h * (i + 1) / n, col)


def drone(o, x, y, s=1.0, col=(20, 20, 26)):
    o.poly([(x, y), (x - 9 * s, y + 4 * s), (x - 7 * s, y + 5.5 * s), (x + 2 * s, y + 2 * s)], col)
    o.poly([(x, y), (x - 9 * s, y - 4 * s), (x - 7 * s, y - 5.5 * s), (x + 2 * s, y - 2 * s)], col)
    o.rect(x - 8 * s, y - 1 * s, x + 4 * s, y + 1 * s, col)
    o.glow(x - 9 * s, y, 4 * s, (255, 120, 40), 0.7)


# ====================================================================== MAINS
def scene_kyiv(o):
    w, h = o.w, o.h
    o.vgrad(0, 0, w, 92, (6, 10, 30), (70, 34, 60))
    o.stars(34, 0, 14, w, 60)
    o.glow(292, 34, 18, (230, 226, 190), 0.5)
    o.circle(292, 34, 7, (236, 232, 205))
    o.circle(295, 32, 6, (14, 18, 42), 0.35)
    # distant skyline with lit windows
    for bx, bw, bh in [(0, 30, 30), (30, 24, 40), (54, 34, 26), (232, 30, 34), (262, 26, 46), (288, 36, 30)]:
        o.rect(bx, 92 - bh, bx + bw, 94, (26, 28, 58))
        o.windows(bx + 3, 92 - bh + 4, max(1, bw // 7), bh // 9, 7, 9, 3, 4, (240, 200, 100), (30, 34, 66), 0.35)
    # ground / street
    o.rect(0, 94, w, h, (14, 15, 26))
    o.rect(0, 100, w, 102, (50, 46, 60))
    o.dline(0, 111, w, 111, 1, (110, 100, 80), 0.6, 8, 8)
    # Vyshneve supermarket (left) - smoking, 3 dead
    o.rect(12, 74, 78, 98, (46, 48, 72))
    o.rect(12, 70, 78, 75, (176, 50, 50))
    o.rect(18, 80, 40, 94, (20, 24, 40))
    o.rect(46, 80, 72, 92, (240, 196, 90), 0.85)
    o.poly([(50, 80), (58, 88), (54, 92), (46, 92)], (20, 24, 40))
    for k in range(3):
        o.circle(36 + k * 14, 64 - k * 5, 8 + k * 2, (80, 80, 94), 0.5 - k * 0.1)
    o.glow(58, 76, 10, FIRE, 0.6)
    o.label(14, 90, "VYSHNEVE: 3 DEAD", "CB", 6.5, WHITE, (150, 30, 30), 2)
    # Dymer block - standing wing
    o.rect(118, 34, 168, 98, (62, 64, 92))
    for fl in range(5):
        o.rect(118, 34 + fl * 12.6, 168, 35 + fl * 12.6, (40, 42, 66))
    o.windows(122, 38, 5, 5, 9.5, 12.6, 5, 7, (244, 206, 96), (28, 30, 52), 0.5)
    # collapsed wing: broken slabs + rubble slope
    o.poly([(168, 34), (176, 34), (176, 47), (186, 47), (186, 60), (198, 60), (198, 74), (220, 90), (240, 98), (168, 98)],
           (54, 56, 82))
    o.poly([(176, 47), (214, 54), (190, 52)], (36, 38, 58))
    o.poly([(168, 74), (184, 70), (200, 80), (224, 92), (246, 99), (168, 99)], (84, 76, 76))
    o.poly([(180, 84), (196, 78), (214, 90), (180, 96)], (110, 98, 90))
    o.glow(190, 70, 17, FIRE, 0.65)
    o.poly([(184, 74), (190, 56), (194, 70), (199, 60), (202, 76)], (255, 170, 40), 0.95)
    o.poly([(188, 76), (191, 66), (194, 76)], (255, 235, 140))
    for k in range(4):
        o.circle(194 + k * 8, 52 - k * 9, 8 + k * 2, (92, 90, 100), 0.55 - k * 0.1)
    # rescue: ladder, figures with helmets, stretcher
    o.line(172, 96, 188, 66, 1.6, (200, 190, 150))
    o.line(177, 97, 192, 68, 1.6, (200, 190, 150))
    for k in range(5):
        o.line(174 + k * 3.6, 91 - k * 6.5, 179.5 + k * 3.6, 92 - k * 6.5, 1, (200, 190, 150))
    o.person(206, 95, 1.5, (240, 130, 30), helmet=(255, 220, 40))
    o.person(220, 98, 1.5, (240, 130, 30), helmet=(255, 220, 40))
    o.rect(209, 94, 221, 96, (230, 230, 230))
    o.person(150, 99, 1.5, (60, 150, 220), helmet=(255, 220, 40))
    o.cone(224, 96, 196, 214, 58, (255, 250, 200), 0.22)
    o.label(118, 28, "DYMER: 11 DEAD", "CB", 7.5, WHITE, (150, 30, 30), 2)
    # drones and trajectories
    for dx, dy in [(300, 26), (270, 44), (246, 20)]:
        o.dline(dx - 8, dy + 1, 172, 52 + (dy - 26) * 0.3, 1, (255, 120, 60), 0.8, 4, 3)
        drone(o, dx, dy, 1.0)
    # searchlights
    o.cone(262, 98, 215, 236, 14, (200, 225, 255), 0.17)
    o.cone(100, 98, 108, 138, 14, (200, 225, 255), 0.14)
    # locator inset
    o.rect(6, 17, 74, 60, (8, 12, 26), 0.85)
    o.frame(6, 17, 74, 60, (120, 140, 190), 1, 0.9)
    o.poly([(10, 34), (30, 22), (60, 24), (70, 38), (62, 56), (16, 56)], (36, 52, 84))
    o.circle(36, 37, 3.2, WHITE)
    o.text(41, 40, "KYIV", "CB", 6.5, WHITE)
    for px, py, nm, tx, ty_ in [(48, 27, "Dymer", 52, 29), (20, 44, "Vyshneve", 24, 47), (44, 51, "B. Tserkva", 48, 54)]:
        o.circle(px, py, 2.4, (240, 60, 50))
        o.text(tx, ty_, nm, "CR", 6.3, (255, 214, 190))
    # banner
    o.rect(0, h - 24, 172, h, (176, 28, 28))
    o.rect(0, h - 24, 172, h - 22, (255, 205, 80))
    o.text(7, h - 7, "14 DEAD  ·  11 IN DYMER", "CB", 14, WHITE)


def scene_markets(o):
    w, h = o.w, o.h
    o.vgrad(0, 0, w, h, (8, 18, 40), (14, 30, 58))
    # chart panel
    cx0, cx1, cy0, cy1 = 8, 206, 30, 104
    o.rect(cx0, cy0, cx1, cy1, (10, 24, 46))
    for k in range(5):
        yy = cy0 + k * (cy1 - cy0) / 4
        o.rect(cx0, yy, cx1, yy + 1, (36, 62, 96))
    for k in range(1, 9):
        o.rect(cx0 + k * 22, cy0, cx0 + k * 22 + 1, cy1, (24, 44, 74))
    # candles (open, close, high, low) in y coords (smaller = higher price)
    cd = [(50, 46, 44, 52), (46, 52, 44, 54), (52, 50, 48, 56), (50, 58, 48, 60), (58, 66, 56, 68),
          (66, 62, 60, 70), (62, 76, 60, 80), (76, 88, 74, 94), (88, 98, 84, 102),  # crash: red, falling
          (98, 78, 74, 100), (78, 62, 58, 80), (62, 44, 40, 66), (44, 36, 32, 46), (36, 24, 20, 40)]
    for i, (op, cl, hi, lo) in enumerate(cd):
        x = cx0 + 8 + i * 13.4
        up = cl < op
        col = (36, 190, 100) if up else (214, 56, 56)
        o.line(x + 3, hi + 0, x + 3, lo + 0, 1, col)
        o.rect(x, min(op, cl), x + 6, max(op, cl) + 1, col)
    o.polyline([(14, 54), (60, 56), (96, 70), (122, 96), (140, 80), (160, 58), (200, 30)], 1.2, (255, 255, 255), 0.0)
    # annotations on chart
    o.text(cx0 + 4, cy0 - 3, "NASDAQ, 6 SESSIONS", "CB", 7, (150, 180, 220))
    o.label(86, 100, "FRI -5.28%", "CB", 8, WHITE, (170, 40, 40), 2)
    o.line(128, 104, 134, 100, 1, (255, 255, 255), 0.0)
    o.dline(110, 30, 176, 30, 1, (255, 255, 255), 0.5, 3, 3)
    o.label(150, 61, "MON +6.51%", "CB", 8, (8, 40, 20), (60, 220, 120), 2)
    o.poly([(172, 40), (186, 36), (183, 46)], (255, 255, 255))
    o.text(cx0 + 2, cy1 + 7, "THU", "CR", 7, (150, 180, 220))
    o.text(86, cy1 + 7, "FRI 20", "CR", 7, (150, 180, 220))
    o.text(168, cy1 + 7, "MON 23", "CR", 7, (150, 180, 220))
    # NVDA banner
    o.rect(8, 6, 206, 25, (24, 150, 70))
    o.circle(20, 15.5, 7, (118, 185, 0))
    o.text(20, 19, "N", "CB", 9, (10, 20, 10), "c")
    o.text(32, 20, "NVDA  +31%", "SB", 15, WHITE)
    o.text(200, 19, "$165.05", "CB", 9, (220, 255, 230), "r")
    o.rect(120, 8, 202, 23, (10, 90, 40), 0.6)
    o.text(160, 19, "HUANG REINSTATED", "CB", 7.5, (255, 240, 180), "c")
    # index board
    bx = 214
    rows = [("NASDAQ", "24,089.56", "+6.51%", (80, 230, 140)), ("S&P 500", "7,237.17", "+4.73%", (80, 230, 140)),
            ("DOW", "49,595.31", "+3.01%", (80, 230, 140))]
    o.rect(bx, 6, w - 6, 108, (12, 30, 54))
    o.frame(bx, 6, w - 6, 108, (60, 100, 150), 1)
    for i, (nm, lv, pc, col) in enumerate(rows):
        yy = 8 + i * 25
        o.rect(bx + 2, yy + 1, w - 8, yy + 24, (16, 40, 70) if i % 2 == 0 else (12, 32, 58))
        o.text(bx + 5, yy + 10, nm, "CB", 8, (180, 205, 235))
        o.text(w - 10, yy + 10, lv, "CR", 8, (200, 220, 240), "r")
        o.text(bx + 5, yy + 22, pc, "SB", 12.5, col)
        pts = [(w - 62 + k * 9, yy + 22 - (k * 1.6 + (2 if k % 2 else 0))) for k in range(6)]
        o.polyline(pts, 1.4, col)
    o.rect(bx + 2, 84, w - 8, 106, (16, 40, 70))
    o.text(bx + 5, 94, "412 UP / 86 DOWN", "CB", 8, (200, 225, 255))
    o.rect(bx + 5, 98, bx + 5 + 90 * 412 / 498, 103, (60, 210, 120))
    o.rect(bx + 5 + 90 * 412 / 498, 98, bx + 95, 103, (210, 60, 60))
    # bottom axis strip + big badge
    o.rect(0, 114, w, h, (6, 14, 30))
    o.text(8, 124, "BEST DAY SINCE APRIL 2025  ·  2ND-LARGEST NASDAQ POINTS GAIN: +1,471.83", "CB", 8, (255, 220, 120))


def scene_sanctions(o):
    w, h = o.w, o.h
    o.rect(0, 0, w, h, (0, 48, 140))
    o.vgrad(0, 0, w, 96, (0, 62, 160), (0, 40, 120))
    # faint star ring
    for k in range(12):
        a = k * math.pi / 6
        sx, sy = 262 + 44 * math.cos(a), 52 + 44 * math.sin(a)
        o.poly([(sx + 6 * math.cos(t * math.pi / 5 - math.pi / 2) * (1 if t % 2 == 0 else 0.42),
                 sy + 6 * math.sin(t * math.pi / 5 - math.pi / 2) * (1 if t % 2 == 0 else 0.42)) for t in range(10)],
               (255, 214, 60), 0.28)
    # sea + tankers
    o.rect(0, 94, w, h, (18, 58, 98))
    for k in range(5):
        o.rect(0, 100 + k * 6, w, 101 + k * 6, (40, 90, 140), 0.6)
    for tx, col in [(204, (30, 30, 36)), (258, (50, 30, 30))]:
        o.poly([(tx, 90), (tx + 44, 90), (tx + 38, 100), (tx + 4, 100)], col)
        o.rect(tx + 30, 80, tx + 38, 90, (190, 190, 200))
        o.rect(tx + 8, 86, tx + 28, 90, (130, 40, 40))
        o.line(tx + 4, 77, tx + 4, 90, 1, (200, 200, 200))
        o.line(tx - 6, 106, tx + 52, 106, 1, (120, 170, 210), 0.6)
    o.dline(190, 76, 316, 76, 1, (255, 220, 90), 0.0)
    o.label(204, 116, "70+ SHADOW-FLEET SHIPS", "CB", 8, (255, 230, 120), (6, 30, 70), 2)
    # document
    o.rect(14, 16, 186, 120, (252, 249, 238))
    o.rect(14, 16, 186, 34, (6, 38, 110))
    for k in range(12):
        a = k * math.pi / 6
        o.circle(32 + 8 * math.cos(a), 25 + 8 * math.sin(a), 1.3, GOLD)
    o.text(48, 29, "EUROPEAN COMMISSION", "CB", 9, WHITE)
    o.text(48, 38, "", "CR", 6, WHITE)
    rows = [("BANKS", "60 OFF SWIFT", RED), ("SHIPS", "70+ LISTED", (20, 60, 130)),
            ("ENERGY", "ELECTRICITY BAN", (20, 60, 130)), ("VISAS", "EX-COMBATANTS", (20, 60, 130)),
            ("FLAGS", "RUSSIAN BANNED", (20, 60, 130))]
    for i, (a, b, col) in enumerate(rows):
        yy = 44 + i * 12.5
        o.rect(20, yy - 8, 26, yy - 2, col)
        o.text(31, yy - 1, a, "CB", 8.5, INK)
        o.text(70, yy - 1, b, "CR", 8.5, (40, 40, 50))
        o.rect(20, yy + 3, 180, yy + 4, (210, 205, 190))
    o.line(68, 39, 128, 39, 1.2, RED)  # strike-through of SWIFT row
    o.text(130, 99, "", "CR", 7, INK)
    # stamps
    o.frame(112, 104, 180, 118, RED, 1.6)
    o.text(146, 115, "PROPOSED", "CB", 9, RED, "c")
    o.circle(40, 108, 9, (176, 28, 28))
    o.ring(40, 108, 7, 1, (255, 220, 220))
    o.text(40, 111, "22", "SB", 8, WHITE, "c")
    o.text(54, 111, "22ND PACKAGE", "CB", 7.5, (110, 20, 20))
    # SWIFT 60-dot grid panel
    o.rect(196, 14, 316, 70, (8, 30, 86), 0.92)
    o.frame(196, 14, 316, 70, (255, 214, 60), 1)
    o.text(201, 24, "RUSSIAN BANKS CUT OFF", "CB", 7.5, (255, 214, 60))
    for r in range(6):
        for k in range(10):
            xx, yy = 202 + k * 11, 29 + r * 6.8
            o.rect(xx, yy, xx + 8, yy + 4.6, (220, 70, 70))
    o.text(256, 66, "60 = ALL OFF SWIFT", "CB", 7.5, WHITE, "c")
    o.label(316, 8, "NEEDS ALL 27 STATES", "CB", 7.5, (6, 30, 90), (255, 214, 60), 2, "r")


# ====================================================================== CARDS
def card_fifa(o):
    w, h = o.w, o.h
    o.vgrad(0, 0, w, 36, (40, 110, 180), (150, 205, 235))
    o.ellipse(80, 62, 96, 34, (110, 112, 128))
    o.ellipse(80, 62, 84, 27, (74, 76, 94))
    o.ellipse(80, 62, 66, 19, (40, 130, 62))
    for k in range(6):
        o.rect(28 + k * 18, 50, 36 + k * 18, 74, (50, 150, 74), 0.7)
    o.ellipse(80, 60, 20, 6, (255, 255, 255), 0.0)
    o.ring(80, 62, 7, 1, WHITE, 0.8)
    o.windows(30, 36, 14, 2, 8.5, 5, 6, 3, (240, 235, 220), (200, 205, 220), 0.5)
    # four flags on poles
    for i, (cols, vert) in enumerate([((178, 34, 52), False), ((20, 120, 60), True), ((30, 60, 160), False),
                                      ((20, 130, 50), False)]):
        px = 14 + i * 21
        o.rect(px, 16, px + 1, 40, (60, 60, 70))
        if i == 0:
            flag3(o, px + 1, 16, 14, 10, [(178, 34, 52), WHITE, (178, 34, 52), WHITE, (178, 34, 52)])
            o.rect(px + 1, 16, px + 7, 21, (30, 50, 120))
        elif i == 1:
            flag3(o, px + 1, 16, 15, 10, [(20, 120, 60), WHITE, (200, 40, 40)], True)
        elif i == 2:
            flag3(o, px + 1, 16, 15, 10, [(30, 60, 160), WHITE, (200, 40, 40), WHITE, (30, 60, 160)])
        else:
            o.rect(px + 1, 16, px + 16, 26, (20, 130, 50))
            o.poly([(px + 1, 16), (px + 16, 26), (px + 16, 16), (px + 1, 26)], (20, 20, 20))
            o.line(px + 1, 16, px + 16, 26, 1.4, GOLD)
            o.line(px + 1, 26, px + 16, 16, 1.4, GOLD)
    # trophy
    o.poly([(96, 18), (108, 18), (106, 28), (102, 33), (98, 28)], GOLD)
    o.rect(99, 33, 105, 37, GOLD)
    o.rect(96, 37, 108, 40, (200, 150, 30))
    o.ring(96, 22, 4, 1.2, GOLD)
    o.ring(108, 22, 4, 1.2, GOLD)
    # numeral
    o.text(w - 6, 42, "48", "SB", 30, WHITE, "r")
    o.text(w - 6, 52, "TEAMS", "CB", 8, (255, 240, 170), "r")
    o.label(6, 52, "2031: 4 HOSTS", "CB", 7, WHITE, (20, 40, 90), 2)


def card_brentford(o):
    w, h = o.w, o.h
    o.rect(0, 0, w, h, (36, 120, 56))
    for k in range(9):
        o.rect(k * 20, 0, k * 20 + 10, h, (44, 134, 64))
    o.frame(6, 18, w - 6, h - 2, (230, 240, 230), 1, 0.7)
    o.rect(w - 36, 22, w - 6, 50, (230, 240, 230), 0.0)
    o.frame(w - 40, 24, w - 6, 48, WHITE, 1.4)
    for k in range(6):
        o.line(w - 40 + k * 7, 24, w - 40 + k * 7, 48, 0.6, WHITE, 0.5)
    for k in range(4):
        o.line(w - 40, 24 + k * 6, w - 6, 24 + k * 6, 0.6, WHITE, 0.5)
    o.ring(54, 38, 14, 1, (230, 240, 230), 0.6)
    # scoreboard
    o.rect(34, 16, 100, 38, (14, 20, 36))
    o.frame(34, 16, 100, 38, GOLD, 1)
    o.text(67, 34, "4–0", "SB", 20, WHITE, "c")
    # players
    for px, py, col in [(52, 52, (210, 40, 40)), (62, 53, (230, 230, 230)), (86, 50, (30, 70, 170)), (96, 54, (30, 70, 170))]:
        o.person(px, py, 1.3, col)
    o.circle(74, 51, 2.6, WHITE)
    o.circle(74, 51, 1, (30, 30, 30))
    o.dline(74, 50, w - 30, 38, 1, WHITE, 0.8, 3, 2)
    # red card
    o.rect(112, 14, 124, 30, (216, 30, 30))
    o.frame(112, 14, 124, 30, WHITE, 1)
    o.text(118, 42, "40'", "CB", 8, WHITE, "c")
    o.text(12, 50, "ONLY MON MATCH", "CB", 6.5, (220, 255, 220))


def card_gaza(o):
    w, h = o.w, o.h
    o.rect(0, 0, w, h, (70, 130, 178))
    o.vgrad(0, 0, 70, h, (60, 120, 172), (40, 96, 150))
    for k in range(4):
        o.line(4, 14 + k * 11, 60, 18 + k * 11, 0.8, (170, 210, 235), 0.5)
    o.poly([(66, 14), (w, 14), (w, h), (50, h), (60, 40)], (206, 186, 140))
    o.poly([(62, 16), (84, 14), (90, 24), (70, 50), (52, h), (44, h), (58, 40)], (190, 160, 96))
    for k in range(5):
        o.dline(70 + k * 4, 28 + k * 2, 124, 20 + k * 6, 0.6, (150, 130, 90), 0.8, 2, 2)
    # buildings in the camp
    for bx, by in [(86, 22), (94, 28), (102, 24), (110, 30), (118, 26)]:
        o.rect(bx, by, bx + 6, by + 6, (240, 230, 205))
    # well + blast
    o.glow(92, 25, 12, (255, 130, 40), 0.7)
    o.ring(92, 25, 9, 1.5, (255, 90, 40))
    o.circle(92, 25, 3, (255, 240, 180))
    o.rect(86, 34, 98, 40, (110, 110, 120))
    o.poly([(88, 34), (96, 34), (92, 29)], (80, 80, 94))
    o.circle(92, 38, 2, (60, 150, 220))
    # UN flag
    o.rect(120, 16, 150, 34, (90, 160, 225))
    o.circle(135, 25, 5, WHITE, 0.0)
    o.ring(135, 25, 5, 1, WHITE)
    o.ring(135, 25, 2.5, 0.8, WHITE)
    o.rect(119, 16, 120, 44, (80, 80, 90))
    o.text(4, 52, "JABALIA", "CB", 7, WHITE)
    o.pin = None
    o.circle(60, 20, 3, (255, 60, 50))
    o.text(w - 6, 50, "4", "SB", 30, (120, 30, 20), "r")
    o.text(w - 36, 50, "KILLED", "CB", 7, (120, 30, 20), "r")
    o.text(w - 36, 42, "MONDAY", "CB", 7, (120, 30, 20), "r")


def card_commod(o):
    w, h = o.w, o.h
    o.rect(0, 0, 80, h, (56, 42, 12))
    o.rect(80, 0, w, h, (30, 32, 44))
    o.vgrad(0, 0, 80, h, (66, 50, 14), (36, 28, 8))
    # gold bars
    for bx, by in [(6, 41), (28, 41), (17, 33)]:
        o.poly([(bx, by + 8), (bx + 3, by), (bx + 17, by), (bx + 20, by + 8)], GOLD)
        o.rect(bx + 3, by, bx + 17, by + 1.2, (255, 235, 140))
    o.polyline([(6, 30), (20, 26), (30, 28), (44, 20), (56, 14), (70, 9)], 1.8, (80, 230, 130))
    o.poly([(76, 7), (66, 8), (72, 15)], (80, 230, 130))
    o.text(76, 49, "+2.7%", "SB", 12, (110, 240, 150), "r")
    o.text(5, 20, "GOLD $3,635", "CB", 7, (255, 225, 140))
    # oil barrel
    o.rect(88, 28, 112, 52, (30, 30, 36))
    o.rect(88, 28, 112, 52, (24, 24, 30))
    for yy in (32, 40, 48):
        o.rect(88, yy, 112, yy + 2, (90, 90, 110))
    o.ellipse(100, 28, 12, 3, (70, 70, 84))
    o.circle(100, 40, 4, (240, 190, 40))
    o.polyline([(92, 12), (108, 15), (122, 20), (138, 28), (152, 36)], 1.8, (240, 80, 80))
    o.poly([(156, 40), (146, 38), (152, 31)], (240, 80, 80))
    o.text(w - 4, 50, "-4%", "SB", 15, (255, 120, 120), "r")
    o.text(86, 20, "WTI $81.29", "CB", 7, (200, 205, 225))
    o.rect(79, 14, 81, h, (150, 150, 160))


def card_deal(o):
    w, h = o.w, o.h
    o.vgrad(0, 0, w, h, (10, 24, 52), (20, 40, 80))
    for k in range(6):
        o.line(0, 18 + k * 8, w, 18 + k * 8, 0.6, (30, 56, 98), 0.8)
    # circuit traces
    o.polyline([(0, 44), (30, 44), (36, 38), (60, 38)], 0.9, (40, 90, 150))
    o.polyline([(w, 44), (w - 30, 44), (w - 36, 38), (w - 60, 38)], 0.9, (40, 90, 150))
    # shields
    def shield(cx, cy, s, col):
        o.poly([(cx - 11 * s, cy - 10 * s), (cx + 11 * s, cy - 10 * s), (cx + 11 * s, cy + 2 * s),
                (cx, cy + 14 * s), (cx - 11 * s, cy + 2 * s)], col)
        o.poly([(cx - 7 * s, cy - 6 * s), (cx + 7 * s, cy - 6 * s), (cx + 7 * s, cy + 1 * s),
                (cx, cy + 9 * s), (cx - 7 * s, cy + 1 * s)], mix(col, WHITE, 0.25))
    shield(20, 32, 1.1, (210, 40, 40))
    shield(w - 20, 32, 1.1, (40, 130, 230))
    o.text(28, 18, "", "CB", 6, WHITE)
    o.text(20, 53, "CROWDSTRIKE", "CB", 5.6, (255, 180, 170), "c")
    o.text(w - 20, 53, "ZSCALER", "CB", 6.5, (170, 210, 255), "c")
    o.poly([(34, 30), (40, 30), (40, 27), (45, 33), (40, 39), (40, 36), (34, 36)], (255, 215, 90))
    o.poly([(w - 34, 30), (w - 40, 30), (w - 40, 27), (w - 45, 33), (w - 40, 39), (w - 40, 36), (w - 34, 36)], (255, 215, 90))
    # contract
    o.rect(47, 16, w - 47, 48, (250, 247, 236))
    o.text(w / 2, 31, "$43.9bn", "SB", 13, INK, "c")
    o.rect(51, 36, w - 51, 37, (190, 185, 170))
    o.text(w / 2, 45, "ALL STOCK  1.135x", "CB", 6.5, (150, 30, 30), "c")
    o.label(w / 2, 13, "+34% PREMIUM", "CB", 6.5, (20, 40, 20), (110, 230, 140), 2, "c")


def card_ariane(o):
    w, h = o.w, o.h
    o.vgrad(0, 0, w, h, (6, 10, 34), (40, 60, 120))
    o.stars(24, 0, 13, w, 40)
    # earth limb
    o.ellipse(80, 98, 130, 56, (22, 70, 120))
    o.ellipse(80, 98, 130, 56, (60, 150, 200), 0.0)
    o.arc(80, 98, 130, math.pi * 1.1, math.pi * 1.9, 2, (130, 200, 255), 0.9)
    # orbit ring with 36 sats
    o.ellipse(112, 30, 40, 11, (0, 0, 0), 0.0)
    pts = ellipse_pts(112, 29, 40, 11, 0, 2 * math.pi, 36)
    o.polyline(pts + [pts[0]], 0.8, (255, 220, 120), 0.6)
    for (px, py) in pts:
        o.circle(px, py, 1.5, (255, 225, 120))
    # pad, gantry, rocket
    o.rect(20, 48, 100, 56, (70, 66, 60))
    o.rect(24, 22, 40, 50, (90, 94, 110))
    for k in range(6):
        o.line(24, 22 + k * 5, 40, 27 + k * 5, 0.8, (180, 184, 200), 0.9)
        o.line(40, 22 + k * 5, 24, 27 + k * 5, 0.8, (180, 184, 200), 0.9)
    o.rect(46, 18, 56, 50, (240, 240, 244))
    o.poly([(46, 18), (51, 8), (56, 18)], (230, 230, 236))
    o.rect(43, 34, 46, 50, (220, 120, 40))
    o.rect(56, 34, 59, 50, (220, 120, 40))
    o.rect(46, 30, 56, 32, (30, 30, 40))
    o.glow(51, 52, 9, (255, 200, 80), 0.35)
    o.label(w - 4, 14, "36 HELD", "CB", 8.5, (30, 20, 0), GOLD, 2, "r")
    o.text(w - 4, 44, "36", "SB", 24, WHITE, "r")
    o.text(w - 4, 53, "AMAZON LEO", "CB", 6.5, (200, 220, 255), "r")
    # scrub stripe
    o.rect(66, 36, 82, 44, (200, 40, 40))
    o.text(74, 43, "HOLD", "CB", 6, WHITE, "c")


def card_taiwan(o):
    w, h = o.w, o.h
    o.vgrad(0, 0, w, h, (60, 130, 180), (30, 90, 140))
    for k in range(5):
        o.dline(10, 20 + k * 9, w - 10, 20 + k * 9, 0.6, (150, 200, 230), 0.4, 4, 5)
    o.poly([(0, 13), (34, 13), (30, 24), (38, 34), (28, 44), (36, h), (0, h)], (150, 128, 82))
    o.poly([(0, 13), (20, 13), (16, 22), (0, 28)], (110, 140, 80))
    o.poly([(w - 36, 20), (w - 24, 16), (w - 12, 30), (w - 16, 50), (w - 26, h), (w - 34, 44), (w - 30, 30)], (96, 150, 90))
    o.poly([(w - 34, 28), (w - 26, 22), (w - 20, 34), (w - 28, 46)], (70, 120, 70))
    o.text(w - 26, 14, "TAIWAN", "CB", 6.5, WHITE, "c")
    o.dline(80, 13, 80, h, 1.2, (255, 235, 120), 1.0, 4, 3)
    o.text(80, h - 2, "MEDIAN LINE", "CB", 6, (255, 235, 120), "c")
    for i, yy in enumerate([22, 28, 34, 40, 46]):
        xs = 50 + (i % 2) * 4
        o.line(xs, yy, xs + 54, yy, 1.4, (255, 70, 60))
        o.poly([(xs + 58, yy), (xs + 52, yy - 3), (xs + 52, yy + 3)], (255, 70, 60))
    for k in range(12):
        sx = 6 + (k % 6) * 7 + (k // 6) * 3
        sy = 46 - (k // 6) * 4
        o.poly([(sx, sy), (sx + 5, sy), (sx + 4, sy + 2), (sx + 1, sy + 2)], (216, 220, 228))
    o.text(6, 55, "12 SHIPS", "CB", 6.5, WHITE)
    o.text(2, 42, "5", "SB", 26, (255, 90, 80), "l", 1.0)
    o.text(26, 28, "CROSSED", "CB", 6.5, WHITE)


def card_quake(o):
    w, h = o.w, o.h
    o.vgrad(0, 0, w, 22, (40, 110, 170), (80, 170, 210))
    o.vgrad(0, 22, w, h, (74, 50, 36), (30, 20, 28))
    o.rect(0, 20, w, 24, (30, 100, 150))
    for ix, iw in [(24, 12), (36, 8), (50, 14), (76, 7)]:
        o.poly([(ix, 20), (ix + iw / 2, 14), (ix + iw, 20)], (80, 150, 80))
    o.text(100, 13, "VANUATU", "CB", 7, WHITE)
    # depth ruler
    o.dline(40, 24, 40, 50, 1.2, (255, 255, 255), 0.9, 3, 2)
    for k, lab in enumerate(["0", "200", "400", "598"]):
        yy = 24 + k * 8.8
        o.rect(36, yy, 44, yy + 1, WHITE)
        o.text(31, yy + 3, lab, "CR", 5.5, WHITE, "r")
    for r_, a in [(12, 0.9), (8, 0.7), (4, 0.9)]:
        o.ring(40, 50, r_, 1.3, (255, 90, 60), a)
    o.circle(40, 50, 2.5, (255, 220, 120))
    # seismograph
    o.rect(70, 28, w - 4, 50, (12, 16, 24), 0.85)
    pts = []
    for k in range(30):
        amp = 0.5 if k < 14 else (9 * math.exp(-(k - 14) / 8.0))
        pts.append((72 + k * 2.2, 39 + math.sin(k * 1.7) * amp))
    o.polyline(pts, 1.0, (120, 255, 150))
    o.text(w - 6, 20 + 0, "", "CR", 6, WHITE)
    o.text(w - 6, 47, "M6.5", "SB", 14, WHITE, "r")
    o.label(52, 51, "598 KM DEEP", "CB", 6.5, WHITE, (140, 30, 30), 2)
    o.text(6, 12, "02:40 UTC", "CB", 6.5, WHITE)


def card_zambia(o):
    w, h = o.w, o.h
    o.vgrad(0, 0, w, h, (22, 60, 70), (14, 34, 44))
    o.stars(10, 0, 13, w, 30)
    # courthouse
    o.poly([(8, 28), (52, 28), (30, 16)], (226, 218, 196))
    o.rect(10, 28, 50, 31, (200, 190, 166))
    for k in range(5):
        o.rect(12 + k * 8.6, 31, 15 + k * 8.6, 46, (236, 228, 206))
    o.rect(6, 46, 54, 50, (200, 190, 166))
    o.rect(4, 50, 56, 54, (170, 160, 140))
    o.circle(30, 24, 2.2, (60, 70, 80))
    # gavel
    o.poly([(72, 22), (92, 16), (96, 24), (76, 30)], (150, 96, 46))
    o.line(86, 25, 70, 50, 3, (130, 84, 40))
    o.ellipse(84, 52, 14, 3, (70, 50, 30))
    o.rect(72, 46, 96, 52, (110, 70, 34))
    # scales
    o.line(112, 20, 112, 46, 1.4, GOLD)
    o.line(100, 24, 124, 24, 1.4, GOLD)
    o.poly([(100, 24), (95, 33), (105, 33)], (255, 215, 90), 0.9)
    o.poly([(124, 24), (119, 33), (129, 33)], (255, 215, 90), 0.9)
    o.rect(106, 46, 118, 48, GOLD)
    # flag
    o.rect(134, 18, 154, 32, (30, 130, 50))
    for k, col in enumerate([(210, 40, 40), (20, 20, 20), (240, 130, 20)]):
        o.rect(144 + k * 3, 24, 147 + k * 3, 32, col)
    o.rect(133, 18, 134, 46, (160, 160, 170))
    o.rect(0, 40, w, 53, (0, 0, 0), 0.0)
    o.label(w - 4, 51, "TREASON", "CB", 10, WHITE, (170, 30, 30), 2, "r")
    o.text(w - 4, 42, "13 CHARGED", "CB", 6.5, (255, 225, 160), "r")


def card_spain(o):
    w, h = o.w, o.h
    o.rect(0, 0, w, h, (28, 34, 52))
    o.rect(0, 13, w, 17, (200, 40, 40))
    o.rect(0, 17, w, 21, (250, 200, 40))
    o.rect(0, 21, w, 25, (200, 40, 40))
    # stacked majority bar PP + VOX
    sc = 92 / 190.0
    x0 = 8
    o.rect(x0, 30, x0 + 131 * sc, 40, (40, 120, 220))
    o.rect(x0 + 131 * sc, 30, x0 + 191 * sc, 40, (90, 190, 80))
    o.text(x0 + 3, 38, "PP 131", "CB", 7, WHITE)
    o.text(x0 + 131 * sc + 3, 38, "VOX", "CB", 7, (10, 40, 10))
    o.rect(x0, 43, x0 + 118 * sc, 51, (214, 60, 60))
    o.text(x0 + 3, 50, "PSOE 118", "CB", 6.5, WHITE)
    lx = x0 + 176 * sc
    o.dline(lx, 26, lx, 54, 1.2, WHITE, 1.0, 3, 2)
    o.text(lx, 28, "", "CB", 6, WHITE, "c")
    o.text(w - 4, 52, "176", "SB", 22, WHITE, "r")
    o.text(w - 4, 36, "SEATS NEEDED", "CB", 6.5, (255, 225, 150), "r")
    o.text(w - 4, 29, "PP+VOX 190+", "CB", 6.5, (140, 230, 130), "r")


def card_fed(o):
    w, h = o.w, o.h
    o.vgrad(0, 0, w, h, (22, 48, 44), (14, 30, 34))
    # Fed building
    o.poly([(6, 24), (46, 24), (26, 14)], (216, 210, 190))
    for k in range(5):
        o.rect(9 + k * 7.5, 25, 12 + k * 7.5, 44, (230, 224, 204))
    o.rect(4, 44, 48, 50, (190, 184, 164))
    o.text(26, 21, "", "CB", 5, INK)
    # gauge
    gx, gy = 94, 46
    o.arc(gx, gy, 26, math.pi, math.pi * 1.34, 7, (60, 190, 110))
    o.arc(gx, gy, 26, math.pi * 1.34, math.pi * 1.67, 7, (240, 200, 60))
    o.arc(gx, gy, 26, math.pi * 1.67, math.pi * 2, 7, (220, 60, 50))
    ang = math.pi + math.pi * 0.96
    o.line(gx, gy, gx + 22 * math.cos(ang), gy + 22 * math.sin(ang), 2, WHITE)
    o.circle(gx, gy, 3, WHITE)
    o.text(gx, gy - 9, "96%", "SB", 16, WHITE, "c")
    o.text(gx, h - 1, "DEC HIKE ODDS", "CB", 6, (190, 230, 210), "c")
    # inflation path
    o.polyline([(128, 18), (138, 20), (150, 34)], 1.4, (255, 140, 100))
    o.dline(124, 40, w - 2, 40, 0.8, (170, 210, 190), 0.9, 2, 2)
    o.polyline([(128, 22), (140, 24), (150, 32), (158, 39)], 1.6, (255, 150, 110))
    o.text(w - 2, 38, "2% 2028", "CB", 6, (170, 210, 190), "r")
    o.text(126, 17, "3.5%", "CB", 8, (255, 160, 120))
    


def card_awacs(o):
    w, h = o.w, o.h
    o.vgrad(0, 0, w, h, (28, 40, 96), (120, 80, 100))
    o.stars(10, 0, 13, w, 26)
    # Poland map
    pol = [(98, 34), (112, 30), (132, 31), (146, 36), (148, 46), (136, 54), (112, 54), (100, 48)]
    o.poly(pol, (210, 205, 180))
    o.poly([(98, 34), (112, 30), (132, 31), (146, 36), (148, 46), (136, 54), (112, 54), (100, 48)], (80, 120, 70), 0.0)
    o.circle(126, 44, 2.6, (255, 60, 50))
    o.text(124, 53, "POLAND", "CB", 6, (30, 30, 50), "c")
    # radar rings
    for r_ in (10, 18, 26):
        o.ring(126, 44, r_, 0.9, (120, 255, 160), 0.65)
    o.poly([(126, 44), (126 + 26 * math.cos(-0.9), 44 + 26 * math.sin(-0.9)), (126 + 26 * math.cos(-0.4), 44 + 26 * math.sin(-0.4))],
           (120, 255, 160), 0.35)
    # missiles
    for k, sy in enumerate([18, 24, 30]):
        o.dline(w - 4, sy - 4, 134, 40 + k * 2, 0.9, (255, 120, 60), 0.9, 3, 2)
        o.poly([(134, 40 + k * 2), (140, 38 + k * 2), (140, 42 + k * 2)], (255, 90, 50))
    # AWACS aircraft
    o.ellipse(40, 28, 26, 4.2, (220, 224, 232))
    o.poly([(28, 28), (48, 28), (58, 38), (50, 38)], (190, 194, 204))
    o.poly([(28, 28), (48, 28), (56, 19), (50, 19)], (200, 204, 214))
    o.poly([(14, 28), (16, 18), (22, 28)], (190, 194, 204))
    o.ellipse(38, 22, 10, 2.8, (240, 90, 60))
    o.rect(32, 24, 44, 26, (60, 66, 80))
    o.dline(40, 31, 100, 46, 0.9, (120, 255, 160), 0.9, 3, 2)
    o.label(6, 51, "NATO AWACS", "CB", 8.5, WHITE, (20, 40, 100), 2)
    o.text(w - 4, 15, "3 KH-101", "CB", 6.5, (255, 200, 160), "r")


MAIN_SCENES = [scene_kyiv, scene_markets, scene_sanctions]
CARD_SCENES = [card_fifa, card_brentford, card_gaza, card_commod, card_deal, card_ariane, card_taiwan,
               card_quake, card_zambia, card_spain, card_fed, card_awacs]
