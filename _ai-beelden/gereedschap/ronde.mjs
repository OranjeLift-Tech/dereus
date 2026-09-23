// Eén commando dat een complete beeldronde opzet: map, N versies parallel, en de reviewpagina.
//
//   node _ai-beelden/gereedschap/ronde.mjs <ronde.json>           hele ronde
//   node _ai-beelden/gereedschap/ronde.mjs <ronde.json> 2 4       alleen versie 2 en 4 opnieuw
//   node _ai-beelden/gereedschap/ronde.mjs <ronde.json> --pagina  alleen de pagina herbouwen
//   node _ai-beelden/gereedschap/ronde.mjs <ronde.json> --prompts alleen prompts.md schrijven
//
// De ronde staat in één json-bestand. Minimaal:
//
//   {
//     "naam": "drie-verhuizers-doos",
//     "titel": "Drie verhuizers met een doos",
//     "ratio": "1:1",
//     "cast": ["mannen/man-18.png", "mannen/man-01.png"],
//     "versies": [
//       { "nr": 1, "naam": "Bank de stoep af", "scene": "Two movers carry a sofa ..." }
//     ]
//   }
//
// Optioneel: "lead", "datum", "eenheid" (Versie of Kandidaat), "grootte" (2K), "extra" (regels die
// achter de merkregels aan gaan), "lagen" en "crop" voor de pagina.
//
// Twee dingen zitten ingebakken en staan niet per ronde in het json-bestand:
//   1. Het merk gaat nooit in het prompt. Zie gereedschap/gemini.mjs, MERK.
//   2. Alle versies van één ronde krijgen dezelfde cast referentiegezichten, want er overleeft er
//      maar één. Wisselende gezichten maken de keuze een keuze tussen mensen in plaats van beelden.
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { MERK, STIJL, MODEL, personenRegel, laadCast, genereer, parallel } from './gemini.mjs';

const HIER = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HIER, '..', '..');

function vandaag() {
  const d = new Date();
  return `${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, '0')}${String(d.getDate()).padStart(2, '0')}`;
}

export function promptVan(ronde, v) {
  const delen = [MERK];
  if (ronde.extra) delen.push(ronde.extra.trim());
  if (v.extra) delen.push(v.extra.trim());
  if (ronde.cast?.length) delen.push(personenRegel(ronde.cast.length));
  delen.push(`SCENE: ${v.scene.trim()}`);
  delen.push(STIJL(ronde.ratio || '3:2'));
  return delen.join('\n\n');
}

function prompts(ronde, map_) {
  const kop = `# Prompts ${ronde.titel}\n\n` +
    `Model: ${MODEL} (nano banana pro), beeldverhouding ${ronde.ratio || '3:2'}, imageSize ${ronde.grootte || '2K'}.\n` +
    (ronde.cast?.length
      ? `Per versie gaan dezelfde ${ronde.cast.length} referentiegezichten mee als inline_data delen, in deze volgorde:\n` +
        ronde.cast.map((c, i) => `${i + 1}. \`${c}\``).join('\n') + '\n\n' +
        `Ze komen uit \`~/.claude/skills/foto-verbeteren/assets/gezichten/\`, op wit gezet en naar 512 px op de\n` +
        `langste zijde geschaald, verder onbewerkt. Dezelfde cast in alle versies, want er overleeft er maar een.\n\n`
      : 'Geen referentiegezichten in deze ronde.\n\n') +
    `Geen logo-referentie en geen merk in het prompt: het model tekent het merk na in plaats van het te\n` +
    `plaatsen. Het echte beeldmerk komt er naderhand met sharp op (gereedschap/merk-op-doos.py).\n\n` +
    `## Vaste merkregels\n\n\`\`\`\n${MERK}\n\`\`\`\n\n`;
  const blokken = ronde.versies.map((v) =>
    `## Versie ${v.nr}${v.naam ? `: ${v.naam}` : ''}\n\nVolledig prompt:\n\n\`\`\`\n${promptVan(ronde, v)}\n\`\`\`\n`,
  ).join('\n');
  fs.writeFileSync(path.join(map_, 'prompts.md'), kop + blokken, 'utf8');
}

function pagina(ronde, map_) {
  const args = [
    path.join(HIER, 'rondepagina.py'), map_,
    '--titel', ronde.titel,
    // De nummers uit het rondebestand zelf, niet 1..N: een vervolgronde met alleen 2, 4 en 5
    // houdt die nummers, zodat de gebruiker zijn eigen keuze terugziet.
    '--nrs', ronde.versies.map((v) => v.nr).join(','),
    '--eenheid', ronde.eenheid || 'Versie',
    '--verhouding', (ronde.ratio || '3:2').replace(':', '/'),
  ];
  if (ronde.lead) args.push('--lead', ronde.lead);
  if (ronde.lagen) args.push('--lagen', JSON.stringify(ronde.lagen));
  if (ronde.crop) args.push('--crop', JSON.stringify(ronde.crop));
  return execFileSync('python', args, { encoding: 'utf8' }).trim();
}

async function main() {
  const args = process.argv.slice(2);
  const bestand = args.find((a) => !a.startsWith('--') && a.endsWith('.json'));
  if (!bestand) {
    console.error('Gebruik: node _ai-beelden/gereedschap/ronde.mjs <ronde.json> [nr ...] [--pagina] [--prompts]');
    process.exit(1);
  }
  const ronde = JSON.parse(fs.readFileSync(bestand, 'utf8'));
  for (const veld of ['naam', 'titel', 'versies']) {
    if (!ronde[veld]) { console.error(`ronde.json mist "${veld}"`); process.exit(1); }
  }
  const datum = ronde.datum || vandaag();
  const map_ = path.join(ROOT, 'website', 'review', `${ronde.naam}-${datum}`);
  fs.mkdirSync(map_, { recursive: true });

  const alleenPagina = args.includes('--pagina');
  const alleenPrompts = args.includes('--prompts');
  const nrs = args.filter((a) => /^\d+$/.test(a)).map(Number);

  if (!alleenPagina) prompts(ronde, map_);
  if (alleenPrompts) { console.log(path.join(map_, 'prompts.md')); return; }

  if (!alleenPagina) {
    // De cast één keer laden en aan elke versie meegeven: zelfde gezichten in alle versies.
    const cast = ronde.cast?.length ? await laadCast(ronde.cast) : [];
    const welke = nrs.length ? ronde.versies.filter((v) => nrs.includes(v.nr)) : ronde.versies;
    const start = Date.now();
    const uit = await parallel(welke, (v) => genereer({
      naam: `versie-${v.nr}`,
      prompt: promptVan(ronde, v),
      cast,
      ratio: ronde.ratio || '3:2',
      grootte: ronde.grootte || '2K',
      doel: path.join(map_, `versie-${v.nr}.png`),
    }));
    const gelukt = uit.filter((r) => r.ok).length;
    console.log(`${gelukt} van de ${welke.length} beelden in ${((Date.now() - start) / 1000).toFixed(0)} s`);
    for (const r of uit.filter((x) => !x.ok)) console.log(`  mislukt: ${r.naam} (${r.fout})`);
  }

  const index = pagina(ronde, map_);
  // Eén regel met het pad, zodat een sessie dat meteen aan de gebruiker kan geven.
  console.log(index);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  await main();
}
