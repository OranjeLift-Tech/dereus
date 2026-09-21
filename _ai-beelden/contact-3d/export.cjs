// uit/<naam>.png -> <site>/img/contact-3d/<naam>.webp (bijgesneden op de alfa, 400 px breed)
const fs = require('fs'); const sharp = require('C:/Users/tugce/Documents/GitHub/de-reus/dereus/_ai-beelden/node_modules/sharp');
const DOEL = 'C:/Users/tugce/Documents/GitHub/de-reus/dereus/img/contact-3d'; fs.mkdirSync(DOEL, { recursive: true });
(async () => { for (const n of ['telefoon', 'envelop', 'formulier', 'doos']) {
  const knip = await sharp(`${__dirname}/uit/${n}.png`).trim({ threshold: 2 }).toBuffer();
  const info = await sharp(knip).resize({ height: 400 }).webp({ quality: 90, alphaQuality: 95, effort: 6 }).toFile(`${DOEL}/${n}.webp`);
  console.log(n, info.width, info.height, Math.round(info.size / 1024) + ' kB'); } })();
