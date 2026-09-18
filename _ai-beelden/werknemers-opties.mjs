// Five unreviewed employee-at-work options, explicitly requested with Nano Banana Pro.
// Run: node _ai-beelden/werknemers-opties.mjs
// Credentials: GEMINI_API_KEY or a single key piped to stdin. Never saved or logged.
// This script saves the returned image bytes without opening or evaluating images.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUTPUT = path.join(ROOT, 'beeld-opties', 'werknemers-20260918');
const REFERENCE = 'brandbook/assets/logo-v2/dereus-logo.png';
const PRIMARY = 'gemini-3-pro-image';
const PREVIEW = 'gemini-3-pro-image-preview';
const CONCURRENCY = 2;
const MAX_ATTEMPTS = 3;
const COMMON = `Use case: photorealistic-natural.
Asset type: an original landscape website photograph for Verhuisbedrijf De Reus, a moving company in The Hague, Netherlands.
Input image 1: brand reference only, the existing De Reus logo; not an image to edit.
Subject: realistic fictional adult moving-company employees actively performing the described task. Natural concentration on their work and interaction with the objects; candid, unposed, no looking into the camera.
Brand and clothing: royal-blue (#1746A2) polo shirts with a small yellow (#FFCC33) De Reus house-and-arms emblem on the left chest, dark navy work trousers, black work shoes. Use the attached logo as the faithful brand reference. A varied, believable team of adults with different ages and backgrounds.
Style: photorealistic editorial photography, natural Dutch daylight, realistic skin pores, fabric folds, wood grain and everyday material textures; 35mm or 50mm lens, believable perspective, natural color balance.
Composition: one coherent landscape photograph, action clearly visible, hands naturally gripping the objects, useful surrounding context, subjects comfortably within the frame.
Constraints: original fictional people, plausible human anatomy and lifting posture, protect furniture and floors, realistic tools and materials. No collage, no before/after panels, no illustration or 3D render, no staged team portrait, no dramatic HDR or plastic skin, no text overlay, no visible watermark. No brands other than De Reus. Only the attached brand lettering where appropriate, no invented phone numbers or slogans.
Generate exactly one image.`;

const SCENES = [
  {
    id: '01-verhuiswagen-laden', title: 'Verhuiswagen laden', ratio: '16:9',
    scene: 'On a quiet brick street in The Hague, two De Reus movers actively load a white moving van through its open rear doors. One guides a hand truck with two securely stacked kraft moving boxes up a proper loading ramp, while the other steadies the load from inside the van. Show both workers in action, the hands, boxes and ramp clearly. Typical Dutch brick row houses, white window frames and a parked bicycle in the background. The visible van side carries the supplied De Reus logo. Soft overcast morning light, eye-level three-quarter view.'
  },
  {
    id: '02-bank-dragen', title: 'Samen een bank verhuizen', ratio: '3:2',
    scene: 'Two De Reus movers actively carry a compact grey sofa protected with thick blue moving blankets through the open front doorway of a Dutch brick townhouse. Each mover grips one end firmly with both hands, working together, faces focused on the passage. The sofa and both workers fit in the frame. A protective runner covers the threshold and wooden hallway floor. A white De Reus van is softly visible outside. Candid eye-level view from the hallway, soft natural daylight.'
  },
  {
    id: '03-zorgvuldig-inpakken', title: 'Breekbare spullen inpakken', ratio: '3:2',
    scene: 'In a bright lived-in Dutch living room, a De Reus employee is actively wrapping a ceramic vase in packing paper at a sturdy table while a second colleague carefully places already wrapped items into a compartmented moving box. Capture hands doing the work and the employees upper bodies, with natural focused expressions. Kraft boxes, reusable protective blankets and a simple tape dispenser, neatly arranged. Tall white-framed windows, soft side light, warm realistic domestic textures, medium-wide candid photograph.'
  },
  {
    id: '04-meubels-monteren', title: 'Meubels monteren', ratio: '3:2',
    scene: 'Inside a bright Dutch bedroom after a move, two De Reus employees actively assemble a wooden bed frame. One kneels on a protective floor mat and tightens a corner bracket with a cordless driver, while the second steadies the side rail in correct alignment. The action, practical tools and both people are visible in one coherent frame. A few neatly stacked moving boxes near the wall, soft window light, realistic joinery and proportions. Photograph at a slightly low eye-level angle, candid and skilled.'
  },
  {
    id: '05-kantoor-verhuizen', title: 'Kantoorverhuizing', ratio: '16:9',
    scene: 'A working team of three De Reus movers in a modern Dutch office during an organized office move. In the foreground one actively pushes a stable wheeled trolley of closed reusable moving crates along a clear aisle; a second carefully wraps a detached monitor in a padded protective sleeve at a desk; a third carries a compact desk chair toward the exit. Show realistic active movement without motion blur obscuring faces or hands. Glass partitions, daylight through large windows, neutral desks and clear protected walkways. Natural documentary business photography.'
  }
].map(scene => ({ ...scene, prompt: `${COMMON}\nScene/backdrop and action: ${scene.scene}` }));

class SafeError extends Error {}
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
const escapeHtml = value => String(value).replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[ch]);

async function readKey() {
  if (process.env.GEMINI_API_KEY?.trim()) return process.env.GEMINI_API_KEY.trim();
  if (process.stdin.isTTY) throw new SafeError('Set GEMINI_API_KEY or pipe the key to stdin.');
  let key = '';
  process.stdin.setEncoding('utf8');
  for await (const chunk of process.stdin) key += chunk;
  if (!key.trim()) throw new SafeError('No Gemini API key supplied.');
  return key.trim();
}

function gallery(manifest) {
  const items = manifest.scenes.map(scene => `<section><h2>${escapeHtml(scene.title)}</h2>${scene.files.length ? scene.files.map(file => `<a href="${encodeURIComponent(file)}"><img src="${encodeURIComponent(file)}" alt="${escapeHtml(scene.title)}" loading="lazy"></a><p><a href="${encodeURIComponent(file)}" download>Download ${escapeHtml(file)}</a></p>`).join('') : `<p>${scene.status === 'failed' ? 'Genereren is niet gelukt.' : 'Nog niet gegenereerd.'}</p>`}</section>`).join('\n');
  return `<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>De Reus: vijf beeldopties</title><style>body{margin:0;padding:32px;background:#f5f6f8;color:#10254b;font:16px/1.6 system-ui}main{max-width:1200px;margin:auto}h1{line-height:1.15}article{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:24px}section{background:white;border-radius:16px;padding:20px}h2{margin-top:0;font-size:22px}img{display:block;width:100%;height:auto;border-radius:8px}a{color:#1746a2}footer{margin-top:32px}</style><main><h1>De Reus aan het werk</h1><p>Vijf AI-beeldopties met fictieve medewerkers. De beelden zijn onbewerkt en niet visueel beoordeeld. Kies zelf welke je wilt gebruiken.</p><article>${items}</article><footer><a href="prompts-manifest.json" download>Download prompts en bestandslijst</a></footer></main></html>`;
}

async function main() {
  // A fresh directory prevents accidental overwrite or paid regeneration of previous results.
  if (fs.existsSync(OUTPUT)) throw new SafeError('Output folder already exists; nothing overwritten or generated.');
  const key = await readKey();
  const logo = fs.readFileSync(path.join(ROOT, REFERENCE)).toString('base64');
  fs.mkdirSync(OUTPUT, { recursive: true });
  const manifest = {
    createdAt: new Date().toISOString(), provider: 'Google Gemini API', requestedModel: PRIMARY,
    fallbackModel: PREVIEW, imageSize: '2K', brandReference: REFERENCE,
    outputInspection: 'Not opened, inspected, filtered or visually evaluated; user selects.',
    scenes: SCENES.map(({ id, title, ratio, prompt }) => ({ id, title, aspectRatio: ratio, prompt, status: 'pending', files: [], attempts: [] }))
  };
  function saveManifest() {
    fs.writeFileSync(path.join(OUTPUT, 'prompts-manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
    fs.writeFileSync(path.join(OUTPUT, 'index.html'), gallery(manifest));
  }
  saveManifest();

  async function generate(scene) {
    let model = PRIMARY;
    let attempts = 0;
    const body = JSON.stringify({
      contents: [{ role: 'user', parts: [
        { inlineData: { mimeType: 'image/png', data: logo } },
        { text: scene.prompt }
      ] }],
      generationConfig: { candidateCount: 1, responseModalities: ['IMAGE'], imageConfig: { aspectRatio: scene.aspectRatio, imageSize: '2K' } }
    });
    while (true) {
      attempts++;
      let response;
      try {
        response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`, {
          method: 'POST', headers: { 'Content-Type': 'application/json', 'x-goog-api-key': key },
          body, signal: AbortSignal.timeout(600000)
        });
      } catch {
        // A transport failure may have reached the provider, so never retry it blindly.
        throw new SafeError('Transport failure or timeout; not retried.');
      }
      scene.attempts.push({ model, httpStatus: response.status });
      saveManifest();
      if (!response.ok) {
        await response.body?.cancel();
        if (response.status === 404 && model === PRIMARY) {
          model = PREVIEW;
          attempts = 0;
          console.log(`${scene.id}: primary model unavailable; trying same-family Pro preview.`);
          continue;
        }
        if ((response.status === 429 || response.status >= 500) && attempts < MAX_ATTEMPTS) {
          const seconds = Number(response.headers.get('retry-after'));
          const delay = Math.min(30000, Math.max(4000 * attempts, Number.isFinite(seconds) ? seconds * 1000 : 0));
          console.log(`${scene.id}: HTTP ${response.status}; retry ${attempts + 1}/${MAX_ATTEMPTS}.`);
          await sleep(delay);
          continue;
        }
        throw new SafeError(`HTTP ${response.status}; no further retry.`);
      }
      let payload;
      try { payload = await response.json(); }
      catch { throw new SafeError('Response was not valid JSON; not retried.'); }
      // Extract only transport data. No image decoding, display, analysis or selection.
      const images = (payload.candidates ?? []).flatMap(candidate => candidate.content?.parts ?? [])
        .map(part => part.inlineData ?? part.inline_data)
        .filter(part => part?.data && (part.mimeType ?? part.mime_type ?? '').startsWith('image/'));
      if (!images.length) throw new SafeError('No image data returned; not retried.');
      for (const [index, image] of images.entries()) {
        const mime = image.mimeType ?? image.mime_type;
        const extension = ({ 'image/png': 'png', 'image/jpeg': 'jpg', 'image/webp': 'webp', 'image/gif': 'gif' })[mime] ?? 'img';
        const file = `${scene.id}${index ? `-${index + 1}` : ''}.${extension}`;
        fs.writeFileSync(path.join(OUTPUT, file), Buffer.from(image.data, 'base64'), { flag: 'wx' });
        scene.files.push(file);
      }
      scene.status = 'generated';
      scene.model = model;
      saveManifest();
      console.log(`${scene.id}: saved ${scene.files.length} returned image(s), not inspected.`);
      return;
    }
  }

  let cursor = 0;
  async function worker() {
    while (cursor < manifest.scenes.length) {
      const scene = manifest.scenes[cursor++];
      scene.status = 'generating';
      saveManifest();
      try { await generate(scene); }
      catch (error) {
        scene.status = 'failed';
        scene.error = error instanceof SafeError ? error.message : 'Local save or processing failed; no retry.';
        saveManifest();
        console.error(`${scene.id}: ${scene.error}`);
      }
    }
  }
  await Promise.all(Array.from({ length: CONCURRENCY }, worker));
  const completed = manifest.scenes.filter(scene => scene.status === 'generated').length;
  manifest.completedAt = new Date().toISOString();
  manifest.completedScenes = completed;
  saveManifest();
  console.log(`Saved ${completed}/5 scenes. Gallery: ${path.relative(ROOT, path.join(OUTPUT, 'index.html'))}`);
  if (completed !== 5) process.exitCode = 1;
}

main().catch(error => {
  console.error(error instanceof SafeError ? error.message : 'Local setup failed. No credentials or provider response logged.');
  process.exitCode = 1;
});
