// Contact: echte klantenservice-medewerker van De Reus die over het contactformulier heen kijkt.
// Maakt 3 varianten op groen scherm (nano banana pro), knipt ze uit en zet ze als webp in foto/.
//   node contact-gen.mjs          genereren + uitknippen
//   node contact-gen.mjs knip     alleen opnieuw uitknippen
// Key uit GEMINI_API_KEY of ~/.gemini_api_key (nooit in de repo).
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const HIER = path.dirname(fileURLToPath(import.meta.url));
const UIT = path.join(HIER, 'foto');
fs.mkdirSync(UIT, { recursive: true });
const MODEL = 'gemini-3-pro-image-preview';
const URL = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`;

const PROMPT = `
The attached image is the real logo of Verhuisbedrijf De Reus (a moving company in The Hague): a yellow house (#FFCC33)
between two flexing royal-blue arms (#1746A2).

Photorealistic studio portrait of a friendly De Reus customer-service planner, a Dutch woman of about 30,
sitting at a desk and talking to a customer through a slim black office headset with a microphone boom.
She looks warmly into the camera, mid-sentence, natural relaxed smile, one hand lightly raised as if explaining.
She wears a royal-blue (#1746A2) polo shirt with ONLY the small yellow house-with-arms symbol embroidered on the left chest
(symbol only, no text on the shirt).
Framing: head and upper body, from the top of the head down to the desk edge; the top of a laptop screen seen from behind
is just visible at the bottom edge of the frame. Camera at eye level, 50 mm lens, soft even studio light,
realistic skin texture, anatomically correct hands (five fingers).
BACKGROUND: completely flat, even chroma-key green (#00FF00), no shadow, no desk lamp, no office, nothing else.
Leave some green margin above her head and at both sides. Not an illustration, not a 3D render, no text, no watermark.
`;

function sleutel() {
  const f = path.join(os.homedir(), '.gemini_api_key');
  return process.env.GEMINI_API_KEY || (fs.existsSync(f) ? fs.readFileSync(f, 'utf8').trim() : '');
}

async function maak(nr) {
  const KEY = sleutel();
  if (!KEY) { console.error('Geen GEMINI_API_KEY (omgeving of ~/.gemini_api_key).'); process.exit(1); }
  const body = {
    contents: [{ role: 'user', parts: [
      { inline_data: { mime_type: 'image/png', data: fs.readFileSync(path.join(HIER, 'refs', 'ref-logo.png')).toString('base64') } },
      { text: PROMPT },
    ] }],
    generationConfig: { responseModalities: ['IMAGE'], imageConfig: { aspectRatio: '4:5', imageSize: '2K' } },
  };
  for (let poging = 1; poging <= 3; poging++) {
    try {
      const r = await fetch(URL, { method: 'POST', headers: { 'Content-Type': 'application/json', 'x-goog-api-key': KEY }, body: JSON.stringify(body) });
      const j = await r.json();
      if (!r.ok) throw new Error(`${r.status} ${j.error?.message?.slice(0, 160)}`);
      const d = j.candidates?.[0]?.content?.parts?.find(p => p.inlineData || p.inline_data);
      if (!d) throw new Error('geen beeld: ' + (j.candidates?.[0]?.finishReason || 'onbekend'));
      const data = (d.inlineData || d.inline_data).data;
      fs.writeFileSync(path.join(UIT, `contact-planner-${nr}.png`), Buffer.from(data, 'base64'));
      console.log('OK   contact-planner-' + nr);
      return;
    } catch (e) {
      console.log(`FOUT ${nr} (poging ${poging}): ${e.message}`);
      await new Promise(r => setTimeout(r, 4000 * poging));
    }
  }
}

// groen scherm eruit, groene gloed van de randen af, bijsnijden en webp
async function knip(nr) {
  const bron = path.join(UIT, `contact-planner-${nr}.png`);
  if (!fs.existsSync(bron)) return;
  const { data, info } = await sharp(bron).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  for (let i = 0; i < data.length; i += 4) {
    const r = data[i], g = data[i + 1], b = data[i + 2];
    const groen = g - Math.max(r, b);
    if (groen > 70) data[i + 3] = 0;
    else if (groen > 20) { data[i + 3] = Math.round(255 * (1 - (groen - 20) / 50)); data[i + 1] = Math.max(r, b); }
    else if (groen > 0) data[i + 1] = Math.max(r, b) + Math.round(groen / 3);
  }
  await sharp(data, { raw: info }).trim({ threshold: 1 }).resize({ width: 900, withoutEnlargement: true })
    .webp({ quality: 86, alphaQuality: 90 }).toFile(path.join(UIT, `contact-planner-${nr}.webp`));
  console.log('KNIP contact-planner-' + nr);
}

const alleenKnip = process.argv[2] === 'knip';
if (!alleenKnip) await Promise.all([1, 2, 3].map(maak));
for (const nr of [1, 2, 3]) await knip(nr);
console.log('Klaar:', UIT);
