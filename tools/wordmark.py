"""SAFI wordmark — custom-drawn, extended technical capitals.
Cap height 100, stroke 16. Rounded-stadium S, flat-apex A, open F, plain I."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from shapely.geometry import Polygon, LineString, box
from shapely.ops import unary_union
from shapes import polys
from fit import fit_ring, ring_to_d

H = 100.0
T = 15.0
SLOPE = 0.375   # dx/dy of the A legs; reused for the S terminal cuts

def arc_pts(cx, cy, r, a0, a1, n=96):
    return [(cx + r*math.cos(math.radians(a0 + (a1-a0)*k/n)),
             cy + r*math.sin(math.radians(a0 + (a1-a0)*k/n))) for k in range(n+1)]

def glyph_S(W=80):
    h = T/2; y0, y1, ym = h, H-h, H/2
    r = (ym - y0) / 2
    xl, xr = h, W - h
    pts = [(W + 6, y0)]                           # top terminal (cut below)
    pts += [(xl + r, y0)]
    pts += arc_pts(xl + r, y0 + r, r, -90, -270)   # left upper bowl (ccw)
    pts += [(xr - r, ym)]
    pts += arc_pts(xr - r, ym + r, r, -90, 90)     # right lower bowl (cw)
    pts += [(-6, y1)]                              # bottom terminal
    g = LineString(pts).buffer(h, cap_style="flat", join_style="round", quad_segs=48)
    # terminals cut on the A-leg angle: parallel slants tie S to A and give the
    # word a forward, upward lean (an echo of the flame tip)
    k = SLOPE * T
    cut_top = Polygon([(W - k, 0), (W, T), (W + 20, T), (W + 20, -1), (W - k, -1)])
    cut_bot = Polygon([(k, H), (0, H - T), (-20, H - T), (-20, H + 1), (k, H + 1)])
    return g.difference(cut_top).difference(cut_bot), W

def glyph_A(W=92, ap=8.5, bar_y=64):
    L = math.hypot(W/2 - ap, H); tx = T * L / H
    left = Polygon([(0, H), (tx, H), (W/2 - ap + tx, 0), (W/2 - ap, 0)])
    right = Polygon([(W, H), (W - tx, H), (W/2 + ap - tx, 0), (W/2 + ap, 0)])
    bar = box(0, bar_y, W, bar_y + T * 0.92)
    outer = Polygon([(0, H), (W/2 - ap, 0), (W/2 + ap, 0), (W, H)])
    g = unary_union([left, right, bar.intersection(outer)])
    return g.intersection(box(0, 0, W, H)), W

def glyph_F(W=68):
    g = unary_union([box(0, 0, T, H), box(0, 0, W, T), box(0, H/2 - T/2 + 2, W * 0.86, H/2 + T/2 + 2)])
    return g, W

def glyph_I():
    return box(0, 0, T, H), T

GAPS = [17, 15, 13]  # S|A, A|F, F|I

def wordmark(err=0.04):
    from shapely import affinity
    gl = [glyph_S(), glyph_A(), glyph_F(), glyph_I()]
    x = 0; paths = []; geoms = []
    for i, (g, w) in enumerate(gl):
        g2 = affinity.translate(g, x, 0); geoms.append(g2)
        for p in polys(g2):
            for ring in [p.exterior] + list(p.interiors):
                s, segs = fit_ring(list(ring.coords)[:-1], err=err, ang=28, step=0.2)
                paths.append(ring_to_d(s, segs))
        x += w + (GAPS[i] if i < len(GAPS) else 0)
    return " ".join(paths), x  # d, total width

if __name__ == "__main__":
    d, w = wordmark(); print(w, len(d))
