# Foto in de huisvorm op /werkwijze/, 23-09-2026

`master.png` is het goedgekeurde beeld: variant **F** uit ronde 5. Vijf rondes, elk met zijn eigen
opdracht van de gebruiker; de reviewmap met alles ertussenin staat in
`website/review/lijstplaat-dozen-20260923/` (gitignored).

Geplaatst als `img/voorbereiding-dozen.webp`, 720x405, in het `FOTO`-veld van
`_werk/blokken/lijstplaat.py`.

| Bestand | Wat |
|---|---|
| `master.png` | het gekozen beeld, 2752x1536, md5 370bd30336 |
| `master-crop-voorste-3x.png` / `-achterste-3x.png` | de belettering per doos op 3x |
| `bron-blanco-dozen.png` | dezelfde foto met blanco dozen; hier begint elke nieuwe belettering |
| `paneel-voorste-doos.png` / `paneel-achterste-doos.png` | de twee panelen zoals ze op de dozen liggen, inclusief hun lichtijking |
| `ronde-1` t/m `ronde-5.json` | de vijf rondebestanden met prompts en lagen |
| `gereedschap/` | `licht.py` meet en tint, `ronde4.py` en `ronde5.py` bouwen en plaatsen, `slotmaat.py` en `huisuitsnede.py` controleren |

## Wat het vervangt, en waarom dat het punt van de ronde was

Er stond `/img/headers/studenten.webp`. Drie dingen mis:

1. **Het was de header van een andere pagina.** `img/headers/bronnen.json` heeft hem als route
   `/diensten/studentenverhuizing/`, afgeleid van `img/dienst-woningontruiming.webp`. Precies het
   dubbelgebruik waarom `img/verwachten-inpakken.webp` eerder voor dit vak is afgewezen.
2. **Er stonden twee onbekende mensen in**, wat de notitie boven `FOTO` uitsloot.
3. **Het merk op de voorste doos was verzonnen.** Op 4x uitgesneden: het gele huis zonder
   deuropening, de armen vormeloze blauwe vlekken, en de regel die VERHUISBEDRIJF moest zijn een
   onleesbare krabbel. Precies die doos staat midden in de huisvorm-uitsnede.

De dozen in `master.png` zijn blanco gegenereerd en het merk is er naderhand met het echte
logobestand op gezet. Daarmee is wat de notitie boven `FOTO` altijd al vroeg voor het eerst
letterlijk waar.

## De twee doosvlakken

```
voorste doos    [[475,754],[1493,746],[1493,1435],[475,1399]]     1018x667 px
achterste doos  [[505,155],[1240,45],[1240,725],[505,700]]        739x612 px
```

Paneel op 85% van de vlakbreedte, dus 866 px op de voorste doos en 628 px op de achterste.
Het logo staat bij allebei in het hart van de ruimte bóven het nummer (variant D), het nummer met
zijn grondlijn op de onderrand van het paneel.

## Het licht per vlak, en waarom F de meting overrulet

`licht.py` trekt elk vlak recht en meet het apart:

| | voorste doos | achterste doos |
|---|---|---|
| gemiddelde kleur | R129 G82 B50 | R152 G106 B72 |
| luminantie | 0,351 | 0,445 |
| verloop overdwars | +6,0% | −11,5% |
| verloop omlaag | −14,2% | −8,5% |

**De val waar de eerste poging in liep:** de kleurzweem die je van een kraftdoos afmeet is die van
het KARTON, niet van de lamp. Beide vlakken lezen R1,4 / B0,6 omdat kraft bruin is; de inkt daarmee
tinten maakt het blauw bruin. Beide dozen zijn hetzelfde karton, dus wat de twee metingen
onderscheidt ís het licht. Elke meting delen door het gemiddelde van de twee geeft:

- voorste doos: kleur R1,037 G0,987 B0,946, belichting 0,882 → inkt maal **R0,915 G0,871 B0,834**
- achterste doos: kleur R0,964 G1,013 B1,057, belichting **1,118**

`merk-op-doos.py` neemt het verloop bínnen een vlak al mee via zijn luminantiekaart, maar ijkt op de
mediaan onder het merk en kan daardoor het verschil tússen twee vlakken nooit dragen. Die helft komt
hiervandaan.

**F zet de belichting van de achterste doos van 1,118 terug naar 0,882**, dus inkt maal
**R0,850 G0,893 B0,933**: 21,1% donkerder dan de meting voorschrijft, en precies even donker als de
voorste doos. Dat is een smaakkeuze van de gebruiker bovenop een correcte meting, met opzet gemaakt:
hij kreeg E (alleen de daglichtopslag eraf, 10,6% donkerder) en F naast elkaar te zien, met het
advies E te nemen omdat dat de twee dozen als twee dozen in één kamer laat lezen, en koos F. Wie dit
later "corrigeert" naar de meting draait zijn keuze terug.

## Hoe groot het op het scherm wordt, en waar het onder de norm zit

De keten: 2752 px bron -> 720 px bestand in `img/` -> de plaat neemt een venster van 425 px
(`object-fit: cover`, 535.3/509.8, `object-position: 25%`) -> getoond op de breedte van
`.b-lijstplaat__huis`.

**Die laatste breedte moet je meten, niet uit de CSS lezen.** Ik las eerst `clamp(9rem, 18vw, 15rem)`
en rekende met 144 tot 240 px; dat is een andere regel. Gemeten in de browser op de gebouwde pagina
loopt het huisje van 146 px (venster 360) tot 264 px (venster 1600 en breder), met 259 op 1440, 230
op 1280, 198 op 1100 en 208 van 600 tot 1000. Het venster van 1100 is het smalst van de brede
reeks, niet 1280: daar knijpt de beeldkolom voor de omslag naar de smalle opmaak.

Bij een huisje van B px is een bronpixel `(720/2752) x (B/425)` schermpixel.

| huisje | naam voorste doos | cijfers voorste | naam achterste doos | cijfers achterste |
|---|---|---|---|---|
| 264 px (>=1600) | 140,7 | 13,1 | 102,1 | 9,5 |
| 259 px (1440) | 138,1 | 12,8 | 100,1 | 9,3 |
| 230 px (1280) | 122,6 | 11,4 | 88,9 | 8,3 |
| 208 px (600-1000) | 110,9 | 10,3 | 80,4 | 7,5 |
| 198 px (1100) | 105,6 | 9,8 | 76,6 | 7,1 |
| 176 px (480) | 93,8 | 8,7 | 68,0 | 6,3 |
| 161 px (390) | 85,8 | 8,0 | 62,2 | 5,8 |
| 146 px (360) | 77,8 | 7,2 | 56,4 | 5,2 |

Het brandbook vraagt 100 px voor het logo mét naam. **De voorste doos haalt dat tot en met een
huisje van 198 px, dus op alle vensters van 600 px en breder; de achterste doos haalt het alleen op
1440 en breder, en dan nog net.** Onder die grenzen is de naam decoratie en geen tekst.

Dat is geen omissie. In ronde 2 kreeg de gebruiker die rekensom voorgelegd, met het voorstel om op
de achterste doos alleen het beeldmerk te zetten (dat haalt 49,6 px op 240 en blijft overal boven de
32 px die het brandbook voor het beeldmerk vraagt). Hij heeft in ronde 4 uitdrukkelijk gevraagd om
op beide dozen precies dezelfde belettering. Hij koos met de getallen in de hand. Haal de naam er
dus niet alsnog af.

Wat wél helpt als het ooit moet: de doos groter en vlakker in beeld. Dat is de enige knop die
werkt, en het is de reden dat ronde 2 de doos al 61% breder maakte dan ronde 1 (vlak van 631x832
naar 1018x667).

## Een volgende ronde

- Andere belettering op dezelfde dozen: begin bij `bron-blanco-dozen.png`, houd de hoekpunten
  hierboven aan, draai `ronde5.py` met een ander paneel. Niets opnieuw genereren.
- Een andere foto voor dit vak: het onderwerp moet links van het midden en laag staan, want de
  uitsnede begint links en de huisvorm snijdt de bovenhoeken weg. `gereedschap/huisuitsnede.py`
  laat zien wat de plaat er werkelijk van toont; beoordeel nooit op de 16:9-foto zelf.
- `merk-op-doos.py` meldt "merk op karton 90,4%" op de voorste doos. Dat is de kartondetector die
  op de donkere onderhelft van dat vlak reageert; "binnen het vlak" is 100% en de 3x-uitsnede is
  schoon.
