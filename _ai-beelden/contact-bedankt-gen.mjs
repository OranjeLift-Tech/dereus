// Kop van /contact/bedankt/: vijf kandidaten met een verhuizer van De Reus, ter vervanging van
// img/headers/contact-bedankt.webp (560x315 stockfoto van een onbekende man, wordt tot 1440x810
// opgeblazen, afgekeurd in de audit).
//   node contact-bedankt-gen.mjs           genereren + afwerken
//   node contact-bedankt-gen.mjs af        alleen opnieuw afwerken uit de ruwe png's
//   node contact-bedankt-gen.mjs 2 4       alleen die nummers opnieuw genereren
// Key uit GEMINI_API_KEY of ~/.gemini_api_key (nooit in de repo, nooit in de uitvoer).
//
// Maatvoering, gemeten op de echte pagina (kop 662 px hoog, object-fit cover, 50% 50%):
//   1920: alleen de middelste 61,3 % van de hoogte staat in beeld  -> y 0,194 tot 0,807
//   1440: de middelste 81,7 % van de hoogte                        -> y 0,092 tot 0,908
//    390: alleen de middelste 41,9 % van de breedte                -> x 0,290 tot 0,710
// Het koptekstvak staat op 1440 op x 0,21 tot 0,79 en y 0,33 tot 0,61, op 390 op y 0,24 tot 0,63,
// met een donkere radiale waas eromheen en een verloop over de bovenste 56 en de onderste 48 procent.
// Daarom staat de verhuizer in de onderste derde, naast het midden: hoofd en borst op y 0,63 tot 0,80
// en x 0,30 tot 0,70. Een gecentreerde figuur op volle hoogte wordt door de tekstwaas opgeslokt.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const HIER = path.dirname(fileURLToPath(import.meta.url));
const RUW = path.join(HIER, 'foto', 'contact-bedankt');
const UIT = path.resolve(HIER, '..', 'website', 'review', 'contact-bedankt-ronde-1');
fs.mkdirSync(RUW, { recursive: true });
fs.mkdirSync(UIT, { recursive: true });

const MODEL = 'gemini-3-pro-image-preview';
const URL = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`;

// Wat alle vijf de prompts delen: het merk, het kader en wat er niet in mag.
const KADER = `
The attached image is the real logo of Verhuisbedrijf De Reus, a moving company in The Hague: a yellow house
(#FFCC33) standing between two flexing royal-blue arms (#1746A2), with the company name set below it.

Use case: photorealistic-natural. Asset type: wide website page-header background photograph for that company.
Generate a photorealistic landscape photograph in a 4:3 frame, shot on a 35 mm lens, natural daylight, real skin
and fabric texture, shallow but believable depth of field. Not an illustration, not a 3D render.

COMPOSITION. This is the single most important instruction and it overrides the usual way of framing a person.
The website keeps only the TOP THREE QUARTERS of this 4:3 photograph, lays a dark royal-blue gradient over it
and prints a large white heading across the upper middle of what is left. So the useful part of the picture is
the upper area, and the person has to sit at the middle of the height, not above it.

Measuring downwards from the top edge of the 4:3 frame:
- The whole upper half, everything above 50 percent, holds NO person at all. It is open sky, a plain wall, a
  plain vehicle panel or softly defocused street: quiet, low in detail, no faces, no props, no hard edges. Give
  that empty area real space, it is half the picture.
- The top of the mover's head sits at about 50 percent of the height, just under that empty area. His shoulders
  and chest follow right below it, and his legs run down towards the bottom edge.
- This is a wide establishing shot taken from far back, not a portrait. The mover is a small figure standing in
  the lower half of a large open frame, no taller than half the picture height.
- Measuring across from the left edge, he stands between 30 and 70 percent of the width, clearly to one side of
  the exact centre. Nothing important lies outside that band: the sides are cropped away on a phone, and the
  photograph must still read when only the middle 42 percent of its width is shown.
DO NOT make a portrait. DO NOT fill the frame with the person. DO NOT place his head in the upper half. Pull the
camera back far enough that he takes up no more than the lower half of the height.

THE MOVER: a Dutch professional mover in a royal-blue (#1746A2) pique polo shirt. On the left chest of the polo,
and nowhere else on the clothing, sits the small embroidered De Reus mark from the attached logo: the yellow
house between two blue arms. Copy that mark exactly as attached, same shape, same two colours, no other emblem,
no invented crest, no lettering on the shirt. Work trousers in dark grey or navy, plain.

FORBIDDEN: any readable text, letters, numbers, slogans, phone numbers, web addresses, watermarks or signage
anywhere in the frame apart from that one embroidered mark. No bystanders, no passers-by, no onlookers, no
children, no pets: the only people in frame are De Reus movers. No identifiable real person, no celebrity
likeness, no real brand other than the attached mark, no real company vehicle livery from another firm. No
graphic overlay, no border, no vignette drawn into the photograph itself. Anatomically correct hands with five
fingers. Do NOT draw any grid, guide lines, rulers, percentages, numbers, labels or annotations onto the
photograph: the framing notes above describe where to point the camera, they are not to be rendered.
Every person in the frame must be whole and correctly formed, with head, torso, arms and legs all present and
attached. No headless figure, no stray pair of legs, no half body appearing behind or beside the vehicle, no
extra person other than the movers described in the scene.
`;

const SCENES = [
  {
    nr: 1,
    naam: 'Busdeuren sluiten',
    scene: `SCENE: the end of a job. A mover stands at the open back of a plain unmarked white box van parked at
the kerb of a quiet Dutch residential street, swinging the rear door closed with one hand, looking back over his
shoulder towards the camera with a calm satisfied half-smile. He is small and low in the frame, his head at half the frame height,
offset to the LEFT of centre at about 36 percent of the frame width; the van fills the right-hand side and its plain white
flank gives a quiet empty surface across the upper right. Above him: soft overcast Dutch sky and the blurred
roofline of brick terraced houses, no detail. Late afternoon light, long soft shadows, work done.`,
  },
  {
    nr: 2,
    naam: 'Doos op de stoep',
    scene: `SCENE: a mover on the front step of a Dutch terraced house, holding one closed brown cardboard moving
box against his hip with both hands, half turned towards the camera with a friendly relaxed expression, as if he
has just said goodbye. He is small and low in the frame, his head at half the frame
height, offset to the RIGHT of centre at about 63 percent of the frame width. Behind and above him a plain brick front wall and an open dark green door, both softly out of
focus and free of any house number, nameplate, letterbox lettering or sticker. The upper half of the frame is
quiet brickwork and sky. Soft diffuse morning light.`,
  },
  {
    nr: 3,
    naam: 'Aan de telefoon bij de wagen',
    scene: `SCENE: a mover standing beside a plain unmarked white moving truck, holding a phone to his ear with
one hand and listening, nodding, with a warm attentive expression, the other hand resting on the truck. This is
the moment a message has been answered. He is small and low in the frame, his head at half the frame height,
offset to the LEFT of centre at about 38 percent of the frame width. The plain white side of the truck runs across the right of the frame and up
into the quiet upper half, giving a large calm empty surface. Above: bright overcast sky, no detail. Soft even
daylight.`,
  },
  {
    nr: 4,
    naam: 'Met zijn tweeen door de straat',
    scene: `SCENE: two De Reus movers, both in the same royal-blue polo with the same embroidered mark, carrying
one wrapped piece of furniture in a grey moving blanket between them along a narrow street of Dutch canal-side
terraced houses. They walk towards the camera, easy and unhurried, the front one glancing up with a small friendly
smile. Both are small and low in the frame, their heads at half the frame height, the pair held
between 32 and 68 percent of the frame width so that neither is lost when the sides are cropped. Above them the street recedes into soft defocus: brick facades,
a few bare trees, flat grey sky filling the quiet upper half. Cool soft daylight, wet cobbles.`,
  },
  {
    nr: 5,
    naam: 'Groet vanuit de cabine',
    scene: `SCENE: a mover in the driver's seat of a plain unmarked white moving truck, arm resting on the open
window frame, raising his hand in a short friendly wave towards the camera, calm and unhurried, about to drive off.
The truck is seen from far back and sits low in the frame: the open cab window with his head and shoulders is
just under half the frame height, offset to the RIGHT of centre at about 64 percent of the frame width, under a
wide empty sky that fills the whole upper half. The plain white cab door and flank fill the lower left; the quiet
upper half is the blank white upper cab panel and pale sky, with no mirror, lamp, aerial or badge breaking it.
Warm low afternoon light on his face.`,
  },
];

function sleutel() {
  const f = path.join(os.homedir(), '.gemini_api_key');
  return process.env.GEMINI_API_KEY || (fs.existsSync(f) ? fs.readFileSync(f, 'utf8').trim() : '');
}

function prompt(s) {
  return `${KADER}\n${s.scene}\n`;
}

async function maak(s) {
  const KEY = sleutel();
  if (!KEY) { console.error('Geen GEMINI_API_KEY (omgeving of ~/.gemini_api_key).'); process.exit(1); }
  const body = {
    contents: [{ role: 'user', parts: [
      { inline_data: { mime_type: 'image/png', data: fs.readFileSync(path.join(HIER, 'refs', 'ref-logo.png')).toString('base64') } },
      { text: prompt(s) },
    ] }],
    generationConfig: { responseModalities: ['IMAGE'], imageConfig: { aspectRatio: '4:3', imageSize: '2K' } },
  };
  for (let poging = 1; poging <= 3; poging++) {
    try {
      const r = await fetch(URL, { method: 'POST', headers: { 'Content-Type': 'application/json', 'x-goog-api-key': KEY }, body: JSON.stringify(body) });
      const j = await r.json();
      if (!r.ok) throw new Error(`${r.status} ${String(j.error?.message || '').slice(0, 160)}`);
      const d = j.candidates?.[0]?.content?.parts?.find(p => p.inlineData || p.inline_data);
      if (!d) throw new Error('geen beeld: ' + (j.candidates?.[0]?.finishReason || 'onbekend'));
      fs.writeFileSync(path.join(RUW, `kandidaat-${s.nr}.png`), Buffer.from((d.inlineData || d.inline_data).data, 'base64'));
      console.log(`OK   ${s.nr} ${s.naam}`);
      return;
    } catch (e) {
      console.log(`FOUT ${s.nr} (poging ${poging}): ${e.message}`);
      await new Promise(r => setTimeout(r, 4000 * poging));
    }
  }
}

// De BOVENSTE 16:9 uit het 4:3 beeld, daarna 1920x1080 webp op kwaliteit 85.
// Waarom de bovenste en niet het midden: het model zet een staande figuur hoe dan ook met het hoofd rond de
// halve beeldhoogte, hoe stellig de prompt ook is. Laat je de onderste kwart weg, dan komt dat hoofd op twee
// derde van de hoogte te staan, en dat is precies waar de kop van de pagina hem wil hebben. Een vaste snede is
// betrouwbaarder dan het model nog een keer om een andere uitsnede vragen.
async function af(s) {
  const bron = path.join(RUW, `kandidaat-${s.nr}.png`);
  if (!fs.existsSync(bron)) { console.log(`MIS  ${s.nr}: geen ruw beeld`); return; }
  const m = await sharp(bron).metadata();
  const hoog = Math.min(m.height, Math.round(m.width * 9 / 16));
  await sharp(bron).extract({ left: 0, top: 0, width: m.width, height: hoog })
    .resize(1920, 1080, { fit: 'cover', position: 'centre' })
    .webp({ quality: 85 }).toFile(path.join(UIT, `kandidaat-${s.nr}.webp`));
  console.log(`AF   ${s.nr} uit ${m.width}x${m.height}, bovenste ${hoog} naar 1920x1080`);
}

const args = process.argv.slice(2);
const alleenAf = args[0] === 'af';
const gekozen = args.filter(a => /^[1-5]$/.test(a)).map(Number);
const doen = gekozen.length ? SCENES.filter(s => gekozen.includes(s.nr)) : SCENES;
if (!alleenAf) for (const s of doen) await maak(s);
for (const s of doen) await af(s);
console.log('Klaar:', UIT);

export { SCENES, KADER, MODEL, prompt };
