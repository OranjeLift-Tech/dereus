// Handyman: uitsnede van boor, handschoen, beide onderarmen en de rechterhand.
// Het model (imgly) levert boor + handschoen goed, maar laat de armen weg en de rechterhand half doorzichtig.
// De huid is donkerbruin op een lichte houten vloer: binnen twee handgetekende vlakken is huid = donker en roder dan blauw.
const path = require('path');
const W = 'C:/Users/tugce/Documents/GitHub/de-reus/dereus/';
const sharp = require(W + '_ai-beelden/node_modules/sharp');
const B = 1080, H = 810;

const binnen = (px, py, poly) => { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const [xi, yi] = poly[i], [xj, yj] = poly[j]; if ((yi > py) !== (yj > py) && px < (xj - xi) * (py - yi) / (yj - yi) + xi) c = !c; } return c; };
// vlakken in coördinaten van de 720x540-foto
const S = B / 720;
const ARM_LINKS = [[0, 0], [150, 0], [300, 95], [255, 165], [120, 120], [0, 78]].map(([x, y]) => [x * S, y * S]);
const ARM_RECHTS = [[335, 0], [462, 0], [480, 200], [492, 300], [488, 425], [355, 425], [372, 330], [412, 285], [418, 200], [352, 70]].map(([x, y]) => [x * S, y * S]);
const POLSBAND = [[230, 70], [289, 82], [264, 152], [220, 128]].map(([x, y]) => [x * S, y * S]);

(async () => {
  const foto = await sharp(W + 'img/dienst-handyman.webp').resize(B, H, { fit: 'cover' }).removeAlpha().raw().toBuffer();
  const model = await sharp(W + '_ai-beelden/foto/Onze diensten/uitsnede/handyman.png').resize(B, H, { fit: 'cover' }).ensureAlpha().extractChannel(3).raw().toBuffer();
  const a = Buffer.alloc(B * H);
  for (let y = 0; y < H; y++) for (let x = 0; x < B; x++) {
    const i = y * B + x, r = foto[i * 3], g = foto[i * 3 + 1], b = foto[i * 3 + 2];
    const lum = .299 * r + .587 * g + .114 * b;
    let v = model[i] > 110 ? 255 : 0;                                   // boor + handschoen uit het model, hard gemaakt
    const huid = r - b > 56 && r - g > 38;                         // huid is roder dan de houten vloer (vloer: r-b rond 45, r-g rond 25)
    if (!v && huid && (binnen(x, y, ARM_LINKS) || binnen(x, y, ARM_RECHTS))) v = 255;
    if (!v && binnen(x, y, POLSBAND)) v = 255;                          // de polsband, als geheel
    if (!v && binnen(x, y, ARM_RECHTS) && y > 195 * S && y < 250 * S && lum > 120 && Math.abs(r - b) < 40 && x > 425 * S) v = 255;   // het horloge
    a[i] = v;
  }
  // gaatjes dicht en rand glad: vervagen, drempel, nog eens licht vervagen
  let glad = await sharp(a, { raw: { width: B, height: H, channels: 1 } }).blur(4).threshold(118).blur(1.2).raw().toBuffer();
  const rgba = Buffer.alloc(B * H * 4);
  for (let i = 0; i < B * H; i++) { rgba[i * 4] = foto[i * 3]; rgba[i * 4 + 1] = foto[i * 3 + 1]; rgba[i * 4 + 2] = foto[i * 3 + 2]; const al = glad[i * 3]; rgba[i * 4 + 3] = al < 30 ? 0 : al; }
  await sharp(rgba, { raw: { width: B, height: H, channels: 4 } }).webp({ quality: 78, effort: 6, alphaQuality: 80 }).toFile(W + 'img/dienst-handyman-uit.webp');
  console.log('ok');
})();
