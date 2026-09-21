// node render.cjs [naam ...] -> r3d/uit/<naam>.png (1000x1000, transparant)
const http = require('http'), fs = require('fs'), path = require('path');
const HIER = __dirname, SITE = 'C:/Users/tugce/Documents/GitHub/de-reus/dereus', POORT = 8951;
const { chromium } = require('C:/Users/tugce/AppData/Local/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.png': 'image/png' };
const namen = process.argv.slice(2).length ? process.argv.slice(2) : ['telefoon', 'envelop', 'formulier', 'doos'];
fs.mkdirSync(`${HIER}/uit`, { recursive: true });
const srv = http.createServer((q, r) => { let p = decodeURIComponent(q.url.split('?')[0]); const f = p.startsWith('/site/') ? path.join(SITE, p.slice(6)) : path.join(HIER, p);
  fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' }); r.end(d); }); }).listen(POORT, async () => {
  const b = await chromium.launch({ channel: 'chrome', args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await b.newPage({ viewport: { width: 1000, height: 1000 } });
  pg.on('console', m => console.log('[pagina]', m.text())); pg.on('pageerror', e => console.log('[fout]', e.message));
  await pg.goto(`http://127.0.0.1:${POORT}/scene.html`); await pg.waitForFunction('window.klaar === true', null, { timeout: 30000 });
  for (const n of namen) { const url = await pg.evaluate(x => window.maak(x), n); fs.writeFileSync(`${HIER}/uit/${n}.png`, Buffer.from(url.split(',')[1], 'base64')); console.log('gerenderd', n); }
  await b.close(); srv.close(); });
