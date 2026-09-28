# na-bericht-bureau: de klantenservice aan haar bureau (/contact/ #na-bericht)

Gemaakt op 28-09-2026. Uitvoer: `img/contact-klantenservice-bureau-uit.webp` (1060 x 690, alfa), gebruikt in
`_werk/blokken/na-bericht.py`. Opzet zoals de contactkop van referentie A: persoon met bureau en scherm,
zonder kamer, onderaan ronde hoeken (css), en een grote duim ernaast.

Geen nieuwe generatie, alleen bestaande beelden:

- de vrouw uit `img/contact-klantenservice-uit.webp`;
- uit `img/contact-klantenservice-foto.webp` (zelfde 1200 x 800-raster) een veelhoek met het bureau, de kop,
  het schrijfblok, het toetsenbord, de telefoon, de papieren en het scherm. De bovenrand van het bureau ligt
  op y 522 (net onder de vensterbank), de linkerrand van het scherm loopt van (1066, 62) naar (1051, 492);
- de lichte vlek links onder (armleuning van de stoel die in de uitsnede bleef hangen) is weggehaald;
- uitsnede x 140-1200, y 40-730: kruin bijna tegen de bovenrand, onderkant door het bureaufront.

Draaien met de canvas-harnas van `../helpen-drie/canvas.cjs` (zelfde helpers `laad`, `doek`, `bewaar`):

    PLAYWRIGHT=<pad-naar-playwright> MSYS_NO_PATHCONV=1 node ../helpen-drie/canvas.cjs bureau.js .

`contact-klantenservice-bureau-uit.webp` (kwaliteit 0,9) is daarna het bestand in `img/`.
