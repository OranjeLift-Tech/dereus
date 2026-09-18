// Maakt de werkwijze-rit klaar voor de site:
//  - foto/rit-wagen.*  -> groen weg (chroma key), randen zacht, groene rand eraf -> ../img/rit-wagen.webp
//  - foto/rit-straat.* -> ../img/rit-straat.webp (2400 breed) en rit-straat-mobiel.webp (1200 breed)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const HIER = path.dirname(fileURLToPath(import.meta.url));
const IMG = path.join(HIER, '..', 'img');
const vind = naam => ['png', 'jpg', 'jpeg', 'webp'].map(e => path.join(HIER, 'foto', `${naam}.${e}`)).find(fs.existsSync);

// ---- vrachtwagen: groen scherm eruit ----
const wagen = vind('rit-wagen');
if (wagen) {
  const { data, info } = await sharp(wagen).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  for (let i = 0; i < data.length; i += 4) {
    const r = data[i], g = data[i + 1], b = data[i + 2];
    const groen = g - Math.max(r, b);            // hoe "groen" is deze pixel
    if (groen > 60) data[i + 3] = 0;             // achtergrond
    else if (groen > 20) {                       // rand: half doorzichtig
      data[i + 3] = Math.round(255 * (60 - groen) / 40);
    }
    if (groen > 0) data[i + 1] = Math.max(r, b); // groene weerschijn op de rand weghalen
  }
  await sharp(data, { raw: info })
    .trim({ threshold: 1 })
    .resize({ width: 1100, withoutEnlargement: true })
    .webp({ quality: 88, alphaQuality: 90 })
    .toFile(path.join(IMG, 'rit-wagen.webp'));
  console.log('OK rit-wagen.webp');
} else console.log('ontbreekt: foto/rit-wagen');

// ---- straat ----
const straat = vind('rit-straat');
if (straat) {
  await sharp(straat).resize({ width: 2400, withoutEnlargement: true }).webp({ quality: 80 }).toFile(path.join(IMG, 'rit-straat.webp'));
  await sharp(straat).resize({ width: 1200 }).webp({ quality: 78 }).toFile(path.join(IMG, 'rit-straat-mobiel.webp'));
  console.log('OK rit-straat.webp + rit-straat-mobiel.webp');
} else console.log('ontbreekt: foto/rit-straat');
