// Realistische AI-foto's voor de homepage van Verhuisbedrijf De Reus.
// Model: gemini-3-pro-image-preview (nano banana pro), 2K.
//
// Key nooit in een bestand in de repo. Uit de omgeving, of uit ~/.gemini_api_key:
//   node gen.mjs              alles
//   node gen.mjs hero dienst  alleen scenes waarvan de naam zo begint
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

const HIER = path.dirname(fileURLToPath(import.meta.url));
const KEY = process.env.GEMINI_API_KEY ||
  (fs.existsSync(path.join(os.homedir(), '.gemini_api_key')) ? fs.readFileSync(path.join(os.homedir(), '.gemini_api_key'), 'utf8').trim() : '');
if (!KEY) { console.error('Geen GEMINI_API_KEY gevonden (omgeving of ~/.gemini_api_key).'); process.exit(1); }

const MODEL = 'gemini-3-pro-image-preview';
const URL = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`;
const LOGO = path.join(HIER, 'refs', 'ref-logo.png');

// ---- vaste afspraken voor elke foto ---------------------------------------------------------
const MERK = `
BRAND RULES (Verhuisbedrijf De Reus, a moving company in The Hague, the Netherlands):
- The attached image is the real De Reus logo: a yellow house (#FFCC33) between two flexing royal-blue arms (#1746A2),
  with the words "VERHUISBEDRIJF DE REUS". Reproduce it faithfully wherever the logo appears.
- VANS / TRUCKS: white box truck or white Mercedes Sprinter-type van. On the side: the full logo LARGE (house + arms +
  "DE REUS" in big yellow letters on a royal-blue band). No phone numbers, no other text, no other brands.
- CLOTHING: movers wear a royal-blue (#1746A2) polo shirt with a small yellow house symbol on the left chest (symbol only,
  NO text on shirts), navy work trousers, black safety shoes. Neat, clean, well-fitting.
- BOXES: plain brown kraft moving boxes with only the small yellow house symbol printed on the side. NO words on boxes,
  nothing handwritten.
- PEOPLE: an honest, diverse mix of Dutch people (different ages, builds, backgrounds). Natural, friendly, confident,
  not posed stock smiles. Never recreate a real, recognisable person. Hands must be anatomically correct (five fingers).
- SETTING: recognisably The Hague / the Netherlands: brick row houses, white window frames, bicycles, trees, brick
  streets. Realistic Dutch weather: bright, soft daylight, light clouds; not overly sunny.
- STYLE: photorealistic editorial photography, full-frame camera, 35 mm or 50 mm lens, natural colours, realistic skin
  texture, shallow depth of field where it fits. NOT illustration, NOT 3D render, NOT HDR, no text overlays, no watermark.
`;

// ---- scenes: naam, beeldverhouding, beschrijving -------------------------------------------
const SCENES = [
  ['hero-laden-bus', '16:9', 'Two movers load a De Reus box truck in a typical The Hague street with brick row houses. One passes a box to the other standing on the tail lift. Truck side with the large logo clearly visible. Eye level, wide shot, morning light. Leave calm space on the left side of the frame for a headline.'],
  ['over-ons-verhuisadviseur', '4:5', 'A De Reus moving advisor (woman, about 40) sits at a kitchen table with a couple in their thirties, going through the move plan on a tablet. Warm, trustworthy atmosphere in a Dutch home, a few folded moving boxes against the wall.'],
  ['dienst-particulier', '4:3', 'Two movers carefully carry a grey sofa wrapped in blue moving blankets out of the front door of a brick townhouse in The Hague, down the front steps. The De Reus van is parked in front.'],
  ['dienst-zakelijk', '4:3', 'Office move in a modern Dutch office: movers roll dollies with stacked plain grey crates between desks, one mover wraps a monitor. Clean, organised, professional.'],
  ['dienst-nationaal', '4:3', 'A De Reus box truck drives on a Dutch provincial road through a green polder landscape with a windmill far in the background. Side view with the logo readable, motion blur on the wheels.'],
  ['dienst-internationaal', '4:3', 'Movers load furniture wrapped in blankets and stretch film into a De Reus box truck at a loading dock, a wooden shipping crate on a pallet next to it. Early morning, professional logistics feel.'],
  ['dienst-woningontruiming', '4:3', 'A mostly empty, clean apartment after a house clearance: one mover sweeps the wooden floor, another carries out the last stack of De Reus boxes. Light falls through tall windows. Calm and respectful mood.'],
  ['dienst-opslag', '4:3', 'A clean, well-lit storage warehouse with rows of large wooden storage crates, each with the small yellow house symbol. A mover pushes a pallet jack. Tidy, secure, organised.'],
  ['dienst-handyman', '4:3', 'A mover in the De Reus polo assembles a white wardrobe with a cordless drill in a bright new bedroom, a few boxes around. Focus on skilled hands and the tool.'],
  ['dienst-verhuislift', '4:3', 'A moving lift (ladder lift) stands against the facade of a brick apartment building in The Hague, with a sofa going up on the platform to an open third-floor window. A mover operates the lift at street level, the De Reus van nearby. Low angle.'],
  ['verwachten-inpakken', '4:5', 'Close-up of a mover carefully wrapping an antique wooden cabinet in a thick blue moving blanket, taping it neatly. Shows care and craftsmanship. Soft window light.'],
  ['reviews-blij-nieuw-huis', '3:2', 'A happy couple in their new bright living room in The Hague, unpacking a De Reus box, laughing together. In the soft-focus background a mover places the last chair. Genuine, relaxed moment.'],
  ['werkwijze-planning', '4:5', 'A friendly De Reus planner at a desk in a small office, on the phone with a headset, laptop with a calendar open, a small De Reus logo sign on the wall behind. Bright, organised.'],
  ['aanvraag-verhuizer-doos', '4:5', 'Portrait of a strong, friendly mover (about 35) holding a De Reus box, looking into the camera, the De Reus van softly blurred behind him on a Hague street. Confident, approachable.'],
  // Werkwijze-rit: straatfoto + losse vrachtwagen die over de weg rijdt
  ['rit-straat', '21:9', 'A wide, eye-level panoramic street photo in The Hague. LEFT third: an older brick row house with white window frames and a few stacked moving boxes by the door (the old home). RIGHT third: a brighter, newer brick house with a small front garden and an open front door (the new home). Between and in front of them: an EMPTY asphalt road running horizontally across the ENTIRE width of the frame, filling the bottom 30% of the image, with a brick sidewalk behind it. NO vehicles, NO people, NO bicycles on the road. Camera perfectly level and perpendicular to the road, like a side-scrolling game background. Soft Dutch daylight.'],
  ['rit-wagen', '16:9', 'A PERFECT SIDE VIEW (exactly 90 degrees, facing RIGHT) of a white De Reus moving box truck (7.5-ton, cab on the right). The box body carries the full De Reus logo LARGE and sharp: yellow house between two flexing royal-blue arms, and "DE REUS" in big yellow letters on a royal-blue band along the bottom of the box. Realistic reflections, black tyres, chrome details. The truck is isolated on a PURE FLAT CHROMA-KEY GREEN background (#00FF00), completely even, no shadow, no floor, no road, nothing else in the image. The whole truck fits in frame with margin around it.'],
  ['contact-team-bus', '3:2', 'The De Reus team of four movers (mixed ages and backgrounds, one woman) standing relaxed in front of the De Reus box truck with its large logo, in a street in The Hague. Arms folded or hands in pockets, natural smiles.'],
];

const UIT = path.join(HIER, 'foto');
fs.mkdirSync(UIT, { recursive: true });

async function maak([naam, ratio, beschrijving]) {
  const body = {
    contents: [{ role: 'user', parts: [
      { inline_data: { mime_type: 'image/png', data: fs.readFileSync(LOGO).toString('base64') } },
      { text: `${MERK}\nSCENE: ${beschrijving}` },
    ] }],
    generationConfig: { responseModalities: ['IMAGE'], imageConfig: { aspectRatio: ratio, imageSize: '2K' } },
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
      const bestand = path.join(UIT, `${naam}.${ext}`);
      fs.writeFileSync(bestand, Buffer.from(d.data, 'base64'));
      console.log('OK   ', naam);
      return;
    } catch (e) {
      console.log(`FOUT ${naam} (poging ${poging}): ${e.message}`);
      await new Promise(r => setTimeout(r, 4000 * poging));
    }
  }
}

const filter = process.argv.slice(2);
const lijst = filter.length ? SCENES.filter(s => filter.some(f => s[0].startsWith(f))) : SCENES;
const TEGELIJK = 5;
for (let i = 0; i < lijst.length; i += TEGELIJK) await Promise.all(lijst.slice(i, i + TEGELIJK).map(maak));
console.log('Klaar:', UIT);
