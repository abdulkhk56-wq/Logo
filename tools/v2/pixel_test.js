// Honest small-size test: rasterise each concept at true pixel sizes (DPR 1).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const dir = path.join(__dirname, '..', '..', 'public', 'branding', 'concepts');
const sizes = [16, 24, 32, 48];
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 1 });
  for (const k of ['01-tandem', '02-laminar', '03-gate']) {
    fs.mkdirSync(path.join(dir, k, 'pixel-test'), { recursive: true });
    for (const [src, bg] of [['symbol-black.svg', '#fff'], ['app-icon.svg', 'transparent']]) {
      const svg = fs.readFileSync(path.join(dir, k, src), 'utf8');
      for (const s of sizes) {
        await p.setViewportSize({ width: s, height: s });
        await p.setContent(`<style>html,body{margin:0;background:${bg}}img{width:${s}px;height:${s}px;object-fit:contain;display:block}</style><img src="data:image/svg+xml;base64,${Buffer.from(svg).toString('base64')}">`);
        await p.screenshot({ path: path.join(dir, k, 'pixel-test', `${src.replace('.svg', '')}-${s}.png`), omitBackground: bg === 'transparent' });
      }
    }
  }
  await b.close(); console.log('ok');
})();
