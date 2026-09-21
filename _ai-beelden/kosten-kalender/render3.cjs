// node render2.cjs <scene.html> <naam> [naam ...] -> uit/<naam>.png (1000 x 1000, transparant) + uit/blad-<scene>.png
const http = require('http'), fs = require('fs'), path = require('path');
const HIER = __dirname, SITE = 'C:/Users/tugce/Documents/GitHub/de-reus/dereus', POORT = 8972;
const { chromium } = require('C:/Users/tugce/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
const sharp = require(SITE + '/_ai-beelden/node_modules/sharp');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.png': 'image/png', '.woff2': 'font/woff2' };
const [sceneBestand, ...namen] = process.argv.slice(2);
fs.mkdirSync(`${HIER}/uit`, { recursive: true });
const srv = http.createServer((q, r) => { const p = decodeURIComponent(q.url.split('?')[0]); const f = p.startsWith('/site/') ? path.join(SITE, p.slice(6)) : path.join(HIER, p);
  fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' }); r.end(d); }); }).listen(POORT, async () => {
  const b = await chromium.launch({ channel: 'chrome', args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await b.newPage({ viewport: { width: 1200, height: 1200 } });
  pg.on('pageerror', e => console.log('[fout]', e.message));
  await pg.goto(`http://127.0.0.1:${POORT}/${sceneBestand}`); await pg.waitForFunction('window.klaar === true', null, { timeout: 30000 });
  for (const n of namen) { const url = await pg.evaluate(x => window.maak(x), n); fs.writeFileSync(`${HIER}/uit/${n}.png`, Buffer.from(url.split(',')[1], 'base64')); console.log('gerenderd', n); }
  await b.close(); srv.close();
  const delen = await Promise.all(namen.map(async (x, i) => ({ input: await sharp(`${HIER}/uit/${x}.png`).resize(500, 500).toBuffer(), left: i * 500, top: 0 })));
  await sharp({ create: { width: 500 * namen.length, height: 500, channels: 4, background: '#FFFFFF' } }).composite(delen).png().toFile(`${HIER}/uit/blad-${path.basename(sceneBestand, '.html')}.png`);
});
