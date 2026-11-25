"""Exact SVG export for shapes built from circles and straight lines.

Shapes are composed with shapely booleans (dense polygons), then every
boundary segment is matched back to the construction primitive it lies on.
Runs on a circle become a single SVG arc (true circle, known centre and
radius); everything else becomes straight lines, merged when collinear.
The output therefore contains only the circles of the construction drawing
and straight edges: no Beziers, no sampling error."""
import math
from shapely.geometry import Point, MultiPolygon
from shapely.geometry.polygon import orient

QS = 1024   # quad segments for circle polygons

def disc(c, r):
    return Point(*c).buffer(r, quad_segs=QS)

def fmt(v):
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s

def _on(c, r, p, eps):
    return abs(math.hypot(p[0]-c[0], p[1]-c[1]) - r) < eps

def ring_path(coords, circles, eps=0.02):
    pts = list(coords)[:-1]
    n = len(pts)
    # label every edge i -> i+1
    lab = []
    for i in range(n):
        a, b = pts[i], pts[(i+1) % n]
        m = ((a[0]+b[0])/2, (a[1]+b[1])/2)
        hit = None
        L = math.hypot(b[0]-a[0], b[1]-a[1])
        for k, (c, r) in enumerate(circles):
            # chord midpoint sits inside the circle by the sagitta
            sag = r - math.sqrt(max(r*r - (L/2)**2, 0))
            if _on(c, r, a, eps) and _on(c, r, b, eps) and abs(math.hypot(m[0]-c[0], m[1]-c[1]) - (r - sag)) < eps and L < r * 0.2:
                hit = k; break
        lab.append(hit)
    # rotate so we start at a label change
    start = 0
    for i in range(n):
        if lab[i] != lab[i-1]:
            start = i; break
    pts = pts[start:] + pts[:start]; lab = lab[start:] + lab[:start]
    # group runs
    groups = []
    for i in range(n):
        if groups and groups[-1][0] == lab[i] and lab[i] is not None:
            groups[-1][1].append(i)
        else:
            groups.append([lab[i], [i]])
    out = [f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"]
    last_dir = None; buf_end = None
    def flush_line():
        nonlocal buf_end, last_dir
        if buf_end is not None:
            out.append(f"L{fmt(buf_end[0])} {fmt(buf_end[1])}")
        buf_end = None; last_dir = None
    for k, idx in groups:
        a = pts[idx[0]]; b = pts[(idx[-1]+1) % n]
        if k is None:
            # straight edges; merge collinear
            for i in idx:
                p, q = pts[i], pts[(i+1) % n]
                d = math.atan2(q[1]-p[1], q[0]-p[0])
                if last_dir is not None and abs((d - last_dir + math.pi) % (2*math.pi) - math.pi) < 1e-3:
                    buf_end = q
                else:
                    flush_line(); buf_end = q; last_dir = d
                if math.hypot(q[0]-p[0], q[1]-p[1]) < 1e-9: pass
            continue
        flush_line()
        c, r = circles[k]
        # signed sweep (screen coords, y down: positive = clockwise)
        tot = 0
        for i in idx:
            p, q = pts[i], pts[(i+1) % n]
            a1 = math.atan2(p[1]-c[1], p[0]-c[0]); a2 = math.atan2(q[1]-c[1], q[0]-c[0])
            tot += (a2 - a1 + math.pi) % (2*math.pi) - math.pi
        sweep = 1 if tot > 0 else 0
        large = 1 if abs(tot) > math.pi else 0
        if abs(abs(tot) - 2*math.pi) < 1e-3:   # full circle: split in two
            mid = pts[idx[len(idx)//2]]
            out.append(f"A{fmt(r)} {fmt(r)} 0 0 {sweep} {fmt(mid[0])} {fmt(mid[1])}")
        out.append(f"A{fmt(r)} {fmt(r)} 0 {large} {sweep} {fmt(b[0])} {fmt(b[1])}")
    flush_line()
    return " ".join(out) + "Z"

def to_d(geom, circles, eps=0.02):
    polys = list(geom.geoms) if isinstance(geom, MultiPolygon) else [geom]
    parts = []
    for p in polys:
        p = orient(p, sign=-1.0)  # exterior clockwise on screen
        parts.append(ring_path(p.exterior.coords, circles, eps))
        for hole in p.interiors:
            parts.append(ring_path(hole.coords, circles, eps))
    return " ".join(parts)
