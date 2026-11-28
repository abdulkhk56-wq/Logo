"""SAFI brand guidelines -> public/branding/brand-guide.html (+ body-only copy for publishing)."""
import os, sys
D = os.path.join(os.path.dirname(__file__), "..", "public", "branding")

def svg(p):
    s = open(os.path.join(D, p)).read().strip()
    return s.replace('<svg xmlns="http://www.w3.org/2000/svg"', "<svg", 1)

SW = [("SAFI Navy", "#0B2A3C", "11 42 60", "Symbol tile, wordmarks, text.", "light"),
      ("Gold", "#C49A4A", "196 154 74", "Divider rule and one highlight per layout.", "light"),
      ("White", "#FFFFFF", "255 255 255", "Primary ground.", "dark"),
      ("Deep Navy", "#071C29", "7 28 41", "Dark interface ground.", "light"),
      ("Steel", "#5E6E7A", "94 110 122", "Secondary text, rules.", "light"),
      ("Mist", "#E9EDF0", "233 237 240", "Panels, table fills.", "dark")]

def tile(cls, file, cap, name, span):
    return f'<div class="tile {cls} {span}"><div class="art">{svg(file)}</div><div class="cap"><span>{cap}</span><span>{file}</span></div></div>'

def page(standalone):
    sw = "".join(f'<div class="sw" style="background:{h};color:{"#fff" if t=="light" else "#0B2A3C"}"><b>{n}</b><span class="mono">{h}<br>RGB {r}</span><span class="r">{d}</span></div>' for n, h, r, d, t in SW)
    ramp = "".join(f'<figure><div style="width:{s}px;height:{s}px">{svg("safi-favicon.svg" if s <= 32 else "safi-app-icon.svg")}</div><figcaption class="mono">{s}</figcaption></figure>' for s in (16, 24, 32, 48, 64, 96))
    fonts = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">'
    body = f'''<title>SAFI Brand Guidelines</title>
<meta name="claude:viewport-fit-sides" content="cover">
{fonts}
<style>
/* Layout: a bilingual corporate standards manual. White sheets, navy ink,
   gold used only as rules, as the identity uses it. */
:root {{ --navy: #0B2A3C; --gold: #C49A4A; --white: #FFFFFF; --deep: #071C29; --steel: #5E6E7A; --mist: #E9EDF0; --rule: #D6DCE1;
  --sans: "Readex Pro", "Segoe UI", Tahoma, sans-serif; --mono: "IBM Plex Mono", ui-monospace, Menlo, monospace; color-scheme: light; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--white); color: var(--navy); font-family: var(--sans); font-size: 16px; line-height: 1.6; font-weight: 300; }}
.wrap {{ max-width: 1180px; margin: 0 auto; padding-block: 0 72px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }}
h2, h3 {{ margin: 0; font-weight: 500; line-height: 1.15; text-wrap: balance; }}
h2 {{ font-size: clamp(1.6rem, 3.2vw, 2.4rem); }}
h3 {{ font-size: 1.1rem; }}
p {{ margin: 0; max-width: 64ch; }}
b {{ font-weight: 500; }}
svg {{ display: block; max-width: 100%; height: auto; }}
.mono {{ font-family: var(--mono); font-size: .76rem; }}
.k {{ font-weight: 500; font-size: .74rem; letter-spacing: .14em; text-transform: uppercase; color: var(--steel); }}
.muted {{ color: var(--steel); }}
.ar {{ font-family: var(--sans); }}
section {{ padding-block: 72px; border-top: 1px solid var(--rule); display: grid; gap: 36px; }}
.head {{ display: grid; grid-template-columns: 220px minmax(0, 1fr); gap: 24px; align-items: baseline; }}
.head > div {{ display: grid; gap: 12px; }}
.cover {{ padding-block: 40px 0; }}
.cover-top {{ display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap; padding-bottom: 18px; border-bottom: 2px solid var(--navy); }}
.cover-logo {{ padding-block: clamp(64px, 12vw, 150px); display: grid; place-items: center; }}
.cover-logo svg {{ width: min(680px, 94%); }}
.band {{ background: var(--navy); color: var(--white); display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; padding: 28px; }}
.band div {{ display: grid; gap: 4px; min-width: 0; }}
.band .k {{ color: #9DB0BF; }}
.idea {{ display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: 48px; align-items: center; }}
.word {{ display: grid; gap: 18px; justify-items: center; padding: 48px 24px; background: var(--mist); text-align: center; }}
.word .big {{ font-size: clamp(4rem, 10vw, 7rem); font-weight: 600; line-height: 1.45; }}
.word .gloss {{ display: flex; gap: 14px; flex-wrap: wrap; justify-content: center; font-size: .95rem; }}
.word .gloss span {{ border-top: 2px solid var(--gold); padding-top: 6px; }}
.list {{ margin: 0; padding: 0; list-style: none; display: grid; gap: 18px; }}
.list li {{ display: grid; grid-template-columns: 120px minmax(0, 1fr); gap: 16px; border-top: 1px solid var(--rule); padding-top: 14px; }}
.list b {{ text-transform: uppercase; letter-spacing: .1em; font-size: .78rem; }}
.grid6 {{ display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 16px; }}
.tile {{ display: grid; grid-template-rows: 1fr auto; gap: 18px; padding: clamp(24px, 4vw, 44px); min-width: 0; border: 1px solid var(--rule); }}
.tile.navy {{ background: var(--navy); border-color: var(--navy); color: var(--white); }}
.tile.black {{ background: #000; border-color: #000; color: #fff; }}
.tile .art {{ display: grid; place-items: center; min-height: 120px; }}
.tile .art svg {{ max-height: 120px; width: auto; max-width: 100%; }}
.s6 {{ grid-column: span 6; }} .s3 {{ grid-column: span 3; }} .s2 {{ grid-column: span 2; }}
.s6 .art svg {{ max-height: 96px; }}
.tile .cap {{ display: flex; justify-content: space-between; gap: 10px; flex-wrap: wrap; font-family: var(--mono); font-size: .72rem; opacity: .75; }}
.icons {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; }}
.icons figure {{ margin: 0; display: grid; gap: 10px; }}
.icons figcaption {{ font-family: var(--mono); font-size: .72rem; color: var(--steel); }}
.ramp {{ display: flex; gap: 28px; align-items: end; flex-wrap: wrap; padding: 28px; background: var(--mist); }}
.ramp figure {{ margin: 0; display: grid; gap: 8px; justify-items: center; }}
.ramp div svg {{ width: 100%; height: 100%; }}
.sws {{ display: grid; grid-template-columns: 2.2fr 1.2fr 1.2fr 1fr 1fr 1fr; border: 1px solid var(--rule); }}
.sw {{ min-height: 220px; padding: 18px; display: grid; align-content: space-between; gap: 12px; min-width: 0; }}
.sw b {{ font-size: 1.02rem; }}
.sw .r {{ font-size: .85rem; line-height: 1.35; }}
.ratio {{ display: flex; height: 18px; }}
.note {{ border-left: 3px solid var(--gold); padding: 4px 0 4px 18px; }}
.type {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 16px; }}
.spec {{ border: 1px solid var(--rule); padding: 28px; display: grid; gap: 14px; align-content: start; min-width: 0; }}
.spec .h {{ font-size: clamp(2rem, 4.4vw, 3rem); font-weight: 500; line-height: 1.15; }}
.vals {{ font-weight: 400; font-size: 1.35rem; font-variant-numeric: tabular-nums; }}
.rules3 {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }}
.rule {{ border: 1px solid var(--rule); padding: 24px; display: grid; gap: 14px; align-content: start; min-width: 0; }}
.cs {{ padding: 22px; background: var(--mist); }} .cs-box {{ outline: 1px dashed var(--gold); padding: 7%; background: var(--white); }}
.donts {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; }}
.donts figure {{ margin: 0; display: grid; gap: 10px; }}
.x {{ border: 1px solid var(--rule); aspect-ratio: 4/3; display: grid; place-items: center; overflow: hidden; position: relative; }}
.x > div {{ width: 34%; }}
.x::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(to top right, transparent calc(50% - 1px), #B3261E calc(50% - 1px), #B3261E calc(50% + 1px), transparent calc(50% + 1px)); }}
.donts figcaption {{ font-size: .88rem; color: var(--steel); }}
.apps {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 16px; }}
.app {{ background: var(--mist); padding: clamp(20px, 4vw, 44px); display: grid; gap: 18px; place-items: center; min-width: 0; }}
.app .cap {{ justify-self: start; }}
.cards {{ display: flex; gap: 16px; flex-wrap: wrap; justify-content: center; width: 100%; }}
.card {{ width: min(100%, 320px); aspect-ratio: 85 / 55; background: var(--white); padding: 7% 8%; display: grid; grid-template-rows: auto 1fr auto; box-shadow: 0 1px 2px rgba(7,28,41,.18); }}
.card .lg svg {{ width: 74%; }}
.card .who {{ align-self: end; font-size: .76rem; line-height: 1.4; }}
.card .who b {{ font-size: .86rem; }}
.card .ct {{ font-size: .64rem; color: var(--steel); display: flex; justify-content: space-between; gap: 8px; border-top: 1px solid var(--gold); padding-top: 6px; margin-top: 8px; }}
.card.back {{ background: var(--navy); place-items: center; grid-template-rows: 1fr; }}
.card.back svg {{ width: 22%; }}
.card.ar {{ direction: rtl; }}
.letter {{ width: min(100%, 420px); aspect-ratio: 210 / 150; background: var(--white); box-shadow: 0 1px 2px rgba(7,28,41,.18); padding: 6% 7%; display: grid; grid-template-rows: auto auto 1fr; gap: 9%; }}
.letter .lg svg {{ width: 58%; }}
.letter h4 {{ margin: 0; font-size: .8rem; font-weight: 500; border-top: 1px solid var(--gold); padding-top: 10px; }}
.letter .ln {{ display: grid; gap: 7px; }}
.letter .ln i {{ display: block; height: 4px; background: var(--mist); }}
.hmi {{ width: 100%; background: var(--deep); color: #DCE3E8; }}
.hmi-bar {{ display: flex; align-items: center; gap: 18px; padding: 10px 16px; border-bottom: 1px solid #1C3546; flex-wrap: wrap; }}
.hmi-bar .lg svg {{ width: 150px; }}
.hmi-bar nav {{ display: flex; gap: 16px; font-size: .84rem; color: #8FA2B1; flex-wrap: wrap; }}
.hmi-bar nav b {{ color: #fff; }}
.hmi-bar .st {{ margin-left: auto; font-size: .72rem; letter-spacing: .08em; border: 1px solid #3C5466; padding: 3px 8px; }}
.hmi-body {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1px; background: #1C3546; }}
.hmi-body div {{ background: var(--deep); padding: 14px 16px; display: grid; gap: 2px; min-width: 0; }}
.hmi-body span {{ font-size: .74rem; color: #8FA2B1; }}
.hmi-body b {{ font-size: 1.3rem; font-weight: 400; color: #fff; font-variant-numeric: tabular-nums; }}
.files {{ overflow-x: auto; }}
table {{ width: 100%; min-width: 560px; border-collapse: collapse; font-size: .9rem; }}
th, td {{ text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--rule); vertical-align: top; }}
th {{ font-weight: 500; letter-spacing: .12em; text-transform: uppercase; font-size: .72rem; color: var(--steel); }}
td:first-child {{ font-family: var(--mono); font-size: .78rem; white-space: nowrap; }}
@media (max-width: 900px) {{
  .head, .idea, .type, .apps {{ grid-template-columns: minmax(0, 1fr); }}
  .grid6 {{ grid-template-columns: minmax(0, 1fr); }} .s6, .s3, .s2 {{ grid-column: auto; }}
  .icons, .donts {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  .sws {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  .rules3, .band, .hmi-body {{ grid-template-columns: minmax(0, 1fr); }}
  .list li {{ grid-template-columns: minmax(0, 1fr); gap: 4px; }}
}}
</style>

<div class="wrap">
  <header class="cover">
    <div class="cover-top"><span class="k">SAFI · Brand guidelines</span><span class="k">Version 1.0</span></div>
    <div class="cover-logo">{svg("safi-logo-primary.svg")}</div>
    <div class="band">
      <div><span class="k">Product</span><span>Operational co-pilot for oil and gas control rooms</span></div>
      <div><span class="k">Name</span><span><span class="ar" lang="ar">صافي</span> means pure, clear, filtered</span></div>
      <div><span class="k">Colours</span><span>SAFI Navy and Gold</span></div>
    </div>
  </header>

  <section>
    <div class="head"><span class="k">01 · Idea</span><div><h2>The name already says what the product does</h2><p class="muted">In Arabic, <span class="ar" lang="ar">صافي</span> means pure, clear: what remains after filtering. SAFI takes a flood of alarms and process noise and leaves the operator with a clear picture. The identity is built on the name itself, not on a picture.</p></div></div>
    <div class="idea">
      <div class="word"><span class="big ar" lang="ar">صافي</span><div class="gloss"><span>pure</span><span>clear</span><span>filtered</span><span>net</span></div></div>
      <ul class="list">
        <li><b>Symbol</b><p>The letter <span class="ar" lang="ar">ص</span> (Sad), the first letter of the name, reversed out of a navy tile. A single letter, recognisable in both the Arab world and abroad, and robust at any size.</p></li>
        <li><b>Two scripts</b><p>The name always appears in Arabic and English, set from one type family so both scripts share stroke weight and rhythm. That is how established regional energy companies present themselves.</p></li>
        <li><b>Gold rule</b><p>A thin gold line separates the scripts: a precise, measured detail, like a scale mark on an instrument.</p></li>
        <li><b>No pictures</b><p>No flames, drops or circuits. The mark relies on letterforms and proportion, so it doesn't date and can't be mistaken for an icon.</p></li>
      </ul>
    </div>
  </section>

  <section>
    <div class="head"><span class="k">02 · Logo</span><div><h2>Versions</h2><p class="muted">The bilingual logo is the default. Use the single-script versions where only one language is used. Latin cap height is 0.40 × tile height, and both scripts share one baseline.</p></div></div>
    <div class="grid6">
      {tile("", "safi-logo-primary.svg", "Primary, bilingual", "", "s3")}
      {tile("navy", "safi-logo-primary-dark.svg", "Primary, reversed", "", "s3")}
      {tile("", "safi-logo-latin.svg", "Latin", "", "s2")}
      {tile("", "safi-logo-arabic.svg", "Arabic", "", "s2")}
      {tile("", "safi-logo-stacked.svg", "Stacked", "", "s2")}
      {tile("", "safi-symbol.svg", "Symbol", "", "s2")}
      {tile("navy", "safi-symbol-dark.svg", "Symbol, reversed", "", "s2")}
      {tile("navy", "safi-symbol-gold.svg", "Symbol, gold (special use)", "", "s2")}
      {tile("", "safi-logo-mono-black.svg", "One colour, black", "", "s3")}
      {tile("black", "safi-logo-mono-white.svg", "One colour, white", "", "s3")}
    </div>
  </section>

  <section>
    <div class="head"><span class="k">03 · Icon</span><div><h2>App icon and small sizes</h2><p class="muted">The symbol is already an icon: one letter in one tile. The sizes below are shown at actual size.</p></div></div>
    <div class="icons">
      <figure>{svg("safi-app-icon.svg")}<figcaption>safi-app-icon.svg</figcaption></figure>
      <figure>{svg("safi-symbol-dark.svg").replace("<rect", '<rect stroke="#D6DCE1" stroke-width="1"', 1)}<figcaption>safi-symbol-dark.svg</figcaption></figure>
      <figure>{svg("safi-app-icon-ios.svg")}<figcaption>safi-app-icon-ios.svg · iOS masks the corners</figcaption></figure>
      <figure>{svg("safi-app-icon-maskable.svg")}<figcaption>safi-app-icon-maskable.svg · Android / PWA</figcaption></figure>
    </div>
    <div class="ramp">{ramp}</div>
  </section>

  <section>
    <div class="head"><span class="k">04 · Colour</span><div><h2>Navy carries the brand. Gold marks the detail.</h2><p class="muted">Solid colours only. Navy and white do almost all the work. Gold appears only as thin rules and small highlights, never as a large fill or as text.</p></div></div>
    <div class="sws">{sw}</div>
    <div><p class="k" style="margin-bottom:8px">Proportion in a typical layout</p><div class="ratio"><span style="flex:55;background:var(--white);outline:1px solid var(--rule)"></span><span style="flex:32;background:var(--navy)"></span><span style="flex:8;background:var(--mist)"></span><span style="flex:3;background:var(--steel)"></span><span style="flex:2;background:var(--gold)"></span></div></div>
    <p class="note">In operator displays (ISA-101), colour is reserved for abnormal conditions. Navy, white and grey suit a calm screen, and the brand never competes with alarm colours.</p>
  </section>

  <section>
    <div class="head"><span class="k">05 · Typography</span><div><h2>Readex Pro, one family for both scripts</h2><p class="muted">Readex Pro covers Arabic and Latin with matched weights. It is the family the logo is drawn from, and it is open source (SIL OFL) for software, documents and print.</p></div></div>
    <div class="type">
      <div class="spec"><span class="k">Latin</span><span class="h">Clear operations</span><p>Fewer alarms, clearer priorities. SAFI works inside the limits your operators set and filters out the noise around them.</p><span class="vals">FIC-3104 · 214.6 m³/h · TI-2207 · 356.2 °C</span><span class="mono muted">Medium 500 headlines · Light 300 text</span></div>
      <div class="spec" dir="rtl" lang="ar"><span class="k">العربية</span><span class="h">عمليات صافية</span><p>إنذارات أقل وأولويات أوضح. يعمل صافي ضمن الحدود التي يضعها المشغّلون ويصفّي الضجيج من حولهم.</p><span class="vals">٢١٤٫٦ م³/س · ٣٥٦٫٢ °م</span><span class="mono muted" dir="ltr">Medium 500 headlines · Light 300 text</span></div>
    </div>
  </section>

  <section>
    <div class="head"><span class="k">06 · Usage</span><div><h2>Clear space, size and misuse</h2></div></div>
    <div class="rules3">
      <div class="rule"><h3>Clear space</h3><div class="cs"><div class="cs-box">{svg("safi-logo-primary.svg")}</div></div><p class="muted">Half the tile width on every side.</p></div>
      <div class="rule"><h3>Minimum size</h3><p class="mono">Bilingual logo ≥ 140px / 35mm wide<br>Latin or Arabic logo ≥ 90px / 22mm<br>Symbol ≥ 16px / 5mm</p></div>
      <div class="rule"><h3>Backgrounds</h3><p class="muted">Primary on white or Mist. Reversed on Navy. On photographs or other colours, use the one-colour versions.</p></div>
    </div>
    <div class="donts">
      <figure><div class="x"><div style="transform:scaleX(1.5)">{svg("safi-symbol.svg")}</div></div><figcaption>Don't stretch or squeeze.</figcaption></figure>
      <figure><div class="x"><div>{svg("safi-symbol.svg").replace("#0B2A3C", "#2E7D32")}</div></div><figcaption>Don't recolour the tile.</figcaption></figure>
      <figure><div class="x"><div style="filter:drop-shadow(0 8px 6px rgba(0,0,0,.45))">{svg("safi-symbol.svg")}</div></div><figcaption>Don't add shadows, glows or gradients.</figcaption></figure>
      <figure><div class="x"><div style="transform:rotate(-12deg)">{svg("safi-symbol.svg")}</div></div><figcaption>Don't rotate the symbol.</figcaption></figure>
    </div>
  </section>

  <section>
    <div class="head"><span class="k">07 · Applications</span><div><h2>In use</h2><p class="muted">Example layouts with sample content.</p></div></div>
    <div class="apps">
      <div class="app">
        <div class="cards">
          <div class="card"><div class="lg">{svg("safi-logo-latin.svg")}</div><div class="who"><b>Operations Engineer</b><br>Control Room Systems</div><div class="ct"><span>+000 0000 0000</span><span>name@company.com</span></div></div>
          <div class="card ar" lang="ar"><div class="lg">{svg("safi-logo-arabic.svg")}</div><div class="who"><b>مهندس عمليات</b><br>أنظمة غرف التحكم</div><div class="ct"><span dir="ltr">+000 0000 0000</span><span>name@company.com</span></div></div>
        </div>
        <span class="k cap">Business card, 85 × 55 mm, English and Arabic sides</span>
      </div>
      <div class="app">
        <div class="letter"><div class="lg">{svg("safi-logo-primary.svg")}</div><h4>Alarm rationalisation summary · Unit 3</h4><div class="ln"><i></i><i></i><i style="width:82%"></i><i></i><i style="width:64%"></i></div></div>
        <span class="k cap">Document header, A4</span>
      </div>
      <div class="app" style="grid-column:1 / -1">
        <div class="hmi">
          <div class="hmi-bar"><div class="lg">{svg("safi-logo-latin-dark.svg")}</div><nav><b>CDU-3 · Atmospheric column</b><span>Overview</span><span>Alarms</span><span>Limits</span></nav><span class="st">WITHIN LIMITS</span></div>
          <div class="hmi-body"><div><span>Alarms presented / raw, last hour</span><b>6 / 148</b></div><div><span>Chattering alarms filtered</span><b>42</b></div><div><span>Tags inside operator limits</span><b>99.2 %</b></div></div>
        </div>
        <span class="k cap">Control-room application header</span>
      </div>
    </div>
  </section>

  <section>
    <div class="head"><span class="k">08 · Files</span><div><h2>/public/branding/</h2></div></div>
    <div class="files"><table><thead><tr><th>File</th><th>Use</th></tr></thead><tbody>
      <tr><td>safi-logo-primary(-dark).svg</td><td>Bilingual logo, light / navy grounds</td></tr>
      <tr><td>safi-logo-latin(-dark).svg</td><td>English-only logo</td></tr>
      <tr><td>safi-logo-arabic(-dark).svg</td><td>Arabic-only logo</td></tr>
      <tr><td>safi-logo-stacked(-dark).svg</td><td>Centred and square formats</td></tr>
      <tr><td>safi-logo-mono-black / white.svg</td><td>One-colour logo</td></tr>
      <tr><td>safi-symbol(-dark / -gold / -mono-*).svg</td><td>Symbol tile</td></tr>
      <tr><td>safi-symbol-letter.svg</td><td>The letter alone, for embossing and patterns</td></tr>
      <tr><td>safi-wordmark(-arabic)(-white / -black).svg</td><td>Wordmarks alone</td></tr>
      <tr><td>safi-app-icon(-ios / -maskable).svg, safi-favicon.svg, png/</td><td>App icons, favicon, PNG exports</td></tr>
      <tr><td>safi-colors.css, safi-tokens.json, site.webmanifest</td><td>Tokens and manifest</td></tr>
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
