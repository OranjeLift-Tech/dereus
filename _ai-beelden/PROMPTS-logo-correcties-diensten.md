# Dienstfoto's: gerichte logocorrecties

Datum: 2026-09-18. Provider: ingebouwde imagegen-tool. Referentiebeelden zijn alleen gebruikt om het bestaande merkbeeld toe te passen.

De volledige gegenereerde masters staan in `foto/logo-correcties/`. Alleen plaatselijke correcties zijn met een zacht masker over de oorspronkelijke dienstfoto gezet. De rest van de foto blijft behouden. De drie websitebestanden blijven 720 × 540 pixels. Exportscript: `foto/logo-correcties/export-three.mjs`.

## Particulier

- Doel: `img/dienst-particulier.webp`
- Master: `foto/logo-correcties/dienst-particulier-imagegen.png`
- Beeld 1: bestaande dienstfoto. Beeld 2: `brandbook/assets/logo-v2/dereus-beeldmerk-negatief.png`.
- Bewerkt gebied op 720 × 540: afgeronde rechthoek x=74, y=265, breedte=171, hoogte=138; maskerrand 3px verzacht.

Prompt:

> Use case: precise-object-edit. Image 1 is the photograph to edit. Image 2 is a transparent brand emblem reference only.
> Make one localized edit to Image 1: remove the conspicuous white rectangular logo patch from the back of the foreground mover's royal-blue polo. Restore natural uninterrupted blue fabric there, with the existing lighting, folds and texture. In its place put a modest direct garment print of the exact emblem from Image 2, WHITE flexing arms and YELLOW house, with no rectangle, no background and no lettering. Place it centered on the upper back below the collar, entirely on the shirt, about 65 percent of the existing patch width. It should follow the turned torso perspective and fabric folds, like a real worn screen print, with the same slight photographic softness as the clothing.
> Preserve all people, identities, hair, skin, poses, the green sofa, doorway, building, existing scene details, lighting and original 4:3 framing. Do not redraw the photo into a different scene. Change only the old patch area and the replacement natural garment print. Return one edited photograph, no comparison layout. Save a full-resolution master.

## Internationaal

- Doel: `img/dienst-internationaal.webp`
- Master: `foto/logo-correcties/dienst-internationaal-imagegen.png`
- Beeld 1: bestaande dienstfoto. Beeld 2: `brandbook/assets/logo-v2/dereus-beeldmerk-negatief.png`.
- Bewerkt gebied: bovenrug en schouderstof van de voorste verhuizer; geen gezicht, nek, handen of andere persoon. Het exacte masker staat in het exportscript.

Prompt:

> Use case: precise-object-edit. Image 1 is the existing photograph to edit; Image 2 is the transparent brand emblem reference only.
> Correct ONLY the foreground grey-haired mover's blue polo shirt and its pasted-on back patch. Remove the whole oversized white rectangular patch. Restore naturally textured royal-blue cotton fabric across that area and repair the unnaturally pale recoloring on his shoulders, preserving seams, shading and folds. Put a modest direct print of Image 2's WHITE flexing arms and YELLOW house emblem on his upper back below the collar, entirely on blue fabric and away from his neck, sleeves and arms. No white rectangle, no background, no lettering. Emblem about half the existing white patch width, gently following the bent torso perspective and fabric folds, naturally photographic.
> Preserve both workers' identities, faces, skin, hair, poses and hands, the other worker's clothing, wrapped furniture, truck interior, cargo, colors, shadows, camera position and original 4:3 crop. Do not alter the work scene or add objects. Return a single edited photograph.

## Verhuislift

- Doel: `img/dienst-verhuislift.webp`
- Master: `foto/logo-correcties/dienst-verhuislift-imagegen.png`
- Beeld 1: bestaande dienstfoto. Beeld 2: `brandbook/assets/logo-v2/dereus-beeldmerk.png`.
- Bewerkt gebied op 720 × 540: afgeronde rechthoek x=525, y=229, breedte=122, hoogte=102; maskerrand 3px verzacht.

Prompt:

> Use case: precise-object-edit. Image 1 is the existing lift-truck photograph. Image 2 is a transparent brand symbol reference only.
> Make one tightly localized correction on the white cab door at the right of Image 1. Remove the oversized white rounded rectangular sticker with lettering that currently partly covers the cab window and door. Restore the original-looking glass, white painted metal, trim, door handle and panel details beneath this pasted patch. Place a modest direct cut-vinyl emblem using exactly Image 2's BLUE flexing arms and YELLOW house, with no rectangle, no background and no lettering. Put it entirely on the flat white painted door panel BELOW the glass window, to the left of the handle and above the curved wheel arch, and sufficiently small to fit without touching glass, handle, seam or wheel arch. Approximately half the current patch width. Follow the cab door's angle and lighting, with realistic subtle photographic softness.
> Preserve the entire existing truck, ladder lift, wheels, geometry, building, trees, street, all details outside this cab-door patch area, photographic look and original 4:3 crop. Do not redesign the truck. Return one edited photograph.
