// Stap 1 "Offerte aanvragen" op de home (#werkwijze): vijf kandidaten om img/stap-1-formulier.webp te vervangen.
// Zelfde patroon als contact-gen.mjs: nano banana pro (gemini-3-pro-image-preview) met het officiële logo als referentie.
//   node stap-1-gen.mjs            genereren (5 kandidaten, ruwe png in website/review/stap-1-ronde-1/ruw/)
//   node stap-1-gen.mjs 2 4        alleen kandidaat 2 en 4 opnieuw
//   node stap-1-gen.mjs webp       alleen de webp's maken (1120x760, kwaliteit 90) uit ruw/ of, als die er is, uit klaar/
// Key uit GEMINI_API_KEY of ~/.gemini_api_key (nooit in de repo, nooit printen).
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const HIER = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HIER, '..');
const UIT = path.join(ROOT, 'website', 'review', 'stap-1-ronde-1');
const RUW = path.join(UIT, 'ruw');
const KLAAR = path.join(UIT, 'klaar');
for (const d of [UIT, RUW, KLAAR]) fs.mkdirSync(d, { recursive: true });
const LOGO = path.join(ROOT, 'brandbook', 'assets', 'logo', 'dereus-logo.png');
const MODEL = 'gemini-3-pro-image-preview';
const URL = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`;

const MERK = `The attached image is the real logo of Verhuisbedrijf De Reus, a moving company in The Hague: a yellow (#FFCC33) house
between two flexing royal-blue (#1746A2) arms, with the words VERHUISBEDRIJF in blue and DE REUS in yellow underneath.
Wherever the logo appears, reproduce it EXACTLY like the reference, flat and undistorted, and put no other text or slogan near it.`;

const STIJL = `Photorealistic photograph, 50 mm lens, warm natural daylight from a window, shallow depth of field, natural colours,
realistic skin and anatomically correct hands (five fingers). No faces, no people in frame except hands and forearms.
Not an illustration, not a 3D render, no watermark, no extra text anywhere. Landscape framing with the main subject centred
and margin on all sides, so the picture can be cropped a little on the left and right or at the top and bottom.`;

export const KANDIDATEN = [
  {
    nr: 1, naam: 'Telefoon aan de keukentafel',
    prompt: `${MERK}

A hand holds a smartphone above a light wooden kitchen table, seen from above at about 45 degrees. On the screen is the
online quote request form of De Reus: a royal-blue header bar with the De Reus logo in its negative white-and-yellow
version on the left, and below it a clean white web form with the Dutch heading "Offerte aanvragen" and short input
fields labelled "Van", "Naar" and "Verhuisdatum", the last one being typed with a thumb. In the soft background,
out of focus: a stack of brown cardboard moving boxes and a cup of coffee. ${STIJL}`,
  },
  {
    nr: 2, naam: 'Laptop met plattegrond',
    prompt: `${MERK}

Two hands type on a silver laptop on a wooden desk, seen from the side at desk height, like a candid office photo.
The laptop screen faces the camera at a slight angle and shows one plain white web page with NOTHING on it except:
the De Reus logo at the top left, the Dutch heading "Offerte aanvragen" in bold dark blue, and three empty rounded
input boxes with no labels underneath the heading. No menu, no navigation bar, no browser tabs, no address bar,
no paragraph text, no small print, no button text: the screen edge is plain and the page is otherwise empty white.
Next to the laptop lies a printed floor plan of a flat (lines only, no readable words) and a set of house keys.
The room behind is blurred and bright. ${STIJL}`,
  },
  {
    nr: 3, naam: 'Papieren formulier op klembord',
    prompt: `${MERK}

Top-down flat lay on an oak table: a printed De Reus quote request form on a black clipboard. The paper has the De Reus
logo printed at the top left, the Dutch title "Offerteaanvraag" and a few neat empty lines and tick boxes underneath
(no readable small text, just clean lines and boxes). A hand with a blue ballpoint pen is filling in the first line.
Beside the clipboard: a pair of reading glasses, a house key with a plain tag, and the corner of a brown moving box.
${STIJL}`,
  },
  {
    nr: 4, naam: 'Tablet in de lege woning',
    prompt: `${MERK}

Inside an empty, freshly painted living room with a large window and wooden floor, two hands and forearms enter the frame
from the bottom edge and hold a tablet in landscape orientation, seen from above at about 45 degrees. Strictly no head,
no shoulders, no body in the frame, only the hands and forearms. The tablet shows the De Reus quote form: royal-blue
header with the negative white-and-yellow De Reus logo, white page with the Dutch heading "Offerte aanvragen" and the
fields "Van", "Naar" and "Verhuisdatum", with a finger about to tap a yellow button. Two moving boxes and a roll of
tape stand on the floor further back, out of focus. ${STIJL}`,
  },
  {
    nr: 5, naam: 'Map met notitie en telefoon',
    prompt: `${MERK}

Top-down flat lay on a white kitchen counter in warm morning light: a royal-blue cardboard folder with the De Reus logo
printed large and flat on its front, a smartphone lying next to it whose screen shows ONLY a plain white page with a
royal-blue header bar and the Dutch heading "Offerte aanvragen" in bold dark blue below it and three empty rounded input
boxes; no browser bar, no status bar, no menu, no labels, no small print, no other words anywhere on the screen.
Also a blank yellow sticky note with nothing written on it, a pen, and a small bunch of house keys. One hand reaches into the frame from the bottom edge and picks up the phone. Everything is arranged loosely,
not perfectly aligned, like a real counter. ${STIJL}`,
  },
];

function sleutel() {
  const f = path.join(os.homedir(), '.gemini_api_key');
  return process.env.GEMINI_API_KEY || (fs.existsSync(f) ? fs.readFileSync(f, 'utf8').trim() : '');
}

async function logoRef() {
  // Het officiële merk op wit, 1024 breed, zodat het model het teken scherp ziet.
  return (await sharp(LOGO).flatten({ background: '#ffffff' }).resize({ width: 1024 })
    .extend({ top: 60, bottom: 60, left: 60, right: 60, background: '#ffffff' }).png().toBuffer()).toString('base64');
}

async function maak(k, ref) {
  const KEY = sleutel();
  if (!KEY) { console.error('Geen GEMINI_API_KEY (omgeving of ~/.gemini_api_key).'); process.exit(1); }
  const body = {
    contents: [{ role: 'user', parts: [
      { inline_data: { mime_type: 'image/png', data: ref } },
      { text: k.prompt },
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
      const data = (d.inlineData || d.inline_data).data;
      fs.writeFileSync(path.join(RUW, `kandidaat-${k.nr}.png`), Buffer.from(data, 'base64'));
      const m = await sharp(path.join(RUW, `kandidaat-${k.nr}.png`)).metadata();
      console.log(`OK   kandidaat-${k.nr} ${m.width}x${m.height}`);
      return;
    } catch (e) {
      console.log(`FOUT kandidaat-${k.nr} (poging ${poging}): ${e.message}`);
      await new Promise(r => setTimeout(r, 4000 * poging));
    }
  }
}

// 1120x760, het onderwerp in het midden (cover-crop vanuit het midden), kwaliteit 90.
async function webp(nr) {
  const klaar = path.join(KLAAR, `kandidaat-${nr}.png`);
  const bron = fs.existsSync(klaar) ? klaar : path.join(RUW, `kandidaat-${nr}.png`);
  if (!fs.existsSync(bron)) { console.log(`--   kandidaat-${nr}: geen bron`); return; }
  await sharp(bron).resize(1120, 760, { fit: 'cover', position: 'centre' }).webp({ quality: 90 })
    .toFile(path.join(UIT, `kandidaat-${nr}.webp`));
  console.log(`WEBP kandidaat-${nr} uit ${path.basename(path.dirname(bron))}/`);
}

export function prompts() {
  // prompts.md in de kandidatenmap: per kandidaat het exacte prompt en het model.
  const kop = `# Prompts stap 1, ronde 1\n\nModel: ${MODEL} (nano banana pro), beeldverhouding 3:2, 2K, met als bijlage het officiële logo ` +
    `brandbook/assets/logo/dereus-logo.png op wit. Daarna met sharp naar 1120x760 (cover, midden), webp kwaliteit 90.\n\n`;
  const blokken = KANDIDATEN.map(k => `## Kandidaat ${k.nr}: ${k.naam}\n\n\`\`\`\n${k.prompt.trim()}\n\`\`\`\n`).join('\n');
  fs.writeFileSync(path.join(UIT, 'prompts.md'), kop + blokken, 'utf8');
  console.log('prompts.md geschreven');
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  if (args[0] === 'prompts') {
    prompts();
  } else {
    if (args[0] !== 'webp') {
      const welke = args.length ? KANDIDATEN.filter(k => args.includes(String(k.nr))) : KANDIDATEN;
      const ref = await logoRef();
      await Promise.all(welke.map(k => maak(k, ref)));
    }
    for (const k of KANDIDATEN) await webp(k.nr);
    prompts();
    console.log('Klaar:', UIT);
  }
}
