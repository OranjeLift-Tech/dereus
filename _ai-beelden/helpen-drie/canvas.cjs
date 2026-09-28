// Beeldwerk in headless Edge: node canvas.cjs <script.js> [uitmap]
// Het script draait in de pagina (http://127.0.0.1:8766, siteroot = repo) en krijgt helpers:
//   laad(pad) -> ImageBitmap, doek(w,h) -> [canvas, ctx], bewaar(naam, canvas, type?, q?)
const { chromium } = require(process.env.PLAYWRIGHT || 'playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [script, uit = __dirname] = process.argv.slice(2);
  const code = fs.readFileSync(script, 'utf8');
  const browser = await chromium.launch({ channel: 'msedge' });
  const page = await browser.newPage();
  await page.goto((process.env.BASIS || 'http://127.0.0.1:8767') + '/robots.txt');
  page.on('console', m => console.log('[pagina]', m.text()));
  const bestanden = await page.evaluate(async code => {
    const uit = [];
    const laad = async p => {
      const r = await fetch(p); if (!r.ok) throw new Error('niet gevonden ' + p);
      const buf = await r.arrayBuffer();
      const type = p.endsWith('.svg') ? 'image/svg+xml' : p.endsWith('.png') ? 'image/png' : p.endsWith('.jpg') ? 'image/jpeg' : 'image/webp';
      if (type === 'image/svg+xml') {
        const url = URL.createObjectURL(new Blob([buf], { type }));
        const im = new Image(); im.src = url; await im.decode(); return im;
      }
      return await createImageBitmap(new Blob([buf], { type }));
    };
    const doek = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return [c, c.getContext('2d', { willReadFrequently: true })]; };
    const bewaar = (naam, c, type = 'image/png', q) => uit.push([naam, c.toDataURL(type, q)]);
    const f = new Function('laad', 'doek', 'bewaar', `return (async () => { ${code} })()`);
    const res = await f(laad, doek, bewaar);
    if (res !== undefined) console.log(JSON.stringify(res));
    return uit;
  }, code);
  for (const [naam, data] of bestanden) {
    fs.writeFileSync(path.join(uit, naam), Buffer.from(data.split(',')[1], 'base64'));
    console.log('geschreven', naam);
  }
  await browser.close();
})();
