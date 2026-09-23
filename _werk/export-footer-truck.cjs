// Exporteert de goedgekeurde vrachtwagen naar de footerfoto.
// Gebruik: node _werk/export-footer-truck.cjs
//
// Waarom naast export-footer-wagen.cjs en niet erin: dat script leest één bepaalde bronfoto en
// controleert dat die 1200x896 is. Op deze bron zou het meteen stuk lopen. Zelfde vorm, andere
// constanten, dus een eigen bestand. export-footer-wagen.cjs blijft staan voor als de oude foto
// terug moet.
//
// De bron is master.png uit _ai-beelden/archief/truck-zijkant-20260923/: variant D uit ronde 3,
// de wagen die de gebruiker koos. 2528x1696, verhouding 1,4906.
//
// De footer wil 1200x847, verhouding 1,4168, dus er moet 125 pixels breedte af. Die gaan er
// LINKS af, en dat is geen willekeurige kant:
//
//   .footer__wagen staat rechts uitgelijnd met een masker dat van doorzichtig op 0 naar dekkend
//   op 38% van de beeldbreedte loopt (css/style.css). De linkerrand van de foto vervaagt dus
//   sowieso in het Diepblauw. De belettering op de flank zit op 58 tot 89 procent van de breedte
//   en valt daarmee ruim in het dekkende deel.
//
//   Gemeten loopt de wagen van x=127 (bumper) tot x=2285 (achterhoek). Links 125 px wegsnijden
//   zet de bumper dus op x=2, tegen de beeldrand aan. In elk ander vak zou dat fout zijn; hier
//   valt precies die rand weg onder het masker.
const fs = require("fs");
const path = require("path");
const sharp = require("C:/Users/arnas/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp");

const WORTEL = path.join(__dirname, "..");
const BRON = path.join(WORTEL, "_ai-beelden/archief/truck-zijkant-20260923/master.png");
const MASTER = path.join(WORTEL, "_ai-beelden/archief/footer-wagen-20260923/footer-wagen-truck-master.png");
const DOEL = path.join(WORTEL, "img/footer-wagen.webp");

const BRON_MAAT = { width: 2528, height: 1696 };
const SNEE = { left: 125, top: 0, width: 2403, height: 1696 };
const UIT = { width: 1200, height: 847 };
const KWALITEIT = 78;   // hetzelfde knikpunt dat export-footer-wagen.cjs vond

const kb = (p) => Math.round(fs.statSync(p).size / 1024);

(async () => {
  const m = await sharp(BRON).metadata();
  if (m.width !== BRON_MAAT.width || m.height !== BRON_MAAT.height) {
    throw new Error(`bron is ${m.width}x${m.height}, verwacht ${BRON_MAAT.width}x${BRON_MAAT.height}`);
  }
  if (Math.abs(SNEE.width / SNEE.height - UIT.width / UIT.height) > 0.001) {
    throw new Error("de snee heeft niet de verhouding van het doel; dan wordt er alsnog vervormd");
  }

  await sharp(BRON).extract(SNEE).png({ compressionLevel: 9 }).toFile(MASTER);
  await sharp(MASTER).resize(UIT.width, UIT.height).webp({ quality: KWALITEIT, effort: 6 }).toFile(DOEL);

  const d = await sharp(DOEL).metadata();
  console.log(`master  ${SNEE.width}x${SNEE.height}  ${kb(MASTER)} kB  ${path.relative(WORTEL, MASTER)}`);
  console.log(`footer  ${d.width}x${d.height}  ${kb(DOEL)} kB  ${path.relative(WORTEL, DOEL)}`);
  if (d.width !== UIT.width || d.height !== UIT.height) {
    throw new Error("de uitvoer heeft niet de maat die in navigatie.py staat (1200x847)");
  }
})();
