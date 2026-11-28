"""SAFI identity build: python3 tools/build.py   (pip install fonttools uharfbuzz)

Concept: SAFI is «صافي», Arabic for pure, clear, filtered. The symbol is the
letter «ص» (Sad), the name's first letter, set in a navy tile. The name is
always shown in both scripts, drawn from one type family (Readex Pro) so the
Arabic and Latin share stroke weight and rhythm."""
import os, io, json
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.varLib import instancer

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "public", "branding")
os.makedirs(OUT, exist_ok=True)
for _f in os.listdir(OUT):            # start clean: every SVG is regenerated
    if _f.endswith(".svg"): os.remove(os.path.join(OUT, _f))
C = dict(navy="#0B2A3C", gold="#C49A4A", white="#FFFFFF", black="#000000",
         deep="#071C29", steel="#5E6E7A", mist="#E9EDF0")

_FONTS = {}
def font(wght):
    if wght not in _FONTS:
        tt = TTFont(os.path.join(HERE, "fonts", "ReadexPro.ttf"))
        tt = instancer.instantiateVariableFont(tt, {"wght": wght, "HEXP": 0})
        b = io.BytesIO(); tt.save(b)
        _FONTS[wght] = (tt, hb.Font(hb.Face(b.getvalue())))
    return _FONTS[wght]

def shape(text, wght=600, track=0.0):
    """Shaped text -> (svg path d, bounds (x0,y0,x1,y1) in font units, y down)."""
    tt, hf = font(wght)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(hf, buf, {})
    gs = tt.getGlyphSet(); order = tt.getGlyphOrder(); upm = tt["head"].unitsPerEm
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
    bp = BoundsPen(gs); x = 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        g = order[info.codepoint]; m = (1, 0, 0, -1, x + pos.x_offset, -pos.y_offset)
        gs[g].draw(TransformPen(pen, m)); gs[g].draw(TransformPen(bp, m))
        x += pos.x_advance + track * upm
    return pen.getCommands(), bp.bounds

SAD, SADB = shape("ص", 600)
AR, ARB = shape("صافي", 600)
LA, LAB = shape("SAFI", 600, track=0.1)

def place(d, b, x, y, s, fill):
    """Draw path d (bounds b) so its bounds' left/top-left lands at x, y_baseline=y, scale s."""
    return f'<path fill="{fill}" transform="translate({x - b[0]*s:.2f} {y:.2f}) scale({s:.5f})" d="{d}"/>'

def svg(vb, body, label):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>\n'

def w(name, s): open(os.path.join(OUT, name), "w").write(s)

# ---------------------------------------------------------------- symbol
# 120 unit tile, corner radius 28 (23%). «ص» body width = 68% of the tile,
# optically centred: the letter's bowl sits on the tile's centre line.
T = 120
def sad_in_tile(fg, x=0, y=0, size=T):
    k = size / T
    sw = SADB[2] - SADB[0]; s = 0.68 * T / sw * k
    sh = SADB[3] - SADB[1]
    cx = x + size/2 - (sw * s)/2
    base = y + size/2 + (sh * s)/2 - SADB[3]*s + 0.045*size  # optical: slightly low
    return place(SAD, SADB, cx, base, s, fg)

def tile(x, y, size, bg, fg, rx=28):
    if fg == "knock":   # one colour: the letter is cut out of the tile
        mid = f"k{int(x)}{int(size)}"
        return (f'<mask id="{mid}"><rect x="{x}" y="{y}" width="{size}" height="{size}" fill="#fff"/>'
                + sad_in_tile("#000", x, y, size) + '</mask>'
                + f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{rx*size/T:.2f}" fill="{bg}" mask="url(#{mid})"/>')
    return f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{rx*size/T:.2f}" fill="{bg}"/>' + sad_in_tile(fg, x, y, size)

# ---------------------------------------------------------------- lockups
# Latin cap height = 0.40 x tile; Arabic scaled to the same stroke weight and
# its main body height (ص) = Latin cap height; both share one baseline at
# 0.70 of the tile height. Spacing: tile-to-word 0.24 x tile; divider gap 0.16.
CAPH = 0.40 * T
LS = CAPH / (-LAB[1])                 # Latin: cap top = -bounds y0
AS = CAPH / (-SADB[1]) * 0.68         # Arabic: optically balanced with the caps
BASE = 0.70 * T

def lw(): return (LAB[2] - LAB[0]) * LS
def aw(): return (ARB[2] - ARB[0]) * AS

def bilingual(navy, gold, tilebg, tilefg):
    gap, dg = 0.24 * T, 0.16 * T
    x = T + gap
    body = tile(0, 0, T, tilebg, tilefg) + place(LA, LAB, x, BASE, LS, navy)
    x += lw() + dg
    body += f'<rect x="{x:.2f}" y="{BASE - CAPH - 4:.2f}" width="2.4" height="{CAPH + 8 + 0.16*T:.2f}" fill="{gold}"/>'
    x += 2.4 + dg
    body += place(AR, ARB, x, BASE, AS, navy)
    x += aw()
    return svg(f"0 0 {x:.2f} {T}", body, "SAFI صافي")

def latin(navy, tilebg, tilefg):
    x = T + 0.24 * T
    return svg(f"0 0 {x + lw():.2f} {T}", tile(0, 0, T, tilebg, tilefg) + place(LA, LAB, x, BASE, LS, navy), "SAFI")

def arabic(navy, tilebg, tilefg):
    a = aw(); x = a + 0.24 * T
    return svg(f"0 0 {x + T:.2f} {T}", place(AR, ARB, 0, BASE, AS, navy) + tile(x, 0, T, tilebg, tilefg), "صافي")

def stacked(navy, gold, tilebg, tilefg):
    ls, as_ = LS * 0.8, AS * 0.8
    lwid = (LAB[2]-LAB[0]) * ls; awid = (ARB[2]-ARB[0]) * as_
    W = max(T, lwid, awid) + 8
    y1 = T + 0.26*T + (-LAB[1]) * ls                 # Latin baseline
    rule = y1 + 0.14*T
    y2 = rule + 0.14*T + (-ARB[1]) * as_             # Arabic baseline (ascenders clear the rule)
    body = (tile((W - T)/2, 0, T, tilebg, tilefg) + place(LA, LAB, (W - lwid)/2, y1, ls, navy)
            + f'<rect x="{W/2 - 14:.2f}" y="{rule:.2f}" width="28" height="2.4" fill="{gold}"/>'
            + place(AR, ARB, (W - awid)/2, y2, as_, navy))
    return svg(f"0 0 {W:.2f} {y2 + ARB[3]*as_ + 4:.2f}", body, "SAFI صافي")

n, g, wt, k = C["navy"], C["gold"], C["white"], C["black"]
w("safi-logo-primary.svg", bilingual(n, g, n, wt))
w("safi-logo-primary-dark.svg", bilingual(wt, g, wt, n))
w("safi-logo-latin.svg", latin(n, n, wt))
w("safi-logo-latin-dark.svg", latin(wt, wt, n))
w("safi-logo-arabic.svg", arabic(n, n, wt))
w("safi-logo-arabic-dark.svg", arabic(wt, wt, n))
w("safi-logo-stacked.svg", stacked(n, g, n, wt))
w("safi-logo-stacked-dark.svg", stacked(wt, g, wt, n))
w("safi-logo-mono-black.svg", bilingual(k, k, k, "knock"))
w("safi-logo-mono-white.svg", bilingual(wt, wt, wt, "knock"))
# symbol
w("safi-symbol.svg", svg(f"0 0 {T} {T}", tile(0, 0, T, n, wt), "صافي SAFI"))
w("safi-symbol-dark.svg", svg(f"0 0 {T} {T}", tile(0, 0, T, wt, n), "صافي SAFI"))
w("safi-symbol-gold.svg", svg(f"0 0 {T} {T}", tile(0, 0, T, n, g), "صافي SAFI"))
for nm, fill in (("", n), ("-white", wt), ("-black", k)):
    lb = LAB; ab = ARB
    w(f"safi-wordmark{nm}.svg", svg(f"{lb[0]:.0f} {lb[1]-10:.0f} {lb[2]-lb[0]:.0f} {lb[3]-lb[1]+20:.0f}", f'<path fill="{fill}" d="{LA}"/>', "SAFI"))
    w(f"safi-wordmark-arabic{nm}.svg", svg(f"{ab[0]:.0f} {ab[1]-10:.0f} {ab[2]-ab[0]:.0f} {ab[3]-ab[1]+20:.0f}", f'<path fill="{fill}" d="{AR}"/>', "صافي"))
w("safi-symbol-letter.svg", svg(f"0 0 {T} {T}", sad_in_tile(n), "ص"))
w("safi-symbol-mono-black.svg", svg(f"0 0 {T} {T}", tile(0, 0, T, k, "knock"), "صافي SAFI"))
w("safi-symbol-mono-white.svg", svg(f"0 0 {T} {T}", tile(0, 0, T, wt, "knock"), "صافي SAFI"))
# icons
w("safi-app-icon.svg", svg("0 0 1024 1024", tile(0, 0, 1024, n, wt, rx=27), "SAFI"))
w("safi-app-icon-ios.svg", svg("0 0 1024 1024", f'<rect width="1024" height="1024" fill="{n}"/>' + sad_in_tile(wt, 0, 0, 1024), "SAFI"))
def mask():
    inner = 1024*0.70; o = (1024 - inner)/2
    return f'<rect width="1024" height="1024" fill="{n}"/>' + sad_in_tile(wt, o, o, inner)
w("safi-app-icon-maskable.svg", svg("0 0 1024 1024", mask(), "SAFI"))
w("safi-favicon.svg", svg("0 0 32 32", tile(0, 0, 32, n, wt), "SAFI"))

tok = {"color": {
    "navy": {"value": n, "role": "Primary: symbol tile, wordmarks, text"},
    "gold": {"value": g, "role": "Accent: divider rules, one highlight per layout; never body text"},
    "white": {"value": wt, "role": "Primary ground"},
    "deep": {"value": C["deep"], "role": "Dark interface ground"},
    "steel": {"value": C["steel"], "role": "Secondary text, rules"},
    "mist": {"value": C["mist"], "role": "Panels, table fills"}},
    "type": {"family": "Readex Pro (Arabic + Latin)", "mono": "IBM Plex Mono"},
    "logo": {"clearSpace": "half the tile width on every side", "minTilePx": 16, "minBilingualPx": 140}}
w("safi-tokens.json", json.dumps(tok, indent=2, ensure_ascii=False) + "\n")
w("safi-colors.css", "/* SAFI colour tokens */\n:root {\n" + "".join(f"  --safi-{a}: {b['value']};\n" for a, b in tok["color"].items()) + "}\n")
w("site.webmanifest", json.dumps({"name": "SAFI صافي", "short_name": "SAFI", "theme_color": n, "background_color": n,
    "icons": [{"src": "safi-app-icon.svg", "type": "image/svg+xml", "sizes": "any", "purpose": "any"},
              {"src": "png/safi-app-icon-192.png", "type": "image/png", "sizes": "192x192", "purpose": "any"},
              {"src": "png/safi-app-icon-512.png", "type": "image/png", "sizes": "512x512", "purpose": "any"},
              {"src": "png/safi-app-icon-maskable-512.png", "type": "image/png", "sizes": "512x512", "purpose": "maskable"}]},
    indent=2, ensure_ascii=False) + "\n")
print("ok")
