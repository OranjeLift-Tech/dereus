# Het merk op een doos zetten

`merk-op-doos.py` zet het echte beeldmerk van De Reus op een onbedrukt dooszijvlak in een
gegenereerd beeld. Het merk gaat nooit in de prompt naar het beeldmodel, want dat tekent een
logo na in plaats van het te plaatsen; dit script is het "achteraf" waar die regel om vraagt.

`hoekraster.py` staat ernaast en helpt je de vier hoekpunten aflezen.

## In twee stappen

**1. De vier hoekpunten aflezen.** Zet een raster over de doos:

```
python hoekraster.py versie-1.png --vak "620,260 900,500"
```

Dat schrijft `versie-1-raster.png`: het vak vergroot, met de coordinaten van het
originele beeld erover. Lees de vier hoeken van het vlak af waar het merk op komt.

**2. Het merk erop zetten.**

```
python merk-op-doos.py versie-1.png --hoeken "663,331 866,297 861,441 669,452"
```

Schrijft `versie-1-merk.png` en `versie-1-merkcrop.png` (het merkgebied op minimaal 3x,
om te lezen of het merk klopt). Voeg `--debug` toe en je krijgt er `versie-1-merkvlak.png`
bij, met het opgegeven vlak als rode vierhoek over het resultaat: daarmee zie je in een
oogopslag of je hoekpunten kloppen.

## Een hele ronde in een keer

Zet de vlakken in een platte lijst, zoals de `jobs.json` van de archiefreeksen:

```json
[
  {"bron": "versie-1.png",
   "hoeken": [[663,331],[866,297],[861,441],[669,452]]},
  {"bron": "versie-2.png", "breedte": 0.42, "variant": "beeldmerk",
   "hoeken": [[732,1002],[1505,984],[1502,1460],[745,1500]]}
]
```

```
python merk-op-doos.py --vlakken vlakken.json --uit-map ../uit
```

Paden in het json staan relatief aan het json zelf. `variant`, `breedte`, `midden` en
`logo` horen bij het merk en niet bij de ronde: ze staan als standaard in het script en zijn
per job te overschrijven, zodat ze niet in elk rondebestand uit elkaar gaan lopen.

## De hoekpunten

Met de klok mee vanaf linksboven: **linksboven, rechtsboven, rechtsonder, linksonder**,
van het vlak waar het merk op komt. Een andere volgorde geeft een omgeklapt merk, dus
het script weigert een vierhoek die niet bol is.

Een paar pixels mis is geen ramp. Het merk staat gecentreerd op het vlak en op de helft
van de breedte, dus het valt ruim binnen de randen.

## Wat het script meldt

```
vlak 199x133 px   merk 100x82 px (50% van de doosbreedte)
merk op karton 99.9%   binnen het vlak 100.0%   schaduw 0.91-1.20x
```

- **merk op karton** onder de 90%: er ligt een hand, een band of een rand voor het merk.
  Verklein `--breedte` of verschuif `--midden`.
- **schaduw**: hoeveel het karton het merk donkerder en lichter maakt. Blijft dat rond
  1.00x, dan is de doos vlak belicht en zie je weinig verloop. Dat is geen fout.
- Wordt het merk **smaller dan 100 px**, dan loopt de naam dicht en waarschuwt het
  script. Neem dan `--variant beeldmerk`: alleen de armen en het huis, zonder naam.
  Dat is wat het brandbook voor kleine plekken voorschrijft (vanaf 32 px).

## Knoppen

| | |
|---|---|
| `--variant logo` \| `beeldmerk` | armen, huis en naam, of alleen armen en huis. Standaard `logo` |
| `--breedte 0.50` | breedte van het merk als deel van de doosbreedte. Afgesproken 0.45-0.55 |
| `--midden 0.5,0.5` | het middelpunt op het vlak in u,v (0-1). Standaard het hart |
| `--korrel 0.3` | kartonkorrel over het merk. Op 0 wordt het een schone sticker |
| `--zacht 0.8` | verzachting van de merkrand |
| `--schaduw 5` | venster van de luminantiekaart |
| `--crop-schaal 3` | minimale vergroting van de merkcrop |

Het merk komt uit `brandbook/assets/logo/`: het kleurenmerk (blauw en geel), versie 2 van
september 2026, zonder tagline. Niet de negatieve variant, die is voor blauw.

## Hoe het werkt

Het logo wordt via een projectieve afbeelding naar de vier hoekpunten getrokken, met
drievoudige supersampling zodat de randen recht en zacht blijven. Daarna wordt het
vermenigvuldigd met de luminantie van het karton eronder, 5x5 gladgestreken en geijkt op
de mediaan onder het merk. Zo houdt het merk zijn eigen helderheid, maar neemt het het
verloop en de ribbels van de doos over. Tot slot gaat de korrel van het karton er
overheen. Zonder die twee stappen ligt het merk als een sticker op het beeld.

## Hoe het werkt

Het logo wordt via een projectieve afbeelding naar de vier hoekpunten getrokken, met
drievoudige supersampling zodat de randen recht en zacht blijven. Daarna wordt het
vermenigvuldigd met de luminantie van het karton eronder, 5x5 gladgestreken en geijkt op
de mediaan onder het merk. Zo houdt het merk zijn eigen helderheid, maar neemt het het
verloop en de ribbels van de doos over. Tot slot gaat de korrel van het karton er
overheen. Zonder die twee stappen ligt het merk als een sticker op het beeld.

Python met numpy, PIL en scipy, geen node: dit draait na de generatie op een bestand dat er
al is, en deelt dus geen code met de generatoren.

## Bewezen op

Vier dozen: twee uit de ronde twee-verhuizers en twee uit de afgekeurde doosronde, waaronder
een vlak in scherp perspectief. De proefbeelden staan in
`website/review/drie-verhuizers-doos-20260922/`.
