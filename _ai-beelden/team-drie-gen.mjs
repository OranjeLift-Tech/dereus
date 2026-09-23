// Vijf kandidaten "drie verhuizers dicht bij elkaar", als vervanger van img/team-de-reus.webp.
// In het huidige beeld staan de drie ver uit elkaar over de volle breedte; deze ronde zoekt
// een compositie waarin ze bij elkaar staan, bezig met hetzelfde karwei.
//
// Patroon van gen.mjs: gemini-3-pro-image-preview, 2K, key uit ~/.gemini_api_key.
//   node team-drie-gen.mjs            alle vijf
//   node team-drie-gen.mjs v2 v4      alleen die versies (bijgenereren na afkeuren)
//
// Twee afwijkingen van gen.mjs, allebei met opzet:
// 1. Het merk gaat NIET mee in de prompt en refs/ref-logo.png wordt niet gestuurd. Dat bestand
//    is het oude logo mét tagline, en het model tekent een merk sowieso na in plaats van het te
//    plaatsen. Effen polo's, effen witte bus; het echte beeldmerk komt er later met sharp op.
// 2. Drie referentiegezichten gaan als aparte delen mee, dezelfde drie in alle vijf composities.
//    Er blijft er maar één versie over, dus de gebruiker moet composities vergelijken en geen
//    wisselende bezettingen.
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
const UIT = path.join(HIER, 'archief', 'team-drie-20260922');
fs.mkdirSync(path.join(UIT, 'refs'), { recursive: true });

// ---- de ploeg ---------------------------------------------------------------------------------
// Drie duidelijk verschillende mensen: dat gezichten op elkaar lijken is de vaste fout in deze
// beelden. Leeftijden 60 / 45 / 30, verschillende huid, en een vrouw erbij zoals in het huidige
// beeld. De gezichten van de tweetalronde van dereus-ad blijven buiten schot.
const PLOEG = [
  { rol: 'Person 1 (the oldest, on the left)', bestand: 'mannen/man-07.png',
    zegt: 'a weathered Dutch man of about 60, short grey hair, full grey beard, deep lines around the eyes' },
  { rol: 'Person 2 (in the middle)', bestand: 'mannen/man-10.png', snij: { top: 0, left: 0, width: 222, height: 158 },
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
    const doel = path.join(UIT, 'refs', path.basename(p.bestand));
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

// ---- vijf composities ---------------------------------------------------------------------------
const VERSIES = [
  ['v1', 'Samen tillen bij de laadklep',
   'The three movers lift ONE heavy cabinet wrapped in thick blue moving blankets together onto the tail lift of a plain white box truck. All three have their hands on the same piece; their shoulders almost touch. Eye level, slightly low angle looking up at them, full bodies, brick row houses behind. The effort is visible in their arms and faces.'],
  ['v2', 'Om de steekwagen heen',
   'The three movers cluster tightly around ONE hand truck stacked with plain brown boxes at the open rear of a plain white van. The oldest steadies the top box with both hands, the middle one tilts the hand truck back, the youngest has a hand on the stack and is looking at the other two. Camera just above eye level, three-quarter view, the group filling the middle of the frame.'],
  ['v3', 'Doorgeven bij de open laadbak',
   'A tight human chain of three at the open rear of a plain white box truck: two stand on the brick pavement and the third stands on the tail lift, all within arm\'s reach, passing the same plain brown box from hand to hand. Their bodies overlap in the frame. Eye level, 50 mm, shallow depth of field, the truck interior soft behind them.'],
  ['v4', 'Overleg op de stoep voor de voordeur',
   'The three movers stand shoulder to shoulder on the front steps of a brick townhouse, halfway through the job. The middle one points at the doorway while the other two look that way; one has a folded blue moving blanket over his shoulder, one holds a roll of tape. Slightly low angle from the pavement, their heads close together, the open front door dark behind them.'],
  ['v5', 'Schouder aan schouder met een zware kast',
   'Close waist-up framing of the three movers carrying ONE blanket-wrapped cabinet together along a brick pavement in The Hague, walking towards the camera. They are pressed close, the cabinet held between them, all faces clearly visible and all different. 35 mm, the street and a plain white van soft behind them.'],
];

async function maak([naam, titel, beschrijving], refBestanden) {
  const personen = PLOEG.map((p, i) =>
    `${p.rol}: use reference image ${i + 1} for face identity, age and expression ONLY. Ignore the clothing, helmet, glasses frame, background and any markings in that reference. He or she is ${p.zegt}.`).join('\n');
  const tekst = `${MERK}
THE THREE PEOPLE (they must look like three clearly different individuals, not three versions of one face):
${personen}

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

const jsonPad = path.join(UIT, 'team-drie.json');
const bestaand = fs.existsSync(jsonPad) ? JSON.parse(fs.readFileSync(jsonPad, 'utf8')) : {};
fs.writeFileSync(jsonPad, JSON.stringify({
  beeld: 'kandidaten voor de vervanger van img/team-de-reus.webp (1200x1140, home en over-ons)',
  datum: '2026-09-22',
  aanleiding: 'In het huidige beeld staan de drie verhuizers ver uit elkaar over de volle breedte. Gevraagd: drie verhuizers dicht bij elkaar, vijf versies om uit te kiezen.',
  model: MODEL,
  beeldverhouding: '1:1, 2K. Uitsnede naar 1200x1140 pas na de keuze.',
  merk: 'Bewust uit de prompt gehouden, en refs/ref-logo.png NIET meegestuurd: dat is het oude logo met tagline. Polo effen, bus effen wit. Het echte beeldmerk (brandbook/assets/logo/dereus-beeldmerk-negatief.png op de borst) wordt na de keuze met sharp gecomposit.',
  referentiegezichten: PLOEG.map(p => ({ rol: p.rol, bestand: p.bestand, beschrijving: p.zegt, bewerking: p.snij ? 'onderrand weggesneden vanwege het Getty-watermerk' : 'ongewijzigd' })),
  gezichten_elders: 'man-01, 02, 04, 05, 06, 09, 16, 18, 20 en vrouw-02 zijn vergeven aan de tweetalronde van dereus-ad; die blijven hier buiten beeld.',
  versies: { ...(bestaand.versies || {}), ...Object.fromEntries(gedaan.map(g => [g.naam, { titel: g.titel, prompt: g.prompt, mislukt: g.mislukt || false }])) },
}, null, 2));
console.log('Klaar:', UIT);
