"""Build the black-and-white concept round into public/branding/concepts/."""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(__file__))
import concepts as K
from exact import to_d, fmt
from wordmark2 import wordmark

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "public", "branding", "concepts")
os.makedirs(OUT, exist_ok=True)
F = K.F

def svgdoc(vb, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{title}">'
            f'{body}</svg>\n')

WG, WW, WC = wordmark()
WD = to_d(WG, WC)

def pts_label(p, name, dx=2.2, dy=-2.2, anchor="start"):
    return (f'<circle cx="{fmt(p[0])}" cy="{fmt(p[1])}" r="1.1" fill="#000"/>'
            f'<text x="{fmt(p[0]+dx)}" y="{fmt(p[1]+dy)}" font-size="4.2" font-family="IBM Plex Mono, monospace" text-anchor="{anchor}" fill="#000">{name}</text>')

def grid():
    g = []
    for i in range(0, 121, 6):
        w = ".25" if i % 24 else ".45"
        g.append(f'<line x1="{i}" y1="0" x2="{i}" y2="120" stroke="#000" stroke-opacity=".12" stroke-width="{w}"/>')
        g.append(f'<line x1="0" y1="{i}" x2="120" y2="{i}" stroke="#000" stroke-opacity=".12" stroke-width="{w}"/>')
    return "".join(g)

def construction(d, circles, extra=""):
    cs = "".join(f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(r)}" fill="none" stroke="#000" stroke-opacity=".55" stroke-width=".35" stroke-dasharray="1.6 1.2"/>'
                 f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r=".7" fill="#000" fill-opacity=".55"/>' for c, r in circles)
    body = (f'<rect x="-40" y="-40" width="200" height="200" fill="#fff"/>{grid()}'
            f'<path d="{d}" fill="#000" fill-opacity=".1" stroke="#000" stroke-width=".6"/>'
            f'<g clip-path="url(#cl)">{cs}</g>{extra}')
    return svgdoc("-24 -24 168 168", f'<defs><clipPath id="cl"><rect x="-24" y="-24" width="168" height="168"/></clipPath></defs>' + body, "Construction")

def lockup(d, bbox, fill="#000"):
    x0, y0, x1, y1 = bbox; sh = y1 - y0
    cap = sh * 0.5; s = cap / 100; gap = sh * 0.3
    wx = x1 + gap; wy = y0 + (sh - cap) / 2
    body = (f'<path fill="{fill}" d="{d}"/>'
            f'<path fill="{fill}" transform="translate({fmt(wx)} {fmt(wy)}) scale({fmt(s)})" d="{WD}"/>')
    return svgdoc(f"{fmt(x0)} {fmt(y0)} {fmt(wx + WW*s - x0)} {fmt(sh)}", body, "SAFI")

def icon(d, bbox, bg="#000", fg="#FFF", frac=0.58):
    x0, y0, x1, y1 = bbox; w, h = x1-x0, y1-y0
    s = 1024 * frac / max(w, h)
    tx = 512 - (x0 + w/2) * s; ty = 512 - (y0 + h/2) * s
    body = (f'<rect width="1024" height="1024" rx="230" fill="{bg}"/>'
            f'<path fill="{fg}" transform="translate({fmt(tx)} {fmt(ty)}) scale({fmt(s)})" d="{d}"/>')
    return svgdoc("0 0 1024 1024", body, "SAFI app icon")

def flame_points():
    return (pts_label(F.T, "T") + pts_label(F.T2, "T₂", -2.2, -2.2, "end") + pts_label(F.N, "N", 2.2, 4.5)
            + f'<line x1="-24" y1="108" x2="144" y2="108" stroke="#000" stroke-width=".35"/>')

C = {
  "01-tandem": dict(name="Tandem", fn=K.tandem, args={}, frac=.6),
  "02-laminar": dict(name="Laminar", fn=K.laminar, args={}, frac=.6),
  "03-gate": dict(name="Gate", fn=K.gate, args={}, frac=.62),
}
meta = {}
for key, c in C.items():
    geo, circles, info = c["fn"](**c["args"])
    d = to_d(geo, circles)
    bbox = geo.bounds
    od = os.path.join(OUT, key); os.makedirs(od, exist_ok=True)
    extra = ""
    if key == "01-tandem":
        extra = flame_points() + pts_label(info["channel"][0], "C", 2.2, -2.2)
    elif key == "02-laminar":
        extra = flame_points() + "".join(
            f'<rect x="{x}" y="-24" width="{w}" height="168" fill="none" stroke="#000" stroke-width=".35" stroke-dasharray="3 1.5"/>' for x, w in info["plates"])
    else:
        extra = '<rect x="0" y="0" width="120" height="120" fill="none" stroke="#000" stroke-width=".35"/>'
    open(os.path.join(od, "construction.svg"), "w").write(construction(d, circles, extra))
    vb = f"{fmt(bbox[0])} {fmt(bbox[1])} {fmt(bbox[2]-bbox[0])} {fmt(bbox[3]-bbox[1])}"
    open(os.path.join(od, "symbol-black.svg"), "w").write(svgdoc(vb, f'<path fill="#000" d="{d}"/>', f"SAFI symbol, concept {c['name']}"))
    open(os.path.join(od, "symbol-white.svg"), "w").write(svgdoc(vb, f'<path fill="#FFF" d="{d}"/>', f"SAFI symbol, concept {c['name']}"))
    open(os.path.join(od, "lockup-black.svg"), "w").write(lockup(d, bbox))
    open(os.path.join(od, "lockup-white.svg"), "w").write(lockup(d, bbox, "#FFF"))
    if key == "03-gate":
        # the tile IS the block: flame counter cut from the rounded tile, standing on its base
        from shapely.geometry import box as _b
        from shapely import affinity as _a
        from exact import disc as _disc
        sc = 1024 / 120
        tile = _b(0, 0, 1024, 1024).buffer(-230, join_style=2).buffer(230, quad_segs=1024)
        fl = _a.scale(F.geom(), 0.625*sc, 0.625*sc, origin=(60, 108)); fl = _a.translate(fl, 512-60, 1024-108)
        cs = [((512 + (cc[0]-60)*0.625*sc, 1024 + (cc[1]-108)*0.625*sc), r*0.625*sc) for cc, r in F.circles()]
        cs += [((230, 230), 230), ((794, 230), 230), ((230, 794), 230), ((794, 794), 230)]
        g = tile.difference(fl)
        open(os.path.join(od, "app-icon.svg"), "w").write(svgdoc("0 0 1024 1024", f'<path fill="#000" d="{to_d(g, cs, eps=0.05)}"/>', "SAFI app icon"))
    else:
        open(os.path.join(od, "app-icon.svg"), "w").write(icon(d, bbox, frac=c["frac"]))
    meta[key] = dict(name=c["name"], d=d, bbox=bbox, arcs=d.count("A"), lines=d.count("L"), circles=len(circles))
open(os.path.join(OUT, "wordmark-provisional.svg"), "w").write(svgdoc(f"0 0 {fmt(WW)} 100", f'<path fill="#000" d="{WD}"/>', "SAFI"))
json.dump(meta, open(os.path.join(os.path.dirname(__file__), "meta.json"), "w"), indent=1)
print(json.dumps({k: (v["arcs"], v["lines"], v["circles"]) for k, v in meta.items()}))
