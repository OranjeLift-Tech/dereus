// Vervangt de drie verzonnen merktekens in verhuisdag-aankomst door het officiële beeldmerk.
// Techniek: oude print maskeren (ver van de mediaan-stofkleur), wegvullen uit de omgeving,
// luminantie van de vulling als schaduwkaart, officieel merk erin schalen en vermenigvuldigen.
const sharp = require('C:/Users/arnas/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const path = require('node:path');
const fs = require('node:fs');
const root = path.resolve(__dirname, '../../..');
const src = path.join(root, 'website/review/beeld-verhuisdag-aankomst-ronde-1/origineel/verhuisdag-aankomst.webp');
const out = process.argv[2];
const NEG = path.join(root, 'brandbook/assets/logo/dereus-beeldmerk-negatief.png');
const KLEUR = path.join(root, 'brandbook/assets/logo/dereus-beeldmerk.png');
const MARK_RATIO = 2048 / 1043;

// Per gebied: vak (met marge), drempel voor "is print", dilatie, en waar en hoe groot het merk komt.
const JOBS = [
  { name: 'polo-links', box: { left: 596, top: 350, width: 52, height: 54 }, thr: 38, dil: 3,
    mark: NEG, cx: 620, cy: 379, h: 19, squeeze: 0.66, tint: [222, 228, 236], yellow: [255, 206, 60] },
  { name: 'polo-rechts', box: { left: 984, top: 362, width: 60, height: 62 }, thr: 38, dil: 3,
    mark: NEG, cx: 1013, cy: 393, h: 22, squeeze: 0.80, tint: [214, 222, 232], yellow: [250, 200, 56] },
  // bus: de lichte plaat achter het oude merk gaat helemaal weg; vast maskervak, vulling als vlak (paneel is een egale gradient)
  { name: 'bus', box: { left: 298, top: 471, width: 172, height: 107 }, maskRect: { left: 305, top: 474, width: 160, height: 90, r: 18 }, dirs: [[-1, 0], [1, 0], [0, 1]], blur: 4,
    mark: KLEUR, cx: 383, cy: 517, w: 120, squeeze: 1.0, tint: null, yellow: null },
];

function median(arr) { const a = [...arr].sort((p, q) => p - q); return a[a.length >> 1]; }

async function run() {
  const img = sharp(src);
  const { data, info } = await img.raw().toBuffer({ resolveWithObject: true });
  const W = info.width, H = info.height, C = info.channels;
  const px = (x, y) => (y * W + x) * C;
  const overlays = [];
  const debug = [];

  for (const job of JOBS) {
    const { left, top, width: w, height: h } = job.box;
    // mediaan van de rand (stof of buspaneel)
    const ring = [[], [], []];
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      if (Math.min(x, y, w - 1 - x, h - 1 - y) > 3) continue;
      for (let c = 0; c < 3; c++) ring[c].push(data[px(left + x, top + y) + c]);
    }
    const med = ring.map(median);
    // masker: ver van de mediaan
    let mask = new Uint8Array(w * h);
    if (job.maskRect) {
      const m = job.maskRect;
      for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
        const X = left + x, Y = top + y;
        const dx = Math.max(m.left + m.r - X, X - (m.left + m.width - 1 - m.r), 0);
        const dy = Math.max(m.top + m.r - Y, Y - (m.top + m.height - 1 - m.r), 0);
        const inside = X >= m.left && X < m.left + m.width && Y >= m.top && Y < m.top + m.height && Math.hypot(dx, dy) <= m.r;
        mask[y * w + x] = inside ? 1 : 0;
      }
    } else for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const o = px(left + x, top + y);
      const d = Math.hypot(data[o] - med[0], data[o + 1] - med[1], data[o + 2] - med[2]);
      mask[y * w + x] = d > job.thr ? 1 : 0;
    }
    // rand nooit maskeren, dilateren
    for (let it = 0; it < (job.dil || 0); it++) {
      const m2 = new Uint8Array(mask);
      for (let y = 1; y < h - 1; y++) for (let x = 1; x < w - 1; x++) {
        if (mask[y * w + x]) continue;
        if (mask[y * w + x - 1] || mask[y * w + x + 1] || mask[(y - 1) * w + x] || mask[(y + 1) * w + x]) m2[y * w + x] = 1;
      }
      mask = m2;
    }
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (Math.min(x, y, w - 1 - x, h - 1 - y) < 2) mask[y * w + x] = 0;

    // vulling: gewogen gemiddelde van de dichtstbijzijnde niet-gemaskerde pixels in vier richtingen
    const fill = new Float32Array(w * h * 3);
    let plane = null;
    if (job.fill === 'plane') {
      // kleinste kwadraten: v = a + b*x + c*y per kanaal, uit de niet-gemaskerde pixels
      plane = [];
      for (let c = 0; c < 3; c++) {
        let n = 0, sx = 0, sy = 0, sxx = 0, syy = 0, sxy = 0, sv = 0, svx = 0, svy = 0;
        for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
          if (mask[y * w + x]) continue;
          if (job.planeMargin) { // pixels vlak naast het masker (de halo) niet meenemen in de fit
            let near = false;
            for (let dy = -job.planeMargin; dy <= job.planeMargin && !near; dy++) for (let dx = -job.planeMargin; dx <= job.planeMargin; dx++) {
              const yy = y + dy, xx = x + dx; if (yy < 0 || yy >= h || xx < 0 || xx >= w) continue; if (mask[yy * w + xx]) { near = true; break; }
            }
            if (near) continue;
          }
          const v = data[px(left + x, top + y) + c];
          n++; sx += x; sy += y; sxx += x * x; syy += y * y; sxy += x * y; sv += v; svx += v * x; svy += v * y;
        }
        // normaalvergelijkingen oplossen (3x3) met Cramer
        const A = [[n, sx, sy], [sx, sxx, sxy], [sy, sxy, syy]], B = [sv, svx, svy];
        const det = m => m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]);
        const D = det(A);
        const col = (i) => A.map((row, r) => row.map((v, j) => j === i ? B[r] : v));
        plane.push([det(col(0)) / D, det(col(1)) / D, det(col(2)) / D]);
      }
    }
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const o = px(left + x, top + y);
      if (!mask[y * w + x]) { for (let c = 0; c < 3; c++) fill[(y * w + x) * 3 + c] = data[o + c]; continue; }
      if (plane) { for (let c = 0; c < 3; c++) fill[(y * w + x) * 3 + c] = plane[c][0] + plane[c][1] * x + plane[c][2] * y; continue; }
      let sw = 0; const acc = [0, 0, 0];
      for (const [dx, dy] of (job.dirs || [[-1, 0], [1, 0], [0, -1], [0, 1]])) {
        let xx = x, yy = y, dist = 0;
        while (xx >= 0 && xx < w && yy >= 0 && yy < h && mask[yy * w + xx]) { xx += dx; yy += dy; dist++; }
        if (xx < 0 || xx >= w || yy < 0 || yy >= h) continue;
        const wgt = 1 / (dist * dist);
        const oo = px(left + xx, top + yy);
        for (let c = 0; c < 3; c++) acc[c] += data[oo + c] * wgt;
        sw += wgt;
      }
      for (let c = 0; c < 3; c++) fill[(y * w + x) * 3 + c] = sw ? acc[c] / sw : med[c];
    }
    // lichte vervaging binnen het masker tegen naden
    let blurred = new Float32Array(fill);
    for (let pass = 0; pass < (job.blur || 1); pass++) {
      const srcB = blurred; blurred = new Float32Array(srcB);
      for (let y = 1; y < h - 1; y++) for (let x = 1; x < w - 1; x++) {
        if (!mask[y * w + x]) continue;
        for (let c = 0; c < 3; c++) {
          let s = 0;
          for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) s += srcB[((y + dy) * w + x + dx) * 3 + c];
          blurred[(y * w + x) * 3 + c] = s / 9;
        }
      }
    }

    // schaduwkaart: luminantie / mediaanluminantie
    const medL = 0.299 * med[0] + 0.587 * med[1] + 0.114 * med[2];

    // merk renderen
    const mh = job.h || Math.round(job.w / MARK_RATIO), mw = job.w || Math.round(mh * MARK_RATIO * job.squeeze);
    const mark = await sharp(job.mark).resize(mw, mh, { fit: 'fill', kernel: 'lanczos3' }).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
    const mx0 = Math.round(job.cx - mw / 2) - left, my0 = Math.round(job.cy - mh / 2) - top;

    const outBuf = Buffer.alloc(w * h * 4);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const i = y * w + x;
      let r = blurred[i * 3], g = blurred[i * 3 + 1], b = blurred[i * 3 + 2];
      const L = 0.299 * r + 0.587 * g + 0.114 * b;
      const shade = Math.max(0.3, Math.min(1.4, L / medL));
      const mxx = x - mx0, myy = y - my0;
      if (mxx >= 0 && mxx < mw && myy >= 0 && myy < mh) {
        const mo = (myy * mw + mxx) * 4;
        const a = mark.data[mo + 3] / 255;
        if (a > 0) {
          let mr = mark.data[mo], mg = mark.data[mo + 1], mb = mark.data[mo + 2];
          if (job.tint) {
            const isYellow = mr > 200 && mb < 120;
            if (isYellow) [mr, mg, mb] = job.yellow; else [mr, mg, mb] = job.tint;
            mr *= shade; mg *= shade; mb *= shade;
          } else {
            // kleurenmerk op wit paneel: vermenigvuldigen met het paneel (folie in hetzelfde licht)
            mr *= r / 255; mg *= g / 255; mb *= b / 255;
          }
          r = r * (1 - a) + mr * a; g = g * (1 - a) + mg * a; b = b * (1 - a) + mb * a;
        }
      }
      outBuf[i * 4] = Math.max(0, Math.min(255, r)); outBuf[i * 4 + 1] = Math.max(0, Math.min(255, g)); outBuf[i * 4 + 2] = Math.max(0, Math.min(255, b));
      const edge = Math.min(x, y, w - 1 - x, h - 1 - y);
      outBuf[i * 4 + 3] = Math.round(255 * Math.min(1, edge / 3));
    }
    overlays.push({ input: await sharp(outBuf, { raw: { width: w, height: h, channels: 4 } }).png().toBuffer(), left, top });
    debug.push({ name: job.name, med, maskPixels: mask.reduce((a, b) => a + b, 0), mark: { w: mw, h: mh, x: mx0 + left, y: my0 + top } });
  }
  const final = await sharp(src).composite(overlays).png().toBuffer();
  fs.writeFileSync(out, final);
  console.log(JSON.stringify(debug, null, 1));
}
run().catch(e => { console.error(e); process.exitCode = 1; });
