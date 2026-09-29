# na-bericht-boog: de klantenservice in de witte boog (/contact/ #na-bericht)

Gemaakt op 29-09-2026. Uitvoer: `img/contact-klantenservice-boog-uit.webp` (850 x 730, alfa), gebruikt in
`_werk/blokken/na-bericht.py` (optie `beeld="boog"`, constante `BOOG`). Opzet zoals "Na uw aanvraag" bij
referentie A: persoon zonder kamer in een lichte boog met een dunne binnenlijn, die op de onderrand van de band
staat (css: blok "Beeld boog" in `css/blok/na-bericht.css`).

Geen nieuwe generatie, alleen bestaande beelden, zelfde werkwijze als `../na-bericht-bureau/`:

- de vrouw uit `img/contact-klantenservice-uit.webp`;
- uit `img/contact-klantenservice-foto.webp` (zelfde 1200 x 800-raster) een veelhoek met het bureau, het
  schrijfblok en de kop. Bovenrand van het bureau op y 522; rechts houdt alles op bij x 945, net rechts van de
  kop: scherm, toetsenbord en telefoon vallen weg, zodat het beeld binnen de boog past;
- de lichte vlek links onder (zitting van de stoel) en de halfdoorzichtige donkere waas onder haar rug zijn weg;
- uitsnede x 95-945, y 0-730: 40 px lucht links van haar rug, kruin op y 50, onderkant door het bureaufront.
  Met de boog op precies deze maat (ronding = halve breedte) blijven haar rug, haar knot en de kop binnen de
  ronding.

Draaien met de canvas-harnas van `../helpen-drie/canvas.cjs` (een server op de repo, standaard poort 8767):

    PLAYWRIGHT=<pad-naar-playwright> MSYS_NO_PATHCONV=1 node ../helpen-drie/canvas.cjs boog.js .

Dat schrijft `contact-klantenservice-boog-uit.webp` (kwaliteit 0,9, naar `img/` kopiëren) en
`boog-voorbeeld.png` (op Diepblauw in een witte boog en op een dambord, alleen om te kijken).
