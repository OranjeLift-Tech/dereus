# Logo Verhuisbedrijf De Reus

Bron: `logo_try-source.png` (origineel `logo_try.jpeg`, 10 versies), **versie 02 "Koningsblauw & goudgeel"**.
Referentie-uitsnede van versie 02 in de originele resolutie: `logo_try-02-crop.png`.

## Bestanden

Alle SVG's zijn vectortekeningen met tekst in outlines (geen fonts nodig), een strakke viewBox zonder marge en dezelfde schaal: **het beeldmerk is 1000 eenheden breed**, in elk logobestand. 1 eenheid is dus overal even groot.
De logo-PNG's hebben dezelfde bestandsnaam, zijn 2048 px breed, hebben een transparante achtergrond en zijn gerenderd uit de SVG.

### Logo

| Bestand (.svg + .png) | Kleuren | Gebruik | viewBox |
|---|---|---|---|
| `dereus-logo` | blauw + geel | **Primair logo.** Op wit of licht | 0 0 1000 989.61 |
| `dereus-logo-negatief` | wit + geel | Op koningsblauw `#1746A2` en diepblauw `#0B2352` | 0 0 1000 989.61 |
| `dereus-logo-1kleur` | zwart | Stempel, fax, gravure, laser, één drukgang | 0 0 1000 989.61 |
| `dereus-logo-1kleur-wit` | wit | Op foto's en donkere vlakken waar geel niet kan | 0 0 1000 989.61 |
| `dereus-logo-zonder-tagline` | blauw + geel | Kleine formaten waar de tagline onleesbaar wordt | 0 0 1000 884.78 |
| `dereus-logo-horizontaal` | blauw + geel | Alleen waar de hoogte beperkt is, zie hieronder | 0 0 2576.32 539.04 |
| `dereus-logo-horizontaal-negatief` | wit + geel | Idem, op koningsblauw of diepblauw | 0 0 2576.32 539.04 |
| `dereus-beeldmerk` | blauw + geel | Alleen het beeld, zonder tekst | 0 0 1000 539.04 |
| `dereus-beeldmerk-negatief` | wit + geel | Bus, polo, social avatar op blauw | 0 0 1000 539.04 |
| `dereus-logo-1kleur-blauw` | koningsblauw | Karton, flexodruk. Eén drukgang in koningsblauw `#1746A2` | 0 0 1000 989.61 |
| `dereus-logo-zonder-tagline-negatief` | wit + geel | Social post, websitefooter, kleine formaten op blauw | 0 0 1000 884.78 |

### Favicon en app-iconen

| Bestand | Inhoud | Gebruik |
|---|---|---|
| `dereus-favicon.svg` | geel huis op koningsblauw afgerond vierkant (viewBox 0 0 512 512) | Schaalbare bron |
| `dereus-favicon.ico` | 16, 32 en 48 px in één bestand | `<link rel="icon" href="/favicon.ico" sizes="any">` |
| `dereus-favicon-16.png`, `-32.png`, `-48.png` | idem, per formaat op de pixels uitgelijnd | Browsertab, snelkoppeling |
| `dereus-favicon-180.png` | idem, **vierkant tot de rand** (geen afronding, geen transparantie) | `apple-touch-icon`. iOS rondt zelf af, transparante hoeken worden zwart |
| `dereus-favicon-512.png` | idem, afgerond | Web app manifest |
| `dereus-favicon-armen.svg` | negatief beeldmerk (witte armen, geel huis) op koningsblauw afgerond vierkant | Schaalbare bron, alleen voor grote iconen |
| `dereus-favicon-armen-180.png` | idem, vierkant tot de rand | Alternatief `apple-touch-icon` |
| `dereus-favicon-armen-512.png` | idem, afgerond | Alternatief manifest-icoon, social avatar |

- Het volledige beeldmerk loopt onder ± 48 px dicht. Daarom is het favicon vereenvoudigd tot alleen het huis, met dezelfde vorm als in het logo (70 % van de icoonbreedte, gecentreerd).
- De PNG's van 16, 32 en 48 px zijn per formaat iets geschaald en verschoven (69,75 % tot 71,5 % breed, maximaal een halve pixel), zodat muren, dakrand en voet op hele pixels vallen. Dat geeft scherpere randen dan de SVG op dat formaat, dus gebruik voor de browsertab de `.ico` of de PNG's.
- De versie met armen is bekeken op ware grootte en leest goed op 180 en 512 px: armen, vuisten en huis blijven herkenbaar. Op 48 px en kleiner niet gebruiken.
- Advies: huis-favicon voor de browsertab, armen-versie voor `apple-touch-icon` en het manifest-icoon. Beide delen het gele huis, dus ze passen bij elkaar.

## Horizontaal logo

> **Afgeleide van logo 02, ter goedkeuring door de klant.** Deze opstelling staat niet op het originele ontwerpblad.

- Het staande logo (`dereus-logo`) blijft het **primaire** logo. Gebruik de horizontale versie alleen waar de hoogte beperkt is: websiteheader, e-mailhandtekening, achterkant bus, pen, spandoek.
- Opbouw: beeldmerk links (0 tot 1000 breed, zelfde schaal als in het staande logo), dan **1x** ruimte (117 eenheden), dan het woordmerk (1117 tot 2576,32).
- Het woordmerk bestaat uit dezelfde outlines als in het staande logo, met dezelfde onderlinge verhouding tussen de twee regels. Het is 1,693× vergroot en links uitgelijnd.
- Optische balans: het woordmerk loopt van de bovenkant van de schoorsteen (y 27) tot de voet van het huis (y 537). Het is dus even hoog als het huis. VERHUISBEDRIJF loopt van y 27 tot 192,5, DE REUS van y 241,6 tot 537.
- Geen tagline in deze versie.
- Group-ids zijn gelijk aan het staande logo: `beeldmerk` (`arm-links`, `arm-rechts`, `huis`) en `woordmerk` (`verhuisbedrijf`, `de-reus`).

## Anatomie (staand logo)

Coördinaten in viewBox-eenheden van `dereus-logo.svg` (1000 × 989.61). Spiegelas: **x = 500**. Beeldmerk en alle tekstregels zijn daarop gecentreerd.

| Nr | Onderdeel | Omschrijving | Kader (x · y) | Punt voor label |
|---|---|---|---|---|
| 1 | Linkerarm | Gespierde arm, biceps aangespannen, vuist omhoog. Koningsblauw. | 0-389 · 0-539 | vuist ≈ (265, 100) |
| 2 | Rechterarm | Exact spiegelbeeld van 1 | 611-1000 · 0-539 | vuist ≈ (735, 100) |
| 3 | Huis | Goudgeel, zadeldak van 40,5°, dakranden steken uit over de muren | 232-768 · 27-537 | (500, 300) |
| 4 | Schoorsteen | Rechts op het dak | 553-589 · vanaf 27 | (571, 60) |
| 5 | Deur | Uitgespaard (transparant), gecentreerd. Basis voor de maat **x** | 441,5-558,5 · 411-537 | (500, 474) |
| 6 | VERHUISBEDRIJF | Koningsblauw, kapitalen, smal en zwaar | 69-931 · 584-681 | (500, 632) |
| 7 | DE REUS | Goudgeel, kapitalen, 1,8× de kaphoogte van regel 6 | 95-905 · 710-885 | (500, 797) |
| 8 | Tagline | "Geen verhuizing te groot!" Goudgeel, onderkast met hoofdletter | 59-941 · 916-990 | (500, 953) |

De witte lijnen in de armen (vingers, duim, biceps, onderarm) zijn **uitsparingen**, geen witte vlakken. Op een gekleurde achtergrond schijnt die kleur er dus doorheen. Dat is bewust zo.

## Vrije ruimte

**x = de breedte van de deur = 117 eenheden.** Houd rondom minimaal **1x** vrij, gemeten vanaf de buitenste rand van het logo. Omdat het beeldmerk in elk bestand even groot is, is x overal 117 eenheden:

| Variant | x als deel van het logo |
|---|---|
| Staand logo (met of zonder tagline) | 11,7 % van de breedte |
| Beeldmerk | 11,7 % van de breedte |
| Horizontaal logo | 21,7 % van de hoogte (4,5 % van de breedte) |

Voorbeelden: staand logo van 200 px breed geeft x ≈ 23 px. Horizontaal logo van 40 px hoog geeft x ≈ 9 px.

## Minimumformaten

Getest door de logo's op deze formaten te renderen en op ware grootte te bekijken.

| Variant | Scherm | Print | Waarom |
|---|---|---|---|
| Logo met tagline | 160 px breed | 40 mm breed | Daaronder is de tagline niet meer leesbaar |
| Logo zonder tagline | 100 px breed | 25 mm breed | VERHUISBEDRIJF blijft leesbaar |
| Horizontaal logo | 28 px hoog (134 px breed) | 8 mm hoog (± 38 mm breed) | VERHUISBEDRIJF heeft dan 8,5 px kaphoogte. Op 20 px valt het weg |
| Beeldmerk | 32 px breed | 12 mm breed | Het silhouet blijft herkenbaar. De lijnen in de vuisten vallen weg onder ± 48 px |
| Favicon (huis) | 16 px | n.v.t. | Per formaat op de pixels uitgelijnd |

## Kleuren

| Naam | HEX | RGB | In het logo |
|---|---|---|---|
| Koningsblauw | `#1746A2` | 23 70 162 | armen, VERHUISBEDRIJF, favicon-achtergrond |
| Goudgeel | `#FFCC33` | 255 204 51 | huis, DE REUS, tagline |
| Wit | `#FFFFFF` | 255 255 255 | negatief (armen, VERHUISBEDRIJF) |
| Zwart | `#000000` | 0 0 0 | 1kleur |

- Koningsblauw en goudgeel zijn de waarden die bij versie 02 in het ontwerp staan. De SVG's gebruiken precies deze twee.
- Gemeten in de JPEG (ter controle): armen `#124597`, VERHUISBEDRIJF `#144493`, huis `#FFC315`, DE REUS `#FCC423`, kleurstaaltjes `#154A9C` en `#FECB38`. Die afwijking komt door JPEG-compressie en de AI-render. Gebruik de gemeten waarden niet.
- Inkt `#0E1A33` **komt niet voor in logo 02**, dat alleen blauw en geel bevat. Als tekstkleur in het merkboek werkt hij prima (17,3:1 op wit), maar hij hoort niet bij het logo. Wil je de 1kleur-versie in inkt, verander dan de `fill` van `#000000` naar `#0E1A33`.
- CMYK en Pantone zijn niet bepaald. Daarvoor is een drukproef nodig.

Contrast (WCAG):

| Voorgrond | Achtergrond | Ratio |
|---|---|---|
| Koningsblauw | wit | 8,63 : 1 |
| Goudgeel | wit | **1,51 : 1** |
| Wit | koningsblauw | 8,63 : 1 |
| Goudgeel | koningsblauw | 5,73 : 1 |
| Wit | diepblauw `#0B2352` | 15,26 : 1 |
| Goudgeel | diepblauw `#0B2352` | 10,13 : 1 |
| Koningsblauw | diepblauw `#0B2352` | **1,77 : 1**, daarom de negatief-versie op blauw |

Goudgeel op wit is zwak. Logo's vallen buiten WCAG, maar gebruik op kleine formaten op wit liever de versie zonder tagline of de horizontale versie.

## Lettertypen (dichtstbijzijnde Google Fonts)

Het origineel is AI-gegenereerd, dus het echte font is onbekend. Hieronder staan de beste overeenkomsten. Ze zijn gevonden door ± 40 kandidaten over de pixels van het origineel te leggen en de overlap (IoU) te meten.

| Tekst | Font | Instelling | Letterafstand |
|---|---|---|---|
| VERHUISBEDRIJF en DE REUS | **Archivo** ExtraBold | `font-weight: 800; font-stretch: 68%` (tussen ExtraCondensed 62 en Condensed 75) | -0,024 em en +0,026 em |
| Tagline | **Inter** ExtraBold | `font-weight: 800` | -0,02 em |

- Google Fonts: `https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Inter:wght@400..800&display=swap`
- Archivo scoorde op beide woordmerkregels het best (IoU 0,82). Roboto Condensed en Sofia Sans Condensed komen dichtbij op DE REUS, maar niet op VERHUISBEDRIJF. Voor de tagline scoort Roboto Black (900) even hoog als Inter.
- Voorstel voor het merkboek: Archivo voor koppen, Inter voor lopende tekst.

## Hoe de vector is gemaakt (en wat er is aangepast)

Logo 02 was in de bron maar ± 293 px breed. De SVG is daarom een hertekening, geen uitsnede:

- **Huis**: een exact geometrisch veelhoek, op de pixels gepast (overlap 0,945). Het kleine hapje waar de dakrand de muur raakt (een AI-artefact) is rechtgetrokken.
- **Armen**: overgetrokken met potrace uit het gemiddelde van de linkerarm en de gespiegelde rechterarm, en daarna gespiegeld. Daardoor zijn ze perfect symmetrisch (overlap 0,94).
- **Tekst**: echte fonts, omgezet naar outlines. In het origineel stonden de tekstregels 1 tot 3 px (± 1 % van de breedte) links van de as van het beeldmerk. Dat is gecorrigeerd: alles staat nu op x = 500.
- **Tagline**: in het origineel had die een donkergouden rand of reliëf. Hier is hij vlak goudgeel.
- **Horizontaal logo en favicon**: gemaakt uit precies dezelfde outlines, alleen verschaald en verplaatst. Er is niets nieuw getekend en er zijn geen nieuwe fonts gebruikt.
- Het beeldmerk is breed (1,86 : 1). Zet het voor een vierkante avatar gecentreerd in een vierkant met minimaal 1x ruimte, of gebruik `dereus-favicon-armen-512.png`.
