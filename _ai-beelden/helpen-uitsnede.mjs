// Achtergrond weg bij helpen-wij-u-snel.jpg: lokaal model, geen key.
// Stap 2 van 3.  1. sharp -> foto/helpen-bron.png   2. dit script -> foto/helpen-uit.png   3. sharp -> ../img/helpen-wij-u-snel.webp
import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath, pathToFileURL } from 'node:url';
import { removeBackground } from '@imgly/background-removal-node';
const HIER = path.dirname(fileURLToPath(import.meta.url));
const png = path.join(HIER, 'foto', 'helpen-bron.png');
const blob = await removeBackground(pathToFileURL(png).href, { model: 'medium', output: { format: 'image/png' } });
fs.writeFileSync(path.join(HIER, 'foto', 'helpen-uit.png'), Buffer.from(await blob.arrayBuffer()));
console.log('OK foto/helpen-uit.png');
