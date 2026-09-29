// node vrij.mjs in/a.png ... -> uit/a.png (alleen imgly, geen sharp in hetzelfde proces)
import { removeBackground } from '@imgly/background-removal-node';
import fs from 'fs';
import path from 'path';
for (const f of process.argv.slice(2)) {
  const blob = await removeBackground(new Blob([fs.readFileSync(f)], { type: 'image/png' }), { model: 'medium', output: { format: 'image/png' } });
  fs.writeFileSync('uit/' + path.basename(f), Buffer.from(await blob.arrayBuffer()));
  console.log('klaar', f);
}
