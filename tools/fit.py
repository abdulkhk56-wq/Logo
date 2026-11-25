"""Cubic-bezier fitting (Schneider, Graphics Gems 1990) with corner detection.
Turns the boolean/offset results of the construction into clean, compact
SVG paths: a handful of smooth cubic segments instead of polylines."""
import math
import numpy as np

def _bez(ctrl, t):
    t = np.asarray(t)[:, None]
    p0, p1, p2, p3 = ctrl
    return ((1-t)**3)*p0 + 3*((1-t)**2)*t*p1 + 3*(1-t)*t*t*p2 + (t**3)*p3

def _bez_d(ctrl, t):
    t = np.asarray(t)[:, None]; p0, p1, p2, p3 = ctrl
    return 3*((1-t)**2)*(p1-p0) + 6*(1-t)*t*(p2-p1) + 3*t*t*(p3-p2)

def _bez_dd(ctrl, t):
    t = np.asarray(t)[:, None]; p0, p1, p2, p3 = ctrl
    return 6*(1-t)*(p2-2*p1+p0) + 6*t*(p3-2*p2+p1)

def _chord(pts):
    d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
    return d / d[-1]

def _gen(pts, u, t1, t2):
    p0, p3 = pts[0], pts[-1]
    A1 = u[:, None] * 3 * (1-u)[:, None]**2 * t1
    A2 = (3 * u**2 * (1-u))[:, None] * t2
    C = np.zeros((2, 2)); X = np.zeros(2)
    C[0, 0] = (A1*A1).sum(); C[0, 1] = C[1, 0] = (A1*A2).sum(); C[1, 1] = (A2*A2).sum()
    tmp = pts - _bez(np.array([p0, p0, p3, p3]), u)
    X[0] = (A1*tmp).sum(); X[1] = (A2*tmp).sum()
    det = C[0, 0]*C[1, 1] - C[0, 1]*C[1, 0]
    seg = np.linalg.norm(p3 - p0)
    if abs(det) > 1e-12:
        a1 = (X[0]*C[1, 1] - X[1]*C[0, 1]) / det
        a2 = (C[0, 0]*X[1] - C[1, 0]*X[0]) / det
    else:
        a1 = a2 = seg / 3
    eps = 1e-6 * seg
    if a1 < eps or a2 < eps:
        a1 = a2 = seg / 3
    return np.array([p0, p0 + a1*t1, p3 + a2*t2, p3])

def _reparam(ctrl, pts, u):
    d = _bez(ctrl, u) - pts
    d1 = _bez_d(ctrl, u); d2 = _bez_dd(ctrl, u)
    num = (d*d1).sum(1); den = (d1*d1 + d*d2).sum(1)
    with np.errstate(divide="ignore", invalid="ignore"):
        nu = np.where(np.abs(den) > 1e-12, u - num/den, u)
    return np.clip(nu, 0, 1)

def _maxerr(ctrl, pts, u):
    d = np.linalg.norm(_bez(ctrl, u) - pts, axis=1)
    i = int(np.argmax(d)); return d[i], i

def _unit(v):
    n = np.linalg.norm(v); return v / n if n else v

def fit_open(pts, err, t1=None, t2=None):
    pts = np.asarray(pts, float)
    if t1 is None: t1 = _unit(pts[1] - pts[0])
    if t2 is None: t2 = _unit(pts[-2] - pts[-1])
    if len(pts) == 2:
        dist = np.linalg.norm(pts[1]-pts[0]) / 3
        return [np.array([pts[0], pts[0]+t1*dist, pts[1]+t2*dist, pts[1]])]
    q = pts - pts[0]; ch = pts[-1] - pts[0]; L = np.linalg.norm(ch)
    if L > 0 and np.abs(ch[0]*q[:, 1] - ch[1]*q[:, 0]).max() / L < err * 0.5 \
            and abs(float(_unit(ch) @ t1)) > 0.999 and abs(float(_unit(ch) @ t2)) > 0.999:
        return [("L", pts[-1])]
    u = _chord(pts)
    ctrl = _gen(pts, u, t1, t2)
    e, split = _maxerr(ctrl, pts, u)
    if e < err: return [ctrl]
    if e < err * 4:
        for _ in range(20):
            u = _reparam(ctrl, pts, u); ctrl = _gen(pts, u, t1, t2)
            e, split = _maxerr(ctrl, pts, u)
            if e < err: return [ctrl]
    split = min(max(split, 1), len(pts) - 2)
    tc = _unit(pts[split-1] - pts[split+1])
    return fit_open(pts[:split+1], err, t1, tc) + fit_open(pts[split:], err, -tc, t2)

def resample(ring, step):
    """Uniform resample of a closed ring (list of xy, first != last)."""
    r = np.asarray(ring, float); r = np.vstack([r, r[:1]])
    seg = np.linalg.norm(np.diff(r, axis=0), axis=1)
    L = seg.sum(); n = max(int(L / step), 12)
    cum = np.r_[0, np.cumsum(seg)]
    s = np.linspace(0, L, n, endpoint=False)
    x = np.interp(s, cum, r[:, 0]); y = np.interp(s, cum, r[:, 1])
    return np.c_[x, y]

def corners(ring, ang_deg=35, win=3):
    r = np.asarray(ring); n = len(r); out = []
    for i in range(n):
        a = r[(i-win) % n]; b = r[i]; c = r[(i+win) % n]
        v1 = _unit(b-a); v2 = _unit(c-b)
        ang = math.degrees(math.acos(max(-1, min(1, float(v1 @ v2)))))
        if ang > ang_deg: out.append((i, ang))
    # keep local maxima only
    keep = []
    for i, ang in out:
        if all(not (abs(i-j) <= win*2 or abs(i-j) >= n-win*2) or ang >= a2 for j, a2 in out):
            keep.append(i)
    return sorted(set(keep))

def fit_ring(ring, err=0.08, ang=35, step=0.25, corner_pts=None):
    """Fit closed ring. corner_pts: exact corner coordinates to snap to."""
    r = resample(ring, step)
    if corner_pts:
        idx = sorted({int(np.argmin(np.linalg.norm(r - np.array(c), axis=1))) for c in corner_pts})
        for c in corner_pts:
            j = int(np.argmin(np.linalg.norm(r - np.array(c), axis=1))); r[j] = c
    else:
        idx = corners(r, ang)
    if not idx:
        idx = [0]
    n = len(r); segs = []
    for k in range(len(idx)):
        i0 = idx[k]; i1 = idx[(k+1) % len(idx)]
        if i1 <= i0: i1 += n
        pts = np.array([r[j % n] for j in range(i0, i1+1)])
        # straight run?
        chord = pts[-1] - pts[0]; L = np.linalg.norm(chord)
        if L > 0:
            q = pts - pts[0]; cu = chord / L
            dev = np.abs(cu[0]*q[:, 1] - cu[1]*q[:, 0]).max()
            if dev < err:
                segs.append(("L", pts[-1])); continue
        for c in fit_open(pts, err):
            segs.append(c if isinstance(c, tuple) else ("C", c))
    start = r[idx[0]]
    return start, segs

def ring_to_d(start, segs, nd=2):
    fm = lambda v: (f"{v:.{nd}f}").rstrip("0").rstrip(".").replace("-0", "0") if abs(v) >= 10**-nd else "0"
    p = lambda q: f"{fm(q[0])} {fm(q[1])}"
    s = "M" + p(start)
    for kind, v in segs:
        if kind == "L": s += " L" + p(v)
        else: s += " C" + p(v[1]) + " " + p(v[2]) + " " + p(v[3])
    return s + "Z"
