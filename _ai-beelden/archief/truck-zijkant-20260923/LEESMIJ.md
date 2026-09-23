# Vrachtwagen met belettering, 23-09-2026

`master.png` is het goedgekeurde beeld: variant **D** uit ronde 3. De gebruiker koos hem met
"Versie 5: D version", nadat hij in ronde 1 versie 5 had gehouden, in ronde 2 de maat van het
nummer (B) en in ronde 3 de plek van het logo.

De reviewmap met alle vijf de wagens en alle tussenstappen staat in
`website/review/truck-zijkant-20260923/` (gitignored). Hier staat alleen wat een volgende ronde
nodig heeft.

| Bestand | Wat |
|---|---|
| `master.png` | het gekozen beeld, 2528x1696, md5 5353dd2487 |
| `master-crop-3x.png` | de belettering op 3x, om te lezen dat het merk en het nummer kloppen |
| `bron-blanke-flank.png` | dezelfde foto met een lege flank, md5 0569ecfd48; hier begint elke nieuwe belettering |
| `paneel-D.png` | het beletteringspaneel zoals het op de flank ligt, sleet en al |
| `ronde-1/2/3.json` | de drie rondebestanden, met de prompts en de lagen van de reviewpagina |
| `gereedschap/` | de scripts; `ronde3.py` maakt paneel en composiet in één keer |

## De route: blanke flank, belettering erna

Het merk ging nooit in het prompt. De wagens zijn gegenereerd met een **volledig lege witte
flank** (een `TRUCK OVERRIDE` in de `extra` van het rondebestand die de vaste regel "nooit een
leesbaar zijpaneel" buiten werking zet, plus de sleetregel in twee helften zodat een lege flank
niet fabrieksnieuw terugkomt). Daarna is het echte beeldmerk er met `merk-op-doos.py` op gelegd.

Reden: het nummer moest exact `085 000 5647` zijn, en kleine letters op een flank zijn precies wat
het model onleesbaar maakt. De naam is nooit opnieuw gezet; die komt als outline uit
`brandbook/assets/logo/dereus-logo-horizontaal.png`, conform het brandbook. Alleen het nummer is
echte tekst: Archivo ExtraBold uit `brandbook/assets/mockups/_bron/fonts/Archivo-VF.ttf`, in
koningsblauw `#1746A2`, met 16 px letterspatiering.

## De hoekpunten van de flank

```
[[1465,186],[2262,345],[2257,1043],[1480,1110]]
```

Met de klok mee vanaf linksboven. Bovenrand langs de naad onder de dakrand, onderrand op de
bovenkant van de stootlijst, zijkanten op de hoekstijlen.

**Ronde 1 had hier de grootste fout van de hele reeks.** Toen stonden er met de hand afgelezen
hoekpunten `[[1454,253],[2250,360],[2250,1049],[1454,1106]]`: beide zijkanten verticaal gedwongen
en een bovenrand met helling 0,134 in plaats van 0,1995. De belettering lag daardoor op een ander
vlak dan de flank, en dat is wat de gebruiker terugstuurde als "make the branding more accurate to
the angle".

**Hoe je het controleert, en dat is het stuk dat een volgende ronde moet overnemen:** lees de vier
hoeken af met `hoekraster.py` op 6x per hoek, niet op de hele foto in één keer, en reken daarna het
verdwijnpunt uit. De boven- en onderrand snijden elkaar hier op (4700, 831). Dat klopt pas als twee
andere lijnen die in de werkelijkheid evenwijdig aan deze lopen op hetzelfde punt uitkomen: de
dakrand geeft (4700, 790) en de onderrand van de bak (4700, 775). Drie lijnen binnen 56 px van
elkaar op een verdwijnpunt dat 2200 px buiten beeld ligt, en een horizon net onder het midden, wat
past bij een laag gehouden camera. Komt er één lijn ver buiten die groep uit, dan is een hoekpunt
verkeerd afgelezen en niet de wagen scheef.

`--debug` schrijft `versie-5-merkvlak.png` met het vlak als rode vierhoek over het resultaat; dat is
de laatste controle voor je iets warpt.

## De maat en de plek

Het vlak meet 796 x 811 px. Het paneel is 2048 x 1700 met het logo bovenin en de grondlijn van het
nummer op de onderrand.

| | breedte van het vlak | paneel in px | nummer |
|---|---|---|---|
| ronde 1 | 0,72 | 576 x 216 | 449 px |
| A | 0,82 | 653 x 542 | 614 px |
| **B en D** | **0,94** | **749 x 621** | **703 px** |

Het nummer ligt op vlak-v 0,797 tot 0,883. Het logo staat bij D op vlak-v 0,302 tot 0,495: het hart
van de ruimte bóven het nummer, niet het hart van de flank. Dat laatste was variant C (logo op
v 0,404 tot 0,596) en dat oogt als een logo dat naar beneden geduwd is, omdat er dan 40 procent lege
flank boven staat tegen 20 procent eronder. Bij D is dat 30 om 30.

## De sleet, afgelezen van de wagen zelf

`meet-flank.py` trekt de flank recht naar 800x800 in vlakcoordinaten (perspectief eruit) en meet:

| Wat | Meting |
|---|---|
| korrel | std 0,0085 / 0,0084 / 0,0086 per kanaal, ongeveer 2 niveaus van 255 |
| vuilverloop omlaag | vlak tot v=0,8, dan 0,986 en 0,938 in de onderste tiende: een 6,2 procent donkere vuilband boven de stootlijst |
| licht overdwars | 1,000 naar 0,988 van voor naar achter |
| vlekken | std 0,0083 tot 0,0094 op schalen 6, 14 en 30 px, en scheef: p1 −0,032 tot −0,040 tegen p99 +0,015 tot +0,025, dus de havens zijn donker en twee keer zo diep als de lichte plekken |
| streekrichting | \|dy\| 0,00046 tegen \|dx\| 0,00027: horizontaal gestreept |

Daaruit volgen vijf termen in `ronde3.py`, en elk is terug te voeren op een van die getallen:

1. 5 procent grondverlies over de hele folie
2. tot 30 procent verlies waar de flank zelf lokaal −0,04 donkerder is dan zijn omgeving. **Dit is
   de term die het beeld eigen maakt aan déze wagen**: de belettering verliest dekking op precies de
   plekken waar de carrosserie een veeg heeft. Een generieke distress-laag doet dat niet.
3. eigen vlekken van de folie, ±0,10, met de donkere kant verdubbeld in dezelfde 2:1-verhouding
4. krassen die horizontaal lopen, mee met de gemeten streekrichting
5. de vuilband, opgelegd over de onderste tiende van het vlak

Plus rafelige randen en verzadigingsverlies evenredig met de fade. De sleet wordt in het **paneel**
gebakken vóór de warp, zodat de schaduwkaart, de korrel en de randverzachting van `merk-op-doos.py`
er daarna gewoon overheen lopen.

Resultaat op de inkt: gemiddeld 12,0 procent dekkingsverlies, p99 24,5, hoogste 38,0.

De vuilband begint op vlak-v 0,90 en het nummer eindigt op 0,883. Dat is met opzet: de band schampt
de cijfers en loopt er niet doorheen.

## Blijft het nummer leesbaar

`leesbaar.py` meet het WCAG-contrast tussen de inkt van de cijfers en de flank eromheen, op de
maten waarop de site zo'n beeld toont.

| | volledig | 1200 px | 720 px | 390 px |
|---|---|---|---|---|
| zonder sleet (B) | 6,0:1 | 6,0:1 | 6,2:1 | 6,6:1 |
| met sleet (D) | 5,0:1 | 5,0:1 | 5,1:1 | 5,3:1 |
| cijferhoogte | 67 px | 32 px | 19 px | 10 px |

De sleet kost één punt contrast en blijft ruim boven 4,5:1. Belangrijker voor verkleinen: het deel
van het cijfervak dat duidelijk inkt is blijft 19,8 tot 20,9 procent op élke maat, dus de cijfers
lopen niet dicht en lossen niet op. De stroken in `_controle/leesbaar-*.png` van de reviewmap laten
dat ook met het oog zien; op 390 px breed staat er nog steeds 085 000 5647.

## Een volgende ronde

- Andere belettering op dezelfde wagen: begin bij `bron-blanke-flank.png`, houd de hoekpunten
  hierboven aan, pas `ronde3.py` aan. Niets opnieuw genereren.
- Een andere wagen: nieuw rondebestand naar het model van `ronde-1.json`, met de `TRUCK OVERRIDE`
  erin. Meet daarna de hoekpunten van die flank opnieuw met de verdwijnpuntcontrole hierboven; de
  hoekpunten in dit bestand gelden alleen voor deze foto.
- `merk-op-doos.py` waarschuwt bij een breedte buiten 0,45-0,55 en over "merk niet op karton". Beide
  waarschuwingen horen hier: dit is een flank, geen doos.
