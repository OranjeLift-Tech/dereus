// Maakt img/footer-wagen-breed.webp: de footerfoto met links EXTRA (800) px straat erbij.
// Gebruik: node _werk/footer-wagen-breder.cjs [pad-naar-playwright]
//
// Waarom: in img/footer-wagen.webp staat de bumper op x=2, tegen de linkerrand. Het masker van
// .footer__wagen (css/style.css) laat de linkerkant van de foto wegvallen in het Diepblauw, dus de
// voorkant van de wagen vervaagde mee en zag er afgesneden uit. De gebruiker vroeg op 28-09-2026 om
// de foto "bi tik daha sola doğru" te laten doorlopen (eerst 360 px, daarna 560, daarna 800).
// De bron van de wagen (master.png, 2528x1696)
// staat niet in de repo, dus de strook links wordt hier uit de foto zelf opgebouwd:
//
//   rij   0-430  gevel met ramen: gespiegelde strook x 0-100, vaste breedte zodat de ramen recht blijven
//   rij 430-545  gevelvoet met fietsen: strook x 0-50 (daarnaast begint de motorkap)
//   rij 545-700  stoep: klinkertextuur (rij 762-847, x 0-56) in de kleur van de echte stoep onder de bumper
//   rij 700-736  echte stoep en stoeprand, gespiegeld
//   rij 736-847  klinkers; rij 736-762 overgeslagen, daar ligt de schaduw van het wiel
//
// Hoe verder van de wagen, hoe zachter (blur tot 7 px), de fietsenrij sneller, anders leest de
// herhaling als een hek. Het masker is op 41% van 2000 dekkend en de bumper staat op 800 (40%).
// Het oude bestand blijft staan: export-footer-truck.cjs schrijft nog steeds footer-wagen.webp.
const fs = require('fs');
const path = require('path');
const { pak } = require('./controle-kit.cjs');

const WORTEL = path.join(__dirname, '..');
const BRON = path.join(WORTEL, 'img/footer-wagen.webp');
const DOEL = path.join(WORTEL, 'img/footer-wagen-breed.webp');
const KWALITEIT = 0.8;
const EXTRA = 800;   // css/style.css rekent met 2000/732 en het masker; die gaan mee als dit verandert

function bouw(bron, E) {
  const W0 = bron.naturalWidth, H = bron.naturalHeight;
  const src = document.createElement('canvas'); src.width = W0; src.height = H;
  const sg = src.getContext('2d'); sg.drawImage(bron, 0, 0);
  const sd = sg.getImageData(0, 0, W0, H).data;
  const pp = (t, w) => { t = t % (2 * w); return t < w ? t : 2 * w - 1 - t; };
  const px = (x, y) => { const j = (y * W0 + x) * 4; return [sd[j], sd[j + 1], sd[j + 2]]; };
  const lum = ([r, g, b]) => 0.2126 * r + 0.7152 * g + 0.0722 * b;
  let stoep = [0, 0, 0], n = 0;
  for (let y = 704; y < 718; y++) for (let x = 4; x < 56; x++) { const p = px(x, y); stoep[0] += p[0]; stoep[1] += p[1]; stoep[2] += p[2]; n++; }
  stoep = stoep.map(v => v / n);
  let kl = 0, m = 0;
  for (let y = 762; y < H; y++) for (let x = 0; x < 56; x++) { kl += lum(px(x, y)); m++; }
  kl /= m;
  const kaart = (y) => {
    if (y < 430) return { sy: y, w: 100 };
    if (y < 545) return { sy: 430 + pp(y - 430, 58), w: 50 };
    if (y < 700) return { sy: 762 + pp(y - 545, 85), w: 56, stoep: 1 };
    if (y < 722) return { sy: y, w: 60 };
    if (y < 736) return { sy: y, w: 64 };
    if (y < 762) return { sy: y + 26, w: 56 };
    return { sy: y, w: 56 };
  };
  const ext = new ImageData(E, H), ed = ext.data;
  for (let y = 0; y < H; y++) {
    const k = kaart(y);
    const schaduw = k.stoep ? 0.95 + 0.2 * Math.min(1, (y - 545) / 60) : 1;   // bij de gevel iets donkerder
    for (let x = 0; x < E; x++) {
      const d = E - 1 - x, sx = pp(d, k.w);
      let c = px(sx, k.sy);
      if (k.stoep) { const t = lum(c) / kl; c = stoep.map(v => v * t * schaduw); }
      // vlak naast de wagen overvloeien in de echte randpixels, behalve naast de bumper zelf
      if (k.stoep && d < 18 && (y < 600 || y > 650)) { const o = px(pp(d, 4), y), a = 1 - d / 18; c = c.map((v, q) => v * (1 - a) + o[q] * a); }
      const i = (y * E + x) * 4;
      ed[i] = c[0]; ed[i + 1] = c[1]; ed[i + 2] = c[2]; ed[i + 3] = 255;
    }
  }
  const ec = document.createElement('canvas'); ec.width = E; ec.height = H; ec.getContext('2d').putImageData(ext, 0, 0);
  const uit = document.createElement('canvas'); uit.width = E + W0; uit.height = H;
  const g = uit.getContext('2d');
  g.drawImage(src, E, 0);
  const STROOK = 8;
  for (let x0 = 0; x0 < E; x0 += STROOK) {
    const d = E - (x0 + STROOK / 2);
    const lagen = [[0, H, Math.min(7, 0.5 + d / 45)], [426, 124, Math.min(7, 0.5 + d / 16)]];
    for (const [y0, h, blur] of lagen) {
      g.save(); g.beginPath(); g.rect(x0, y0, STROOK, h); g.clip();
      g.filter = `blur(${blur.toFixed(2)}px)`; g.drawImage(ec, 0, 0); g.restore();
    }
  }
  return uit;
}

(async () => {
  const b = await pak(process.argv[2]).chromium.launch({ channel: 'msedge', headless: true });
  const p = await b.newPage();
  const data = 'data:image/webp;base64,' + fs.readFileSync(BRON).toString('base64');
  const uit = await p.evaluate(async ({ data, code, kwaliteit, extra }) => {
    const bron = new Image(); bron.src = data; await bron.decode();
    if (bron.naturalWidth !== 1200 || bron.naturalHeight !== 847) throw new Error(`bron is ${bron.naturalWidth}x${bron.naturalHeight}, verwacht 1200x847`);
    const bouw = new Function('return ' + code)();
    return bouw(bron, extra).toDataURL('image/webp', kwaliteit);
  }, { data, code: bouw.toString(), kwaliteit: KWALITEIT, extra: EXTRA });
  await b.close();
  fs.writeFileSync(DOEL, Buffer.from(uit.split(',')[1], 'base64'));
  console.log(`geschreven: ${path.relative(WORTEL, DOEL)} (${1200 + EXTRA}x847, ${Math.round(fs.statSync(DOEL).size / 1024)} kB)`);
})().catch(e => { console.error(e); process.exit(1); });
