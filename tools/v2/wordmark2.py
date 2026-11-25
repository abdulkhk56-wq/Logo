"""Provisional SAFI wordmark (black only), built from exact primitives.
Cap height 100, stroke 15. Used identically with every concept so the
comparison is about the symbol. Final typography follows symbol approval."""
from shapely.geometry import box, Polygon
from shapely.ops import unary_union
from shapely import affinity
from exact import disc

H, T = 100.0, 15.0
SLOPE = 0.375

def glyph_S(W=80):
    h = T/2; r = (H/2 - h)/2           # bowl centre-line radius
    c1 = (h + r, h + r); c2 = (W - h - r, H/2 + r)
    ring = lambda c: disc(c, r + h).difference(disc(c, r - h))
    k = SLOPE * T
    parts = [
        box(c1[0], 0, W, T),                                   # top bar
        ring(c1).intersection(box(0, 0, c1[0], H/2 + h)),     # upper bowl
        box(c1[0], H/2 - h, c2[0], H/2 + h),                   # spine
        ring(c2).intersection(box(c2[0], H/2 - h, W, H)),     # lower bowl
        box(0, H - T, c2[0], H),                               # bottom bar
    ]
    g = unary_union(parts)
    g = g.difference(Polygon([(W - k, 0), (W, T), (W + 5, T), (W + 5, -1), (W - k, -1)]))
    g = g.difference(Polygon([(k, H), (0, H - T), (-5, H - T), (-5, H + 1), (k, H + 1)]))
    circles = [(c1, r + h), (c1, r - h), (c2, r + h), (c2, r - h)]
    return g, W, circles

def glyph_A(W=92, ap=8.5, bar_y=64):
    import math
    L = math.hypot(W/2 - ap, H); tx = T * L / H
    left = Polygon([(0, H), (tx, H), (W/2 - ap + tx, 0), (W/2 - ap, 0)])
    right = Polygon([(W, H), (W - tx, H), (W/2 + ap - tx, 0), (W/2 + ap, 0)])
    outer = Polygon([(0, H), (W/2 - ap, 0), (W/2 + ap, 0), (W, H)])
    bar = box(0, bar_y, W, bar_y + T * 0.92).intersection(outer)
    return unary_union([left, right, bar]), W, []

def glyph_F(W=68):
    return unary_union([box(0, 0, T, H), box(0, 0, W, T), box(0, H/2 - T/2 + 2, W*0.86, H/2 + T/2 + 2)]), W, []

def glyph_I():
    return box(0, 0, T, H), T, []

GAPS = [17, 15, 13]

def wordmark():
    x = 0; geoms = []; circles = []
    for i, (g, w, cs) in enumerate([glyph_S(), glyph_A(), glyph_F(), glyph_I()]):
        geoms.append(affinity.translate(g, x, 0))
        circles += [((c[0] + x, c[1]), r) for c, r in cs]
        x += w + (GAPS[i] if i < 3 else 0)
    return unary_union(geoms), x, circles
