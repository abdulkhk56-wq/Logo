"""SAFI identity build: python3 tools/build.py  (needs: pip install fonttools)
Writes every SVG asset and the tokens into public/branding/."""
import os, json
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib import instancer

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "public", "branding")

# ---------------------------------------------------------------- the flame
# Drawn on a 160 x 240 artboard. Three flat layers, back to front:
#   outer flame (two tongues), flame body, core.
OUTER = "M86 2C102 46 140 82 140 142C140 198 110 234 80 234C48 234 20 208 20 168C20 128 40 108 50 82C54 104 60 118 68 126C64 80 76 40 86 2Z"
BODY = "M84 52C96 88 128 112 128 160C128 204 104 230 80 230C54 230 32 210 32 178C32 150 46 132 56 114C60 130 64 140 72 146C68 112 72 82 84 52Z"
CORE = "M78 112C84 144 110 160 110 190C110 214 96 228 80 228C60 228 48 214 48 196C48 176 58 166 64 154C66 166 70 174 76 176C72 152 72 132 78 112Z"
SX0, SY0, SW, SH = 20, 2, 120, 232          # flame bounds

C = dict(red="#D63A1A", orange="#EE7420", yellow="#F8B320", navy="#0E2236",
         deep="#081624", steel="#5B6B78", mist="#E8ECEF", white="#FFFFFF", black="#000000")

def flame(t="", mono=None):
    tr = f' transform="{t}"' if t else ""
    if mono:  # one colour: outer flame with the core knocked out
        return f'<path fill="{mono}" fill-rule="evenodd"{tr} d="{OUTER} {CORE}"/>'
    return (f'<g{tr}><path fill="{C["red"]}" d="{OUTER}"/><path fill="{C["orange"]}" d="{BODY}"/>'
            f'<path fill="{C["yellow"]}" d="{CORE}"/></g>')

# ---------------------------------------------------------------- wordmark
# Archivo (SIL OFL), width 112, weight 640, outlined; tracking 0.08 em.
def outline(text="SAFI", track=0.08):
    f = TTFont(os.path.join(HERE, "fonts", "Archivo.ttf"))
    f = instancer.instantiateVariableFont(f, {"wdth": 112, "wght": 640})
    gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f["head"].unitsPerEm
    cap = f["OS/2"].sCapHeight
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
    x = 0
    for ch in text:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(pen, (1, 0, 0, -1, x, cap)))
        x += gs[g].width + track * upm
    return pen.getCommands(), x - track * upm, cap

WD, WW, CAP = outline()

def word(fill, x, y, s):
    return f'<path fill="{fill}" transform="translate({x:.2f} {y:.2f}) scale({s:.5f})" d="{WD}"/>'

def svg(vb, body, label):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>\n'

def w(name, s):
    open(os.path.join(OUT, name), "w").write(s)

# ---------------------------------------------------------------- lockups
# Cap height = 0.42 x flame height. Gap = 0.16 x flame height.
# Baseline sits 4% above the flame's lowest point (optical: the base is round).
def horizontal(wf, mono=None):
    cap = SH * 0.42; s = cap / CAP; gap = SH * 0.16
    base = SY0 + SH * 0.96
    x = SX0 + SW + gap
    body = flame(mono=mono) + word(mono or wf, x, base - cap, s)
    return svg(f"{SX0} {SY0} {x + WW*s - SX0:.2f} {SH}", body, "SAFI")

def stacked(wf, mono=None):
    cap = SH * 0.22; s = cap / CAP; gap = SH * 0.12; ww = WW * s
    W = max(ww, SW)
    body = flame(f"translate({(W-SW)/2 - SX0:.2f} {-SY0})", mono) + word(mono or wf, (W - ww)/2, SH + gap, s)
    return svg(f"0 0 {W:.2f} {SH + gap + cap:.2f}", body, "SAFI")

w("safi-logo-primary.svg", horizontal(C["navy"]))
w("safi-logo-primary-dark.svg", horizontal(C["white"]))
w("safi-logo-stacked.svg", stacked(C["navy"]))
w("safi-logo-stacked-dark.svg", stacked(C["white"]))
w("safi-logo-mono-black.svg", horizontal(None, C["black"]))
w("safi-logo-mono-white.svg", horizontal(None, C["white"]))
w("safi-logo-mono-navy.svg", horizontal(None, C["navy"]))

vb = f"{SX0} {SY0} {SW} {SH}"
w("safi-symbol.svg", svg(vb, flame(), "SAFI symbol"))
w("safi-symbol-mono-black.svg", svg(vb, flame(mono=C["black"]), "SAFI symbol"))
w("safi-symbol-mono-white.svg", svg(vb, flame(mono=C["white"]), "SAFI symbol"))
w("safi-symbol-mono-navy.svg", svg(vb, flame(mono=C["navy"]), "SAFI symbol"))
for n, fill in (("", C["navy"]), ("-white", C["white"]), ("-black", C["black"])):
    w(f"safi-wordmark{n}.svg", svg(f"-10 {-CAP*0.03:.1f} {WW+20:.1f} {CAP*1.06:.1f}", word(fill, 0, 0, 1), "SAFI"))

# ---------------------------------------------------------------- icons
def tile(size=1024, rx=230, frac=0.62, bg=C["navy"]):
    s = size * frac / SH
    tx = size/2 - (SX0 + SW/2) * s; ty = size/2 - (SY0 + SH/2) * s
    r = f' rx="{rx*size/1024:.2f}"' if rx else ""
    return svg(f"0 0 {size} {size}", f'<rect width="{size}" height="{size}"{r} fill="{bg}"/>' + flame(f"translate({tx:.2f} {ty:.2f}) scale({s:.4f})"), "SAFI")
w("safi-app-icon.svg", tile())
w("safi-app-icon-light.svg", tile(bg=C["white"]))
w("safi-app-icon-ios.svg", tile(rx=0))
w("safi-app-icon-maskable.svg", tile(rx=0, frac=0.48))
w("safi-favicon.svg", tile(size=32, frac=0.72))

# ---------------------------------------------------------------- tokens
tok = {"color": {
    "flame-red": {"value": C["red"], "role": "Outer flame"},
    "flame-orange": {"value": C["orange"], "role": "Flame body; the single accent colour in layouts"},
    "flame-yellow": {"value": C["yellow"], "role": "Flame core"},
    "navy": {"value": C["navy"], "role": "Wordmark, primary brand colour, text"},
    "deep": {"value": C["deep"], "role": "Dark interface ground"},
    "steel": {"value": C["steel"], "role": "Secondary text, rules"},
    "mist": {"value": C["mist"], "role": "Light panels"}},
    "type": {"brand": "Archivo", "data": "Archivo (width 87-100)", "mono": "IBM Plex Mono"},
    "logo": {"clearSpace": "half the flame width on every side", "minLockupPx": 96, "minSymbolPx": 16}}
w("safi-tokens.json", json.dumps(tok, indent=2) + "\n")
w("safi-colors.css", "/* SAFI colour tokens */\n:root {\n" + "".join(f"  --safi-{k}: {v['value']};\n" for k, v in tok["color"].items()) + "}\n")
w("site.webmanifest", json.dumps({"name": "SAFI", "short_name": "SAFI", "theme_color": C["navy"], "background_color": C["navy"],
    "icons": [{"src": "safi-app-icon.svg", "type": "image/svg+xml", "sizes": "any", "purpose": "any"},
              {"src": "png/safi-app-icon-192.png", "type": "image/png", "sizes": "192x192", "purpose": "any"},
              {"src": "png/safi-app-icon-512.png", "type": "image/png", "sizes": "512x512", "purpose": "any"},
              {"src": "png/safi-app-icon-maskable-512.png", "type": "image/png", "sizes": "512x512", "purpose": "maskable"}]}, indent=2) + "\n")
print("ok", round(WW), CAP)
