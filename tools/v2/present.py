"""Black-and-white concept presentation -> public/branding/concepts/index.html
(+ body-only copy for publishing when a path is given)."""
import os, sys, re, base64, json
sys.path.insert(0, os.path.dirname(__file__))
from flame import Flame
D = os.path.join(os.path.dirname(__file__), "..", "..", "public", "branding", "concepts")
F = Flame()
meta = json.load(open(os.path.join(os.path.dirname(__file__), "meta.json")))

def svg(path, cls=""):
    s = open(os.path.join(D, path)).read().strip()
    s = s.replace('<svg xmlns="http://www.w3.org/2000/svg"', f'<svg{(" class=%s" % chr(34)+cls+chr(34)) if cls else ""}', 1)
    if "construction" in path:  # unique clip ids per drawing
        uid = path.split("/")[0].replace("-", "")
        s = s.replace('id="cl"', f'id="cl{uid}"').replace('url(#cl)', f'url(#cl{uid})')
    return s

def png(path):
    return "data:image/png;base64," + base64.b64encode(open(os.path.join(D, path), "rb").read()).decode()

f2 = lambda v: f"{v:.1f}".rstrip("0").rstrip(".")
P = lambda p: f"({f2(p[0])}, {f2(p[1])})"

CONCEPTS = [
 dict(key="01-tandem", name="Tandem", sub="One flame, one channel",
  build=[
   "Start from the flame primitive (shared construction, above).",
   "Draw two concentric circles at grid point C = (0, 96), radii 45 and 51. The 6-unit band between them (1u) is the channel.",
   "Subtract the band. The flame divides into an outer blade (main tongue) and an inner blade (secondary tongue)."],
  meaning="The outer blade is the process: energy, throughput, the plant. The inner blade is the operator. The channel is the boundary SAFI maintains between them: a filtered path where noise is removed before it reaches the person. Two parts, one flame: a co-pilot, not a replacement.",
  scores=[2, 4, 3, 3, 4, 3],
  critique=["The outer silhouette sits in the same family as well-known consumer flame icons (fire emoji, dating apps). Once the channel closes, which it does below 24px, that generic silhouette is all that remains.",
            "The channel carries all the meaning, and it is the first thing to disappear when the mark is reduced.",
            "Construction is clean: 9 arcs and 2 straight edges, all from 8 circles."]),
 dict(key="02-laminar", name="Laminar", sub="The flame read through plates",
  build=[
   "Start from the flame primitive.",
   "Lay three vertical plates over it on the module: width 24 (4u), gap 12 (2u), from x = 12 to x = 108. The plate edges fall on the primitive's key points: x = 36 on the secondary tip T₂, x = 48 on the notch N, x = 72 on the main tip T.",
   "Keep only what lies inside the plates. Each plate inherits its top from the flame and ends in one arc and one sharp corner: the outer plates take the flank arcs, and the centre plate takes the notch-to-tip arc. The notch arc to T₂ falls entirely in a gap."],
  meaning="Three plates are a filter element, a heat-exchanger plate pack and a row of level bars on an HMI, all at once. The flame exists only where they agree. Energy that has passed through structure is controlled, laminar and measurable. The flame is never drawn: it appears in the collective outline of the plates.",
  scores=[4, 4, 4, 5, 5, 4],
  critique=["At a glance it can be read as three blades, a bar chart or a tulip. The flame reading depends on the centre plate's rising edge, so plate count and gaps must stay fixed.",
            "The 12-unit gaps become 1.6px at 16px. They hold in the test below, but this is the limit; a dedicated favicon cut may be needed.",
            "Most disciplined of the three: one primitive and one rule (intersection with equal plates). 7 arcs and 7 straight edges."]),
 dict(key="03-gate", name="Gate", sub="The flame as the counter of a block",
  build=[
   "Draw the block: a 120 × 120 square, the full 20u artboard.",
   "Scale the flame primitive to 10/16 (base width 60 = 10u) and stand it on the block's base line.",
   "Subtract it. The flame becomes the counter, opening at the base, and the block becomes the structure that contains it."],
  meaning="The block is the operating envelope: the limits the operators define. The flame burns inside it, rising from the base and never touching the walls. Stability is the dominant form, and energy is the space that it holds.",
  scores=[2, 5, 3, 4, 4, 5],
  critique=["A flame cut out of a square is a common icon pattern (fire-safety signage, generic 'burn' icons). This is its weakest point, and it is a serious one for a corporate mark.",
            "It is an emblem rather than a symbol: it needs its container, and in a lockup the solid square outweighs the wordmark.",
            "It is the strongest at 16px: one solid shape with one counter."]),
]
CRIT = ["Originality", "Simplicity", "Memorability", "Industrial credibility", "Geometric quality", "Scalability"]

def concept_block(i, c):
    k = c["key"]; m = meta[k]
    tests = "".join(f'<figure class="px"><img src="{png(f"{k}/pixel-test/app-icon-{s}.png")}" width="{s*3}" height="{s*3}" alt="App icon rendered at {s} pixels, enlarged"><figcaption>{s}px</figcaption></figure>' for s in (16, 24, 32, 48))
    actual = "".join(f'<img src="{png(f"{k}/pixel-test/{n}-{s}.png")}" width="{s}" height="{s}" alt="">' for n in ("symbol-black", "app-icon") for s in (16, 24, 32, 48))
    build = "".join(f"<li>{b}</li>" for b in c["build"])
    crit = "".join(f"<li>{x}</li>" for x in c["critique"])
    return f'''
<section class="concept" id="{k}">
  <header class="c-head">
    <p class="label">Concept {i}</p>
    <h2>{c["name"]}</h2>
    <p class="sub">{c["sub"]}</p>
  </header>
  <div class="steps">
    <div class="step s-construct">
      <p class="step-n">1 · Construction</p>
      <div class="drawing">{svg(k + "/construction.svg")}</div>
      <ol class="build">{build}</ol>
      <p class="spec">{m["circles"]} construction circles · {m["arcs"]} arcs · {m["lines"]} straight edges · module u = 6</p>
    </div>
    <div class="step s-logo">
      <p class="step-n">2 · Black-and-white logo</p>
      <div class="hero-mark">{svg(k + "/symbol-black.svg")}</div>
    </div>
    <div class="step s-meaning">
      <p class="step-n">3 · Meaning</p>
      <p>{c["meaning"]}</p>
    </div>
    <div class="step s-symbol">
      <p class="step-n">4 · Standalone symbol</p>
      <div class="pair"><div class="on-white">{svg(k + "/symbol-black.svg")}</div><div class="on-black">{svg(k + "/symbol-white.svg")}</div></div>
    </div>
    <div class="step s-lockup">
      <p class="step-n">5 · With the SAFI wordmark</p>
      <div class="lock on-white">{svg(k + "/lockup-black.svg")}</div>
      <div class="lock on-black">{svg(k + "/lockup-white.svg")}</div>
    </div>
    <div class="step s-pixels">
      <p class="step-n">6 · Small-size app icon test</p>
      <p class="note">Rasterised at true pixel size, then enlarged 3× with no smoothing. What you see is what a phone or browser tab renders.</p>
      <div class="pxrow">{tests}</div>
      <p class="note">Actual size:</p>
      <div class="actual">{actual}</div>
    </div>
    <div class="step s-crit">
      <p class="step-n">Critique</p>
      <ul>{crit}</ul>
    </div>
  </div>
</section>'''

def table():
    rows = ""
    for j, cr in enumerate(CRIT):
        rows += f"<tr><th scope=row>{cr}</th>" + "".join(f'<td><span class="pips" aria-label="{c["scores"][j]} of 5">' + "".join(f'<i class="{"on" if q < c["scores"][j] else ""}"></i>' for q in range(5)) + f'</span> <span class="n">{c["scores"][j]}</span></td>' for c in CONCEPTS) + "</tr>"
    rows += "<tr class=tot><th scope=row>Total</th>" + "".join(f'<td><span class="n">{sum(c["scores"])}</span> / 30</td>' for c in CONCEPTS) + "</tr>"
    head = "<tr><th></th>" + "".join(f'<th scope=col>{i+1} · {c["name"]}</th>' for i, c in enumerate(CONCEPTS)) + "</tr>"
    return f"<div class=tablewrap><table><thead>{head}</thead><tbody>{rows}</tbody></table></div>"

def primitive_list():
    return f'''<ol class="build">
  <li>Artboard 120 × 120, module u = 6 (a 20 × 20 grid). Base line at y = 108.</li>
  <li>Two flank circles of radius 96 (16u), centred at {P(F.FR)} and {P(F.FL)}. Their lens is the flame body, 96 wide.</li>
  <li>Main tip T is where the right flank crosses x = 72 (12u): T = {P(F.T)}. Secondary tip T₂ is where the left flank crosses x = 36 (6u): T₂ = {P(F.T2)}.</li>
  <li>Notch N = (48, 60), on the grid. Two concave circles carve it: radius 72 (12u) through N and T, and radius 48 (8u) through N and T₂.</li>
  <li>Cut the lens flat at the base line. Round both feet with radius 12 (2u), tangent to base and flank.</li>
</ol>'''

def page(standalone):
    fonts = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">'
    css = '''
/* Layout: an engineering drawing sheet. White paper, black ink, one grey for
   construction; every concept follows the same six-step sequence. */
:root { --paper: #FFFFFF; --ink: #0B0B0B; --rule: #D6D6D6; --sheet: #F3F3F3; --muted: #5E5E5E;
  --sans: "IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, monospace; color-scheme: light; }
* { box-sizing: border-box; }
body { background: var(--paper); color: var(--ink); font-family: var(--sans); font-size: 16px; line-height: 1.55; margin: 0; }
.wrap { max-width: 1160px; margin: 0 auto; padding-block: 0 64px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
h1, h2, h3 { font-weight: 600; line-height: 1.12; margin: 0; text-wrap: balance; letter-spacing: -.01em; }
h1 { font-size: clamp(1.9rem, 4.4vw, 3rem); }
h2 { font-size: clamp(1.6rem, 3.2vw, 2.3rem); }
p, li { max-width: 68ch; }
p { margin: 0; }
svg, img { display: block; max-width: 100%; height: auto; }
.label, .step-n { font-family: var(--mono); font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
.note, .spec { font-size: .85rem; color: var(--muted); }
.spec { font-family: var(--mono); font-size: .75rem; }
header.top { padding-block: 56px 40px; display: grid; gap: 18px; border-bottom: 2px solid var(--ink); }
.lede { font-size: 1.12rem; max-width: 62ch; }
.rules { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; padding-block: 28px; border-bottom: 1px solid var(--rule); }
.rules div { display: grid; gap: 6px; min-width: 0; font-size: .92rem; }
section { padding-block: 56px; border-bottom: 1px solid var(--rule); }
.prim { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: 40px; align-items: start; }
.build { margin: 0; padding-left: 1.2em; display: grid; gap: 8px; font-size: .93rem; }
.drawing { background: var(--paper); border: 1px solid var(--rule); }
.c-head { display: grid; gap: 6px; margin-bottom: 32px; }
.sub { color: var(--muted); font-size: 1.05rem; }
.steps { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 20px; }
.step { display: grid; gap: 14px; align-content: start; min-width: 0; }
.s-construct { grid-column: span 5; grid-row: span 2; }
.s-logo { grid-column: span 4; }
.s-meaning { grid-column: span 3; }
.s-symbol { grid-column: span 7; }
.s-lockup { grid-column: span 7; }
.s-pixels { grid-column: span 5; }
.s-crit { grid-column: span 12; border-top: 1px solid var(--rule); padding-top: 20px; }
.s-crit ul { margin: 0; padding-left: 1.1em; display: grid; gap: 6px; font-size: .93rem; }
.hero-mark { background: var(--sheet); aspect-ratio: 1; display: grid; place-items: center; padding: 18%; }
.hero-mark svg { width: 100%; max-height: 100%; }
.pair { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.on-white, .on-black { aspect-ratio: 16 / 10; display: grid; place-items: center; padding: 10%; border: 1px solid var(--rule); }
.on-black { background: var(--ink); border-color: var(--ink); }
.pair svg { height: 100%; width: auto; max-height: 120px; }
.lock { aspect-ratio: auto; padding: 36px 28px; }
.lock svg { width: 100%; max-width: 340px; }
.pxrow { display: flex; flex-wrap: wrap; gap: 18px; align-items: end; }
.px { margin: 0; display: grid; gap: 6px; justify-items: center; }
.px img { image-rendering: pixelated; image-rendering: crisp-edges; }
.px figcaption { font-family: var(--mono); font-size: .72rem; color: var(--muted); }
.actual { display: flex; gap: 12px; align-items: end; flex-wrap: wrap; }
.tablewrap { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; min-width: 560px; font-size: .93rem; }
th, td { text-align: left; padding: 12px; border-bottom: 1px solid var(--rule); }
thead th { font-family: var(--mono); font-size: .72rem; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); font-weight: 500; }
tbody th { font-weight: 500; }
.pips { display: inline-flex; gap: 3px; vertical-align: middle; }
.pips i { width: 16px; height: 6px; background: var(--rule); }
.pips i.on { background: var(--ink); }
.n { font-family: var(--mono); font-variant-numeric: tabular-nums; margin-left: 6px; }
tr.tot td, tr.tot th { font-weight: 600; border-bottom: 2px solid var(--ink); }
.rec { display: grid; grid-template-columns: minmax(0, 4fr) minmax(0, 7fr); gap: 40px; align-items: start; }
.rec .hero-mark { padding: 14%; }
.rec-body { display: grid; gap: 16px; }
.rec-body ul { margin: 0; padding-left: 1.1em; display: grid; gap: 8px; }
.approve { border: 2px solid var(--ink); padding: 20px; display: grid; gap: 8px; }
@media (max-width: 900px) {
  .prim, .rec { grid-template-columns: minmax(0, 1fr); }
  .steps { grid-template-columns: minmax(0, 1fr); }
  .steps > .step { grid-column: auto; grid-row: auto; }
  .rules { grid-template-columns: minmax(0, 1fr); }
}
'''
    body = f'''<title>SAFI Symbol Concepts</title>
<meta name="claude:viewport-fit-sides" content="cover">
{fonts}
<style>{css}</style>
<div class="wrap">
  <header class="top">
    <p class="label">SAFI · Symbol development · Round 2 · Black and white</p>
    <h1>Three directions for the SAFI symbol</h1>
    <p class="lede">Every mark here is built with compass and straight-edge on a 6-unit grid and drawn in black only. Colour, final typography and the wider identity are held back until one symbol is approved.</p>
  </header>
  <div class="rules">
    <div><span class="label">Geometry</span><span>Every edge is a circle from the construction drawing or a straight line. There are no freehand curves.</span></div>
    <div><span class="label">Silhouette</span><span>Each mark is tested as one solid black shape, at 24px and 16px, without the wordmark.</span></div>
    <div><span class="label">Presentation</span><span>No colour, gradients, shadows or mockups. The provisional wordmark is the same for all three.</span></div>
  </div>

  <section>
    <div class="c-head"><p class="label">Shared construction</p><h2>The flame primitive</h2><p class="sub">All three concepts integrate the same flame in different ways. It is drawn once, from five circles and one line.</p></div>
    <div class="prim">
      <div class="drawing">{svg("01-tandem/construction.svg").replace('fill-opacity=".1"', 'fill-opacity=".04"')}</div>
      <div class="rec-body">{primitive_list()}
        <p class="note">Why two tongues: a single pointed shape with a round base reads as a drop of oil. A second, lower tongue is what makes a flame a flame. The flat base stops it reading as a drop and sets it on a level.</p>
      </div>
    </div>
  </section>

  {"".join(concept_block(i+1, c) for i, c in enumerate(CONCEPTS))}

  <section>
    <div class="c-head"><p class="label">Evaluation</p><h2>Scored on the same six criteria</h2><p class="sub">1 = weak, 5 = strong. Scores are critical, and the most complex concept is not favoured.</p></div>
    {table()}
  </section>

  <section>
    <div class="c-head"><p class="label">Recommendation</p><h2>Develop Concept 2, Laminar</h2></div>
    <div class="rec">
      <div class="hero-mark">{svg("02-laminar/symbol-black.svg")}</div>
      <div class="rec-body">
        <p>Laminar is the only direction where the flame is integrated rather than drawn. There is no flame outline anywhere in the mark: three equal plates, cut by one construction, produce it. That is what makes it ownable.</p>
        <ul>
          <li><b>Originality.</b> Tandem and Gate both end in silhouettes that already exist: a flame icon, and a flame cut out of a square. Laminar's silhouette of three rising plates is not a stock shape.</li>
          <li><b>Industrial credibility.</b> Plates are the vocabulary of the industry: filter elements, plate heat exchangers, separator internals and HMI level bars. It looks engineered because it is built the way engineered parts are.</li>
          <li><b>It covers the brief without decoration.</b> Energy is the flame outline. Filtration and purification are the plates and the gaps between them. Control and stability are equal plates, a common base and a fixed rhythm.</li>
          <li><b>Scalability.</b> It still reads as three rising forms at 16px. Tandem's meaning lives in a channel that disappears at that size.</li>
          <li><b>Not chosen for complexity.</b> Gate is simpler and scores higher on scalability. It loses on originality, which matters most for a corporate symbol.</li>
        </ul>
        <div class="approve">
          <p class="label">Before colour and identity</p>
          <p>Approve or redirect the symbol first. On approval, the next step is optical refinement: tip overshoot, gap compensation at small sizes and a dedicated 16px cut. Only then come the final wordmark (drawn to the plate rhythm), the palette and the complete identity.</p>
        </div>
      </div>
    </div>
  </section>
</div>'''
    if standalone:
        return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                + body.replace("</style>", "</style>\n</head>\n<body>", 1) + "\n</body>\n</html>\n")
    return body

open(os.path.join(D, "index.html"), "w").write(page(True))
if len(sys.argv) > 1: open(sys.argv[1], "w").write(page(False))
print("ok")
