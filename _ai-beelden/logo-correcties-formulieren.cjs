/* Plaats uitsluitend de door imagegen gewijzigde borstregio terug in het origineel.
   Alpha en alle pixels buiten de opgegeven regio blijven ongewijzigd. */
const fs = require('node:fs');
const path = require('node:path');
const sharp = require('C:/Users/arnas/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root = path.resolve(__dirname, '..');
const out = path.join(__dirname, 'foto/logo-correcties');
const jobs = [
  { name: 'aanvraag-foto-uit', generated: 'exec-f54de4ff-fd39-497f-8333-a5db2fd07f1d.png', region: [323, 214, 90, 102, 12] },
  { name: 'verwachten-inpakken', generated: 'exec-ad0e2c19-ef62-4583-a734-c861178eb0d5.png', region: [461, 192, 60, 65, 8] }
];
(async () => {
  fs.mkdirSync(out, { recursive: true });
  for (const job of jobs) {
    const target = path.join(root, 'img', job.name + '.webp');
    const original = path.join(out, job.name + '-origineel.webp');
    const master = path.join(out, job.name + '-imagegen.png');
    if (!fs.existsSync(original)) fs.copyFileSync(target, original);
    if (!fs.existsSync(master)) fs.copyFileSync(path.join('C:/Users/arnas/.codex/generated_images/01a0b4ea-4326-7b53-b0d6-b574ef9b1141', job.generated), master);
    const meta = await sharp(original).metadata();
    const source = await sharp(original).ensureAlpha().raw().toBuffer();
    const correction = await sharp(master).resize(meta.width, meta.height, { fit: 'fill' }).ensureAlpha().raw().toBuffer();
    const result = Buffer.from(source);
    const [left, top, width, height, feather] = job.region;
    for (let y = top; y < top + height; y++) for (let x = left; x < left + width; x++) {
      const distance = Math.min(x - left, left + width - 1 - x, y - top, top + height - 1 - y);
      const t = Math.min(1, distance / feather), weight = t * t * (3 - 2 * t);
      const offset = (y * meta.width + x) * 4;
      for (let c = 0; c < 3; c++) result[offset + c] = Math.round(source[offset + c] * (1 - weight) + correction[offset + c] * weight);
    }
    let pipeline = sharp(result, { raw: { width: meta.width, height: meta.height, channels: 4 } });
    if (!meta.hasAlpha) pipeline = pipeline.removeAlpha();
    await pipeline.webp({ lossless: true, effort: 6 }).toFile(target);
    const saved = await sharp(target).ensureAlpha().raw().toBuffer();
    let outside = 0, alpha = 0;
    for (let y = 0; y < meta.height; y++) for (let x = 0; x < meta.width; x++) {
      const offset = (y * meta.width + x) * 4;
      if (saved[offset + 3] !== source[offset + 3]) alpha++;
      if (x < left || x >= left + width || y < top || y >= top + height) {
        // RGB behind fully transparent pixels is not visible and may be discarded by WebP.
        if (source[offset + 3] && [0, 1, 2].some(c => saved[offset + c] !== source[offset + c])) outside++;
      }
    }
    if (outside || alpha) throw new Error(`${job.name}: ${outside} outside pixels and ${alpha} alpha pixels changed`);
    console.log(`${job.name}: ${meta.width}x${meta.height}, alpha=${meta.hasAlpha}, outside changes=${outside}, alpha changes=${alpha}`);
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
