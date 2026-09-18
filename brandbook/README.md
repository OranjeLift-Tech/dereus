# Merkboek Verhuisbedrijf De Reus

Het merkboek van Verhuisbedrijf De Reus, in een compacte webeditie. Hierin staat wat u nodig heeft om de website te bouwen of er teksten voor te schrijven: het logo, de kleuren en letters, de webcomponenten, het beeld en de schrijfstijl.

**Status:** v1.1, compacte webeditie, september 2026, met het nieuwe logo (grotere biceps, zonder tagline).

## Openen

- **In de browser:** open `index.html`. Het werkt ook zonder internet.
- **Als PDF:** `Merkboek-De-Reus-v1.1.pdf` (A4, om te lezen of te delen).

## Wat staat waar

| Pad | Wat het is |
|---|---|
| `index.html` | Het merkboek |
| `Merkboek-De-Reus-v1.1.pdf` | Hetzelfde merkboek als PDF |
| `tokens.css` | Kleuren, lettertypes, maten, ruimte en vorm als CSS-variabelen |
| `book.css`, `book.js` | Opmaak en gedrag van het merkboek zelf |
| `assets/logo/` | Alle logobestanden, SVG en PNG, met een eigen `README.md` |
| `assets/imagery/` | De acht diensticonen (SVG) |
| `assets/fonts/` | Archivo Condensed en Inter (woff2), met de licenties |
| `assets/mockups/` | De mockups uit het boek: de verhuiswagen en de websiteheader |

## Welk logobestand waarvoor

| Bestand in `assets/logo/` | Gebruik |
|---|---|
| `dereus-logo.svg` | Primair logo, op wit of licht. Websiteheader, documenten |
| `dereus-logo-negatief.svg` | Op koningsblauw en diepblauw, zoals de footer |
| `dereus-logo-horizontaal.svg`, `-negatief.svg` | Alleen waar weinig hoogte is. Ter goedkeuring door de klant |
| `dereus-beeldmerk.svg`, `-negatief.svg` | Social avatar en kleine plekken, vanaf 32 px |
| `dereus-favicon.ico`, `.svg` | Browsertab |
| `dereus-favicon-180.png`, `-512.png` | `apple-touch-icon` en webmanifest |
| `.png` met dezelfde naam | Voor mail en Office (2048 px breed, transparant) |

## Kleuren en letters in het kort

| Naam | HEX | Token | Gebruik |
|---|---|---|---|
| Koningsblauw | `#1746A2` | `--brand-primary` | Koppen, links, iconen, blauwe banden |
| Diepblauw | `#0B2352` | `--brand-secondary` | Footer, tekst op de gele knop |
| Goudgeel | `#FFCC33` | `--brand-accent` | De offerteknop, sterren, één markering per scherm |
| Inkt | `#0E1A33` | `--ink` | Lopende tekst |
| Mist | `#F6F7F9` | `--off-white` | Panelen en afwisselende secties |

- **Koppen:** Archivo Condensed, 800 en 700 (`--font-display`).
- **Tekst en knoppen:** Inter, 400, 600 en 700 (`--font-sans`).
- **Lopende tekst:** 18 px (`--text-body`).

### tokens.css gebruiken

Laad `tokens.css` vóór uw eigen CSS en gebruik de variabelen in plaats van losse waarden:

```html
<link rel="stylesheet" href="brandbook/tokens.css">
```

```css
.knop-offerte {
  background: var(--color-cta);
  color: var(--color-cta-text);
  border-radius: var(--radius-button);
  font: var(--weight-bold) var(--text-button) var(--font-sans);
}
.knop-offerte:hover { background: var(--color-cta-hover); }
```

`tokens.css` laadt de lettertypes uit `assets/fonts/`, relatief ten opzichte van zichzelf. Kopieert u het bestand naar een andere map, neem dan `assets/fonts/` mee of pas de paden in de `@font-face`-regels aan.

## De regels in acht punten

1. **Eén slogan per blok.** "Geen verhuizing te groot!" is de slogan, los van het logo, altijd met uitroepteken. "Sterk in verhuizen. Zorgeloos geregeld." is de afsluiter voor de footer. Nooit samen.
2. **Op blauw altijd het negatieve logo.**
3. **Minimale maten op scherm:** logo 100 px breed, horizontaal logo 28 px hoog, beeldmerk 32 px, favicon 16 px.
4. **Geel nooit als tekst op wit.** Een gele knop is er alleen voor "Offerte aanvragen", hooguit één per blok.
5. **Altijd u en uw,** nooit je, jij of jouw.
6. **Geen gedachtestreepjes,** lang of kort. Gebruik een komma, punt of dubbele punt.
7. **Geen onbevestigde feiten.** Gebruik alleen de feiten uit hoofdstuk 01 van het merkboek: geen keurmerken, oprichtingsjaar of beloftes die niet waar te maken zijn.
8. **"Standaard verzekerd",** nooit "volledig verzekerd".

## Mockups en drukwerk

De mockups in `assets/mockups/` zijn gegenereerde voorbeelden: een voorstel voor de belettering van de wagen en het eerste scherm van de website. De scripts die ze maken en de drukbestanden (CMYK) horen niet bij deze webeditie. Drukklare bestanden van het nieuwe logo moeten nog gemaakt worden. Vraag ze aan voordat er iets gedrukt of beletterd wordt.

## Rechten

- **Logo, naam, merkteksten en mockups:** eigendom van Verhuisbedrijf De Reus. Gebruik ze alleen voor De Reus en verander het logo niet.
- **Diensticonen in `assets/imagery/`:** gemaakt voor De Reus, alleen voor gebruik door De Reus.
- **Lettertypes:** Archivo en Inter staan onder de SIL Open Font License 1.1, zie `assets/fonts/OFL-Archivo.txt` en `assets/fonts/OFL-Inter.txt`.
- **Interface-iconen in het boek** (telefoon, mail, pijl, melding): Lucide, ISC-licentie.

## Contact

Verhuisbedrijf De Reus · Lau Mazirellaan 336, 2525 ZJ Den Haag · 085 000 5647 · info@verhuisbedrijfdereus.nl · www.verhuisbedrijfdereus.nl
