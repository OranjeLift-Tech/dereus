// Exporteert de goedgekeurde dozenfoto naar het fotovak van het lijstplaat-blok op /werkwijze/.
// Gebruik: node _werk/export-lijstplaat-dozen.cjs [--sweep]
//
// Bron: master.png uit _ai-beelden/archief/lijstplaat-dozen-20260923/, variant F uit ronde 5.
// 2752x1536, verhouding 1,7917. Het blok vraagt 720x405, verhouding 1,7778, dus er moet 21 px
// breedte af. Die gaan er RECHTS af: de stapel staat links van het midden en de plaat snijdt
// bovendien zelf vanaf 25% links, dus links wegnemen zou aan het onderwerp komen en rechts niet.
//
// --sweep schrijft niets en laat alleen zien wat de kwaliteitsknop kost.
const fs = require("fs");
const path = require("path");
const sharp = require("C:/Users/arnas/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp");

const WORTEL = path.join(__dirname, "..");
const BRON = path.join(WORTEL, "_ai-beelden/archief/lijstplaat-dozen-20260923/master.png");
const DOEL = path.join(WORTEL, "img/voorbereiding-dozen.webp");

const BRON_MAAT = { width: 2752, height: 1536 };
const UIT = { width: 720, height: 405 };
const SNEE = { left: 0, top: 0, width: Math.round(BRON_MAAT.height * UIT.width / UIT.height), height: BRON_MAAT.height };
const KWALITEIT = 86;   // de belettering is het onderwerp; onder 80 gaan de cijferranden rafelen

const kb = (p) => Math.round(fs.statSync(p).size / 1024);

(async () => {
  const m = await sharp(BRON).metadata();
  if (m.width !== BRON_MAAT.width || m.height !== BRON_MAAT.height) {
    throw new Error(`bron is ${m.width}x${m.height}, verwacht ${BRON_MAAT.width}x${BRON_MAAT.height}`);
  }
  if (Math.abs(SNEE.width / SNEE.height - UIT.width / UIT.height) > 0.002) {
    throw new Error("de snee heeft niet de verhouding van het doel; dan wordt er alsnog vervormd");
  }
  const basis = sharp(BRON).extract(SNEE).resize(UIT.width, UIT.height);

  if (process.argv.includes("--sweep")) {
    for (const q of [74, 78, 82, 86, 90, 94]) {
      const tmp = path.join(require("node:os").tmpdir(), `lijstplaat-q${q}.webp`);
      await sharp(BRON).extract(SNEE).resize(UIT.width, UIT.height)
        .webp({ quality: q, effort: 6 }).toFile(tmp);
      console.log(`q${q}  ${kb(tmp)} kB`);
      fs.unlinkSync(tmp);
    }
    return;
  }

  await basis.webp({ quality: KWALITEIT, effort: 6 }).toFile(DOEL);
  const d = await sharp(DOEL).metadata();
  console.log(`snee    ${SNEE.width}x${SNEE.height} uit ${BRON_MAAT.width}x${BRON_MAAT.height}`);
  console.log(`foto    ${d.width}x${d.height}  q${KWALITEIT}  ${kb(DOEL)} kB  ${path.relative(WORTEL, DOEL)}`);
  if (d.width !== UIT.width || d.height !== UIT.height) {
    throw new Error("de uitvoer heeft niet de maat die in lijstplaat.py staat (720x405)");
  }
})();
