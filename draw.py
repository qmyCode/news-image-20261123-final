"""Page assembly for NI23 v2: Monday 23 November 2026."""
import math
import re

from content import (ALSO, CARDS, CERT, DATE_LEFT, DATE_MID, DATE_NOTYET, MAINS, RCODE, RCOL, REGIONS,
                     STATS, TIMELINE)
from gfx import Canvas
from scenes import CARD_SCENES, MAIN_SCENES, Off

W = H = 1024
PAPER = (247, 243, 232)
INK = (16, 28, 52)
RED = (160, 26, 26)
GREY = (96, 94, 90)
RULE = (150, 144, 128)
M = 14  # page margin


def T(s):
    """Typography: curly quotes, proper minus and en dash."""
    s = re.sub(r"(?<=\d)-(?=\d)", "–", s)
    s = re.sub(r"(?<![\w)])-(?=\d)", "–", s)  # the fonts have no U+2212, so minus is an en dash
    s = s.replace("'", "’")
    return s


def fit(c, s, font, size, maxw, minsize=5.5):
    while size > minsize and c.tw(s, font, size) > maxw:
        size -= 0.25
    return size


def story_stats():
    allr = [m[1] for m in MAINS] + [k[1] for k in CARDS] + [a[0] for a in ALSO]
    return len(allr), {r: allr.count(r) for r in REGIONS}


def chip(c, x, y, s, col, size=7, h=None, pad=3, anchor="l"):
    """Certainty chip: filled rect + white text; (x, y) is top-left; returns width."""
    w = c.tw(s, "CB", size) + 2 * pad
    h = h or size + 4
    if anchor == "r":
        x -= w
    c.rect(x, y, x + w, y + h, col)
    c.text(x + pad, y + h - (h - size) / 2 - 1.2, s, "CB", size, (255, 255, 255))
    return w


def numchip(c, cx, cy, r, n, col):
    c.circle(cx, cy, r + 1, (255, 255, 255))
    c.circle(cx, cy, r, col)
    c.text(cx, cy + r * 0.38, str(n), "SB", r * 1.15, (255, 255, 255), "c")


def draw_masthead(c, total, nreg):
    c.rect(0, 0, W, 25, INK)
    c.text(M, 17, "THE WORLD IN ONE DAY", "CB", 12, (255, 255, 255), sp=1.2)
    claim = "%d STORIES  ·  %d REGIONS  ·  EVERY ONE DATED MONDAY 23 NOVEMBER 2026 (UTC)" % (total, nreg)
    sz = fit(c, claim, "CB", 11, 700)
    c.text(W - M, 17, claim, "CB", sz, (255, 255, 255), "r")
    c.rect(0, 25, W, 28, RED)


def draw_title(c):
    c.text(W / 2, 88, "Monday 23 November 2026", "SB", 70, (18, 20, 28), "c")
    deck = "Kyiv block falls in Dymer  ·  Huang back, Wall Street soars  ·  EU cuts 60 banks off SWIFT"
    c.text(W / 2, 108, T(deck), "SI", 16, RED, "c")
    c.rect(M, 113, W - M, 115, INK)


def draw_stats(c, y):
    cw = (W - 2 * M) / 6.0
    for i, (num, cap, src) in enumerate(STATS):
        x = M + i * cw
        if i:
            c.rect(x, y + 3, x + 1, y + 50, RULE)
        col = RED if i in (1,) else INK
        sz = fit(c, num, "SB", 33, cw - 12)
        c.text(x + cw / 2, y + 31, num, "SB", sz, col, "c")
        c.text(x + cw / 2, y + 41, T(cap), "CR", fit(c, T(cap), "CR", 9, cw - 8), (50, 50, 56), "c")
        c.text(x + cw / 2, y + 50, "source: " + src, "CR", 7.5, GREY, "c")
    c.rect(M, y + 54, W - M, y + 55, INK)


def draw_tally(c, y, counts, total):
    c.text(M, y + 10.5, "STORIES BY REGION", "CB", 8, INK, sp=0.5)
    x = M + 108
    wtot = W - M - x
    for r in sorted(REGIONS, key=lambda r: -counts[r]):
        n = counts[r]
        sw = wtot * n / total
        c.rect(x, y, x + sw - 1, y + 14, RCOL[r])
        lab = "%s %d" % (r, n)
        if c.tw(lab, "CB", 8.5) > sw - 5:
            lab = "%s %d" % (RCODE[r], n)
        c.text(x + sw / 2, y + 10.8, lab, "CB", 8.5, (255, 255, 255), "c")
        x += sw
    c.text(W - M, y + 24, "", "CR", 6, GREY, "r")


def draw_timeline(c, y):
    c.text(M, y + 15, "THE DAY IN UTC", "CB", 9, INK, sp=0.5)
    x0, x1 = M + 112, W - M - 14
    ry = y + 14
    c.rect(x0, ry, x1, ry + 2, INK)
    for hh in range(0, 25, 3):
        xx = x0 + (x1 - x0) * hh / 24.0
        c.rect(xx, ry - 1, xx + 1, ry + 4, GREY)
        c.text(xx, ry + 13 if False else ry + 4 + 0, "", "CR", 5, GREY)
    for i, (tm, lab) in enumerate(TIMELINE):
        hh, mm = tm.split(":")
        t = (int(hh) + int(mm) / 60.0) / 24.0
        xx = x0 + (x1 - x0) * t
        top = i % 2 == 0
        c.circle(xx, ry + 1, 3.6, RED)
        txt = "%s %s" % (tm, T(lab))
        wd = c.tw(tm, "CB", 8.5) + 3 + c.tw(T(lab), "CR", 8.5)
        ty = ry - 6 if top else ry + 16
        c.text(xx - wd / 2, ty, tm, "CB", 8.5, RED)
        c.text(xx - wd / 2 + c.tw(tm, "CB", 8.5) + 3, ty, T(lab), "CR", 8.5, (30, 30, 36))
    c.rect(M, y + 28, W - M, y + 29, INK)


def draw_strip(c, x, y, w, hgt, n, region, kicker, cert, big=False):
    col = RCOL[region]
    c.rect(x, y, x + w, y + hgt, col, 0.93)
    r = hgt / 2 - 1.5
    numchip(c, x + hgt / 2 + 1, y + hgt / 2, r, n, col)
    ksz = 8.5 if big else 7
    ccol = CERT[cert][1]
    csz = 7.5 if big else 6.2
    cw = c.tw(cert, "CB", csz) + 6
    avail = w - hgt - cw - 10
    k = T(kicker)
    kz = fit(c, k, "CB", ksz, avail, 5.2)
    c.text(x + hgt + 2, y + hgt / 2 + kz * 0.36, k, "CB", kz, (255, 255, 255))
    chip(c, x + w - 2, y + 1.5, cert, ccol, csz, hgt - 3, 3, "r")


def draw_mains(c, y):
    cw = 324
    gap = (W - 2 * M - 3 * cw) / 2.0
    sh = 134
    for i, (n, region, kicker, cert, head, deck, src) in enumerate(MAINS):
        x = M + i * (cw + gap)
        o = Off(c, x, y, cw, sh, (10, 14, 14)[i])
        MAIN_SCENES[i](o)
        o.done()
        draw_strip(c, x, y, cw, 17, n, region, kicker, cert, True)
        c.frame(x, y, x + cw, y + sh, INK, 1)
        yy = y + sh + 17
        hs = fit(c, T(head), "SB", 21, cw * 1.9) if False else 19.5
        lines = c.wrap(T(head), "SB", hs, cw - 2)
        for k, ln in enumerate(lines[:2]):
            c.text(x, yy + k * 21.5, ln, "SB", hs, (18, 20, 28))
        yy += 21.5 * min(2, len(lines)) + 1
        drawn, tot = c.para(x, yy, T(deck), "CR", 10, (40, 40, 48), cw, 12, 4)
        yy += 12 * drawn + 1
        c.text(x, yy, "SOURCE: " + T(src), "CR", 8, GREY)
        yy += 4
        if i:
            c.rect(x - gap / 2 - 0.5, y, x - gap / 2 + 0.5, y + sh + 96, RULE)
    return y + sh + 96


def draw_cards(c, y):
    cols = 6
    gap = 6
    cw = (W - 2 * M - gap * (cols - 1)) / cols
    sh = 62
    ch = 124
    for i, (n, region, kicker, cert, head, deck, src) in enumerate(CARDS):
        r, k = divmod(i, cols)
        x = M + k * (cw + gap)
        yy = y + r * (ch + 4)
        o = Off(c, x, yy, cw, sh, 5)
        CARD_SCENES[i](o)
        o.done()
        draw_strip(c, x, yy, cw, 13, n, region, kicker, cert)
        c.frame(x, yy, x + cw, yy + sh, INK, 1)
        ty = yy + sh + 12
        hs = 11.6
        lines = c.wrap(T(head), "SB", hs, cw - 1)
        while len(lines) > 2 and hs > 9:
            hs -= 0.3
            lines = c.wrap(T(head), "SB", hs, cw - 1)
        for j, ln in enumerate(lines[:2]):
            c.text(x, ty + j * 12, ln, "SB", hs, (18, 20, 28))
        dy = ty + 12 * min(2, len(lines)) + 1
        drawn, tot = c.para(x, dy, T(deck), "CR", 8.5, (50, 50, 56), cw, 9.4, 2)
        c.text(x, yy + ch - 3, T(src), "SI", 7.5, RCOL[region])
        if k < cols - 1:
            c.rect(x + cw + gap / 2, yy, x + cw + gap / 2 + 1, yy + ch - 6, (222, 216, 200))
    return y + 2 * ch + 4


# ----------------------------------------------------------------- map
LAND = [
    [(-168, 66), (-150, 70), (-125, 70), (-95, 72), (-80, 68), (-62, 60), (-55, 50), (-67, 45), (-76, 38), (-81, 31),
     (-80, 25), (-84, 30), (-90, 29), (-97, 27), (-97, 21), (-88, 21), (-87, 15), (-83, 10), (-78, 8), (-86, 12),
     (-92, 15), (-105, 20), (-112, 29), (-117, 32), (-124, 40), (-124, 48), (-135, 58), (-150, 60), (-165, 60)],
    [(-78, 8), (-72, 12), (-62, 10), (-52, 5), (-35, -6), (-39, -14), (-48, -26), (-58, -38), (-65, -42), (-68, -52),
     (-72, -52), (-74, -40), (-71, -20), (-76, -14), (-81, -5), (-79, 3)],
    [(-55, 60), (-45, 60), (-20, 70), (-18, 80), (-40, 83), (-65, 80), (-72, 76)],
    [(-9, 37), (-9, 43), (-2, 44), (-5, 48), (2, 51), (5, 53), (9, 55), (10, 58), (5, 62), (12, 66), (20, 70), (30, 71),
     (45, 68), (60, 70), (75, 72), (100, 77), (130, 73), (160, 70), (180, 68), (180, 65), (170, 60), (160, 58),
     (155, 52), (142, 53), (140, 48), (135, 43), (130, 42), (128, 36), (126, 38), (122, 40), (121, 31), (118, 24),
     (110, 20), (108, 14), (106, 9), (100, 13), (103, 2), (98, 8), (98, 16), (92, 22), (88, 22), (80, 15), (77, 8),
     (73, 17), (68, 24), (62, 25), (57, 26), (59, 22), (52, 16), (44, 12), (40, 20), (35, 28), (34, 31), (36, 36),
     (30, 36), (27, 37), (26, 40), (23, 37), (18, 40), (16, 38), (12, 42), (8, 44), (3, 43), (-1, 38)],
    [(-6, 36), (10, 37), (11, 33), (20, 32), (32, 31), (34, 28), (38, 20), (43, 12), (51, 12), (41, -2), (40, -15),
     (35, -24), (32, -29), (26, -34), (19, -35), (14, -22), (12, -6), (9, 3), (6, 5), (-8, 4), (-17, 14), (-16, 22),
     (-10, 30)],
    [(114, -22), (122, -18), (130, -12), (137, -12), (142, -11), (146, -19), (153, -26), (150, -37), (141, -38),
     (135, -35), (130, -32), (115, -34)],
    [(-5, 50), (1, 51), (2, 53), (-2, 56), (-3, 58.5), (-6, 57), (-3, 54), (-5, 52)],
    [(131, 31), (136, 34), (140, 35), (142, 40), (141, 45), (139, 43), (136, 36), (131, 33)],
    [(109, 1), (117, 7), (119, 1), (116, -4), (110, -3)],
    [(95, 5), (106, -6), (104, -6), (96, 2)],
    [(44, -25), (50, -15), (49, -12), (44, -17)],
    [(167, -46), (174, -41), (178, -38), (172, -35), (168, -44)],
]

# story -> (lon, lat, pin dx, pin dy)
PINS = {
    1: (31, 50, 17, -13), 2: (-74, 41, 24, -6), 3: (4, 51, -6, -21), 4: (8.5, 47, -4, 15), 5: (-0.3, 51.5, -22, -14),
    6: (34.5, 31.5, 14, 17), 8: (-77, 39, -16, 14), 9: (-52.8, 5.2, 0, -14), 10: (120, 24, -16, -15),
    11: (167, -16, 0, -15), 12: (28.3, -15.4, 0, -14), 13: (-3.7, 40.4, -20, 7), 14: (-74, 41, 14, 15),
    15: (19, 52, 6, -22),
}
PINREG = {m[0]: m[1] for m in MAINS}
PINREG.update({k[0]: k[1] for k in CARDS})


def draw_map(c, x, y, w, h, counts):
    c.text(x, y + 9, "WHERE IT HAPPENED", "CB", 9.5, INK, sp=0.6)
    c.text(x + w, y + 9, "pins = story numbers 1-15", "CR", 8, GREY, "r")
    my = y + 14
    mh = h - 14 - 24
    c.rect(x, my, x + w, my + mh, (214, 228, 238))
    c.frame(x, my, x + w, my + mh, INK, 1)
    c.clip(x, my, x + w, my + mh)

    def proj(lon, lat):
        return x + (lon + 180) / 360.0 * w, my + (84 - lat) / 142.0 * mh

    for k in range(1, 6):
        c.rect(x, my + mh * k / 6, x + w, my + mh * k / 6 + 1, (200, 216, 228))
    for k in range(1, 12):
        c.rect(x + w * k / 12, my, x + w * k / 12 + 1, my + mh, (200, 216, 228))
    for poly in LAND:
        pts = [proj(lo, la) for lo, la in poly]
        c.poly(pts, (192, 196, 176))
        c.polyline(pts + [pts[0]], 0.8, (140, 146, 124))
    # pins
    for n, (lo, la, dx, dy) in sorted(PINS.items()):
        px, py = proj(lo, la)
        col = RCOL[PINREG[n]]
        c.line(px, py, px + dx, py + dy, 1, col)
        c.circle(px, py, 1.6, col)
    for n, (lo, la, dx, dy) in sorted(PINS.items()):
        px, py = proj(lo, la)
        col = RCOL[PINREG[n]]
        numchip(c, px + dx, py + dy, 6.2, n, col)
    c.unclip()
    # off-map callout
    c.rect(x + 4, my + mh - 16, x + 158, my + mh - 3, (255, 255, 255))
    c.frame(x + 4, my + mh - 16, x + 158, my + mh - 3, RCOL["WORLD"], 1)
    numchip(c, x + 12, my + mh - 9.5, 5.4, 7, RCOL["WORLD"])
    c.text(x + 21, my + mh - 6.2, "GOLD AND OIL: global markets", "CR", 7.8, INK)
    # region legend with tally counts
    ly = my + mh + 11
    items = sorted(REGIONS, key=lambda r: -counts[r])
    cx = x
    for j, r in enumerate(items):
        row, col = divmod(j, 4)
        lx = x + col * (w / 4.0)
        yy = ly + row * 11
        c.rect(lx, yy - 7, lx + 8, yy + 1, RCOL[r])
        c.text(lx + 11, yy, "%s %d" % (r, counts[r]), "CR", 8, INK)


def draw_also(c, x, y, w, rows_h, counts):
    n0 = 16
    c.text(x, y + 9, "ALSO ON MONDAY 23 NOVEMBER", "CR", 10.5, INK, sp=0.5)
    c.text(x + w, y + 9, "%d more stories, in order of consequence; source and certainty on every line" % len(ALSO),
           "CR", 8.5, GREY, "r")
    c.rect(x, y + 13, x + w, y + 14, INK)
    colw = w / 2.0
    half = (len(ALSO) + 1) // 2
    # one font size for every line (regular weight only)
    size = 10.0
    lines = []
    for i, (reg, txt, src, cert) in enumerate(ALSO):
        lines.append((n0 + i, reg, T(txt), src, CERT[cert][0]))
    avail = colw - 10
    for (n, reg, txt, src, cc) in lines:
        full = "%d  %s  %s — %s %s" % (n, RCODE[reg], txt, src, cc)
        while c.tw(full, "CR", size) > avail and size > 7:
            size -= 0.1
    for idx, (n, reg, txt, src, cc) in enumerate(lines):
        col, row = divmod(idx, half)
        if idx >= half:
            col, row = 1, idx - half
        lx = x + col * colw + (6 if col else 0)
        ly = y + 26 + row * rows_h
        col_r = RCOL[reg]
        px = lx
        c.text(px, ly, str(n), "CR", size, col_r)
        px += c.tw("00", "CR", size) + 3
        c.text(px, ly, RCODE[reg], "CR", size - 1.5, col_r)
        px += c.tw("EU", "CR", size - 1.5) + 4
        px += c.text(px, ly, txt, "CR", size, (28, 28, 34)) + 3
        px += c.text(px, ly, "— " + src, "CR", size - 0.5, GREY) + 3
        c.text(px, ly, cc, "CR", size - 1.5, CERT[[k for k, v in CERT.items() if v[0] == cc][0]][1])
        if idx % half != half - 1 or True:
            c.rect(lx, ly + 3, lx + colw - 10, ly + 3.6, (226, 220, 204))
    c.rect(x + colw - 3, y + 17, x + colw - 2, y + 26 + half * rows_h - 8, RULE)
    return size


def draw_datecheck(c, y, h):
    c.rect(M, y, W - M, y + h, (252, 240, 236))
    c.frame(M, y, W - M, y + h, RED, 1.5)
    c.rect(M, y, M + 76, y + h, RED)
    c.text(M + 38, y + h / 2 - 2, "DATE", "SB", 15, (255, 255, 255), "c")
    c.text(M + 38, y + h / 2 + 12, "CHECK", "SB", 15, (255, 255, 255), "c")
    cx = M + 84
    cw = (W - M - 6 - cx) / 3.0
    blocks = [("LEFT OUT: these belong to other days", DATE_LEFT),
              ("LEFT OUT, continued", DATE_MID),
              ("NOT YET: had not happened at page time", DATE_NOTYET)]
    for k, (title, lines) in enumerate(blocks):
        bx = cx + k * cw
        c.text(bx, y + 11, title, "CB", 8.3, RED)
        for j, ln in enumerate(lines):
            sz = fit(c, T(ln), "CR", 8.3, cw - 8, 6.4)
            c.text(bx, y + 21 + j * 8.6, T(ln), "CR", sz, (40, 30, 30))
        if k:
            c.rect(bx - 5, y + 4, bx - 4, y + h - 4, (215, 170, 160))


def draw_footer(c, y):
    c.rect(M, y, W - M, y + 1, INK)
    c.text(M, y + 11, "Every story here happened or was first reported on Monday 23 November 2026 (UTC). "
           "Weekend events appear only where Monday brought the first report, with real dates in DATE CHECK.",
           "CR", 8.6, INK)
    src = ("SOURCES: Reuters · AP · AFP · Euronews · European Commission · US Treasury · Arianespace · FIFA · UEFA · "
           "Sky Sports · USGS/GDACS · Taiwan MND · UNRWA · NIHR · CNBC Africa · OkayAfrica · Informist · CREA · "
           "CME FedWatch · market data")
    c.text(M, y + 21, src, "CR", 8.0, GREY)
    x = M
    yy = y + 33
    c.text(x, yy, "HOW SURE:", "CB", 8, INK)
    x += c.tw("HOW SURE:", "CB", 8) + 5
    defs = [("CONFIRMED", "CNF", "wire or several outlets"), ("OFFICIAL", "OFF", "on the record from the body"),
            ("REPORTED", "REP", "one outlet or aggregator"), ("CLAIM", "CLM", "one side's account"),
            ("FORECAST", "FCT", "poll, preview or pricing")]
    for name, code, d in defs:
        wch = chip(c, x, yy - 8, name, CERT[name][1], 7, 10, 3)
        x += wch + 3
        s = "%s %s;" % (code, T(d))
        x += c.text(x, yy, s, "CR", 8, (40, 40, 46)) + 7
    c.text(W - M, y + 11, "", "CR", 7, GREY, "r")
    c.text(W - M, y + 41 + 1, "Pictures are drawn illustrations, not photographs.", "SI", 8, GREY, "r")


def render():
    total, counts = story_stats()
    nreg = len([r for r in REGIONS if counts[r]])
    c = Canvas(W, H, PAPER)
    draw_masthead(c, total, nreg)
    draw_title(c)
    y = 117
    draw_stats(c, y)
    y += 60
    draw_tally(c, y, counts, total)
    y += 17
    draw_timeline(c, y)
    y += 37
    y = draw_mains(c, y)
    c.rect(M, y + 2, W - M, y + 3, INK)
    y = draw_cards(c, y + 7)
    c.rect(M, y + 2, W - M, y + 3, INK)
    by = y + 6
    draw_map(c, M, by, 338, 184, counts)
    draw_also(c, M + 352, by, W - 2 * M - 352, 13.4, counts)
    dy = by + 188
    draw_datecheck(c, dy, 60)
    draw_footer(c, dy + 64)
    return c, total, counts, y
