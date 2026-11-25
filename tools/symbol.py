"""SAFI symbol — 'Tandem Flame'.
Construction: a two-tongued flame hull is split by an S-shaped channel of
constant width into an outer blade (process / energy) and an inner blade
(operator), sitting on a flat, level base (stability)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from shapes import poly, polys
from fit import fit_ring, ring_to_d

HULL = ("M66 4 C68 30 100 46 100 80 C100 96 92 106 82 110 L38 110 "
        "C28 106 20 96 20 82 C20 64 26 52 34 42 C34 54 38 60 44 64 C42 40 54 24 66 4Z")
TONGUE = ("M10 120 L10 20 L40 20 C40 44 72 60 74 80 C76 96 62 100 48 100 "
          "C38 100 32 106 30 120Z")
GAP = 4.6

def pieces():
    H = poly(HULL, 200); T = poly(TONGUE, 200)
    outer = H.difference(T.buffer(GAP, join_style=1, quad_segs=32))
    inner = H.intersection(T)
    return [p for p in polys(outer) + polys(inner) if p.area > 8]

def symbol_paths(err=0.06):
    out = []
    for p in pieces():
        ring = list(p.exterior.coords)[:-1]
        s, segs = fit_ring(ring, err=err, ang=32, step=0.2)
        out.append(ring_to_d(s, segs))
    return out

def bbox():
    from shapely.ops import unary_union
    return unary_union(pieces()).bounds

if __name__ == "__main__":
    ps = symbol_paths()
    print(bbox())
    for d in ps: print(len(d), d[:300])
