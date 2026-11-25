"""Final SAFI symbol (Laminar) and wordmark, exact geometry."""
from shapely.geometry import box, Polygon
from shapely.ops import unary_union
from shapely import affinity
import concepts as K
from exact import disc, to_d
import math

# ---------------------------------------------------------------- symbol
def symbol(small=False):
    """Master: plates 24 / gap 12. Small-size cut (<= 24px): gaps opened to 16
    by trimming the plates' inner edges, so the gaps survive pixel snapping."""
    F = K.F
    if small:
        plates = unary_union([box(12, -10, 34, 130), box(50, -10, 72, 130), box(88, -10, 108, 130)])
    else:
        plates = unary_union([box(12, -10, 36, 130), box(48, -10, 72, 130), box(84, -10, 108, 130)])
    g = F.geom().intersection(plates)
    return g, F.circles()

# ---------------------------------------------------------------- wordmark
# Cap height 100, stroke 16. Strokes, terminals and joins are vertical or
# horizontal like the plates; the only diagonals are the A's legs.
H, T = 100.0, 16.0

def S(W=82):
    h = T/2; r = (H/2 - h)/2
    c1 = (h + r, h + r); c2 = (W - h - r, H/2 + r)
    ring = lambda c: disc(c, r + h).difference(disc(c, r - h))
    g = unary_union([box(c1[0], 0, W - 2, T), ring(c1).intersection(box(0, 0, c1[0], H/2 + h)),
                     box(c1[0], H/2 - h, c2[0], H/2 + h), ring(c2).intersection(box(c2[0], H/2 - h, W, H)),
                     box(2, H - T, c2[0], H)])
    return g, W, [(c1, r + h), (c1, r - h), (c2, r + h), (c2, r - h)]

def A(W=94, ap=9, bar_y=62):
    L = math.hypot(W/2 - ap, H); tx = T * L / H
    left = Polygon([(0, H), (tx, H), (W/2 - ap + tx, 0), (W/2 - ap, 0)])
    right = Polygon([(W, H), (W - tx, H), (W/2 + ap - tx, 0), (W/2 + ap, 0)])
    outer = Polygon([(0, H), (W/2 - ap, 0), (W/2 + ap, 0), (W, H)])
    return unary_union([left, right, box(0, bar_y, W, bar_y + T).intersection(outer)]), W, []

def Fg(W=70):
    return unary_union([box(0, 0, T, H), box(0, 0, W, T), box(0, 44, W - 8, 44 + T)]), W, []

def I():
    return box(0, 0, T, H), T, []

# letter gaps: optical spacing on a 24-unit base (= the plate gap at lockup scale)
GAPS = [22, 20, 26]

def wordmark():
    x = 0; gs = []; cs = []
    for i, (g, w, c) in enumerate([S(), A(), Fg(), I()]):
        gs.append(affinity.translate(g, x, 0)); cs += [((p[0] + x, p[1]), r) for p, r in c]
        x += w + (GAPS[i] if i < 3 else 0)
    return unary_union(gs), x, cs
