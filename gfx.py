"""Tiny stdlib-only raster engine: anti-aliased polygons, outline text, PNG writer."""
import math
import struct
import zlib

from fontdata import FONTS

INF = 10 ** 6


def coverage(contours, ss, cx0, cx1, cy0, cy1):
    """Nonzero-winding polygon coverage. Returns (bx0, {y: [cov floats]})."""
    cross = {}
    minx = INF
    maxx = -INF
    for pts in contours:
        n = len(pts)
        for i in range(n):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % n]
            if x1 < minx:
                minx = x1
            if x1 > maxx:
                maxx = x1
            if y1 == y2:
                continue
            d = 1
            if y1 > y2:
                x1, y1, x2, y2 = x2, y2, x1, y1
                d = -1
            k0 = math.ceil(y1 * ss - 0.5)
            k1 = math.ceil(y2 * ss - 0.5)
            if k0 < cy0 * ss:
                k0 = cy0 * ss
            if k1 > cy1 * ss:
                k1 = cy1 * ss
            if k0 >= k1:
                continue
            dx = (x2 - x1) / (y2 - y1)
            for k in range(k0, k1):
                x = x1 + ((k + 0.5) / ss - y1) * dx
                lst = cross.get(k)
                if lst is None:
                    cross[k] = [(x, d)]
                else:
                    lst.append((x, d))
    if not cross:
        return 0, {}
    bx0 = max(cx0, int(math.floor(minx)))
    bx1 = min(cx1, int(math.ceil(maxx)) + 1)
    width = bx1 - bx0
    if width <= 0:
        return 0, {}
    wgt = 1.0 / ss
    accs = {}
    for k, lst in cross.items():
        lst.sort()
        y = k // ss
        a = accs.get(y)
        if a is None:
            a = ([0.0] * (width + 2), [0.0] * (width + 2))
            accs[y] = a
        acc, dif = a
        wind = 0
        start = 0.0
        for x, d in lst:
            prev = wind
            wind += d
            if prev == 0 and wind != 0:
                start = x
            elif prev != 0 and wind == 0:
                xa = start - bx0
                xb = x - bx0
                if xa < 0:
                    xa = 0.0
                if xb > width:
                    xb = float(width)
                if xb <= xa:
                    continue
                ia = int(xa)
                ib = int(xb)
                if ia == ib:
                    acc[ia] += (xb - xa) * wgt
                else:
                    acc[ia] += (ia + 1 - xa) * wgt
                    dif[ia + 1] += wgt
                    dif[ib] -= wgt
                    acc[ib] += (xb - ib) * wgt
    rows = {}
    for y, (acc, dif) in accs.items():
        run = 0.0
        out = [0.0] * width
        for i in range(width):
            run += dif[i]
            out[i] = acc[i] + run
        rows[y] = out
    return bx0, rows


def ellipse_pts(cx, cy, rx, ry, a0=0.0, a1=2 * math.pi, n=None):
    if n is None:
        n = max(10, min(72, int(max(rx, ry) * 1.3) + 8))
    full = abs(a1 - a0) >= 2 * math.pi - 1e-9
    pts = []
    steps = n if full else n + 1
    for i in range(steps):
        t = a0 + (a1 - a0) * i / n
        pts.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
    return pts


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.buf = bytearray(bytes(bg) * (w * h))
        self.cl = (0, 0, w, h)
        self.gcache = {}
        self.gamma = [min(255, int(255 * ((i / 255.0) ** 0.78) + 0.5)) for i in range(256)]

    # ---- clip -------------------------------------------------------
    def clip(self, x0, y0, x1, y1):
        self.cl = (max(0, int(x0)), max(0, int(y0)), min(self.w, int(x1)), min(self.h, int(y1)))

    def unclip(self):
        self.cl = (0, 0, self.w, self.h)

    # ---- pixel level -----------------------------------------------
    def px(self, x, y, col, a=1.0):
        cx0, cy0, cx1, cy1 = self.cl
        if x < cx0 or x >= cx1 or y < cy0 or y >= cy1:
            return
        p = (y * self.w + x) * 3
        b = self.buf
        if a >= 0.999:
            b[p], b[p + 1], b[p + 2] = col
        else:
            b[p] = int(b[p] + (col[0] - b[p]) * a + 0.5)
            b[p + 1] = int(b[p + 1] + (col[1] - b[p + 1]) * a + 0.5)
            b[p + 2] = int(b[p + 2] + (col[2] - b[p + 2]) * a + 0.5)

    def get(self, x, y):
        p = (y * self.w + x) * 3
        return tuple(self.buf[p:p + 3])

    # ---- shapes ----------------------------------------------------
    def rect(self, x0, y0, x1, y1, col, a=1.0):
        cx0, cy0, cx1, cy1 = self.cl
        x0 = max(int(round(x0)), cx0)
        x1 = min(int(round(x1)), cx1)
        y0 = max(int(round(y0)), cy0)
        y1 = min(int(round(y1)), cy1)
        if x1 <= x0 or y1 <= y0:
            return
        b = self.buf
        w = self.w
        if a >= 0.999:
            chunk = bytes(col) * (x1 - x0)
            for y in range(y0, y1):
                o = (y * w + x0) * 3
                b[o:o + len(chunk)] = chunk
        else:
            r, g, bl = col
            for y in range(y0, y1):
                o = (y * w + x0) * 3
                for i in range(x1 - x0):
                    p = o + 3 * i
                    b[p] = int(b[p] + (r - b[p]) * a + 0.5)
                    b[p + 1] = int(b[p + 1] + (g - b[p + 1]) * a + 0.5)
                    b[p + 2] = int(b[p + 2] + (bl - b[p + 2]) * a + 0.5)

    def frame(self, x0, y0, x1, y1, col, t=1, a=1.0):
        self.rect(x0, y0, x1, y0 + t, col, a)
        self.rect(x0, y1 - t, x1, y1, col, a)
        self.rect(x0, y0, x0 + t, y1, col, a)
        self.rect(x1 - t, y0, x1, y1, col, a)

    def vgrad(self, x0, y0, x1, y1, c0, c1):
        n = max(1, int(y1 - y0))
        for i in range(n):
            t = i / max(1, n - 1)
            col = tuple(int(c0[k] + (c1[k] - c0[k]) * t + 0.5) for k in range(3))
            self.rect(x0, y0 + i, x1, y0 + i + 1, col)

    def polys(self, contours, col, a=1.0, ss=4):
        cx0, cy0, cx1, cy1 = self.cl
        bx0, rows = coverage(contours, ss, cx0, cx1, cy0, cy1)
        if not rows:
            return
        b = self.buf
        w = self.w
        r, g, bl = col
        opaque = a >= 0.999
        cb = bytes(col)
        for y, cv in rows.items():
            o = (y * w + bx0) * 3
            for i, c in enumerate(cv):
                if c < 0.01:
                    continue
                p = o + 3 * i
                if opaque and c > 0.99:
                    b[p:p + 3] = cb
                else:
                    k = c * a
                    b[p] = int(b[p] + (r - b[p]) * k + 0.5)
                    b[p + 1] = int(b[p + 1] + (g - b[p + 1]) * k + 0.5)
                    b[p + 2] = int(b[p + 2] + (bl - b[p + 2]) * k + 0.5)

    def poly(self, pts, col, a=1.0, ss=4):
        self.polys([pts], col, a, ss)

    def ellipse(self, cx, cy, rx, ry, col, a=1.0):
        self.poly(ellipse_pts(cx, cy, rx, ry), col, a)

    def circle(self, cx, cy, r, col, a=1.0):
        self.poly(ellipse_pts(cx, cy, r, r), col, a)

    def ring(self, cx, cy, r, t, col, a=1.0):
        n = max(14, min(90, int(r * 1.4) + 10))
        o = ellipse_pts(cx, cy, r, r, n=n)
        i = ellipse_pts(cx, cy, max(0.1, r - t), max(0.1, r - t), n=n)[::-1]
        self.polys([o, i], col, a)

    def arc(self, cx, cy, r, a0, a1, t, col, a=1.0):
        n = max(8, int(r * abs(a1 - a0) * 0.7) + 6)
        o = ellipse_pts(cx, cy, r, r, a0, a1, n)
        i = ellipse_pts(cx, cy, r - t, r - t, a0, a1, n)[::-1]
        self.poly(o + i, col, a)

    def line(self, x0, y0, x1, y1, t, col, a=1.0):
        dx, dy = x1 - x0, y1 - y0
        d = math.hypot(dx, dy)
        if d == 0:
            return
        nx, ny = -dy / d * t / 2, dx / d * t / 2
        self.poly([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)], col, a)

    def dline(self, x0, y0, x1, y1, t, col, a=1.0, dash=5, gap=3):
        dx, dy = x1 - x0, y1 - y0
        d = math.hypot(dx, dy)
        if d == 0:
            return
        ux, uy = dx / d, dy / d
        s = 0.0
        while s < d:
            e = min(d, s + dash)
            self.line(x0 + ux * s, y0 + uy * s, x0 + ux * e, y0 + uy * e, t, col, a)
            s += dash + gap

    def polyline(self, pts, t, col, a=1.0):
        for i in range(len(pts) - 1):
            self.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], t, col, a)

    def glow(self, cx, cy, r, col, a=0.5, steps=7):
        for i in range(steps):
            k = (i + 1) / steps
            self.circle(cx, cy, r * (1 - k * 0.85), col, a / steps * 1.6)

    def cone(self, x, y, tx0, tx1, ty, col, a=0.25):
        self.poly([(x, y), (tx0, ty), (tx1, ty)], col, a)

    # ---- text ------------------------------------------------------
    def _glyph(self, font, ch, size, fbin):
        key = (font, ch, size, fbin)
        g = self.gcache.get(key)
        if g is not None:
            return g
        upm, gl = FONTS[font]
        if ch not in gl:
            ch = "?"
        adv, cs = gl[ch]
        sc = size / upm
        fx = fbin / 4.0
        contours = []
        for flat in cs:
            pts = [(flat[i] * sc + fx, -flat[i + 1] * sc) for i in range(0, len(flat), 2)]
            contours.append(pts)
        bx0, rows = coverage(contours, 6, -INF // 2, INF // 2, -INF // 2, INF // 2) if contours else (0, {})
        gm = self.gamma
        mask = []
        for y, cv in sorted(rows.items()):
            mask.append((y, bx0, bytes(gm[min(255, int(c * 255 + 0.5))] for c in cv)))
        g = (adv * sc, mask)
        self.gcache[key] = g
        return g

    def tw(self, s, font, size, sp=0.0):
        upm, gl = FONTS[font]
        sc = size / upm
        t = 0.0
        for ch in s:
            e = gl.get(ch) or gl["?"]
            t += e[0] * sc + sp
        return t

    def text(self, x, y, s, font, size, col, anchor="l", a=1.0, sp=0.0):
        """y is the baseline. Returns width."""
        w = self.tw(s, font, size, sp)
        if anchor == "c":
            x -= w / 2
        elif anchor == "r":
            x -= w
        cx0, cy0, cx1, cy1 = self.cl
        b = self.buf
        W = self.w
        pen = x
        r, g, bl = col
        ka = a / 255.0
        yi = int(round(y))
        for ch in s:
            if ch == " ":
                pen += self.tw(" ", font, size, sp)
                continue
            ix = int(math.floor(pen))
            fb = int((pen - ix) * 4)
            adv, mask = self._glyph(font, ch, size, fb)
            for dy, dx0, row in mask:
                yy = yi + dy
                if yy < cy0 or yy >= cy1:
                    continue
                base = (yy * W) * 3
                for i, v in enumerate(row):
                    if v < 6:
                        continue
                    xx = ix + dx0 + i
                    if xx < cx0 or xx >= cx1:
                        continue
                    p = base + xx * 3
                    if v > 248 and a >= 0.999:
                        b[p] = r
                        b[p + 1] = g
                        b[p + 2] = bl
                    else:
                        k = v * ka
                        b[p] = int(b[p] + (r - b[p]) * k + 0.5)
                        b[p + 1] = int(b[p + 1] + (g - b[p + 1]) * k + 0.5)
                        b[p + 2] = int(b[p + 2] + (bl - b[p + 2]) * k + 0.5)
            e = FONTS[font][1].get(ch) or FONTS[font][1]["?"]
            pen += e[0] * size / FONTS[font][0] + sp
        return w

    def wrap(self, s, font, size, maxw, sp=0.0):
        words = s.split(" ")
        lines = []
        cur = ""
        for wd in words:
            t = wd if not cur else cur + " " + wd
            if self.tw(t, font, size, sp) <= maxw or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, s, font, size, col, maxw, lh, maxlines=99, a=1.0):
        """Draw wrapped text; y = baseline of first line. Returns number of lines drawn."""
        lines = self.wrap(s, font, size, maxw)
        for i, ln in enumerate(lines[:maxlines]):
            self.text(x, y + i * lh, ln, font, size, col, "l", a)
        return min(len(lines), maxlines), len(lines)

    # ---- output ----------------------------------------------------
    def png_bytes(self, filt=2):
        w, h = self.w, self.h
        stride = w * 3
        raw = bytearray()
        buf = self.buf
        prev = bytes(stride)
        for y in range(h):
            row = bytes(buf[y * stride:(y + 1) * stride])
            if filt == 2:
                raw.append(2)
                raw += bytes((a - b) & 255 for a, b in zip(row, prev))
            else:
                raw.append(0)
                raw += row
            prev = row

        def chunk(tag, data):
            c = struct.pack(">I", len(data)) + tag + data
            return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

        out = b"\x89PNG\r\n\x1a\n"
        out += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
        out += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        out += chunk(b"IEND", b"")
        return out
