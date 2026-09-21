// node render.cjs [naam ...] -> uit/<naam>.png + ../../img/kaart-3d/<naam>.webp + uit/vlakken.json
// Het beeld wordt NIET bijgesneden: het tekstvlak in vlakken.json is in procenten van het hele beeld.
const http = require('http'), fs = require('fs'), path = require('path');
const HIER = __dirname, SITE = 'C:/Users/tugce/Documents/GitHub/de-reus/dereus', POORT = 8977;
const { chromium } = require('C:/Users/tugce/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
const sharp = require(SITE + '/_ai-beelden/node_modules/sharp');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.png': 'image/png' };
const namen = process.argv.length > 2 ? process.argv.slice(2) : ['telefoon', 'klembord', 'doos'];
fs.mkdirSync(`${HIER}/uit`, { recursive: true }); fs.mkdirSync(`${SITE}/img/kaart-3d`, { recursive: true });
const srv = http.createServer((q, r) => { const p = decodeURIComponent(q.url.split('?')[0]);
  const f = p.startsWith('/site/') ? path.join(SITE, p.slice(6)) : p.startsWith('/node_modules/') ? path.join(SITE, '_ai-beelden', p) : path.join(HIER, p);
  fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' }); r.end(d); }); }).listen(POORT, async () => {
  const b = await chromium.launch({ channel: 'chrome', args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await b.newPage({ viewport: { width: 1500, height: 1600 } });
  pg.on('pageerror', e => console.log('[fout]', e.message));
  await pg.goto(`http://127.0.0.1:${POORT}/scene.html`); await pg.waitForFunction('window.klaar === true', null, { timeout: 30000 });
  const vlakken = fs.existsSync(`${HIER}/uit/vlakken.json`) ? JSON.parse(fs.readFileSync(`${HIER}/uit/vlakken.json`, 'utf8')) : {};
  for (const n of namen) {
    const uit = await pg.evaluate(x => window.maak(x), n);
    fs.writeFileSync(`${HIER}/uit/${n}.png`, Buffer.from(uit.png.split(',')[1], 'base64'));
    const info = await sharp(`${HIER}/uit/${n}.png`).resize({ width: Math.round(uit.maat[0] * .6) }).webp({ quality: 88, alphaQuality: 92, effort: 6 }).toFile(`${SITE}/img/kaart-3d/${n}.webp`);
    vlakken[n] = { ...uit.tekst, beeld: [info.width, info.height] };
    console.log('gerenderd', n, JSON.stringify(vlakken[n]), Math.round(info.size / 1024) + ' kB');
  }
  fs.writeFileSync(`${HIER}/uit/vlakken.json`, JSON.stringify(vlakken, null, 2));
  await b.close(); srv.close();
});
