// Rasterise app icons / favicons from the master SVGs (platform delivery only).
// Usage: node tools/export-png.js   (uses the pre-installed Playwright Chromium)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const dir = path.join(__dirname, '..', 'public', 'branding');
const jobs = [
  ['safi-app-icon.svg', 'png/safi-app-icon-1024.png', 1024],
  ['safi-app-icon.svg', 'png/safi-app-icon-512.png', 512],
  ['safi-app-icon.svg', 'png/safi-app-icon-192.png', 192],
  ['safi-app-icon-ios.svg', 'png/apple-touch-icon-180.png', 180],
  ['safi-app-icon-maskable.svg', 'png/safi-app-icon-maskable-512.png', 512],
  ['safi-favicon.svg', 'png/favicon-32.png', 32],
  ['safi-favicon.svg', 'png/favicon-16.png', 16],
  ['safi-logo-primary.svg', 'png/safi-logo-primary-1200w.png', 1200, 'w'],
  ['safi-logo-primary-dark.svg', 'png/safi-logo-primary-dark-1200w.png', 1200, 'w'],
];
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  for (const [src, out, size, mode] of jobs) {
    const svg = fs.readFileSync(path.join(dir, src), 'utf8');
    const vb = svg.match(/viewBox="([^"]+)"/)[1].split(' ').map(Number);
    const w = size, h = mode === 'w' ? Math.round(size * vb[3] / vb[2]) : size;
    await p.setViewportSize({ width: w, height: h });
    await p.setContent(`<style>html,body{margin:0;background:transparent}</style><img style="width:${w}px;height:${h}px;display:block" src="data:image/svg+xml;base64,${Buffer.from(svg).toString('base64')}">`);
    await p.screenshot({ path: path.join(dir, out), omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
  }
  await b.close(); console.log('exported', jobs.length);
})();
