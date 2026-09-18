// Zet het echte De Reus-logo op kleding, dozen en voertuigen in de dienstfoto's (img/dienst-*.webp).
// Logo komt uit het vectorbestand, nooit nagetekend. Bron blijft bewaard in foto/origineel.
//   node dienst-logo.mjs            alle dienstfoto's
//   node dienst-logo.mjs nationaal  alleen die
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const HIER = path.dirname(fileURLToPath(import.meta.url));
const IMG = path.join(HIER, '..', 'img');
const ORIG = path.join(HIER, 'foto', 'origineel');
const W = 720, H = 540;

// ---------- logo's ----------
const VB = { vol: '316 195 296 252', beeld: '316 195 296 150', payoff: '316 195 296 291' };
const logoCache = {};
async function logo(soort) {
  if (logoCache[soort]) return logoCache[soort];
  let svg = fs.readFileSync(path.join(IMG, 'de-reus-logo-02.svg'), 'utf8').replace(/viewBox="[^"]*"/, `viewBox="${VB[soort]}"`);
  const buf = await sharp(Buffer.from(svg), { density: 300 }).resize({ width: 600 }).png().toBuffer();
  const m = await sharp(buf).metadata();
  return (logoCache[soort] = { b64: buf.toString('base64'), w: m.width, h: m.height });
}

// affiene afbeelding van een rechthoek (pw x ph) op drie punten: linksboven, rechtsboven, linksonder
const matrix = ([tl, tr, bl], pw, ph) =>
  `matrix(${(tr[0] - tl[0]) / pw} ${(tr[1] - tl[1]) / pw} ${(bl[0] - tl[0]) / ph} ${(bl[1] - tl[1]) / ph} ${tl[0]} ${tl[1]})`;

// ---------- kleur ----------
function hsl(r, g, b) {
  r /= 255; g /= 255; b /= 255;
  const mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2;
  if (mx === mn) return [0, 0, l];
  const d = mx - mn, s = l > .5 ? d / (2 - mx - mn) : d / (mx + mn);
  const h = mx === r ? (g - b) / d + (g < b ? 6 : 0) : mx === g ? (b - r) / d + 2 : (r - g) / d + 4;
  return [h * 60, s, l];
}
function rgb(h, s, l) {
  const c = (1 - Math.abs(2 * l - 1)) * s, x = c * (1 - Math.abs((h / 60) % 2 - 1)), m = l - c / 2;
  const [r, g, b] = h < 60 ? [c, x, 0] : h < 120 ? [x, c, 0] : h < 180 ? [0, c, x] : h < 240 ? [0, x, c] : h < 300 ? [x, 0, c] : [c, 0, x];
  return [(r + m) * 255, (g + m) * 255, (b + m) * 255];
}
const zacht = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };

async function masker(poly) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}"><polygon points="${poly.map(p => p.join(',')).join(' ')}" fill="#fff"/></svg>`;
  return sharp(Buffer.from(svg)).blur(2).extractChannel(0).raw().toBuffer();
}

// kleding in een gebied naar koningsblauw; 'soort' bepaalt welke pixels stof zijn
async function kleur(data, { poly, soort }) {
  const m = await masker(poly);
  for (let p = 0, i = 0; p < W * H; p++, i += 3) {
    if (!m[p]) continue;
    const [h, s, l] = hsl(data[i], data[i + 1], data[i + 2]);
    let w, L;
    if (soort === 'petrol') { w = zacht(150, 168, h) * (1 - zacht(212, 225, h)) * zacht(.1, .25, s) * (1 - zacht(.62, .8, l)); L = Math.min(.6, l * 1.45 + .03); }
    else if (soort === 'grijs') { w = (1 - zacht(.14, .26, s)) * zacht(.06, .12, l) * (1 - zacht(.55, .68, l)); L = Math.min(.58, l * 1.2 + .04); }
    else if (soort === 'wit') { w = (1 - zacht(.12, .22, s)) * zacht(.5, .62, l); L = Math.min(.62, l * .62); }
    w *= m[p] / 255;
    if (w <= 0) continue;
    const [r, g, b] = rgb(221, soort === 'wit' ? .72 : Math.min(1, s * .9 + .45), L);
    data[i] += (r - data[i]) * w; data[i + 1] += (g - data[i + 1]) * w; data[i + 2] += (b - data[i + 2]) * w;
  }
}

// ---------- lagen ----------
// wit logovlak met het logo (kleding): quad = [linksboven, rechtsboven, linksonder]
async function vlak({ quad, soort = 'vol', schaal = .82 }) {
  const L = await logo(soort), PW = 1000, PH = 1000 * L.h / L.w / schaal;
  const k = (PW * schaal) / L.w, x = (PW - L.w * k) / 2, y = (PH - L.h * k) / 2;
  return `<g transform="${matrix(quad, PW, PH)}">
    <rect x="-8" y="10" width="${PW + 16}" height="${PH}" rx="70" fill="#0B1F45" opacity=".28"/>
    <rect width="${PW}" height="${PH}" rx="70" fill="url(#stof)"/>
    <image href="data:image/png;base64,${L.b64}" x="${x}" y="${y}" width="${L.w * k}" height="${L.h * k}"/></g>`;
}
// logo rechtstreeks gedrukt (dozen, voertuigen)
async function druk({ quad, soort = 'beeld', dekking = .9 }) {
  const L = await logo(soort);
  return `<image href="data:image/png;base64,${L.b64}" width="${L.w}" height="${L.h}" opacity="${dekking}" transform="${matrix(quad, L.w, L.h)}"/>`;
}
const band = ({ poly, kleur = '#1746A2', dekking = .92 }) =>
  `<polygon points="${poly.map(p => p.join(',')).join(' ')}" fill="${kleur}" opacity="${dekking}"/>`;
const wit = ({ poly }) => `<polygon points="${poly.map(p => p.join(',')).join(' ')}" fill="#F4F2EE"/>`;

// ---------- per foto ----------
const FOTOS = {
  particulier: {
    kleur: [{ soort: 'petrol', poly: [[0, 250], [70, 228], [250, 232], [298, 300], [300, 430], [240, 540], [0, 540]] }],
    boven: [{ t: 'vlak', quad: [[98, 292], [214, 286], [100, 372]], blur: .5 }],
  },
  zakelijk: {
    druk: [
      { t: 'wit', poly: [[287, 387], [449, 390], [448, 520], [287, 519]] },
      { t: 'druk', soort: 'vol', quad: [[300, 398], [436, 400], [300, 510]], dekking: 1 },
    ],
  },
  nationaal: {
    kleur: [{ soort: 'wit', poly: [[426, 228], [462, 222], [470, 260], [466, 322], [430, 324], [420, 280]] }],
    druk: [
      { t: 'band', poly: [[150, 348], [352, 347], [352, 362], [150, 364]] },
      { t: 'band', poly: [[492, 345], [632, 344], [632, 359], [492, 361]] },
      { t: 'band', poly: [[150, 348], [352, 347], [352, 351], [150, 352]], kleur: '#FFCC33' },
      { t: 'band', poly: [[492, 345], [632, 344], [632, 348], [492, 349]], kleur: '#FFCC33' },
      { t: 'druk', soort: 'payoff', quad: [[505, 192], [620, 190], [505, 305]], dekking: .96 },
      { t: 'druk', soort: 'beeld', quad: [[362, 300], [414, 298], [362, 327]], dekking: .85 },
    ],
  },
  internationaal: {
    kleur: [{ soort: 'grijs', poly: [[140, 300], [330, 295], [360, 360], [372, 540], [128, 540]] }],
    boven: [{ t: 'vlak', quad: [[148, 318], [286, 318], [150, 402]], blur: .5 }],
  },
  woningontruiming: {
    druk: [
      { t: 'druk', soort: 'payoff', quad: [[130, 318], [300, 318], [130, 485]], dekking: .88, blur: 3 },
      { t: 'druk', soort: 'beeld', quad: [[522, 140], [594, 138], [522, 176]], dekking: .88 },
      { t: 'druk', soort: 'beeld', quad: [[412, 124], [470, 122], [412, 154]], dekking: .88 },
    ],
  },
  opslag: {
    druk: [
      { t: 'druk', soort: 'beeld', quad: [[312, 312], [370, 310], [312, 342]], dekking: .88 },
      { t: 'druk', soort: 'beeld', quad: [[432, 316], [490, 314], [432, 345]], dekking: .88 },
    ],
    boven: [
      { t: 'vlak', soort: 'beeld', quad: [[344, 262], [372, 260], [345, 284]], blur: .35 },
      { t: 'vlak', soort: 'beeld', quad: [[468, 276], [496, 274], [469, 297]], blur: .35 },
    ],
  },
  handyman: {},
  verhuislift: {
    boven: [{ t: 'vlak', soort: 'vol', quad: [[532, 238], [632, 234], [533, 320]], schaal: .86, blur: .5 }],
  },
};

async function laag(items) {
  const delen = [];
  for (const it of items) {
    const svgDeel = it.t === 'vlak' ? await vlak(it) : it.t === 'druk' ? await druk(it) : it.t === 'band' ? band(it) : wit(it);
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}"><defs>
      <linearGradient id="stof" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FAFBFC"/><stop offset=".7" stop-color="#EEF0F4"/><stop offset="1" stop-color="#D8DCE4"/></linearGradient></defs>${svgDeel}</svg>`;
    delen.push({ input: await sharp(Buffer.from(svg)).blur(it.blur || .45).png().toBuffer(), blend: it.t === 'druk' || it.t === 'band' ? 'multiply' : 'over' });
  }
  return delen;
}

const filter = process.argv.slice(2);
for (const [naam, cfg] of Object.entries(FOTOS)) {
  if (filter.length && !filter.includes(naam)) continue;
  const bron = path.join(ORIG, `dienst-${naam}.webp`);
  if (!fs.existsSync(bron)) fs.copyFileSync(path.join(IMG, `dienst-${naam}.webp`), bron);
  const { data } = await sharp(bron).resize(W, H).removeAlpha().raw().toBuffer({ resolveWithObject: true });
  for (const k of cfg.kleur || []) await kleur(data, k);
  const lagen = [...await laag(cfg.druk || []), ...await laag(cfg.boven || [])];
  await sharp(data, { raw: { width: W, height: H, channels: 3 } }).composite(lagen).webp({ quality: 80 }).toFile(path.join(IMG, `dienst-${naam}.webp`));
  console.log('OK', naam);
}
