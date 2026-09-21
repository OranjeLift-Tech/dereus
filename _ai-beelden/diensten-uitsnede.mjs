// Diensten: de mensen los van de achtergrond, voor het "uit de foto stappen"-effect op de home.
// Stap 1 van 2. Bewust ZONDER sharp: de achtergrondverwijderaar brengt zijn eigen beeldbibliotheek mee.
//   1. dit script            -> foto/Onze diensten/uitsnede/<dienst>.png (met transparantie)
//   2. diensten-uit-export.cjs -> ../img/dienst-<dienst>-uit.webp
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { removeBackground } from '@imgly/background-removal-node';

const HIER = path.dirname(fileURLToPath(import.meta.url));
const BRON = path.join(HIER, 'foto', 'Onze diensten');
const UIT = path.join(BRON, 'uitsnede');

// bestand in "Onze diensten" -> naam van de dienstfoto in /img
const KAART = {
  'Particuliere verhuizingen.jpg': 'particulier',
  'Zakelijke verhuizingen.jpg': 'zakelijk',
  'Nationale verhuizingen.jpg': 'nationaal',
  'Internationale verhuizing.jpg': 'internationaal',
  'Verhuisliftservice.jpg': 'verhuislift',
  'Tijdelijke opslag.jpg': 'opslag',
  'Handymanservice.webp': 'handyman',
  'Woningontruiming.png': 'woningontruiming',
};

fs.mkdirSync(UIT, { recursive: true });
for (const [bestand, naam] of Object.entries(KAART)) {
  const doel = path.join(UIT, `${naam}.png`);
  if (fs.existsSync(doel)) { console.log(`- ${naam} bestaat al`); continue; }
  const t = Date.now();
  const blob = await removeBackground(pathToFileURL(path.join(BRON, bestand)).href, {
    model: 'medium',
    output: { format: 'image/png' },
  });
  fs.writeFileSync(doel, Buffer.from(await blob.arrayBuffer()));
  console.log(`OK ${naam}.png  (${((Date.now() - t) / 1000).toFixed(0)}s)`);
}
