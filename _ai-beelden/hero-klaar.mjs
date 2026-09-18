// Echte verhuizer voor de hero: groen weg -> ../img/reus-echt.webp (760 breed, zelfde maat als de getekende Reus)
//   node hero-klaar.mjs                 pakt foto/hero-reus-echt.*
//   node hero-klaar.mjs "C:\pad\naar\Gemini_Generated_Image_x.png"   pakt een gedownload bestand
import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
import { groenWeg } from './groen-weg.mjs';
const HIER = path.dirname(fileURLToPath(import.meta.url));
const bron = process.argv[2] ||
  ['png', 'jpg', 'jpeg', 'webp'].map(e => path.join(HIER, 'foto', `hero-reus-echt.${e}`)).find(fs.existsSync);
if (!bron || !fs.existsSync(bron)) { console.log('Geen bronfoto. Geef een pad mee, of zet hem in foto/hero-reus-echt.png'); process.exit(1); }
const uit = path.join(HIER, '..', 'img', 'reus-echt.webp');
const info = await (await groenWeg(bron)).resize({ width: 760, withoutEnlargement: true }).webp({ quality: 88, alphaQuality: 92 }).toFile(uit);
console.log(`OK img/reus-echt.webp ${info.width}x${info.height}`);
