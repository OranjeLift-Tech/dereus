// De gedeelde kern onder elke beeldronde: sleutel, model, aanroep met herkansing, en de twee
// vaste regels die anders elke ronde opnieuw bedacht worden.
//
// Waarom dit bestand bestaat: er stonden vierentwintig losse *-gen.mjs naast elkaar die allemaal
// dezelfde vijftien regels herhaalden (sleutel uit ~/.gemini_api_key, de modelnaam, de fetch met
// drie pogingen, het uitpakken van inlineData). Eén modelnaam wijzigen was vierentwintig keer
// zoeken en vervangen. Hier staat het één keer.
//
// Wat hier NIET in hoort: de scenes van een ronde. Die horen bij de ronde zelf.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import sharp from 'sharp';

export const MODEL = 'gemini-3-pro-image-preview';           // nano banana pro
export const URL = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`;

// De gezichtenbank van de foto-verbeteren-skill. Lees daar eerst GEZICHTEN.md: de gezichten zijn
// een schaarse voorraad die tussen parallelle rondes gedeeld wordt.
export const GEZICHTEN = path.join(os.homedir(), '.claude', 'skills', 'foto-verbeteren', 'assets', 'gezichten');

// ---------------------------------------------------------------------------
// Sleutel. Nooit in de repo, nooit printen.
// ---------------------------------------------------------------------------
export function sleutel() {
  const f = path.join(os.homedir(), '.gemini_api_key');
  return process.env.GEMINI_API_KEY || (fs.existsSync(f) ? fs.readFileSync(f, 'utf8').trim() : '');
}

export function eisSleutel() {
  const k = sleutel();
  if (!k) {
    console.error('Geen GEMINI_API_KEY gevonden (omgeving of ~/.gemini_api_key).');
    process.exit(1);
  }
  return k;
}

// ---------------------------------------------------------------------------
// REGEL 1: het merk gaat nooit in het prompt.
// ---------------------------------------------------------------------------
// Het model tekent een logo na in plaats van het te plaatsen. Elke ronde die om een borstteken
// vroeg kreeg een vervormd huisje met een onleesbaar regeltje eronder terug, ook als het prompt
// letterlijk "symbol only, NO text" zei. Vragen om een kleiner huisje helpt niet; de borst
// helemaal leeg vragen wel. Het echte beeldmerk komt er naderhand met sharp op.
// Zie gereedschap/merk-op-doos.py voor de dozen en _werk/export-teambeeld.cjs voor kleding.
export const MERK = `BRAND RULES (a moving company in The Hague, the Netherlands):
- CLOTHING: the movers wear a royal-blue (#1746A2) polo shirt, navy work trousers and black safety shoes.
  Neat, clean, well-fitting. The polo is COMPLETELY PLAIN royal blue: no symbol, no house, no logo, no emblem,
  no embroidery, no print, no badge and no lettering on the chest, the sleeves or the back. Plain blue fabric only.
- BOXES: plain brown kraft cardboard moving boxes, completely blank, no printing of any kind.
- VAN OR TRUCK: only far away and out of focus, or outside the frame. Never a readable side panel.
- PEOPLE: an honest, diverse mix of Dutch people, different ages and builds. Natural, friendly, confident,
  not posed stock smiles. Real working men and women with wear and tear, not models.
- SETTING: recognisably The Hague / the Netherlands: brick row houses, white window frames, bicycles, trees,
  brick streets. Realistic Dutch weather: bright, soft daylight, light clouds; not overly sunny.
- STYLE: photorealistic editorial photography, full-frame camera, natural colours, shallow depth of field
  where it fits. NOT illustration, NOT 3D render, NOT HDR, no text overlays.
- natural skin texture, visible pores, uneven skin tone, no retouching.
- HANDS: each hand has exactly four fingers and one thumb. Do not add extra fingers. Every visible fingertip
  must belong to a hand that is itself visible in the frame. Grip consistent with the object's weight.
- ABSOLUTELY NO TEXT: no letters, no numbers, no house numbers, no number plates (leave the plate surface
  blank or out of frame), no street signs, no doorbell labels, no shop signs, no printing or handwriting on
  boxes or tape, no watermark anywhere in the image.`;

export const STIJL = (ratio) => `Photorealistic editorial photograph, aspect ratio ${ratio}, full-frame camera,
natural colours, realistic depth of field. An original scene with original people, not a real recognisable individual.`;

// De personenregel hoort bij het aantal referentiegezichten dat meegaat.
export function personenRegel(aantal) {
  const letters = ['FIRST', 'SECOND', 'THIRD', 'FOURTH', 'FIFTH'];
  const namen = ['A', 'B', 'C', 'D', 'E'];
  const regels = [];
  for (let i = 0; i < aantal; i++) {
    regels.push(`Person ${namen[i]}: use the ${letters[i]} attached reference photo for face identity, age, skin` +
      ` and expression only; ignore its clothing, helmet and background.`);
  }
  if (aantal > 1) regels.push('The people must look clearly like different individuals.');
  return regels.join('\n');
}

// ---------------------------------------------------------------------------
// REGEL 2: alle versies van één ronde krijgen dezelfde cast.
// ---------------------------------------------------------------------------
// Er overleeft er maar één. Wisselen de gezichten per versie, dan kiest de gebruiker tussen
// verschillende mensen in plaats van tussen verschillende composities, en dan zegt de keuze niets
// over het beeld. De cast wordt daarom één keer per ronde geladen en aan elke versie meegegeven.
//
// De uitsneden in de bank zijn klein (65 tot 430 px). Op wit en naar 512 op de langste zijde,
// zodat het model het gezicht scherp genoeg ziet. Verder niets aan veranderd.
export async function gezichtRef(rel, maat = 512) {
  const bron = path.isAbsolute(rel) ? rel : path.join(GEZICHTEN, rel);
  if (!fs.existsSync(bron)) throw new Error(`referentiegezicht ontbreekt: ${bron}`);
  const m = await sharp(bron).metadata();
  const schaal = maat / Math.max(m.width, m.height);
  const buf = await sharp(bron).flatten({ background: '#ffffff' })
    .resize({ width: Math.round(m.width * schaal), height: Math.round(m.height * schaal), kernel: 'lanczos3' })
    .png().toBuffer();
  return buf.toString('base64');
}

/** Laadt de cast één keer. Geef de lijst bestandsnamen uit de gezichtenbank. */
export async function laadCast(namen) {
  return Promise.all(namen.map((n) => gezichtRef(n)));
}

// ---------------------------------------------------------------------------
// De aanroep, met herkansing bij een tijdelijke fout.
// ---------------------------------------------------------------------------
const TIJDELIJK = [429, 500, 502, 503, 504];

/**
 * Genereert één beeld en schrijft het naar `doel`.
 * cast: lijst base64-png's die vóór het prompt meegaan (de referentiegezichten).
 * Geeft {ok, naam, breedte, hoogte, pogingen} of {ok:false, naam, fout}.
 */
export async function genereer({ naam, prompt, cast = [], ratio = '3:2', grootte = '2K', doel, pogingen = 3 }) {
  const KEY = eisSleutel();
  const parts = [
    ...cast.map((data) => ({ inline_data: { mime_type: 'image/png', data } })),
    { text: prompt },
  ];
  const body = {
    contents: [{ role: 'user', parts }],
    generationConfig: { responseModalities: ['IMAGE'], imageConfig: { aspectRatio: ratio, imageSize: grootte } },
  };
  let laatste = '';
  for (let poging = 1; poging <= pogingen; poging++) {
    try {
      const r = await fetch(URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-goog-api-key': KEY },
        body: JSON.stringify(body),
      });
      const j = await r.json();
      if (!r.ok) {
        const e = new Error(`${r.status} ${j.error?.message?.slice(0, 160) || ''}`);
        e.status = r.status;
        throw e;
      }
      const deel = j.candidates?.[0]?.content?.parts?.find((p) => p.inlineData || p.inline_data);
      if (!deel) throw new Error('geen beeld in antwoord: ' + (j.candidates?.[0]?.finishReason || 'onbekend'));
      const d = deel.inlineData || deel.inline_data;
      fs.mkdirSync(path.dirname(doel), { recursive: true });
      fs.writeFileSync(doel, Buffer.from(d.data, 'base64'));
      const m = await sharp(doel).metadata();
      console.log(`OK   ${naam} ${m.width}x${m.height}${poging > 1 ? ` (poging ${poging})` : ''}`);
      return { ok: true, naam, breedte: m.width, hoogte: m.height, pogingen: poging };
    } catch (e) {
      laatste = e.message;
      const nogmaals = poging < pogingen && (e.status === undefined || TIJDELIJK.includes(e.status));
      console.log(`FOUT ${naam} (poging ${poging}): ${e.message}${nogmaals ? '' : ' — opgegeven'}`);
      if (!nogmaals) break;
      await new Promise((r) => setTimeout(r, 4000 * poging));     // 4s, 8s
    }
  }
  return { ok: false, naam, fout: laatste };
}

// ---------------------------------------------------------------------------
// Parallel, met een dak erop.
// ---------------------------------------------------------------------------
// Vijf beelden achter elkaar is vijf keer de wachttijd van één; tegelijk is ongeveer de wachttijd
// van de traagste. Het dak staat er omdat de API bij te veel tegelijk 429 teruggeeft, en dan ben je
// met herkansingen alsnog langer bezig.
export const TEGELIJK = 5;

export async function parallel(lijst, fn, tegelijk = TEGELIJK) {
  const uit = [];
  for (let i = 0; i < lijst.length; i += tegelijk) {
    uit.push(...await Promise.all(lijst.slice(i, i + tegelijk).map(fn)));
  }
  return uit;
}
