# Het merk op een polo zetten

`merk-op-doos.py` is geschreven voor een dooszijvlak, maar doet op stof precies hetzelfde werk. Dit
is de afspraak die op 23-09-2026 is vastgelegd toen het borstmerk op de hero-drieluik, op een losse
verhuizer en op de contactfoto tegelijk gezet werd. Houd je eraan, dan staat het merk overal op de
site even groot ten opzichte van de persoon.

## De maat: 16,5% van de schouderbreedte

**Schouderbreedte** is de volle breedte van de blauwe stof, mouwen inbegrepen, gemeten over een band
van 40 px op de hoogte waar het merk komt. Dus niet van deltoid tot deltoid met de hand aangewezen,
en ook niet de romp zonder mouwen: gewoon de breedte van het blauwe vlak.

**Merkbreedte = 0,165 x die schouderbreedte.** Die verhouding komt van `img/team/team-hero-1600.webp`,
waar het merk al stond: de twee borsten die daar schoon te meten zijn geven 15,3% en 17,7%.

Een kleiner merk is fotografisch eerlijker, maar de hero staat op 350 tot 700 px en onder ongeveer
13% loopt het huisje dicht. Ga dus niet lager. Ga ook niet hoger: de contactfoto had een print van
51 tot 66% en dat las de gebruiker meteen als "veel te groot".

**Onderkant:** het brandbook wil het beeldmerk niet kleiner dan 32 px. Reken uit wat je merk wordt na
de export naar de maat waarop het beeld getoond wordt. Kom je onder de 32, dan hoort het merk niet op
die persoon, en moet het niet alsnog kleiner.

**Botsen de 16,5% en de 32 px, maak het merk dan nooit groter dan de verhouding.** Zo zijn de merken van
48 tot 77% van de schouderbreedte ontstaan, en die las de gebruiker telkens als veel te groot. Valt het
merk op de norm onder de 32 px, dan staat de foto te klein afgebeeld: verander de weergave (het beeld
groter tonen) of de uitsnede (krapper, zodat de persoon groter in beeld komt), niet het logo. Kan geen
van beide, dan geldt de regel hierboven: geen borstmerk op die persoon, of een rugprint op iemand die
van achteren in beeld staat.

**Geen schouder in beeld? Dan 0,49 x de mouwbreedte, en noem het een vervanging.** Op een poloshirt is
de schouderbreedte met mouwen ongeveer drie keer de platte breedte van een mouw op de bovenarm
(schouder circa 50 cm, mouw circa 17 cm), dus 0,165 x schouder is ongeveer 0,49 x mouwbreedte. Meet
de mouw loodrecht op de armas. Dit is een schatting uit kledingmaten, geen meting aan de foto: zet in
het verslag "maat via de mouw (0,49 x mouwbreedte), schouder niet in beeld", zodat niemand het later
voor een schoudermeting aanziet. Staat er wel een schouder in beeld, meet dan die. Afgeleid door
dereus-df in `website/review/contact-header-20260923/mouwmerk.py`.

## De plaats

- Zijwaarts: **0,22 x schouderbreedte** vanaf de knooplijst naar de draagzijde links, dus op een
  frontale figuur naar de rechterkant van het beeld.
- Verticaal: **ter hoogte van de onderste knoop** van de knooplijst.
- Daarna schuiven binnen +/- 80 px tot het merkvak **100% op stof** ligt: geen doos, hand, deken,
  armsgat of silhouetrand eronder. Blauwmasker: `b > 100 && b - max(r,g) > 32`.
- **Scoor ook het vak verruimd met 12 px** en kies de plek met de meeste schone stof eromheen.
  Zonder die tweede score is "100% stof" ook waar als de rand van het vak precies op de silhouetrand
  ligt, en dan staat het merk tegen de rand aan geplakt (gevonden door dereus-79 op een mouwmerk).

## Het vlak en de aanroep

Het vlak is **een vierkant met een zijde van 2 x de merkbreedte, gecentreerd op het merkmidden**, en
`--breedte 0.5` zet daar een merk van de halve vlakbreedte in. Dus geen borstpaneel met het merk
ergens in een hoek: een klein vak op maat van het merk zelf. De verhouding van het vlak doet er niet
toe, het script houdt altijd de eigen verhouding van het logo (0,510) aan; het vlak bepaalt alleen
de maat en het perspectief. Een vierkant vlak betekent geen perspectief, en dat klopt voor een borst
die naar de lens toe staat. Staat de stof schuin, geef dan vier hoeken die de stof volgen.

```
python _ai-beelden/gereedschap/merk-op-doos.py <bron.png> \
  --hoeken "1087,490 1227,490 1227,629 1087,629" \
  --logo brandbook/assets/logo/dereus-beeldmerk-negatief.png \
  --breedte 0.5 --korrel 0.15 --midden 0.5,0.5 \
  --uit <uit.png> --crop <crop.png>
```

Lees dat voorbeeld zo: het merk werd 70x35 px, het vlak is een vierkant van 139 px om het midden
(1157,560), hoeken met de klok mee vanaf linksboven.

Afwijkingen van de standaardwaarden: **`--korrel 0.15`** in plaats van 0.3, want dat is kartonkorrel
en stof is fijner. `--schaduw 5` en `--zacht 0.8` blijven zoals ze zijn; die werkten op alle negen
merken van het hero-drieluik en op de drie van de contactfoto.

**Negatieve variant op blauw**, `dereus-beeldmerk-negatief.png`. Het kleurenmerk met blauwe armen
verdwijnt in een koningsblauwe polo.

## Wat je tegenkomt

- **Eén merk per aanroep.** Voor meerdere personen: ketting de uitvoer van de ene aanroep in als
  bron van de volgende.
- **`merk op karton 0.0%` met een waarschuwing** komt op elke stofklus. Die controle is een
  kartondetector. Op kleding zegt hij niets, negeer hem.
- **De luminantiekaart werkt goed op donkerblauw.** Het script ijkt op de mediaan onder het merk, dus
  het merk houdt zijn eigen helderheid en neemt alleen het verloop over. Gemeten schaduwbereik op de
  negen hero-merken: 0,92 tot 1,07x op vlakke stof, 0,64 tot 1,15x op een merk dat over een plooi
  valt. Dat laatste mag: de arm van het merk wordt daar donkerder en dat is precies goed.
- **Schouderbreedte meten gaat twee keer mis** als je het automatisch doet. Een knoop of een vouw
  knipt de blauwe loop van één beeldrij doormidden, dus meet niet per rij. En raken twee polo's
  elkaar, dan is het samenhangende blauwe vlak de hele groep. Geef de breedte dan met de hand mee,
  één waarde per beeld: mensen die even ver van de camera staan horen even grote merken te krijgen.
- **Controleer elk merk op minstens 3x** voordat je het laat zien. Op de thumbnail zie je niet of de
  armen kloppen. `--crop` schrijft die uitsnede zelf.
- **Alfa.** Werk je op een uitsnede met transparantie, dan gooit het script het alfakanaal weg
  (`convert('RGB')`). Zet het achteraf terug uit het origineel.

## Waar het gebruikt is

- `website/review/team-hero-drie-r2-20260923/` - negen merken op drie beelden, 66 tot 102 px.
- `website/review/helpen-merk-20260923/` - drie merken op de contactfoto, 60 tot 78 px, waar eerst
  een print van 51 tot 66% van de schouderbreedte stond.
- `website/review/klantenservice-plooi-20260923/` - het borstmerk op de klantenservicefoto dat met de
  plooien meebuigt (verplaatsingsveld uit de stof zelf, pijplijn in `werk/`). Gemeten volgens dit document
  is het huidige merk daar 19,5% (175 van 898 px), niet de 27 tot 48% die eerder genoemd werd. De 27%
  kwam uit een merkbreedte die door het houten bureau in het goudmasker vervuild was (dereus-28, STAND
  van 23-09); hoe de 48% gemeten is, staat nergens.
