# Logo v2 Verhuisbedrijf De Reus

**Status:** nieuwe versie van het logo, gekozen door de klant: optie 1 "Evolutie" uit `logo-opties/optie-1-evolutie.png` (een raster van 2048 px uit een beeldmodel). Brief: grotere biceps, en **geen tagline** onder de naam.

- **Merkboek 1.0** gaat nog uit met het oude logo in `brandbook/assets/logo/`. Die map is niet aangeraakt.
- **Wisselen:** de bestandsnamen zijn gelijk aan die in `logo/`, dus de wissel is het vervangen van de map.
- **Referentiebeeld:** `vergelijking.png` zet het raster, deze vector en het oude logo naast elkaar: groot en op 120, 64 en 32 px, op wit en op koningsblauw.

## Bestanden

Alle SVG's zijn vectortekeningen met tekst in outlines (geen fonts nodig) en een strakke viewBox zonder marge. Ze hebben één schaal: **het beeldmerk is 1000 eenheden breed**, in elk logobestand. De PNG's hebben dezelfde naam, zijn 2048 px breed en transparant, en zijn gerenderd uit de SVG.

| Bestand (.svg + .png) | Kleuren | Gebruik | viewBox |
|---|---|---|---|
| `dereus-logo` | blauw + geel | **Primair logo**, zonder tagline. Op wit of licht | 0 0 1000 827.99 |
| `dereus-logo-negatief` | wit + geel | Op koningsblauw `#1746A2` en diepblauw `#0B2352` | 0 0 1000 827.99 |
| `dereus-logo-1kleur` | zwart | Stempel, fax, gravure, laser, één drukgang | 0 0 1000 827.99 |
| `dereus-logo-1kleur-wit` | wit | Op foto's en donkere vlakken waar geel niet kan | 0 0 1000 827.99 |
| `dereus-logo-1kleur-blauw` | koningsblauw | Karton, flexodruk: één drukgang in `#1746A2` | 0 0 1000 827.99 |
| `dereus-logo-zonder-tagline` | blauw + geel | **Alias** van `dereus-logo` (identiek), zodat bestaande verwijzingen blijven werken | 0 0 1000 827.99 |
| `dereus-logo-zonder-tagline-negatief` | wit + geel | **Alias** van `dereus-logo-negatief` (identiek) | 0 0 1000 827.99 |
| `dereus-logo-horizontaal` | blauw + geel | Alleen waar de hoogte beperkt is | 0 0 2444.21 509.39 |
| `dereus-logo-horizontaal-negatief` | wit + geel | Idem, op koningsblauw of diepblauw | 0 0 2444.21 509.39 |
| `dereus-beeldmerk` | blauw + geel | Alleen het beeld, zonder tekst | 0 0 1000 509.39 |
| `dereus-beeldmerk-negatief` | wit + geel | Bus, polo, social avatar op blauw | 0 0 1000 509.39 |

- **Group-ids** zijn gelijk aan versie 1: `beeldmerk` (`arm-links`, `arm-rechts`, `huis`) en `woordmerk` (`verhuisbedrijf`, `de-reus`).
- **Titels:** "Verhuisbedrijf De Reus" en "Verhuisbedrijf De Reus, beeldmerk".

### Favicon en app-iconen

| Bestand | Inhoud |
|---|---|
| `dereus-favicon.svg`, `.ico`, `-16.png`, `-32.png`, `-48.png`, `-180.png`, `-512.png` | Het gele huis op een koningsblauw afgerond vierkant. **Ongewijzigd overgenomen** uit `logo/`: het huis is in versie 2 niet veranderd. Gebruik, de uitlijning op pixels en de apple-touch-regels staan in `logo/README.md`. |
| `dereus-favicon-armen.svg`, `-armen-180.png` (vierkant tot de rand), `-armen-512.png` (afgerond) | **Opnieuw gemaakt** met de nieuwe armen: het negatieve beeldmerk op 90 % van de breedte. Bekeken op ware grootte: leest goed op 180 en 512 px. Niet gebruiken op 48 px en kleiner. |

## Horizontaal logo

> Afgeleide van het gekozen logo, ter goedkeuring door de klant. Deze opstelling staat niet op het ontwerpblad.

- **Opbouw:**
  - het beeldmerk links, op de vaste schaal (1000 breed);
  - dan 1x ruimte (de breedte van de deur, 107,2 eenheden);
  - dan het woordmerk, links uitgelijnd. Het loopt van de bovenkant van de schoorsteen tot de voet van het huis, dus het is **even hoog als het huis**.
- **Beide regels** hebben dezelfde onderlinge verhouding als in het staande logo.
- **Gebruik:** het staande logo blijft primair. Gebruik de horizontale versie alleen waar de hoogte beperkt is: websiteheader, e-mailhandtekening, achterkant bus, pen, spandoek.

## Anatomie (staand logo)

Coördinaten in viewBox-eenheden van `dereus-logo.svg` (1000 × 827.99). Spiegelas: **x = 500**. Beeldmerk en tekst staan daarop gecentreerd.

| Nr | Onderdeel | Omschrijving | Kader (x · y) | Punt voor label |
|---|---|---|---|---|
| 1 | Linkerarm | Gespierde arm met een grote, ronde biceps en een brede schouder, vuist omhoog. Koningsblauw. | 0-328 · 0-508 | vuist ≈ (205, 70), biceps ≈ (170, 360) |
| 2 | Rechterarm | Exact spiegelbeeld van 1 | 672-1000 · 0-508 | vuist ≈ (795, 70) |
| 3 | Huis | Goudgeel, zadeldak van 40,5°, dakranden steken uit over de muren. Gelijk aan versie 1. | 255-745 · 42-509 | (500, 280) |
| 4 | Schoorsteen | Rechts op het dak | 549-582 · vanaf 42 | (565, 70) |
| 5 | Deur | Uitgespaard (transparant), gecentreerd. Basis voor de maat **x** | 446,4-553,6 · 394-509 | (500, 452) |
| 6 | VERHUISBEDRIJF | Koningsblauw, kapitalen, Archivo ExtraBold op breedte 68 | 105-895 · 552-642 | (500, 597) |
| 7 | DE REUS | Goudgeel, kapitalen, 1,8× de kaphoogte van regel 6 | 129-871 · 668-828 | (500, 748) |

- **Uitsparingen:** de witte lijnen in de armen zijn uitsparingen, geen witte vlakken. Het gaat om de knokkels, de duim, de plooi bij de pols, de plooi in de elleboog, de rand van de biceps en de boog onder de biceps. Op een gekleurde achtergrond schijnt die kleur erdoor.
- **Spleet:** tussen arm en muur zit een vaste spleet van 19,2 eenheden. De bovenarm loopt achter het huis door.

## Vrije ruimte

**x = de breedte van de deur = 107,2 eenheden.** Houd rondom minimaal **1x** vrij, gemeten vanaf de buitenste rand van het logo.

| Variant | x als deel van het logo |
|---|---|
| Staand logo | 10,7 % van de breedte |
| Beeldmerk | 10,7 % van de breedte |
| Horizontaal logo | 21,1 % van de hoogte (4,4 % van de breedte) |

Voorbeelden: staand logo van 200 px breed geeft x ≈ 21 px. Logo van 50 mm breed geeft x ≈ 5,4 mm.

## Minimumformaten

Opnieuw getest door op deze formaten te renderen en op ware grootte te bekijken.

| Variant | Scherm | Print | Waarom |
|---|---|---|---|
| Staand logo (geen tagline meer) | 100 px breed | 25 mm breed | VERHUISBEDRIJF heeft dan 8,9 px kaphoogte en blijft leesbaar; op 80 px valt het weg |
| Horizontaal logo | 28 px hoog (134 px breed) | 8 mm hoog (± 38 mm breed) | VERHUISBEDRIJF heeft dan ± 8,3 px kaphoogte |
| Beeldmerk | 32 px breed | 12 mm breed | Met de zwaardere armen blijft het silhouet herkenbaar. Onder ± 48 px lopen de lijnen in de vuisten dicht; op 24 px is het een vlek |
| Favicon (huis) | 16 px | n.v.t. | Ongewijzigd |
| Favicon met armen | 180 px | n.v.t. | Leest goed op 180 en 512 px |

## Kleuren en letter

- **Kleuren:** precies twee, Koningsblauw `#1746A2` en Goudgeel `#FFCC33`. Wit voor de negatieve versies, zwart voor 1kleur, Koningsblauw voor 1kleur-blauw. Het raster wijkt daar in de pixels een beetje van af (`#1C47A3`, `#FFC933`); dat is overgenomen van het merkboek, niet van het raster.
- **Letter:** Archivo ExtraBold op breedte 68, dezelfde outlines als versie 1 (zie `logo/README.md`).

## Hoe getrouw de vector is

Gemeten als overlap (IoU) met het raster, per kleur, in de pixels van het raster:

| Onderdeel | IoU | Toelichting |
|---|---|---|
| Armen, puur overgetrokken (zonder de aanpassingen hieronder) | **0,981** | het overtrekken zelf is nauwkeurig |
| Huis (veelhoek van versie 1) | **0,982** | de verhoudingen van het huis in het raster zijn gelijk aan versie 1, binnen 0,3 % |
| VERHUISBEDRIJF (outlines van versie 1) | **0,959** | breedte, hoogte en positie gelijk binnen 1 eenheid van versie 1 |
| DE REUS (outlines van versie 1) | **0,963** | idem |
| Hele logo, puur | **0,979** | |
| Hele logo, definitief | 0,900 (armen 0,790) | het verschil komt volledig door de bewuste aanpassingen hieronder |

## Wat er veranderd is ten opzichte van het raster

1. **Symmetrie:** één arm is overgetrokken uit het gemiddelde van de linkerarm en de gespiegelde rechterarm (spiegel-IoU 0,995) en daarna gespiegeld. De armen zijn nu exact symmetrisch om x = 500.
2. **Vuisten 1,2× groter**, via een zachte vervorming vanaf de pols, zonder trapje. Dat gaat richting de verhouding van het oude logo: in het raster waren de vuisten klein geworden naast de zware armen.
3. **Armen los van het huis:**
   - de armen staan 13 eenheden verder naar buiten;
   - de bovenarm loopt achter de muur door en is afgesneden op een **vaste spleet** van 19,2 eenheden van het huis;
   - de biceps is daardoor volledig rond te zien en wordt niet meer door de muur afgekapt.
4. **Artefacten van het beeldmodel weg:**
   - haakjes en sporen aan de duimkrul (zijtakjes van minder dan 30 px in het skelet van de lijnen weggehaald);
   - losse snippers;
   - een knik in de elleboog;
   - kleine deuken in de onderarm.
   - De omtrek is gladgemaakt; de lijnen zijn apart gladgemaakt, zodat ze niet dunner worden.
5. **Huis en woordmerk:** niet overgetrokken, maar overgenomen uit versie 1. Ze zijn gelijk aan het raster, dus een nieuwe trace zou alleen ruis toevoegen.
6. **Geen tagline**, volgens de brief.

## Bij de wissel in het merkboek

- `dereus-logo` heeft nu **geen tagline** meer. Teksten in het merkboek die zeggen dat "Geen verhuizing te groot!" in het logo staat, moeten mee veranderen (onder andere `brandbook/content/copy.md` en het logohoofdstuk). De regel "één slogan per blok" wordt eenvoudiger, omdat er geen slogan meer in het logo zelf staat.
- De minimummaat van het primaire logo gaat van 160 naar **100 px** (van 40 naar 25 mm).
- Mockups die `dereus-logo-zonder-tagline` gebruiken, blijven werken via de alias.
