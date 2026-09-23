// Het model zette een verzonnen rood merklabel op de cargozak van de middelste verhuizer in v2.
// Te klein om te lezen op 533 px, maar het is een merk van een ander bedrijf, dus weg ermee.
// Geen nieuwe generatie: het gaat om een vlakje effen donkerblauwe stof.
//
// Les uit poging 1: het bronvak moet RUIM binnen de broekspijp liggen. Een vak dat tot aan de
// silhouetrand loopt sleept de achtergrond (het gele kenteken en de witte wagenrand) mee naar
// binnen, en dan staat er een lichte veeg op de stof die erger is dan het label.
const sharp = require('../../node_modules/sharp');

const VAK  = { left: 745, top: 1396, width: 30, height: 34 };  // het rode label
const BRON = { left: 745, top: 1447, width: 30, height: 34 };  // schone stof eronder, zelfde zak en licht

(async () => {
  const plak = await sharp('v2.png').extract(BRON).blur(0.8).png().toBuffer();
  const masker = Buffer.from(
    `<svg width="${VAK.width}" height="${VAK.height}"><defs><radialGradient id="g">` +
    `<stop offset="50%" stop-color="#fff" stop-opacity="1"/><stop offset="100%" stop-color="#fff" stop-opacity="0"/>` +
    `</radialGradient></defs><rect width="100%" height="100%" fill="url(#g)"/></svg>`);
  const zacht = await sharp(plak)
    .composite([{ input: await sharp(masker).png().toBuffer(), blend: 'dest-in' }])
    .png().toBuffer();
  await sharp('v2.png')
    .composite([{ input: zacht, left: VAK.left, top: VAK.top }])
    .png().toFile('v2-schoon.png');

  // hoeveel is er veranderd, en ligt dat allemaal in het vak?
  const a = await sharp('v2.png').raw().toBuffer();
  const b = await sharp('v2-schoon.png').raw().toBuffer();
  let n = 0, minX = 1e9, maxX = -1, minY = 1e9, maxY = -1;
  for (let i = 0; i < a.length; i += 3) {
    if (Math.abs(a[i]-b[i]) + Math.abs(a[i+1]-b[i+1]) + Math.abs(a[i+2]-b[i+2]) > 6) {
      const p = i/3, x = p % 2048, y = (p/2048)|0;
      n++; if (x<minX) minX=x; if (x>maxX) maxX=x; if (y<minY) minY=y; if (y>maxY) maxY=y;
    }
  }
  console.log(`gewijzigd: ${n} px (${(100*n/(2048*2048)).toFixed(4)}%), vak x ${minX}-${maxX}, y ${minY}-${maxY}`);
})();
