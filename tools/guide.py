"""Generate the SAFI brand guidelines page from the built SVG assets.
Writes public/branding/brand-guide.html (standalone) and, if a path is given
as argv[1], a body-only copy for publishing."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from symbol import HULL
D = os.path.join(os.path.dirname(__file__), "..", "public", "branding")

def svg(name, cls=""):
    s = open(os.path.join(D, name)).read().strip()
    m = re.search(r"<title[^>]*>(.*?)</title>", s); label = m.group(1) if m else "SAFI"
    s = re.sub(r"<title[^>]*>.*?</title>", "", s)
    s = s.replace(' role="img" aria-labelledby="t"', f' role="img" aria-label="{label}"' + (f' class="{cls}"' if cls else ""))
    return s

CONCEPTS = [
    ("A", "Strata", "concept-a-strata.svg",
     "The flame is sliced into filter lamellae: turbulent input below, a clean tongue above.",
     [3, 4, 3, 2, 2, 3],
     "Stripes read as retro speed lines before they read as filtration, and the slots close up below 24px."),
    ("B", "Envelope", "concept-b-envelope.svg",
     "A burner core inside a protective shell, the layers-of-protection model drawn as one flame.",
     [3, 5, 4, 2, 4, 4],
     "Clean and exact, but the nested arch reads as a doorway or a generic gas-utility mark."),
    ("C", "Filter Gate", "concept-c-filter-gate.svg",
     "The P&amp;ID filter rhombus, cut by its filter line, with a flame passing through it.",
     [4, 2, 5, 4, 2, 4],
     "The most literate to engineers, but a flame in a diamond is the DOT/GHS flammable placard. Too close to a hazard sign."),
    ("D", "Tandem Flame", "concept-d-tandem-flame.svg",
     "Two interlocking flame blades separated by a constant-width S-channel on a level base.",
     [5, 4, 4, 5, 4, 5],
     "Selected. One silhouette, one cut, unmistakably a flame, and the S is there for those who look."),
]
CRIT = ["Recognition", "Simplicity", "Industrial relevance", "Memorability", "Scalability", "Professionalism"]

def concept_cards():
    out = []
    for key, name, f, idea, sc, verdict in CONCEPTS:
        sel = key == "D"
        bars = "".join(f'<li><span>{c}</span><span class="pips" aria-label="{v} of 5">' +
                       "".join(f'<i class="{"on" if k < v else ""}"></i>' for k in range(5)) +
                       f'</span></li>' for c, v in zip(CRIT, sc))
        out.append(f'''<article class="concept{' is-selected' if sel else ''}">
  <div class="concept-art">{svg("exploration/" + f)}</div>
  <div class="concept-body">
    <p class="eyebrow">Concept {key}{' · selected' if sel else ''}</p>
    <h3>{name}</h3>
    <p>{idea}</p>
    <ul class="scores">{bars}</ul>
    <p class="total"><span class="mono">{sum(sc)}/30</span> {verdict}</p>
  </div>
</article>''')
    return "\n".join(out)

def construction():
    sym = open(os.path.join(D, "safi-symbol.svg")).read()
    paths = re.findall(r'<path[^>]*d="([^"]+)"', sym)[0]
    tr = re.search(r'transform="([^"]+)"', sym).group(1)
    return f'''<svg viewBox="0 0 120 120" role="img" aria-label="Construction of the SAFI symbol" class="construct">
  <g transform="{tr}">
    <path d="{paths}" fill="var(--flare)"/>
    <path d="{HULL}" fill="none" stroke="var(--ivory)" stroke-width=".35" stroke-dasharray="1.2 1.2" opacity=".7"/>
    <line x1="10" y1="110" x2="110" y2="110" stroke="var(--steel)" stroke-width=".4"/>
    <line x1="66" y1="0" x2="66" y2="110" stroke="var(--steel)" stroke-width=".3" stroke-dasharray=".8 1.2"/>
  </g>
</svg>'''

SIZES = [16, 20, 24, 32, 48, 64]

def page(standalone=True):
    sym = svg("safi-symbol.svg")
    small = "".join(f'<figure class="sz"><div style="width:{s}px;height:{s}px">{svg("safi-app-icon.svg")}</div><figcaption class="mono">{s}</figcaption></figure>' for s in SIZES)
    small_sym = "".join(f'<figure class="sz"><div style="width:{s}px;height:{s}px">{sym}</div><figcaption class="mono">{s}</figcaption></figure>' for s in SIZES)
    head = '''<title>SAFI Brand Identity</title>
<meta name="claude:viewport-fit-sides" content="cover">'''
    fonts = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,400..800&family=IBM+Plex+Mono:wght@400;500&display=swap">'
    body = f'''{head}
{fonts}
<style>
/* Layout: a long, single-column specimen on graphite; light-background
   demonstrations sit on ivory plates, like drawing sheets on a desk. */
:root {{
  --graphite: #16191D; --graphite-2: #1E2227; --graphite-3: #2A2F35;
  --flare: #E0782A; --ember: #A34C16; --ivory: #F4EFE6; --ivory-2: #E9E2D5;
  --petroleum: #14403D; --steel: #8A9199; --fg: #F4EFE6; --muted: #A4ABB3;
  --display: "Archivo", "Arial Narrow", system-ui, sans-serif;
  --body: "Archivo", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, "SFMono-Regular", Menlo, monospace;
  color-scheme: dark;
}}
* {{ box-sizing: border-box; }}
body {{ background: var(--graphite); color: var(--fg); font-family: var(--body); font-size: 16px; line-height: 1.55; margin: 0; }}
.wrap {{ max-width: 1120px; margin: 0 auto; padding-block: 0; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }}
h1, h2, h3 {{ font-family: var(--display); font-stretch: 112%; letter-spacing: .01em; line-height: 1.1; text-wrap: balance; margin: 0; }}
h2 {{ font-size: clamp(1.6rem, 3.2vw, 2.25rem); font-weight: 650; }}
h3 {{ font-size: 1.15rem; font-weight: 650; }}
p {{ margin: 0; max-width: 65ch; }}
.mono {{ font-family: var(--mono); font-size: .8rem; letter-spacing: .02em; font-variant-numeric: tabular-nums; }}
.eyebrow {{ font-family: var(--mono); font-size: .72rem; letter-spacing: .14em; text-transform: uppercase; color: var(--flare); }}
.muted {{ color: var(--muted); }}
section {{ padding-block: clamp(56px, 9vw, 104px); border-top: 1px solid var(--graphite-3); }}
.sec-head {{ display: grid; gap: 12px; margin-bottom: 40px; }}
svg {{ display: block; max-width: 100%; height: auto; }}

/* hero */
.hero {{ padding-block: clamp(48px, 10vw, 120px) clamp(40px, 7vw, 80px); display: grid; gap: 40px; }}
.hero-logo {{ width: min(560px, 100%); }}
.hero-meta {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 24px; border-top: 1px solid var(--graphite-3); padding-top: 24px; }}
.hero-meta div {{ display: grid; gap: 6px; min-width: 0; }}
.lede {{ font-size: clamp(1.15rem, 2.2vw, 1.4rem); line-height: 1.45; max-width: 46ch; }}

/* idea */
.idea {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 48px; align-items: center; }}
.construct {{ width: 100%; max-width: 440px; background: var(--graphite-2); border-radius: 4px; }}
.parts {{ display: grid; gap: 22px; list-style: none; padding: 0; margin: 0; }}
.parts li {{ display: grid; grid-template-columns: 112px minmax(0, 1fr); gap: 16px; }}
.parts b {{ font-family: var(--mono); font-size: .75rem; font-weight: 500; letter-spacing: .08em; text-transform: uppercase; color: var(--flare); padding-top: 3px; }}

/* concepts */
.concepts {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }}
.concept {{ display: grid; grid-template-columns: 132px minmax(0, 1fr); gap: 20px; background: var(--graphite-2); padding: 20px; border-radius: 4px; border: 1px solid transparent; }}
.concept.is-selected {{ border-color: var(--flare); }}
.concept-art {{ background: var(--ivory); border-radius: 3px; padding: 14px; align-self: start; }}
.concept-body {{ display: grid; gap: 10px; min-width: 0; align-content: start; }}
.scores {{ list-style: none; padding: 0; margin: 4px 0 0; display: grid; gap: 4px; }}
.scores li {{ display: flex; justify-content: space-between; gap: 12px; font-size: .82rem; color: var(--muted); }}
.pips {{ display: inline-flex; gap: 3px; align-items: center; }}
.pips i {{ width: 14px; height: 4px; background: var(--graphite-3); }}
.pips i.on {{ background: var(--steel); }}
.is-selected .pips i.on {{ background: var(--flare); }}
.total {{ font-size: .88rem; color: var(--muted); border-top: 1px solid var(--graphite-3); padding-top: 10px; }}
.total .mono {{ color: var(--fg); margin-right: 6px; }}

/* logo suite */
.suite {{ display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 16px; }}
.plate {{ border-radius: 4px; padding: clamp(24px, 4vw, 48px); display: grid; grid-template-rows: 1fr auto; gap: 28px; min-width: 0; }}
.plate.light {{ background: var(--ivory); color: var(--graphite); }}
.plate.dark {{ background: var(--graphite-2); }}
.plate.flare {{ background: var(--flare); color: var(--graphite); }}
.plate.white {{ background: #FFFFFF; color: #000; }}
.plate.black {{ background: #000; color: #fff; }}
.plate .cap {{ display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; font-family: var(--mono); font-size: .72rem; letter-spacing: .06em; opacity: .75; }}
.span-3 {{ grid-column: span 3; }} .span-2 {{ grid-column: span 2; }} .span-6 {{ grid-column: span 6; }}
.plate .art {{ display: grid; place-items: center; min-height: 140px; }}
.plate .art svg {{ width: 100%; }}
.art .w-lock {{ max-width: 360px; }} .art .w-stack {{ max-width: 170px; }} .art .w-sym {{ max-width: 120px; }} .art .w-word {{ max-width: 260px; }}

/* icons */
.icons {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }}
.icons figure {{ margin: 0; display: grid; gap: 12px; }}
.icons svg {{ width: 100%; max-width: 220px; filter: drop-shadow(0 10px 24px rgba(0,0,0,.35)); }}
.ramp {{ display: flex; flex-wrap: wrap; align-items: end; gap: 28px; margin-top: 40px; padding: 28px; background: var(--graphite-2); border-radius: 4px; }}
.ramp.light {{ background: var(--ivory); color: var(--graphite); }}
.sz {{ margin: 0; display: grid; gap: 8px; justify-items: center; }}
.sz div svg {{ width: 100%; height: 100%; }}
.sz figcaption {{ opacity: .7; }}

/* colour */
.swatches {{ display: grid; grid-template-columns: 2fr 2fr 1.4fr 1fr 1fr 1fr; gap: 12px; }}
.sw {{ border-radius: 4px; min-height: 220px; padding: 18px; display: grid; align-content: space-between; gap: 18px; min-width: 0; }}
.sw b {{ font-family: var(--display); font-stretch: 112%; font-size: 1.05rem; font-weight: 650; }}
.sw p {{ font-size: .82rem; line-height: 1.4; }}
.note {{ margin-top: 32px; display: grid; grid-template-columns: 112px minmax(0, 1fr); gap: 16px; padding: 22px; border-left: 2px solid var(--flare); background: var(--graphite-2); }}

/* usage */
.usage {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }}
.rule {{ background: var(--graphite-2); border-radius: 4px; padding: 22px; display: grid; gap: 14px; align-content: start; min-width: 0; }}
.clear {{ background: var(--ivory); border-radius: 3px; padding: 18px; }}
.clear-box {{ outline: 1px dashed var(--flare); outline-offset: 0; padding: 12%; }}
.dont {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; margin-top: 16px; }}
.dont figure {{ margin: 0; display: grid; gap: 10px; }}
.dont .x {{ background: var(--ivory); border-radius: 3px; padding: 18px; aspect-ratio: 4 / 3; display: grid; place-items: center; position: relative; overflow: hidden; }}
.dont .x::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(to top right, transparent calc(50% - 1px), #C0392B calc(50% - 1px), #C0392B calc(50% + 1px), transparent calc(50% + 1px)); opacity: .8; }}
.dont .x svg {{ width: 70%; }}
.dont figcaption {{ font-size: .85rem; color: var(--muted); }}

/* in context */
.app {{ border-radius: 6px; overflow: hidden; border: 1px solid var(--graphite-3); background: #23272C; }}
.app-bar {{ display: flex; align-items: center; gap: 24px; flex-wrap: wrap; padding: 12px 20px; background: var(--graphite); border-bottom: 1px solid var(--graphite-3); }}
.app-bar .lock {{ width: 104px; }}
.app-bar nav {{ display: flex; gap: 18px; font-size: .85rem; color: var(--muted); flex-wrap: wrap; }}
.app-bar nav b {{ color: var(--fg); font-weight: 600; }}
.pill {{ margin-left: auto; font-family: var(--mono); font-size: .72rem; letter-spacing: .06em; padding: 5px 10px; border-radius: 99px; background: var(--petroleum); color: #CFE5E1; }}
.app-body {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1px; background: var(--graphite-3); }}
.kpi {{ background: #23272C; padding: 20px; display: grid; gap: 6px; min-width: 0; }}
.kpi .v {{ font-family: var(--mono); font-size: 1.6rem; color: var(--fg); font-variant-numeric: tabular-nums; }}
.kpi .l {{ font-size: .8rem; color: var(--muted); }}

/* files */
.files {{ overflow-x: auto; }}
table {{ width: 100%; border-collapse: collapse; font-size: .88rem; min-width: 560px; }}
th, td {{ text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--graphite-3); vertical-align: top; }}
th {{ font-family: var(--mono); font-size: .7rem; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); font-weight: 500; }}
td:first-child {{ font-family: var(--mono); font-size: .8rem; color: var(--fg); white-space: nowrap; }}
footer {{ padding-block: 48px; border-top: 1px solid var(--graphite-3); color: var(--muted); font-size: .85rem; }}

@media (max-width: 860px) {{
  .idea, .concepts {{ grid-template-columns: minmax(0, 1fr); }}
  .suite {{ grid-template-columns: minmax(0, 1fr); }}
  .span-3, .span-2, .span-6 {{ grid-column: auto; }}
  .icons, .usage {{ grid-template-columns: minmax(0, 1fr); }}
  .swatches {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  .dont {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  .app-body {{ grid-template-columns: minmax(0, 1fr); }}
}}
@media (max-width: 480px) {{
  .concept {{ grid-template-columns: minmax(0, 1fr); }}
  .concept-art {{ max-width: 160px; }}
  .parts li, .note {{ grid-template-columns: minmax(0, 1fr); gap: 6px; }}
}}
</style>

<div class="wrap">
  <header class="hero">
    <p class="eyebrow">Brand identity · v1.0 · November 2026</p>
    <div class="hero-logo">{svg("safi-logo-primary-dark.svg")}</div>
    <p class="lede">An operational co-pilot for oil and gas control rooms. The identity is built for the people who run the process: calm, exact and confident, with one point of heat.</p>
    <div class="hero-meta">
      <div><span class="eyebrow">Symbol</span><span>Tandem Flame</span></div>
      <div><span class="eyebrow">Wordmark</span><span>Custom extended capitals, cap-height 100u, stroke 15u</span></div>
      <div><span class="eyebrow">Palette</span><span>Graphite, Flare, Ivory, with Petroleum and Steel for product UI</span></div>
    </div>
  </header>

  <section>
    <div class="sec-head"><p class="eyebrow">The idea</p><h2>Two flames, one boundary between them</h2></div>
    <div class="idea">
      {construction()}
      <ul class="parts">
        <li><b>Outer blade</b><p>The process: energy, throughput, the flame of the plant. It wraps and protects everything inside it.</p></li>
        <li><b>Inner blade</b><p>The operator. A second, smaller tongue that leans the other way: SAFI and the crew working in tandem, neither one replacing the other.</p></li>
        <li><b>S-channel</b><p>A cut of constant width (4.6u) that separates the two. It is the filter path, where noise is taken out before it reaches the operator, and it draws the letter S.</p></li>
        <li><b>Level base</b><p>The flame stands on a flat, horizontal base: a setpoint, a stable operating level. No drop, no bulb, no flicker.</p></li>
      </ul>
    </div>
  </section>

  <section>
    <div class="sec-head"><p class="eyebrow">Exploration</p><h2>Four constructions, scored on the same six criteria</h2><p class="muted">Each concept uses a different visual construction: subtraction by bands, concentric offset, figure and ground in a container, and a single channel cut. Scores are 1 to 5.</p></div>
    <div class="concepts">{concept_cards()}</div>
  </section>

  <section>
    <div class="sec-head"><p class="eyebrow">Logo suite</p><h2>Primary, secondary and single-colour versions</h2></div>
    <div class="suite">
      <div class="plate light span-3"><div class="art"><div class="w-lock" style="width:100%">{svg("safi-logo-primary.svg")}</div></div><div class="cap"><span>Primary · light backgrounds</span><span>safi-logo-primary.svg</span></div></div>
      <div class="plate dark span-3"><div class="art"><div class="w-lock" style="width:100%">{svg("safi-logo-primary-dark.svg")}</div></div><div class="cap"><span>Primary · dark backgrounds</span><span>safi-logo-primary-dark.svg</span></div></div>
      <div class="plate light span-2"><div class="art"><div class="w-sym" style="width:100%">{svg("safi-symbol.svg")}</div></div><div class="cap"><span>Secondary · symbol</span><span>safi-symbol.svg</span></div></div>
      <div class="plate dark span-2"><div class="art"><div class="w-stack" style="width:100%">{svg("safi-logo-stacked-dark.svg")}</div></div><div class="cap"><span>Stacked</span><span>safi-logo-stacked-dark.svg</span></div></div>
      <div class="plate light span-2"><div class="art"><div class="w-word" style="width:100%">{svg("safi-wordmark.svg")}</div></div><div class="cap"><span>Wordmark</span><span>safi-wordmark.svg</span></div></div>
      <div class="plate white span-3"><div class="art"><div class="w-lock" style="width:100%">{svg("safi-logo-mono-black.svg")}</div></div><div class="cap"><span>Monochrome · black</span><span>safi-logo-mono-black.svg</span></div></div>
      <div class="plate black span-3"><div class="art"><div class="w-lock" style="width:100%">{svg("safi-logo-mono-white.svg")}</div></div><div class="cap"><span>Monochrome · white</span><span>safi-logo-mono-white.svg</span></div></div>
    </div>
  </section>

  <section>
    <div class="sec-head"><p class="eyebrow">App icon</p><h2>Built to hold at 16 pixels</h2><p class="muted">The symbol is one solid silhouette with a single cut, so it keeps its shape at favicon size. Below about 20px the channel closes and the silhouette carries the mark on its own. That is intended.</p></div>
    <div class="icons">
      <figure>{svg("safi-app-icon.svg")}<figcaption class="mono muted">safi-app-icon.svg · primary</figcaption></figure>
      <figure>{svg("safi-app-icon-light.svg")}<figcaption class="mono muted">safi-app-icon-light.svg</figcaption></figure>
      <figure>{svg("safi-app-icon-mono.svg")}<figcaption class="mono muted">safi-app-icon-mono.svg</figcaption></figure>
    </div>
    <div class="ramp">{small}</div>
    <div class="ramp light">{small_sym}</div>
  </section>

  <section>
    <div class="sec-head"><p class="eyebrow">Colour</p><h2>Graphite and Flare, with Ivory for air</h2><p class="muted">Solid colours only. No gradients in the mark. Graphite carries the brand, Flare is the single point of heat, Ivory is the light surface.</p></div>
    <div class="swatches">
      <div class="sw" style="background:var(--graphite);outline:1px solid var(--graphite-3)"><b>Graphite</b><p class="mono">#16191D<br>RGB 22 25 29</p><p class="muted">Primary dark. Wordmark, UI chrome, icon field.</p></div>
      <div class="sw" style="background:var(--flare);color:var(--graphite)"><b>Flare</b><p class="mono">#E0782A<br>RGB 224 120 42</p><p>Signature accent. The symbol and brand moments.</p></div>
      <div class="sw" style="background:var(--ivory);color:var(--graphite)"><b>Ivory</b><p class="mono">#F4EFE6<br>RGB 244 239 230</p><p>Light surface. Wordmark on dark.</p></div>
      <div class="sw" style="background:var(--petroleum)"><b>Petroleum</b><p class="mono">#14403D</p><p>Stable, in-limits states.</p></div>
      <div class="sw" style="background:var(--steel);color:var(--graphite)"><b>Steel</b><p class="mono">#8A9199</p><p>Neutral, rules, secondary text.</p></div>
      <div class="sw" style="background:var(--ember)"><b>Ember</b><p class="mono">#A34C16</p><p>Flare at text size. 5.1:1 on Ivory.</p></div>
    </div>
    <div class="note"><b class="eyebrow">Inside the HMI</b><p>Control-room displays built to ISA-101 keep colour for abnormal conditions, and amber is commonly an alarm-priority colour. Inside operator screens, keep Flare to the logo and splash. Use Graphite, Steel and Petroleum for interface accents so the brand never looks like an alarm.</p></div>
  </section>

  <section>
    <div class="sec-head"><p class="eyebrow">Usage</p><h2>Clear space, minimum size, and what to avoid</h2></div>
    <div class="usage">
      <div class="rule"><h3>Clear space</h3><div class="clear"><div class="clear-box">{svg("safi-logo-primary.svg")}</div></div><p class="muted">Keep a margin of one quarter of the symbol height on every side.</p></div>
      <div class="rule"><h3>Minimum size</h3><p class="mono">Lockup ≥ 96px wide (24mm print)<br>Symbol ≥ 16px (5mm print)</p><p class="muted">Below 96px, use the symbol alone. The wordmark is never set smaller than 12px cap height.</p></div>
      <div class="rule"><h3>Proportions</h3><p class="mono">Cap height = 0.54 × symbol height<br>Gap = 0.27 × symbol height<br>S-channel = 4.6 / 106 of symbol height</p><p class="muted">Always use the supplied files. Never retype the wordmark in a font.</p></div>
    </div>
    <div class="dont">
      <figure><div class="x"><div style="width:70%;transform:scaleX(1.4)">{svg("safi-symbol.svg")}</div></div><figcaption>Don't stretch or condense.</figcaption></figure>
      <figure><div class="x"><div style="width:70%;transform:rotate(-18deg)">{svg("safi-symbol.svg")}</div></div><figcaption>Don't rotate or tilt the flame.</figcaption></figure>
      <figure><div class="x"><div style="width:70%"><svg viewBox="0 0 120 120"><defs><linearGradient id="bad" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#C0392B"/><stop offset="1" stop-color="#F7C948"/></linearGradient></defs>{re.sub(r'fill="#[0-9A-Fa-f]+"', 'fill="url(#bad)"', re.sub(r"<title.*?</title>", "", open(os.path.join(D, "safi-symbol.svg")).read()).split(">",1)[1].rsplit("</svg>",1)[0])}</svg></div></div><figcaption>Don't add gradients or effects.</figcaption></figure>
      <figure><div class="x"><div style="width:70%">{svg("safi-symbol.svg").replace('fill="#E0782A"', 'fill="#2F6FD6"')}</div></div><figcaption>Don't recolour the flame outside the palette.</figcaption></figure>
    </div>
  </section>

  <section>
    <div class="sec-head"><p class="eyebrow">In context</p><h2>Application header</h2><p class="muted">Example screen, with sample values.</p></div>
    <div class="app">
      <div class="app-bar"><div class="lock">{svg("safi-logo-primary-dark.svg")}</div><nav><b>CDU-3 · Atmospheric column</b><span>Overview</span><span>Alarms</span><span>Limits</span></nav><span class="pill">WITHIN LIMITS</span></div>
      <div class="app-body">
        <div class="kpi"><span class="l">Alarms presented / raw, last hour</span><span class="v">6 / 148</span></div>
        <div class="kpi"><span class="l">Chattering alarms filtered</span><span class="v">42</span></div>
        <div class="kpi"><span class="l">Tags inside operator limits</span><span class="v">99.2%</span></div>
      </div>
    </div>
  </section>

  <section>
    <div class="sec-head"><p class="eyebrow">Files</p><h2>/public/branding/</h2></div>
    <div class="files"><table>
      <thead><tr><th>File</th><th>Use</th></tr></thead>
      <tbody>
        <tr><td>safi-logo-primary.svg</td><td>Symbol + wordmark, light backgrounds</td></tr>
        <tr><td>safi-logo-primary-dark.svg</td><td>Symbol + wordmark, dark backgrounds</td></tr>
        <tr><td>safi-logo-stacked(-dark).svg</td><td>Square formats, splash screens</td></tr>
        <tr><td>safi-logo-mono-black/white.svg</td><td>One-colour print, engraving, fax, embossing</td></tr>
        <tr><td>safi-symbol(-ivory/-graphite/-mono-*).svg</td><td>Symbol alone, 120 × 120 artboard</td></tr>
        <tr><td>safi-wordmark(-ivory/-mono-*).svg</td><td>Wordmark alone</td></tr>
        <tr><td>safi-app-icon(-light/-mono).svg</td><td>Rounded-square app tiles, 1024 grid</td></tr>
        <tr><td>safi-app-icon-ios.svg / -maskable.svg</td><td>Full-bleed squares for OS-applied masks</td></tr>
        <tr><td>safi-favicon.svg</td><td>Browser tab icon</td></tr>
        <tr><td>png/</td><td>Raster exports for platforms that need them (touch icon, PWA, favicon)</td></tr>
        <tr><td>safi-colors.css / safi-tokens.json</td><td>Colour tokens for product code</td></tr>
        <tr><td>exploration/</td><td>The four concept constructions</td></tr>
      </tbody>
    </table></div>
  </section>

  <footer><p>SAFI brand identity v1.0. Every mark is a true vector outline made of cubic curves and straight lines. No fonts, no images and no masks are used inside the logo files.</p></footer>
</div>'''
    if standalone:
        return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                '<link rel="icon" href="safi-favicon.svg" type="image/svg+xml">\n'
                '<link rel="apple-touch-icon" href="png/apple-touch-icon-180.png">\n'
                + body.replace("</style>", "</style>\n</head>\n<body>", 1) + "\n</body>\n</html>\n")
    return body

open(os.path.join(D, "brand-guide.html"), "w").write(page(True))
if len(sys.argv) > 1:
    open(sys.argv[1], "w").write(page(False))
print("ok")
