// uit/<naam>.png -> <site>/img/contact-3d/<naam>.webp (bijgesneden op de alfa, 320 px hoog)
const fs = require('fs'); const sharp = require('C:/Users/tugce/Documents/GitHub/de-reus/dereus/_ai-beelden/node_modules/sharp');
const DOEL = 'C:/Users/tugce/Documents/GitHub/de-reus/dereus/img/contact-3d';
(async () => { for (const n of process.argv.slice(2)) {
  const knip = await sharp(`${__dirname}/uit/${n}.png`).trim({ threshold: 2 }).toBuffer();
  const info = await sharp(knip).resize({ height: 320 }).webp({ quality: 90, alphaQuality: 95, effort: 6 }).toFile(`${DOEL}/${n}.webp`);
  console.log(n, info.width, info.height, Math.round(info.size / 1024) + ' kB'); } })();
