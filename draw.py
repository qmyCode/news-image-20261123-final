#!/usr/bin/env python3
"""NI23 build — Monday 23 November 2026 on one page.

Broadsheet family geometry (the #1s' convergent core): cream page, navy
masthead with a count claim, giant serif date, italic deck, 6-stat bar,
region tally, UTC timeline, 3 illustrated mains, 12 illustrated cards,
WHERE IT HAPPENED map with numbered pins, sourced ALSO lines in regular
weight only, DATE CHECK band, sources footer + certainty legend.

Story bank: ../newsimage-research/23nov/story-bank.md (29 stories, 7 regions,
every story wire-verified for Mon 23 Nov 2026). Anti-flat rule enforced in
every scene: background layer + >=2 mid-ground subjects + an in-scene data
layer + light/texture; every event named in a headline is drawn.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MX = 26
CW = W - 2 * MX

CREAM = (247, 243, 233)
PAPER = (252, 250, 244)
INK = (24, 24, 24)
MUTE = (96, 90, 80)
NAVY = (16, 30, 52)
RULE = (40, 40, 40)
RED = (176, 32, 26)
DARKRED = (140, 24, 18)
GOLD = (198, 148, 32)
NIGHT = (14, 20, 38)

REG = {  # region -> colour
    "EUROPE": (38, 92, 140), "MIDDLE EAST": (178, 84, 30),
    "AMERICAS": (122, 44, 128), "ASIA-PACIFIC": (16, 118, 110),
    "AFRICA": (44, 128, 60), "OCEANIA": (198, 148, 32), "WORLD": (90, 90, 90),
}
TAGC = {"CONFIRMED": (30, 120, 62), "REPORTED": (38, 92, 140),
        "CLAIM": (196, 60, 20), "OFFICIAL": (110, 60, 160)}

FD = "/usr/share/fonts/truetype/dejavu/"


def F(name, size):
    return ImageFont.truetype(FD + name, size)


def SER(s):
    return F("DejaVuSerif.ttf", s)


def SERB(s):
    return F("DejaVuSerif-Bold.ttf", s)


def SAN(s):
    return F("DejaVuSans.ttf", s)


def SANB(s):
    return F("DejaVuSans-Bold.ttf", s)


img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img, "RGBA")


def tw(t, f):
    b = d.textbbox((0, 0), t, font=f)
    return b[2] - b[0]


def wrap(t, f, maxw):
    words, lines, cur = t.split(), [], ""
    for w_ in words:
        t2 = (cur + " " + w_).strip()
        if tw(t2, f) <= maxw:
            cur = t2
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text(x, y, t, f, fill=INK, anchor="la"):
    d.text((x, y), t, font=f, fill=fill, anchor=anchor)


def ctext(cx, y, t, f, fill=INK):
    d.text((cx, y), t, font=f, fill=fill, anchor="ma")


def para(x, y, t, f, maxw, lh, fill=INK, max_lines=None):
    lines = wrap(t, f, maxw)
    if max_lines:
        lines = lines[:max_lines]
    for i, ln in enumerate(lines):
        text(x, y + i * lh, ln, f, fill)
    return y + len(lines) * lh


def rule(x0, x1, y, wdt=1, fill=RULE):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)


def chip(x, y, label, col, align="l"):
    f = SANB(9)
    wdt = tw(label, f) + 10
    if align == "r":
        x -= wdt
    d.rectangle([x, y, x + wdt, y + 15], fill=col)
    text(x + 5, y + 2, label, f, (255, 255, 255))
    return wdt


def loctag(x, y, label):
    f = SANB(9)
    wdt = tw(label, f) + 10
    d.rectangle([x, y, x + wdt, y + 15], fill=(20, 20, 20, 215))
    text(x + 5, y + 2, label, f, (255, 255, 255))
    return wdt


def banner(x, y, t, col=RED):
    f = SANB(11)
    wdt = tw(t, f) + 14
    d.rectangle([x, y, x + wdt, y + 19], fill=col)
    text(x + 7, y + 3, t, f, (255, 255, 255))
    return wdt


def flame(cx, cy, s):
    d.polygon([(cx, cy - s), (cx + s * 0.55, cy + s * 0.4), (cx + s * 0.2, cy + s * 0.75),
               (cx - s * 0.2, cy + s * 0.75), (cx - s * 0.55, cy + s * 0.4)], fill=(232, 119, 34))
    d.polygon([(cx, cy - s * 0.35), (cx + s * 0.3, cy + s * 0.4), (cx, cy + s * 0.7),
               (cx - s * 0.3, cy + s * 0.4)], fill=(245, 197, 66))


def drone(cx, cy, s):
    d.line([(cx - s, cy - s * 0.6), (cx + s, cy + s * 0.6)], fill=(230, 230, 220), width=2)
    d.line([(cx - s, cy + s * 0.6), (cx + s, cy - s * 0.6)], fill=(230, 230, 220), width=2)
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 210, 90))


# ------------------------------------------------------------------ data
# (num, region, place, tag, headline, deck) — all from story-bank.md
MAINS = [
    (1, "EUROPE", "KYIV REGION, UKRAINE", "CONFIRMED",
     "Overnight strikes kill at least 14; a block falls in Dymer",
     "11 dead in Dymer, where a five-storey block partly collapsed; 3 dead "
     "at a Vyshneve supermarket, 15 wounded. Monday: 5 hurt in central Kyiv; "
     "Zelenskiy warns of new strikes. (AFP via Euronews, Reuters)"),
    (2, "AMERICAS", "NEW YORK, WALL STREET", "CONFIRMED",
     "Huang back at Nvidia; Wall Street's biggest rally since April 2025",
     "NVDA +31% as the board reinstates Jensen Huang 11 days after he quit. "
     "Nasdaq +6.51% to 24,089.56; S&P 500 +4.73%; Dow +3.01%. (Reuters)"),
    (3, "EUROPE", "BRUSSELS", "OFFICIAL",
     "EU unveils 22nd sanctions package: 60 banks off SWIFT",
     "~60 Russian banks face a transaction ban and SWIFT removal; 70+ "
     "shadow-fleet ships listed; visa ban for ex-combatants; Russian flag "
     "banned at EU sports events. Needs all 27 to agree. (European Commission)"),
]
CARDS = [
    (4, "WORLD", "ZURICH", "CONFIRMED", "48",
     "FIFA gives 2031 Women's World Cup to four nations; UK gets 2035",
     "USA–Mexico–Costa Rica–Jamaica by acclamation — first 48-team WWC. "
     "England, N. Ireland, Scotland, Wales host 2035. (Reuters)"),
    (5, "EUROPE", "BRENTFORD", "CONFIRMED", "4–0",
     "Brentford 4–0 Everton: the only Monday match",
     "Lewis-Potter 23', 25'; Janelt 67'; Carvalho 90'. Tarkowski sent off "
     "40'. Matchweek 11 closes. (Sky Sports)"),
    (6, "MIDDLE EAST", "GAZA", "CONFIRMED", "4",
     "Israeli strike kills UNRWA worker in Gaza",
     "Adel Al-Helo killed at a Jabalia well; 3 wounded. 4 Palestinians "
     "killed Monday; Gaza toll since Oct 2023: 74,746. (Reuters, UNRWA)"),
    (7, "WORLD", "COMMODITIES", "CONFIRMED", "+2.7%",
     "Gold rebounds +2.7% off a 14-month low; oil slides −4%",
     "Gold ~$3,635/oz after Friday's $3,503 low; silver +~4%. WTI ~$81.29 "
     "as Trump gives Iran talks time. (Market wires)"),
    (8, "AMERICAS", "WASHINGTON", "OFFICIAL", "$43.9bn",
     "CrowdStrike buys Zscaler for $43.9bn",
     "All-stock: $260.41 a share, ~34% premium; 1.135 CrowdStrike shares "
     "per Zscaler share. Closes H2 FY2028. (Companies, Reuters)"),
    (9, "EUROPE", "KOUROU", "OFFICIAL", "36",
     "Ariane 6 scrubs Amazon's 36-satellite launch",
     "Ground-systems fault halts the countdown; rocket and satellites safe. "
     "Retry no earlier than Tue 24 Nov. (Arianespace)"),
    (10, "ASIA-PACIFIC", "TAIWAN STRAIT", "OFFICIAL", "5",
     "Five Chinese sorties cross Taiwan's median line",
     "6 sorties, 12 naval vessels in 24 hours to Mon 06:00. Taipei warns of "
     "Beijing interference in Sat 28 Nov elections. (Taiwan MND)"),
    (11, "OCEANIA", "VANUATU", "CONFIRMED", "M6.5",
     "M6.5 quake strikes Vanuatu — deep, no damage",
     "02:40 UTC, ~598 km deep; M4.9 aftershock 03:07 UTC. GDACS green: no "
     "deaths, injuries or damage. (USGS)"),
    (12, "AFRICA", "LUSAKA", "CONFIRMED", "TREASON",
     "Zambia charges opposition leader with treason",
     "Brian Mundubile and 12+ associates charged over an alleged Apr–Aug "
     "2026 plot; committed to the High Court. (Reuters)"),
    (13, "EUROPE", "MADRID", "CONFIRMED", "176",
     "Spain's right set for joint majority, final polls show",
     "PP 127–136 seats, Vox 51–61 — jointly over the 176-seat threshold in "
     "the 350-seat Congress. Vote Sun 29 Nov. (Reuters)"),
    (14, "WORLD", "HOLLYWOOD", "CONFIRMED", "$225m",
     "Hunger Games reaps $225m worldwide opening",
     "$120m domestic, $105m international, 85 territories. ~13× the No. 2 "
     "film ('I Play Rocky', $9.3m). (Screen Daily)"),
    (15, "EUROPE", "POLAND", "CONFIRMED", "AWACS",
     "NATO sends AWACS to Poland after missile incident",
     "Early-warning aircraft to deploy after three Russian Kh-101 missiles "
     "landed in Poland on Fri 20 Nov. (Reuters)"),
]
ALSO = [  # (num, region, lead, text, source)
    (16, "EUROPE", "Moscow", "accuses Estonia of acts 'on the verge of open war'", "Reuters"),
    (17, "EUROPE", "Kyiv", "Zelenskiy: intelligence shows Russia planning new strikes", "Reuters"),
    (18, "MIDDLE EAST", "Washington", "US sanctions Iran's shadow banks; ~$15bn suspect flows", "US Treasury"),
    (19, "AMERICAS", "Washington", "Trump hush-money appeal revived by appeals court", "AP"),
    (20, "AMERICAS", "Landover", "MNF preview: Bengals' 5-game streak at Commanders, 20:15 ET", "Reuters"),
    (21, "ASIA-PACIFIC", "Seoul", "KOSPI −3.31% despite stabilisation pledge; Taiwan +2.35%", "Market data"),
    (22, "ASIA-PACIFIC", "Taipei", "Golden Horse: Singapore's 'The Violinist' wins two prizes", "Bandwagon"),
    (23, "AFRICA", "Nairobi", "Kenya and DR Congo restore ambassadors after 2+ years", "OkayAfrica"),
    (24, "AFRICA", "Niger State", "64 killed in weekend attacks in Nigeria's Niger state", "Reuters"),
    (25, "AFRICA", "Lausanne", "CAS to rule Tuesday on Senegal's stripped AFCON title", "Reuters"),
    (26, "OCEANIA", "Melbourne", "Will Jacks ruled out of England's Australia tour — broken hand", "AFP"),
    (27, "WORLD", "Crypto", "Bitcoin back above $60,000 after Saturday's $55,130 low", "Market data"),
    (28, "WORLD", "Antalya", "COP31 fallout: Guterres 'deeply disappointed'", "CNBC Africa"),
    (29, "WORLD", "Rome", "WFP: wars may cost $727m more, put aid for 7.3m at risk", "Reuters"),
]
STATS = [("14", "killed in Kyiv-region overnight strikes"),
         ("+6.51%", "Nasdaq's Monday jump, best since Apr 2025"),
         ("60", "Russian banks to be cut from SWIFT"),
         ("48", "teams at the 2031 Women's World Cup"),
         ("M6.5", "Vanuatu quake, 598 km deep"),
         ("$225m", "Hunger Games global opening")]
TIMELINE = [("02:40", "Vanuatu quake"), ("06:13", "Kyiv toll: 14 dead"),
            ("12:27", "Zambia treason charge"), ("15:19", "FIFA awards 2031"),
            ("17:12", "EU–US split public"), ("21:00", "Wall St: Nasdaq +6.51%")]

# ------------------------------------------------------------------ masthead
d.rectangle([0, 0, W, 30], fill=NAVY)
text(MX, 8, "THE WORLD IN ONE DAY", SANB(12), (255, 255, 255))
_r = "29 STORIES · 7 REGIONS · ALL DATED MONDAY 23 NOVEMBER 2026"
text(W - MX, 9, _r, SANB(10), (255, 255, 255), anchor="ra")
ctext(W // 2, 40, "Monday 23 November 2026", SERB(50))
ctext(W // 2, 100, "14 killed in Kyiv overnight · Huang back, Wall Street soars · "
      "EU unveils 22nd sanctions package", SER(14), DARKRED)
rule(MX, W - MX, 126, 2)

# stat bar
sy = 132
cellw = CW / 6
for i, (num, lab) in enumerate(STATS):
    cx = MX + i * cellw
    if i:
        d.line([(cx, sy + 2), (cx, sy + 44)], fill=RULE, width=1)
    ctext(cx + cellw / 2, sy, num, SERB(25), DARKRED if i in (1, 2) else INK)
    for j, ln in enumerate(wrap(lab, SAN(8), cellw - 12)):
        ctext(cx + cellw / 2, sy + 32 + j * 10, ln, SAN(8), MUTE)
rule(MX, W - MX, sy + 52, 1)

# region tally bar (counts computed from the data itself)
from collections import Counter
tally = Counter([m[1] for m in MAINS] + [c[1] for c in CARDS] + [a[1] for a in ALSO])
order = ["EUROPE", "MIDDLE EAST", "AMERICAS", "ASIA-PACIFIC", "AFRICA", "OCEANIA", "WORLD"]
ty = sy + 58
tx = MX
for rname in order:
    seg = f" {rname} {tally[rname]} "
    wdt = tw(seg, SANB(10)) + 8
    d.rectangle([tx, ty, tx + wdt, ty + 18], fill=REG[rname])
    text(tx + 4, ty + 3, seg, SANB(10), (255, 255, 255))
    tx += wdt + 3
rule(MX, W - MX, ty + 24, 1)

# timeline strip
ly = ty + 30
text(MX, ly + 2, "THE DAY IN UTC", SANB(10), NAVY)
lx = MX + tw("THE DAY IN UTC", SANB(10)) + 12
for tme, ev in TIMELINE:
    text(lx, ly + 2, tme, SANB(9.5), DARKRED)
    lx += tw(tme, SANB(9.5)) + 4
    text(lx, ly + 2, ev, SAN(9.5))
    lx += tw(ev, SAN(9.5)) + 12
rule(MX, W - MX, ly + 20, 2)

# ------------------------------------------------------------------ main scenes
def scene_kyiv(x, y, w, h):
    """Night over the Kyiv region: sky gradient + stars, lit five-storey
    blocks, one section collapsed and burning, rescue figures in the rubble,
    drone swarm, searchlight cone, count banner."""
    for i in range(6):
        d.rectangle([x, y + i * h // 6, x + w, y + (i + 1) * h // 6 + 1],
                    fill=(13 + i * 3, 19 + i * 4, 38 + i * 6))
    for sx, sy_ in [(28, 12), (86, 28), (148, 9), (228, 20), (282, 11), (190, 32)]:
        d.ellipse([x + sx, y + sy_, x + sx + 2, y + sy_ + 2], fill=(220, 220, 200))
    base = y + h
    blocks = [(8, 42, 32), (46, 58, 38), (92, 48, 28), (196, 62, 42), (246, 46, 28), (280, 54, 30)]
    for bx, bh, bw in blocks:  # lit five-storey blocks
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(38, 42, 58))
        for r_ in range(4):
            for c_ in range(3):
                if (r_ * 3 + c_ + bx) % 3:
                    d.rectangle([x + bx + 5 + c_ * 9, base - bh + 6 + r_ * 11,
                                 x + bx + 10 + c_ * 9, base - bh + 11 + r_ * 11],
                                fill=(250, 205, 100))
    # the collapsed section of the Dymer block: tilted slab + flame + smoke
    d.polygon([(x + 122, base), (x + 146, base - 32), (x + 162, base)], fill=(70, 60, 55))
    d.polygon([(x + 130, base - 14), (x + 150, base - 26), (x + 158, base - 10)],
              fill=(52, 46, 42))
    d.ellipse([x + 132, y + 10, x + 168, y + 34], fill=(95, 95, 100))
    d.ellipse([x + 142, y + 4, x + 166, y + 20], fill=(110, 110, 115))
    flame(x + 144, base - 38, 17)
    for dx, dy, s in [(58, 15, 6), (102, 25, 7), (182, 13, 6), (222, 29, 7),
                      (262, 19, 5), (136, 7, 5), (208, 40, 5)]:
        drone(x + dx, y + dy, s)
    d.polygon([(x + 196, base), (x + 236, y + 26), (x + 248, y + 30), (x + 214, base)],
              fill=(255, 240, 170, 60))  # searchlight cone
    # two rescue figures at the rubble, one carrying a stretcher line
    for fx in (128, 152):
        d.ellipse([x + fx, base - 16, x + fx + 5, base - 11], fill=(240, 200, 90))
        d.rectangle([x + fx - 1, base - 11, x + fx + 6, base - 1], fill=(240, 200, 90))
    banner(x + 8, y + h - 25, "14 DEAD · 11 IN DYMER")


def scene_markets(x, y, w, h):
    """The rally as a chart: paper panel, gridlines, three rising index
    lines with % moves and levels, green candle wall, NVDA ticker tape."""
    d.rectangle([x, y, x + w, y + h], fill=(250, 248, 240))
    for gy in range(5):
        yy = y + 10 + gy * (h - 34) // 4
        d.line([(x + 8, yy), (x + w - 8, yy)], fill=(220, 214, 200), width=1)
    rows = [("NASDAQ", "+6.51%", "24,089.56", (16, 118, 60), 0),
            ("S&P 500", "+4.73%", "7,237.17", (38, 92, 140), 1),
            ("DOW", "+3.01%", "49,595.31", (122, 44, 128), 2)]
    for name, pct, lvl, col, i in rows:
        text(x + 10, y + 14 + i * 26, f"{name} {pct}", SANB(9.5), col)
        pts = [(x + 118 + j * 26, y + 22 + i * 26 - j * 2.4) for j in range(7)]
        d.line(pts, fill=col, width=2)
        for px, py in pts[::2]:
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=col)
    d.line([(x + 8, y + h - 24), (x + w - 8, y + h - 24)], fill=(220, 214, 200), width=1)
    d.rectangle([x, y + h - 20, x + w, y + h], fill=(16, 30, 52))
    ctext(x + w / 2, y + h - 16, "NVDA +31%  ·  BEST DAY SINCE APR 2025",
          SANB(9.5), (255, 244, 214))


def scene_sanctions(x, y, w, h):
    """The 22nd package as a stamped document: EU stars header, four
    ledger rows with figures, red 22ND PACKAGE seal, signature line."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 208))
    d.rectangle([x + 10, y + 8, x + w - 10, y + h - 8], fill=(252, 250, 244),
                outline=(150, 144, 128))
    d.rectangle([x + 10, y + 8, x + w - 10, y + 30], fill=(16, 30, 52))
    for i in range(12):  # EU star ring, simplified as 12 dots
        a = 2 * math.pi * i / 12
        sx, sy_ = x + 30 + 9 * math.cos(a), y + 19 + 7 * math.sin(a)
        d.ellipse([sx - 1.5, sy_ - 1.5, sx + 1.5, sy_ + 1.5], fill=(250, 205, 100))
    text(x + 48, y + 12, "EUROPEAN COMMISSION", SANB(10), (255, 255, 255))
    rows = [("60 BANKS", "OFF SWIFT — transaction ban"),
            ("70+ SHIPS", "shadow fleet listed"),
            ("VISAS", "ex-combatants banned"),
            ("FLAGS", "Russian symbols banned")]
    for i, (big, small) in enumerate(rows):
        ry = y + 34 + i * 14
        text(x + 18, ry, big, SANB(10), DARKRED)
        text(x + 108, ry + 1, small, SAN(9), INK)
        if i < 3:
            d.line([(x + 18, ry + 12), (x + w - 18, ry + 12)], fill=(220, 214, 200), width=1)
    d.rectangle([x + w - 82, y + h - 24, x + w - 10, y + h - 8], outline=(163, 22, 33), width=2)
    ctext(x + w - 46, y + h - 21, "PROPOSED", SANB(9), (163, 22, 33))
    d.line([(x + 18, y + h - 16), (x + 120, y + h - 16)], fill=(120, 110, 92), width=1)
    text(x + 18, y + h - 13, "needs all 27 to agree", SAN(8), MUTE)

# ------------------------------------------------------------------ card scenes
def scene_card(x, y, w, h, glyph):
    """Mini-scene per card (top-#1 standard): scene zone below the 15px tag
    band, scene elements left, the big numeral right. Never a lone glyph on
    a flat field."""
    WHT = (245, 245, 240)

    def num(t, f=19):
        # dark pill behind the numeral so it never sits on a light scene element
        wdt = tw(t, SER(f))
        cx = x + w - 8 - wdt / 2
        d.rectangle([cx - wdt / 2 - 4, y + 15, cx + wdt / 2 + 4, y + 19 + f + 4],
                    fill=(15, 15, 18, 200))
        ctext(cx, y + 17, t, SER(f), WHT)

    def band(bg):
        d.rectangle([x, y, x + w, y + h], fill=bg)
        d.rectangle([x, y, x + w, y + 15], fill=(15, 15, 18, 190))

    if glyph == "48":  # Zurich: stadium arc, four flags, ball
        band((22, 40, 66))
        d.arc([x + 6, y + 12, x + 106, y + 52], 180, 360, fill=(210, 210, 220), width=2)
        for i in range(7):
            a = math.pi * (0.1 + 0.8 * i / 6)
            px, py = x + 56 + 44 * math.cos(a), y + 52 - 34 * math.sin(a)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(250, 205, 100))
        flag_cols = [(178, 32, 26), (16, 118, 60), (38, 92, 140), (122, 44, 128)]
        for i, fc in enumerate(flag_cols):
            fx = x + 12 + i * 13
            d.line([fx, y + 18, fx, y + 32], fill=(230, 230, 230), width=1)
            d.rectangle([fx + 1, y + 19, fx + 10, y + 26], fill=fc)
        d.ellipse([x + 96, y + 28, x + 104, y + 36], fill=(250, 250, 245),
                  outline=(20, 20, 20))
        num("48")
    elif glyph == "4–0":  # Brentford: pitch stripes, goal, ball, red card
        band((34, 108, 58))
        for i in range(4):
            d.rectangle([x + i * w // 4, y + 16, x + (i + 1) * w // 4, y + h],
                        fill=(46, 128, 70) if i % 2 else (38, 112, 60))
        d.rectangle([x + 8, y + 20, x + 34, y + 34], outline=WHT, width=2)
        d.line([x + 8, y + 27, x + 34, y + 27], fill=WHT, width=1)
        d.ellipse([x + 52, y + 24, x + 60, y + 32], fill=(250, 250, 245),
                  outline=(20, 20, 20))
        d.rectangle([x + 78, y + 18, x + 86, y + 30], fill=(178, 32, 26))
        num("4–0")
    elif glyph == "4":  # Gaza: strip map, Jabalia pin, UN flag, well
        band((110, 84, 28))
        d.polygon([(x + 10, y + 34), (x + 26, y + 20), (x + 62, y + 18),
                   (x + 78, y + 30), (x + 60, y + 36)], fill=(196, 178, 128))
        d.ellipse([x + 30, y + 20, x + 36, y + 26], fill=RED, outline=WHT)
        d.line([x + 48, y + 18, x + 48, y + 30], fill=(230, 230, 230), width=1)
        d.rectangle([x + 49, y + 19, x + 58, y + 25], fill=(38, 92, 140))
        d.ellipse([x + 66, y + 26, x + 72, y + 32], outline=(38, 92, 140), width=2)
        d.line([x + 69, y + 26, x + 69, y + 22], fill=(38, 92, 140), width=2)
        num("4")
    elif glyph == "+2.7%":  # commodities: gold line up, oil line down, bars
        band((28, 40, 66))
        for i in range(5):
            bh = 4 + i * 2
            d.rectangle([x + 12 + i * 9, y + h - 4 - bh, x + 18 + i * 9, y + h - 4],
                        fill=(198, 148, 32))
        d.line([(x + 66, y + 32), (x + 84, y + 24), (x + 102, y + 18)], fill=(250, 205, 100), width=2)
        d.line([(x + 66, y + 18), (x + 84, y + 26), (x + 102, y + 32)], fill=(232, 80, 60), width=2)
        d.ellipse([x + 100, y + 16, x + 104, y + 20], fill=(250, 205, 100))
        d.ellipse([x + 100, y + 30, x + 104, y + 34], fill=(232, 80, 60))
        num("+2.7%", 15)
    elif glyph == "$43.9bn":  # CrowdStrike+Zscaler: two shields, arrow, doc
        band((38, 38, 46))
        d.polygon([(x + 12, y + 18), (x + 30, y + 18), (x + 30, y + 28),
                   (x + 21, y + 36), (x + 12, y + 28)], fill=(38, 92, 140))
        d.polygon([(x + 36, y + 18), (x + 54, y + 18), (x + 54, y + 28),
                   (x + 45, y + 36), (x + 36, y + 28)], fill=(198, 148, 32))
        d.line([(x + 58, y + 27), (x + 74, y + 27)], fill=WHT, width=2)
        d.polygon([(x + 74, y + 23), (x + 82, y + 27), (x + 74, y + 31)], fill=WHT)
        d.rectangle([x + 88, y + 19, x + 106, y + 35], fill=(240, 240, 235))
        for ly_ in range(3):
            d.line([x + 91, y + 23 + ly_ * 4, x + 103, y + 23 + ly_ * 4],
                   fill=(140, 140, 140), width=1)
        num("$43.9bn", 14)
    elif glyph == "36":  # Kourou: rocket on pad, gantry, orbit dots
        band((22, 22, 40))
        d.rectangle([x + 14, y + 16, x + 20, y + 36], fill=(150, 150, 160))
        d.rectangle([x + 24, y + 20, x + 34, y + 36], fill=(240, 240, 235))
        d.polygon([(x + 24, y + 20), (x + 29, y + 14), (x + 34, y + 20)], fill=(178, 32, 26))
        d.ellipse([x + 27, y + 24, x + 31, y + 28], fill=(38, 92, 140))
        for i in range(6):
            a = 2 * math.pi * i / 6
            px, py = x + 78 + 22 * math.cos(a), y + 26 + 8 * math.sin(a)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(250, 205, 100))
        d.ellipse([x + 76, y + 24, x + 80, y + 28], fill=(240, 240, 235))
        num("36", 20)
    elif glyph == "5":  # Taiwan Strait: coastline, median line, arrows, ships
        band((16, 80, 96))
        d.polygon([(x + 8, y + 16), (x + 22, y + 16), (x + 26, y + h), (x + 10, y + h)],
                  fill=(196, 178, 128))
        d.polygon([(x + 96, y + 16), (x + 112, y + 16), (x + 108, y + h), (x + 92, y + h)],
                  fill=(214, 192, 140))
        for yy in range(y + 17, y + h, 5):
            d.line([(x + 58, yy), (x + 58, yy + 3)], fill=(250, 250, 245), width=2)
        for ay in (20, 27, 34):
            d.line([(x + 66, ay), (x + 82, ay)], fill=(232, 80, 60), width=2)
            d.polygon([(x + 82, ay - 2), (x + 88, ay), (x + 82, ay + 2)], fill=(232, 80, 60))
        for sx_ in (40, 74):
            d.polygon([(x + sx_, y + 33), (x + sx_ + 4, y + 29), (x + sx_ + 12, y + 29),
                       (x + sx_ + 16, y + 33)], fill=(230, 230, 230))
        num("5", 20)
    elif glyph == "M6.5":  # Vanuatu: seismograph trace, depth line, island
        band((48, 48, 56))
        pts = []
        for i in range(22):
            amp = 2 if i % 4 else (9 if i in (8, 9) else 5)
            pts.append((x + 10 + i * 3.4, y + 27 + (amp if i % 2 else -amp)))
        d.line(pts, fill=(80, 230, 130), width=2)
        d.line([(x + 92, y + 18), (x + 92, y + 36)], fill=(250, 205, 100), width=2)
        d.line([(x + 88, y + 36), (x + 96, y + 36)], fill=(250, 205, 100), width=2)
        d.ellipse([x + 118, y + 28, x + 126, y + 36], fill=(196, 178, 128))
        num("M6.5", 16)
    elif glyph == "TREASON":  # Lusaka: courthouse, columns, gavel
        band((66, 48, 42))
        d.polygon([(x + 12, y + 22), (x + 38, y + 16), (x + 64, y + 22)], fill=(205, 205, 210))
        for cx_ in (18, 30, 42, 54):
            d.rectangle([x + cx_, y + 22, x + cx_ + 5, y + 34], fill=(205, 205, 210))
        d.rectangle([x + 10, y + 34, x + 66, y + 36], fill=(205, 205, 210))
        d.line([(x + 84, y + 20), (x + 100, y + 28)], fill=(150, 110, 60), width=3)
        d.rectangle([x + 96, y + 24, x + 106, y + 30], fill=(120, 90, 50))
        d.line([(x + 84, y + 32), (x + 104, y + 32)], fill=(150, 110, 60), width=2)
        text(x + w - 56, y + 19, "TREASON", SANB(10), WHT)
    elif glyph == "176":  # Madrid: poll bars + 176 threshold line
        band((28, 40, 68))
        bars = [(16, 16, (38, 92, 140)), (38, 12, (178, 32, 26)), (60, 9, (44, 128, 60))]
        for bx, bh, bc in bars:
            d.rectangle([x + bx, y + h - 4 - bh, x + bx + 14, y + h - 4], fill=bc)
        d.line([(x + 8, y + 18), (x + 84, y + 18)], fill=(250, 205, 100), width=2)
        num("176", 18)
    elif glyph == "$225m":  # Hollywood: marquee, stars, ticket stubs
        band((80, 30, 60))
        d.rectangle([x + 10, y + 18, x + 66, y + 36], fill=(250, 244, 214),
                    outline=(198, 148, 32), width=1)
        text(x + 14, y + 21, "CINEMA", SANB(9), DARKRED)
        text(x + 14, y + 30, "NOW SHOWING", SAN(7), INK)
        for sx_, sy_ in [(76, 20), (88, 28), (100, 19)]:
            d.polygon([(x + sx_, sy_ - 3), (x + sx_ + 1, sy_), (x + sx_ + 3, sy_ - 3),
                       (x + sx_ + 1, sy_ + 3)], fill=(250, 205, 100))
        d.polygon([(x + 112, y + 24), (x + 128, y + 24), (x + 126, y + 32),
                   (x + 110, y + 32)], fill=(240, 240, 235))
        num("$225m", 15)
    elif glyph == "AWACS":  # Poland: AWACS plane, radar rings, map pin
        band((40, 62, 96))
        for r_ in (6, 12, 18):
            d.ellipse([x + 30 - r_, y + 26 - r_, x + 30 + r_, y + 26 + r_],
                      outline=(140, 190, 225), width=1)
        d.polygon([(x + 58, y + 24), (x + 66, y + 20), (x + 96, y + 20), (x + 104, y + 24),
                   (x + 96, y + 28), (x + 66, y + 28)], fill=(230, 230, 235))
        d.ellipse([x + 76, y + 16, x + 88, y + 21], fill=(200, 200, 210))
        d.polygon([(x + 104, y + 22), (x + 112, y + 19), (x + 112, y + 27)], fill=(200, 200, 210))
        d.ellipse([x + 118, y + 24, x + 124, y + 30], fill=RED, outline=WHT)
        num("AWACS", 13)

# ------------------------------------------------------------------ mains
SCENES = [scene_kyiv, scene_markets, scene_sanctions]
MY = ly + 28
MW = (CW - 30) // 3
for i, (num, region, place, tag, head, deck) in enumerate(MAINS):
    x = MX + i * (MW + 15)
    SCENES[i](x, MY, MW, 104)
    d.rectangle([x, MY, x + MW, MY + 104], outline=RULE, width=1)
    chip(x + MW - 6, MY + 6, tag, TAGC[tag], align="r")
    text(x + 2, MY + 110, f"{num}", SERB(15), DARKRED)
    text(x + 22, MY + 113, f"{place} · {region}", SANB(10), REG[region])
    para(x + 2, MY + 128, head, SERB(19), MW - 4, 23, INK, max_lines=2)
    para(x + 2, MY + 178, deck, SAN(10), MW - 4, 13.5, (52, 48, 42), max_lines=3)
rule(MX, W - MX, MY + 224, 1)

# ------------------------------------------------------------------ cards
CY = MY + 232
CWID = 155
for idx, (num, region, place, tag, glyph, head, deck) in enumerate(CARDS):
    r_, c_ = divmod(idx, 6)
    x = MX + c_ * (CWID + 8)
    y = CY + r_ * 118
    scene_card(x, y, CWID, 40, glyph)
    loctag(x + 4, y + 1, place)
    chip(x + CWID - 4, y + 1, tag, TAGC[tag], align="r")
    noff = tw(str(num), SANB(11)) + 7
    text(x + 2, y + 45, f"{num}", SANB(11), DARKRED)
    para(x + 2 + noff, y + 44, head, SANB(11), CWID - 4 - noff, 13.5, INK, max_lines=2)
    para(x + 2, y + 74, deck, SAN(8.5), CWID - 4, 11, (52, 48, 42), max_lines=2)
rule(MX, W - MX, CY + 228, 1)

# ------------------------------------------------------------------ map
BY = CY + 236
MAPY, MAPH, MAPW = BY + 18, 200, 330
text(MX, BY, "WHERE IT HAPPENED", SANB(11), NAVY)
text(MX + MAPW, BY, "pins = story numbers", SAN(9), MUTE, anchor="ra")
d.rectangle([MX, MAPY, MX + MAPW, MAPY + MAPH], fill=(228, 234, 226), outline=RULE)


def proj(lon, lat):
    return (MX + (lon + 170) / 350 * MAPW, MAPY + (78 - lat) / 145 * MAPH)


def land(pts, col=(196, 206, 188)):
    d.polygon([proj(a, b) for a, b in pts], fill=col)


# simplified continent outlines, drawn for this page
land([(-166, 68), (-140, 70), (-124, 71), (-108, 68), (-95, 69), (-86, 66),
      (-80, 73), (-76, 62), (-66, 58), (-56, 52), (-60, 46), (-68, 44),
      (-74, 39), (-76, 35), (-81, 25), (-84, 30), (-90, 29), (-97, 26),
      (-104, 23), (-109, 24), (-114, 29), (-120, 34), (-124, 42), (-126, 49),
      (-134, 58), (-152, 58), (-162, 58), (-166, 60)])
land([(-78, 8), (-70, 11), (-62, 10), (-54, 5), (-50, 0), (-44, -3), (-36, -8),
      (-40, -14), (-41, -22), (-49, -28), (-54, -34), (-58, -38), (-65, -45),
      (-69, -52), (-74, -44), (-72, -32), (-70, -20), (-76, -14), (-80, -6),
      (-81, -2), (-78, 2)])
land([(-10, 36), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (40, 15),
      (43, 12), (51, 12), (48, 6), (42, -2), (40, -10), (38, -18), (36, -26),
      (33, -28), (27, -33), (19, -35), (17, -30), (15, -22), (13, -12),
      (12, -6), (9, -1), (9, 4), (-8, 4), (-13, 8), (-17, 12), (-17, 20),
      (-16, 27), (-10, 31)])
land([(-9, 43), (-2, 48), (2, 50), (6, 54), (8, 57), (12, 56), (18, 56),
      (21, 60), (25, 60), (30, 61), (32, 70), (45, 68), (60, 69), (75, 72),
      (95, 76), (110, 74), (130, 72), (150, 70), (170, 67), (178, 65),
      (178, 62), (162, 60), (156, 52), (142, 50), (140, 44), (142, 40),
      (138, 36), (132, 34), (128, 38), (122, 38), (120, 34), (118, 25),
      (110, 20), (108, 12), (104, 6), (101, 8), (98, 14), (94, 17), (92, 21),
      (89, 22), (86, 20), (80, 15), (77, 8), (74, 13), (72, 20), (68, 23),
      (62, 25), (57, 27), (52, 29), (50, 26), (55, 24), (58, 22), (55, 17),
      (52, 15), (44, 12), (40, 20), (36, 28), (34, 28), (36, 36), (30, 36),
      (26, 38), (22, 37), (19, 40), (15, 38), (12, 42), (8, 44), (3, 43),
      (-2, 44), (-9, 43)])
land([(113, -22), (115, -34), (124, -33), (132, -32), (135, -35), (140, -38),
      (145, -38), (150, -37), (153, -31), (151, -24), (146, -19), (143, -15),
      (142, -11), (139, -21), (136, -15), (132, -11), (126, -14), (118, -20)])
land([(-5, 50), (-3, 53), (-5, 55), (-3, 57), (-1, 58), (0, 54), (1, 52)])
land([(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (142, 44),
      (140, 42), (138, 38), (135, 34), (132, 33)])
land([(167, -45), (170, -44), (172, -42), (174, -40), (176, -38), (174, -37),
      (172, -40), (170, -43), (168, -46)])
for cx_, cy_, s in [(100, 2, 16), (107, -3, 13), (113, -6, 12), (119, -3, 9)]:
    px, py = proj(cx_, cy_)
    d.ellipse([px - s / 2, py - 3, px + s / 2, py + 3], fill=(196, 206, 188))
PINS = [(1, 31, 50, "EUROPE"), (2, -74, 41, "AMERICAS"), (3, 4, 51, "EUROPE"),
        (4, 8.5, 47, "WORLD"), (5, -0.3, 51.5, "EUROPE"), (6, 34.5, 31.5, "MIDDLE EAST"),
        (8, -77, 39, "AMERICAS"), (9, -52.8, 5.2, "EUROPE"), (10, 120, 24, "ASIA-PACIFIC"),
        (11, 167, -16, "OCEANIA"), (12, 28.3, -15.4, "AFRICA"), (13, -3.7, 40.4, "EUROPE"),
        (14, -118.3, 34.1, "WORLD"), (15, 19, 52, "EUROPE")]
for num, lon, lat, region in PINS:
    px, py = proj(lon, lat)
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=REG[region],
              outline=(255, 255, 255), width=1)
    ctext(px, py - 6, str(num), SANB(9), (255, 255, 255))
d.rectangle([MX + 6, MAPY + MAPH - 26, MX + 196, MAPY + MAPH - 6], fill=(252, 250, 244),
            outline=RULE)
text(MX + 10, MAPY + MAPH - 22, "7 · GOLD & OIL — markets, not a place", SAN(9), INK)

# ------------------------------------------------------------------ ALSO
AX = MX + MAPW + 28
AW = (W - MX - AX - 14) // 2
text(AX, BY, "ALSO ON MONDAY 23 NOVEMBER", SANB(11), NAVY)
text(AX + tw("ALSO ON MONDAY 23 NOVEMBER", SANB(11)) + 8, BY + 1,
     "— 14 MORE STORIES", SAN(10), MUTE)
for k, (num, region, lead, body, src) in enumerate(ALSO):
    col = 0 if k < 7 else 1
    row = k % 7
    x = AX + col * (AW + 14)
    y = BY + 18 + row * 28
    # regular weight only in ALSO (user rule) — region colour carries the lead
    head = f"{num} {lead}: "
    text(x, y, head, SAN(10), REG[region])
    rest = body + f" ({src})"
    lines = wrap(rest, SAN(10), AW - tw(head, SAN(10)))
    if lines:
        text(x + tw(head, SAN(10)), y, lines[0], SAN(10))
        if len(lines) > 1:
            text(x, y + 12, lines[1], SAN(10))
        if len(lines) > 2:
            text(x, y + 24, lines[2], SAN(10))

# ------------------------------------------------------------------ date check + footer
DY = BY + 232
d.rectangle([MX, DY, W - MX, DY + 42], outline=DARKRED, width=1)
dcf = SAN(9)
dct = ("DATE CHECK — Left out as other days' news: COP31 collapse itself (Sun 22 Nov — Monday is the "
       "fallout) · F1 Las Vegas GP (Sat 21 Nov) · Wembanyama's 50 (Sat 21 Nov) · Peru M6.8 quake "
       "(Fri 20 Nov) · Russian missiles in Poland (Fri 20 Nov — Monday is NATO's AWACS reply) · "
       "Friday's market crash, Nasdaq −5.28% (Fri 20 Nov — Monday is the rally) · Sparta II strike "
       "(Sat 21 Nov). Not yet: CAS Senegal ruling (Tue 24 Nov) · MNF result, Bengals at Commanders "
       "(kicked off 20:15 ET Mon).")
for i, ln in enumerate(wrap(dct, dcf, CW - 16)[:3]):
    text(MX + 8, DY + 4 + i * 12, ln, dcf, (60, 30, 20))
fy = DY + 48
text(MX, fy, "Sources: Reuters · AP · AFP · Euronews · FIFA · European Commission · USGS · "
     "Screen Daily · Sky Sports · Arianespace · Taiwan MND · US Treasury · wires", SAN(8), MUTE)
text(MX, fy + 11, "CERTAINTY: CONFIRMED = two or more outlets · OFFICIAL = on the record · "
     "REPORTED = one outlet or witnesses · CLAIM = one side's account, labelled as such",
     SAN(8), MUTE)
text(W - MX, fy + 11, "Pictures are drawn illustrations, not photographs.",
     SAN(8), MUTE, anchor="ra")

img.save("entry.png")
img.resize((300, 300), Image.LANCZOS).save("entry-300.png")
img.resize((150, 150), Image.LANCZOS).save("entry-150.png")
print("saved entry.png", img.size)
print("tally:", dict(tally), "total:", sum(tally.values()))
