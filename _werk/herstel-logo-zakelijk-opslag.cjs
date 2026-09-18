/* Behoud originele foto's buiten de twee lokaal gecorrigeerde logogebieden. */
const fs = require('node:fs');
const path = require('node:path');
const sharp = require('C:/Users/arnas/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root = path.resolve(__dirname, '..');
const output = path.join(root, '_ai-beelden/foto/logo-correcties');
const jobs = [
  { name: 'dienst-zakelijk', generated: 'exec-521bbddc-7234-45ea-9052-442258bdd812.png', regions: [{ left: 267, top: 377, width: 197, height: 157 }] },
  { name: 'dienst-opslag', generated: 'exec-ff24edec-4359-4f95-bf55-599d6e47c537.png', regions: [{ left: 337, top: 256, width: 40, height: 36 }, { left: 465, top: 269, width: 40, height: 35 }] }
];
(async () => {
  fs.mkdirSync(output, { recursive: true });
  for (const job of jobs) {
    const source = path.join(root, 'img', job.name + '.webp');
    const backup = path.join(output, job.name + '-origineel.webp');
    if (!fs.existsSync(backup)) fs.copyFileSync(source, backup);
    const generated = path.join(output, job.name + '-generatie.png');
    if (!fs.existsSync(generated)) fs.copyFileSync(path.join('C:/Users/arnas/.codex/generated_images/01a0b4ea-6966-7400-aff7-184e0ff47bb7', job.generated), generated);
    const resized = await sharp(generated).resize(720, 540, { fit: 'fill' }).png().toBuffer();
    const overlays = [];
    for (const region of job.regions) {
      const { data, info } = await sharp(resized).extract(region).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
      if (job.name === 'dienst-zakelijk') {
        const original = await sharp(backup).extract(region).ensureAlpha().raw().toBuffer();
        const delta = [0, 0, 0];
        let samples = 0;
        for (let y = 0; y < info.height; y++) for (let x = 0; x < info.width; x++) {
          if (Math.min(x, y, info.width - 1 - x, info.height - 1 - y) > 2) continue;
          for (let channel = 0; channel < 3; channel++) {
            const offset = (y * info.width + x) * 4 + channel;
            delta[channel] += original[offset] - data[offset];
          }
          samples++;
        }
        for (let y = 0; y < info.height; y++) for (let x = 0; x < info.width; x++) {
          for (let channel = 0; channel < 3; channel++) {
            const offset = (y * info.width + x) * 4 + channel;
            data[offset] = Math.max(0, Math.min(255, data[offset] + delta[channel] / samples));
          }
        }
      }
      for (let y = 0; y < info.height; y++) for (let x = 0; x < info.width; x++) {
        const edge = Math.min(x, y, info.width - 1 - x, info.height - 1 - y);
        data[(y * info.width + x) * 4 + 3] = Math.round(255 * Math.min(1, edge / (job.name === 'dienst-zakelijk' ? 8 : 4)));
      }
      const input = await sharp(data, { raw: { width: info.width, height: info.height, channels: 4 } }).png().toBuffer();
      overlays.push({ input, left: region.left, top: region.top });
    }
    const final = await sharp(backup).composite(overlays).png().toBuffer();
    fs.writeFileSync(path.join(output, job.name + '.png'), final);
    await sharp(final).webp({ quality: 92, effort: 6 }).toFile(source);
    console.log(job.name + ': localized corrections saved, 720x540');
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
