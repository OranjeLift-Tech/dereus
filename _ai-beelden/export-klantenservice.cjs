/* Exporteert een gekozen beeld naar de formaten die de blokken echt vragen.
   Stap 3 van 3 in de route: kleding-logo, dan uitsnede, dan dit.
   De naam van dit bestand is inmiddels te smal: het bedient ook het huisvenster van /over-ons/.

   node _ai-beelden/export-klantenservice.cjs <bron.jpg> [--uit <uitsnede.png>] [opties]

   Opties
     --vorm <naam>    welk slot je vult, standaard homecontact. Zie VORMEN hieronder.
     --naar <map>     doelmap, standaard _ai-beelden/foto/klantenservice-proef (tijdelijk)
     --naam <naam>    basisnaam van de bestanden, standaard de naam van de bron
     --x <0..1>       horizontaal zwaartepunt van de uitsnijding, standaard 0.5
     --y <0..1>       verticaal zwaartepunt, standaard 0.5. Lager getal is hoger in beeld.
     --vullend        laat de staande variant het vlak vullen in plaats van passen.
                      Gebruik dit bij een staand figuur; bij een zittend figuur juist niet.
     --vervang        sta toe dat een bestaand bestand wordt overschreven

   --vorm homecontact (standaard), drie bestanden, afgelezen van de blokken, niet zelf bedacht:
     <naam>.webp        1200x800, zonder alfa, voor homecontact__achter (homecontact.py)
     <naam>-uit.webp    1200x800, met alfa,    voor homecontact__uit, exact over de achtergrond
     <naam>-staand.webp  640x954, met alfa,    voor b-formulier__beeld (formulier.py, _zijkolom)
   Hiervoor is --uit verplicht: de achtergrond en de uitsnede krijgen dezelfde uitsnijding, anders
   schuiven de twee lagen over elkaar heen. Daarom rekent snijvlak() de rechthoek een keer uit.

   --vorm huis, een bestand plus een proef:
     <naam>.webp             1200x1140, zonder alfa, voor .huisvenster in over-ons.py (TEAM_BEELD)
     <naam>-maskerproef.png  hetzelfde beeld door het huismasker, alleen om te controleren
   Hier is geen uitsnede nodig: het blok zet er een gewoon beeld in met object-fit cover, zonder
   tweede laag. De maskerproef hoort niet op de site, die is om te zien wat er wegvalt.
*/
const fs = require('node:fs');
const path = require('node:path');
const sharp = require(process.env.SHARP_MODULE || 'C:/Users/arnas/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');

const root = path.resolve(__dirname, '..');
const argv = process.argv.slice(2);
const vlag = (naam, standaard) => {
  const i = argv.indexOf('--' + naam);
  return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : standaard;
};
const bron = argv[0] && !argv[0].startsWith('--') ? argv[0] : null;
const uitsnede = vlag('uit');
const naar = path.resolve(root, vlag('naar', '_ai-beelden/foto/klantenservice-proef'));
const naam = vlag('naam', bron ? path.basename(bron, path.extname(bron)) : '');
const zwaartepunt = { x: Number(vlag('x', '0.5')), y: Number(vlag('y', '0.5')) };
const vervang = argv.includes('--vervang');
const vullend = argv.includes('--vullend');

const STAAND = { breedte: 640, hoogte: 954 };   // formulierzijkolom, staand
const VORMEN = {
  homecontact: { breedte: 1200, hoogte: 800, uitsnede: true, staand: true },
  huis: { breedte: 1200, hoogte: 1140, uitsnede: false, staand: false, masker: true },
};
const vorm = VORMEN[vlag('vorm', 'homecontact')];

// Het huismasker uit css/style.css (--huisvlak), viewBox 535.3 bij 509.8. Zelfde punten als in
// beeld-opties/over-ons-20260921/_bron/genereer.py, zodat de proef hier hetzelfde toont als daar.
const HUIS = 'M267.6 7.8L320.9 53.2V0H356.8V83.9L535.3 236.2H457.6V509.8H77.7V236.2H0Z';
const HUIS_VIEWBOX = [535.3, 509.8];

// De rechthoek die van een bron van w bij h een 3:2 beeld maakt, met het zwaartepunt als schuifknop.
function snijvlak(w, h, doelverhouding) {
  let bw = w, bh = Math.round(w / doelverhouding);
  if (bh > h) { bh = h; bw = Math.round(h * doelverhouding); }
  const links = Math.round((w - bw) * Math.min(1, Math.max(0, zwaartepunt.x)));
  const boven = Math.round((h - bh) * Math.min(1, Math.max(0, zwaartepunt.y)));
  return { left: links, top: boven, width: bw, height: bh };
}

async function schrijf(pijp, bestand, opties) {
  const doel = path.join(naar, bestand);
  if (fs.existsSync(doel) && !vervang) throw new Error(`${bestand} bestaat al. Gebruik --vervang als dat de bedoeling is.`);
  const info = await pijp.webp(opties).toFile(doel);
  const kb = Math.round(fs.statSync(doel).size / 1024);
  const grens = kb > 250 ? '  BOVEN DE 250 KB' : '';
  console.log(`${bestand.padEnd(34)} ${info.width}x${info.height}  ${String(kb).padStart(3)} KB${grens}`);
  return kb;
}

(async () => {
  if (!vorm) throw new Error(`Onbekende --vorm. Kies uit: ${Object.keys(VORMEN).join(', ')}.`);
  if (!bron || !fs.existsSync(bron)) throw new Error('Geef een bestaande bronafbeelding op.');
  if (vorm.uitsnede && !uitsnede) throw new Error('Geef met --uit de uitsnede op, gemaakt met klantenservice-uitsnede.mjs.');
  if (uitsnede && !fs.existsSync(uitsnede)) throw new Error(`De uitsnede ${uitsnede} bestaat niet.`);
  const bm = await sharp(bron).metadata();
  if (uitsnede) {
    const um = await sharp(uitsnede).metadata();
    if (!um.hasAlpha) throw new Error('De uitsnede mist een alfakanaal.');
    if (bm.width !== um.width || bm.height !== um.height) {
      throw new Error(`Bron (${bm.width}x${bm.height}) en uitsnede (${um.width}x${um.height}) zijn niet even groot; dan vallen de lagen niet samen.`);
    }
  }
  fs.mkdirSync(naar, { recursive: true });
  const vak = snijvlak(bm.width, bm.height, vorm.breedte / vorm.hoogte);

  // 1. het hoofdbeeld, zonder alfa
  await schrijf(
    sharp(bron).extract(vak).resize(vorm.breedte, vorm.hoogte).flatten({ background: '#ffffff' }),
    `${naam}.webp`, { quality: 82 });

  // 2. bovenlaag: dezelfde uitsnijding, zodat de persoon exact over de achtergrond valt
  if (vorm.uitsnede) {
    await schrijf(
      sharp(uitsnede).extract(vak).resize(vorm.breedte, vorm.hoogte),
      `${naam}-uit.webp`, { quality: 86, alphaQuality: 90 });
  }

  // 2b. proef door het huismasker, zodat te zien is wat de dakdriehoek en de zijkanten wegnemen
  if (vorm.masker) {
    const schaal = [vorm.breedte / HUIS_VIEWBOX[0], vorm.hoogte / HUIS_VIEWBOX[1]];
    const masker = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${vorm.breedte}" height="${vorm.hoogte}">
      <path d="${HUIS}" fill="white" transform="scale(${schaal[0]} ${schaal[1]})"/></svg>`);
    const proef = path.join(naar, `${naam}-maskerproef.png`);
    await sharp(bron).extract(vak).resize(vorm.breedte, vorm.hoogte).ensureAlpha()
      .composite([{ input: await sharp(masker).png().toBuffer(), blend: 'dest-in' }])
      .flatten({ background: '#F6F7F9' })                        // Mist eronder, zodat de huisvorm meteen leest
      .png().toFile(proef);
    console.log(`${(naam + '-maskerproef.png').padEnd(34)} ${vorm.breedte}x${vorm.hoogte}  proef, hoort niet op de site`);
  }

  // 3. staande zijkolom: bijgesneden tot de persoon, onderaan uitgelijnd zoals de CSS hem toont
  //    (.b-formulier__beeld heeft object-fit:contain en object-position:center bottom)
  //    Een staand figuur vult het staande vlak met --vullend; een zittend figuur is breder dan hoog
  //    en houdt met de standaard lege ruimte boven zich, wat daar juist klopt.
  if (vorm.staand) {
    const bijgesneden = await sharp(uitsnede).trim({ threshold: 1 }).png().toBuffer();
    const staandVak = vullend
      ? { fit: 'cover', position: sharp.strategy.entropy }
      : { fit: 'contain', position: 'bottom', background: { r: 0, g: 0, b: 0, alpha: 0 } };
    await schrijf(
      sharp(bijgesneden).resize({ width: STAAND.breedte, height: STAAND.hoogte, ...staandVak }),
      `${naam}-staand.webp`, { quality: 86, alphaQuality: 90 });
  }

  console.log(`\nKlaar in ${path.relative(root, naar)}. Uitsnijding: ${vak.width}x${vak.height} vanaf ${vak.left},${vak.top}.`);
})().catch(error => { console.error(error.message); process.exitCode = 1; });
