// node knip.mjs bron/a.jpg ... -> uit/<naam>-vrij.png (achtergrond weg, zelfde maat)
import { removeBackground } from '@imgly/background-removal-node';
import sharp from 'sharp';
import fs from 'fs';
import path from 'path';
fs.mkdirSync('uit', { recursive: true });
for (const f of process.argv.slice(2)) {
  const png = await sharp(f).png().toBuffer();
  const blob = await removeBackground(new Blob([png], { type: 'image/png' }), { model: 'medium', output: { format: 'image/png' } });
  const naam = path.basename(f).replace(/\.\w+$/, '');
  fs.writeFileSync(`uit/${naam}-vrij.png`, Buffer.from(await blob.arrayBuffer()));
  console.log('klaar', naam);
}
