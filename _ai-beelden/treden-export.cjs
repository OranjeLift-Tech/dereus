// Trede 3: uitsnede -> ../img/treden/dozen.webp. Stap 2 van 2, na treden-uitsnede.mjs.
//   - zachte alfa onder de drempel weg (de waas rond de randen)
//   - strak bijsnijden op de persoon, zodat de onderkant van het beeld precies de zolen is; de CSS
//     zet hem met de onderkant op de traprand, dus alles wat eronder zit zou hem laten zweven
//   - hoogte 440 px: tussen stoel-rechts.webp (420) en bank.webp (477), zodat de drie figuren
//     ongeveer even groot op de treden staan
// Meldt de gemeten breedte, die heb je nodig voor FIGUREN in _werk/blokken/treden.py.
const fs = require('node:fs');
const path = require('node:path');
const HIER = __dirname;
const sharp = require(path.join(HIER, 'node_modules', 'sharp'));

const BRON = path.join(HIER, 'foto', 'treden', 'dozen-uit.png');
const DOEL = path.join(HIER, '..', 'img', 'treden', 'dozen.webp');
const DREMPEL = 45, HOOGTE = 440;

(async () => {
  if (!fs.existsSync(BRON)) {
    console.error('Geen uitsnede gevonden: ' + BRON + '\nDraai eerst: node treden-uitsnede.mjs');
    process.exit(1);
  }
  const { data, info } = await sharp(BRON).ensureAlpha().raw().toBuffer({ resolveWithObject: true });

  let boven = info.height, onder = -1, links = info.width, rechts = -1;
  for (let y = 0; y < info.height; y++) {
    for (let x = 0; x < info.width; x++) {
      const i = (y * info.width + x) * 4;
      if (data[i + 3] < DREMPEL) { data[i + 3] = 0; continue; }
      if (data[i + 3] > 240) data[i + 3] = 255;
      if (y < boven) boven = y;
      if (y > onder) onder = y;
      if (x < links) links = x;
      if (x > rechts) rechts = x;
    }
  }
  if (onder < 0) { console.error('Alles doorzichtig; klopt de uitsnede wel?'); process.exit(1); }

  const vak = { left: links, top: boven, width: rechts - links + 1, height: onder - boven + 1 };
  const uit = await sharp(data, { raw: { width: info.width, height: info.height, channels: 4 } })
    .extract(vak)
    .resize({ height: HOOGTE })
    .webp({ quality: 82, effort: 6, alphaQuality: 85 })
    .toBuffer({ resolveWithObject: true });

  fs.mkdirSync(path.dirname(DOEL), { recursive: true });
  fs.writeFileSync(DOEL, uit.data);
  console.log('OK img/treden/dozen.webp  ' + uit.info.width + 'x' + uit.info.height +
    '  (' + Math.round(uit.data.length / 1024) + ' kB)');
  console.log('Zet in _werk/blokken/treden.py bij DOZEN de maat ' + uit.info.width + ', ' + uit.info.height + '.');
})();
