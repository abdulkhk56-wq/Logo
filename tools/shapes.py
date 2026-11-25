"""Path sampling + boolean helpers (shapely) used during symbol construction."""
import re, math
from shapely.geometry import Polygon, LineString, MultiPolygon
from shapely.ops import unary_union

def _tok(d):
    return re.findall(r"[MLCZHVA]|-?\d*\.?\d+(?:e-?\d+)?", d)

def sample(d, n=64):
    """Sample an absolute M/L/C/Z path into point lists (one per subpath)."""
    t = _tok(d); i = 0; cur = None; out = []; pts = []
    cmd = None
    def num():
        nonlocal i; v = float(t[i]); i += 1; return v
    while i < len(t):
        if t[i] in "MLCZ":
            cmd = t[i]; i += 1
            if cmd == "Z":
                if pts: out.append(pts); pts = []
                continue
        if cmd == "M":
            if pts: out.append(pts)
            cur = (num(), num()); pts = [cur]; cmd = "L"
        elif cmd == "L":
            cur = (num(), num()); pts.append(cur)
        elif cmd == "C":
            p1 = (num(), num()); p2 = (num(), num()); p3 = (num(), num())
            p0 = cur
            for k in range(1, n + 1):
                s = k / n; a = (1 - s) ** 3; b = 3 * (1 - s) ** 2 * s; c = 3 * (1 - s) * s * s; e = s ** 3
                pts.append((a*p0[0]+b*p1[0]+c*p2[0]+e*p3[0], a*p0[1]+b*p1[1]+c*p2[1]+e*p3[1]))
            cur = p3
    if pts: out.append(pts)
    return out

def poly(d, n=96):
    return unary_union([Polygon(p).buffer(0) for p in sample(d, n)])

def line(d, n=96):
    return LineString(sample(d, n)[0])

def polys(g):
    if isinstance(g, MultiPolygon): return list(g.geoms)
    if g.is_empty: return []
    return [g]

def to_path(g, nd=2):
    """Polygon(s) -> SVG path (polyline, preview only)."""
    out = []
    for p in polys(g):
        for ring in [p.exterior] + list(p.interiors):
            c = list(ring.coords)[:-1]
            out.append("M" + " L".join(f"{x:.{nd}f} {y:.{nd}f}" for x, y in c) + "Z")
    return " ".join(out)
