// Vijf kandidaten "drie verhuizers dicht bij elkaar, één met een doos".
// Afgeleid van team-drie-gen.mjs (zelfde ronde, zelfde ploeg). Verschil met die ronde: in elke
// versie draagt precies ÉÉN van de drie een doos, en die doos moet één schoon plat vlak naar de
// camera hebben. Daar gaat het echte beeldmerk later met sharp op; een gekantelde, half bedekte
// of beplakte doos is daarmee onbruikbaar.
//
//   node drie-doos-gen.mjs                 alle vijf, gelijktijdig
//   node drie-doos-gen.mjs versie-2 versie-4   alleen die versies (bijgenereren na afkeuren)
//
// Twee afwijkingen van gen.mjs, allebei met opzet en overgenomen uit team-drie-gen.mjs:
// 1. Het merk gaat NIET mee in de prompt en refs/ref-logo.png wordt niet gestuurd. Het model
//    tekent een merk sowieso na in plaats van het te plaatsen. Effen polo's, effen witte bus,
//    onbedrukte doos; het echte beeldmerk komt er later met sharp op.
// 2. Dezelfde drie referentiegezichten in alle vijf composities. Er blijft maar één versie over,
//    dus de gebruiker vergelijkt composities en geen wisselende bezetting.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import sharp from 'sharp';
import { fileURLToPath } from 'node:url';

const HIER = path.dirname(fileURLToPath(import.meta.url));
const KEY = process.env.GEMINI_API_KEY ||
  (fs.existsSync(path.join(os.homedir(), '.gemini_api_key')) ? fs.readFileSync(path.join(os.homedir(), '.gemini_api_key'), 'utf8').trim() : '');
if (!KEY) { console.error('Geen GEMINI_API_KEY gevonden (omgeving of ~/.gemini_api_key).'); process.exit(1); }

const MODEL = 'gemini-3-pro-image-preview';
const URL = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`;
const GEZICHTEN = path.join(os.homedir(), '.claude', 'skills', 'foto-verbeteren', 'assets', 'gezichten');
const UIT = path.join(HIER, '..', 'website', 'review', 'drie-verhuizers-doos-20260922');
const WERK = path.join(HIER, 'archief', 'drie-doos-20260922');
fs.mkdirSync(UIT, { recursive: true });
fs.mkdirSync(path.join(WERK, 'refs'), { recursive: true });

// ---- de ploeg ---------------------------------------------------------------------------------
// Exact dezelfde drie als de team-drie-ronde van vandaag, inclusief dezelfde uitsnede op man-10.
const PLOEG = [
  { rol: 'Person 1 (the oldest)', bestand: 'mannen/man-07.png',
    zegt: 'a weathered Dutch man of about 60, short grey hair, full grey beard, deep lines around the eyes' },
  { rol: 'Person 2 (the middle one)', bestand: 'mannen/man-10.png', snij: { top: 0, left: 0, width: 222, height: 158 },
    zegt: 'a broad-shouldered man of about 45 with brown skin, short dark hair, an open warm smile' },
  { rol: 'Person 3 (the youngest)', bestand: 'vrouwen/vrouw-03.png',
    zegt: 'a woman of about 30 with brown skin, dark hair in braids tied back, slim glasses' },
];

// man-10 draagt rechtsonder een Getty-watermerk. Als gezichtsreferentie mag hij, maar het
// watermerk mag het model niet te zien krijgen: tekst in beeld is een afkeurgrond.
async function refs() {
  const uit = [];
  for (const p of PLOEG) {
    const bron = path.join(GEZICHTEN, p.bestand);
    const doel = path.join(WERK, 'refs', path.basename(p.bestand));
    const s = sharp(bron).flatten({ background: '#ffffff' });
    await (p.snij ? s.extract(p.snij) : s).png().toFile(doel);
    uit.push(doel);
  }
  return uit;
}

// ---- vaste afspraken, merkregels eruit ---------------------------------------------------------
const MERK = `
BRAND AND SCENE RULES (De Reus, a moving company in The Hague, the Netherlands):
- NO LOGOS AND NO TEXT ANYWHERE IN THE IMAGE. This is essential. The movers wear PLAIN royal-blue
  (#1746A2) polo shirts with NOTHING printed or embroidered on them: no symbol, no logo, no text,
  clean empty fabric on chest, back and sleeves. Navy work trousers, black safety shoes.
- The van or box truck in frame is PLAIN WHITE with no lettering, no logo, no phone number, no
  livery of any kind. Moving boxes are plain brown kraft with NOTHING printed on them.
- No signage, no house numbers, no street names, no number plates, no brand names anywhere.
  If any surface would normally carry text, leave it blank.
- This includes SMALL objects, which is where invented branding creeps in: work gloves carry NO
  brand mark, NO coloured lettering, NO logo patch and no printed cuff - either bare hands or
  plain unmarked gloves in one flat colour. Tape rolls are blank, no labels, no stickers, no tags,
  no product markings on tools. Look over every object in the frame and leave it unbranded.
- PEOPLE: real, ordinary Dutch working people. Natural skin texture, visible pores, uneven skin
  tone, stubble and wrinkles where they belong, no retouching, no beauty filter, no stock smiles.
  Hands with five fingers, grip consistent with the object's weight, knuckles and tendons visible
  under load. Working clothes that have been worn: slight creases, a little dust.
- SETTING: recognisably The Hague: brick row houses, white window frames, bicycles, trees, brick
  pavement. Realistic Dutch daylight, bright but softly overcast, not sunny.
- STYLE: photorealistic editorial reportage, full-frame camera, 35 mm or 50 mm lens, natural
  colours, shallow depth of field where it fits. NOT illustration, NOT 3D render, NOT HDR,
  no text overlays, no watermark.
- THE THREE STAY CLOSE TOGETHER: all three within roughly one metre of each other, busy with the
  same single task, bodies overlapping in the frame. Never spread across the width of the picture.
`;

// De doosregels staan apart en aan het eind, want dit is wat deze ronde van de vorige onderscheidt.
// Het vlak naar de camera is de plek waar het beeldmerk later op gecomposit wordt.
const DOOS = `
THE BOX (this is the most important requirement of the whole image):
- Exactly ONE of the three carries a single plain cardboard moving box. The other two do not carry
  a box; they are busy with the same job (steadying it, a blanket, a hand truck, the van doors).
- The box is ordinary brown corrugated kraft cardboard, completely unprinted and unmarked: no
  logo, no text, no stamp, no barcode, no stickers, no handwriting, no shipping label, no coloured
  tape, no printed arrows or symbols. Blank on every side that is visible.
- ONE LARGE FACE OF THE BOX IS TURNED SQUARELY TOWARDS THE CAMERA and is fully visible: flat, not
  tilted away, not foreshortened, not in perspective at a sharp angle, not cropped by the edge of
  the frame. That face is clean, evenly lit, free of deep shadow and free of glare.
- Nothing crosses that face: no hand, no fingers, no forearm, no strap, no tape seam, no other
  object in front of it. The carrying hands grip the box at the bottom edge and the far side only.
- The box is held high enough to be clearly readable in the frame, roughly between waist and chest
  height, and it is a decent size in the picture: not a small prop in the distance.
- The cardboard looks used but sound: slight scuffs and soft corners, no crushed or torn panels.
`;

// ---- vijf composities ---------------------------------------------------------------------------
// Bewust vijf verschillende camerahoogtes, afstanden, plekken en dragers. Niet vijf keer dezelfde
// opstelling met een andere uitsnede.
const VERSIES = [
  ['versie-1', 'Op straat, lage camera, de jongste draagt de doos',
   'On the brick pavement of a Hague street, in front of brick row houses. LOW CAMERA, kneeling at about hip height and looking slightly up at the three, FULL BODIES from head to shoes. The youngest (Person 3) stands in the middle of the group and carries the box in both arms at chest height, with one face of the box turned flat towards the camera. The oldest (Person 1) stands immediately to her left with a folded blue moving blanket over his forearm, the middle one (Person 2) immediately to her right with a hand on the top corner of the box. Their shoulders touch; the group fills the centre of the frame. A plain white van is parked soft in the background.'],

  ['versie-2', 'Halffiguur bij de open achterdeuren van de bus, middelste draagt',
   'At the open rear doors of a plain white van, both doors swung wide. CAMERA AT EYE LEVEL, straight on, MEDIUM FRAMING from the waist up, the three filling the width of the frame. The middle one (Person 2) is in the centre and holds the box in front of his chest, both hands under the bottom edge, one face of the box turned flat towards the camera. The oldest (Person 1) leans in from the left with a hand on the door frame, the youngest (Person 3) from the right looking at the box. Their heads are close together. The dark interior of the van is soft behind them.'],

  ['versie-3', 'In de laadruimte, camera op kniehoogte van buiten naar binnen, de oudste draagt',
   'Inside the cargo hold of a plain white box truck, seen from just outside the open tail. CAMERA LOW, at about knee height, looking slightly up into the load space; THREE-QUARTER BODIES. The three are crowded together in the opening between stacked plain brown boxes and blue moving blankets. The oldest (Person 1) is in the middle, stepping forward with the box held at chest height in both hands, one face turned flat towards the camera. The middle one (Person 2) crouches beside him steadying a stack, the youngest (Person 3) stands right behind them with a hand on his shoulder. Soft daylight falls in from the open tail; the inside of the truck is dim and plain.'],

  ['versie-4', 'Hoge camera vanaf de stoeptrede, neerkijkend op de drie, middelste draagt',
   'Seen from the top of the front steps of a brick townhouse, looking DOWN at the three movers standing close together on the brick pavement below. HIGH CAMERA ANGLE, about a metre above their heads, MEDIUM-WIDE framing from the knees up; their heads are close together and tilted up towards the camera. The middle one (Person 2 - he has BROWN SKIN, short dark hair and a warm open smile, exactly the man in reference image 2; do not replace him with a light-skinned man) holds the box up in front of him at chest height, one face of the box turned flat up towards the camera. The oldest (Person 1) stands on his left with a roll of plain tape, the youngest (Person 3) on his right, both looking up. Brick pavement, a parked bicycle and a plain white van around them.'],

  ['versie-5', 'Dichtbij, borstbeeld, de drie lopen samen naar de camera, de jongste draagt',
   'CLOSE FRAMING, chest up, the three movers walking side by side straight towards the camera along a brick pavement in The Hague. CAMERA AT CHEST HEIGHT, 35 mm, the three pressed close so their shoulders overlap and all three faces are large and clearly visible and clearly different. The youngest (Person 3) walks in the centre and carries the box in front of her, so the box sits large in the lower third of the frame with one face turned flat towards the camera. The oldest (Person 1) is on the left, the middle one (Person 2) on the right, both with empty hands close to the box as if ready to take it. The street and a plain white van are soft and out of focus behind them.'],
];

async function maak([naam, titel, beschrijving], refBestanden) {
  const personen = PLOEG.map((p, i) =>
    `${p.rol}: use reference image ${i + 1} for face identity, age and expression ONLY. Ignore the clothing, helmet, glasses frame, background and any markings in that reference. He or she is ${p.zegt}.`).join('\n');
  const tekst = `${MERK}
THE THREE PEOPLE (they must look like three clearly different individuals, not three versions of one face):
${personen}
${DOOS}
SCENE: ${beschrijving}`;

  const body = {
    contents: [{ role: 'user', parts: [
      ...refBestanden.map(f => ({ inline_data: { mime_type: 'image/png', data: fs.readFileSync(f).toString('base64') } })),
      { text: tekst },
    ] }],
    generationConfig: { responseModalities: ['IMAGE'], imageConfig: { aspectRatio: '1:1', imageSize: '2K' } },
  };

  for (let poging = 1; poging <= 3; poging++) {
    try {
      const r = await fetch(URL, { method: 'POST', headers: { 'Content-Type': 'application/json', 'x-goog-api-key': KEY }, body: JSON.stringify(body) });
      const j = await r.json();
      if (!r.ok) throw new Error(`${r.status} ${j.error?.message?.slice(0, 160)}`);
      const deel = j.candidates?.[0]?.content?.parts?.find(p => p.inlineData || p.inline_data);
      if (!deel) throw new Error('geen beeld in antwoord: ' + (j.candidates?.[0]?.finishReason || 'onbekend'));
      const d = deel.inlineData || deel.inline_data;
      fs.writeFileSync(path.join(UIT, `${naam}.png`), Buffer.from(d.data, 'base64'));
      console.log('OK   ', naam, '-', titel);
      return { naam, titel, prompt: tekst };
    } catch (e) {
      console.log(`FOUT ${naam} (poging ${poging}): ${e.message}`);
      await new Promise(r => setTimeout(r, 4000 * poging));
    }
  }
  return { naam, titel, prompt: tekst, mislukt: true };
}

const filter = process.argv.slice(2);
const lijst = filter.length ? VERSIES.filter(v => filter.includes(v[0])) : VERSIES;
const refBestanden = await refs();
const gedaan = await Promise.all(lijst.map(v => maak(v, refBestanden)));

const jsonPad = path.join(UIT, 'LEESMIJ.json');
const bestaand = fs.existsSync(jsonPad) ? JSON.parse(fs.readFileSync(jsonPad, 'utf8')) : {};
fs.writeFileSync(jsonPad, JSON.stringify({
  beeld: 'drie verhuizers dicht bij elkaar, één met een doos - vijf composities om uit te kiezen',
  datum: '2026-09-22',
  aanleiding: 'Gevraagd: "5 versions of a new image of 3 workers close together, one holding a branded box".',
  model: MODEL,
  beeldverhouding: '1:1, 2K (volle resolutie zoals het model levert). Uitsnede pas na de keuze.',
  generator: '_ai-beelden/drie-doos-gen.mjs (kopie van team-drie-gen.mjs, met doosregels erbij)',
  merk: 'Bewust uit de prompt gehouden en refs/ref-logo.png NIET meegestuurd. Polo effen royal blue, bus effen wit, doos onbedrukt met één schoon plat vlak naar de camera. Het echte beeldmerk wordt daarna met sharp op dat vlak gecomposit (aparte sessie).',
  cast: 'Exact dezelfde drie als de team-drie-ronde van vandaag, in alle vijf versies gelijk, zodat de gebruiker composities vergelijkt en geen wisselende bezetting.',
  referentiegezichten: PLOEG.map(p => ({ rol: p.rol, bestand: p.bestand, beschrijving: p.zegt, bewerking: p.snij ? 'onderrand weggesneden vanwege het Getty-watermerk' : 'ongewijzigd' })),
  versies: { ...(bestaand.versies || {}), ...Object.fromEntries(gedaan.map(g => [g.naam, { bestand: `${g.naam}.png`, titel: g.titel, prompt: g.prompt, mislukt: g.mislukt || false }])) },
}, null, 2));
console.log('Klaar:', UIT);
