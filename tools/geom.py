"""Tiny analytic geometry kit used to construct the SAFI symbol.
All shapes are built from circular arcs + straight lines, so every
exported path is exact (no sampling, no booleans, no raster)."""
import math

def f(v):
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s

def circ_circ(c1, r1, c2, r2):
    (x1, y1), (x2, y2) = c1, c2
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy)
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(max(r1 * r1 - a * a, 0))
    xm, ym = x1 + a * dx / d, y1 + a * dy / d
    return [(xm + h * dy / d, ym - h * dx / d), (xm - h * dy / d, ym + h * dx / d)]

def circ_hline(c, r, y):
    cx, cy = c
    h = math.sqrt(r * r - (y - cy) ** 2)
    return [(cx - h, y), (cx + h, y)]

def circ_vline(c, r, x):
    cx, cy = c
    h = math.sqrt(r * r - (x - cx) ** 2)
    return [(x, cy - h), (x, cy + h)]

def arc(r, p, sweep, large=0):
    return f"A{f(r)} {f(r)} 0 {large} {sweep} {f(p[0])} {f(p[1])}"

def M(p): return f"M{f(p[0])} {f(p[1])}"
def L(p): return f"L{f(p[0])} {f(p[1])}"
