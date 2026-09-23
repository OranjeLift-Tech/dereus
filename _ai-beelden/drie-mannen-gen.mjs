// Vijf nieuwe versies "drie verhuizers dicht bij elkaar, één met een doos", na de afkeuring van
// twee volle rondes ("dont like any ... change the photo skill to not lean heavily into the
// photos too much. also only use guys for the worker photos").
//
//   node drie-mannen-gen.mjs                 alle vijf, gelijktijdig
//   node drie-mannen-gen.mjs versie-2        alleen die versie
//
// Drie dingen anders dan drie-doos-gen.mjs, alle drie naar aanleiding van de afkeuring:
// 1. ER GAAN GEEN REFERENTIEBEELDEN MEE. Geen inline_data, alleen tekst. De vorige twee rondes
//    stuurden drie uitsnedes mee en leverden tien beelden met dezelfde drie koppen op; dat is
//    precies waar "not lean heavily into the photos" over gaat. De mannen staan nu in woorden
//    beschreven, losjes geleend van man-14, man-11 en man-15 uit de pool. Gevolg met opzet: de
//    gezichten verschillen tussen de vijf versies. Wat vergeleken wordt is hoe echt ze ogen.
// 2. ALLEEN MANNEN. Geen vrouw in de ploeg.
// 3. De vijf versies verschillen in ECHTHEID, niet alleen in camerastandpunt: de blik, de huid,
//    de lijven, de sleet op de kleren en het licht. De compositie varieert mee, maar dat is hier
//    de bijzaak. Wat afgekeurd werd waren de mensen.
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
const UIT = path.join(HIER, '..', 'website', 'review', 'drie-verhuizers-mannen-20260922');
fs.mkdirSync(UIT, { recursive: true });

// ---- vaste afspraken ---------------------------------------------------------------------------
const MERK = `
BRAND AND SCENE RULES (De Reus, a moving company in The Hague, the Netherlands):
- NO LOGOS AND NO TEXT ANYWHERE IN THE IMAGE. This is essential. The movers wear PLAIN royal-blue
  (#1746A2) polo shirts with NOTHING printed or embroidered on them: no symbol, no logo, no text,
  clean empty fabric on chest, back and sleeves. Navy work trousers, black safety shoes.
- The van or box truck in frame is PLAIN WHITE with no lettering, no logo, no phone number, no
  livery of any kind. Moving boxes are plain brown kraft with NOTHING printed on them.
- No signage, no house numbers, no street names, no number plates, no brand names anywhere, and
  no manufacturer emblems on the van, the wheels or the grille. If any surface would normally
  carry text or a badge, leave it blank.
- This includes SMALL objects, which is where invented branding creeps in: work gloves carry NO
  brand mark, NO coloured lettering, NO logo patch and no printed cuff. Tape rolls are blank, no
  labels, no stickers, no product markings on tools. No lettering on tattoos.
- SETTING: recognisably The Hague: brick row houses, white window frames, bicycles, trees, brick
  pavement. Realistic Dutch daylight, bright but softly overcast, not sunny.
- STYLE: photorealistic documentary reportage shot on a full-frame camera, 35 mm or 50 mm lens,
  natural colours. NOT illustration, NOT 3D render, NOT HDR, no text overlays, no watermark.
- THE THREE STAY CLOSE TOGETHER: all three within roughly one metre of each other, busy with the
  same single task, bodies overlapping in the frame. Never spread across the width of the picture.
`;

// Dit blok is de kern van deze ronde. De vorige twee rondes zijn afgekeurd op de mensen, niet op
// de beelden eromheen: gladde huid, geposeerde glimlach in de lens, vlak portretlicht, splinter-
// nieuwe kleren en drie keer hetzelfde postuur.
const ECHT = `
THESE MUST NOT LOOK LIKE STOCK PHOTO MODELS. This is the most important part of the brief. Two
earlier rounds were rejected because the people looked artificial. Specifically:
- SKIN: visible pores, uneven tone, patches of redness on the nose, ears and cheeks, shaving rash
  on the neck, a mole or two, a small scar, chapped lips, sun-weathered forearms and neck against
  paler skin under the sleeve. NO retouching, NO beauty filter, NO airbrushed or waxy skin, no
  uniform sheen across forehead and cheekbones. Stubble grows unevenly; grey hair is not uniform.
- EXPRESSION AND GAZE: they are working, not posing. NOT ONE OF THE THREE LOOKS INTO THE LENS, in
  any version. No held smiles, no stock-photo cheerfulness, no team-photo line-up. Faces are
  neutral or concentrating, mouths closed or caught mid-sentence, eyes on the box, on the job or
  on each other, or past the camera at something out of frame. Half-turned and partly hidden faces
  are good. Every man is caught between two moments rather than presented.
- ARRANGEMENT: NEVER a row of three men standing side by side square to the camera. That reads as
  a team photo and it is the single thing most often wrong with these pictures. Break the line:
  put them at different distances from the camera, one nearer and one further back, one in profile
  or three-quarter, one partly behind another, one crouching or bent over the work while the others
  stand. They stay within a metre of each other, but the group sits on a diagonal, not on a line
  parallel to the lens.
- BODIES: three plainly different, ordinary men, not three fit models of the same build. Different
  heights, different weights, different postures: one is heavy through the middle with a belly
  pushing the polo, one is thin and wiry, one is broad through the shoulders and stands with his
  weight on one leg. Slouching, thick necks, sloping shoulders and receding hair are all welcome.
- CLOTHES: workwear that has been worn all day. Creases at the elbow and the small of the back,
  the hem untucked on one man, a sweat patch between the shoulder blades or under the arms, dust
  and brick grit on the trouser legs and knees, scuffed shoes. The polos do not all fit the same:
  one is a size too big, one pulls tight across the chest. Nothing looks new or pressed.
- HANDS AND EFFORT: working hands, with short dirty nails, calluses, a scraped knuckle, tendons
  and knuckles standing out under the weight. Where a man carries, the weight shows: forearms
  tight, shoulders pulled down, the body leaning against the load.
- LIGHT: daylight with a DIRECTION, not flat portrait light. Real shadow under the brows, the
  nose and the chin, one side of each face darker than the other, the shadows falling the same
  way on all three because they stand in the same light.
`;

const DOOS = `
THE BOX (this must survive every other instruction):
- Exactly ONE of the three carries a single plain cardboard moving box. The other two do not carry
  a box; they are busy with the same job.
- The box is ordinary brown corrugated kraft cardboard, completely unprinted and unmarked: no
  logo, no text, no stamp, no barcode, no stickers, no handwriting, no shipping label, no coloured
  tape, no printed arrows or symbols. Blank on every visible side.
- ONE LARGE FACE OF THE BOX IS TURNED SQUARELY TOWARDS THE CAMERA and is fully visible: flat, not
  tilted away, not foreshortened, not cropped by the edge of the frame. That face is clean, evenly
  lit, free of deep shadow and free of glare, and it stays SHARP even if something else in the
  frame is caught in motion.
- Nothing crosses that face: no hand, no fingers, no forearm, no strap, no tape seam, no other
  object in front of it. The carrying hands grip the box at the bottom edge and the far side only.
- The box is held roughly between waist and chest height and is a decent size in the picture.
- The cardboard looks used but sound: slight scuffs and soft corners, no crushed or torn panels.
`;

// ---- vijf verschillende ploegen, in woorden ----------------------------------------------------
// Geen uitsnedes, geen identiteit om na te maken: leeftijd, bouw, haar en type, meer niet. Losjes
// geleend van de pool (man-11 t/m man-15 en man-19), maar nooit de bezetting van de afgekeurde
// ronde (man-07, man-10 en vrouw-03).
//
// Elke versie krijgt een ANDERE ploeg. De zwaarste klacht was dat er tien beelden met dezelfde
// drie koppen langskwamen; vijf keer dezelfde drie nette verhuizers zou diezelfde fout zijn in
// een nieuw jasje. Per ploeg drie duidelijk verschillende lijven, en over de vijf ploegen heen
// verschillende leeftijden, postuur, haar en gezichtsvorm.
const KOP = 'THE THREE MEN in this picture (all men, no women in this crew; three plainly different ordinary Dutch workers, none of them stock-photo handsome):';
const STAART = `They must read as three separate men: not the same face, build or haircut three times, and not
the same crew as in any other picture. Ordinary bodies and ordinary faces, the kind you actually
see doing this work.`;

const PLOEGEN = {
  'versie-1': `
- THE OLDEST, about 58: grey hair thinning at the crown, plain metal-framed glasses, clean-shaven
  with grey stubble coming through, heavy through the middle with a belly pushing out the polo,
  red-cheeked, thick forearms, a wedding ring.
- THE MIDDLE ONE, about 38: dark brown hair cut short, three days of stubble, a nose broken once,
  broad through the shoulders and chest, a plain dark tattoo with no lettering on one forearm.
- THE YOUNGEST, about 24: dirty-blond hair, thin and wiry with narrow shoulders, a prominent
  Adam's apple, faint acne scarring on one cheek, patchy stubble that has not filled in.`,

  'versie-2': `
- A MAN OF ABOUT 45: head shaved down to stubble, very thick neck, heavy-set and barrel-chested,
  a flushed face that goes red with effort, small deep-set eyes, heavy jaw.
- A MAN OF ABOUT 30: red hair, heavily freckled pale skin that burns rather than tans, tall and
  thin with bony wrists, sunburn across the back of the neck and the forearms.
- A MAN OF ABOUT 60: lean and weathered, deep vertical lines in the cheeks, a grey moustache,
  hollow temples, sinewy arms, missing a little hair at the front.`,

  'versie-3': `
- A MAN OF ABOUT 27: already stocky with a soft belly, round face, cropped dark hair, thick
  eyebrows that nearly meet, short neck, a small silver stud in one ear.
- A MAN OF ABOUT 52: tall and bony, long face, grey hair combed straight back off a high forehead,
  reading glasses pushed up on his head, a stoop from years of carrying.
- A MAN OF ABOUT 35: average build running to soft, a receding hairline at the temples, ears that
  stick out, a heavy five o'clock shadow, dark circles under the eyes.`,

  'versie-4': `
- A MAN OF ABOUT 40: bald on top with close-cropped hair at the sides, short and very broad, a
  thick moustache, sweat shining on the scalp, forearms like hams.
- A MAN OF ABOUT 29, Dutch-Moroccan, born and raised in The Hague: thick black hair, heavy black
  eyebrows that nearly meet, a short dark beard with a sharp shaving line down the neck, medium
  build and slightly soft, and skin with real texture at this size: large visible pores across the
  nose and cheeks, old acne scarring along the jaw, an uneven tone. He is the one thing this
  picture must not get wrong: his face is NOT smooth, NOT symmetrical and NOT turned to the lens.
- A MAN OF ABOUT 55: grey crew cut, barrel-chested and thickening at the waist, a bulbous nose
  with broken veins across it, a heavy brow, deep crow's feet.`,

  'versie-5': `
- A MAN OF ABOUT 33: very tall and thin, a long narrow face, straight dark hair falling over the
  forehead, a sharp jaw and sunken cheeks, hunched shoulders from stooping through doorways.
- A MAN OF ABOUT 48: short and thickset, grey stubble over a round head, glasses on a cord round
  his neck, a gut, short arms, a permanent squint.
- A MAN IN HIS EARLY TWENTIES: round-cheeked and heavy rather than fit, sandy hair shaved at the
  sides, still boyish in the face, soft chin, ears red from the cold.`,
};

// ---- vijf versies: de echtheidsknop, niet het camerastandpunt ---------------------------------
const VERSIES = [
  ['versie-1', 'Niemand kijkt in de lens',
   'NOT ONE OF THE THREE LOOKS AT THE CAMERA. Caught mid-job at the open rear of a plain white van: the youngest carries the box out towards the pavement, the middle one is half-turned saying something to him with his mouth open mid-word, the oldest is looking down into the van with a hand on the door frame. Eye level, 35 mm, three-quarter bodies, the three overlapping in the centre of the frame. It should look like a frame grabbed from a working afternoon, not a picture anybody posed for.'],

  ['versie-2', 'Huid van dichtbij, licht met richting',
   'CLOSE FRAMING, chest up, so the skin is the subject, but NOT a portrait and NOT a row: the oldest of the three is carrying the box past the camera from right to left, caught mid-stride and seen in three-quarter view with his face turned down towards the load; the second man walks a step behind him in profile with a hand out to steady the box; the third is further back and half hidden behind the first man\'s shoulder, looking back over his own shoulder at the van. Daylight comes clearly from one side: one half of every face is in shadow, the other catches the light, with real shadow under the brows, the nose and the chin. At this distance you can see pores, uneven colour, redness across the nose and ears, shaving rash on the neck, a sheen of sweat and smeared glasses. No eye contact with the camera by anyone, no smiles. CRITICAL AT THIS FRAMING, because the chests fill much of the picture. Two things must both be true of every polo. FIRST, it carries no mark: no print, no embroidery, no badge, no breast pocket logo, nothing but bare blue jersey, the placket and the buttons. SECOND, it has had a full day of work in it and must NOT look factory-new: the fabric is limp and creased across the belly and at the elbows, dark with sweat at the chest, under the arms and down the back with pale salt rings drying at the edges, a smear of grey dust where a box has rubbed, the collar curling and one hem pulled out of the trousers. Wet foreheads above crisp shirts is exactly the contradiction that reads as fake. Their hands and forearms are dirty with it too: grime in the creases of the knuckles, grey dust up the forearms, nails short and dark at the edge. Keep the van cropped or turned so that no grille, bonnet or wheel centre is visible in the frame.'],

  ['versie-3', 'Drie alledaagse lijven',
   'FULL BODIES, head to shoes, on the brick pavement in front of brick row houses with the plain white van behind, arranged ON A DIAGONAL running away from the camera, NOT in a line. Nearest the camera and turned three-quarters away, one man is bent over a stack of plain boxes with his back rounded and his shirt riding up; a second stands a pace beyond him in profile holding the box against his chest and looking down the street; the third is furthest back at the van door, half turned away, reaching in. The point of this frame is that they are three ORDINARY, PHYSICALLY DIFFERENT men: one short and heavy with his belly pushing out the polo and the hem untucked, one a head taller and bony, one soft and average with a receding hairline. They stand the way tired men actually stand, weight on one leg, shoulders not square. Slightly low camera at hip height. Nobody looks at the camera and nobody poses.'],

  ['versie-4', 'Halverwege de dag, alles versleten',
   'HALFWAY THROUGH A LONG JOB and it shows on everything. Medium framing from the thighs up, the three crowded together at the tail of a plain white box truck, but at three different depths and NOT in a row: the balding man with the moustache sits on the edge of the tail lift with his forearms on his knees and his head down, seen from the side; the bearded man of 29 stands beyond him holding the box, three-quarters turned away with his face angled down towards the load, eyes on the box and never towards the lens; the grey-haired man leans against the open door in the near foreground, partly cut by the edge of the frame, drinking from a plain unmarked bottle with his eyes closed. Their polos are creased and dark with sweat between the shoulder blades and under the arms, the trouser knees are grey with brick dust, hands are dirty with black smudges and short broken nails. Tired faces, flushed skin, wet hair at the temples, no grimacing and no pulled faces. Eye level, overcast daylight with direction. Nobody looks at the camera.'],

  ['versie-5', 'Een kiekje, niet een foto',
   'THIS SHOULD LOOK LIKE A SNAPSHOT SOMEBODY TOOK, not a commissioned photograph. Slightly off-centre framing with the group not perfectly placed, the horizon a degree or two off level, the exposure a touch uneven so the sky is a little blown out behind them. The three walk close together along the brick pavement; the OLDEST carries the box, the other two flank him mid-stride, one with a folded blue moving blanket under his arm. One man is caught between expressions and the middle one is half blinking; a swinging hand shows a trace of motion blur. THE BOX ITSELF STAYS SHARP AND SQUARE TO THE CAMERA. Nobody is looking at the lens. 35 mm, eye level, ordinary daylight.'],
];

async function maak([naam, titel, beschrijving]) {
  const ploeg = `\n${KOP}${PLOEGEN[naam]}\n${STAART}\n`;
  const tekst = `${MERK}${ploeg}${ECHT}${DOOS}
SCENE: ${beschrijving}`;

  const body = {
    contents: [{ role: 'user', parts: [{ text: tekst }] }],
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
const gedaan = await Promise.all(lijst.map(maak));

const jsonPad = path.join(UIT, 'LEESMIJ.json');
const bestaand = fs.existsSync(jsonPad) ? JSON.parse(fs.readFileSync(jsonPad, 'utf8')) : {};
fs.writeFileSync(jsonPad, JSON.stringify({
  beeld: 'drie verhuizers dicht bij elkaar, één met een doos - vijf versies, alleen mannen',
  datum: '2026-09-22',
  aanleiding: '"dont like any ... change the photo skill to not lean heavily into the photos too much. also only use guys for the worker photos." Twee rondes afgekeurd: website/review/alle-kandidaten-20260922 en website/review/drie-verhuizers-doos-20260922.',
  model: MODEL,
  beeldverhouding: '1:1, 2K, echte PNG. Uitsnede pas na de keuze.',
  generator: '_ai-beelden/drie-mannen-gen.mjs',
  referentiegezichten: 'GEEN. Er gaat geen enkele uitsnede mee in de prompt; de mannen staan in woorden beschreven, losjes geleend van de pool. Daarmee raakt de pool ook niet verder vergeven. Gevolg met opzet: de bezetting verschilt per versie, want zonder referentiebeeld is een identieke cast niet af te dwingen.',
  cast: 'Alleen mannen, en per versie een ANDERE ploeg van drie: 58/38/24 (versie 1), 45/30/60 (versie 2), 27/52/35 (versie 3), 40/23/55 (versie 4), 33/48/begin twintig (versie 5). Geen enkele ploeg is die van de afgekeurde ronde. De zwaarste klacht was dat tien beelden dezelfde drie koppen toonden; vijf keer dezelfde nieuwe ploeg zou diezelfde fout zijn.',
  waar_de_versies_in_verschillen: 'De echtheid van de mensen, niet het camerastandpunt: de blik (versie 1), de huid en het licht (versie 2), de lijven (versie 3), de sleet en de vermoeidheid (versie 4) en de kiekje-indruk (versie 5). Daarbovenop verschilt de ploeg zelf per versie in leeftijd, postuur en haar.',
  blik: 'In alle vijf kijkt niemand in de lens. Dat was het goedkoopste punt uit de diagnose: een half afgewend gezicht dat werk doet verraadt zich veel minder dan een frontale glimlach.',
  merk: 'Nog niet op de doos. Het doosvlak is blanco gehouden; het beeldmerk gaat er pas op nadat de gebruiker een versie gekozen heeft (merk-op-doos.py van dereus-82).',
  versies: { ...(bestaand.versies || {}), ...Object.fromEntries(gedaan.map(g => [g.naam, { bestand: `${g.naam}.png`, titel: g.titel, prompt: g.prompt, mislukt: g.mislukt || false }])) },
}, null, 2));
console.log('Klaar:', UIT);
