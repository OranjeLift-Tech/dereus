// Trede 3: de verhuizer met dozen los van de achtergrond. Stap 1 van 2, bewust ZONDER sharp
// (de achtergrondverwijderaar brengt zijn eigen beeldbibliotheek mee, zie diensten-uitsnede.mjs).
//   1. dit script        -> foto/treden/dozen-uit.png (met transparantie)
//   2. treden-export.cjs -> ../img/treden/dozen.webp
// Bron: foto/treden/dozen.png, gemaakt met PROMPTS-treden-dozen.txt.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { removeBackground } from '@imgly/background-removal-node';

const HIER = path.dirname(fileURLToPath(import.meta.url));
const MAP = path.join(HIER, 'foto', 'treden');
const bron = ['dozen.png', 'dozen.jpg', 'dozen.jpeg', 'dozen.webp']
  .map(n => path.join(MAP, n)).find(p => fs.existsSync(p));

if (!bron) {
  console.error('Geen bronbeeld gevonden. Verwacht: ' + path.join(MAP, 'dozen.png'));
  console.error('Maak het eerst in de Gemini-app met PROMPTS-treden-dozen.txt.');
  process.exit(1);
}

const blob = await removeBackground(pathToFileURL(bron).href, { model: 'medium', output: { format: 'image/png' } });
const doel = path.join(MAP, 'dozen-uit.png');
fs.writeFileSync(doel, Buffer.from(await blob.arrayBuffer()));
console.log('OK ' + path.relative(HIER, doel) + '  (nu: node treden-export.cjs)');
