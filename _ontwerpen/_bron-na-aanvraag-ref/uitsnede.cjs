// De medewerker zonder kamer, met een bureau dat rechts zacht uitloopt in plaats van recht af te houden.
// Bron: img/contact-klantenservice-boog-uit.webp (850x730, zij + bureau + schrijfblok + kop, al zonder achtergrond;
// gemaakt voor /contact/ #na-bericht, zie _ai-beelden/na-bericht-boog/). Daar houdt het bureau op bij x 850, precies
// langs de rechterkant van de kop; in een boog of lijst valt die rand weg, maar waar zij vrij staat zie je een
// rechte snede door het blad, de voorkant en de poot.
// Hier: boven de kop (rij < 537) en onder de kop (rij > 657) loopt de alfa van x 770 naar 0 bij x 850; de kop
// zelf (rij 537 tot 657) blijft heel, alleen het randje rechts ervan (x >= 847, een stukje toetsenbord) gaat weg.
// node uitsnede.cjs  ->  img/offerte-klantenservice-uit.webp
const path = require('path');
const REPO = path.resolve(__dirname, '../..');
const sharp = require(path.resolve(REPO, '../_ai-beelden/node_modules/sharp'));

(async () => {
  const { data, info } = await sharp(path.join(REPO, 'img/contact-klantenservice-boog-uit.webp')).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  const W = info.width, H = info.height;
  const VAN = 770, TOT = 850, KOP_BOVEN = 537, KOP_ONDER = 657;
  const glad = t => t * t * (3 - 2 * t);
  for (let y = 522; y < H; y++) {
    const kop = y >= KOP_BOVEN && y <= KOP_ONDER;
    for (let x = VAN; x < W; x++) {
      const i = (y * W + x) * 4 + 3;
      if (kop) { if (x >= 847) data[i] = 0; continue; }
      const f = glad(Math.min(1, Math.max(0, (TOT - x) / (TOT - VAN))));
      data[i] = Math.round(data[i] * f);
    }
  }
  await sharp(data, { raw: { width: W, height: H, channels: 4 } }).webp({ quality: 90, alphaQuality: 100 })
    .toFile(path.join(REPO, 'img/offerte-klantenservice-uit.webp'));
  console.log('ok', W, H);
})();
