// Borstmerk adviseur: de AI-print (geel, met verzonnen tekst) weg, het echte negatieve beeldmerk erop.
// Afspraak: _ai-beelden/gereedschap/MERK-OP-KLEDING.md (16,5% van de schouderbreedte, onderste knoop,
// 0,22 x schouder naast de knooplijst, luminantie van de stof overnemen, fijne korrel).
const im = await laad('/img/contact-adviseur-uit.webp');
const W = im.width, H = im.height;
const [c, x] = doek(W, H); x.drawImage(im, 0, 0);
const org = x.getImageData(0, 0, W, H);
const d = new Uint8ClampedArray(org.data);

// 1. de print vinden: alles in het borstvak dat niet blauwe stof is (geel en de lichte tekst)
const VAK = { l: 336, t: 208, r: 410, b: 272 };
const isPrint = i => { const r = d[i], g = d[i+1], b = d[i+2]; return r > 90 && r - b > 0 || g > 110; };
let masker = new Uint8Array(W * H), n = 0, bb = [1e9, 1e9, -1, -1];
for (let y = VAK.t; y < VAK.b; y++) for (let xx = VAK.l; xx < VAK.r; xx++) {
  const i = (y * W + xx) * 4;
  if (isPrint(i)) { masker[y * W + xx] = 1; n++; bb = [Math.min(bb[0], xx), Math.min(bb[1], y), Math.max(bb[2], xx), Math.max(bb[3], y)]; }
}
// ruim verbreden: de gele rand loopt met halftinten in het blauw over
const verbreed = (m, k) => { const u = new Uint8Array(m); for (let y = VAK.t - k; y < VAK.b + k; y++) for (let xx = VAK.l - k; xx < VAK.r + k; xx++) {
  let z = 0; for (let dy = -k; dy <= k && !z; dy++) for (let dx = -k; dx <= k; dx++) if (m[(y+dy)*W + xx+dx]) { z = 1; break; } u[y*W+xx] = z; } return u; };
masker = verbreed(masker, 3);

// 2. invullen met stof van direct eronder (zelfde plooirichting en licht), zacht overgeblend
const DY = 52;
for (let y = VAK.t - 4; y < VAK.b + 4; y++) for (let xx = VAK.l - 4; xx < VAK.r + 4; xx++) {
  if (!masker[y * W + xx]) continue;
  const i = (y * W + xx) * 4, j = ((y + DY) * W + xx) * 4;
  d[i] = d[j]; d[i+1] = d[j+1]; d[i+2] = d[j+2];
}
// naad wegwerken: een paar rondes middelen op de rand van het masker
const rand = verbreed(masker, 2);
for (let ronde = 0; ronde < 3; ronde++) {
  const kopie = new Uint8ClampedArray(d);
  for (let y = VAK.t - 6; y < VAK.b + 6; y++) for (let xx = VAK.l - 6; xx < VAK.r + 6; xx++) {
    if (!rand[y * W + xx] || (masker[y*W+xx] && masker[(y-2)*W+xx] && masker[(y+2)*W+xx] && masker[y*W+xx-2] && masker[y*W+xx+2])) continue;
    for (let k = 0; k < 3; k++) { let s = 0; for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) s += kopie[((y+dy)*W + xx+dx)*4 + k]; d[(y*W+xx)*4 + k] = s / 9; }
  }
}
x.putImageData(new ImageData(d, W, H), 0, 0);

// 3. maat en plaats volgens de afspraak
const SCHOUDER = 257;                       // blauwe stof incl. mouwen, y 230-250 (gemeten)
const MB = Math.round(0.165 * SCHOUDER);    // 42 px
const merk = await laad('/img/logo/dereus-beeldmerk-negatief.svg');
const MH = Math.round(MB * 509.39 / 1000);
const KNOOPLIJST = 322, CX = KNOOPLIJST + Math.round(0.22 * SCHOUDER), CY = 231;
const ml = CX - MB / 2, mt = CY - MH / 2;

// merk op een eigen doek, dan de luminantie van de stof eroverheen (geijkt op de mediaan onder het merk)
const [mc, mx] = doek(W, H);
mx.drawImage(merk, ml, mt, MB, MH);
const md = mx.getImageData(0, 0, W, H).data;
const stof = x.getImageData(0, 0, W, H).data;
const lum = i => 0.2126 * stof[i] + 0.7152 * stof[i+1] + 0.0722 * stof[i+2];
const onder = [];
for (let y = Math.floor(mt); y < mt + MH; y++) for (let xx = Math.floor(ml); xx < ml + MB; xx++) { const i = (y*W+xx)*4; if (md[i+3] > 128) onder.push(lum(i)); }
onder.sort((a, b) => a - b); const med = onder[onder.length >> 1];
// zachte schaduw onder het merk (stiksel ligt iets op de stof)
x.save(); x.filter = 'blur(0.8px)'; x.globalAlpha = 0.28;
const [sc, sx] = doek(W, H); sx.drawImage(merk, ml + 0.4, mt + 0.8, MB, MH); sx.globalCompositeOperation = 'source-in'; sx.fillStyle = '#061536'; sx.fillRect(0, 0, W, H);
x.drawImage(sc, 0, 0); x.restore();
const uit = x.getImageData(0, 0, W, H); const u = uit.data;
let zaad = 7; const ruis = () => { zaad = (zaad * 16807) % 2147483647; return (zaad / 2147483647) - 0.5; };
for (let y = Math.floor(mt) - 2; y < mt + MH + 2; y++) for (let xx = Math.floor(ml) - 2; xx < ml + MB + 2; xx++) {
  const i = (y*W+xx)*4, a = md[i+3] / 255; if (!a) continue;
  const f = Math.min(1.12, Math.max(0.85, lum(i) / med)) * (1 + 0.15 * 0.25 * ruis());
  for (let k = 0; k < 3; k++) u[i+k] = u[i+k] * (1 - a) + Math.min(255, md[i+k] * f) * a;
}
// alfa terug uit het origineel
for (let i = 3; i < u.length; i += 4) u[i] = org.data[i];
x.putImageData(uit, 0, 0);
bewaar('adviseur-merk.png', c);

// controle op 4x, voor en na
const [cc, cx2] = doek(800, 400); cx2.imageSmoothingEnabled = false;
cx2.drawImage(im, 330, 200, 100, 100, 0, 0, 400, 400);
cx2.drawImage(c, 330, 200, 100, 100, 400, 0, 400, 400);
bewaar('merk-voor-na-4x.png', cc);
return { printPx: n, printBbox: bb, merk: [ml, mt, MB, MH], mediaan: Math.round(med) };
