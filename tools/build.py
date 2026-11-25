"""Build every SAFI brand asset into public/branding/.
Run:  python3 tools/build.py   (requires shapely + numpy)"""
import os, sys, math, json
sys.path.insert(0, os.path.dirname(__file__))
from symbol import symbol_paths, HULL
from wordmark import wordmark
import geom
from shapes import poly, polys
from fit import fit_ring, ring_to_d
from shapely.geometry import box, Polygon
from shapely import affinity

ROOT = os.path.join(os.path.dirname(__file__), "..", "public", "branding")
os.makedirs(os.path.join(ROOT, "exploration"), exist_ok=True)

C = dict(graphite="#16191D", flare="#E0782A", ivory="#F4EFE6",
         petroleum="#14403D", steel="#8A9199", ember="#A34C16", black="#000000", white="#FFFFFF")

SYM = symbol_paths()
SX0, SY0, SW, SH = 20, 4, 80, 106          # symbol bounding box (construction units)
WD, WW = wordmark()                        # wordmark path, width at cap height 100

def svg(vb, body, title, w=None, h=None):
    size = (f' width="{w}"' if w else "") + (f' height="{h}"' if h else "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{size} role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title>{body}</svg>\n')

def sym_g(fill, tx=0, ty=0, s=1):
    d = " ".join(SYM)
    return f'<path fill="{fill}" transform="translate({geom.f(tx)} {geom.f(ty)}) scale({geom.f(s)})" d="{d}"/>'

def word_g(fill, tx, ty, s):
    return f'<path fill="{fill}" transform="translate({geom.f(tx)} {geom.f(ty)}) scale({geom.f(s)})" d="{WD}"/>'

def write(name, content):
    with open(os.path.join(ROOT, name), "w") as fh: fh.write(content)

# ---------------------------------------------------------------- symbol
# square artboard 120x120, symbol optically centred (flat base sits slightly low)
def symbol_square(fill):
    s = 1.0; tx = (120 - SW) / 2 - SX0; ty = (120 - SH) / 2 - SY0
    return sym_g(fill, tx, ty, s)

for name, fill, title in [
    ("safi-symbol.svg", C["flare"], "SAFI symbol"),
    ("safi-symbol-ivory.svg", C["ivory"], "SAFI symbol (ivory, for dark backgrounds)"),
    ("safi-symbol-graphite.svg", C["graphite"], "SAFI symbol (graphite)"),
    ("safi-symbol-mono-black.svg", C["black"], "SAFI symbol (monochrome black)"),
    ("safi-symbol-mono-white.svg", C["white"], "SAFI symbol (monochrome white)"),
]:
    write(name, svg("0 0 120 120", symbol_square(fill), title))

# ---------------------------------------------------------------- wordmark
for name, fill, title in [
    ("safi-wordmark.svg", C["graphite"], "SAFI"),
    ("safi-wordmark-ivory.svg", C["ivory"], "SAFI"),
    ("safi-wordmark-mono-black.svg", C["black"], "SAFI"),
    ("safi-wordmark-mono-white.svg", C["white"], "SAFI"),
]:
    write(name, svg(f"0 0 {geom.f(WW)} 100", f'<path fill="{fill}" d="{WD}"/>', title))

# ---------------------------------------------------------------- horizontal lockup
# Symbol height = 106u. Cap height = 0.54 x symbol height. Gap = 0.27 x symbol height.
# The type is centred on the flame's visual mass (which sits below its geometric centre).
CAP = SH * 0.54; WS = CAP / 100
GAP = SH * 0.27
BASE = SY0 + SH * 0.58 + CAP / 2
def horizontal(sym_fill, word_fill):
    x_word = SX0 + SW + GAP
    body = sym_g(sym_fill) + word_g(word_fill, x_word, BASE - CAP, WS)
    w = x_word + WW * WS - SX0
    return f"{SX0} {SY0} {geom.f(w)} {SH}", body

for name, sf, wf, title in [
    ("safi-logo-primary.svg", C["flare"], C["graphite"], "SAFI — primary logo (light backgrounds)"),
    ("safi-logo-primary-dark.svg", C["flare"], C["ivory"], "SAFI — primary logo (dark backgrounds)"),
    ("safi-logo-mono-black.svg", C["black"], C["black"], "SAFI — monochrome black"),
    ("safi-logo-mono-white.svg", C["white"], C["white"], "SAFI — monochrome white"),
]:
    vb, body = horizontal(sf, wf); write(name, svg(vb, body, title))

# ---------------------------------------------------------------- stacked lockup
def stacked(sym_fill, word_fill):
    cap = SH * 0.42; ws = cap / 100; gap = SH * 0.26
    word_w = WW * ws
    W = max(SW, word_w)
    sx = (W - SW) / 2 - SX0
    body = sym_g(sym_fill, sx, -SY0) + word_g(word_fill, (W - word_w) / 2, SH + gap, ws)
    return f"0 0 {geom.f(W)} {geom.f(SH + gap + cap)}", body

for name, sf, wf, title in [
    ("safi-logo-stacked.svg", C["flare"], C["graphite"], "SAFI — stacked logo (light backgrounds)"),
    ("safi-logo-stacked-dark.svg", C["flare"], C["ivory"], "SAFI — stacked logo (dark backgrounds)"),
]:
    vb, body = stacked(sf, wf); write(name, svg(vb, body, title))

# ---------------------------------------------------------------- app icons
# 1024 grid, continuous-corner approximation via rx = 22.5%
def app_icon(bg, fg, rx=230):
    s = 1024 * 0.60 / SH
    tx = 512 - (SX0 + SW / 2) * s
    ty = 512 - (SY0 + SH / 2) * s + 6
    return (f'<rect width="1024" height="1024" rx="{rx}" fill="{bg}"/>' + sym_g(fg, tx, ty, s))

write("safi-app-icon.svg", svg("0 0 1024 1024", app_icon(C["graphite"], C["flare"]), "SAFI app icon"))
write("safi-app-icon-light.svg", svg("0 0 1024 1024", app_icon(C["ivory"], C["flare"]), "SAFI app icon (light)"))
write("safi-app-icon-ios.svg", svg("0 0 1024 1024", app_icon(C["graphite"], C["flare"], 0), "SAFI app icon (iOS, square — the OS applies the corner mask)"))
write("safi-app-icon-mono.svg", svg("0 0 1024 1024", app_icon(C["black"], C["white"]), "SAFI app icon (monochrome)"))
# full-bleed square (OS applies its own mask: Android adaptive / maskable PWA)
def maskable():
    s = 1024 * 0.46 / SH
    tx = 512 - (SX0 + SW / 2) * s; ty = 512 - (SY0 + SH / 2) * s + 4
    return f'<rect width="1024" height="1024" fill="{C["graphite"]}"/>' + sym_g(C["flare"], tx, ty, s)
write("safi-app-icon-maskable.svg", svg("0 0 1024 1024", maskable(), "SAFI app icon (maskable, full-bleed)"))

# favicon: tile for contrast on any browser chrome
def favicon():
    s = 32 * 0.70 / SH
    tx = 16 - (SX0 + SW / 2) * s; ty = 16 - (SY0 + SH / 2) * s + 0.3
    return f'<rect width="32" height="32" rx="7" fill="{C["graphite"]}"/>' + sym_g(C["flare"], tx, ty, s)
write("safi-favicon.svg", svg("0 0 32 32", favicon(), "SAFI"))

# ---------------------------------------------------------------- exploration concepts
def fitted(geoms, err=0.05):
    out = []
    for g in geoms:
        for p in polys(g):
            for ring in [p.exterior] + list(p.interiors):
                s, segs = fit_ring(list(ring.coords)[:-1], err=err, ang=32, step=0.2)
                out.append(ring_to_d(s, segs))
    return " ".join(out)

hull = poly(HULL, 200)
# A — Strata: flame silhouette sliced into filter lamellae
bands = [box(0, y, 120, y + 5) for y in (66, 80, 94)]
strata = hull
for b in bands: strata = strata.difference(b)
write("exploration/concept-a-strata.svg",
      svg("0 0 120 120", f'<path fill="{C["flare"]}" transform="translate(0 3)" d="{fitted([strata])}"/>', "Concept A — Strata"))

# B — Envelope: burner core inside a protective shell (layers of protection), exact arcs
def arch(cL, rL, cR, rR, base):
    T = min(geom.circ_circ(cL, rL, cR, rR), key=lambda p: p[1])
    return geom.circ_hline(cL, rL, base)[0], T, geom.circ_hline(cR, rR, base)[1]
def archpath(cL, rL, cR, rR, base):
    BL, T, BR = arch(cL, rL, cR, rR, base)
    return f"{geom.M(BL)} {geom.arc(rL, T, 1)} {geom.arc(rR, BR, 1)} Z"
def shellpath(cL, rL, cR, rR, base, w):
    BL, T, BR = arch(cL, rL, cR, rR, base); bl, t, br = arch(cL, rL - w, cR, rR - w, base)
    return (f"{geom.M(BL)} {geom.arc(rL, T, 1)} {geom.arc(rR, BR, 1)} {geom.L(br)} "
            f"{geom.arc(rR - w, t, 0)} {geom.arc(rL - w, bl, 0)} Z")
cL, cR = (100, 82), (20, 76)
env = (f'<path fill="{C["flare"]}" d="{shellpath(cL, 78, cR, 80, 104, 12)} {archpath(cL, 59, cR, 61, 104)}"/>'
       f'<rect x="18" y="108" width="84" height="6" fill="{C["graphite"]}"/>')
write("exploration/concept-b-envelope.svg", svg("0 0 120 120", env, "Concept B — Envelope"))

# C — Filter Gate: P&ID filter rhombus, split by the filter line, flame passing through
dia = Polygon([(60, 4), (116, 60), (60, 116), (4, 60)]).buffer(-4).buffer(4, join_style=1)
small = affinity.translate(affinity.scale(hull, 0.5, 0.5, origin=(60, 57)), 0, 3)
gate = dia.difference(small.buffer(4.5, join_style=1)).difference(box(0, 58, 120, 62.5))
gate_body = (f'<path fill="{C["graphite"]}" d="{fitted([gate])}"/>'
             f'<path fill="{C["flare"]}" d="{fitted([small])}"/>')
write("exploration/concept-c-filter-gate.svg", svg("0 0 120 120", gate_body, "Concept C — Filter Gate"))

# D — Tandem Flame (selected)
write("exploration/concept-d-tandem-flame.svg", svg("0 0 120 120", symbol_square(C["flare"]), "Concept D — Tandem Flame (selected)"))

# ---------------------------------------------------------------- tokens
tokens = {
    "color": {
        "graphite": {"value": C["graphite"], "use": "Primary dark: wordmark, UI chrome, app-icon field"},
        "flare": {"value": C["flare"], "use": "Signature accent: the symbol, key actions — never body text on ivory"},
        "ivory": {"value": C["ivory"], "use": "Primary light surface; wordmark on dark"},
        "petroleum": {"value": C["petroleum"], "use": "Secondary: stable / in-limits state, data surfaces"},
        "steel": {"value": C["steel"], "use": "Neutral: rules, secondary text on graphite"},
        "ember": {"value": C["ember"], "use": "Flare at text weight / pressed state (AA on ivory)"},
    },
    "logo": {"symbolToCapHeight": 2.0, "clearSpace": "0.25 x symbol height", "minSymbolPx": 16, "minLockupPx": 96},
}
write("safi-tokens.json", json.dumps(tokens, indent=2) + "\n")
css = ":root {\n" + "".join(f"  --safi-{k}: {v['value']};\n" for k, v in tokens["color"].items()) + "}\n"
write("safi-colors.css", "/* SAFI brand colour tokens */\n" + css)
print("built", WW)
