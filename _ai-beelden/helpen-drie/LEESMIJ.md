# helpen-drie: de drie verhuizers bij "Zo helpen wij u snel" (/contact/)

Gemaakt op 28-09-2026. Uitvoer: `img/helpen-drie-uit.webp` (685 x 591, alfa), gebruikt via de optie
`figuur` van het blok formulier in `_werk/paginas/contact.py`.

Geen nieuwe generatie: alleen bestaande beelden uit de repo.

1. `merk.js`: haalt op `img/contact-adviseur-uit.webp` de door AI getekende borstprint weg (geel, met
   verzonnen tekst) door stof van 52 px lager in te zetten, en zet het echte merk
   `img/logo/dereus-beeldmerk-negatief.svg` erop volgens `gereedschap/MERK-OP-KLEDING.md`: 42 px breed
   (16,5% van 257 px schouder), midden op x 379 (knooplijst 322 + 0,22 x schouder), y 231 (onderste knoop),
   luminantie van de stof overgenomen, fijne korrel, alfa terug uit het origineel. Schrijft `adviseur-merk.png`.
2. `groep.js`: knipt uit `img/team/team-hero-1600.webp` de man met de dozen (grens = rechterrand van de
   dozen) en de blonde man met de deken (hij staat voor de middelste man; de grens valt achter de adviseur),
   schaalt ze naar 0,95 van de adviseur met de voetlijn 25 px hoger, zet ze erachter met een zachte
   slagschaduw van de adviseur, en knipt af op 62% van zijn lengte (de rest ligt achter het blauwe paneel).
   De middelste man uit team-hero is niet gebruikt: dozen en buurman dekken hem aan beide kanten af.

Draaien: `canvas.cjs` opent een pagina op een lokale server (`BASIS`, standaard http://127.0.0.1:8767) met
de repo als root, voert het script in Edge uit en schrijft de bestanden weg. `groep.js` leest
`/_tmp/adviseur-merk.png`: zet de uitvoer van stap 1 daar neer (of pas het pad aan).

    PLAYWRIGHT=<pad-naar-playwright> MSYS_NO_PATHCONV=1 node canvas.cjs merk.js .
    PLAYWRIGHT=<pad-naar-playwright> MSYS_NO_PATHCONV=1 node canvas.cjs groep.js .

`groep.webp` (kwaliteit 0,9) is daarna `img/helpen-drie-uit.webp`. Controleer het merk altijd op 4x
(`merk-voor-na-4x.png`).
