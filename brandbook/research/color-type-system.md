# Kleur en typografie · Verhuisbedrijf De Reus

- **Versie:** 1.0, 18 september 2026
- **Bron:** logo #02 "Koningsblauw & goudgeel" uit `logo_try.jpeg` (het vel heeft 10 varianten; #02 staat bovenaan als tweede van links en is ook zo genummerd), plus de huidige site (`research/website-brief.md` en de live CSS).
- **Methode:** kleuren gemeten met pixel-sampling (mediaan per vlak), tinten berekend in OKLCH, contrast berekend volgens WCAG 2.x (niet geschat), CMYK omgerekend met het ICC-profiel Coated FOGRA39, Pantone gekozen op de kleinste kleurafstand (CIEDE2000) tot de sRGB-waarden die Pantone publiceert. Het lettertype is gecontroleerd door de tekst uit het logo naast Archivo te zetten.
- **Voor de bouwer:** het `:root`-blok in hoofdstuk 8 gebruikt dezelfde variabelen als `brandbook/tokens.css` en kan het voorlopige blok 1 plus de typografie vervangen.

---

## 1. Samenvatting

| | |
|---|---|
| **Merkkleuren** | Koningsblauw `#1746A2` (primair) · Diepblauw `#0B2352` (secundair) · Goudgeel `#FFCC33` (accent) |
| **Neutralen** | Inkt `#0E1A33` · Grafiet `#2E3647` · Leisteen `#5E6675` · Staalgrijs `#838996` · Zilvergrijs `#D3D7DE` · Mist `#F6F7F9` · Wit `#FFFFFF` |
| **Functioneel** | Fout `#B42318` · Succes `#1E7A3C` |
| **CTA-knop** | Goudgeel `#FFCC33` met Diepblauwe tekst (10,13:1), hover `#F7B817` (8,59:1) |
| **Koppen** | Archivo, Condensed (breedte 75), ExtraBold 800 en Bold 700 |
| **Tekst en interface** | Inter, 400 / 600 / 700 (800 alleen in taglineregels) |
| **Verhouding** | 60 licht / 30 blauw / 10 geel |

---

## 2. Bron: de kleuren van logo #02

Het vel noemt de kleuren van #02 zelf: **#1746A2** en **#FFCC33**. De gemeten pixels:

| Onderdeel | Gemeten (mediaan) | Opgegeven | Kleurafstand (ΔE2000) |
|---|---|---|---|
| Armen en vuisten | `#134697` | `#1746A2` | 1,8 |
| "VERHUISBEDRIJF" | `#134391` | `#1746A2` | 2,5 |
| Huis | `#FEC316` | `#FFCC33` | 2,7 |
| "DE REUS" | `#FCC422` | `#FFCC33` | 2,1 |
| Kleurvlakje op het vel zelf | `#154A9C` / `#FECB38` | `#1746A2` / `#FFCC33` | 2,0 / 0,5 |

Het kleurvlakje met de opgegeven waarde komt in de JPEG zelf al op ΔE 2,0 uit. De afwijking in het logo zit dus grotendeels in de compressie. **Besluit:** de opgegeven waarden zijn de officiële merkkleuren. De voorlopige waarden in `tokens.css` (`#1746A2`, `#FFCC33`) kloppen en blijven staan. Wordt het logo als vector nagetekend, vul het dan met exact deze twee waarden en niet met de gemeten pixels.

---

## 3. Palet

### Merkkleuren

| Rol | Naam | HEX | RGB | CMYK (FOGRA39) | Pantone (dichtstbij) | Token |
|---|---|---|---|---|---|---|
| Primair | **Koningsblauw** | `#1746A2` | 23 70 162 | 97 77 0 0 | **293 C** (ΔE 3,0; alternatief 2728 C of 7687 C) | `--brand-primary` |
| Secundair | **Diepblauw** | `#0B2352` | 11 35 82 | 98 75 1 60 | **655 C** (ΔE 1,8; alternatief 2768 C) | `--brand-secondary` |
| Accent | **Goudgeel** | `#FFCC33` | 255 204 51 | 0 20 85 0 | **123 C** (ΔE 1,6; alternatief 122 C) | `--brand-accent` |

- **Koningsblauw** is de kleur van de armen en van "VERHUISBEDRIJF": kracht en betrouwbaarheid. Gebruik het voor koppen, links, iconen, blauwe banden en de secundaire knop.
- **Diepblauw** komt niet in het logo voor. Het is Koningsblauw in de donkerste stap: zelfde tint, veel donkerder. Het geeft diepte (footer, donkere banden, tekst op geel) en is de donkere partner die het oude `#054A76` niet kon zijn (zie hoofdstuk 6).
- **Goudgeel** is het huis en "DE REUS". Het is de tweede logokleur, maar in de opmaak werkt het als accent: de knop die telt, de sterren bij reviews, één markering. Geel op wit is onleesbaar (1,51:1).

### Neutralen

| Naam | HEX | RGB | CMYK | Pantone | Token | Gebruik |
|---|---|---|---|---|---|---|
| **Inkt** | `#0E1A33` | 14 26 51 | 83 62 17 81 | 282 C (benadering) | `--ink` | Lopende tekst. In drukwerk kleine tekst in 100 K. |
| **Grafiet** | `#2E3647` | 46 54 71 | 66 49 23 71 | 7546 C (benadering) | `--graphite` | Titels in kaarten, tekst op lichte knoppen |
| **Leisteen** | `#5E6675` | 94 102 117 | 50 36 22 46 | Cool Gray 10 C (benadering) | `--grey-600` | Gedempte tekst, bijschriften |
| **Staalgrijs** | `#838996` | 131 137 150 | 41 29 20 29 | 7544 C (benadering) | `--grey-400` | Randen van invoervelden. **Gewijzigd**, was `#8C93A0` (2,88:1 op Mist, te licht). |
| **Zilvergrijs** | `#D3D7DE` | 211 215 222 | 20 13 11 0 | 7541 C (benadering) | `--grey-300` | Scheidingslijnen (alleen decoratief) |
| **Mist** | `#F6F7F9` | 246 247 249 | 4 2 2 0 | geen (alleen scherm) | `--off-white` | Afwisselende secties, panelen |
| **Wit** | `#FFFFFF` | 255 255 255 | 0 0 0 0 | papierwit | `--white` | Hoofdachtergrond |

### Functioneel (alleen scherm)

| Naam | HEX | RGB | Token | Contrast op wit |
|---|---|---|---|---|
| **Fout** | `#B42318` | 180 35 24 | `--error` (tint `--error-50` `#FEF3F2`) | 6,57:1 |
| **Succes** | `#1E7A3C` | 30 122 60 | `--success` (tint `--success-50` `#EDF7F0`) | 5,38:1 |

Succes is een verdonkerde versie van het oude CTA-groen `#319C5A` (zelfde tint). Het groen blijft dus alleen als meldingskleur bestaan.

**Over CMYK en Pantone.** CMYK is omgerekend van sRGB met het ICC-profiel Coated FOGRA39 (ISO 12647-2, de gangbare norm voor offset op gestreken papier in Nederland), relatief colorimetrisch met zwartpuntcompensatie. Voor ongestreken papier of digitaal drukwerk laat de drukker zelf omrekenen vanaf HEX of Pantone. Pantone is de dichtstbijzijnde Solid Coated-kleur. Leg die vóór de eerste oplage naast een Pantone Formula Guide, want op ongestreken papier (U) valt dezelfde kleur anders uit. Bij de neutralen is de afstand groter (ΔE 4 tot 6): gebruik die Pantone-waarden alleen als er echt een steunkleur nodig is.

### Tinten en schaduwen

Berekend in OKLCH op de tint van de merkkleur. De bouwer leidt de tinten zelf af met `color-mix()`. Deze tabel geeft de doelwaarden voor mockups en drukwerk.

| Stap | Koningsblauw | Goudgeel |
|---|---|---|
| 50 | `#F3F7FE` blauwe kaart op wit | `#FFFAEC` **Crème**: tipvak, markering (≈ 10 % Goudgeel) |
| 100 | `#E6EFFF` | `#FFF3D1` |
| 200 | `#CDDFFF` | `#FFE6A4` |
| 300 | `#9EBEF8` links op Diepblauw (8,12:1) | `#FFDA7A` |
| 400 | `#5483DD` alleen iconen en grote vlakken (3,71:1) | `#FFD460` |
| **500** | **`#1746A2` Koningsblauw** | **`#FFCC33` Goudgeel** |
| 600 | `#123780` hover van de blauwe knop (11,15:1 met wit) | `#F7B817` hover van de CTA |
| 700 | `#0F2D68` | `#DB940E` alleen illustratie, nooit tekst (2,54:1) |
| 800 | `#0B2352` **= Diepblauw** | niet gebruiken |
| 900 | `#091938` | niet gebruiken |

Donkerder geel dan stap 700 wordt bruin of olijf en hoort niet bij het merk. Tip voor `tokens.css`: zet `--primary-800: var(--brand-secondary)`, dan valt die stap precies op Diepblauw.

### Verhoudingen: 60 / 30 / 10

| Deel | Kleuren | Aandeel |
|---|---|---|
| **60 % licht** | Wit (± 45 %), Mist (± 15 %) | De rust van de pagina |
| **30 % blauw** | Koningsblauw (± 20 %), Diepblauw (± 10 %) | Koppen, iconen, banden, footer |
| **10 % geel** | Goudgeel en Crème | CTA, sterren, één markering per scherm |

Tekst in Inkt telt niet mee: dat is inhoud. Voelt een pagina geel aan, dan zit er te veel geel in.

---

## 4. De CTA-knop

Hier is de keuze gemaakt: de logokleuren gaan voor en het groen verdwijnt als knopkleur.

| Token | Waarde | Contrast | Oordeel |
|---|---|---|---|
| `--color-cta` | Goudgeel `#FFCC33` | | |
| `--color-cta-text` | Diepblauw `#0B2352` | 10,13:1 op `#FFCC33` | AA en AAA |
| `--color-cta-hover` | `#F7B817` (goud 600), de tekst blijft Diepblauw | 8,59:1 | AA en AAA |

- **Vorm:** pil (`--radius-button: 999px`), zoals op de huidige site. Tekst in Inter 700 op 17 px, minimaal 48 px hoog.
- **Focus:** een ring van 3 px met 2 px afstand. Koningsblauw op lichte achtergronden (8,63:1 op wit), wit op Koningsblauw of Diepblauw.
- **Waarom de hover geel blijft.** De voorlopige tokens lieten de knop bij hover blauw worden met witte tekst. Op een blauwe band valt de knop dan weg in de achtergrond en springt de tekstkleur om. Een donkerder geel werkt op elke achtergrond.
- **Secundaire knop:** Koningsblauw met witte tekst (8,63:1), hover `#123780` (11,15:1). Op blauwe banden wordt het een witte knop met Koningsblauwe tekst.
- **Waarom geen groen.** Witte tekst op `#319C5A` haalt 3,48:1. Knoptekst van 18 px bold telt niet als grote tekst, dus de huidige knoppen zakken voor AA. Groen staat bovendien niet in het logo.

---

## 5. Contrast (WCAG 2.2, niveau AA)

Normale tekst vraagt minstens 4,5:1. Grote tekst (vanaf 24 px, of 18,66 px bold) en interface-onderdelen (randen van velden, iconen, focusringen) vragen 3:1.

| Voorgrond | Achtergrond | Ratio | Tekst (4,5) | Groot en UI (3,0) | Gebruik |
|---|---|---|---|---|---|
| Inkt `#0E1A33` | Wit | 17,29 | ja | ja | Lopende tekst |
| Inkt | Mist `#F6F7F9` | 16,13 | ja | ja | Tekst in panelen |
| Inkt | Goudgeel | 11,48 | ja | ja | Tekst op gele vlakken |
| Grafiet `#2E3647` | Wit | 12,10 | ja | ja | Kaarttitels |
| Leisteen `#5E6675` | Wit | 5,78 | ja | ja | Gedempte tekst |
| Leisteen | Mist | 5,39 | ja | ja | Gedempte tekst in panelen |
| Koningsblauw | Wit | 8,63 | ja | ja | Koppen, links (AAA) |
| Koningsblauw | Mist | 8,05 | ja | ja | Koppen in panelen |
| Koningsblauw | Crème `#FFFAEC` | 8,27 | ja | ja | Tipvakken |
| Wit | Koningsblauw | 8,63 | ja | ja | Blauwe banden, secundaire knop |
| Wit | Diepblauw | 15,26 | ja | ja | Footer |
| Goudgeel | Diepblauw | 10,13 | ja | ja | Koppen en iconen op donker |
| Goudgeel | Koningsblauw | 5,73 | ja | ja | Accentwoorden op blauw |
| Diepblauw | Goudgeel | 10,13 | ja | ja | **CTA** |
| Diepblauw | `#F7B817` | 8,59 | ja | ja | **CTA hover** |
| Blauw 300 `#9EBEF8` | Diepblauw | 8,12 | ja | ja | Links in de footer |
| Staalgrijs `#838996` | Wit / Mist | 3,51 / 3,27 | nee | ja | Alleen randen van velden |
| Fout `#B42318` | Wit / Mist | 6,57 / 6,13 | ja | ja | Foutmeldingen |
| Succes `#1E7A3C` | Wit / Mist | 5,38 / 5,02 | ja | ja | Bevestigingen |

### Combinaties die niet mogen

| Voorgrond | Achtergrond | Ratio | Waarom niet |
|---|---|---|---|
| Goudgeel | Wit | 1,51 | Onleesbaar, ook voor iconen. Zet de tagline nooit als losse gele tekst op wit. In het logo zelf mag het (logo's vallen buiten WCAG). |
| Wit | Goudgeel | 1,51 | Onleesbaar |
| Goud 700 `#DB940E` | Wit | 2,54 | Haalt zelfs 3:1 niet |
| Koningsblauw | Diepblauw | 1,77 | Valt weg. Het logo in full colour op Diepblauw verliest zijn armen: gebruik daar de negatieve versie. |
| Goudgeel | Fout-rood | 4,36 | Te zwak voor tekst, en rood met geel leest als "aanbieding" of "waarschuwing" |
| Zilvergrijs `#D3D7DE` | Wit | 1,44 | Alleen voor decoratieve lijnen, nooit als enige rand van een veld |
| Wit | oud groen `#319C5A` | 3,48 | De huidige knoppen: zakt voor AA |
| Oud grijs `#6E6E6E` | oud `#F0F0F0` | 4,47 | De huidige USP-balk: zakt net voor AA |

---

## 6. Overgang van de huidige website

Wat blijft: een witte basis, blauw als hoofdkleur, pilvormige knoppen, afwisselend lichte secties en lopende tekst van rond 18 px. Wat verandert:

| Oude kleur | Waar nu | Wordt | Waarom |
|---|---|---|---|
| Navy `#054A76` | Header, footer, koppen, lopende tekst | Koningsblauw (koppen, links, iconen), Diepblauw (footer, donkere banden), Inkt (lopende tekst) | `#054A76` is petrolblauw (tint 245°), Koningsblauw ligt op 262°: ΔE 7,7. Naast elkaar ziet dat eruit als een fout. Ze zijn ook even donker (onderling contrast 1,08), dus `#054A76` kan niet de donkere partner zijn. |
| CTA-groen `#319C5A` | Alle offerteknoppen, het offertepaneel | Goudgeel met Diepblauwe tekst. Groen leeft voort als Succes `#1E7A3C`. | Staat niet in het logo; witte tekst haalt maar 3,48:1 |
| Accentblauw `#287EDC` | Vinkjes in cirkels, hover van de header-CTA | Koningsblauwe cirkel met wit vinkje; op blauw een gele cirkel met Diepblauw vinkje | Een derde blauw is er één te veel |
| Blauwgrijs `#E2E8EF` | Dienstentegels, reviewsectie | Mist `#F6F7F9` voor secties; tegels wit op Mist of blauw 50 `#F3F7FE` | Lichter en rustiger naast Koningsblauw |
| Grijs `#F0F0F0` | USP-balk, afwisselende secties | Mist `#F6F7F9` | Eén lichte vlakkleur in plaats van twee |
| Lijnblauw `#CBDCE9` | Scheidingslijnen | Zilvergrijs `#D3D7DE` | Neutraal, botst niet met Koningsblauw |
| Grijs `#6E6E6E` | USP-balk (cursief) | Leisteen `#5E6675` | 5,39:1 op Mist, het oude grijs zakte op `#F0F0F0` |
| Zwart `#000000` | Reviewtekst | Inkt `#0E1A33` | Zachter, met een blauwe ondertoon |
| Stergeel `~#FFDE45` | Google-sterren | Goudgeel `#FFCC33` | Past vanzelf; zet de score er altijd als tekst bij ("4,9/5") |
| Mascotte: navy `#055285`, karton `#CA9C4E`, huid `#E4AC67` | Mascotte | Geen merkkleuren. Blijft de mascotte in gebruik (dat besluit hoort bij de logosessie), kleur het uniform dan om naar Koningsblauw en Diepblauw. | Karton en huid zijn illustratiekleuren |
| Wix-standaarden `#1A6AFF`, `#116DFF`, `#2B5672` | Ongebruikte widgets | Vervallen | Nooit merkkleuren geweest |

Ook de lettertypes gaan over: zie hoofdstuk 7.

---

## 7. Typografie

### Twee lettertypes, rechtstreeks uit het logo

| Rol | Lettertype | Gewichten | Waarom |
|---|---|---|---|
| **Koppen** | **Archivo** (Google Fonts), breedte 75 = "Condensed" | 800 ExtraBold (Display, H1, H2), 700 Bold (H3) | Het woordmerk is Archivo ExtraBold op een breedte van ± 68 (vastgesteld door de logosessie en door ons naast het logo gezet: dezelfde R met rechte poot, dezelfde compacte S). Koppen staan op 75: net wat opener, beter leesbaar in lange Nederlandse koppen, en er bestaat een los "Condensed"-bestand voor drukwerk. Breedte 68 blijft voor het logo. |
| **Tekst en interface** | **Inter** (Google Fonts) | 400 lopende tekst, 600 nadruk en labels, 700 H4 tot H6 en knoppen, 800 alleen voor regels in taglinestijl | De tagline "Geen verhuizing te groot!" staat in Inter ExtraBold. Inter is gemaakt voor schermen, heeft een grote x-hoogte en duidelijke cijfers (prijzen, 085 000 5647, 4,9/5). |

- **Licentie:** beide staan onder de SIL Open Font License 1.1. Ze zijn gratis voor web, drukwerk, commercieel gebruik en insluiten in pdf, zonder naamsvermelding.
- **Bestanden voor drukwerk** (download op fonts.google.com, map `static`): `Archivo_Condensed-ExtraBold.ttf`, `Archivo_Condensed-Bold.ttf`, `Inter_18pt-Regular.ttf`, `Inter_18pt-SemiBold.ttf`, `Inter_18pt-Bold.ttf`, `Inter_18pt-ExtraBold.ttf`. Voor grote koppen in Inter zijn er ook de `Inter_24pt`- en `Inter_28pt`-varianten.
- **Wat vervalt:** Wix Madefor Display (koppen), Almarai (tekst), Wix Madefor Text (knoppen) en Glacial Indifference (het oude logo). Wix Madefor en Almarai staan wel gratis op Google Fonts; dat is dus niet de reden. Ze passen alleen niet bij het zware, smalle woordmerk. Glacial Indifference hoorde bij het oude, breed gespatieerde logo.

### Typeschaal

Rootgrootte 16 px. Vloeiende maten groeien mee van mobiel (375 px) naar desktop (1280 px).

| Rol | Token | px (mobiel tot desktop) | rem | Lettertype | Gewicht | Regelhoogte | Spatiëring | Schrijfwijze |
|---|---|---|---|---|---|---|---|---|
| Display | `--text-display` | 44 tot 72 | `clamp(2.75rem, 2rem + 3.2vw, 4.5rem)` | Archivo Condensed | 800 | 1.05 | 0 | Hoofdletters mag, maximaal 5 woorden |
| H1 | `--text-h1` | 40 tot 56 | `clamp(2.5rem, 2rem + 2vw, 3.5rem)` | Archivo Condensed | 800 | 1.05 | 0 | Zinsnaamval |
| H2 | `--text-h2` | 32 tot 40 | `clamp(2rem, 1.75rem + 1vw, 2.5rem)` | Archivo Condensed | 800 | 1.15 | 0 | Zinsnaamval |
| H3 | `--text-h3` | 24 tot 28 | `clamp(1.5rem, 1.4rem + 0.4vw, 1.75rem)` | Archivo Condensed | 700 | 1.15 | 0 | Zinsnaamval |
| H4 | `--text-h4` | 20 tot 22 | `clamp(1.25rem, 1.2rem + 0.2vw, 1.375rem)` | Inter | 700 | 1.3 | -0.01em | Zinsnaamval |
| H5 | `--text-h5` | 18 | `1.125rem` | Inter | 700 | 1.3 | 0 | Zinsnaamval |
| H6 / label | `--text-h6` | 14 | `0.875rem` | Inter | 700 | 1.3 | 0.08em | HOOFDLETTERS |
| Intro | `--text-lead` | 20 | `1.25rem` | Inter | 400 | 1.5 | 0 | |
| Lopende tekst | `--text-body` | 18 | `1.125rem` | Inter | 400 | 1.6 | 0 | |
| Klein | `--text-small` | 16 | `1rem` | Inter | 400 | 1.5 | 0 | Bijschriften, formulieren |
| Extra klein | `--text-xs` | 14 | `0.875rem` | Inter | 400 | 1.5 | 0 | Alleen juridische regels en copyright |
| Knop | `--text-button` | 17 | `1.0625rem` | Inter | 700 | 1 | 0 | Zinsnaamval |

Ten opzichte van de voorlopige `tokens.css` veranderen deze maten: lopende tekst gaat van 17 naar **18 px** (de doelgroep bestaat deels uit ouderen, en de huidige site zit al op 18 tot 20 px), klein van 15 naar **16 px** en extra klein van 13 naar **14 px**.

### Google Fonts

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75,700..800&family=Inter:opsz,wght@14..32,400..800&display=swap" rel="stylesheet">
```

Getest: de link geeft Archivo op breedte 75 (700 tot 800) en Inter variabel (400 tot 800, met optische grootte). Wie zelf host, haalt deze CSS op met een moderne browser, bewaart de woff2-bestanden voor `latin` en `latin-ext` in `assets/fonts/` en neemt de `@font-face`-regels over:

```css
@font-face {
  font-family: "Archivo";
  font-style: normal;
  font-weight: 700 800;
  font-stretch: 75%;
  font-display: swap;
  src: url("assets/fonts/archivo-condensed-latin.woff2") format("woff2");
}
@font-face {
  font-family: "Inter";
  font-style: normal;
  font-weight: 400 800;
  font-display: swap;
  src: url("assets/fonts/inter-latin.woff2") format("woff2");
}
/* Koppen: font-family: var(--font-display); font-stretch: var(--font-display-stretch); */
```

Neem de `unicode-range`-regels uit de opgehaalde CSS over als je `latin` en `latin-ext` apart host.

---

## 8. CSS custom properties

Zelfde namen als `brandbook/tokens.css`. Dit vervangt blok 1 (merktokens) en de typografie in blok 4. Tinten en rollen leidt de bouwer zelf af. Nieuw ten opzichte van de huidige `tokens.css`: `--brand-secondary`, de CTA-tokens, `--text-h5`, `--text-h6`, `--text-button`, `--leading-snug`, `--leading-text` en `--radius-button`.

```css
:root {
  /* Merkkleuren: logo #02 "Koningsblauw & goudgeel" */
  --brand-primary: #1746A2;              /* Koningsblauw: koppen, links, iconen, blauwe banden. 8,63:1 op wit */
  --brand-primary-cmyk: "97 77 0 0";
  --brand-primary-pantone: "293 C";
  --brand-secondary: #0B2352;            /* Diepblauw: footer, donkere banden, tekst op geel. 15,26:1 met wit */
  --brand-secondary-cmyk: "98 75 1 60";
  --brand-secondary-pantone: "655 C";
  --brand-accent: #FFCC33;               /* Goudgeel: CTA, sterren, markering. Nooit tekst op wit (1,51:1) */
  --brand-accent-cmyk: "0 20 85 0";
  --brand-accent-pantone: "123 C";

  /* Neutralen */
  --ink: #0E1A33;                        /* Inkt: lopende tekst, 17,29:1 op wit */
  --ink-cmyk: "83 62 17 81";
  --ink-pantone: "282 C";
  --graphite: #2E3647;                   /* Grafiet: kaarttitels, 12,10:1 op wit */
  --graphite-cmyk: "66 49 23 71";
  --graphite-pantone: "7546 C";
  --grey-600: #5E6675;                   /* Leisteen: gedempte tekst, 5,78:1 op wit, 5,39:1 op Mist */
  --grey-600-cmyk: "50 36 22 46";
  --grey-600-pantone: "Cool Gray 10 C";
  --grey-400: #838996;                   /* Staalgrijs: randen van velden, 3,27:1 op Mist (was #8C93A0) */
  --grey-400-cmyk: "41 29 20 29";
  --grey-400-pantone: "7544 C";
  --grey-300: #D3D7DE;                   /* Zilvergrijs: decoratieve lijnen */
  --grey-300-cmyk: "20 13 11 0";
  --grey-300-pantone: "7541 C";
  --off-white: #F6F7F9;                  /* Mist: afwisselende secties */
  --off-white-cmyk: "4 2 2 0";
  --off-white-pantone: "";
  --white: #FFFFFF;

  /* Functioneel, alleen scherm */
  --error: #B42318;                      /* 6,57:1 op wit */
  --error-50: #FEF3F2;
  --success: #1E7A3C;                    /* 5,38:1 op wit; erfgenaam van het oude CTA-groen */
  --success-50: #EDF7F0;

  /* CTA-knop */
  --color-cta: var(--brand-accent);        /* #FFCC33 */
  --color-cta-text: var(--brand-secondary);/* #0B2352, 10,13:1 */
  --color-cta-hover: #F7B817;              /* goud 600; tekst blijft Diepblauw, 8,59:1 */

  /* Lettertypes */
  --font-display: "Archivo", "Arial Narrow", "Roboto Condensed", "Helvetica Neue", Arial, sans-serif;
  --font-display-stretch: condensed;     /* 75 %, altijd samen met --font-display */
  --font-sans: "Inter", ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;

  --weight-regular: 400;
  --weight-medium: 500;
  --weight-semibold: 600;
  --weight-bold: 700;
  --weight-display: 800;

  /* Typeschaal (root 16 px) */
  --text-display: clamp(2.75rem, 2rem + 3.2vw, 4.5rem);    /* 44 tot 72 px, Archivo 800 */
  --text-h1: clamp(2.5rem, 2rem + 2vw, 3.5rem);            /* 40 tot 56 px, Archivo 800 */
  --text-h2: clamp(2rem, 1.75rem + 1vw, 2.5rem);           /* 32 tot 40 px, Archivo 800 */
  --text-h3: clamp(1.5rem, 1.4rem + 0.4vw, 1.75rem);       /* 24 tot 28 px, Archivo 700 */
  --text-h4: clamp(1.25rem, 1.2rem + 0.2vw, 1.375rem);     /* 20 tot 22 px, Inter 700 */
  --text-h5: 1.125rem;                                      /* 18 px, Inter 700 */
  --text-h6: 0.875rem;                                      /* 14 px, Inter 700, hoofdletters */
  --text-lead: 1.25rem;                                     /* 20 px */
  --text-body: 1.125rem;                                    /* 18 px */
  --text-small: 1rem;                                       /* 16 px */
  --text-xs: 0.875rem;                                      /* 14 px, alleen juridisch */
  --text-button: 1.0625rem;                                 /* 17 px, Inter 700 */

  --leading-tight: 1.05;                 /* Display, H1 */
  --leading-heading: 1.15;               /* H2, H3 */
  --leading-snug: 1.3;                   /* H4 tot H6 */
  --leading-text: 1.5;                   /* intro, klein, extra klein */
  --leading-body: 1.6;                   /* lopende tekst */
  --tracking-display: 0;
  --tracking-eyebrow: 0.08em;            /* H6 en labels in hoofdletters */

  /* Vorm */
  --radius-button: 999px;                /* pil, zoals op de huidige site */
  --radius-card: 14px;
}
```

---

## 9. Regels

### Kleur

**Wel**
- Het logo in full colour alleen op Wit, Mist of de lichtste blauwe tint. Op Koningsblauw of Diepblauw altijd de negatieve versie (wit en goudgeel).
- Per scherm één ding in Goudgeel dat aandacht moet trekken: de offerteknop, de sterren of één markering.
- Blauw op licht; wit of Goudgeel op blauw; Diepblauw of Inkt op geel.
- Informatie nooit alleen met kleur overbrengen: een fout krijgt rood, een icoon én tekst.
- Zichtbare focus: Koningsblauw op licht, wit op blauw.

**Niet**
- Geen gele tekst of gele iconen op wit, en geen witte tekst op geel.
- Geen Koningsblauw op Diepblauw.
- Oude kleuren (`#054A76`, `#319C5A`, `#287EDC`) nooit naast de nieuwe blauwen.
- Geen groene knoppen: groen is alleen voor succesmeldingen.
- Geen verlopen tussen blauw en geel, en geen gele achtergrond achter een hele pagina (hoogstens één gele band per pagina).

### Typografie

**Wel**
- Archivo Condensed voor koppen, Inter voor alles wat gelezen of aangeklikt wordt.
- Koppen in zinsnaamval: "Geen verhuizing te groot", niet "Geen Verhuizing Te Groot".
- Lopende tekst op 18 px, links uitgelijnd, regels van hoogstens 68 tekens (`max-width: 68ch`).
- Prijzen, telefoonnummers en de score in Inter 600 of 700.

**Niet**
- Geen Archivo in lopende tekst of knoppen; geen Inter in grote koppen.
- Koppen niet smaller dan breedte 75 en letters nooit horizontaal vervormen. Breedte 68 hoort bij het woordmerk.
- Hoofdletters alleen in Display-regels van hoogstens 5 woorden en in H6-labels.
- Niets wat een klant moet lezen onder 16 px; 14 px alleen voor juridische regels en labels.
- Geen cursief (niet geladen): nadruk gaat met 600.
- Het logo nooit natypen in Archivo of Inter: gebruik altijd het logobestand.
- Geen derde lettertype.
