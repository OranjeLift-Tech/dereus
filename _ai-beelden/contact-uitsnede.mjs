// Contactfoto: medewerker los van de achtergrond (lokaal model, geen key) voor het "uit het scherm"-effect.
// Stap 2 van 3. Bewust ZONDER sharp in dit proces: de achtergrondverwijderaar brengt zijn eigen beeldbibliotheek mee.
//   1. node -e "sharp(...)" maakt foto/contact-bron.png     2. dit script -> foto/contact-uit.png     3. sharp -> ../img/contact-uit.webp
import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath, pathToFileURL } from 'node:url';
import { removeBackground } from '@imgly/background-removal-node';
const HIER = path.dirname(fileURLToPath(import.meta.url));
const png = path.join(HIER, 'foto', 'contact-bron.png');
const blob = await removeBackground(pathToFileURL(png).href, { model: 'medium', output: { format: 'image/png' } });
fs.writeFileSync(path.join(HIER, 'foto', 'contact-uit.png'), Buffer.from(await blob.arrayBuffer()));
console.log('OK foto/contact-uit.png');
