# Geselecteerde footertruck 2

Gebruiker koos optie 2; andere vier opties en de vijfbestanden-ZIP zijn lokaal herstelbaar gearchiveerd. Bron: `02-geselecteerd-origineel.png`. Edit: ingebouwde imagegen met officieel `brandbook/assets/logo/dereus-beeldmerk.png`. Naam en telefoon komen uit `_werk/config.py`.

## Exacte bewerkingsprompt

Use case: precise-object-edit. Image1 is the selected moving-truck EDIT TARGET. Image2 is the official De Reus logo reference. Change ONLY the graphics printed on the large white SIDE CARGO PANEL: make the current blue-arms/yellow-house logo about half its current height, centered in the upper portion of that panel, faithful to the reference. Below the symbol put exact dark-blue lettering 'Verhuisbedrijf De Reus' with 'DE REUS' visually prominent; at the BOTTOM of the white side panel print exact phone number '085 000 5647' in large clean dark-blue sans-serif, with safe margins above the metal lower edge. Every letter and digit must be correct. Logo/name/phone must follow the side panel's perspective and natural reflected lighting, appearing professionally printed on the vehicle, never floating or crossing panel boundaries. Preserve the original truck exactly: front-left three-quarter angle, cab/windows/wheels/mirrors/body geometry, white and blue paint, framing, scale, lighting and all pixels outside the panel as closely as possible. Preserve genuine transparent alpha outside vehicle; no scenery or new background, no platform, no added shadows or watermark, no URLs or invented text. Output a high-resolution PNG with transparency.

## Export en controle

`node _werk/export-footer-truck.cjs` neemt alleen het bewerkte zijpaneel over, behoudt de oorspronkelijke truckpixels daarbuiten en de volledige oorspronkelijke alpha. Master: `_ai-beelden/foto/footer-truck/02-footer-definitief.png`; website: `img/footer-truck.webp` (960 x 640). Visueel gecontroleerd: kleiner beeldmerk, juiste merknaam, exact `085 000 5647`, tekst binnen paneel en geen zichtbare compositienaad. Alleen het echte footerlogo vervangen; headerlogo en decoratief footerbeeldmerk ongewijzigd.
