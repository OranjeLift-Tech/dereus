# Achtergronden per pagina

`manifest.json` koppelt alle 27 pagina's aan een eigen achtergrond. De twaalf livepagina's gebruiken elk een andere fotoscène. De acht werkgebiedpagina's gebruiken de bestaande, afzonderlijke kaarten; zeven concept-dienstpagina's gebruiken verschillende bestaande dienstfoto's.

## Herkomst en keuzes

- Vijf nieuwe foto's zijn met de ingebouwde imagegen gemaakt: `home`, `kosten`, `privacy`, `offerte-bedankt` en `niet-gevonden`. De prompts staan in `PROMPTS.md`; de volledige PNG-masters in `_ai-beelden/foto/header-achtergronden/`.
- De gebruiker koos uitsluitend foto 2 uit `beeld-opties/werknemers-nieuw-20260918/`: deze inpakscène is gebruikt voor `/over-ons/`. De vier afgewezen opties en de oudere aparte opties zijn niet gebruikt.
- De overige foto's komen uit bestaande sitebeelden of de gecontroleerde masters van de logocorrecties. De precieze bron per route staat in `bronnen.json`.
- De oude Wix-hero (`hero-bg-1920.webp` en `hero-verhuizers.jpg`) is niet gebruikt wegens de eerder vastgelegde herkomstbeperking.
- De kaartachtergronden zijn kopieën van de bestaande plaatskaarten. Er zijn geen plaatselijke gebouwen of herkenningspunten gegenereerd.

## Techniek en controle

De nieuwe foto's zijn 1600 × 900 pixels. Bestaande foto's zijn op maximaal hun oorspronkelijke breedte uitgevoerd; er is geen extra detail door opschalen gesuggereerd. De drie bestaande stapfoto's op livepagina's blijven 560 × 315 pixels en zijn bewust zacht uitgevoerd voor gebruik onder de donkere koplaag. De concept-dienstfoto's die alleen klein beschikbaar zijn blijven 720 × 405 pixels. Alle werkelijke afmetingen staan in het manifest.

De foto's zijn als WebP met kwaliteit 84 geëxporteerd. Nieuwe foto's en gebruikte bronfoto's zijn visueel bekeken op storende logo's, ongewenste tekst en bruikbare uitsneden. Alle 27 bestanden bestaan en hebben onderling verschillende SHA-256-hashes. Controle van tekstcontrast en de uiteindelijke header gebeurt in de gedeelde paginatest, omdat de blauwe afdeklaag door CSS wordt toegevoegd.

`maak.cjs` maakt de exports opnieuw vanuit `bronnen.json`. Het script gebruikt de geïnstalleerde Sharp-runtime en wijzigt geen bronfoto's.

## De home: een bewegende collage (28-09-2026)

Sinds 28-09-2026 staat achter de hero van de home een collage van vier beelden die na elkaar bewegen (`_werk/blokken/herocollage.py`). De gebruiker keurde beeld 2, 4, 5 en 6 uit `website/review/hero-collage-20260928/` goed; `home.webp` hoort daar niet bij. Het eerste beeld, `home-collage-1-dragen-stoep.webp`, is de manifestregel voor `/`; de andere drie staan in `herocollage.py`. Alle vier zijn kopieën van bestaande sitebeelden (`verhuisdag-dragen-stoep`, `dienst-verhuislift`, `footer-wagen`, `dienst-nationaal-v2-groot`), op maximaal 1280 breed en WebP q50, gemaakt met `maak-collage.cjs`. Het formaat is 4:3, niet 16:9, en de lift blijft 720 breed.

Let op: `maak.cjs` kent de collage niet. Wie het draait, zet `/` in het manifest terug op `home.webp`; zet daarna de regel voor `/` hier weer terug.

## /diensten/: een lichtere kop (29-09-2026)

Sinds 29-09-2026 wijzen `/diensten/` en de zeven concept-dienstpagina's in het manifest naar `diensten-licht.webp`. Dat is dezelfde uitsnede van `werk-straat.png` op 1600 × 900, maar als WebP q60 in plaats van q84: 99 KB in plaats van 176 KB. Een kleinere breedte voor de telefoon helpt hier niet, want daar staat de kop ongeveer 950 CSS-pixels breed. De vergelijking oud tegen nieuw staat in `website/review/mobiel-beelden-20260929/`. Het bestand komt uit `_werk/beeldvarianten.py` (de tabel `LOS`), niet uit `maak.cjs`. `diensten.webp` wordt daarna niet meer gebruikt.

Let op: `maak.cjs` zet ook deze regels terug op `diensten.webp`.
