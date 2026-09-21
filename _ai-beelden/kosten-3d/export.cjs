// uit/<naam>.png -> <site>/img/kosten-3d/<naam>.webp (bijgesneden op de alfa, 420 px hoog)
const fs = require('fs'); const sharp = require('C:/Users/tugce/Documents/GitHub/de-reus/dereus/_ai-beelden/node_modules/sharp');
const DOEL = 'C:/Users/tugce/Documents/GitHub/de-reus/dereus/img/kosten-3d'; fs.mkdirSync(DOEL, { recursive: true });
const namen = process.argv.length > 2 ? process.argv.slice(2) : ['dozen', 'wagen', 'trap', 'gereedschap', 'opslag'];
(async () => { for (const n of namen) {
  const knip = await sharp(`${__dirname}/uit/${n}.png`).trim({ threshold: 2 }).toBuffer();
  const info = await sharp(knip).resize({ height: 420 }).webp({ quality: 90, alphaQuality: 95, effort: 6 }).toFile(`${DOEL}/${n}.webp`);
  console.log(n, info.width, info.height, Math.round(info.size / 1024) + ' kB'); } })();
