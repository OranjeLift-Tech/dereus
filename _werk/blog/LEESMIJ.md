# Verhuisblog

De blog op `/blog/`: een overzicht en 9 artikelen. Hij staat los van `build.py`: `node _werk/blog/bouw-blog.cjs` bouwt hem, en die schrijft alleen in `blog/`.

## Wat komt van de site

Kop, lade, voet, snelbalk, iconen, de paginakop met offertekaart (`.pk` + `.pk-pil`, alleen tekst en foto vervangen) en het offerteblok (`b-offertepil`) haalt het script letterlijk uit een gebouwde pagina, standaard `kosten/index.html`. Een andere bronpagina kan als argument: `node _werk/blog/bouw-blog.cjs contact/index.html`.

De opmaak komt uit `/css/min/site.min.css`, `kop.min.css` en `offertepil.min.css`. Die schrijft `build.py` nog steeds, naast de paginabundels. Het gedrag komt uit `/js/site.js`.

Verandert de header of footer van de site na een build, draai dit script dan opnieuw. Dan lopen kop en voet weer gelijk en kloppen de `?v=`-hashes.

## Waar staat wat

| Pad | Wat |
|---|---|
| `_werk/blog/inhoud/site.cjs` | Bedrijfsgegevens (gelijk aan `config.py`), de schrijver, de tipgevers en de onderwerpen |
| `_werk/blog/inhoud/artikelen.cjs` | De artikelen; `tekst(h)` gebruikt de bouwstenen uit `bouw-blog.cjs` |
| `_werk/blog/inhoud/beeldmaten.json` | De omtrek van elke uitsnede; daaruit volgt hoe ver iemand uit de foto stapt |
| `blog/blog.css`, `blog/blog.js` | De opmaak en het gedrag van de blog zelf (bron, geen bouwresultaat) |
| `blog/img/foto` + `blog/img/uit` | De foto en de uitsnede, altijd als paar met hetzelfde formaat |
| `blog/img/voorwerp`, `team`, `sfeer` | Voorwerpen op de gele schijven, tipgevers, sfeerfoto |

## Huisregels in de tekst

- De tekst gebruikt "u" en bevat geen gedachtestreepjes. Het script waarschuwt als dat misgaat.
- Er staan geen bedragen in, geen vaste eindprijs, geen "volledig verzekerd" en geen opslagfeiten die in `config.py` nog `None` zijn.
- Medewerkers worden nergens bij naam genoemd. De mensen op de foto's zijn modellen van Pexels (vrij te gebruiken, zie `BRONNEN-zwaluw.md`). Ze staan er dus zonder naam.

## Nog niet gedaan

- `/blog/` staat sinds 30-09-2026 in het hoofdmenu (`website/content/gedeeld.md` + `navigatie.py`). De build laat de link toe via `kit.BUITEN_BUILD`; `bewakers.py` controleert dan alleen dat `blog/index.html` bestaat. In de footer en `sitemap.xml` staat de blog nog niet.
- Het beeld is nog geen eigen De Reus-foto. Een nieuwe foto heeft een uitsnede van hetzelfde formaat nodig, plus een regel in `beeldmaten.json`: `r` (hoogte/breedte), `s` (bovenkant van het onderwerp), `cx` (midden van de bovenkant), `l`, `rr` en `e`.
