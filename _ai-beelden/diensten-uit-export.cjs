// Diensten: uitsnede -> /img/dienst-<naam>-uit.webp, plus de maatvoering voor het uitstap-effect.
// Stap 2 van 2, na diensten-uitsnede.mjs.
//   - zelfde cover-uitsnede als de basisfoto, zodat beide lagen exact over elkaar liggen
//   - zachte alfa onder de drempel weg: haalt de waas rond de randen eruit
//   - meet waar de persoon begint (bovenkant) en hoe breed hij staat, en schrijft dat naar uitstap.json
const fs = require('node:fs');
const path = require('node:path');
const HIER = __dirname;
const sharp = require(path.join(HIER, 'node_modules', 'sharp'));

const UITSNEDE = path.join(HIER, 'foto', 'Onze diensten', 'uitsnede');
const IMG = path.join(HIER, '..', 'img');
const NAMEN = ['particulier', 'zakelijk', 'nationaal', 'internationaal', 'verhuislift', 'opslag', 'handyman', 'woningontruiming'];
const B = 1080, H = 810;            // 1,5x de basisfoto (720x540): scherp als de uitsnede vergroot wordt
const DREMPEL = 45;                 // alfa hieronder = helemaal weg

(async () => {
  const maat = {};
  for (const naam of NAMEN) {
    const { data, info } = await sharp(path.join(UITSNEDE, `${naam}.png`))
      .resize(B, H, { fit: 'cover' }).ensureAlpha().raw().toBuffer({ resolveWithObject: true });

    let boven = info.height, links = info.width, rechts = 0, onder = 0;
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
    await sharp(data, { raw: { width: info.width, height: info.height, channels: 4 } })
      .webp({ quality: 78, effort: 6, alphaQuality: 80 })
      .toFile(path.join(IMG, `dienst-${naam}-uit.webp`));

    maat[naam] = {
      boven: +(boven / info.height).toFixed(4),
      onder: +(onder / info.height).toFixed(4),
      links: +(links / info.width).toFixed(4),
      rechts: +(rechts / info.width).toFixed(4),
      kb: Math.round(fs.statSync(path.join(IMG, `dienst-${naam}-uit.webp`)).size / 1024),
    };
    const m = maat[naam];
    console.log(`${naam.padEnd(18)} boven ${(m.boven * 100).toFixed(1)}%  onder ${(m.onder * 100).toFixed(1)}%  x ${(m.links * 100).toFixed(0)}-${(m.rechts * 100).toFixed(0)}%  ${m.kb}kB`);
  }
  fs.writeFileSync(path.join(HIER, 'uitstap.json'), JSON.stringify(maat, null, 2));
})();
