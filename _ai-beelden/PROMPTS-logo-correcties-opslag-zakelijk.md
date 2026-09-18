# Logo-correcties: opslag en zakelijk

Uitvoering: ingebouwde imagegen, bewerking van bestaande foto's op 18 september 2026.
Referentie: `brandbook/assets/logo-v2/dereus-beeldmerk.png`.
Doel: alleen onnatuurlijk geplakte witte logovlakken corrigeren; bestaande personen, scène en uitsnede behouden.

## Zakelijk

Use case: precise-object-edit. Asset type: existing website service photo, photorealistic. Image 1 is the edit target: preserve its exact 4:3 framing, person identity, face, hair, cream shirt, posture, office, window, plant, shelf, cardboard box geometry, lighting and shadows. Image 2 is a supporting logo reference only: exact De Reus mark consisting of two blue flexed arms around a yellow house. Change ONLY the large white rectangular pasted logo label on the front face of the box: remove its white backing and all its text; restore continuous natural brown cardboard beneath it, then print a modest version of the reference blue-arms/yellow-house symbol directly on the cardboard, centered on that face, about half the current label width. No white patch, no border, no logo words. Match the perspective, material grain, warm scene lighting and box shading so it looks genuinely printed. Preserve the existing MEDIUM and OFFICE labels verbatim and unchanged. Preserve all other image details and crop. Output the edited photograph only, same aspect ratio.

## Opslag

Use case: precise-object-edit. Asset type: existing website storage-service photo, photorealistic. Image 1 is the edit target: preserve exact 4:3 framing, both workers' identities, faces, hats, posture, natural beige/brown garment colors, gloves, boxes, warehouse racks, contents, perspective and lighting. Image 2 is the supporting logo reference only: exact De Reus mark consisting of two blue flexed arms around a yellow house. Change ONLY the two stark white rectangular chest patches on the jackets. Restore the natural jacket fabric in those small areas and replace each white patch with a modest blue-arms/yellow-house emblem embroidered directly onto the chest fabric at the same location, approximately the existing emblem's size, without any white backing or rectangular border. Embroidery must follow garment folds, curvature, cloth texture and scene shadows with plausible thread texture. Keep the existing reasonably positioned printed emblems on BOTH cardboard boxes unchanged. No new words, no additional logos. Preserve every other object, person, scene detail and framing. Output only the edited photograph, same aspect ratio.

## Bestanden

- Bewerkte masters: `_ai-beelden/foto/logo-correcties/dienst-zakelijk.png` en `dienst-opslag.png`.
- Website: `img/dienst-zakelijk.webp` en `img/dienst-opslag.webp`, elk 720 × 540 pixels.
- Masters worden na generatie visueel gecontroleerd; alleen goedgekeurde resultaten vervangen de websitebestanden.

## Afwerking en controle

De gegenereerde correcties zijn met Sharp uitsluitend binnen het oude dooslabel en de twee borstpatches over de originele foto's gelegd. Vier tot acht pixels zachte rand en kleurafstemming op het karton voorkomen zichtbare plakranden. Daardoor blijven gezichten, kleding buiten de patches, magazijn, kantoorscène en bestaande dooslogo's behouden. Beide websitebestanden zijn na export op 720 × 540 pixels visueel gecontroleerd. Originele bronfoto's en ruwe generaties staan naast de definitieve PNG-masters; `_werk/herstel-logo-zakelijk-opslag.cjs` legt de afwerking vast.
