// De vier beelden van de bewegende collage in de hero van de home (_werk/blokken/herocollage.py), 28-09-2026.
// Keuze van de gebruiker (website/review/hero-collage-20260928/): beeld 2, 4, 5 en 6 van de lijst, in deze volgorde.
//   node img/headers/maak-collage.cjs
// Maximaal 1280 breed, WebP q50: onder de 40% verdonkering van de hero ziet niemand het verlies, en 1280 in plaats
// van 1400 scheelt alleen al een derde. De lift is maar 720 breed en wordt niet opgeschaald. Een bestaand bestand
// wordt nooit overschreven: een nieuwe versie krijgt een nieuwe naam (en dan ook in herocollage.py en het manifest).
const fs = require('node:fs');
const path = require('node:path');
const sharp = require('C:/Users/arnas/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root = path.resolve(__dirname, '../..');
const BEELDEN = [
  ['img/verhuisdag-dragen-stoep.webp', 'home-collage-1-dragen-stoep.webp'],
  ['img/dienst-verhuislift.webp', 'home-collage-2-verhuislift.webp'],
  ['img/footer-wagen.webp', 'home-collage-3-wagen.webp'],          // de nieuwe wagen, md5 f26a9436...
  ['img/dienst-nationaal-v2-groot.webp', 'home-collage-4-uitladen.webp'],
];
(async () => {
  for (const [bron, naam] of BEELDEN) {
    const doel = path.join(__dirname, naam);
    if (fs.existsSync(doel)) { console.log('bestaat al, overgeslagen:', naam); continue; }
    const uit = await sharp(path.join(root, bron)).resize({ width: 1280, withoutEnlargement: true }).webp({ quality: 50, effort: 6 }).toFile(doel);
    console.log(naam, `${uit.width}x${uit.height}`, fs.statSync(doel).size, 'bytes, uit', bron);
  }
})().catch((fout) => { console.error(fout); process.exitCode = 1; });
