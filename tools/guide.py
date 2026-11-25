"""SAFI brand guidelines -> public/branding/brand-guide.html (+ body-only copy)."""
import os, sys, re, base64
D = os.path.join(os.path.dirname(__file__), "..", "public", "branding")
sys.path.insert(0, os.path.dirname(__file__))
from build import OUTER, BODY, CORE, C

def svg(p, cls=""):
    s = open(os.path.join(D, p)).read().strip()
    s = s.replace('<svg xmlns="http://www.w3.org/2000/svg"', '<svg' + (f' class="{cls}"' if cls else ""), 1)
    return s.replace('id="cl"', 'id="clf"').replace('url(#cl)', 'url(#clf)')

def png(p): return "data:image/png;base64," + base64.b64encode(open(os.path.join(D, p), "rb").read()).decode()

SW = [("SAFI Navy", "#0E2236", "14 34 54", "Wordmark, text, brand surfaces.", "light"),
      ("Flame Red", "#D63A1A", "214 58 26", "Outer flame.", "light"),
      ("Flame Orange", "#EE7420", "238 116 32", "Flame body. The one accent colour in layouts.", "light"),
      ("Flame Yellow", "#F8B320", "248 179 32", "Flame core. Symbol only.", "dark"),
      ("Steel", "#5B6B78", "91 107 120", "Secondary text, rules.", "light"),
      ("Mist", "#E8ECEF", "232 236 239", "Panels, table fills.", "dark")]

def page(standalone):
    sw = "".join(f'<div class="sw" style="background:{h};color:{"#fff" if t=="light" else "#0F2A3D"}"><b>{n}</b><span class="mono">{h}<br>RGB {r}</span><span class="r">{d}</span></div>' for n, h, r, d, t in SW)
    ramp = "".join(f'<figure><div style="width:{s}px;height:{s}px">{svg("safi-favicon.svg" if s <= 32 else "safi-app-icon.svg")}</div><figcaption class="mono">{s}</figcaption></figure>' for s in (16, 24, 32, 48, 64, 96))
    fonts = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@87..125,400..700&family=IBM+Plex+Mono:wght@400;500&display=swap">'
    body = f'''<title>SAFI Brand Guidelines</title>
<meta name="claude:viewport-fit-sides" content="cover">
{fonts}
<style>
/* Layout: a corporate standards manual. White sheets, navy ink; the flame
   colours appear only where the symbol does. */
:root {{ --navy: #0E2236; --flare: #EE7420; --red: #D63A1A; --yellow: #F8B320; --white: #FFFFFF; --deep: #081624; --steel: #5B6B78; --mist: #E8ECEF; --rule: #D5DBE0;
  --sans: "Archivo", "Helvetica Neue", Arial, sans-serif; --cond: "Archivo", "Arial Narrow", sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, monospace; color-scheme: light; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--white); color: var(--navy); font-family: var(--sans); font-size: 17px; line-height: 1.55; }}
.wrap {{ max-width: 1180px; margin: 0 auto; padding-block: 0 72px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }}
h1, h2, h3 {{ margin: 0; font-weight: 600; font-stretch: 108%; line-height: 1.1; letter-spacing: -.005em; text-wrap: balance; }}
h2 {{ font-size: clamp(1.7rem, 3.4vw, 2.5rem); }}
h3 {{ font-size: 1.15rem; }}
p {{ margin: 0; max-width: 64ch; }}
svg, img {{ display: block; max-width: 100%; height: auto; }}
.mono {{ font-family: var(--mono); font-size: .78rem; letter-spacing: .02em; }}
.k {{ font-family: var(--cond); font-stretch: 87%; font-weight: 600; font-size: .8rem; letter-spacing: .14em; text-transform: uppercase; color: var(--steel); }}
.muted {{ color: var(--steel); }}
section {{ padding-block: 72px; border-top: 1px solid var(--rule); display: grid; gap: 36px; }}
.head {{ display: grid; grid-template-columns: 220px minmax(0, 1fr); gap: 24px; align-items: baseline; }}
.head > div {{ display: grid; gap: 12px; }}
.cover {{ padding-block: 40px 0; display: grid; gap: 0; }}
.cover-top {{ display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap; padding-bottom: 18px; border-bottom: 2px solid var(--navy); }}
.cover-logo {{ padding-block: clamp(64px, 12vw, 150px); display: grid; place-items: center; }}
.cover-logo svg {{ width: min(620px, 92%); }}
.cover-band {{ background: var(--navy); color: var(--white); display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; padding: 28px; }}
.cover-band div {{ display: grid; gap: 4px; min-width: 0; }}
.cover-band .k {{ color: #9FB0BE; }}
.two {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 40px; align-items: start; }}
.anat {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; align-items: end; }}
.anat figure {{ margin: 0; display: grid; gap: 10px; justify-items: center; padding: 18px 10px; background: var(--mist); }}
.anat svg {{ height: 150px; width: auto; }}
.anat .all {{ background: var(--white); border: 1px solid var(--rule); }}
.list {{ margin: 0; padding: 0; list-style: none; display: grid; gap: 18px; }}
.list li {{ display: grid; grid-template-columns: 120px minmax(0, 1fr); gap: 16px; border-top: 1px solid var(--rule); padding-top: 14px; }}
.list b {{ font-family: var(--cond); font-weight: 600; text-transform: uppercase; letter-spacing: .1em; font-size: .82rem; }}
.grid6 {{ display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 16px; }}
.tile {{ display: grid; grid-template-rows: 1fr auto; gap: 18px; padding: clamp(24px, 4vw, 44px); min-width: 0; border: 1px solid var(--rule); }}
.tile.navy {{ background: var(--navy); border-color: var(--navy); color: var(--white); }}
.tile.black {{ background: #000; border-color: #000; color: #fff; }}
.tile .art {{ display: grid; place-items: center; min-height: 130px; }}
.tile .art > * {{ width: 100%; }}
.tile .cap {{ display: flex; justify-content: space-between; gap: 10px; flex-wrap: wrap; font-family: var(--mono); font-size: .72rem; opacity: .75; }}
.s3 {{ grid-column: span 3; }} .s2 {{ grid-column: span 2; }}
.lk {{ max-width: 380px; margin: 0 auto; }} .st {{ max-width: 150px; margin: 0 auto; }} .sy {{ max-width: 110px; margin: 0 auto; }}
.ramp {{ display: flex; gap: 28px; align-items: end; flex-wrap: wrap; padding: 28px; background: var(--mist); }}
.ramp figure {{ margin: 0; display: grid; gap: 8px; justify-items: center; }}
.ramp div svg {{ width: 100%; height: 100%; }}
.icons {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; }}
.icons figure {{ margin: 0; display: grid; gap: 10px; }}
.icons figcaption {{ font-family: var(--mono); font-size: .72rem; color: var(--steel); }}
.sws {{ display: grid; grid-template-columns: 2fr 1.2fr 1.2fr 1.2fr 1fr 1fr; gap: 0; border: 1px solid var(--rule); }}
.sw {{ min-height: 230px; padding: 18px; display: grid; align-content: space-between; gap: 12px; min-width: 0; }}
.sw b {{ font-weight: 600; font-size: 1.05rem; }}
.sw .r {{ font-size: .85rem; line-height: 1.35; }}
.ratio {{ display: flex; height: 18px; }}
.ratio span {{ display: block; }}
.note {{ border-left: 3px solid var(--flare); padding: 4px 0 4px 18px; }}
.type {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 16px; }}
.spec {{ border: 1px solid var(--rule); padding: 28px; display: grid; gap: 14px; min-width: 0; }}
.big {{ font-size: clamp(2.6rem, 6vw, 4.2rem); font-weight: 600; font-stretch: 112%; line-height: 1; }}
.cond {{ font-family: var(--cond); }}
.vals {{ font-family: var(--cond); font-stretch: 87%; font-weight: 500; font-size: 1.6rem; font-variant-numeric: tabular-nums; }}
.rules3 {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }}
.rule {{ border: 1px solid var(--rule); padding: 24px; display: grid; gap: 14px; align-content: start; min-width: 0; }}
.cs {{ padding: 22px; background: var(--mist); }} .cs-box {{ outline: 1px dashed var(--flare); padding: 9%; background: var(--white); }}
.donts {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; }}
.donts figure {{ margin: 0; display: grid; gap: 10px; }}
.x {{ border: 1px solid var(--rule); aspect-ratio: 4/3; display: grid; place-items: center; overflow: hidden; position: relative; }}
.x > div {{ width: 46%; }}
.x::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(to top right, transparent calc(50% - 1px), #B3261E calc(50% - 1px), #B3261E calc(50% + 1px), transparent calc(50% + 1px)); }}
.donts figcaption {{ font-size: .88rem; color: var(--steel); }}
/* applications */
.apps {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 16px; }}
.app {{ background: var(--mist); padding: clamp(20px, 4vw, 44px); display: grid; gap: 18px; place-items: center; min-width: 0; }}
.app .cap {{ justify-self: start; }}
.card {{ width: min(100%, 340px); aspect-ratio: 85 / 55; background: var(--white); padding: 7% 8%; display: grid; grid-template-rows: auto 1fr auto; box-shadow: 0 1px 2px rgba(10,30,44,.18); }}
.card.back {{ background: var(--navy); place-items: center; grid-template-rows: 1fr; }}
.card.back svg {{ width: 16%; }}
.card .lg {{ width: 42%; }}
.card .who {{ align-self: end; font-size: .78rem; line-height: 1.35; }}
.card .who b {{ font-weight: 600; font-size: .9rem; }}
.card .ct {{ font-family: var(--cond); font-size: .68rem; color: var(--steel); display: flex; justify-content: space-between; gap: 8px; border-top: 1px solid var(--rule); padding-top: 6px; margin-top: 8px; }}
.cards {{ display: flex; gap: 16px; flex-wrap: wrap; justify-content: center; width: 100%; }}
.hmi {{ width: 100%; background: var(--deep); color: #DCE3E8; font-family: var(--cond); }}
.hmi-bar {{ display: flex; align-items: center; gap: 18px; padding: 10px 16px; border-bottom: 1px solid #1E3546; flex-wrap: wrap; }}
.hmi-bar .lg {{ width: 92px; }}
.hmi-bar nav {{ display: flex; gap: 16px; font-size: .85rem; color: #8FA2B1; flex-wrap: wrap; }}
.hmi-bar nav b {{ color: #fff; font-weight: 600; }}
.hmi-bar .st {{ margin-left: auto; font-size: .75rem; letter-spacing: .08em; border: 1px solid #3C5466; padding: 3px 8px; }}
.hmi-body {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1px; background: #1E3546; }}
.hmi-body div {{ background: var(--deep); padding: 14px 16px; display: grid; gap: 2px; min-width: 0; }}
.hmi-body span {{ font-size: .75rem; color: #8FA2B1; }}
.hmi-body b {{ font-size: 1.35rem; font-weight: 500; font-variant-numeric: tabular-nums; color: #fff; }}
.letter {{ width: min(100%, 420px); aspect-ratio: 210 / 150; background: var(--white); box-shadow: 0 1px 2px rgba(10,30,44,.18); padding: 6% 7%; display: grid; grid-template-rows: auto auto 1fr; gap: 10%; }}
.letter .top {{ display: flex; justify-content: space-between; align-items: start; gap: 12px; }}
.letter .lg {{ width: 34%; }}
.letter .addr {{ font-family: var(--cond); font-size: .6rem; color: var(--steel); text-align: right; line-height: 1.4; }}
.letter .ln {{ display: grid; gap: 7px; }}
.letter .ln i {{ display: block; height: 4px; background: var(--mist); }}
.letter h4 {{ margin: 0; font-size: .8rem; font-weight: 600; }}
.files {{ overflow-x: auto; }}
table {{ width: 100%; min-width: 560px; border-collapse: collapse; font-size: .92rem; }}
th, td {{ text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--rule); vertical-align: top; }}
th {{ font-family: var(--cond); font-weight: 600; letter-spacing: .12em; text-transform: uppercase; font-size: .75rem; color: var(--steel); }}
td:first-child {{ font-family: var(--mono); font-size: .8rem; white-space: nowrap; }}
@media (max-width: 900px) {{
  .anat {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  .head, .two, .type, .apps {{ grid-template-columns: minmax(0, 1fr); }}
  .grid6 {{ grid-template-columns: minmax(0, 1fr); }} .s3, .s2 {{ grid-column: auto; }}
  .icons, .donts {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  .sws {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  .rules3, .cover-band, .hmi-body {{ grid-template-columns: minmax(0, 1fr); }}
  .list li {{ grid-template-columns: minmax(0, 1fr); gap: 4px; }}
}}
</style>

<div class="wrap">
  <header class="cover">
    <div class="cover-top"><span class="k">SAFI · Brand guidelines</span><span class="k">Version 1.0 · 2026</span></div>
    <div class="cover-logo">{svg("safi-logo-primary.svg")}</div>
    <div class="cover-band">
      <div><span class="k">Product</span><span>Operational co-pilot for oil and gas control rooms</span></div>
      <div><span class="k">Symbol</span><span>The SAFI flame: three flat layers, two tongues</span></div>
      <div><span class="k">Colours</span><span>SAFI Navy with Flame Red, Orange and Yellow</span></div>
    </div>
  </header>

  <section>
    <div class="head"><span class="k">01 · Symbol</span><div><h2>A real gas flame, drawn in three flat layers</h2><p class="muted">The symbol is a burning gas flame: a tall main tongue and a shorter second tongue, as a real flame moves. Depth comes from three solid layers, never from gradients, so it prints, embroiders and engraves cleanly.</p></div></div>
    <div class="two">
      <div class="anat">
        <figure><svg viewBox="20 2 120 232"><path fill="{C["red"]}" d="{OUTER}"/></svg><figcaption class="k">Outer flame</figcaption></figure>
        <figure><svg viewBox="20 2 120 232"><path fill="{C["orange"]}" d="{BODY}"/></svg><figcaption class="k">Body</figcaption></figure>
        <figure><svg viewBox="20 2 120 232"><path fill="{C["yellow"]}" d="{CORE}"/></svg><figcaption class="k">Core</figcaption></figure>
        <figure class="all">{svg("safi-symbol.svg")}<figcaption class="k">Symbol</figcaption></figure>
      </div>
      <ul class="list">
        <li><b>Flame</b><p>Oil, gas and the energy of the plant, shown plainly. Engineers, operators and executives recognise it immediately.</p></li>
        <li><b>Layers</b><p>Each layer sits inside the one behind it, the way a real flame burns hotter towards its core. They also stand for SAFI's job: removing noise layer by layer until only what matters remains.</p></li>
        <li><b>Stable base</b><p>The base is broad and settled, and the flame rises straight up. It is controlled, not wild: a process running inside its limits.</p></li>
        <li><b>One colour</b><p>In a single colour, the core is cut out of the outer flame. The symbol stays a flame in black, white or navy.</p></li>
      </ul>
    </div>
  </section>

  <section>
    <div class="head"><span class="k">02 · Logo</span><div><h2>Versions</h2><p class="muted">The wordmark is Archivo SemiExpanded, converted to outlines and letterspaced for SAFI. Cap height is 0.42 × flame height. Always use the supplied files and never retype it.</p></div></div>
    <div class="grid6">
      <div class="tile s3"><div class="art"><div class="lk">{svg("safi-logo-primary.svg")}</div></div><div class="cap"><span>Primary</span><span>safi-logo-primary.svg</span></div></div>
      <div class="tile navy s3"><div class="art"><div class="lk">{svg("safi-logo-primary-dark.svg")}</div></div><div class="cap"><span>Primary, reversed</span><span>safi-logo-primary-dark.svg</span></div></div>
      <div class="tile s2"><div class="art"><div class="st">{svg("safi-logo-stacked.svg")}</div></div><div class="cap"><span>Stacked</span><span>safi-logo-stacked.svg</span></div></div>
      <div class="tile s2"><div class="art"><div class="sy">{svg("safi-symbol.svg")}</div></div><div class="cap"><span>Symbol</span><span>safi-symbol.svg</span></div></div>
      <div class="tile navy s2"><div class="art"><div class="sy">{svg("safi-symbol.svg")}</div></div><div class="cap"><span>Symbol on navy</span><span>safi-symbol.svg</span></div></div>
      <div class="tile s2"><div class="art"><div class="lk">{svg("safi-logo-mono-black.svg")}</div></div><div class="cap"><span>One colour, black</span><span>safi-logo-mono-black.svg</span></div></div>
      <div class="tile black s2"><div class="art"><div class="lk">{svg("safi-logo-mono-white.svg")}</div></div><div class="cap"><span>One colour, white</span><span>safi-logo-mono-white.svg</span></div></div>
      <div class="tile s2"><div class="art"><div class="lk">{svg("safi-logo-mono-navy.svg")}</div></div><div class="cap"><span>One colour, navy</span><span>safi-logo-mono-navy.svg</span></div></div>
    </div>
  </section>

  <section>
    <div class="head"><span class="k">03 · Icon</span><div><h2>App icon and small sizes</h2><p class="muted">The flame sits on a SAFI Navy tile. It is solid enough to need no special small-size version. Sizes below are shown at actual size.</p></div></div>
    <div class="icons">
      <figure>{svg("safi-app-icon.svg")}<figcaption>safi-app-icon.svg</figcaption></figure>
      <figure>{svg("safi-app-icon-light.svg").replace('<rect', '<rect stroke="#D5DBE0" stroke-width="4"', 1)}<figcaption>safi-app-icon-light.svg</figcaption></figure>
      <figure>{svg("safi-app-icon-ios.svg")}<figcaption>safi-app-icon-ios.svg · iOS masks the corners</figcaption></figure>
      <figure>{svg("safi-app-icon-maskable.svg")}<figcaption>safi-app-icon-maskable.svg · Android / PWA</figcaption></figure>
    </div>
    <div class="ramp">{ramp}</div>
  </section>

  <section>
    <div class="head"><span class="k">04 · Colour</span><div><h2>Navy for the company. Three flame colours for the symbol.</h2><p class="muted">Solid colours only. Navy and white do most of the work. Red and yellow appear only inside the symbol. Flame Orange is the one accent colour for layouts.</p></div></div>
    <div class="sws">{sw}</div>
    <div><p class="k" style="margin-bottom:8px">Proportion in a typical layout</p><div class="ratio"><span style="flex:55;background:var(--white);outline:1px solid var(--rule)"></span><span style="flex:30;background:var(--navy)"></span><span style="flex:10;background:var(--mist)"></span><span style="flex:3;background:var(--steel)"></span><span style="flex:2;background:var(--flare)"></span><span style="flex:1;background:var(--red)"></span><span style="flex:1;background:var(--yellow)"></span></div></div>
    <p class="note">Inside operator displays (ISA-101), orange is commonly an alarm colour. On control-room screens, the flame colours appear only in the logo. Interface states use their own alarm palette, never the brand colours.</p>
  </section>

  <section>
    <div class="head"><span class="k">05 · Typography</span><div><h2>Archivo, the typeface behind the wordmark</h2><p class="muted">Archivo is a grotesk with a width axis, built for both print and screens. It is open source (SIL OFL), so it can be used in software, documents and print without licensing friction. Use the wider cuts for headlines and the narrower ones for data.</p></div></div>
    <div class="type">
      <div class="spec"><span class="k">Archivo · Headlines and text</span><span class="big">Stable operations</span><p>Fewer alarms, clearer priorities. SAFI works inside the limits your operators set and filters out the noise around them.</p><span class="mono muted">Semibold 600 headlines · Regular 400 text</span></div>
      <div class="spec"><span class="k">Archivo Semi Condensed · Data and labels</span><span class="vals cond">FIC-3104 · 214.6 m³/h</span><span class="vals cond">TI-2207 · 356.2 °C</span><span class="vals cond">PIC-1102 · 18.4 barg</span><span class="mono muted">Medium 500 with tabular figures for process values</span></div>
    </div>
  </section>

  <section>
    <div class="head"><span class="k">06 · Usage</span><div><h2>Clear space, size and misuse</h2></div></div>
    <div class="rules3">
      <div class="rule"><h3>Clear space</h3><div class="cs"><div class="cs-box">{svg("safi-logo-primary.svg")}</div></div><p class="muted">Half the flame width on every side.</p></div>
      <div class="rule"><h3>Minimum size</h3><p class="mono">Lockup ≥ 96px / 25mm wide<br>Symbol ≥ 16px / 5mm tall</p><p class="muted">Below 96px wide, use the symbol on its own.</p></div>
      <div class="rule"><h3>Backgrounds</h3><p class="muted">Primary on white or Mist. Reversed on Navy. On photographs or any other colour, use one-colour white or black.</p></div>
    </div>
    <div class="donts">
      <figure><div class="x"><div style="transform:scaleX(1.5);width:30%">{svg("safi-symbol.svg")}</div></div><figcaption>Don't stretch or squeeze.</figcaption></figure>
      <figure><div class="x"><div style="width:30%">{svg("safi-symbol.svg").replace("#D63A1A", "#1B67B1").replace("#EE7420", "#3E8ED8").replace("#F8B320", "#9CC9F2")}</div></div><figcaption>Don't recolour the flame.</figcaption></figure>
      <figure><div class="x"><div style="width:30%;filter:drop-shadow(0 8px 6px rgba(0,0,0,.45))">{svg("safi-symbol.svg")}</div></div><figcaption>Don't add shadows, glows or gradients.</figcaption></figure>
      <figure><div class="x" style="background:var(--flare)"><div style="width:30%">{svg("safi-symbol.svg")}</div></div><figcaption>Don't place the colour symbol on orange or busy grounds.</figcaption></figure>
    </div>
  </section>

  <section>
    <div class="head"><span class="k">07 · Applications</span><div><h2>In use</h2><p class="muted">Example layouts with sample content.</p></div></div>
    <div class="apps">
      <div class="app">
        <div class="cards">
          <div class="card"><div class="lg">{svg("safi-logo-primary.svg")}</div><div class="who"><b>Operations Engineer</b><br>Control Room Systems</div><div class="ct"><span>+00 000 000 000</span><span>name@company.com</span></div></div>
          <div class="card back">{svg("safi-symbol.svg")}</div>
        </div>
        <span class="k cap">Business card, 85 × 55 mm</span>
      </div>
      <div class="app">
        <div class="letter"><div class="top"><div class="lg">{svg("safi-logo-primary.svg")}</div><div class="addr">Operations Support<br>Control Room Systems</div></div><h4>Alarm rationalisation summary · Unit 3</h4><div class="ln"><i></i><i></i><i style="width:82%"></i><i></i><i style="width:64%"></i></div></div>
        <span class="k cap">Document header, A4</span>
      </div>
      <div class="app" style="grid-column:1 / -1">
        <div class="hmi">
          <div class="hmi-bar"><div class="lg">{svg("safi-logo-primary-dark.svg")}</div><nav><b>CDU-3 · Atmospheric column</b><span>Overview</span><span>Alarms</span><span>Limits</span></nav><span class="st">WITHIN LIMITS</span></div>
          <div class="hmi-body"><div><span>Alarms presented / raw, last hour</span><b>6 / 148</b></div><div><span>Chattering alarms filtered</span><b>42</b></div><div><span>Tags inside operator limits</span><b>99.2 %</b></div></div>
        </div>
        <span class="k cap">Control-room application header. Flame colours appear only in the logo.</span>
      </div>
    </div>
  </section>

  <section>
    <div class="head"><span class="k">08 · Files</span><div><h2>/public/branding/</h2></div></div>
    <div class="files"><table><thead><tr><th>File</th><th>Use</th></tr></thead><tbody>
      <tr><td>safi-logo-primary.svg</td><td>Primary logo, light grounds</td></tr>
      <tr><td>safi-logo-primary-dark.svg</td><td>Primary logo, navy and dark grounds</td></tr>
      <tr><td>safi-logo-stacked(-dark).svg</td><td>Square and centred formats</td></tr>
      <tr><td>safi-logo-mono-black / white / navy.svg</td><td>One-colour reproduction</td></tr>
      <tr><td>safi-symbol.svg, safi-symbol-mono-*.svg</td><td>Symbol alone</td></tr>
      <tr><td>safi-wordmark(-white / -black).svg</td><td>Wordmark alone</td></tr>
      <tr><td>safi-app-icon(-light / -ios / -maskable).svg</td><td>App icons, 1024 grid</td></tr>
      <tr><td>safi-favicon.svg, png/</td><td>Favicon and raster exports</td></tr>
      <tr><td>safi-colors.css, safi-tokens.json</td><td>Colour and type tokens</td></tr>
    </tbody></table></div>
  </section>
</div>'''
    if standalone:
        return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                '<link rel="icon" href="safi-favicon.svg" type="image/svg+xml">\n'
                + body.replace("</style>", "</style>\n</head>\n<body>", 1) + "\n</body>\n</html>\n")
    return body

open(os.path.join(D, "brand-guide.html"), "w").write(page(True))
if len(sys.argv) > 1: open(sys.argv[1], "w").write(page(False))
print("ok")
