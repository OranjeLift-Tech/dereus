/* Van de gecorrigeerde bronfoto naar de twee bestanden die de site opvraagt.
 *
 * Zelfde stappen als de bestaande pijplijn:
 *   img/dienst-opslag.webp      diensten-gen.mjs --klaar : 720x540 cover, webp 80
 *   img/dienst-opslag-uit.webp  diensten-uit-export.cjs  : 1080x810 cover, alfadrempel 45, webp 78
 *
 * Twee afwijkingen, met reden:
 *   - de cover-uitsnede staat vast op x=2 in plaats van position:'attention'. Dat is de
 *     uitsnede die de huidige webp ook heeft (gemeten), en attention kan na het wijzigen
 *     van pixels een andere kolom kiezen.
 *   - de achtergrondverwijderaar draait niet opnieuw: de bestaande alfa uit
 *     foto/Onze diensten/uitsnede/opslag.png blijft, alleen de kleuren eronder zijn nieuw.
 *     Zo kan de omhullende niet verschuiven en blijft uitstap.json kloppen.
 */
const fs = require('node:fs');
const path = require('node:path');
const sharp = require('C:/users/arnas/git_repos/dereus/_ai-beelden/node_modules/sharp');

const ROOT = 'C:/users/arnas/git_repos/dereus';
const NIEUW = `${ROOT}/website/review/beeld-opslag-ronde-1/pogingen/opslag-gecorrigeerd.png`;
const ALFA = `${ROOT}/_ai-beelden/foto/Onze diensten/uitsnede/opslag.png`;
const IMG = `${ROOT}/img`;
const DREMPEL = 45;

(async () => {
  await sharp(NIEUW)
    .resize(723, 540)
    .extract({ left: 2, top: 0, width: 720, height: 540 })
    .webp({ quality: 80 })
    .toFile(path.join(IMG, 'dienst-opslag.webp'));

  const kleur = await sharp(NIEUW).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  const masker = await sharp(ALFA).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  if (kleur.info.width !== masker.info.width || kleur.info.height !== masker.info.height) {
    throw new Error(`maat verschilt: ${kleur.info.width}x${kleur.info.height} vs ${masker.info.width}x${masker.info.height}`);
  }
  const samen = Buffer.from(kleur.data);
  for (let i = 3; i < samen.length; i += 4) samen[i] = masker.data[i];

  const { data, info } = await sharp(samen, { raw: { width: kleur.info.width, height: kleur.info.height, channels: 4 } })
    .resize(1080, 810, { fit: 'cover' })
    .ensureAlpha()
    .raw()
    .toBuffer({ resolveWithObject: true });

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
    .toFile(path.join(IMG, 'dienst-opslag-uit.webp'));

  const kb = (p) => Math.round(fs.statSync(path.join(IMG, p)).size / 1024);
  console.log(`dienst-opslag.webp      720x540   ${kb('dienst-opslag.webp')} kB`);
  console.log(`dienst-opslag-uit.webp  1080x810  ${kb('dienst-opslag-uit.webp')} kB`);
  console.log(`omhullende: boven ${(boven / info.height * 100).toFixed(2)}%  onder ${(onder / info.height * 100).toFixed(2)}%  ` +
              `links ${(links / info.width * 100).toFixed(2)}%  rechts ${(rechts / info.width * 100).toFixed(2)}%`);
})();
