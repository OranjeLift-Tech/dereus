// Klantenservicebeeld: de medewerker los van de achtergrond, voor de bovenlaag van het homecontact-blok
// en voor de staande zijkolom van de formulieren.
// Stap 2 van 3 in de route, net als contact-uitsnede.mjs. Bewust ZONDER sharp in dit proces:
// de achtergrondverwijderaar brengt zijn eigen beeldbibliotheek mee en die botst met de sharp uit de cache.
//
//   node _ai-beelden/klantenservice-uitsnede.mjs <bron.jpg> [doel.png]
//
// Zonder doel komt het bestand naast de bron te staan, met -uit.png erachter.
// De uitsnede houdt exact de afmeting van de bron, zodat hij in export-klantenservice.cjs
// precies over de achtergrondlaag valt. Snijd hem dus niet zelf bij.
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { removeBackground } from '@imgly/background-removal-node';

const bron = process.argv[2];
if (!bron || !fs.existsSync(bron)) {
  console.error('Geef een bestaande bronafbeelding op.');
  process.exit(1);
}
const doel = process.argv[3] || path.join(path.dirname(bron), path.basename(bron, path.extname(bron)) + '-uit.png');

const blob = await removeBackground(pathToFileURL(path.resolve(bron)).href, {
  model: 'medium',
  output: { format: 'image/png' },
});
fs.mkdirSync(path.dirname(doel), { recursive: true });
fs.writeFileSync(doel, Buffer.from(await blob.arrayBuffer()));
console.log('OK', doel);
