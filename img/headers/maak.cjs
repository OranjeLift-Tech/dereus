const fs = require('node:fs');
const path = require('node:path');
const sharp = require('C:/Users/arnas/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root = path.resolve(__dirname, '../..');
const sources = require('./bronnen.json');
(async () => {
  const manifest = {};
  for (const item of sources) {
    const source = path.join(root, item.source);
    if (item.kind === 'map') {
      const destination = path.join(__dirname, item.name + '.svg');
      fs.copyFileSync(source, destination);
      const meta = await sharp(destination).metadata();
      manifest[item.route] = { src: '/img/headers/' + item.name + '.svg', width: meta.width, height: meta.height, position: '50% 50%' };
      continue;
    }
    const meta = await sharp(source).metadata();
    const width = Math.min(1600, meta.width);
    const height = Math.round(width * 9 / 16);
    const destination = path.join(__dirname, item.name + '.webp');
    let pipeline = sharp(source).resize(width, height, { fit: 'cover', position: item.name === 'contact' || item.name === 'contact-bedankt' ? 'north' : 'centre', withoutEnlargement: true });
    if (item.kind === 'existing-soft') pipeline = pipeline.blur(.5);
    await pipeline.webp({ quality: 84, effort: 6 }).toFile(destination);
    const output = await sharp(destination).metadata();
    manifest[item.route] = { src: '/img/headers/' + item.name + '.webp', width: output.width, height: output.height, position: '50% 50%' };
  }
  fs.writeFileSync(path.join(__dirname, 'manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
  console.log(Object.keys(manifest).length + ' unique route backgrounds saved.');
  console.log(JSON.stringify(manifest));
})().catch(error => { console.error(error); process.exitCode = 1; });
