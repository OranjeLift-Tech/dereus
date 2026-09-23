// Exporteert de werkfoto voor het fotovak van het lijstplaat-blok op /werkwijze/.
// Gebruik: node _werk/export-lijstplaat-kast.cjs
//
// Bron: versie 5 uit de ideeenronde van 23-09-2026 (website/review/voorbereiding-ideeen-20260923/),
// een verhuizer die in een deuropening kijkt of een massieve kast erdoor past. Door ons gemaakt, dus
// met herkomst. Vervangt voorbereiding-trap.webp, die de gebruiker in zijn beeldinventaris op
// "delete" zette (23-09-2026).
//
// Zelfde aanpak als export-lijstplaat-trap.cjs: het vak is ongeveer vierkant en vult de kolom, dus er
// gaat 65 procent van de breedte mee. Alleen staat het onderwerp hier niet in het midden maar links
// daarvan (kast en man samen ongeveer 19 tot 60 procent van de breedte), dus de snee ligt om 40
// procent in plaats van om het midden.
const fs = require("fs");
const path = require("path");
const sharp = require("C:/Users/arnas/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp");

const WORTEL = path.join(__dirname, "..");
const BRON = path.join(WORTEL, "website/review/voorbereiding-ideeen-20260923/versie-5.png");
const DOEL = path.join(WORTEL, "img/voorbereiding-kast.webp");

const BRON_MAAT = { width: 2752, height: 1536 };
const DEEL = 0.65;                       // aandeel van de breedte dat mee gaat
const MIDDEN = 0.40;                     // waar het onderwerp staat, als deel van de breedte
const UIT_BREED = 1200;
const KWALITEIT = 86;

const kb = (p) => Math.round(fs.statSync(p).size / 1024);

(async () => {
  const m = await sharp(BRON).metadata();
  if (m.width !== BRON_MAAT.width || m.height !== BRON_MAAT.height) {
    throw new Error(`bron is ${m.width}x${m.height}, verwacht ${BRON_MAAT.width}x${BRON_MAAT.height}`);
  }
  const breed = Math.round(m.width * DEEL);
  const links = Math.min(m.width - breed, Math.max(0, Math.round(m.width * MIDDEN - breed / 2)));
  const snee = { left: links, top: 0, width: breed, height: m.height };
  const hoog = Math.round(UIT_BREED * snee.height / snee.width);

  await sharp(BRON).extract(snee).resize(UIT_BREED, hoog)
    .webp({ quality: KWALITEIT, effort: 6 }).toFile(DOEL);

  const d = await sharp(DOEL).metadata();
  console.log(`snee   ${snee.width}x${snee.height} vanaf x ${snee.left} uit ${m.width}x${m.height}`);
  console.log(`foto   ${d.width}x${d.height}  q${KWALITEIT}  ${kb(DOEL)} kB  ${path.relative(WORTEL, DOEL)}`);
  console.log(`zet in lijstplaat.py:  FOTO = ("/img/voorbereiding-kast.webp", ${d.width}, ${d.height})`);
})();
