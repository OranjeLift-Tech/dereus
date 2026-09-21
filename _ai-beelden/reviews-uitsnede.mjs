// Reviews: de drie klantportretten los van de achtergrond. Stap 1 van 2, bewust ZONDER sharp (zie diensten-uitsnede.mjs).
//   1. dit script          -> foto/reviews/klant-<n>-uit.png (met transparantie)
//   2. reviews-export.cjs  -> ../img/review-klant-<n>.webp
// Bron: foto/reviews/klant-1..3.(png|jpg|jpeg|webp), gemaakt met PROMPTS-reviews-klanten.txt.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { removeBackground } from '@imgly/background-removal-node';

const HIER = path.dirname(fileURLToPath(import.meta.url));
const MAP = path.join(HIER, 'foto', 'reviews');

for (const n of [1, 2, 3]) {
  const bron = ['png', 'jpg', 'jpeg', 'webp'].map(e => path.join(MAP, `klant-${n}.${e}`)).find(p => fs.existsSync(p));
  if (!bron) { console.log(`- klant-${n}: geen bronbestand in foto/reviews/`); continue; }
  const doel = path.join(MAP, `klant-${n}-uit.png`);
  if (fs.existsSync(doel) && fs.statSync(doel).mtimeMs > fs.statSync(bron).mtimeMs) { console.log(`- klant-${n} bestaat al`); continue; }
  const t = Date.now();
  const blob = await removeBackground(pathToFileURL(bron).href, { model: 'medium', output: { format: 'image/png' } });
  fs.writeFileSync(doel, Buffer.from(await blob.arrayBuffer()));
  console.log(`OK klant-${n}-uit.png  (${((Date.now() - t) / 1000).toFixed(0)}s)`);
}
