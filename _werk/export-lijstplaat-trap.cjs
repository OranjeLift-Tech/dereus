// Exporteert de werkfoto voor het fotovak van het lijstplaat-blok op /werkwijze/.
// Gebruik: node _werk/export-lijstplaat-trap.cjs
//
// Bron: versie 1 uit de ideeenronde van 23-09-2026 (website/review/voorbereiding-ideeen-20260923/),
// een verhuizer die een smalle Nederlandse trap opmeet. Door ons gemaakt, dus de herkomst is bekend;
// dat was bij elk bestaand bestand in img/ juist niet zo.
//
// Het vak is na de vormwijziging bijna vierkant en vult de kolom (432x453 op 1440, 576x604 op 1920),
// dus van een 16:9-bron blijft maar iets meer dan de helft van de breedte over. Daarom wordt hier de
// MIDDELSTE 65 PROCENT geexporteerd in plaats van het hele kader: dan houdt object-fit cover genoeg
// marge over op elke schermbreedte, en is er nog bijna 2x resolutie op een breed scherm.
const fs = require("fs");
const path = require("path");
const sharp = require("C:/Users/arnas/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp");

const WORTEL = path.join(__dirname, "..");
const BRON = path.join(WORTEL, "website/review/voorbereiding-ideeen-20260923/versie-1.png");
const DOEL = path.join(WORTEL, "img/voorbereiding-trap.webp");

const BRON_MAAT = { width: 2752, height: 1536 };
const DEEL = 0.65;                       // aandeel van de breedte dat mee gaat
const UIT_BREED = 1200;
const KWALITEIT = 86;

const kb = (p) => Math.round(fs.statSync(p).size / 1024);

(async () => {
  const m = await sharp(BRON).metadata();
  if (m.width !== BRON_MAAT.width || m.height !== BRON_MAAT.height) {
    throw new Error(`bron is ${m.width}x${m.height}, verwacht ${BRON_MAAT.width}x${BRON_MAAT.height}`);
  }
  const breed = Math.round(m.width * DEEL);
  const snee = { left: Math.round((m.width - breed) / 2), top: 0, width: breed, height: m.height };
  const hoog = Math.round(UIT_BREED * snee.height / snee.width);

  await sharp(BRON).extract(snee).resize(UIT_BREED, hoog)
    .webp({ quality: KWALITEIT, effort: 6 }).toFile(DOEL);

  const d = await sharp(DOEL).metadata();
  console.log(`snee   ${snee.width}x${snee.height} uit ${m.width}x${m.height} (midden ${DEEL * 100}%)`);
  console.log(`foto   ${d.width}x${d.height}  q${KWALITEIT}  ${kb(DOEL)} kB  ${path.relative(WORTEL, DOEL)}`);
  console.log(`zet in lijstplaat.py:  FOTO = ("/img/voorbereiding-trap.webp", ${d.width}, ${d.height})`);
})();
