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
