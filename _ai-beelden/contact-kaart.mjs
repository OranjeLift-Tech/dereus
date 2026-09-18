// Kaartbeeld voor de adreskaart: OpenStreetMap-tegels rond het kantoor -> ../img/contact-kaart.webp
// Licentie: (c) OpenStreetMap-bijdragers (ODbL). De naamsvermelding staat op de kaart in de HTML.
import sharp from 'sharp'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
const HIER = path.dirname(fileURLToPath(import.meta.url));
const LAT = 52.0596296, LON = 4.2991377, Z = 16, B = 1200, H = 560, T = 256;
const n = 2 ** Z, rad = LAT * Math.PI / 180;
const px = (LON + 180) / 360 * n * T;                                             // wereld-pixels van het kantoor
const py = (1 - Math.log(Math.tan(rad) + 1 / Math.cos(rad)) / Math.PI) / 2 * n * T;
const x0 = Math.floor((px - B / 2) / T), x1 = Math.floor((px + B / 2) / T);
const y0 = Math.floor((py - H / 2) / T), y1 = Math.floor((py + H / 2) / T);
const lagen = [];
for (let x = x0; x <= x1; x++) for (let y = y0; y <= y1; y++) {
  const r = await fetch(`https://tile.openstreetmap.org/${Z}/${x}/${y}.png`, { headers: { 'User-Agent': 'dereus-website-build/1.0 (info@verhuisbedrijfdereus.nl)' } });
  if (!r.ok) throw new Error(`tegel ${x}/${y}: ${r.status}`);
  lagen.push({ input: Buffer.from(await r.arrayBuffer()), left: (x - x0) * T, top: (y - y0) * T });
}
const vel = await sharp({ create: { width: (x1 - x0 + 1) * T, height: (y1 - y0 + 1) * T, channels: 3, background: '#e8eef8' } }).composite(lagen).png().toBuffer();
const info = await sharp(vel)
  .extract({ left: Math.round(px - B / 2) - x0 * T, top: Math.round(py - H / 2) - y0 * T, width: B, height: H })
  .modulate({ saturation: 0.85 }).webp({ quality: 82 }).toFile(path.join(HIER, '..', 'img', 'contact-kaart.webp'));
console.log(`OK img/contact-kaart.webp ${info.width}x${info.height} ${(info.size / 1024) | 0} KB, ${lagen.length} tegels`);
