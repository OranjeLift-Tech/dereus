const fs = require('fs'); const sharp = require('C:/Users/tugce/Documents/GitHub/de-reus/dereus/_ai-beelden/node_modules/sharp');
const DOEL = 'C:/Users/tugce/Documents/GitHub/de-reus/dereus/img/kosten-kalender'; fs.mkdirSync(DOEL, { recursive: true });
(async () => { for (const n of process.argv.slice(2)) { const knip = await sharp(`${__dirname}/uit/${n}.png`).trim({ threshold: 2 }).toBuffer();
  const i = await sharp(knip).resize({ height: 720, withoutEnlargement: true }).webp({ quality: 90, alphaQuality: 95, effort: 6 }).toFile(`${DOEL}/${n}.webp`); console.log(`${n}: [${i.width}, ${i.height}], ${Math.round(i.size / 1024)} kB`); } })();
