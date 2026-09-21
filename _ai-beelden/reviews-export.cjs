// Reviews: uitsnede -> /img/review-klant-<n>.webp. Stap 2 van 2, na reviews-uitsnede.mjs.
//   - zachte alfa onder de drempel weg (waas rond het haar), bijsnijden op de persoon
//   - alle drie even hoog (520 px) en met de kruin op dezelfde plek, zodat ze in de rij even groot staan
const fs = require('node:fs');
const path = require('node:path');
const HIER = __dirname;
const sharp = require(path.join(HIER, 'node_modules', 'sharp'));
const MAP = path.join(HIER, 'foto', 'reviews');
const IMG = path.join(HIER, '..', 'img');
const DREMPEL = 45, HOOGTE = 520;

(async () => {
  for (const n of [1, 2, 3]) {
    const bron = path.join(MAP, `klant-${n}-uit.png`);
    if (!fs.existsSync(bron)) { console.log(`- klant-${n}: eerst reviews-uitsnede.mjs draaien`); continue; }
    const { data, info } = await sharp(bron).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
    for (let i = 3; i < data.length; i += 4) { if (data[i] < DREMPEL) data[i] = 0; else if (data[i] > 240) data[i] = 255; }
    const knip = await sharp(data, { raw: { width: info.width, height: info.height, channels: 4 } }).png().toBuffer();
    const uit = await sharp(knip).trim({ threshold: 2 }).resize({ height: HOOGTE }).webp({ quality: 80, effort: 6, alphaQuality: 85 })
      .toFile(path.join(IMG, `review-klant-${n}.webp`));
    console.log(`review-klant-${n}.webp`, uit.width, uit.height, Math.round(uit.size / 1024) + ' kB');
  }
})();
