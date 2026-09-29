// De collega met headset (img/contact-uit.webp) in het De Reus-uniform: alleen haar kleding wordt een effen
// Koningsblauwe polo. Gezicht, haar, headset, houding en uitsnede blijven. Het merk staat NIET in het prompt
// (zie ../LEESMIJ.md: een model tekent het logo na); het echte beeldmerk komt er daarna op met merk.js.
// node gen.mjs  ->  kandidaat-1.png, kandidaat-2.png in deze map. Sleutel uit OPENAI_API_KEY, nooit printen.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HIER = path.dirname(fileURLToPath(import.meta.url));
const BRON = path.resolve(HIER, '../../img/contact-uit.webp');
const SLEUTEL = process.env.OPENAI_API_KEY;
if (!SLEUTEL) throw new Error('OPENAI_API_KEY ontbreekt');

const PROMPT = [
  'Edit this photo. Replace only her clothing: she now wears a plain royal blue (#1746A2) short-sleeved polo shirt',
  'with a soft collar and a short three-button placket, the staff uniform of a Dutch moving company.',
  'The shirt is completely plain: no logo, no text, no print, no pattern, no badge.',
  'Keep her face, expression, eyes, smile, skin, hair, headset, microphone and cable exactly the same.',
  'Keep the same pose, framing, crop, camera angle and soft studio lighting. Keep the background fully transparent.',
  'Photorealistic, natural cotton fabric with subtle folds.',
].join(' ');

const form = new FormData();
form.append('model', 'gpt-image-1');
form.append('image', new Blob([fs.readFileSync(BRON)], { type: 'image/webp' }), 'contact-uit.webp');
form.append('prompt', PROMPT);
form.append('size', '1536x1024');
form.append('quality', 'high');
form.append('background', 'transparent');
form.append('output_format', 'png');
form.append('input_fidelity', 'high');
form.append('n', '2');

const t0 = Date.now();
const r = await fetch('https://api.openai.com/v1/images/edits', {
  method: 'POST', headers: { Authorization: `Bearer ${SLEUTEL}` }, body: form,
});
const j = await r.json();
if (!r.ok) { console.error('fout', r.status, JSON.stringify(j.error || j).slice(0, 600)); process.exit(1); }
j.data.forEach((d, i) => {
  const uit = path.join(HIER, `kandidaat-${i + 1}.png`);
  fs.writeFileSync(uit, Buffer.from(d.b64_json, 'base64'));
  console.log('geschreven', path.basename(uit));
});
console.log('klaar in', Math.round((Date.now() - t0) / 1000), 's');
