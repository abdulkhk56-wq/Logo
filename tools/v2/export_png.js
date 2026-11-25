// PNG exports of the app icons / favicon (platform delivery only).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const dir = path.join(__dirname, '..', '..', 'public', 'branding');
const jobs = [
  ['safi-app-icon.svg', 'safi-app-icon-1024.png', 1024], ['safi-app-icon.svg', 'safi-app-icon-512.png', 512],
  ['safi-app-icon.svg', 'safi-app-icon-192.png', 192], ['safi-app-icon-ios.svg', 'apple-touch-icon-180.png', 180],
  ['safi-app-icon-maskable.svg', 'safi-app-icon-maskable-512.png', 512],
  ['safi-favicon.svg', 'favicon-32.png', 32], ['safi-favicon.svg', 'favicon-16.png', 16],
  ['safi-logo-primary.svg', 'safi-logo-primary-1600w.png', 1600, 'w'], ['safi-logo-primary-dark.svg', 'safi-logo-primary-dark-1600w.png', 1600, 'w'],
];
(async () => {
  fs.mkdirSync(path.join(dir, 'png'), { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage();
  for (const [src, out, size, mode] of jobs) {
    const svg = fs.readFileSync(path.join(dir, src), 'utf8');
    const vb = svg.match(/viewBox="([^"]+)"/)[1].split(' ').map(Number);
    const W = size, H = mode === 'w' ? Math.round(size * vb[3] / vb[2]) : size;
    await p.setViewportSize({ width: W, height: H });
    await p.setContent(`<style>html,body{margin:0;background:transparent}</style><img style="width:${W}px;height:${H}px;display:block" src="data:image/svg+xml;base64,${Buffer.from(svg).toString('base64')}">`);
    await p.screenshot({ path: path.join(dir, 'png', out), omitBackground: true });
  }
  await b.close(); console.log('png ok');
})();
