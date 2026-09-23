// Controlevel per kandidaat: elk gezicht en elke hand uitvergroot naast elkaar.
// Boxen staan in de coordinaten van een 1000 px brede weergave; het bronbeeld is 2048.
const sharp = require('../../node_modules/sharp');
const fs = require('fs'), path = require('path');
const S = 2048 / 1000, TEGEL = 360;
const UIT = process.argv[2] || '.';
const BOXEN = JSON.parse(fs.readFileSync(path.join(__dirname, 'boxen-borst.json'), 'utf8'));

(async () => {
  for (const [v, groepen] of Object.entries(BOXEN)) {
    const rijen = [];
    for (const [soort, boxen] of Object.entries(groepen)) {
      const tegels = [];
      for (const b of boxen) {
        const ex = { left: Math.round(b[0]*S), top: Math.round(b[1]*S), width: Math.round(b[2]*S), height: Math.round(b[3]*S) };
        tegels.push(await sharp(v + '.png').extract(ex).resize(TEGEL, TEGEL, { fit: 'contain', background: '#111' }).png().toBuffer());
      }
      rijen.push({ soort, tegels });
    }
    const kol = Math.max(...rijen.map(r => r.tegels.length));
    const comp = [];
    rijen.forEach((r, y) => r.tegels.forEach((t, x) => comp.push({ input: t, left: x*TEGEL, top: y*TEGEL })));
    await sharp({ create: { width: kol*TEGEL, height: rijen.length*TEGEL, channels: 3, background: '#111' } })
      .composite(comp).png().toFile(path.join(UIT, `borst-${v}.png`));
    console.log(v, rijen.map(r => `${r.soort}:${r.tegels.length}`).join(' '));
  }
})();
