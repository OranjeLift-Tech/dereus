/* Normaliseert een uitsnede, zodat er downstream geen enkele per-beeld constante meer nodig is.

   node _ai-beelden/uitsnede-normaliseren.cjs <uitsnede.webp|png> [opties]

   Opties
     --naar <map>      doelmap, standaard naast de bron
     --naam <naam>     basisnaam, standaard de naam van de bron
     --doek b,h        het doek waarop we plakken, standaard 1000,1250
     --onder <0..1>    marge onder het onderwerp, als deel van de doekhoogte, standaard 0
     --zij <0..1>      marge links en rechts samen, als deel van de doekbreedte, standaard 0.08
     --vervang         sta toe dat een bestaand bestand wordt overschreven

   Wat het doet en waarom:
   De dienstpanelen meten achteraf waar het onderwerp in elke uitsnede zit (uitstap.json) en geven elk
   beeld daarna zijn eigen pop, knip en y. Dat werkt, maar er hoort een meetstap bij en die kan uit de pas
   gaan lopen zodra iemand de uitsnedes opnieuw exporteert.
   Hier gebeurt het andersom: we snijden op de alfa-omhullende van het onderwerp zelf, en plakken dat op
   een doek van vaste maat, onderaan uitgelijnd en horizontaal gecentreerd. Elk beeld verlaat de route dan
   met dezelfde meetkunde, en downstream is één CSS-regel genoeg voor allemaal. De meetstap verdwijnt dus,
   in plaats van dat hij geautomatiseerd wordt.

   Wat het kost: normaliseren snijdt en herschaalt, dus een genormaliseerde uitsnede ligt niet meer pixel
   voor pixel op zijn eigen bronfoto. Een compositie die de foto en de uitsnede exact laat samenvallen, en
   alleen het onderwerp over een rand laat steken zoals css/blok/homecontact.css doet, kan dus niet met een
   genormaliseerd bestand. Kies vooraf: samenvallen met de eigen bron, of dezelfde meetkunde als alle andere
   uitsnedes. Allebei gaat niet.
   Vuistregel: lagen uit één foto die over elkaar liggen, niet normaliseren. Losse figuren die naast elkaar
   of op een vlak staan, juist wel.
   Het geschreven JSON-bestand legt alleen vast welke fracties gebruikt zijn, zodat de CSS-kant weet met
   welke afspraak de beelden gemaakt zijn. Het bevat bewust geen waarden per beeld. */
const fs = require('node:fs');
const path = require('node:path');
const sharp = require(process.env.SHARP_MODULE || 'C:/Users/arnas/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');

const argv = process.argv.slice(2);
const vlag = (naam, standaard) => {
  const i = argv.indexOf('--' + naam);
  return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : standaard;
};
const bron = argv[0] && !argv[0].startsWith('--') ? argv[0] : null;
const doek = (vlag('doek', '1000,1250')).split(',').map(Number);
const onder = Number(vlag('onder', '0'));
const zij = Number(vlag('zij', '0.08'));
const vervang = argv.includes('--vervang');

(async () => {
  if (!bron || !fs.existsSync(bron)) throw new Error('Geef een bestaande uitsnede op.');
  if (doek.length !== 2 || doek.some(Number.isNaN)) throw new Error('Geef --doek als breedte,hoogte.');
  const naar = path.resolve(vlag('naar', path.dirname(bron)));
  const naam = vlag('naam', path.basename(bron, path.extname(bron)));
  const meta = await sharp(bron).metadata();
  if (!meta.hasAlpha) throw new Error('De bron mist een alfakanaal; dit werkt alleen op een uitsnede.');

  // 1. bijsnijden op de alfa-omhullende: precies het onderwerp, niets eromheen
  const gesneden = await sharp(bron).trim({ threshold: 1 }).png().toBuffer();
  const gm = await sharp(gesneden).metadata();

  // 2. schalen zodat het onderwerp binnen het doek past, met de afgesproken marges
  const [db, dh] = doek;
  const ruimteB = db * (1 - zij);
  const ruimteH = dh * (1 - onder);
  const schaal = Math.min(ruimteB / gm.width, ruimteH / gm.height);
  const nb = Math.max(1, Math.round(gm.width * schaal));
  const nh = Math.max(1, Math.round(gm.height * schaal));
  const geschaald = await sharp(gesneden).resize(nb, nh).png().toBuffer();

  // 3. onderaan uitgelijnd en horizontaal gecentreerd op een doorzichtig doek van vaste maat
  const links = Math.round((db - nb) / 2);
  const boven = Math.round(dh - Math.round(dh * onder) - nh);
  fs.mkdirSync(naar, { recursive: true });
  const doelBeeld = path.join(naar, `${naam}.webp`);
  if (fs.existsSync(doelBeeld) && !vervang) throw new Error(`${naam}.webp bestaat al. Gebruik --vervang als dat de bedoeling is.`);
  await sharp({ create: { width: db, height: dh, channels: 4, background: { r: 0, g: 0, b: 0, alpha: 0 } } })
    .composite([{ input: geschaald, left: links, top: boven }])
    .webp({ quality: 86, alphaQuality: 90 }).toFile(doelBeeld);

  fs.writeFileSync(path.join(naar, `${naam}.json`), JSON.stringify({
    afspraak: 'uitsnede bijgesneden op de alfa-omhullende, daarna onderaan uitgelijnd en gecentreerd op een vast doek',
    doek: { breedte: db, hoogte: dh },
    marges: { onder, zij },
    opmerking: 'Geen waarden per beeld: elke uitsnede uit deze route heeft dezelfde meetkunde.',
  }, null, 2) + '\n');

  const kb = Math.round(fs.statSync(doelBeeld).size / 1024);
  console.log(`${path.basename(doelBeeld).padEnd(34)} ${db}x${dh}  ${kb} KB  (onderwerp ${nb}x${nh}, onderaan uitgelijnd)`);
})().catch(error => { console.error(error.message); process.exitCode = 1; });
