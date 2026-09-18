# Logo voor drukwerk en belettering

Vector-PDF's van het logo van Verhuisbedrijf De Reus, voor de drukker, de belettering van de bus en textieldruk. De vormen zijn een op een overgenomen uit de SVG's in de map erboven. Er is niets gerasterd en er zitten geen fonts in: alle tekst staat in outlines.

## Bestanden

Het beeldmerk is in elk bestand 100 mm breed. De pagina sluit strak om het logo, zonder marge. Schalen mag onbeperkt.

| Bestand | Kleuren | Formaat | Gebruik |
|---|---|---|---|
| `dereus-logo.pdf` | blauw + geel | 100 x 99 mm | Primair logo, op wit of licht |
| `dereus-logo-negatief.pdf` | wit + geel | 100 x 99 mm | Op koningsblauw of diepblauw |
| `dereus-logo-1kleur.pdf` | zwart (alleen K) | 100 x 99 mm | Stempel, gravure, een drukgang |
| `dereus-logo-1kleur-blauw.pdf` | koningsblauw | 100 x 99 mm | Karton, flexodruk |
| `dereus-logo-zonder-tagline.pdf` | blauw + geel | 100 x 88,5 mm | Kleine formaten, briefpapier, offerte |
| `dereus-logo-zonder-tagline-negatief.pdf` | wit + geel | 100 x 88,5 mm | Kleine formaten op blauw |
| `dereus-logo-horizontaal.pdf` | blauw + geel | 257,6 x 53,9 mm | Alleen waar de hoogte beperkt is, zoals de achterkant van de bus |
| `dereus-logo-horizontaal-negatief.pdf` | wit + geel | 257,6 x 53,9 mm | Idem, op blauw |
| `dereus-beeldmerk.pdf` | blauw + geel | 100 x 53,9 mm | Alleen het beeld, zonder tekst |

Let op: het horizontale logo is een afgeleide die nog ter goedkeuring bij de klant ligt. Zie `../README.md`.

## Kleur

De PDF's staan in **CMYK** (DeviceCMYK). Er komt geen RGB in voor.

| Kleur | CMYK in de PDF | HEX (scherm) | Pantone, dichtstbij |
|---|---|---|---|
| Koningsblauw | 97 77 0 0 | `#1746A2` | 293 C |
| Goudgeel | 0 20 85 0 | `#FFCC33` | 123 C |
| Zwart (1kleur) | 0 0 0 100 | `#000000` | |
| Wit (negatief) | 0 0 0 0 | `#FFFFFF` | |

- De CMYK-waarden zijn omgerekend met het profiel Coated FOGRA39 (bron: `brandbook/research/color-type-system.md`). Ze gelden voor gestreken papier. Voor ongestreken papier, karton of textiel stemt de drukker ze af.
- De Pantone-nummers zijn de dichtstbijzijnde match op basis van de schermkleur (293 C met ΔE 3,0 en 123 C met ΔE 1,6). Ze zijn niet op een waaier gecontroleerd. Leg de waaier ernaast voordat u ze vastlegt. De PDF's bevatten geen steunkleuren. Wie in Pantone drukt, zet de twee CMYK-kleuren bij de drukker om naar de gekozen PMS-kleur.
- Er zit geen ICC-profiel of output intent in de bestanden. Het zijn dus geen PDF/X-bestanden. Voor een logo dat in een opmaak wordt geplaatst is dat gebruikelijk: het document waarin het logo komt bepaalt het profiel.
- Wit is in de negatieve versies een vlak zonder inkt (0 0 0 0). Op een witte pagina ziet u de armen en VERHUISBEDRIJF dus niet. Plaats het bestand op koningsblauw of diepblauw. Voor wit op folie, glas of donker textiel vervangt de signmaker of drukker dit vlak door witte folie of wit als extra drukgang.
- De witte lijnen in de armen zijn uitsparingen. De ondergrond schijnt erdoorheen. Dat is bewust zo.

## Gecontroleerd

Elke PDF is geopend en gerenderd met MuPDF en naast de PNG uit de map erboven gelegd. Per bestand: geen afbeeldingen, geen fonts, alleen gevulde paden met de CMYK-operator `k`, en de vorm valt samen met de PNG (overlap 0,98 tot 1,00; het verschil komt door afronding van de PNG-hoogte). Op 2400 % ingezoomd blijven de randen scherp.

Niet gecontroleerd: een drukproef. Hoe blauw en geel op papier, karton, folie en textiel uitvallen, weet u pas na een proef.

## Minimumformaten en vrije ruimte

- Logo met tagline: minimaal 40 mm breed. Zonder tagline: minimaal 25 mm breed. Horizontaal: minimaal 8 mm hoog. Beeldmerk: minimaal 12 mm breed.
- Vrije ruimte rondom: de breedte van de deur in het huis. Dat is 11,7 % van de breedte van het staande logo, of 21,7 % van de hoogte van het horizontale logo.
- Zet het logo in kleur nooit op blauw. Gebruik daar de negatieve versie.

## Opnieuw maken

```
python brandbook/assets/logo/druk/_bron/maak_pdf.py
```

Het script heeft alleen Python 3 nodig. Het leest de SVG's uit de map erboven en schrijft de paden als PDF-paden weg. De CMYK-waarden staan bovenaan in het blok KLEUREN. Na een nieuwe logoversie volstaat een nieuwe run.
