// Masker van imgly repareren: witte vlakken (scherm, kaart, papier) weer dicht, randen hard, bijsnijden.
// node masker.cjs <bron> <vrij.png> <uit.png> [licht-drempel]
// - alpha hard: a<100 -> 0, a>200 -> 255, ertussen lineair
// - gaten vullen: alles wat vanaf de beeldrand niet bereikbaar is over doorzichtige pixels, wordt dicht
// - licht-drempel (optioneel): pixels lichter dan die waarde tellen ook als voorwerp (witte kaart op grijs)
const sharp = require('sharp');
(async () => {
  const [bron, vrij, uit, drempel, doorlaatArg] = process.argv.slice(2); const doorlaat = +(doorlaatArg || 128);
  const { data, info } = await sharp(bron).removeAlpha().raw().toBuffer({ resolveWithObject: true });
  const W = info.width, H = info.height;
  const a0 = await sharp(vrij).ensureAlpha().extractChannel(3).raw().toBuffer();
  const a = new Uint8ClampedArray(W * H);
  for (let i = 0; i < W * H; i++) {
    let v = Math.max(0, Math.min(255, (a0[i] - 100) * 255 / 100));
    if (drempel) {
      const l = (data[i * 3] + data[i * 3 + 1] + data[i * 3 + 2]) / 3;
      const d = +drempel;
      v = Math.max(v, Math.max(0, Math.min(255, (l - (d - 8)) * 255 / 8)));
    }
    a[i] = v;
  }
  // gaten vullen
  const bereikt = new Uint8Array(W * H), stapel = [];
  const duw = (x, y) => { const i = y * W + x; if (!bereikt[i] && a[i] < doorlaat) { bereikt[i] = 1; stapel.push(i); } };
  for (let x = 0; x < W; x++) { duw(x, 0); duw(x, H - 1); }
  for (let y = 0; y < H; y++) { duw(0, y); duw(W - 1, y); }
  while (stapel.length) {
    const i = stapel.pop(), x = i % W, y = (i / W) | 0;
    if (x > 0) duw(x - 1, y); if (x < W - 1) duw(x + 1, y); if (y > 0) duw(x, y - 1); if (y < H - 1) duw(x, y + 1);
  }
  let gevuld = 0;
  // GEEN_VUL=1: gaten laten staan (headset, plant: de ruimte binnen de beugel en tussen de bladeren is echt leeg)
  if (!process.env.GEEN_VUL) for (let i = 0; i < W * H; i++) if (!bereikt[i] && a[i] < 255) { gevuld++; a[i] = 255; }
  // kleine losse vlekjes weg: alleen de grootste samenhangende vorm blijft
  const lab = new Int32Array(W * H), maten = [0];
  for (let s = 0; s < W * H; s++) {
    if (a[s] < 128 || lab[s]) continue;
    const id = maten.length; let n = 0; const st = [s]; lab[s] = id;
    while (st.length) {
      const i = st.pop(); n++; const x = i % W, y = (i / W) | 0;
      for (const j of [x > 0 ? i - 1 : -1, x < W - 1 ? i + 1 : -1, y > 0 ? i - W : -1, y < H - 1 ? i + W : -1])
        if (j >= 0 && !lab[j] && a[j] >= 128) { lab[j] = id; st.push(j); }
    }
    maten.push(n);
  }
  const groot = maten.indexOf(Math.max(...maten.slice(1)));
  // dilateer het label van de grootste vorm 3 px om de zachte rand te houden
  const houd = new Uint8Array(W * H);
  for (let i = 0; i < W * H; i++) if (lab[i] === groot) houd[i] = 1;
  for (let r = 0; r < 3; r++) {
    const k = houd.slice();
    for (let y = 1; y < H - 1; y++) for (let x = 1; x < W - 1; x++) { const i = y * W + x; if (k[i - 1] || k[i + 1] || k[i - W] || k[i + W]) houd[i] = 1; }
  }
  let x0 = W, y0 = H, x1 = 0, y1 = 0;
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const i = y * W + x; if (!houd[i]) a[i] = 0;
    if (a[i] > 8) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
  }
  const rgba = Buffer.alloc(W * H * 4);
  for (let i = 0; i < W * H; i++) { rgba[i * 4] = data[i * 3]; rgba[i * 4 + 1] = data[i * 3 + 1]; rgba[i * 4 + 2] = data[i * 3 + 2]; rgba[i * 4 + 3] = a[i]; }
  const p = 4; x0 = Math.max(0, x0 - p); y0 = Math.max(0, y0 - p); x1 = Math.min(W - 1, x1 + p); y1 = Math.min(H - 1, y1 + p);
  await sharp(rgba, { raw: { width: W, height: H, channels: 4 } }).extract({ left: x0, top: y0, width: x1 - x0 + 1, height: y1 - y0 + 1 }).png().toFile(uit);
  console.log(uit, 'bbox', x0, y0, x1 - x0 + 1, y1 - y0 + 1, 'gevuld', gevuld, 'vormen', maten.length - 1);
})();
