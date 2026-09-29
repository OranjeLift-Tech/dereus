// Zet het De Reus-logo in perspectief op de zijkant van de dozen in een klei-icoon (480 px bron).
// NODE_PATH=<map met node_modules/sharp> node logo-op-doos.cjs <uitmap>  -> <naam>-logo-480.png per icoon; daarna WebP q88 op 480 en 240 (lanczos3) naar img/clay/
// Per vlak: de vier hoeken van het doosvlak (LB, RB, RO, LO) en het logovak daarin in (s,t) 0..1.
// Het logo krijgt de belichting van het vlak mee: kleur x (helderheid hier / helderheid van karton in vol licht),
// zodat een logo op een zijvlak in de schaduw ook donkerder is. Inkt: 80% normaal, 20% vermenigvuldigen met het karton.
const sharp = require('sharp');
const path = require('path');
const REPO = 'C:/Users/tugce/Documents/GitHub/de-reus/dereus/dereus';
const UIT = process.argv[2];
const KARTON = 158; // helderheid van het belichte karton (bovenste doos, opslagdoos)

const ICONEN = {
  dozen: [
    { q: [[201, 78], [405, 55], [405, 227], [201, 250]], s: [0.20, 0.68], t: [0.30, 0.81] },   // bovenste doos, rechterzij
    { q: [[332, 263], [455, 223], [455, 398], [332, 445]], s: [0.23, 0.77], t: [0.35, 0.88] }, // grote doos, rechterzij
    { q: [[14, 326], [150, 349], [150, 467], [14, 444]], s: [0.23, 0.77], t: [0.22, 0.82] },    // kleine doos, linkerzij
  ],
  trap: [
    { q: [[214, 43], [282, 55], [282, 136], [214, 123]], s: [0.19, 0.81], t: [0.24, 0.76] },
  ],
  opslag: [
    { q: [[112, 292], [233, 292], [233, 405], [112, 405]], s: [0.235, 0.765], t: [0.41, 0.88] },
  ],
  // /kosten/ extradiensten: montage heeft geen doos
  verhuislift: [
    { q: [[303, 237], [361, 228], [381, 294], [326, 305]], s: [0.15, 0.85], t: [0.20, 0.79] },   // doos op de steekwagen, lichte zijkant (kantelt mee)
  ],
  woningontruiming: [
    { q: [[62, 246], [220, 292], [220, 403], [62, 353]], s: [0.065, 0.37], t: [0.13, 0.61] },    // linkerzij, tussen de flap en de plakstrip
  ],
};

// homografie eenheidsvierkant -> vierhoek (Heckbert)
function homografie(q) {
  const [[x0, y0], [x1, y1], [x2, y2], [x3, y3]] = q;
  const dx1 = x1 - x2, dx2 = x3 - x2, dx3 = x0 - x1 + x2 - x3;
  const dy1 = y1 - y2, dy2 = y3 - y2, dy3 = y0 - y1 + y2 - y3;
  let g = 0, h = 0;
  if (Math.abs(dx3) > 1e-9 || Math.abs(dy3) > 1e-9) {
    const d = dx1 * dy2 - dx2 * dy1;
    g = (dx3 * dy2 - dx2 * dy3) / d;
    h = (dx1 * dy3 - dx3 * dy1) / d;
  }
  const a = x1 - x0 + g * x1, b = x3 - x0 + h * x3, c = x0;
  const d = y1 - y0 + g * y1, e = y3 - y0 + h * y3, f = y0;
  return [a, b, c, d, e, f, g, h, 1];
}
function inverse(m) {
  const [a, b, c, d, e, f, g, h, i] = m;
  const A = e * i - f * h, B = -(d * i - f * g), C = d * h - e * g;
  const det = a * A + b * B + c * C;
  return [A, -(b * i - c * h), b * f - c * e, B, a * i - c * g, -(a * f - c * d), C, -(a * h - b * g), a * e - b * d].map(v => v / det);
}
const pas = (m, x, y) => { const w = m[6] * x + m[7] * y + m[8]; return [(m[0] * x + m[1] * y + m[2]) / w, (m[3] * x + m[4] * y + m[5]) / w]; };

(async () => {
  const LB = 1600;
  const logo = await sharp(path.join(REPO, 'img/logo/dereus-logo.svg'), { density: 300 }).resize({ width: LB }).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  const LW = logo.info.width, LH = logo.info.height, L = logo.data;
  const monster = (u, v) => { // bilineair, u,v in pixels van het logo; premultiplied
    if (u < 0 || v < 0 || u > LW - 1 || v > LH - 1) return [0, 0, 0, 0];
    const x = Math.floor(u), y = Math.floor(v), fx = u - x, fy = v - y;
    const r = [0, 0, 0, 0];
    for (const [dx, dy, w] of [[0, 0, (1 - fx) * (1 - fy)], [1, 0, fx * (1 - fy)], [0, 1, (1 - fx) * fy], [1, 1, fx * fy]]) {
      const xx = Math.min(x + dx, LW - 1), yy = Math.min(y + dy, LH - 1), o = (yy * LW + xx) * 4, a = L[o + 3] / 255;
      r[0] += L[o] * a * w; r[1] += L[o + 1] * a * w; r[2] += L[o + 2] * a * w; r[3] += a * w;
    }
    return r;
  };

  for (const [naam, vlakken] of Object.entries(ICONEN)) {
    const { data, info } = await sharp(path.join(REPO, `img/clay/${naam}-480.webp`)).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
    const W = info.width, H = info.height;
    const helder = (o) => 0.2126 * data[o] + 0.7152 * data[o + 1] + 0.0722 * data[o + 2];
    const uit = Buffer.from(data);
    for (const v of vlakken) {
      const vlak = homografie(v.q);
      // logovak in het vlak, logo-aspect wordt bepaald door s/t (de gebruiker ziet het vlak verkort)
      const hoek = [[v.s[0], v.t[0]], [v.s[1], v.t[0]], [v.s[1], v.t[1]], [v.s[0], v.t[1]]].map(([s, t]) => pas(vlak, s, t));
      const Hl = homografie(hoek), Hinv = inverse(Hl);
      const xs = hoek.map(p => p[0]), ys = hoek.map(p => p[1]);
      const x0 = Math.floor(Math.min(...xs)) - 1, x1 = Math.ceil(Math.max(...xs)) + 1;
      const y0 = Math.floor(Math.min(...ys)) - 1, y1 = Math.ceil(Math.max(...ys)) + 1;
      // referentiehelderheid: mediaan in het logovak
      const hs = [];
      for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
        const [s, t] = pas(Hinv, x + 0.5, y + 0.5);
        if (s >= 0 && s <= 1 && t >= 0 && t <= 1) hs.push(helder((y * W + x) * 4));
      }
      hs.sort((a, b) => a - b);
      const ref = hs[Math.floor(hs.length / 2)];
      const N = 5; // 5x5 monsters per pixel
      for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
        let r = 0, g = 0, b = 0, a = 0;
        for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
          const [s, t] = pas(Hinv, x + (i + 0.5) / N, y + (j + 0.5) / N);
          if (s < 0 || s > 1 || t < 0 || t > 1) continue;
          const m = monster(s * (LW - 1), t * (LH - 1));
          r += m[0]; g += m[1]; b += m[2]; a += m[3];
        }
        const n = N * N; a /= n; if (a <= 0) continue;
        r /= n * a; g /= n * a; b /= n * a;
        const o = (y * W + x) * 4;
        const k = Math.max(0.4, Math.min(1.15, Math.pow(helder(o) / KARTON, 0.6)));
        const dek = a * 0.93; // inkt, niet helemaal dekkend
        for (let c = 0; c < 3; c++) {
          const inkt = [r, g, b][c], karton = data[o + c];
          const kleur = Math.min(255, (0.8 * inkt + 0.2 * inkt * karton / 255 * 1.35) * k);
          uit[o + c] = Math.round(karton * (1 - dek) + kleur * dek);
        }
      }
      console.log(naam, 'vlak', v.q[0], 'ref', ref.toFixed(1), 'logo', hoek.map(p => p.map(Math.round).join(',')).join(' '));
    }
    await sharp(uit, { raw: { width: W, height: H, channels: 4 } }).png().toFile(path.join(UIT, `${naam}-logo-480.png`));
  }
})();
