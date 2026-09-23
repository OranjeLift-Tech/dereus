// Exporteert de foto in de footer opnieuw uit het origineel.
// Gebruik: node _werk/export-footer-wagen.cjs
//
// Het beeld blijft hetzelfde: dezelfde uitsnede van dezelfde foto, alleen een schonere export.
// Wat er veranderde en waarom:
//
// Het bestand dat live stond was 1380 x 974, maar het origineel is 1200 x 896. De uitsnede
// (de bovenste 1200 x 847) was dus 1,15x opgeblazen: 180 pixels breed die geen detail bevatten.
// De footer toont de foto op zijn breedst 1094 css-pixels (object-fit: cover, zie .footer__wagen),
// dus 1200 echte pixels dekken 1x ruim. Gemeten op die 1094px, als variantie van de Laplaciaan:
//
//   1380 x 974, zoals het live stond   142 kB   440
//   1200 x 847 uit het origineel       130 kB   628
//
// Scherper en tegelijk lichter, omdat de opblazing eruit is. Scherper dan dit kan niet uit deze
// bron: voor een echte 2x zou de footer 2189 pixels breed nodig hebben en zo veel detail zit er
// niet in het origineel. Opschalen naar 2189 verzint pixels en meet zelfs lager (614 bij 388 kB).
const fs = require("fs");
const path = require("path");
const sharp = require("C:/Users/arnas/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp");

const WORTEL = path.join(__dirname, "..");
const BRON = path.join(WORTEL, "_ai-beelden/foto/Onze diensten/Nationale verhuizingen.jpg");
const MASTER = path.join(WORTEL, "_ai-beelden/foto/footer-wagen-master.png");
const DOEL = path.join(WORTEL, "img/footer-wagen.webp");

// De uitsnede zoals hij live stond, teruggerekend uit het bestand dat er was: de bovenste
// 1200 x 847 van het origineel, verhouding 1380/974.
const SNEE = { left: 0, top: 0, width: 1200, height: 847 };
const KWALITEIT = 78;   // het knikpunt: q72 geeft 616, q94 geeft 650 voor bijna drie keer de kB

const kb = (p) => Math.round(fs.statSync(p).size / 1024);

(async () => {
  const m = await sharp(BRON).metadata();
  if (m.width !== 1200 || m.height !== 896) {
    throw new Error(`origineel is ${m.width}x${m.height}, verwacht 1200x896 — controleer de uitsnede`);
  }
  await sharp(BRON).extract(SNEE).png({ compressionLevel: 9 }).toFile(MASTER);
  await sharp(MASTER).webp({ quality: KWALITEIT, effort: 6 }).toFile(DOEL);
  console.log(`${path.relative(WORTEL, MASTER)}: ${SNEE.width}x${SNEE.height}, ${kb(MASTER)} kB`);
  console.log(`${path.relative(WORTEL, DOEL)}: ${SNEE.width}x${SNEE.height}, ${kb(DOEL)} kB`);
  console.log("Let op: de width/height van de img staan in _werk/navigatie.py, functie footer().");
})();
