"""Build the final SAFI identity kit into public/branding/.
python3 tools/v2/identity.py && node tools/v2/export_png.js"""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from shapely.geometry import box
from shapely import affinity
from exact import to_d, fmt, disc
from final import symbol, wordmark

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "public", "branding")
C = dict(navy="#0F2A3D", flare="#DD5A1E", white="#FFFFFF", steel="#5B6B78", mist="#E8ECEF",
         deep="#0A1E2C", black="#000000")

G, CIRC = symbol()
CORE = box(40, -10, 80, 130)                       # the centre plate
PLATES_D = to_d(G.difference(CORE), CIRC)
CORE_D = to_d(G.intersection(CORE), CIRC)
ALL_D = to_d(G, CIRC)
GS, CS = symbol(small=True)
SMALL_PLATES = to_d(GS.difference(CORE), CS); SMALL_CORE = to_d(GS.intersection(CORE), CS)
X0, Y0, X1, Y1 = G.bounds                         # 12, 9.06, 108, 108
SH = Y1 - Y0
WG, WW, WC = wordmark(); WD = to_d(WG, WC)

def doc(vb, body, label):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>\n'

def sym(plates, core, tx=0, ty=0, s=1, small=False):
    pd, cd = (SMALL_PLATES, SMALL_CORE) if small else (PLATES_D, CORE_D)
    t = f' transform="translate({fmt(tx)} {fmt(ty)}) scale({fmt(s)})"' if (tx or ty or s != 1) else ""
    if plates == core:
        return f'<path fill="{plates}"{t} d="{pd} {cd}"/>'
    return f'<g{t}><path fill="{plates}" d="{pd}"/><path fill="{core}" d="{cd}"/></g>'

def word(fill, tx, ty, s):
    return f'<path fill="{fill}" transform="translate({fmt(tx)} {fmt(ty)}) scale({fmt(s)})" d="{WD}"/>'

def w(name, s): open(os.path.join(OUT, name), "w").write(s)

# Lockup system --------------------------------------------------------------
# Wordmark sits on the symbol's base line; cap height = 0.52 x symbol height;
# symbol-to-word gap = one plate width (24).
CAP = 0.52 * SH; WS = CAP / 100; GAP = 24
def horizontal(pl, co, wf):
    xw = X1 + GAP
    return doc(f"{fmt(X0)} {fmt(Y0)} {fmt(xw + WW*WS - X0)} {fmt(SH)}", sym(pl, co) + word(wf, xw, Y1 - CAP, WS), "SAFI")
def stacked(pl, co, wf):
    cap = 0.36 * SH; ws = cap / 100; ww = WW * ws; gap = 0.22 * SH
    W = max(ww, X1 - X0); sx = (W - (X1 - X0)) / 2 - X0
    body = sym(pl, co, sx, -Y0) + word(wf, (W - ww) / 2, SH + gap, ws)
    return doc(f"0 0 {fmt(W)} {fmt(SH + gap + cap)}", body, "SAFI")

w("safi-logo-primary.svg", horizontal(C["navy"], C["flare"], C["navy"]))
w("safi-logo-primary-dark.svg", horizontal(C["white"], C["flare"], C["white"]))
w("safi-logo-stacked.svg", stacked(C["navy"], C["flare"], C["navy"]))
w("safi-logo-stacked-dark.svg", stacked(C["white"], C["flare"], C["white"]))
w("safi-logo-mono-black.svg", horizontal(C["black"], C["black"], C["black"]))
w("safi-logo-mono-white.svg", horizontal(C["white"], C["white"], C["white"]))
w("safi-logo-mono-navy.svg", horizontal(C["navy"], C["navy"], C["navy"]))

vb = f"{fmt(X0)} {fmt(Y0)} {fmt(X1-X0)} {fmt(SH)}"
w("safi-symbol.svg", doc(vb, sym(C["navy"], C["flare"]), "SAFI symbol"))
w("safi-symbol-dark.svg", doc(vb, sym(C["white"], C["flare"]), "SAFI symbol"))
w("safi-symbol-mono-black.svg", doc(vb, sym(C["black"], C["black"]), "SAFI symbol"))
w("safi-symbol-mono-white.svg", doc(vb, sym(C["white"], C["white"]), "SAFI symbol"))
w("safi-symbol-small.svg", doc(vb, sym(C["navy"], C["flare"], small=True), "SAFI symbol, small-size cut"))
w("safi-wordmark.svg", doc(f"0 0 {fmt(WW)} 100", f'<path fill="{C["navy"]}" d="{WD}"/>', "SAFI"))
w("safi-wordmark-white.svg", doc(f"0 0 {fmt(WW)} 100", f'<path fill="{C["white"]}" d="{WD}"/>', "SAFI"))
w("safi-wordmark-black.svg", doc(f"0 0 {fmt(WW)} 100", f'<path fill="{C["black"]}" d="{WD}"/>', "SAFI"))

# Icons ------------------------------------------------------------------------
def tile(bg, pl, co, rx=230, frac=0.56, small=False, size=1024):
    s = size * frac / SH
    tx = size/2 - (X0 + (X1-X0)/2) * s; ty = size/2 - (Y0 + SH/2) * s
    r = f' rx="{fmt(rx*size/1024)}"' if rx else ""
    return doc(f"0 0 {size} {size}", f'<rect width="{size}" height="{size}"{r} fill="{bg}"/>' + sym(pl, co, tx, ty, s, small), "SAFI")
w("safi-app-icon.svg", tile(C["navy"], C["white"], C["flare"]))
w("safi-app-icon-light.svg", tile(C["white"], C["navy"], C["flare"]))
w("safi-app-icon-ios.svg", tile(C["navy"], C["white"], C["flare"], rx=0))
w("safi-app-icon-maskable.svg", tile(C["navy"], C["white"], C["flare"], rx=0, frac=0.44))
w("safi-favicon.svg", tile(C["navy"], C["white"], C["flare"], rx=230, frac=0.64, small=True, size=32))

# Tokens -----------------------------------------------------------------------
tok = {"color": {
  "navy":  {"value": C["navy"],  "role": "Primary. Symbol plates and wordmark on light grounds; brand surfaces."},
  "flare": {"value": C["flare"], "role": "Accent. The centre plate only, plus one highlight per layout. Never body text."},
  "white": {"value": C["white"], "role": "Primary light ground; plates and wordmark on navy."},
  "deep":  {"value": C["deep"],  "role": "Dark UI ground (control-room screens)."},
  "steel": {"value": C["steel"], "role": "Secondary text and rules."},
  "mist":  {"value": C["mist"],  "role": "Light panels and table fills."}},
 "type": {"family": "Barlow", "data": "Barlow Semi Condensed", "mono": "IBM Plex Mono"},
 "logo": {"clearSpace": "one plate width (24/96 of symbol width) on every side",
          "minLockupPx": 100, "minSymbolPx": 16, "smallCutBelowPx": 24}}
w("safi-tokens.json", json.dumps(tok, indent=2) + "\n")
w("safi-colors.css", "/* SAFI colour tokens */\n:root {\n" + "".join(f"  --safi-{k}: {v['value']};\n" for k, v in tok["color"].items()) + "}\n")
print("ok", WW)
