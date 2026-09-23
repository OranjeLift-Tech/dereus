/* Herstel de merkprints in de bronfoto van dienst-woningontruiming (1184x896).
   Per gebied: oude print maskeren op chromaticiteit (ver van de mediane stofkleur), wegvullen vanuit de stof
   eromheen, de luminantie van de gevulde stof als schaduwkaart houden, het officiele merk erin vermenigvuldigen.
   node herstel.cjs <bron.png> <uit.png> <jobs.json>  */
const fs = require('node:fs');
const path = require('node:path');
const sharp = require('C:/Users/arnas/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const LOGO = 'C:/users/arnas/git_repos/dereus/brandbook/assets/logo/';

const [, , bron, uit, jobsPad] = process.argv;
const JOBS = JSON.parse(fs.readFileSync(jobsPad || path.join(__dirname, 'jobs.json'), 'utf8'));

function blurBox(src, w, h, r, weight) {
  // separabele boxblur van src (Float32, 1 kanaal) met gewichtskaart; geeft [som, gewichtsom]
  const tmpS = new Float32Array(w * h), tmpW = new Float32Array(w * h);
  const outS = new Float32Array(w * h), outW = new Float32Array(w * h);
  const cx = (x) => Math.min(w - 1, Math.max(0, x));
  const cy = (y) => Math.min(h - 1, Math.max(0, y));
  for (let y = 0; y < h; y++) {
    let s = 0, ws = 0;
    for (let x = -r; x <= r; x++) { const xx = cx(x); s += src[y * w + xx] * weight[y * w + xx]; ws += weight[y * w + xx]; }
    for (let x = 0; x < w; x++) {
      tmpS[y * w + x] = s; tmpW[y * w + x] = ws;
      const xo = cx(x - r), xi = cx(x + r + 1);
      s += src[y * w + xi] * weight[y * w + xi] - src[y * w + xo] * weight[y * w + xo];
      ws += weight[y * w + xi] - weight[y * w + xo];
    }
  }
  for (let x = 0; x < w; x++) {
    let s = 0, ws = 0;
    for (let y = -r; y <= r; y++) { const yy = cy(y); s += tmpS[yy * w + x]; ws += tmpW[yy * w + x]; }
    for (let y = 0; y < h; y++) {
      outS[y * w + x] = s; outW[y * w + x] = ws;
      const yo = cy(y - r), yi = cy(y + r + 1);
      s += tmpS[yi * w + x] - tmpS[yo * w + x];
      ws += tmpW[yi * w + x] - tmpW[yo * w + x];
    }
  }
  return [outS, outW];
}
function gauss() { let u = 0, v = 0; while (u === 0) u = Math.random(); while (v === 0) v = Math.random(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }

(async () => {
  const meta = await sharp(bron).metadata();
  const W = meta.width, H = meta.height;
  const beeld = await sharp(bron).removeAlpha().raw().toBuffer();
  for (const job of JOBS) {
    const { left, top, width: w, height: h } = job.gebied;
    const ch = [new Float32Array(w * h), new Float32Array(w * h), new Float32Array(w * h)];
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) for (let c = 0; c < 3; c++) ch[c][y * w + x] = beeld[((top + y) * W + left + x) * 3 + c];

    // 1. mediane stofkleur uit de rand van het gebied
    const buiten = new Uint8Array(w * h);
    if (job.buiten) for (const r of job.buiten) for (let y = r.top; y < r.top + r.height; y++) for (let x = r.left; x < r.left + r.width; x++) if (x >= 0 && y >= 0 && x < w && y < h) buiten[y * w + x] = 1;
    const blauw = (i) => ch[2][i] > 1.5 * ch[1][i] && ch[2][i] > 4 * ch[0][i];   // stof: blauw domineert duidelijk
    const ring = [];
    const RING = job.ring || 5;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (Math.min(x, y, w - 1 - x, h - 1 - y) < RING && !buiten[y * w + x] && blauw(y * w + x)) ring.push(y * w + x);
    const med = [0, 1, 2].map(c => { const v = ring.map(i => ch[c][i]).sort((a, b) => a - b); return v[v.length >> 1]; });
    const medSom = med[0] + med[1] + med[2];
    const medChr = med.map(v => v / medSom);
    const medLum = 0.299 * med[0] + 0.587 * med[1] + 0.114 * med[2];

    // 2. masker: chromaticiteit ver van de stof (schaduwplooien houden dezelfde chromaticiteit)
    const mask = new Uint8Array(w * h);
    let nMask = 0;
    for (let i = 0; i < w * h; i++) {
      const som = ch[0][i] + ch[1][i] + ch[2][i] || 1;
      let d = 0;
      for (let c = 0; c < 3; c++) d += (ch[c][i] / som - medChr[c]) ** 2;
      const lum = 0.299 * ch[0][i] + 0.587 * ch[1][i] + 0.114 * ch[2][i];
      if (buiten[i] || blauw(i)) continue;
      if (Math.sqrt(d) > (job.drempel || 0.055) || lum > medLum * (job.lichtFactor || 1.6)) { mask[i] = 1; nMask++; }
    }
    if (job.extraMask) for (const r of job.extraMask) for (let y = r.top; y < r.top + r.height; y++) for (let x = r.left; x < r.left + r.width; x++) mask[y * w + x] = 1;
    if (job.nooitMask) for (const r of job.nooitMask) for (let y = r.top; y < r.top + r.height; y++) for (let x = r.left; x < r.left + r.width; x++) mask[y * w + x] = 0;
    // dilatie: de lichte halo rond de print meenemen
    const DIL = job.dilatie == null ? 2 : job.dilatie;
    const mask2 = new Uint8Array(mask);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (!mask[y * w + x]) {
      let hit = false;
      for (let dy = -DIL; dy <= DIL && !hit; dy++) for (let dx = -DIL; dx <= DIL; dx++) {
        const xx = x + dx, yy = y + dy;
        if (xx >= 0 && yy >= 0 && xx < w && yy < h && mask[yy * w + xx]) { hit = true; break; }
      }
      if (hit && !buiten[y * w + x]) mask2[y * w + x] = 1;
    }
    // 3. grain van de stof meten (hoogfrequent deel van de ongemaskerde pixels)
    const known = new Float32Array(w * h); for (let i = 0; i < w * h; i++) known[i] = (mask2[i] || buiten[i]) ? 0 : 1;
    let grain = 0;
    {
      const [s, ws] = blurBox(ch[1], w, h, 2, known);
      let n = 0, acc = 0;
      for (let i = 0; i < w * h; i++) if (known[i] && ws[i] > 0) { const d = ch[1][i] - s[i] / ws[i]; acc += d * d; n++; }
      grain = Math.sqrt(acc / Math.max(1, n));
    }
    // 4. wegvullen: push-pull, van buiten naar binnen
    const fill = ch.map(c => Float32Array.from(c));
    const kn = Float32Array.from(known);
    for (let pas = 0; pas < 80; pas++) {
      let open = 0;
      const res = fill.map(c => blurBox(c, w, h, 3, kn));
      const next = Float32Array.from(kn);
      for (let i = 0; i < w * h; i++) if (!kn[i] && !buiten[i]) {
        if (res[0][1][i] > 0.5) { for (let c = 0; c < 3; c++) fill[c][i] = res[c][0][i] / res[c][1][i]; next[i] = 1; }
        else open++;
      }
      kn.set(next);
      if (!open) break;
    }
    // 5. gladstrijken van het gevulde deel, zachte overgang naar de echte stof
    const ones = new Float32Array(w * h).fill(1);
    const binnen = Float32Array.from(buiten, v => 1 - v);
    const soft = fill.map(c => { const [s, ws] = blurBox(c, w, h, job.glad || 4, binnen); return s.map((v, i) => ws[i] ? v / ws[i] : c[i]); });
    const [fm, fw] = blurBox(Float32Array.from(mask2, v => v), w, h, 3, ones);
    const grainF = job.grainFactor == null ? 0.9 : job.grainFactor;
    for (let i = 0; i < w * h; i++) {
      const a = buiten[i] ? 0 : fm[i] / fw[i];   // 0 = stof, 1 = midden in de oude print
      const g = gauss() * grain * grainF;
      for (let c = 0; c < 3; c++) fill[c][i] = ch[c][i] * (1 - a) + (soft[c][i] + g) * a;
    }
    // 6. schaduwkaart = luminantie van de gevulde stof t.o.v. de mediaan
    const shade = new Float32Array(w * h);
    for (let i = 0; i < w * h; i++) shade[i] = Math.min(1.35, Math.max(0.45, (0.299 * fill[0][i] + 0.587 * fill[1][i] + 0.114 * fill[2][i]) / medLum));
    // 7. het merk erin
    let lg = sharp(LOGO + job.logo).resize({ width: job.plaats.breedte });
    if (job.plaats.hoogteFactor) {
      const m = await sharp(await lg.png().toBuffer()).metadata();
      lg = sharp(LOGO + job.logo).resize({ width: job.plaats.breedte, height: Math.round(m.height * job.plaats.hoogteFactor), fit: 'fill' });
    }
    if (job.plaats.rotatie) lg = sharp(await lg.png().toBuffer()).rotate(job.plaats.rotatie, { background: { r: 0, g: 0, b: 0, alpha: 0 } });
    if (job.plaats.blur) lg = sharp(await lg.png().toBuffer()).blur(job.plaats.blur);
    const { data: ld, info: li } = await lg.ensureAlpha().raw().toBuffer({ resolveWithObject: true });
    const lx = Math.round(job.plaats.cx - li.width / 2), ly = Math.round(job.plaats.cy - li.height / 2);
    const dek = job.dek == null ? 0.97 : job.dek;
    for (let y = 0; y < li.height; y++) for (let x = 0; x < li.width; x++) {
      const px = lx + x, py = ly + y;
      if (px < 0 || py < 0 || px >= w || py >= h || buiten[py * w + px]) continue;
      const a = ld[(y * li.width + x) * 4 + 3] / 255 * dek;
      if (!a) continue;
      const i = py * w + px;
      const g = gauss() * grain * 0.6;
      for (let c = 0; c < 3; c++) {
        const ink = ld[(y * li.width + x) * 4 + c] * shade[i] + g;
        fill[c][i] = fill[c][i] * (1 - a) + Math.min(255, Math.max(0, ink)) * a;
      }
    }
    // terugschrijven
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) for (let c = 0; c < 3; c++) beeld[((top + y) * W + left + x) * 3 + c] = Math.round(Math.min(255, Math.max(0, fill[c][y * w + x])));
    // maskerbeeld voor controle: rood = na dilatie, geel = ruwe maskering
    const mk = Buffer.alloc(w * h * 3);
    for (let i = 0; i < w * h; i++) { mk[i * 3] = mask2[i] ? 255 : 0; mk[i * 3 + 1] = mask[i] ? 255 : 0; mk[i * 3 + 2] = buiten[i] ? 255 : 0; }
    await sharp(mk, { raw: { width: w, height: h, channels: 3 } }).resize({ width: w * 2, kernel: 'nearest' }).png().toFile(uit.replace(/\.png$/, `-masker-${job.naam}.png`));
    console.log(`${job.naam}: stof mediaan rgb(${med.join(',')}) lum ${medLum.toFixed(0)}  masker ${nMask} px (+dilatie)  grain s ${grain.toFixed(1)}  logo ${li.width}x${li.height} op ${lx},${ly}`);
  }
  await sharp(beeld, { raw: { width: W, height: H, channels: 3 } }).png().toFile(uit);
  console.log('geschreven', uit);
})().catch(e => { console.error(e); process.exitCode = 1; });
