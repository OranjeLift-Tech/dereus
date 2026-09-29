# Echte voorwerpen op de contactkaarten (/contact/, 29-09-2026)

De vier kanaalkaarten (Bel ons, Mail ons, Stuur een bericht, Vraag een offerte aan) hadden klei-iconen
(`img/clay/`). De gebruiker vond die "te AI, gemaakt" en wilde iets echts. Nu staan er vrijstaande foto's:

| kaart | bestand | bron |
|---|---|---|
| Bel ons | `img/contact-echt/telefoon-240/480.webp` | Unsplash dBESAHgPL6c + belscherm van De Reus |
| Mail ons | `img/contact-echt/envelop-216/432.webp` | Unsplash ehI8qokwP7s + briefkaart met logo |
| Stuur een bericht | `img/contact-echt/klembord-136/272.webp` | Unsplash UEQedPdLXVU + contactformulier met logo |
| Offerte | `img/contact-echt/dozen-166/307.webp` | uitsnede uit `img/voorbereiding-dozen.webp` |

Licenties: `img/LICENTIES.md`, kop `img/contact-echt/*.webp`.

## Stappen

Nodig in een losse map (niet in de repo): `npm i @imgly/background-removal-node playwright-core`, daarna
`npm install-scripts approve onnxruntime-node sharp` en `npm rebuild onnxruntime-node sharp`.

1. `node knip.mjs bron/<id>.jpg` - achtergrond weg (imgly, model medium) -> `uit/<id>-vrij.png`.
2. `node masker.cjs <bron> <vrij.png> <naam>-m.png [lichtgrens] [doorlaat]` - imgly maakt witte vlakken half
   doorzichtig (scherm, kaart, papier). Dit script vult ze weer: gaten dicht vanaf de rand gezien, voor de
   briefkaart ook alles lichter dan 249 (lichtgrens), voor het klembord doorlaat 250. Daarna bijgesneden.
3. `node vlak.cjs <naam>-m.png <x> <y> <grens> <masker.png>` - het witte vlak (scherm/kaart/papier) als masker
   en zijn vier hoeken (rechte lijnen door de randen, dus scherpe hoeken ook bij afgeronde schermhoeken).
   `RECHT=1` voor een vlak dat recht staat (klembord).
4. `node samenstel.cjs` - zet belscherm, briefkaart en formulier in perspectief op de foto (matrix3d, multiply,
   zodat papier en glas van de foto blijven), in headless Chrome -> `uit/<naam>-klaar.png`.
5. Met sharp naar WebP op 1x en 2x van de weergavemaat van ontwerp 05 "Gele schijf": telefoon 240 breed,
   envelop 216 breed, klembord 218 hoog, dozen 205 hoog (2x hoogstens de bron: 378). De breedtes staan in VOORWERP in
   `_werk/blokken/contactkaarten.py`; de maat op de kaart in `css/blok/contactkaarten.css` (blok 29-09-2026).

De scripts verwachten `bron/` en `uit/` naast zich. De paden naar logo en lettertypes in `samenstel.cjs` wijzen naar
de repo.

## Ontwerp

Live staat ontwerp 05 "Gele schijf" uit `_ontwerpen/contactkaarten-echt-varianten.html` (29-09-2026): witte kaart,
voorwerp groot en gecentreerd op een dikke goudgele schijf. De eerste, kleine versie op het gele huis vond de
gebruiker "klein en flets".

## Punaise en wekker (/contact/ #kaart, 29-09-2026)

"Zo vindt u ons" had lijniconen (pin, klok) in kleine gele tegels. De gebruiker: "ikonları daha gerçekçi yap ve bi tık
o kutudan çıkıyor gibi olsun". Nu staan er twee echte voorwerpen in een dik goudgeel blok, die boven de tegel uitsteken:

| regel | bestand | bron |
|---|---|---|
| Hoofdkantoor | `img/contact-echt/punaise-44/88.webp` | Unsplash 46Tg56viOUg, de blauwe punaise bij Stoke-on-Trent |
| Bereikbaar | `img/contact-echt/wekker-48/96.webp` | Unsplash flpCsXSVgoo, zilveren wekker |

Werkwijze: punaise eerst uitgesneden uit het origineel van 3534 px (x 1131-1484, y 35-441), dan `knip.mjs`; wekker
direct `knip.mjs`. Daarna de alfa hard gemaakt (a<40 weg, a>215 dicht, ertussen lineair), `trim`, resize naar 1x/2x
met `sharpen({sigma:.5})`, WebP q90. Tussenresultaten: `uit/punaise-klaar.png`, `uit/wekker-klaar.png`.
Maat en plaats: VOORWERP in `_werk/blokken/kaart.py`, CSS in `css/blok/kaart.css` (blok "echte voorwerpen in de gele
tegels"). De punaise krijgt `brightness(1.28)`, anders verdwijnt de kop in het Diepblauw.

## Werkgebied en Zo werken wij (home, /over-ons/, 29-09-2026)

De gebruiker: "bu bölümdeki figürleri de gerçek ve kutudan çıkacakmış gibi yap" (home #werkgebied) en daarna hetzelfde
voor /over-ons/ "Zo werken wij". Beide blokken hadden lijniconen in gele tegels; nu staat er in elke tegel een echt
voorwerp, net als bij de punaise en de wekker hierboven. Het werkgebied staat ook op /over-ons/ #den-haag.

| blok, regel | icoon | bestand | bron |
|---|---|---|---|
| werkgebied, Den Haag | pin | `punaise-44/88` | zelfde als /contact/ #kaart |
| werkgebied, Nederland | vrachtwagen | `bakwagen-96/192` | uitsnede uit `img/footer-wagen-breed.webp` (eigen beeld) |
| werkgebied, buitenland | wereld | `wereldbol-58/116` | Unsplash 9tmrYLRL7Ww |
| kernwaarden, zware werk | doos | `dozen-58/116` | zelfde uitsnede als de kanaalkaart, kleiner |
| kernwaarden, netjes neer | schild | `plant-62/124` | Unsplash 2LlRY-bMmig |
| kernwaarden, afspreken | klok | `wekker-48/96` | zelfde als /contact/ #kaart |
| kernwaarden, prijs | euro | `munten-80/160` | Unsplash OApHds2yEGQ, de twee rechter stapels |
| kernwaarden, meedenken | persoon | `headset-53/106` | Unsplash dJ2hnNSqsmk |

Werkwijze: de bron eerst met sharp naar PNG (in een eigen proces), dan `vrij.mjs` (alleen imgly; imgly en sharp in één
proces laten Node soms vallen), dan `masker.cjs`. Voor de bakwagen met lichtgrens 236 (de witte laadbak), voor de
headset en de plant met `GEEN_VUL=1` (gaten binnen de beugel en tussen de bladeren zijn echt leeg). Daarna:
- plant: `pot-dicht.cjs <m.png> <uit.png> 0.625` zet alleen de pot dicht (randen gemeten onder de bladeren);
- headset: `headset-merk.cjs <in.png> <uit.png>` poetst het merkteken op de oorschelp weg;
- munten: vanaf x 955 van de uitsnede, zodat alleen de twee goudkleurige stapels overblijven.
Export: alfa hard (a<40 weg, a>215 dicht), `trim`, resize naar 1x/2x met `sharpen({sigma:.5})`, WebP q90, alfa q95.
Tussenresultaten in `uit/*-klaar.png`. De plakbandhouder (p10qtOive_E) is geprobeerd en afgevallen: op tegelformaat
las hij als een rode vlek.

Maat en plaats: VOORWERP in `_werk/blokken/werkgebied.py` en `kernwaarden.py`; CSS in de blokken "echte voorwerpen in de
gele tegels" onderaan `css/blok/werkgebied.css` en `css/blok/kernwaarden.css`. De bakwagen is 5.2rem breed en pas vanaf
1280 px 5.6rem (dan steekt hij links verder uit); smaller raakte hij de schermrand.
