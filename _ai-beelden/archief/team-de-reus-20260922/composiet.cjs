/* Zet het officiële negatieve beeldmerk over de drie nagetekende borstlogo's in team-de-reus.
   node composiet.cjs <bron.webp> <uit.png> [variant]
   Per gebied: oude print maskeren (ver van de mediane stofkleur), harmonisch vullen vanuit de stof,
   luminantie van de gevulde stof als schaduwkaart, merk in de oude doos schalen en vermenigvuldigen. */
const path = require('node:path');
const sharp = require('C:/Users/arnas/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const ROOT = path.resolve(__dirname, '../../..');
const MERK = path.join(ROOT, 'brandbook/assets/logo/dereus-beeldmerk-negatief.png');
const [bron, uit, variant = 'a'] = process.argv.slice(2);
const RATIO = 1043 / 2048;

// zoekgebieden rond de oude prints (met marge), plus per gebied de plaatsing van het nieuwe merk
const GEBIEDEN = {
  links:  { box: { left: 418, top: 594, width: 44, height: 38 }, drempel: 8, verwijd: 8, donkerVrij: 70, extra: [{ x: 439, y: 604, r: 4 }], squeeze: 1, uitHoogte: true, schuin: 0.10 },
  midden: { box: { left: 692, top: 588, width: 52, height: 42 }, drempel: 8, squeeze: 1.0, breedte: 1.0, schuin: 0 },
  rechts: { box: { left: 1004, top: 559, width: 44, height: 40 }, drempel: 8, squeeze: 0.92, breedte: 1.0, schuin: -0.12 },
};
if (variant === 'b') { GEBIEDEN.links.squeeze = 0; } // b: linkermerk helemaal weg (achter de torsorand)

const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const med = arr => { const s = [...arr].sort((x, y) => x - y); return s[s.length >> 1]; };
const BUREN = [[1, 0], [-1, 0], [0, 1], [0, -1]];
const lumC = (d, o) => 0.299 * d[o] + 0.587 * d[o + 1] + 0.114 * d[o + 2];

async function bewerk(naam, g, beeld) {
  const { box } = g;
  const { data, info } = await sharp(beeld).extract(box).raw().toBuffer({ resolveWithObject: true });
  const W = info.width, H = info.height, C = info.channels;
  const px = (x, y) => (y * W + x) * C;
  // stofkleur: mediaan van de buitenste ring van 3 px
  const ring = [[], [], []];
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    if (Math.min(x, y, W - 1 - x, H - 1 - y) > 2) continue;
    for (let c = 0; c < 3; c++) ring[c].push(data[px(x, y) + c]);
  }
  const stof = ring.map(med);
  // masker: geel (rood en groen ruim boven blauw). De glans op de polo is blauwwit en blijft zo stof;
  // de bleke rand om de oude print komt mee door de verwijding van 4 px hieronder.
  let mask = new Uint8Array(W * H);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const o = px(x, y);
    mask[y * W + x] = (data[o] + data[o + 1]) / 2 - data[o + 2] > g.drempel ? 1 : 0;
  }
  // grootste samenhangende component houden (geen deurrand of baksteen meenemen), dan 3 px verwijden
  const lab = new Int32Array(W * H).fill(-1); const groottes = [];
  for (let i = 0; i < W * H; i++) if (mask[i] && lab[i] < 0) {
    const id = groottes.length; const st = [i]; lab[i] = id; let n = 0;
    while (st.length) {
      const k = st.pop(); n++; const x = k % W, y = (k / W) | 0;
      for (const [dx, dy] of BUREN) {
        const nx = x + dx, ny = y + dy;
        if (nx < 0 || ny < 0 || nx >= W || ny >= H) continue;
        const j = ny * W + nx;
        if (mask[j] && lab[j] < 0) { lab[j] = id; st.push(j); }
      }
    }
    groottes.push(n);
  }
  // houden: componenten van minstens 2 px die de rand van het gebied niet raken (haar, baksteen en
  // deurrand raken de rand) en minstens één duidelijk gele pixel bevatten
  const raakt = groottes.map(() => false), kern = groottes.map(() => false);
  for (let i = 0; i < W * H; i++) if (lab[i] >= 0) {
    const x = i % W, y = (i / W) | 0;
    if (x === 0 || y === 0 || x === W - 1 || y === H - 1) raakt[lab[i]] = true;
    if ((data[i * C] + data[i * C + 1]) / 2 - data[i * C + 2] > 12) kern[lab[i]] = true;
  }
  for (let i = 0; i < W * H; i++) mask[i] = lab[i] >= 0 && groottes[lab[i]] >= 2 && !raakt[lab[i]] && kern[lab[i]] ? 1 : 0;
  let bx0 = W, by0 = H, bx1 = 0, by1 = 0;
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (mask[y * W + x]) {
    bx0 = Math.min(bx0, x); by0 = Math.min(by0, y); bx1 = Math.max(bx1, x); by1 = Math.max(by1, y);
  }
  const oud = { x: bx0, y: by0, w: bx1 - bx0 + 1, h: by1 - by0 + 1 };
  // bleke rand en witte glimmers vlak naast de print horen bij de print: heldere pixels binnen 4 px erbij
  if (g.helderRand) {
    let ringL = []; for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (Math.min(x, y, W - 1 - x, H - 1 - y) <= 2) ringL.push(lumC(data, (y * W + x) * C));
    const stofL = med(ringL);
    const dicht = new Uint8Array(mask);
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (!mask[y * W + x] && lumC(data, (y * W + x) * C) > stofL + g.helderRand) {
      let bij = false;
      for (let dy = -4; dy <= 4 && !bij; dy++) for (let dx = -4; dx <= 4; dx++) {
        const nx = x + dx, ny = y + dy; if (nx >= 0 && ny >= 0 && nx < W && ny < H && mask[ny * W + nx]) { bij = true; break; }
      }
      if (bij) dicht[y * W + x] = 1;
    }
    mask = dicht;
  }
  // met de hand aangewezen restjes (witte vuisttop op de schouderglans, niet geel genoeg voor de drempel)
  for (const e of g.extra || []) for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    if (Math.hypot(x + box.left - e.x, y + box.top - e.y) <= e.r) mask[y * W + x] = 1;
  }
  for (let r = 0; r < (g.verwijd || 4); r++) {
    const m2 = new Uint8Array(mask);
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (!mask[y * W + x]) {
      for (const [dx, dy] of BUREN) {
        const nx = x + dx, ny = y + dy;
        if (nx >= 0 && ny >= 0 && nx < W && ny < H && mask[ny * W + nx]) { m2[y * W + x] = 1; break; }
      }
    }
    mask = m2;
  }
  if (process.env.MASKDIR) {
    const dbg = Buffer.alloc(W * H * 3);
    for (let i = 0; i < W * H; i++) for (let c = 0; c < 3; c++) dbg[i * 3 + c] = mask[i] ? (c === 0 ? 255 : 0) : data[i * C + c];
    await sharp(dbg, { raw: { width: W, height: H, channels: 3 } }).resize(W * 8, H * 8, { kernel: 'nearest' }).png().toFile(path.join(process.env.MASKDIR, `mask-${naam}.png`));
  }
  // donkere pixels (de schaduwspleet naast de polo) horen niet bij de print: die blijven staan, zo blijft de rand strak
  if (g.donkerVrij) for (let i = 0; i < W * H; i++) if (mask[i] && lumC(data, i * C) < g.donkerVrij) mask[i] = 0;
  // harmonische vulling: gemaskerde pixels = gemiddelde van de buren, herhaald
  const f = new Float32Array(W * H * 3);
  for (let i = 0; i < W * H; i++) for (let c = 0; c < 3; c++) f[i * 3 + c] = data[i * C + c];
  for (let it = 0; it < 400; it++) for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const i = y * W + x; if (!mask[i]) continue;
    for (let c = 0; c < 3; c++) {
      let s = 0, n = 0;
      for (const [dx, dy] of BUREN) {
        const nx = x + dx, ny = y + dy;
        if (nx >= 0 && ny >= 0 && nx < W && ny < H) { s += f[(ny * W + nx) * 3 + c]; n++; }
      }
      f[i * 3 + c] = s / n;
    }
  }
  // stofkorrel terug: ruis met de halve spreiding van de ongemaskerde stof
  let s1 = 0, s2 = 0, n = 0;
  const lum = i => 0.299 * data[i * C] + 0.587 * data[i * C + 1] + 0.114 * data[i * C + 2];
  for (let y = 1; y < H - 1; y++) for (let x = 1; x < W - 1; x++) {
    const i = y * W + x; if (mask[i]) continue;
    const res = lum(i) - (lum(i - 1) + lum(i + 1) + lum(i - W) + lum(i + W)) / 4; s2 += res * res; s1 += lum(i); n++;
  }
  const gemL = s1 / n; const sd = Math.sqrt(s2 / n) * 0.35;
  let seed = 7; const rnd = () => { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff - 0.5; };
  for (let i = 0; i < W * H; i++) if (mask[i]) { const r = rnd() * sd * 2; for (let c = 0; c < 3; c++) f[i * 3 + c] = clamp(f[i * 3 + c] + r, 0, 255); }
  // nieuw merk: breedte van de oude doos, hoogte uit de merkverhouding, horizontaal geknepen als de borst wegdraait
  let laag = null;
  if (g.squeeze > 0) {
    const mw = g.uitHoogte ? Math.round(oud.h / RATIO) : Math.round(oud.w * g.breedte);
    const mh = Math.round(mw * RATIO);
    const sw = Math.max(4, g.uitHoogte ? oud.w : Math.round(mw * g.squeeze));
    let m = sharp(MERK).resize(mw * 4, mh * 4, { fit: 'fill' });
    if (g.schuin) m = m.affine([[1, g.schuin], [0, 1]], { background: { r: 0, g: 0, b: 0, alpha: 0 } });
    const mb = await m.resize(sw, mh, { fit: 'fill', kernel: 'lanczos3' }).blur(0.6).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
    laag = { buf: mb.data, w: mb.info.width, h: mb.info.height,
      x: Math.round(oud.x + oud.w / 2 - mb.info.width / 2), y: Math.round(oud.y + oud.h / 2 - mb.info.height / 2) };
  }
  const Lk = new Float32Array(W * H);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    let s = 0, k = 0;
    for (let dy = -2; dy <= 2; dy++) for (let dx = -2; dx <= 2; dx++) {
      const nx = x + dx, ny = y + dy; if (nx < 0 || ny < 0 || nx >= W || ny >= H) continue;
      const j = (ny * W + nx) * 3; s += 0.299 * f[j] + 0.587 * f[j + 1] + 0.114 * f[j + 2]; k++;
    }
    Lk[y * W + x] = clamp(s / k / gemL, 0.55, 1.25);
  }
  const out = Buffer.alloc(W * H * 4);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const i = y * W + x;
    let r = f[i * 3], gg = f[i * 3 + 1], b = f[i * 3 + 2];
    if (laag) {
      const lx = x - laag.x, ly = y - laag.y;
      if (lx >= 0 && ly >= 0 && lx < laag.w && ly < laag.h) {
        const o = (ly * laag.w + lx) * 4; const a = laag.buf[o + 3] / 255 * 0.96;
        const L = Lk[i];
        r = r * (1 - a) + laag.buf[o] * L * a; gg = gg * (1 - a) + laag.buf[o + 1] * L * a; b = b * (1 - a) + laag.buf[o + 2] * L * a;
      }
    }
    out[i * 4] = clamp(r, 0, 255); out[i * 4 + 1] = clamp(gg, 0, 255); out[i * 4 + 2] = clamp(b, 0, 255); out[i * 4 + 3] = 255;
  }
  console.log(`${naam}: stof rgb(${stof.join(',')}), oude print ${oud.w}x${oud.h} op (${box.left + oud.x},${box.top + oud.y})` + (laag ? `, nieuw merk ${laag.w}x${laag.h}` : ', geen merk'));
  return { input: await sharp(out, { raw: { width: W, height: H, channels: 4 } }).png().toBuffer(), left: box.left, top: box.top };
}

(async () => {
  const overlays = [];
  for (const [naam, g] of Object.entries(GEBIEDEN)) overlays.push(await bewerk(naam, g, bron));
  await sharp(bron).composite(overlays).removeAlpha().png().toFile(uit);
  console.log('geschreven', uit);
})().catch(e => { console.error(e); process.exitCode = 1; });
