// Vind een licht vlak (scherm, kaart, papier) in een uitsnede: masker + vier hoeken.
// node vlak.cjs <in.png> <zaadx> <zaady> <lichtgrens> <uit-masker.png>
// Vult vanaf het zaadpunt alle pixels met helderheid > lichtgrens, maakt daar een masker van
// en past vier rechte lijnen op de rand (de afgeronde hoeken tellen niet mee), zodat je scherpe hoeken krijgt.
const sharp = require('sharp');
(async () => {
  const [inp, sx, sy, grens, uit] = process.argv.slice(2);
  const { data, info } = await sharp(inp).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  const W = info.width, H = info.height, g = +grens;
  const lum = i => (data[i * 4] + data[i * 4 + 1] + data[i * 4 + 2]) / 3;
  const m = new Uint8Array(W * H), st = [+sy * W + +sx];
  m[st[0]] = 1;
  while (st.length) {
    const i = st.pop(), x = i % W, y = (i / W) | 0;
    for (const j of [x > 0 ? i - 1 : -1, x < W - 1 ? i + 1 : -1, y > 0 ? i - W : -1, y < H - 1 ? i + W : -1])
      if (j >= 0 && !m[j] && data[j * 4 + 3] > 200 && lum(j) > g) { m[j] = 1; st.push(j); }
  }
  // randpixels
  const rand = [];
  for (let y = 1; y < H - 1; y++) for (let x = 1; x < W - 1; x++) {
    const i = y * W + x; if (m[i] && (!m[i - 1] || !m[i + 1] || !m[i - W] || !m[i + W])) rand.push([x, y]);
  }
  // ruwe hoeken: uiterste punten links, boven, rechts, onder (vlak staat schuin) of +-x+-y (vlak staat recht)
  const recht = process.env.RECHT === '1';
  const kies = f => rand.reduce((b, p) => (f(p) > f(b) ? p : b));
  let hoeken = recht
    ? [kies(p => -p[0] - p[1]), kies(p => p[0] - p[1]), kies(p => p[0] + p[1]), kies(p => -p[0] + p[1])]
    : [kies(p => -p[0]), kies(p => -p[1]), kies(p => p[0]), kies(p => p[1])];
  // lijnen passen per zijde (punten dichter bij het midden van de zijde dan bij de hoeken)
  const lijn = (a, b) => {
    const len = Math.hypot(b[0] - a[0], b[1] - a[1]), ux = (b[0] - a[0]) / len, uy = (b[1] - a[1]) / len;
    const pts = rand.filter(p => {
      const t = ((p[0] - a[0]) * ux + (p[1] - a[1]) * uy) / len, d = Math.abs((p[0] - a[0]) * uy - (p[1] - a[1]) * ux);
      return t > 0.2 && t < 0.8 && d < len * 0.06;
    });
    // totale kleinste kwadraten: richting via covariantie
    const mx = pts.reduce((s, p) => s + p[0], 0) / pts.length, my = pts.reduce((s, p) => s + p[1], 0) / pts.length;
    let sxx = 0, syy = 0, sxy = 0; for (const p of pts) { sxx += (p[0] - mx) ** 2; syy += (p[1] - my) ** 2; sxy += (p[0] - mx) * (p[1] - my); }
    const hoek = 0.5 * Math.atan2(2 * sxy, sxx - syy);
    return { mx, my, dx: Math.cos(hoek), dy: Math.sin(hoek), n: pts.length };
  };
  const snij = (l1, l2) => {
    const det = l1.dx * (-l2.dy) - l1.dy * (-l2.dx);
    const t = ((l2.mx - l1.mx) * (-l2.dy) - (l2.my - l1.my) * (-l2.dx)) / det;
    return [+(l1.mx + t * l1.dx).toFixed(1), +(l1.my + t * l1.dy).toFixed(1)];
  };
  const L = [0, 1, 2, 3].map(k => lijn(hoeken[k], hoeken[(k + 1) % 4]));
  const scherp = [0, 1, 2, 3].map(k => snij(L[(k + 3) % 4], L[k]));
  const out = Buffer.alloc(W * H * 4);
  for (let i = 0; i < W * H; i++) { out[i * 4] = out[i * 4 + 1] = out[i * 4 + 2] = 255; out[i * 4 + 3] = m[i] ? 255 : 0; }
  await sharp(out, { raw: { width: W, height: H, channels: 4 } }).blur(0.8).png().toFile(uit);
  console.log(JSON.stringify({ W, H, ruw: hoeken, hoeken: scherp, punten: L.map(l => l.n), pixels: m.reduce((s, v) => s + v, 0) }));
})();
