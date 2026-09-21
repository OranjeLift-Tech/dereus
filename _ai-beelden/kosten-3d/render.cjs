// node render.cjs [naam ...] -> uit/<naam>.png (1000 x 1000, transparant) + controleblad uit/blad.png
// Daarna: node export.cjs [naam ...] -> img/kosten-3d/<naam>.webp. three staat in _ai-beelden/node_modules.
const http = require('http'), fs = require('fs'), path = require('path');
const HIER = __dirname, SITE = 'C:/Users/tugce/Documents/GitHub/de-reus/dereus', POORT = 8973;
const { chromium } = require('C:/Users/tugce/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
const sharp = require(SITE + '/_ai-beelden/node_modules/sharp');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.png': 'image/png' };
const namen = process.argv.length > 2 ? process.argv.slice(2) : ['dozen', 'wagen', 'trap', 'gereedschap', 'opslag'];
fs.mkdirSync(`${HIER}/uit`, { recursive: true });
const srv = http.createServer((q, r) => { const p = decodeURIComponent(q.url.split('?')[0]);
  const f = p.startsWith('/site/') ? path.join(SITE, p.slice(6)) : p.startsWith('/node_modules/') ? path.join(SITE, '_ai-beelden', p) : path.join(HIER, p);
  fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' }); r.end(d); }); }).listen(POORT, async () => {
  const b = await chromium.launch({ channel: 'chrome', args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await b.newPage({ viewport: { width: 1000, height: 1000 } });
  pg.on('pageerror', e => console.log('[fout]', e.message));
  await pg.goto(`http://127.0.0.1:${POORT}/scene.html`); await pg.waitForFunction('window.klaar === true', null, { timeout: 30000 });
  for (const n of namen) { const url = await pg.evaluate(x => window.maak(x), n); fs.writeFileSync(`${HIER}/uit/${n}.png`, Buffer.from(url.split(',')[1], 'base64')); console.log('gerenderd', n); }
  await b.close(); srv.close();
  const delen = await Promise.all(namen.map(async (x, i) => ({ input: await sharp(`${HIER}/uit/${x}.png`).resize(400, 400).toBuffer(), left: i * 400, top: 0 })));
  await sharp({ create: { width: 400 * namen.length, height: 400, channels: 4, background: '#F6F7F9' } }).composite(delen).png().toFile(`${HIER}/uit/blad.png`);
});
