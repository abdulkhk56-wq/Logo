"""Three SAFI symbol concepts, all on a 120 x 120 artboard with a 6-unit module.
Each returns (shapely geometry, construction circles, construction lines, points)."""
import math
from shapely.geometry import box
from shapely.ops import unary_union
from shapely import affinity
from flame import Flame
from exact import disc

U = 6
F = Flame()

def tandem(cx=0, cy=96, r=48, g=6):
    """Concept 1. The flame split by one arc-shaped channel of constant width g = 1u,
    a band between two concentric circles centred on the grid (0, 96)."""
    band = disc((cx, cy), r + g/2).difference(disc((cx, cy), r - g/2))
    geo = F.geom().difference(band)
    circles = F.circles() + [((cx, cy), r + g/2), ((cx, cy), r - g/2)]
    return geo, circles, dict(channel=((cx, cy), r))

def laminar(w=24, g=12, x0=12, n=3):
    """Concept 2. The flame intersected with n vertical plates of width w, gaps g."""
    plates = unary_union([box(x0 + i*(w+g), -10, x0 + i*(w+g) + w, 130) for i in range(n)])
    geo = F.geom().intersection(plates)
    return geo, F.circles(), dict(plates=[(x0 + i*(w+g), w) for i in range(n)])

def gate(scale=0.625, side=120, plate=0, radius=0):
    """Concept 3. A solid block with the flame as its counter, standing on the base."""
    sc = scale
    fl = affinity.scale(F.geom(), sc, sc, origin=(60, 108))
    fl = affinity.translate(fl, 0, (side - plate) - 108)
    circles = [((60 + (c[0]-60)*sc, (side-plate) + (c[1]-108)*sc), r*sc) for c, r in F.circles()]
    blk = box(0, 0, side, side)
    if radius:
        blk = blk.buffer(-radius, join_style=2).buffer(radius, quad_segs=1024)
        circles += [((radius, radius), radius), ((side-radius, radius), radius)]
    geo = blk.difference(fl)
    return geo, circles, dict(scale=sc)
