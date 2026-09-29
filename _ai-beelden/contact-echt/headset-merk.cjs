// node headset-merk.cjs <in.png> <uit.png> : het merkteken op de oorschelp van dJ2hnNSqsmk weg. De lichte pixels in het
// vak (bronpixels van de uitsnede na masker.cjs) worden ingekleurd vanuit hun buren (diffusie) en dichtgezet.
const sharp = require('sharp');
(async () => {
  const [inp, uit] = process.argv.slice(2);
  const { data, info } = await sharp(inp).raw().toBuffer({ resolveWithObject: true });
  const W = info.width, x0 = 620, x1 = 672, y0 = 664, y1 = 750;
  const lum = i => (data[i * 4] + data[i * 4 + 1] + data[i * 4 + 2]) / 3;
  // referentie: mediaan-helderheid van de schijf rond het vak
  const gat = new Set();
  for (let y = y0; y < y1; y++) for (let x = x0; x < x1; x++) { const i = y * W + x; if (lum(i) > 150 || (data[i*4+2] > data[i*4] + 25)) gat.add(i); }
  // groei 2 px zodat de antialiasrand meegaat
  for (let r = 0; r < 2; r++) for (const i of [...gat]) for (const j of [i - 1, i + 1, i - W, i + W]) gat.add(j);
  for (let it = 0; it < 400; it++) {
    for (const i of gat) {
      let s = [0, 0, 0], n = 0;
      for (const j of [i - 1, i + 1, i - W, i + W]) if (it > 0 || !gat.has(j)) { s[0] += data[j * 4]; s[1] += data[j * 4 + 1]; s[2] += data[j * 4 + 2]; n++; }
      if (n) for (let c = 0; c < 3; c++) data[i * 4 + c] = s[c] / n;
      data[i * 4 + 3] = 255;
    }
  }
  await sharp(data, { raw: info }).png().toFile(uit);
  console.log('pixels', gat.size);
})();
