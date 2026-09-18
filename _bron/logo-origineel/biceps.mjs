// Maakt de armen in het De Reus-logo krachtiger: grotere biceps, dikkere onderarmen en een dichte pols.
// Leest de originelen uit deze map en schrijft naar ../../img (of naar de map in argv[2]).
//   node biceps.mjs [uitmap] [omhoog] [opbollen] [dik]
import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
const HIER = path.dirname(fileURLToPath(import.meta.url));
const UIT = process.argv[2] || path.join(HIER, '..', '..', 'img');
const OMHOOG = +(process.argv[3] ?? 150);   // hoeveel de top van de biceps omhoog gaat (pad-eenheden)
const BOL = +(process.argv[4] ?? 0.22);     // extra opbollen rond het midden van de spier
const DIK = +(process.argv[5] ?? 90);      // hoeveel de buitenrand van de onderarm naar buiten gaat
const AS = 1206;                            // spiegelas tussen linker- en rechterarm
const C = { x: 520, y: 900, rx: 330, ry: 300 };   // linkerbiceps: midden en bereik van de vervorming

// Middellijn van de linkeronderarm (pols naar elleboog). De buitenrand schuift overal evenveel
// naar buiten, zodat de arm recht blijft; de binnenrand langs de biceps blijft liggen.
const A = { x: 475, y: 300 }, B = { x: 95, y: 1100 };
const ABx = B.x - A.x, ABy = B.y - A.y, AB = Math.hypot(ABx, ABy);
const N = { x: -ABy / AB, y: ABx / AB };    // normaal naar de buitenkant (linksboven)
const glad = (a, b, v) => { const t = Math.min(1, Math.max(0, (v - a) / (b - a))); return t * t * (3 - 2 * t); };
function dikker(x, y) {
  const t = ((x - A.x) * ABx + (y - A.y) * ABy) / (AB * AB);   // 0 = pols, 1 = elleboog
  const s = (ABx * (y - A.y) - ABy * (x - A.x)) / AB;          // positief = buitenkant
  const d = DIK * glad(0.1, 0.6, t) * (1 - glad(0.9, 1.14, t)) * glad(-30, 30, s);   // pols smal, onderarm breed
  return [x + N.x * d, y + N.y * d];
}

function vervorm(x, y) {
  const rechts = x > AS; if (rechts) x = 2 * AS - x;
  [x, y] = dikker(x, y);
  const u = (x - C.x) / C.rx, v = (y - C.y) / C.ry, q = u * u + v * v;
  if (q < 1) {
    const w = (1 - q) ** 2;
    const nx = x + (x - C.x) * BOL * w;
    const ny = y - OMHOOG * w + (y - C.y) * BOL * w * (y < C.y ? 1 : 0.3);
    x = nx; y = ny;
  }
  if (rechts) x = 2 * AS - x;
  return [x, y];
}

// Pols dicht: vult de witte inkeping onder de vuist en de spleet tussen duim en arm (linkerarm; rechts gespiegeld).
const POLS = [[380, 372], [430, 345], [500, 318], [575, 292], [640, 285], [668, 318], [640, 360], [590, 408], [530, 452], [480, 490], [448, 498], [410, 470], [385, 425]];
function polsPad(spiegel) {
  const pts = POLS.map(([x, y]) => vervorm(spiegel ? 2 * AS - x : x, y));
  // gesloten Catmull-Rom door de punten, als cubische bezier
  let d = `M ${pts[0][0].toFixed(1)} ${pts[0][1].toFixed(1)}`;
  for (let i = 0; i < pts.length; i++) {
    const p0 = pts[(i - 1 + pts.length) % pts.length], p1 = pts[i], p2 = pts[(i + 1) % pts.length], p3 = pts[(i + 2) % pts.length];
    const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
    const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
    d += ` C ${c1.map(v => v.toFixed(1)).join(' ')}, ${c2.map(v => v.toFixed(1)).join(' ')}, ${p2.map(v => v.toFixed(1)).join(' ')}`;
  }
  return d + ' Z';
}

for (const f of fs.readdirSync(HIER).filter(f => f.endsWith('.svg'))) {
  let s = fs.readFileSync(path.join(HIER, f), 'utf8');
  s = s.replace(/<path([^>]*)fill-rule="evenodd"([^>]*?) d="([^"]*)"([^>]*)>/, (m, voor, na, d, rest) => {
    let i = 0;
    const nums = d.match(/-?\d+(?:\.\d+)?/g).map(Number), uit = [];
    for (let k = 0; k < nums.length; k += 2) uit.push(vervorm(nums[k], nums[k + 1]));
    const nd = d.replace(/-?\d+(?:\.\d+)?/g, () => { const p = uit[i >> 1][i & 1]; i++; return +p.toFixed(2); });
    const kleur = (voor + na).match(/fill="[^"]+"/)[0], trans = (voor + na).match(/transform="[^"]+"/)[0];
    return `<path${voor}fill-rule="evenodd"${na} d="${nd}"${rest}><path ${kleur} ${trans} d="${polsPad(false)} ${polsPad(true)}"/>`;
  });
  // dikkere onderarmen steken verder uit: het logo zonder vlak iets breder maken
  s = s.replace('viewBox="316 195 296 291"', 'viewBox="302 195 324 291"');
  fs.writeFileSync(path.join(UIT, f), s); console.log('OK', f);
}
