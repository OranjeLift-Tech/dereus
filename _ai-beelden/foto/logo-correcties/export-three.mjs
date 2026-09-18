// Export the three localized imagegen corrections without changing the surrounding scene.
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const require = createRequire(import.meta.url);
const sharp = require('C:/Users/arnas/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const directory = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(directory, '../../..');
const generated = 'C:/Users/arnas/.codex/generated_images/01a0b4ea-132d-7c03-917d-b3145abe51d9';
const jobs = [
  { name: 'particulier', source: 'exec-d059913c-3062-4058-bef4-672fb1d74df9.png', mask: '<rect x="74" y="265" width="171" height="138" rx="18" fill="white"/>' },
  { name: 'internationaal', source: 'exec-44902bd6-1fe2-4120-985e-79ffa7507051.png', mask: '<path d="M139 341 Q155 312 189 305 L210 299 L259 306 Q306 316 328 341 L348 380 L365 420 L341 432 L315 412 L293 434 L146 433 L133 387 Z" fill="white"/>' },
  { name: 'verhuislift', source: 'exec-fe09b9e8-e8b6-4778-b3f9-6bf72db31f2b.png', mask: '<rect x="525" y="229" width="122" height="102" rx="6" fill="white"/>' }
];
for (const job of jobs) {
  const target = path.join(root, 'img', `dienst-${job.name}.webp`);
  const master = path.join(directory, `dienst-${job.name}-imagegen.png`);
  const before = path.join(directory, `dienst-${job.name}-before.webp`);
  try { await fs.access(master); }
  catch { await fs.copyFile(path.join(generated, job.source), master); }
  try { await fs.copyFile(target, before, (await import('node:fs')).constants.COPYFILE_EXCL); }
  catch (error) { if (error.code !== 'EEXIST') throw error; }
  const resized = await sharp(master).resize(720, 540, { fit: 'fill' }).png().toBuffer();
  const mask = await sharp(Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="720" height="540">${job.mask}</svg>`)).blur(3).png().toBuffer();
  const overlay = await sharp(resized).ensureAlpha().composite([{ input: mask, blend: 'dest-in' }]).png().toBuffer();
  // Lossless encoding keeps decoded source pixels outside the edit area intact.
  const output = await sharp(before).composite([{ input: overlay }]).webp({ lossless: true, effort: 6 }).toBuffer();
  await fs.writeFile(target, output);
  const info = await sharp(output).metadata();
  console.log(`${path.basename(target)}: ${info.width}x${info.height}, ${output.length} bytes`);
}
