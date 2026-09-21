// Zet het echte De Reus-beeldmerk op de kleding van een gegenereerde kandidaat.
// Zusje van kleding-logo.mjs. Dat script maakt van een borstzakje een wit logovlak; dat hoort bij de drie
// bestaande sitefoto's. Een gegenereerde kandidaat heeft geen zakje maar een geborduurd embleem dat het
// beeldmodel zelf verzonnen heeft, meestal met een losse hand in plaats van de twee armen en met eigen letters.
// Hier dekken we dat embleem af met de stof eromheen en zetten we het echte beeldmerk terug.
//
// Het beeldmerk (witte armen, geel huis, geen tekst) is volgens brandbook/assets/logo-v2/README.md
// het merk voor de polo. Geen woordmerk: op borstformaat is dat toch onleesbaar en dan verzint het model letters.
//
//   node _ai-beelden/kleding-logo-kandidaat.mjs <bron> --vak x,y,b,h [opties]
//
//   --vak x,y,b,h     het gebied van het oude embleem in bronpixels, dit wordt afgedekt
//   --logo x,y,b      linkerbovenhoek en breedte van het nieuwe beeldmerk, standaard gecentreerd in het vak
//   --merk <soort>    negatief (standaard, witte armen, voor blauwe kleding) of vol (voor lichte vlakken)
//   --hoek <graden>   kanteling van het beeldmerk, standaard 0
//   --uit <pad>       doelbestand, standaard naast de bron met -logo erachter
//
// De coordinaten moeten per foto gemeten worden, net als de hoekpunten in kleding-logo.mjs.
// Er bestaat geen betrouwbare automatische vinder voor een borstembleem.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const sharp = require(process.env.SHARP_MODULE || 'C:/Users/arnas/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');

const argv = process.argv.slice(2);
const vlag = (naam, standaard) => {
  const i = argv.indexOf('--' + naam);
  return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : standaard;
};
const bron = argv[0] && !argv[0].startsWith('--') ? argv[0] : null;
const vak = (vlag('vak') || '').split(',').map(Number);
const hoek = Number(vlag('hoek', '0'));
const uit = vlag('uit', bron ? path.join(path.dirname(bron), path.basename(bron, path.extname(bron)) + '-logo.png') : '');

// negatief (witte armen, geel huis) hoort op koningsblauw, dus op de polo. Op een witte bus of een
// lichte ondergrond verdwijnen die witte armen en heb je de gewone versie nodig.
const MERKEN = { negatief: 'dereus-beeldmerk-negatief.png', vol: 'dereus-beeldmerk.png' };
const MERK = 'brandbook/assets/logo-v2/' + (MERKEN[process.argv.includes('--merk') ? process.argv[process.argv.indexOf('--merk') + 1] : 'negatief'] || MERKEN.negatief);
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname.slice(1)), '..');

// Gemiddelde kleur van een strook, gebruikt om de stof rond het embleem te bemonsteren.
async function kleur(beeld, links, boven, breedte, hoogte) {
  const { data } = await sharp(beeld).extract({ left: Math.round(links), top: Math.round(boven), width: Math.round(breedte), height: Math.round(hoogte) })
    .removeAlpha().raw().toBuffer({ resolveWithObject: true });
  let r = 0, g = 0, b = 0;
  for (let i = 0; i < data.length; i += 3) { r += data[i]; g += data[i + 1]; b += data[i + 2]; }
  const n = data.length / 3;
  return [r / n, g / n, b / n].map(v => Math.round(v));
}

if (!bron || !fs.existsSync(bron)) { console.error('Geef een bestaande bronafbeelding op.'); process.exit(1); }
if (vak.length !== 4 || vak.some(Number.isNaN)) { console.error('Geef --vak als x,y,breedte,hoogte in bronpixels.'); process.exit(1); }

const [vx, vy, vb, vh] = vak;
const meta = await sharp(bron).metadata();
const rand = Math.max(6, Math.round(Math.min(vb, vh) * 0.12));

// De stof rond het embleem, als peiling voor wat "gewone stof" is op deze plek.
const stof = await kleur(bron, vx, Math.max(0, vy - rand), vb, rand);

// Het embleem uit de stof halen in plaats van er een vlak overheen leggen: alleen de gele en witte
// pixels gaan weg, de rest van de stof met zijn weefsel en licht blijft staan. Daarna een lichte vervaging,
// zodat de weggehaalde plek niet als een vlek opvalt.
async function stofZonderEmbleem() {
  const { data, info } = await sharp(bron)
    .extract({ left: vx, top: vy, width: vb, height: vh }).removeAlpha().raw().toBuffer({ resolveWithObject: true });
  // Niet op geel of wit toetsen maar op afstand tot de stofkleur: de randen van het borduursel zijn
  // mengkleuren, en juist die bleven anders als een schim van het oude embleem staan.
  const drempel = Number(vlag('drempel', '38'));
  const raak = new Uint8Array(vb * vh);
  for (let p = 0; p < raak.length; p++) {
    const i = p * 3;
    const d = Math.hypot(data[i] - stof[0], data[i + 1] - stof[1], data[i + 2] - stof[2]);
    if (d > drempel) raak[p] = 1;
  }
  // Iets uitdijen, zodat de laatste halo om de letters ook meegaat.
  const straal = Math.max(2, Math.round(vb / 40));
  const wijd = new Uint8Array(raak);
  for (let y = 0; y < vh; y++) {
    for (let x = 0; x < vb; x++) {
      if (raak[y * vb + x]) continue;
      zoek: for (let dy = -straal; dy <= straal; dy++) {
        const ny = y + dy;
        if (ny < 0 || ny >= vh) continue;
        for (let dx = -straal; dx <= straal; dx++) {
          const nx = x + dx;
          if (nx >= 0 && nx < vb && raak[ny * vb + nx]) { wijd[y * vb + x] = 1; break zoek; }
        }
      }
    }
  }
  // Vullen met een enkele stofkleur gaf een donkere schim in de vorm van het oude embleem: de stof is
  // niet overal even licht. Daarom hier een verloop dat uit de vier randen van het vak komt, want die
  // randen zijn schone stof. Per kanaal een menging van de rand boven, onder, links en rechts.
  const rijkleur = (langs, vast, horizontaal) => {
    const som = [0, 0, 0];
    let n = 0;
    for (let k = 0; k < langs; k++) {
      const x = horizontaal ? k : vast, y = horizontaal ? vast : k;
      if (wijd[y * vb + x]) continue;
      const i = (y * vb + x) * 3;
      som[0] += data[i]; som[1] += data[i + 1]; som[2] += data[i + 2]; n++;
    }
    return n ? som.map(v => v / n) : stof.slice();
  };
  const boven = [], onder = [], links = [], rechts = [];
  for (let x = 0; x < vb; x++) {
    boven.push(rijkleur(vh, x, false).slice());                       // hele kolom, schone pixels tellen mee
    onder.push(boven[x]);
  }
  for (let y = 0; y < vh; y++) {
    links.push(rijkleur(vb, y, true).slice());
    rechts.push(links[y]);
  }
  for (let y = 0; y < vh; y++) {
    const ty = vh > 1 ? y / (vh - 1) : 0;
    for (let x = 0; x < vb; x++) {
      const p = y * vb + x;
      if (!wijd[p]) continue;
      const tx = vb > 1 ? x / (vb - 1) : 0;
      const i = p * 3;
      for (let c = 0; c < 3; c++) {
        const verticaal = (1 - ty) * boven[x][c] + ty * onder[x][c];
        const zijwaarts = (1 - tx) * links[y][c] + tx * rechts[y][c];
        data[i + c] = Math.round((verticaal + zijwaarts) / 2);
      }
    }
  }
  return sharp(data, { raw: info }).blur(Math.max(1.6, vb / 70)).png().toBuffer();
}
const schoon = await stofZonderEmbleem();

// Het nieuwe beeldmerk: standaard gecentreerd in het vak, op 92 procent van de vakbreedte.
const opgegeven = (vlag('logo') || '').split(',').map(Number);
const lb = opgegeven.length === 3 && !opgegeven.some(Number.isNaN) ? opgegeven[2] : Math.round(vb * 0.92);
const merkMeta = await sharp(path.join(root, MERK)).metadata();
const lh = Math.round(lb * merkMeta.height / merkMeta.width);
const lx = opgegeven.length === 3 ? opgegeven[0] : Math.round(vx + (vb - lb) / 2);
const ly = opgegeven.length === 3 ? opgegeven[1] : Math.round(vy + (vh - lh) / 2);
const merk = await sharp(path.join(root, MERK)).resize({ width: lb }).rotate(hoek, { background: { r: 0, g: 0, b: 0, alpha: 0 } }).toBuffer();
const merkNu = await sharp(merk).metadata();

// De schoongemaakte stof gaat met een verzachte rand terug op zijn eigen plek, zodat er geen
// zichtbare rechthoek op het shirt ontstaat.
const masker = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${vb}" height="${vh}">
  <defs><filter id="zacht"><feGaussianBlur stdDeviation="${(rand / 2.5).toFixed(1)}"/></filter></defs>
  <rect x="${rand}" y="${rand}" width="${vb - rand * 2}" height="${vh - rand * 2}" rx="${Math.round(Math.min(vb, vh) / 4)}" fill="white" filter="url(#zacht)"/>
</svg>`);
const dekvlak = await sharp(schoon).ensureAlpha()
  .composite([{ input: await sharp(masker).png().toBuffer(), blend: 'dest-in' }]).png().toBuffer();
const dek = { input: dekvlak, left: vx, top: vy };

const merklaag = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${meta.width}" height="${meta.height}">
  <image xlink:href="data:image/png;base64,${merk.toString('base64')}" x="${lx}" y="${ly}" width="${merkNu.width}" height="${merkNu.height}"/>
</svg>`);

// Dezelfde lichte verzachting als in kleding-logo.mjs, anders steekt het vector scherp af tegen de foto.
const zachtMerk = await sharp(merklaag).blur(0.45).png().toBuffer();
const info = await sharp(bron).composite([dek, { input: zachtMerk }]).png().toFile(uit);
console.log('OK', uit, `${info.width}x${info.height}`);
console.log(`Vak ${vx},${vy} ${vb}x${vh} afgedekt. Beeldmerk ${merkNu.width}x${merkNu.height} op ${lx},${ly}${hoek ? `, ${hoek} graden` : ''}.`);
