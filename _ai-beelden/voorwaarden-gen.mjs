// Paginakop van /algemene-voorwaarden/: vijf kandidaten voor img/headers/voorwaarden.webp.
// Het huidige beeld is 560x315 en wordt tot 1440x810 opgerekt; daar viel het op in de beeldaudit.
// Dezelfde opzet als contact-gen.mjs: nano banana pro met het echte logo als bijlage, daarna sharp.
//
//   node voorwaarden-gen.mjs             genereren en klaarzetten als kandidaat-1..5.webp
//   node voorwaarden-gen.mjs 2 4         alleen die nummers opnieuw genereren
//   node voorwaarden-gen.mjs --klaar     alleen de ruwe bestanden omzetten naar 1920x1080 webp
//   node voorwaarden-gen.mjs --merk      het echte logo uit het merkboek in de kandidaten zetten
//   node voorwaarden-gen.mjs --prompts   de prompts naar prompts.md schrijven, zonder sleutel
//
// Sleutel uit GEMINI_API_KEY of ~/.gemini_api_key. Die staat nergens in de repo en wordt nooit geprint.
// Niets in img/ wordt aangeraakt: alles landt in website/review/voorwaarden-ronde-1/.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const HIER = path.dirname(fileURLToPath(import.meta.url));
const RONDE = path.join(HIER, '..', 'website', 'review', 'voorwaarden-ronde-1');
const RUW = path.join(RONDE, 'ruw');
fs.mkdirSync(RUW, { recursive: true });
const LOGO = path.join(HIER, 'refs', 'ref-logo.png');
const MODEL = 'gemini-3-pro-image-preview';
const URL = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`;

function sleutel() {
  const f = path.join(os.homedir(), '.gemini_api_key');
  return process.env.GEMINI_API_KEY || (fs.existsSync(f) ? fs.readFileSync(f, 'utf8').trim() : '');
}

// Het merk. Gelijk aan diensten-gen.mjs, ingekort tot wat op een kopbeeld te zien kan zijn.
const MERK = `
BRAND (Verhuisbedrijf De Reus, a moving company in The Hague, the Netherlands).
The attached image is the real De Reus logo: a yellow house (#FFCC33) held between two flexing royal-blue arms
(#1746A2), with "VERHUISBEDRIJF" small in blue and "DE REUS" large in yellow underneath. Reproduce it faithfully,
sharp and undistorted, wherever it appears. It is the ONLY text allowed anywhere in the picture.
Vehicles are white; clothing is a royal-blue (#1746A2) polo with the small house-with-arms symbol on the left chest;
moving boxes are brown kraft with the logo printed on the side and yellow tape.
`;

// De opdracht van de compositie. Dit beeld is een paginakop van 662 px hoog met witte tekst eroverheen:
// de kop staat gecentreerd op x 0,21 tot 0,79 en y 0,36 tot 0,59, met een donkere waas eromheen, en
// op 1920 px is alleen de middelste 61 procent van de hoogte te zien, op 390 px de middelste 42 procent
// van de breedte. Alles wat telt moet dus laag en dicht bij het midden staan (maten van dereus-b3).
const COMPOSITIE = `
COMPOSITION (critical: this is a wide website page header with a large white headline laid over it).
- 16:9 landscape, photojournalistic, one clear subject.
- The MAIN SUBJECT sits LOW and near the middle: its visual centre about 70% down from the top edge and
  between 38% and 62% across, just off dead centre. Nothing important in the outer 28% on the left or right,
  and nothing important in the top half.
- The TOP HALF of the frame stays visually QUIET and rather dark: plain wall, plain sky, shaded brickwork or
  softly out-of-focus interior. No detail, no faces, no second logo, no strong edges or bright spots there.
- Soft even light, moderate contrast, muted colours. Nothing bright white in the upper half.
- NO people beyond hands and forearms. No head, no face, no hair, no back of a head anywhere in the picture,
  not even blurred, not even far away and out of focus. Do not blur or pixelate a face to hide it: leave the
  head outside the frame altogether.
- NO readable text anywhere except the De Reus logo itself. Any other printing is too small, too soft or too
  far turned to read. No watermark, no border, no caption, no date stamp.
- The De Reus logo may only appear as part of the scene, printed on an object that is really in it. Never as a
  badge, stamp or watermark in a corner of the picture.
- Photorealistic editorial photography, full-frame camera, natural colours, realistic textures and small
  imperfections. NOT an illustration, NOT a 3D render, NOT HDR.
`;

// nummer, korte naam, scene, alt-tekst
const SCENES = [
  [1, 'getekende-offerte',
    `A signed De Reus moving quotation lying on a light oak desk, seen from a low three-quarter angle close to the
     desk surface. The top sheet carries the De Reus logo printed small at its top left corner, sharp and correct;
     the body text is far too small and too soft to read. A dark fountain pen rests across the signature line, and
     just behind the paper stand a pair of reading glasses and a plain white cup. Paper, pen and cup form one
     compact group low in the middle of the frame. Behind and above them the desk falls away into a deep,
     out-of-focus office shadow that fills the whole top half.`,
    'Een getekende offerte van De Reus met een vulpen op een bureau.'],
  [2, 'handdruk-voordeur',
    `A handshake on the doorstep of a brick town house in The Hague, photographed from the side. The frame is cut
     off at mid-chest height: only the two torsos from the chest down, the forearms and the clasped hands are in
     the picture. No head, no face, no shoulders above the chest, nothing to hide or blur. On the left the chest
     and arm of a De Reus mover in a royal-blue polo shirt, with the small yellow house-with-arms symbol on the
     left chest, sharp and correctly drawn; on the right the arm of a customer in a dark grey coat. The clasped
     hands sit low and just left of the middle of the frame. Behind them the dark green panelled front door and
     the brick wall rise into soft shade, out of focus and without any detail. Overcast Dutch daylight, wet
     pavement below.`,
    'Een verhuizer van De Reus geeft een klant een hand op de stoep voor een Haags huis.'],
  [3, 'dozen-in-de-gang',
    `A neat, chest-high stack of brown kraft De Reus moving boxes standing on the wooden floor of a bright but
     quiet Dutch hallway. The logo is printed on the side of the front box, straight on, sharp and correct; the
     boxes are closed with yellow tape and carry blank printed label strips with no readable words on them. The
     stack stands low and a little right of the middle of the frame; a folded blue moving blanket lies at its foot.
     Above the boxes the hallway wall is plain, empty and in soft shadow, with the light falling away towards the
     top of the frame.`,
    'Een stapel verhuisdozen van De Reus in de gang van een woning.'],
  [4, 'bus-in-zacht-licht',
    `Close view of the lower part of the side panel of a De Reus box truck, parked at the kerb of a quiet Dutch
     street at dusk. The camera is close to the panel and low, so the panel fills the whole frame and there is no
     sky, no street scene and no cab in the picture. The panel is in deep shade: cool grey-blue, not glaring white,
     and it grows darker towards the top of the frame until the upper third is almost black. The De Reus logo sits
     low and just right of the middle, sharp, straight on and correctly drawn, and takes up no more than a fifth
     of the frame width, with plenty of empty panel all around it. No phone number, no website, no other lettering.
     ABSOLUTELY NO PEOPLE, no boxes, no second logo, nothing else in the picture. Along the very bottom edge a
     narrow strip of wet brick street catches a little lamplight.`,
    'De zijkant van de verhuiswagen van De Reus met het logo in zacht avondlicht.'],
  [5, 'planner-aan-het-bureau',
    `A dark walnut desk seen from just above, lit by one warm lamp far out of frame. A closed royal-blue folder
     with the De Reus logo on its cover lies flat in the very MIDDLE of the frame, straight on, sharp and
     correctly drawn: this is the centre of the picture and everything else is arranged around it. To its left
     lies a plain ruled paper schedule, and two bare forearms and hands come in from the bottom LEFT corner, one
     resting on the schedule, the other holding a pencil. NOTHING else of the person: no head, no neck, no
     shoulder, no sleeve, no clothing of any kind, no badge. The schedule has faint handwriting far too loose to
     read and no printed heading, no title, no words at all. The whole top half of the frame is bare dark desk
     and a plain unlit wall, with nothing on it, fading into shadow at the top edge.`,
    'De handen van een planner van De Reus bij een verhuisplanning en een map met het logo.'],
];

async function maak([nr, naam, scene]) {
  const KEY = sleutel();
  if (!KEY) { console.error('Geen GEMINI_API_KEY (omgeving of ~/.gemini_api_key).'); process.exit(1); }
  const body = {
    contents: [{ role: 'user', parts: [
      { inline_data: { mime_type: 'image/png', data: fs.readFileSync(LOGO).toString('base64') } },
      { text: `${MERK}\n${COMPOSITIE}\nSCENE: ${scene.replace(/\s+/g, ' ').trim()}` },
    ] }],
    generationConfig: { responseModalities: ['IMAGE'], imageConfig: { aspectRatio: '16:9', imageSize: '2K' } },
  };
  for (let poging = 1; poging <= 3; poging++) {
    try {
      const r = await fetch(URL, { method: 'POST', headers: { 'Content-Type': 'application/json', 'x-goog-api-key': KEY }, body: JSON.stringify(body) });
      const j = await r.json();
      if (!r.ok) throw new Error(`${r.status} ${j.error?.message?.slice(0, 160)}`);
      const deel = j.candidates?.[0]?.content?.parts?.find(p => p.inlineData || p.inline_data);
      if (!deel) throw new Error('geen beeld in antwoord: ' + (j.candidates?.[0]?.finishReason || 'onbekend'));
      const d = deel.inlineData || deel.inline_data;
      const ext = (d.mimeType || d.mime_type || '').includes('png') ? 'png' : 'jpg';
      for (const e of ['png', 'jpg']) fs.rmSync(path.join(RUW, `kandidaat-${nr}.${e}`), { force: true });
      fs.writeFileSync(path.join(RUW, `kandidaat-${nr}.${ext}`), Buffer.from(d.data, 'base64'));
      console.log(`OK    kandidaat-${nr} (${naam})`);
      return;
    } catch (e) {
      console.log(`FOUT  kandidaat-${nr} (poging ${poging}): ${e.message}`);
      await new Promise(r => setTimeout(r, 4000 * poging));
    }
  }
}

// ruw/kandidaat-n.jpg -> 1920x1080. Eerst een platte png in ruw/, want daar zet --merk het echte
// logo in; daarna de webp die de kandidaat zelf is.
async function klaar(nr) {
  const bron = ['png', 'jpg', 'jpeg', 'webp'].map(e => path.join(RUW, `kandidaat-${nr}.${e}`)).find(fs.existsSync);
  if (!bron) { console.log(`--    kandidaat-${nr} (geen ruw bestand)`); return; }
  const plat = path.join(RUW, `kandidaat-${nr}-plat.png`);
  await sharp(bron).resize(1920, 1080, { fit: 'cover', position: 'centre' }).png().toFile(plat);
  const doel = path.join(RONDE, `kandidaat-${nr}.webp`);
  await sharp(plat).webp({ quality: 85 }).toFile(doel);
  const kb = Math.round(fs.statSync(doel).size / 1024);
  console.log(`KLAAR kandidaat-${nr}.webp  1920x1080  ${kb} KB`);
}

// ---------------------------------------------------------------------------
// Het echte merk erin (--merk)
// ---------------------------------------------------------------------------
// Het model verzint het logo elke keer opnieuw: de armen staan verkeerd om, het huis krijgt een raam,
// de woordmerkregels schuiven. Daarom wordt na het genereren het gevonden merk weggepoetst en het
// echte vector-logo uit brandbook/assets/logo/ erin gezet, in het vlak van het voorwerp zelf.
//
//   node voorwaarden-gen.mjs --merk        alle kandidaten
//   node voorwaarden-gen.mjs --merk 1 3    alleen die nummers
const MERKMAP = path.join(HIER, '..', 'brandbook', 'assets', 'logo');

// Per kandidaat: welk officieel bestand, waar het oude merk staat (zoekvlak, fracties), en de vier
// hoeken van het vlak waar het nieuwe merk in moet (px in 1920x1080, met de klok mee vanaf linksboven).
const MERKEN = {
  // 1: het papier ligt schuin, dus hier staan de vier hoeken met de hand; de rest is recht genoeg
  //    om het kader te volgen dat het oude merk achterliet.
  1: { svg: 'dereus-logo-horizontaal.svg', zoek: [0.16, 0.54, 0.33, 0.68], marge: 6,
       hoeken: [[345, 597], [676, 636], [669, 706], [338, 667]] },
  2: { svg: 'dereus-beeldmerk.svg', zoek: [0.26, 0.16, 0.35, 0.29], alleenGeel: true, marge: 6, schaal: 1.05 },
  3: { svg: 'dereus-logo.svg', zoek: [0.45, 0.53, 0.63, 0.81], wis: [903, 583, 1230, 908], marge: 0, schaal: 0.80, duw: [0, -12] },
  4: { svg: 'dereus-logo-horizontaal.svg', zoek: [0.44, 0.48, 0.94, 0.80], wis: [838, 500, 1812, 878], marge: 0, schaal: 0.92 },
  5: { svg: 'dereus-logo-negatief.svg', zoek: [0.39, 0.46, 0.62, 0.77], marge: 10, schaal: 0.96 },
};

function isMerkkleur(r, g, b, alleenGeel) {
  const geel = r > 140 && g > 100 && b < 140 && r - b > 60 && g - b > 40;
  if (alleenGeel) return geel;
  const blauw = b > 65 && b - r > 22 && b - g > 12 && r < 160;
  return geel || blauw;
}

// Het oude merk weghalen. Eerst zoeken waar het zit: alle merkkleur binnen het zoekvlak. Daarna niet
// alleen die pixels wissen maar het hele omhullende kader, want een masker op kleur laat de zachte
// randen van de letters staan en die schemeren door het nieuwe logo heen. De ondergronden zijn vlak
// (papier, karton, paneel, map), dus het kader dichtrekenen vanaf de rand geeft een schone vlakte.
function zoekMerk(data, W, H, ch, zoek, alleenGeel) {
  const [a, b, c, d] = zoek;
  const x0 = Math.round(a * W), y0 = Math.round(b * H), x1 = Math.round(c * W), y1 = Math.round(d * H);
  let minx = 1e9, miny = 1e9, maxx = -1, maxy = -1, tel = 0;
  for (let y = y0; y < y1; y++) for (let x = x0; x < x1; x++) {
    const i = (y * W + x) * ch;
    if (!isMerkkleur(data[i], data[i + 1], data[i + 2], alleenGeel)) continue;
    tel++;
    if (x < minx) minx = x; if (x > maxx) maxx = x;
    if (y < miny) miny = y; if (y > maxy) maxy = y;
  }
  if (maxx < 0) return null;
  return { x0: minx, y0: miny, x1: maxx, y1: maxy, tel };
}

function poetsWeg(data, W, H, ch, kader, marge) {
  const x0 = Math.max(1, kader.x0 - marge), y0 = Math.max(1, kader.y0 - marge);
  const x1 = Math.min(W - 2, kader.x1 + marge), y1 = Math.min(H - 2, kader.y1 + marge);
  // Eerst echt wegvegen, niet blurren: elke pixel in het kader wordt opnieuw gemaakt uit de vier
  // randpixels op zijn eigen rij en kolom. Op een vlakke ondergrond geeft dat precies het verloop
  // van het vlak terug. Daarna een paar rondes middelen om de naad weg te halen.
  const rand = Buffer.from(data);
  for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
    const wx = (x - x0) / Math.max(1, x1 - x0), wy = (y - y0) / Math.max(1, y1 - y0);
    for (let k = 0; k < 3; k++) {
      const L = rand[(y * W + x0 - 1) * ch + k], R = rand[(y * W + x1 + 1) * ch + k];
      const T = rand[((y0 - 1) * W + x) * ch + k], B = rand[((y1 + 1) * W + x) * ch + k];
      data[(y * W + x) * ch + k] = Math.round((L * (1 - wx) + R * wx + T * (1 - wy) + B * wy) / 2);
    }
  }
  for (let ronde = 0; ronde < 12; ronde++) {
    const kopie = Buffer.from(data);
    for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) for (let k = 0; k < 3; k++) {
      const i = (y * W + x) * ch + k;
      data[i] = Math.round((kopie[i - ch] + kopie[i + ch] + kopie[i - W * ch] + kopie[i + W * ch]) / 4);
    }
  }
  // De rand veren, anders tekent het gepoetste vlak zich als een rechthoek af op een ondergrond die
  // toch nooit helemaal egaal is. Binnen de veerband telt het origineel weer mee.
  const veer = 14;
  for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
    const d = Math.min(x - x0, x1 - x, y - y0, y1 - y);
    if (d >= veer) continue;
    const m = d / veer;
    for (let k = 0; k < 3; k++) {
      const i = (y * W + x) * ch + k;
      data[i] = Math.round(rand[i] * (1 - m) + data[i] * m);
    }
  }
  return { x0, y0, x1, y1, px: (x1 - x0) * (y1 - y0) };
}

// Het nieuwe merk in het vlak van het voorwerp leggen: een homografie van de rechthoek van het
// logobestand naar de vier opgegeven hoeken, met bilineaire bemonstering. Daarmee volgt het logo het
// perspectief van het papier, de doos, het paneel of de map, in plaats van er plat op te plakken.
function homografie(bron, doel) {
  // los A * h = b op voor de acht onbekenden van de 3x3 matrix (h9 = 1)
  const A = [], b = [];
  for (let i = 0; i < 4; i++) {
    const [x, y] = bron[i], [u, v] = doel[i];
    A.push([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.push(u);
    A.push([0, 0, 0, x, y, 1, -v * x, -v * y]); b.push(v);
  }
  for (let k = 0; k < 8; k++) {                       // Gauss met partiële pivotering
    let p = k;
    for (let r = k + 1; r < 8; r++) if (Math.abs(A[r][k]) > Math.abs(A[p][k])) p = r;
    [A[k], A[p]] = [A[p], A[k]]; [b[k], b[p]] = [b[p], b[k]];
    for (let r = 0; r < 8; r++) {
      if (r === k || !A[r][k]) continue;
      const f = A[r][k] / A[k][k];
      for (let c = k; c < 8; c++) A[r][c] -= f * A[k][c];
      b[r] -= f * b[k];
    }
  }
  const h = b.map((v, i) => v / A[i][i]);
  return [[h[0], h[1], h[2]], [h[3], h[4], h[5]], [h[6], h[7], 1]];
}

function keerOm(m) {
  const [[a, b, c], [d, e, f], [g, h, i]] = m;
  const det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g);
  return [[(e * i - f * h) / det, (c * h - b * i) / det, (b * f - c * e) / det],
          [(f * g - d * i) / det, (a * i - c * g) / det, (c * d - a * f) / det],
          [(d * h - e * g) / det, (b * g - a * h) / det, (a * e - b * d) / det]];
}

async function merk(nr) {
  const cfg = MERKEN[nr];
  const bron = path.join(RUW, `kandidaat-${nr}-plat.png`);
  if (!fs.existsSync(bron)) { console.log(`--    kandidaat-${nr} (geen platte versie, draai eerst --klaar)`); return; }
  const { data, info } = await sharp(bron).removeAlpha().raw().toBuffer({ resolveWithObject: true });
  const W = info.width, H = info.height, ch = info.channels;
  const kader = zoekMerk(data, W, H, ch, cfg.zoek, cfg.alleenGeel);
  if (!kader) { console.log(`--    kandidaat-${nr}: geen merkkleur gevonden in het zoekvlak`); return; }
  if (cfg.wis) { kader.x0 = cfg.wis[0]; kader.y0 = cfg.wis[1]; kader.x1 = cfg.wis[2]; kader.y1 = cfg.wis[3]; }
  const weg = poetsWeg(data, W, H, ch, kader, cfg.marge ?? 8);

  // Waar komt het nieuwe logo? Bij een recht voorwerp precies in het gepoetste kader, op de
  // verhouding van het echte bestand. Staat het vlak schuin (het papier), dan geeft cfg.hoeken het aan.
  const meta = await sharp(path.join(MERKMAP, cfg.svg)).metadata();
  const verh = meta.width / meta.height;
  let hoeken = cfg.hoeken;
  if (!hoeken) {
    const kb = weg.x1 - weg.x0, kh = weg.y1 - weg.y0;
    const bb = Math.min(kb, kh * verh) * (cfg.schaal ?? 1), bh = bb / verh;
    const mx = (weg.x0 + weg.x1) / 2 + (cfg.duw?.[0] ?? 0), my = (weg.y0 + weg.y1) / 2 + (cfg.duw?.[1] ?? 0);
    hoeken = [[mx - bb / 2, my - bh / 2], [mx + bb / 2, my - bh / 2], [mx + bb / 2, my + bh / 2], [mx - bb / 2, my + bh / 2]];
  }
  const breed = Math.round(Math.max(Math.hypot(hoeken[1][0] - hoeken[0][0], hoeken[1][1] - hoeken[0][1]),
                                    Math.hypot(hoeken[2][0] - hoeken[3][0], hoeken[2][1] - hoeken[3][1])));
  const plaat = await sharp(path.join(MERKMAP, cfg.svg), { density: 600 })
    .resize({ width: breed * 2 }).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  const L = plaat.data, LW = plaat.info.width, LH = plaat.info.height;

  // hoe donker is de ondergrond hier? Het logo krijgt dezelfde belichting, anders plakt het erop.
  const xs = hoeken.map(p => p[0]), ys = hoeken.map(p => p[1]);
  const sy0 = Math.round(Math.min(...ys)), sy1 = Math.round(Math.max(...ys));
  const sx0 = Math.round(Math.min(...xs)), sx1 = Math.round(Math.max(...xs));
  const toppen = [];
  for (let y = sy0; y < sy1; y += 3) for (let x = sx0; x < sx1; x += 3) {
    const i = (y * W + x) * ch;
    toppen.push(Math.max(data[i], data[i + 1], data[i + 2]));
  }
  toppen.sort((a, b) => a - b);
  const top = toppen[Math.floor(toppen.length * 0.9)] || 235;
  const licht = cfg.licht ?? Math.min(1, Math.max(0.35, top / 245));

  const inv = keerOm(homografie([[0, 0], [LW, 0], [LW, LH], [0, LH]], hoeken));
  const x0 = Math.max(0, Math.floor(Math.min(...xs)) - 2), x1 = Math.min(W, Math.ceil(Math.max(...xs)) + 2);
  const y0 = Math.max(0, Math.floor(Math.min(...ys)) - 2), y1 = Math.min(H, Math.ceil(Math.max(...ys)) + 2);
  for (let y = y0; y < y1; y++) for (let x = x0; x < x1; x++) {
    const w = inv[2][0] * (x + .5) + inv[2][1] * (y + .5) + inv[2][2];
    const sx = (inv[0][0] * (x + .5) + inv[0][1] * (y + .5) + inv[0][2]) / w;
    const sy = (inv[1][0] * (x + .5) + inv[1][1] * (y + .5) + inv[1][2]) / w;
    if (sx < 0 || sy < 0 || sx >= LW - 1 || sy >= LH - 1) continue;
    const fx = Math.floor(sx), fy = Math.floor(sy), dx = sx - fx, dy = sy - fy;
    const hoek = [[fy, fx], [fy, fx + 1], [fy + 1, fx], [fy + 1, fx + 1]].map(([r, c]) => (r * LW + c) * 4);
    const gew = [(1 - dx) * (1 - dy), dx * (1 - dy), (1 - dx) * dy, dx * dy];
    let a = 0; const kl = [0, 0, 0];
    for (let k = 0; k < 4; k++) { a += L[hoek[k] + 3] * gew[k]; for (let c = 0; c < 3; c++) kl[c] += L[hoek[k] + c] * gew[k]; }
    a /= 255;
    if (a < 0.004) continue;
    const i = (y * W + x) * ch;
    for (let c = 0; c < 3; c++) data[i + c] = Math.round(data[i + c] * (1 - a) + Math.min(255, kl[c] * licht) * a);
  }
  const doel = path.join(RONDE, `kandidaat-${nr}.webp`);
  await sharp(data, { raw: info }).webp({ quality: 85 }).toFile(doel);
  console.log(`MERK  kandidaat-${nr}: kader ${kader.x0},${kader.y0}-${kader.x1},${kader.y1} (${kader.tel} px merkkleur), ` +
    `${weg.px} px gepoetst, ${cfg.svg} erin op licht ${licht.toFixed(2)}, ` +
    `${Math.round(fs.statSync(doel).size / 1024)} KB`);
}

const args = process.argv.slice(2);
const nummers = args.filter(a => /^\d+$/.test(a)).map(Number);
const lijst = nummers.length ? SCENES.filter(s => nummers.includes(s[0])) : SCENES;

if (args.includes('--prompts')) {
  const tekst = `# Prompts, kopbeeld algemene voorwaarden (ronde 1)\n\n` +
    `Model: ${MODEL} (nano banana pro), beeldverhouding 16:9, formaat 2K, met het echte logo\n` +
    `(brandbook/assets/logo via _ai-beelden/refs/ref-logo.png) als bijlage bij elke prompt.\n` +
    `Script: _ai-beelden/voorwaarden-gen.mjs\n\n## Merkregels (bij elke kandidaat)\n\n\`\`\`\n${MERK.trim()}\n\`\`\`\n` +
    `\n## Compositie (bij elke kandidaat)\n\n\`\`\`\n${COMPOSITIE.trim()}\n\`\`\`\n\n` +
    lijst.map(([nr, naam, scene, alt]) =>
      `## Kandidaat ${nr}: ${naam}\n\n\`\`\`\nSCENE: ${scene.replace(/\s+/g, ' ').trim()}\n\`\`\`\n\nAlt-tekst: ${alt}\n`).join('\n');
  fs.writeFileSync(path.join(RONDE, 'prompts.md'), tekst);
  console.log('prompts.md geschreven');
} else if (args.includes('--merk')) {
  for (const [nr] of lijst) await merk(nr);
} else {
  if (!args.includes('--klaar')) for (const s of lijst) await maak(s);
  for (const [nr] of lijst) await klaar(nr);
}
