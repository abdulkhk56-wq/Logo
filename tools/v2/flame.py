"""The SAFI flame primitive, constructed with compass and straight-edge.

Grid: 120 x 120 artboard, module u = 6 (20 x 20 grid). Base line y = 108.
  1. Two flank circles, R = 16u = 96, centres F_L = (108, 84) and F_R = (12, 84).
     Their lens is the flame body (a pointed arch), width 96 = 16u.
  2. The main tongue tip T is the point of the right-flank circle at x = TX.
     The secondary tongue tip T2 is the point of the left-flank circle at x = T2X.
  3. The notch N sits on the grid. Two concave circles carve the notch:
     radius RM through N and T (centre above-left), radius RS through N and T2
     (centre above-right).
  4. The lens is cut flat at the base line; both foot corners get a fillet of
     radius RC, tangent to the base and to the flank circle.
"""
import math
from shapely.geometry import box
from exact import disc

def cc(c1, r1, c2, r2):
    (x1, y1), (x2, y2) = c1, c2
    dx, dy = x2-x1, y2-y1; d = math.hypot(dx, dy)
    a = (r1*r1 - r2*r2 + d*d) / (2*d); h = math.sqrt(max(r1*r1 - a*a, 0))
    xm, ym = x1 + a*dx/d, y1 + a*dy/d
    return [(xm + h*dy/d, ym - h*dx/d), (xm - h*dy/d, ym + h*dx/d)]

class Flame:
    def __init__(s, R=96, FL=(108, 84), FR=(12, 84), TX=72, T2X=36, N=(48, 60),
                 RM=72, RS=48, RC=12, BASE=108):
        s.__dict__.update(locals()); del s.__dict__["s"]
        s.T = (TX, FR[1] - math.sqrt(R*R - (TX-FR[0])**2))
        s.T2 = (T2X, FL[1] - math.sqrt(R*R - (T2X-FL[0])**2))
        s.CM = min(cc(s.T, RM, N, RM), key=lambda p: p[0])   # above-left of chord
        s.CS = max(cc(N, RS, s.T2, RS), key=lambda p: p[0])  # above-right of chord
        # fillets: centre at y = BASE-RC, internally tangent to flank circle
        dy = BASE - RC - FL[1]
        s.KL = (FL[0] - math.sqrt((R-RC)**2 - dy**2), BASE - RC)
        s.KR = (FR[0] + math.sqrt((R-RC)**2 - dy**2), BASE - RC)

    def geom(s):
        body = disc(s.FL, s.R).intersection(disc(s.FR, s.R)).intersection(box(-50, -50, 200, s.BASE))
        notch = disc(s.CM, s.RM).intersection(disc(s.CS, s.RS)).intersection(box(-50, -50, 200, s.N[1]))
        g = body.difference(notch)
        # fillets
        for K, F in ((s.KL, s.FL), (s.KR, s.FR)):
            # tangent point with the flank circle
            d = math.hypot(K[0]-F[0], K[1]-F[1])
            P = (F[0] + s.R*(K[0]-F[0])/d, F[1] + s.R*(K[1]-F[1])/d)
            x0, x1 = (K[0] - 3*s.RC, K[0]) if K is s.KL else (K[0], K[0] + 3*s.RC)
            corner = box(x0, P[1], x1, s.BASE + 1)
            g = g.difference(corner.difference(disc(K, s.RC)))
        if g.geom_type == "MultiPolygon":
            g = max(g.geoms, key=lambda p: p.area)
        return g

    def circles(s):
        return [(s.FL, s.R), (s.FR, s.R), (s.CM, s.RM), (s.CS, s.RS), (s.KL, s.RC), (s.KR, s.RC)]
