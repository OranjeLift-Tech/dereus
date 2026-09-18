# Gerichte borstlogo-correcties

Datum: 2026-09-18. Skill: imagegen, ingebouwde edit-tool. Eén edit per doelbeeld; geen varianten gegenereerd.

Referentie voor beide edits: `brandbook/assets/logo-v2/dereus-beeldmerk-negatief.png` (geel huis met witte armen, zonder tekst).

## Aanvraag

- Doel en uitvoer: `img/aanvraag-foto-uit.webp`, 720 × 540, alpha behouden.
- Originele backup: `_ai-beelden/foto/logo-correcties/aanvraag-foto-uit-origineel.webp`.
- Gegenereerde master: `_ai-beelden/foto/logo-correcties/aanvraag-foto-uit-imagegen.png`.
- Tooluitvoer: `C:/Users/arnas/.codex/generated_images/01a0b4ea-4326-7b53-b0d6-b574ef9b1141/exec-f54de4ff-fd39-497f-8333-a5db2fd07f1d.png`.

### Prompt

```text
Use case: precise-object-edit.
Asset type: existing website photo/cutout, targeted shirt-logo correction only.
Input images: Image 1 is the edit target img/aanvraag-foto-uit.webp. Image 2 is the exact supporting brand mark reference, not an edit target.
Primary request: On the smiling man's wearer-left chest (viewer-right, currently around x=365 y=264 in the 720x540 original), remove the entire oversized white rectangular pocket/sticker including its lettering. Restore matching royal-blue shirt fabric there. In its place embroider a small, natural chest logo, roughly 60% the width of the old white patch: the yellow house with two WHITE flexed arms shown in Image 2. Stitch the shape directly into blue fabric, with no white rectangular backing, pocket, badge, border, or lettering. Follow the local shirt folds, diagonal perspective, texture, lighting and shadow. The mark should look modest, professional and physically part of the garment.
Invariants: Keep the SAME man, exact face and hair and smile, thumb-up gesture, arms and hands, boxes, shirt color and folds beyond the edited patch, all body proportions, room/floor/background regions, original composition, 4:3 framing, crop and boundaries exactly unchanged. Preserve the original alpha transparency wherever present; genuinely transparent pixels must remain transparent, no replacement backdrop, checkerboard, halo or flattening. No other creative edits. Produce one edited version only.
```

## Inpakken

- Doel en uitvoer: `img/verwachten-inpakken.webp`, 720 × 540, zonder alpha.
- Originele backup: `_ai-beelden/foto/logo-correcties/verwachten-inpakken-origineel.webp`.
- Gegenereerde master: `_ai-beelden/foto/logo-correcties/verwachten-inpakken-imagegen.png`.
- Tooluitvoer: `C:/Users/arnas/.codex/generated_images/01a0b4ea-4326-7b53-b0d6-b574ef9b1141/exec-ad0e2c19-ef62-4583-a734-c861178eb0d5.png`.

### Prompt

```text
Use case: precise-object-edit.
Asset type: existing website packing photo, targeted shirt-logo correction only.
Input images: Image 1 is the edit target img/verwachten-inpakken.webp. Image 2 is the exact supporting brand mark reference, not an edit target.
Primary request: Only on the kneeling man's wearer-left chest (viewer-right, near x=490 y=222 in the original 720x540 image), remove the oversized white rectangular sticker/pocket patch. Restore continuous blue fabric, and replace it with a small natural embroidered brand emblem directly on the shirt: a yellow house with two WHITE flexed arms exactly following Image 2. Scale to a modest professional chest embroidery, no larger than the old patch width, naturally foreshortened by his bent posture and aligned with the shirt folds. No white rectangle, badge backing, border, or lettering. Preserve natural blue texture, folds, shadows and perspective around the mark.
Invariants: Keep both people EXACTLY the same, same identities, faces, hair, head positions, body and hand poses, clothing colors, boxes, blank printed cardboard details, floor, mirror, blue armchair, plants, room, lighting, shadows, photo composition, camera, crop and 4:3 framing. Do not alter or add a logo to the person on the left. Change ONLY the man's existing logo patch area; every other part of Image 1 must remain unchanged. One edited version only, no other creative changes.
```

## Behoud van het origineel

De aanvraagmaster verwijderde ondanks de prompt ook delen van de oorspronkelijke kamer. Daarom zijn na toestemming alleen de door imagegen gecorrigeerde borstregio's teruggeplaatst met Sharp. De masters blijven volledig bewaard. Er is geen logo met code getekend of een ander beeld gegenereerd.

Reproduceerbaar script: `_ai-beelden/logo-correcties-formulieren.cjs`.

- Beide masters worden naar de oorspronkelijke 720 × 540 geschaald.
- Aanvraagregio: links 323, boven 214, breedte 90, hoogte 102; overgang 12 pixels.
- Inpakregio: links 461, boven 192, breedte 60, hoogte 65; overgang 8 pixels.
- Alleen RGB binnen deze borstregio's wordt gemengd met een vloeiende rand. Alle oorspronkelijke alpha-waarden blijven behouden.
- Uitvoer is lossless WebP, zodat buiten de borstregio geen extra compressiewijzigingen ontstaan.
- Controle na export: nul gewijzigde zichtbare pixels buiten de borstregio en nul gewijzigde alpha-pixels, voor beide bestanden.

Visuele controle: originele personen, pose, kamer en uitsnede behouden. Witte rechthoeken vervangen door kleine gele/witte emblemen zonder backing. Randen sluiten aan op de blauwe stof.

Ook gecontroleerd in de werkelijke homepageweergave op 1440 pixels: `aanvraag-site.png` en `inpakken-site.png` in de mastermap. Geen zichtbare compositierand of afwijkende stofkleur op weergaveformaat.
