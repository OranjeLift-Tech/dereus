// Dienstenkaarten op de homepage: 8 realistische foto's waarop je meteen ziet dat het De Reus is
// (bus met groot logo, koningsblauwe polo met logo, dozen en kratten met logo).
//   node diensten-gen.mjs                  genereren (nano banana pro) en meteen klaarzetten in ../img
//   node diensten-gen.mjs zakelijk opslag  alleen deze diensten
//   node diensten-gen.mjs --prompts        zonder key: prompts voor de Gemini-app in PROMPTS-diensten.txt
//   node diensten-gen.mjs --klaar          alleen foto/dienst-*.png|jpg omzetten naar ../img/dienst-*.webp (720x540)
// Key uit GEMINI_API_KEY of ~/.gemini_api_key (nooit in de repo).
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const HIER = path.dirname(fileURLToPath(import.meta.url));
const UIT = path.join(HIER, 'foto');
const IMG = path.join(HIER, '..', 'img');
fs.mkdirSync(UIT, { recursive: true });
const LOGO = path.join(HIER, 'refs', 'ref-logo.png');
const MODEL = 'gemini-3-pro-image-preview';
const URL = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`;
const KEY = process.env.GEMINI_API_KEY ||
  (fs.existsSync(path.join(os.homedir(), '.gemini_api_key')) ? fs.readFileSync(path.join(os.homedir(), '.gemini_api_key'), 'utf8').trim() : '');

const MERK = `
BRAND RULES (Verhuisbedrijf De Reus, a moving company in The Hague, the Netherlands).
The goal of this photo: a viewer must see within one second that this is De Reus. The brand must be clearly visible.
- The attached image is the real De Reus logo: a yellow house (#FFCC33) held between two flexing royal-blue arms (#1746A2),
  with the words "VERHUISBEDRIJF" (small, blue) and "DE REUS" (big, yellow). Reproduce it faithfully, sharp and undistorted,
  wherever the logo appears. The only text allowed anywhere in the image is "VERHUISBEDRIJF DE REUS" / "DE REUS".
- VEHICLES: white box truck or white Mercedes Sprinter-type van. On the side: the full logo LARGE, plus "DE REUS" in big
  yellow letters on a royal-blue band along the bottom. No phone numbers, no website, no other brands.
- CLOTHING: every mover wears a royal-blue (#1746A2) polo shirt. FRONT: the small house-with-arms logo on the left chest.
  BACK: the full logo large between the shoulder blades with "DE REUS" in yellow letters under it. Navy work trousers,
  black safety shoes. Neat, clean, well-fitting. No other prints.
- BOXES / CRATES: brown kraft moving boxes printed on the side with the De Reus logo in blue and yellow, closed with
  yellow tape. Nothing handwritten, no other words.
- PEOPLE: an honest mix of Dutch people (different ages, builds, backgrounds). Natural, friendly, concentrated on their
  work, not posed stock smiles. Never a real, recognisable person. Hands anatomically correct (five fingers).
- SETTING: recognisably The Hague / the Netherlands: brick row houses, white window frames, bicycles, brick streets,
  Dutch licence-plate shape (yellow). Realistic Dutch weather: soft daylight, light clouds.
- STYLE: photorealistic editorial photography, full-frame camera, 35 mm lens, natural colours, realistic skin texture,
  slight imperfections (scuffs on the van, creases in the blankets). NOT illustration, NOT 3D render, NOT HDR,
  no text overlays, no watermark, no borders.
- COMPOSITION: 4:3 landscape. Keep the main subject and at least one clearly readable De Reus logo inside the central
  80% of the frame, because the photo is cropped slightly in a card.
`;

// naam, scene, alt-tekst voor de website
const SCENES = [
  ['dienst-particulier',
    'Two De Reus movers carefully carry a sofa wrapped in royal-blue moving blankets out of the front door of a brick townhouse in The Hague. The white De Reus van is parked right behind them at the kerb, side doors open, its large logo clearly readable. The front mover is seen from the back, so the big logo on the back of his polo is visible; the other faces the camera.',
    'Twee verhuizers van De Reus dragen een ingepakte bank naar de verhuisbus van De Reus.'],
  ['dienst-zakelijk',
    'Office move in a modern Dutch office. Two De Reus movers roll dollies with stacked royal-blue plastic moving crates, each crate carrying the De Reus logo on a white label panel. One mover is seen from the back (big back logo visible), the other wraps a monitor in bubble wrap. Through the floor-to-ceiling window behind them the white De Reus truck with its large logo is parked outside.',
    'Verhuizers van De Reus rijden blauwe verhuiskratten door een kantoor, buiten staat de vrachtwagen van De Reus.'],
  ['dienst-nationaal',
    'A white De Reus box truck drives on a Dutch provincial road through a flat green polder with a ditch, pollard willows and a windmill far in the background. Three-quarter side view so the whole box side is visible: the large logo and "DE REUS" in big yellow letters on the royal-blue band are perfectly readable. Slight motion blur on the wheels and road only.',
    'De vrachtwagen van De Reus rijdt over een polderweg met een molen op de achtergrond.'],
  ['dienst-internationaal',
    'At a loading dock in the early morning, two De Reus movers load furniture wrapped in blankets and stretch film into a white De Reus box truck. Next to it on a pallet stands a wooden export crate, stencilled in blue with the De Reus logo. The truck side with the large logo is in frame and readable; in the far background a few stacked sea containers without any text.',
    'Verhuizers van De Reus laden ingepakte meubels en een houten exportkist in de vrachtwagen van De Reus.'],
  ['dienst-woningontruiming',
    'A nearly empty, clean Dutch apartment with a wooden floor and tall windows after a house clearance. One De Reus mover, seen from the back with the big logo on his polo, carries the last two De Reus boxes to the door; a second mover sweeps the floor. Through the window the white De Reus van with its logo is visible in the street below. Calm, respectful mood, soft window light.',
    'Verhuizers van De Reus dragen de laatste dozen uit een lege, schoongeveegde woning.'],
  ['dienst-opslag',
    'A clean, well-lit storage warehouse with rows of large wooden storage containers, each with a white plate showing the De Reus logo and a number. A De Reus mover pushes a pallet jack with a container down the aisle, walking away from the camera so the big back logo is visible. On the end wall hangs a large royal-blue sign with the De Reus logo. Tidy, secure, organised.',
    'Een medewerker van De Reus rijdt een houten opslagcontainer door de opslagloods van De Reus.'],
  ['dienst-handyman',
    'A De Reus mover kneels in a bright new bedroom and assembles a white wardrobe with a cordless drill (no brand name on the tool). He is turned three-quarters to the camera so the logo on the left chest of his royal-blue polo is sharp and readable. Next to him an open royal-blue tool case with the De Reus logo on the lid and one De Reus moving box. Focus on skilled hands, the tool and the logo.',
    'Een vakman van De Reus zet met een accuboormachine een kledingkast in elkaar.'],
  ['dienst-verhuislift',
    'A moving lift (ladder lift, furniture hoist) stands against the facade of a brick apartment building in The Hague. The lift is mounted on a small white De Reus truck with the large logo on the door and side; the lift platform has a royal-blue panel with "DE REUS" in yellow letters. A sofa wrapped in blue blankets goes up to an open third-floor window where a mover waits. At street level a De Reus mover, seen from the back with the big logo, operates the controls. Slightly low angle.',
    'De verhuislift van De Reus brengt een bank naar de derde verdieping van een Haags appartementengebouw.'],
];

async function maak([naam, scene]) {
  const body = {
    contents: [{ role: 'user', parts: [
      { inline_data: { mime_type: 'image/png', data: fs.readFileSync(LOGO).toString('base64') } },
      { text: `${MERK}\nSCENE: ${scene}` },
    ] }],
    generationConfig: { responseModalities: ['IMAGE'], imageConfig: { aspectRatio: '4:3', imageSize: '2K' } },
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
      for (const e of ['png', 'jpg']) fs.rmSync(path.join(UIT, `${naam}.${e}`), { force: true });
      fs.writeFileSync(path.join(UIT, `${naam}.${ext}`), Buffer.from(d.data, 'base64'));
      console.log('OK   ', naam);
      return;
    } catch (e) {
      console.log(`FOUT ${naam} (poging ${poging}): ${e.message}`);
      await new Promise(r => setTimeout(r, 4000 * poging));
    }
  }
}

// foto/dienst-x.png -> ../img/dienst-x.webp, 720x540 zoals de kaarten, en de alt-tekst in index.html bijwerken
async function klaar(lijst) {
  const html = path.join(HIER, '..', 'index.html');
  let s = fs.readFileSync(html, 'utf8');
  let n = 0;
  for (const [naam, , alt] of lijst) {
    const bron = ['png', 'jpg', 'jpeg', 'webp'].map(e => path.join(UIT, `${naam}.${e}`)).find(fs.existsSync);
    if (!bron) { console.log('--    ', naam, '(geen bron in foto/)'); continue; }
    await sharp(bron).resize(720, 540, { fit: 'cover', position: 'attention' }).webp({ quality: 80 }).toFile(path.join(IMG, `${naam}.webp`));
    s = s.replace(new RegExp(`(<img src="img/${naam}\\.webp" alt=")[^"]*(")`), `$1${alt}$2`);
    console.log('KLAAR ', `img/${naam}.webp`);
    n++;
  }
  // de bronvermelding hoorde bij de oude stockfoto van de verhuislift
  if (lijst.some(l => l[0] === 'dienst-verhuislift') && fs.existsSync(path.join(IMG, 'dienst-verhuislift.webp')) && n)
    s = s.replace(/<figcaption class="dienst__bron">.*?<\/figcaption>/, '');
  if (n) fs.writeFileSync(html, s);
  console.log(`${n} van ${lijst.length} foto's klaargezet.`);
}

const args = process.argv.slice(2);
const filter = args.filter(a => !a.startsWith('--'));
const lijst = filter.length ? SCENES.filter(s => filter.some(f => s[0].includes(f))) : SCENES;

if (args.includes('--prompts')) {
  const tekst = lijst.map(([naam, scene]) =>
    `==================== ${naam}  (beeldverhouding 4:3) ====================
Upload eerst: refs/ref-logo.png
Sla het resultaat op als: _ai-beelden/foto/${naam}.png (of .jpg)

${MERK.trim()}

ASPECT RATIO: 4:3 landscape. Highest resolution available.

SCENE: ${scene}
`).join('\n\n');
  fs.writeFileSync(path.join(HIER, 'PROMPTS-diensten.txt'), tekst);
  console.log(`Geschreven: PROMPTS-diensten.txt (${lijst.length} prompts)`);
} else if (args.includes('--klaar')) {
  await klaar(lijst);
} else {
  if (!KEY) { console.error('Geen GEMINI_API_KEY gevonden (omgeving of ~/.gemini_api_key). Zonder key: node diensten-gen.mjs --prompts'); process.exit(1); }
  const TEGELIJK = 4;
  for (let i = 0; i < lijst.length; i += TEGELIJK) await Promise.all(lijst.slice(i, i + TEGELIJK).map(maak));
  await klaar(lijst);
}
