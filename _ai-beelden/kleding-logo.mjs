// Zet het echte De Reus-logo op de werkkleding in de foto's van de verhuizer.
// AI en stock krijgen het logo nooit precies goed; daarom komt het hier uit het vectorbestand (img/de-reus-logo-02*.svg).
//  1. het petrolgroene shirt wordt koningsblauw (#1746A2), alleen die kleurtoon, huid en hout blijven gelijk
//  2. het borstzakje met het patroon wordt een wit logovlak met het logo, in het perspectief van het zakje
//   node kleding-logo.mjs            alle foto's, bron uit foto/origineel (wordt de eerste keer aangemaakt)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const HIER = path.dirname(fileURLToPath(import.meta.url));
const IMG = path.join(HIER, '..', 'img');
const ORIG = path.join(HIER, 'foto', 'origineel');
fs.mkdirSync(ORIG, { recursive: true });

// hoekpunten van het zakje: linksboven, rechtsboven, rechtsonder, punt, linksonder
const FOTOS = [
  { naam: 'over-verhuizer', zak: [[364, 330], [433, 312], [442, 382], [402, 402], [370, 395]], logo: 'vol' },
  { naam: 'aanvraag-verhuizer', zak: [[340, 245], [386, 234], [392, 280], [370, 296], [347, 291]], logo: 'vol' },
  { naam: 'verwachten-inpakken', zak: [[479, 213], [496, 206], [503, 227], [502, 244], [490, 243], [483, 228]], logo: 'beeld', breed: 1.15 },
];

function rgbNaarHsl(r, g, b) {
  r /= 255; g /= 255; b /= 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b), l = (max + min) / 2;
  if (max === min) return [0, 0, l];
  const d = max - min, s = l > .5 ? d / (2 - max - min) : d / (max + min);
  let h = max === r ? (g - b) / d + (g < b ? 6 : 0) : max === g ? (b - r) / d + 2 : (r - g) / d + 4;
  return [h * 60, s, l];
}
function hslNaarRgb(h, s, l) {
  const c = (1 - Math.abs(2 * l - 1)) * s, x = c * (1 - Math.abs((h / 60) % 2 - 1)), m = l - c / 2;
  const [r, g, b] = h < 60 ? [c, x, 0] : h < 120 ? [x, c, 0] : h < 180 ? [0, c, x] : h < 240 ? [0, x, c] : h < 300 ? [x, 0, c] : [c, 0, x];
  return [(r + m) * 255, (g + m) * 255, (b + m) * 255];
}
const zacht = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };

// petrol/cyaan (tint 160-205) -> koningsblauw, met zachte overgang zodat er geen randen ontstaan
async function shirtBlauw(bron) {
  const { data, info } = await sharp(bron).removeAlpha().raw().toBuffer({ resolveWithObject: true });
  for (let i = 0; i < data.length; i += 3) {
    const [h, s, l] = rgbNaarHsl(data[i], data[i + 1], data[i + 2]);
    const w = zacht(150, 168, h) * (1 - zacht(200, 212, h)) * zacht(.12, .3, s) * (1 - zacht(.62, .8, l));
    if (w <= 0) continue;
    const [r, g, b] = hslNaarRgb(221, Math.min(1, s * .9 + .12), Math.min(.62, l * 1.5 + .02));
    data[i] = data[i] + (r - data[i]) * w; data[i + 1] = data[i + 1] + (g - data[i + 1]) * w; data[i + 2] = data[i + 2] + (b - data[i + 2]) * w;
  }
  return sharp(data, { raw: info }).png().toBuffer();
}

async function logoPng(soort) {
  // 'vol': armen, huis, VERHUISBEDRIJF DE REUS (zonder payoff, die is op deze maat onleesbaar); 'beeld': alleen armen en huis
  let svg = fs.readFileSync(path.join(IMG, 'de-reus-logo-02.svg'), 'utf8');
  svg = svg.replace(/viewBox="[^"]*"/, soort === 'vol' ? 'viewBox="316 195 296 252"' : 'viewBox="316 195 296 150"');
  const buf = await sharp(Buffer.from(svg), { density: 300 }).resize({ width: 600 }).png().toBuffer();
  const m = await sharp(buf).metadata();
  return { buf, w: m.width, h: m.height };
}

async function maak({ naam, zak, logo, breed = 1 }) {
  const doel = path.join(IMG, `${naam}.webp`);
  const bron = path.join(ORIG, `${naam}.webp`);
  if (!fs.existsSync(bron)) fs.copyFileSync(doel, bron);
  const basis = await shirtBlauw(bron);
  const { width: W, height: H } = await sharp(basis).metadata();

  const [lb, rb] = zak, lo = zak[zak.length - 1];
  const u = [rb[0] - lb[0], rb[1] - lb[1]], v = [lo[0] - lb[0], lo[1] - lb[1]];
  const lu = Math.hypot(...u), lv = Math.hypot(...v);
  const U = [u[0] / lu, u[1] / lu], V = [v[0] / lv, v[1] / lv];
  const L = await logoPng(logo);
  let k = .8 * breed * lu / L.w;
  if (k * L.h > .8 * lv) k = .8 * lv / L.h;
  const mx = (lu - k * L.w) / 2, my = Math.max(lv * .07, (lv * .86 - k * L.h) / 2);
  const e = lb[0] + U[0] * mx + V[0] * my, f = lb[1] + U[1] * mx + V[1] * my;
  const pts = zak.map(p => p.join(',')).join(' ');
  const cx = zak.reduce((a, p) => a + p[0], 0) / zak.length, cy = zak.reduce((a, p) => a + p[1], 0) / zak.length;
  const hoek = Math.atan2(u[1], u[0]) * 180 / Math.PI;

  const vlak = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${W}" height="${H}">
    <defs><linearGradient id="s" gradientTransform="rotate(${hoek.toFixed(1)} .5 .5)"><stop offset="0" stop-color="#F7F8FA"/><stop offset=".7" stop-color="#ECEEF2"/><stop offset="1" stop-color="#D5D9E2"/></linearGradient></defs>
    <polygon points="${pts}" fill="#0B2A66" opacity=".45" transform="translate(.6 1.4)" stroke="#0B2A66" stroke-width="3.4" stroke-linejoin="round"/>
    <polygon points="${pts}" fill="url(#s)" stroke="url(#s)" stroke-width="3" stroke-linejoin="round"/>
    <polygon points="${pts}" fill="none" stroke="#8C95A8" stroke-opacity=".55" stroke-width=".6" stroke-dasharray="1.6 1.2" stroke-linejoin="round" transform="translate(${(cx * .08).toFixed(2)} ${(cy * .08).toFixed(2)}) scale(.92)"/>
    <image xlink:href="data:image/png;base64,${L.buf.toString('base64')}" width="${L.w}" height="${L.h}" transform="matrix(${U[0] * k} ${U[1] * k} ${V[0] * k} ${V[1] * k} ${e} ${f})"/>
  </svg>`);
  // heel licht verzachten zodat het vlak dezelfde scherpte heeft als de foto
  const laag = await sharp(vlak).blur(.45).png().toBuffer();
  const info = await sharp(basis).composite([{ input: laag }]).webp({ quality: 84 }).toFile(doel);
  console.log('OK', `img/${naam}.webp`, `${info.width}x${info.height}`);
}

for (const f of FOTOS) await maak(f);
