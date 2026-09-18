/* Exporteert een transparante bron naar alle responsive hero-formaten.
   node _werk/export-teambeeld.cjs <bron.png> <pad-naar-sharp> */
const fs = require('node:fs');
const path = require('node:path');
const sharp = require(process.argv[3] || 'sharp');
const source = process.argv[2];
const target = path.resolve(__dirname, '../img/team');

(async () => {
  if (!source) throw new Error('Geef een transparante bronafbeelding op.');
  const meta = await sharp(source).metadata();
  if (!meta.hasAlpha) throw new Error('De bron mist een alfakanaal.');
  for (const width of [700, 1100, 1600]) {
    await sharp(source).resize({ width }).webp({ quality: width <= 1100 ? 80 : 70, alphaQuality: 100 })
      .toFile(path.join(target, `team-hero-${width}.webp`));
  }
  await sharp(source).resize({ width: 700 }).png({ compressionLevel: 9, palette: true, colours: 256, effort: 10 })
    .toFile(path.join(target, 'team-hero-700.png'));
  fs.writeFileSync(path.join(target, 'team-hero.json'), JSON.stringify({
    naam: 'team-hero', verhouding: [meta.width, meta.height], breedtes: [700, 1100, 1600], png: 700
  }, null, 2) + '\n');
  console.log('Alle teambeeldformaten en afmetingen bijgewerkt; transparantie behouden.');
})().catch(error => { console.error(error.message); process.exitCode = 1; });
