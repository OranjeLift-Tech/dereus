// "Twee verhuizers samen": vijf kandidaatbeelden voor De Reus, met echte referentiegezichten.
// Zelfde patroon als stap-1-gen.mjs: nano banana pro (gemini-3-pro-image-preview), 3:2, 2K.
// Twee referentiegezichten per kandidaat als extra inline_data delen (A = eerste, B = tweede).
// Geen logo-referentie en geen logo in het prompt: het model tekent het merk altijd verkeerd.
//
//   node twee-verhuizers-gen.mjs             genereren (5 kandidaten) + webp + prompts.md
//   node twee-verhuizers-gen.mjs 2 4         alleen kandidaat 2 en 4 opnieuw
//   node twee-verhuizers-gen.mjs webp        alleen de webps maken uit ruw/
//   node twee-verhuizers-gen.mjs prompts     alleen prompts.md schrijven
//   node twee-verhuizers-gen.mjs crop 3 gezicht-a 0.12 0.18 0.14 0.20
//                                            uitsnede (fracties x y b h van het ruwe beeld) op 3x
// Key uit GEMINI_API_KEY of ~/.gemini_api_key (nooit in de repo, nooit printen).
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const HIER = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HIER, '..');
const UIT = path.join(ROOT, 'website', 'review', 'twee-verhuizers-20260922');
const RUW = path.join(UIT, 'ruw');
const CROPS = path.join(UIT, 'crops');
for (const d of [UIT, RUW, CROPS]) fs.mkdirSync(d, { recursive: true });

const GEZICHTEN = path.join(os.homedir(), '.claude', 'skills', 'foto-verbeteren', 'assets', 'gezichten');
const MODEL = 'gemini-3-pro-image-preview';
const URL = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`;
const BREED = 1400, HOOG = 933;   // maat van de webp voor de gebruiker

const MERK = `BRAND RULES (Verhuisbedrijf De Reus, a moving company in The Hague, the Netherlands):
- CLOTHING: the movers wear a royal-blue (#1746A2) polo shirt, navy work trousers and black safety shoes.
  Neat, clean, well-fitting. On the chest only a small yellow house symbol, smaller than 3 cm: symbol only,
  NO text, NO name line underneath it, NO wordmark, no brand name anywhere on the clothing.
- BOXES: plain brown kraft cardboard moving boxes, completely blank, no printing of any kind.
- VAN OR TRUCK: only far away and out of focus, or outside the frame. Never a readable side panel.
- PEOPLE: an honest, diverse mix of Dutch people, different ages and builds. Natural, friendly, confident,
  not posed stock smiles. Real working men with wear and tear, not models.
- SETTING: recognisably The Hague / the Netherlands: brick row houses, white window frames, bicycles, trees,
  brick streets. Realistic Dutch weather: bright, soft daylight, light clouds; not overly sunny.
- STYLE: photorealistic editorial photography, full-frame camera, natural colours, shallow depth of field
  where it fits. NOT illustration, NOT 3D render, NOT HDR, no text overlays.
- natural skin texture, visible pores, uneven skin tone, no retouching.
- hands with five fingers, grip consistent with the object's weight.
- No text, no letters, no numbers, no signage, no watermark anywhere in the image.`;

// Ronde 2, voor kandidaat 3 en 5 na de controle op ronde 1. Drie fouten stuurden deze regels:
// zes vingers aan een hand en een losse vingertop die bij geen hand hoorde (kandidaat 3), een
// bedrukking op een doos die leeg hoorde te zijn (kandidaat 3), en een vervormd borstteken met
// een onleesbaar regeltje eronder (kandidaat 3 en 5).
const MERK2 = `${MERK}
- THE CHEST SYMBOL is a SIMPLE FLAT YELLOW HOUSE: a square body with a triangular roof, nothing else.
  No arrow shapes, no figures, no cape, no ribbon, no line of text or scribble underneath or beside it.
  If in doubt, make the symbol smaller and simpler, or leave the chest completely plain.
- HANDS: each hand has exactly four fingers and one thumb. Do not add extra fingers. Every visible
  fingertip must belong to a hand that is itself visible in the frame.
- ABSOLUTELY NO NUMBERS OR SIGNS: no house numbers on walls, doors or door frames; no number plates
  on any vehicle (leave the plate surface completely blank, or keep it out of the frame); no street
  name signs, no doorbell labels, no shop signs, no printing and no handwriting on boxes or tape.`;

// Ronde 3, alleen kandidaat 3. In ronde 2 zette het model onder allebei de huisjes alsnog een
// onleesbare naamregel, precies de fout die de controle afwijst. Vragen om een klein huisje zonder
// tekst helpt niet; de borst helemaal leeg vragen wel. Het echte beeldmerk gaat er naderhand met
// sharp op, zoals bij team-de-reus en woningontruiming.
const MERK3 = `${MERK2}
- OVERRIDE ON THE CHEST: the polo shirt is COMPLETELY PLAIN royal blue. No symbol, no house, no logo,
  no emblem, no embroidery, no print, no badge, no lettering on the chest, the sleeves or the back.
  Plain blue fabric only. This overrides every earlier instruction about a chest symbol.`;

const PERSONEN = `Person A: use the FIRST attached reference photo for face identity, age, skin and expression only;
ignore its clothing, helmet and background. Person B: use the SECOND attached reference photo the same way.
The two men/people must look clearly like different individuals.`;

export const KANDIDATEN = [
  {
    nr: 1, ronde: 1, naam: 'Bank de stoep af',
    refs: ['mannen/man-18.png', 'mannen/man-01.png'],
    scene: `Two movers carry a sofa wrapped in blue moving blankets down the front steps of a brick townhouse in
The Hague. Mover A walks backwards in front, at the bottom of the steps, taking the weight low; mover B is at the
top of the steps, holding the other end higher. Medium long shot, eye level, the whole staircase and both men in
frame. Both faces clearly visible and in focus. Soft Dutch daylight.`,
  },
  {
    nr: 2, ronde: 1, naam: 'Samen bij de achterdeuren',
    refs: ['mannen/man-02.png', 'mannen/man-09.png'],
    scene: `Two movers stand relaxed side by side in front of the open rear doors of their van in a street in
The Hague. Mover A holds a plain brown box under one arm; mover B stands with his hands loosely at his sides.
Both look straight into the camera, calm and friendly. Medium long shot, eye level. The van is plain white and
completely unmarked, its open doors and panels clearly out of focus behind them, so no side panel, no lettering
and no logo is legible anywhere. Soft Dutch daylight.`,
  },
  {
    nr: 3, ronde: 3, naam: 'Kast inpakken met deken en tape',
    refs: ['mannen/man-16.png', 'mannen/man-05.png'],
    scene: `Two movers work together in an empty living room with a wooden floor and a tall window. Mover A holds
a wooden cabinet upright with both hands; mover B wraps a thick blue moving blanket around it and presses a strip
of tape onto it. The picture is about the cooperation between them: the hands of both men are prominent, large in
the frame and sharp. 50 mm lens, eye level, soft daylight from the window.
FRAMING: step back far enough that BOTH heads are completely inside the frame, whole and uncropped,
with clear empty space above both heads. Nothing is cut off at the top edge. Both faces are fully
visible, including forehead and eyes.`,
  },
  {
    nr: 4, ronde: 1, naam: 'Doos doorgeven aan de laadklep',
    refs: ['mannen/man-20.png', 'vrouwen/vrouw-02.png'],
    scene: `Two movers at the tail lift of their van in a street in The Hague. Mover A, standing on the street,
hands a plain brown moving box to mover B, who stands on the raised tail lift and reaches down for it. A real
moment of movement: the box is between them, both grips visible. Side view, eye level, both faces clearly visible.
The van itself is plain white and unmarked and falls away out of focus, so no side panel, no lettering and no logo
is legible anywhere. Soft Dutch daylight.`,
  },
  {
    nr: 5, ronde: 2, naam: 'Zware kist door het trappenhuis',
    refs: ['mannen/man-06.png', 'mannen/man-04.png'],
    scene: `Two movers carry a heavy wooden crate together up a narrow Dutch stairwell with a wooden handrail and
white plastered walls. Mover A is below the crate, taking the weight with both arms; mover B is above it, guiding
it around the turn of the stairs. Both are concentrating, slightly strained, not smiling. Tight framing, the walls
close on both sides, natural light falling from a window above. Both faces visible in the light from above.`,
  },
];

const STIJL = `Photorealistic editorial photograph, aspect ratio 3:2, full-frame camera, natural colours,
realistic depth of field. An original scene with original people, not a real recognisable individual.`;

export function promptVan(k) {
  return `${k.ronde === 3 ? MERK3 : k.ronde === 2 ? MERK2 : MERK}\n\n${PERSONEN}\n\nSCENE: ${k.scene.trim()}\n\n${STIJL}`;
}

function sleutel() {
  const f = path.join(os.homedir(), '.gemini_api_key');
  return process.env.GEMINI_API_KEY || (fs.existsSync(f) ? fs.readFileSync(f, 'utf8').trim() : '');
}

// De uitsneden zijn klein (65 tot 430 px). Op wit en naar 512 op de langste zijde,
// zodat het model het gezicht scherp genoeg ziet. Verder niets aan veranderd.
async function gezichtRef(rel) {
  const bron = path.join(GEZICHTEN, rel);
  const m = await sharp(bron).metadata();
  const schaal = 512 / Math.max(m.width, m.height);
  return (await sharp(bron).flatten({ background: '#ffffff' })
    .resize({ width: Math.round(m.width * schaal), height: Math.round(m.height * schaal), kernel: 'lanczos3' })
    .png().toBuffer()).toString('base64');
}

async function maak(k) {
  const KEY = sleutel();
  if (!KEY) { console.error('Geen GEMINI_API_KEY (omgeving of ~/.gemini_api_key).'); process.exit(1); }
  const [a, b] = await Promise.all(k.refs.map(gezichtRef));
  const body = {
    contents: [{ role: 'user', parts: [
      { inline_data: { mime_type: 'image/png', data: a } },   // persoon A
      { inline_data: { mime_type: 'image/png', data: b } },   // persoon B
      { text: promptVan(k) },
    ] }],
    generationConfig: { responseModalities: ['IMAGE'], imageConfig: { aspectRatio: '3:2', imageSize: '2K' } },
  };
  for (let poging = 1; poging <= 3; poging++) {
    try {
      const r = await fetch(URL, { method: 'POST', headers: { 'Content-Type': 'application/json', 'x-goog-api-key': KEY }, body: JSON.stringify(body) });
      const j = await r.json();
      if (!r.ok) throw new Error(`${r.status} ${j.error?.message?.slice(0, 160)}`);
      const d = j.candidates?.[0]?.content?.parts?.find(p => p.inlineData || p.inline_data);
      if (!d) throw new Error('geen beeld: ' + (j.candidates?.[0]?.finishReason || 'onbekend'));
      const bestand = path.join(RUW, `kandidaat-${k.nr}.png`);
      fs.writeFileSync(bestand, Buffer.from((d.inlineData || d.inline_data).data, 'base64'));
      const m = await sharp(bestand).metadata();
      console.log(`OK   kandidaat-${k.nr} ${m.width}x${m.height}`);
      return true;
    } catch (e) {
      console.log(`FOUT kandidaat-${k.nr} (poging ${poging}): ${e.message}`);
      await new Promise(r => setTimeout(r, 4000 * poging));
    }
  }
  return false;
}

async function webp(nr) {
  const bron = path.join(RUW, `kandidaat-${nr}.png`);
  if (!fs.existsSync(bron)) { console.log(`--   kandidaat-${nr}: geen bron`); return; }
  await sharp(bron).resize(BREED, HOOG, { fit: 'cover', position: 'centre' }).webp({ quality: 90 })
    .toFile(path.join(UIT, `kandidaat-${nr}.webp`));
  console.log(`WEBP kandidaat-${nr} ${BREED}x${HOOG}`);
}

// Uitsnede op 3x: fracties van het ruwe beeld, uitgeschreven op drie keer de maat
// die het gebied in de geleverde webp (1400 breed) heeft.
async function crop(nr, naam, fx, fy, fb, fh, maal = 3) {
  const bron = path.join(RUW, `kandidaat-${nr}.png`);
  const m = await sharp(bron).metadata();
  const left = Math.max(0, Math.round(fx * m.width)), top = Math.max(0, Math.round(fy * m.height));
  const width = Math.min(m.width - left, Math.round(fb * m.width)), height = Math.min(m.height - top, Math.round(fh * m.height));
  const doel = Math.round(fb * BREED * maal);
  const uit = path.join(CROPS, `kandidaat-${nr}-${naam}.png`);
  await sharp(bron).extract({ left, top, width, height })
    .resize({ width: doel, kernel: 'lanczos3' }).png().toFile(uit);
  console.log(`CROP ${path.basename(uit)} uit ${width}x${height} naar ${doel} breed`);
}

export function prompts() {
  const kop = `# Prompts "twee verhuizers samen", 22-09-2026\n\n` +
    `Model: ${MODEL} (nano banana pro), beeldverhouding 3:2, imageSize 2K. Per kandidaat gaan twee\n` +
    `referentiegezichten mee als inline_data delen: het eerste deel is persoon A, het tweede persoon B.\n` +
    `De gezichten komen uit \`~/.claude/skills/foto-verbeteren/assets/gezichten/\`, op wit gezet en naar\n` +
    `512 px op de langste zijde geschaald, verder onbewerkt. Geen logo-referentie en geen logo in het prompt.\n` +
    `Daarna met sharp naar ${BREED}x${HOOG} (cover, midden), webp kwaliteit 90.\n\n` +
    `## Vaste merkregels\n\n\`\`\`\n${MERK}\n\`\`\`\n\n## Vaste personenregel\n\n\`\`\`\n${PERSONEN}\n\`\`\`\n\n` +
    `## Vaste stijlregel\n\n\`\`\`\n${STIJL}\n\`\`\`\n\n`;
  const blokken = KANDIDATEN.map(k =>
    `## Kandidaat ${k.nr}: ${k.naam}\n\nPersoon A: \`${k.refs[0]}\`  |  Persoon B: \`${k.refs[1]}\`\n\n` +
    `Volledig prompt:\n\n\`\`\`\n${promptVan(k)}\n\`\`\`\n`).join('\n');
  fs.writeFileSync(path.join(UIT, 'prompts.md'), kop + blokken, 'utf8');
  console.log('prompts.md geschreven');
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  if (args[0] === 'prompts') {
    prompts();
  } else if (args[0] === 'crop') {
    await crop(Number(args[1]), args[2], ...args.slice(3, 8).map(Number));
  } else if (args[0] === 'webp') {
    for (const k of KANDIDATEN) await webp(k.nr);
  } else {
    const welke = args.length ? KANDIDATEN.filter(k => args.includes(String(k.nr))) : KANDIDATEN;
    await Promise.all(welke.map(maak));
    for (const k of welke) await webp(k.nr);
    prompts();
    console.log('Klaar:', UIT);
  }
}
