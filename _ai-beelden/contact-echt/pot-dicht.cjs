// node pot-dicht.cjs <m.png> <uit.png> <rand-deel> : de pot dicht tussen zijn randen; die randen gemeten op twee rijen
// onder de bladeren (0,82 en 0,96 van de hoogte) en lineair doorgetrokken tot de potrand
const sharp = require('sharp');
(async () => {
  const [inp, uit, deel] = process.argv.slice(2);
  const { data, info } = await sharp(inp).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  const W = info.width, H = info.height;
  const randen = y => { let x0 = -1, x1 = -1; for (let x = 0; x < W; x++) { if (data[(y * W + x) * 4 + 3] > 128) { if (x0 < 0) x0 = x; x1 = x; } } return [x0, x1]; };
  const ya = Math.round(H * .82), yb = Math.round(H * .96), [a0, a1] = randen(ya), [b0, b1] = randen(yb);
  console.log('randen', ya, a0, a1, yb, b0, b1);
  for (let y = Math.round(H * +deel); y < H; y++) {
    const t = (y - ya) / (yb - ya), x0 = Math.round(a0 + (b0 - a0) * t) + 3, x1 = Math.round(a1 + (b1 - a1) * t) - 3;
    for (let x = x0; x <= x1; x++) { const i = (y * W + x) * 4 + 3; if (data[i] > 12) data[i] = 255; }   // alleen wat imgly half liet staan
  }
  await sharp(data, { raw: info }).png().toFile(uit);
})();
