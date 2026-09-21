/* Bewaar de gekozen truck; neem alleen de nieuwe belettering binnen het zijpaneel over. */
const path = require('node:path');
const sharp = require(process.env.SHARP_MODULE || 'C:/Users/arnas/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root = path.resolve(__dirname, '..');
const source = path.join(root, '_ai-beelden/foto/footer-truck');
(async () => {
  const original = path.join(source, '02-geselecteerd-origineel.png');
  const correction = path.join(source, '02-belettering.png');
  const mask = Buffer.from('<svg xmlns="http://www.w3.org/2000/svg" width="1536" height="1024"><defs><filter id="z"><feGaussianBlur stdDeviation="2"/></filter></defs><path d="M851 105 L1483 216 L1483 650 L851 650 Z" fill="white" filter="url(#z)"/></svg>');
  const patch = await sharp(correction).composite([{ input: mask, blend: 'dest-in' }]).png().toBuffer();
  const alpha = await sharp(original).extractChannel('alpha').toBuffer();
  const merged = await sharp(original).composite([{ input: patch }]).removeAlpha().png().toBuffer();
  const final = await sharp(merged).joinChannel(alpha).png().toBuffer();
  await sharp(final).toFile(path.join(source, '02-footer-definitief.png'));
  await sharp(final).resize({ width: 960, withoutEnlargement: true }).webp({ quality: 90, alphaQuality: 100 }).toFile(path.join(root, 'img/footer-truck.webp'));
  console.log('img/footer-truck.webp: 960x640, originele alpha behouden.');
})().catch(error => { console.error(error); process.exitCode = 1; });
