# Mockups · Verhuisbedrijf De Reus

Platte vectormockups voor hoofdstuk 07 Toepassingen. Elke SVG staat op zichzelf: het logo zit er inline in (overgenomen uit `../logo/`) en alle tekst is omgezet naar outlines in Archivo Condensed en Inter. De bestanden hebben dus geen externe verzoeken en werken gewoon in een `<img>`-tag. Elk bestand heeft een `viewBox`, een `<title>` en een `<desc>`.

In `preview/` staat van elke SVG een PNG van 1600 px breed met dezelfde naam, om te bekijken of te delen.

## Bestanden en bijschriften

De bijschriften komen letterlijk uit `content/microcopy.md`, hoofdstuk 07.

| Bestand | viewBox | Verhouding | Bijschrift |
|---|---|---|---|
| `verhuiswagen.svg` | 0 0 1750 750 | 21:9 | De bus rijdt de hele dag reclame. Groot logo, telefoonnummer en website, leesbaar vanaf de overkant van de straat. |
| `visitekaartje.svg` | 0 0 1760 550 | 2 x 85:55, 6 mm tussenruimte | Het logo aan de ene kant, de gegevens rustig aan de andere. |
| `briefpapier.svg` | 0 0 210 297 | A4 staand (mm) | Logo bovenaan, gegevens in de voet en veel wit: de brief zelf is de hoofdzaak. Op de envelop het logo zonder tagline, met het venster vrij voor het adres. |
| `e-mailhandtekening.svg` | 0 0 1600 700 | 16:7 | Naam, functie, telefoonnummer en het logo. Geen banners, geen citaten. |
| `website-header.svg` | 0 0 1600 700 | 16:7 | Het eerste scherm: logo, één heldere kop en één soort hoofdknop: goudgeel, altijd “Offerte aanvragen”. |
| `social-post.svg` | 0 0 1080 1080 | 1:1 | Eén boodschap per post, in blauw en geel, liefst met een echte klus of review. |
| `avatar.svg` | 0 0 1080 1080 | 1:1 | Het beeldmerk op wit of koningsblauw. Zonder tekst, want die is op dit formaat niet te lezen. |
| `verhuisdoos.svg` | 0 0 1600 1000 | 16:10 | Het logo op de doos, zodat hij tot aan de nieuwe voordeur herkenbaar is. |
| `werkkleding.svg` | 0 0 1600 1000 | 16:10 | Het logo op borst of rug. Zo ziet iedereen meteen wie er komt helpen. |

Later toegevoegd. Deze twee bijschriften staan ook in `content/microcopy.md`:

| Bestand | viewBox | Verhouding | Bijschrift |
|---|---|---|---|
| `verhuiswagen-achterkant.svg` | 0 0 1600 1000 | 16:10 | De achterkant ziet u in de file en voor het stoplicht. Daarom alleen het logo en het telefoonnummer, zo groot als de deur toelaat. |
| `offerte.svg` | 0 0 210 297 | A4 staand (mm) | De offerte in dezelfde opmaak als het briefpapier: logo bovenaan, een rustige tabel en het totaal op een goudgele balk. |

Extra, voor drukwerk of losse weergave:

| Bestand | viewBox | Inhoud |
|---|---|---|
| `visitekaartje-voorkant.svg` | 0 0 850 550 | Alleen de voorkant, 85 x 55 mm (1 eenheid = 0,1 mm) |
| `visitekaartje-achterkant.svg` | 0 0 850 550 | Alleen de achterkant |
| `envelop.svg` | 0 0 220 110 | DL-vensterenvelop (mm) |

## Wat er per mockup is gekozen

Regel overal: één slogan per vlak. Waar het logo met tagline "Geen verhuizing te groot!" staat, staat geen pay-off of campagneregel. De pay-off "Sterk in verhuizen. Zorgeloos geregeld." komt alleen voor naast het logo zonder tagline (briefpapier, e-mail).

- **Verhuiswagen:** witte bakwagen, logo met tagline groot op een wit vlak (vrije ruimte 1x rondom), telefoonnummer in Inter 700 koningsblauw, website wit in de koningsblauwe band met goudgele bies. Verder niets op de zijkant. Op het portier het negatieve beeldmerk op blauw.
- **Verhuiswagen, achterkant:** voor de signmaker. Roldeur zonder middennaad, daarop het horizontale logo (`dereus-logo-horizontaal`, 520 van de 680 eenheden deurbreedte, op een bak van 2,5 m is dat ongeveer 1,9 m) en daaronder het telefoonnummer in Inter 700 koningsblauw, precies even breed als het logo. Tussen logo en nummer zit 2,4x de vrije ruimte van het horizontale logo (21,7 % van de hoogte). Onderaan dezelfde koningsblauwe band met goudgele bies als op de zijkant, zonder tekst. Geen tagline en geen pay-off: het horizontale logo heeft er geen en de achterkant blijft zo leesbaar op afstand. Heeft de wagen twee deuren in plaats van een roldeur, zet dan het logo zo dat de naad niet door het beeldmerk loopt. Het horizontale logo ligt nog ter goedkeuring bij de klant.
- **Visitekaartje:** voorkant negatief logo van 42 mm breed (minimum met tagline is 40 mm) op koningsblauw; achterkant naam in Archivo Condensed 800, gegevens in Inter.
- **Briefpapier:** logo zonder tagline 40 mm breed linksboven, adres op de plek van het venster, in de voet drie kolommen (adres, contact, openingstijden en Google-score) en de pay-off in de band.
- **Offerte:** zelfde kop en voet als het briefpapier (logo zonder tagline 40 mm, pay-off in de band), met rechtsboven het woord OFFERTE in Archivo Condensed 800. Geen aanhef en ondertekening, want de offerte is de bijlage bij de brief. Tabelkop koningsblauw met witte tekst, de even regels op Blauw 50, het totaal op goudgeel met diepblauwe tekst. Alle bedragen staan op € 0,00 en bij Btw staat geen percentage. De regels zijn neutrale voorbeelden. Er staan geen prijzen, voorwaarden, verzekeringen of geldigheidstermijnen in, alleen de zin "Deze offerte is vrijblijvend." en een vak voor akkoord.
- **E-mailhandtekening:** logo zonder tagline (118 px breed, minimum 100 px), grijze scheidingslijn, pay-off als slotregel.
- **Website-header:** opbouw volgens `sitemap/SITEMAP.md` versie 1.2, hoofdstuk 6 Navigatie. Diepblauwe topbalk met telefoonnummer, e-mailadres en de Google-score. Witte header met logo zonder tagline (102 px breed, 12 px vrije ruimte), het hoofdmenu Diensten, Kosten, Werkwijze, Over ons en Contact (alleen het hoogste niveau, met een pijltje bij Diensten en Over ons omdat die uitklappen; Werkwijze en de uitklap van Over ons zijn ankers op de home) en de knop "Offerte aanvragen". Er is geen menu-item Home: het logo linkt naar de homepage. Koningsblauwe hero met boven de kop de kleine regel "Verhuisbedrijf in Den Haag" in goudgeel. Dat is de H1 van de home in de sitemap; de grote kop eronder is de visuele kop van de huidige site. Daaronder dezelfde knop "Offerte aanvragen" groot (goudgeel, diepblauwe tekst, pil) en een secundaire witte knop "Bel ons". De knop staat dus twee keer in beeld, in de header en in de hero, maar het is één actie. Vinkjes: goudgele cirkel met diepblauw vinkje. In het browsertabblad staat `dereus-favicon.svg`. De wagen in de hero is een illustratie van de bus: het logo daarop is een afbeelding van de belettering, net als op een foto, en geen los logogebruik. Het horizontale logo is bewust niet gebruikt, omdat het nog ter goedkeuring bij de klant ligt.
- **Social post:** campagneregel A uit `content/copy.md`, "Het zware werk, met zorg gedaan.", daarom het logo zonder tagline in de negatieve versie (`dereus-logo-zonder-tagline-negatief.svg`). Goudgeel alleen voor de accentregels en de knop. Geen accountnaam, geen volgers.
- **Avatar:** negatief beeldmerk op koningsblauw, past binnen een ronde uitsnede.
- **Verhuisdoos:** eenkleurendruk in koningsblauw op karton met `dereus-logo-1kleur-blauw.svg` (Pantone 293 C is de dichtstbijzijnde match, nog niet op een waaier gecontroleerd). Het telefoonnummer staat minstens 1,2x de vrije ruimte onder het logo, goudgele tape, invulvakken op de zijkant.
- **Werkkleding:** polo in koningsblauw met goudgele kraagbies en mouwboorden, negatief logo op de borst (80 mm) en op de rug (280 mm), met een uitvergroting van het borstlogo.

## Plaatshouders

Bewust nep, niet overnemen:

- `Naam Achternaam` / `Verhuisadviseur` (visitekaartje, brief, e-mail)
- Ontvanger `Familie De Vries, Voorbeeldlaan 12, 2500 AA Den Haag` (brief, offerte, envelop, e-mail), datum, offertenummer en de voorbeeldbrief
- De offerteregels `Verhuizing van adres A naar adres B`, `Verhuislift` en `Inpakmaterialen`, en alle bedragen (€ 0,00)

Er staan geen KvK-, IBAN- of btw-nummers in de mockups: die heeft het bedrijf niet gepubliceerd.

Echte gegevens van verhuisbedrijfdereus.nl: 085 000 5647, info@verhuisbedrijfdereus.nl, www.verhuisbedrijfdereus.nl, Lau Mazirellaan 336, 2525 ZJ Den Haag, ma t/m za 08.00 tot 20.00 uur en zo 09.00 tot 17.00 uur, 4,9 uit 5 op Google.

## Alle teksten per mockup

De tekst in de SVG's is omgezet naar outlines en dus niet doorzoekbaar. Deze lijst wordt bij elke run van het script opnieuw geschreven en bevat elke regel die op een mockup staat, plus de gebruikte logoversies.

<!-- teksten:start (gegenereerd door _bron/build_mockups.py, niet met de hand aanpassen) -->

**verhuiswagen.svg**  
Logo: dereus-beeldmerk-negatief, dereus-logo

- 085 000 5647
- verhuisbedrijfdereus.nl

**verhuiswagen-achterkant.svg**  
Logo: dereus-logo-horizontaal

- 085 000 5647

**visitekaartje.svg**  
Logo: dereus-logo-negatief

- 085 000 5647
- info@verhuisbedrijfdereus.nl
- www.verhuisbedrijfdereus.nl
- Lau Mazirellaan 336, 2525 ZJ Den Haag
- Naam Achternaam
- Verhuisadviseur

**visitekaartje-voorkant.svg**  
Logo: dereus-logo-negatief


**visitekaartje-achterkant.svg**  
Logo: geen

- 085 000 5647
- info@verhuisbedrijfdereus.nl
- www.verhuisbedrijfdereus.nl
- Lau Mazirellaan 336, 2525 ZJ Den Haag
- Naam Achternaam
- Verhuisadviseur

**briefpapier.svg**  
Logo: dereus-logo-zonder-tagline

- Familie De Vries
- Voorbeeldlaan 12
- 2500 AA Den Haag
- DATUM
- 18 september 2026
- BETREFT
- Offerte voor uw verhuizing
- OFFERTENUMMER
- 2026 0918
- Beste familie De Vries,
- Hartelijk dank voor uw aanvraag. Zoals besproken in ons telefoongesprek sturen wij u hierbij onze
- offerte voor de verhuizing van uw woning in Den Haag naar uw nieuwe woning in Delft.
- Wij verzorgen de complete verhuizing: het inpakken van breekbare spullen, het demonteren en
- monteren van meubels en het transport naar uw nieuwe adres. Waar nodig zetten wij een verhuislift
- in, zodat ook grote kasten via het raam naar binnen kunnen.
- In de bijlage vindt u de volledige offerte met een overzicht van alle werkzaamheden. Heeft u vragen
- of wilt u iets aanpassen? Bel ons gerust op 085 000 5647 of stuur een e-mail naar
- info@verhuisbedrijfdereus.nl.
- Wij kijken ernaar uit om uw verhuizing zorgeloos te regelen.
- Met vriendelijke groet,
- Naam Achternaam
- Verhuisadviseur, Verhuisbedrijf De Reus
- Verhuisbedrijf De Reus
- Lau Mazirellaan 336
- 2525 ZJ Den Haag
- 085 000 5647
- info@verhuisbedrijfdereus.nl
- www.verhuisbedrijfdereus.nl
- Ma t/m za 08.00 tot 20.00 uur
- Zo 09.00 tot 17.00 uur
- 4,9 uit 5 op Google
- Sterk in verhuizen. Zorgeloos geregeld.

**offerte.svg**  
Logo: dereus-logo-zonder-tagline

- OFFERTE
- Familie De Vries
- Voorbeeldlaan 12
- 2500 AA Den Haag
- DATUM
- 18 september 2026
- BETREFT
- Uw verhuizing
- OFFERTENUMMER
- 2026 0918
- OMSCHRIJVING
- BEDRAG
- Verhuizing van adres A naar adres B
- € 0,00
- Verhuislift
- Inpakmaterialen
- Subtotaal
- Btw
- Totaal
- Deze offerte is vrijblijvend.
- Heeft u vragen of wilt u iets aanpassen? Bel ons gerust op 085 000 5647 of stuur een e-mail naar
- info@verhuisbedrijfdereus.nl.
- VOOR AKKOORD
- Naam
- Datum
- Handtekening
- Verhuisbedrijf De Reus
- Lau Mazirellaan 336
- 2525 ZJ Den Haag
- 085 000 5647
- info@verhuisbedrijfdereus.nl
- www.verhuisbedrijfdereus.nl
- Ma t/m za 08.00 tot 20.00 uur
- Zo 09.00 tot 17.00 uur
- 4,9 uit 5 op Google
- Sterk in verhuizen. Zorgeloos geregeld.

**envelop.svg**  
Logo: dereus-logo-zonder-tagline

- Verhuisbedrijf De Reus
- Lau Mazirellaan 336
- 2525 ZJ Den Haag
- Familie De Vries
- Voorbeeldlaan 12
- 2500 AA Den Haag
- verhuisbedrijfdereus.nl

**e-mailhandtekening.svg**  
Logo: dereus-logo-zonder-tagline

- Bevestiging verhuisdatum
- Van
- Naam Achternaam  <info@verhuisbedrijfdereus.nl>
- Aan
- Familie De Vries
- Onderwerp
- Bevestiging verhuisdatum zaterdag 3 oktober
- Beste familie De Vries,
- Hierbij bevestigen wij uw verhuizing op zaterdag 3 oktober. Ons team staat om 08.00 uur bij u voor de
- deur en de verhuislift is gereserveerd.
- Heeft u nog vragen? Bel of mail ons gerust.
- Met vriendelijke groet,
- Naam Achternaam
- Verhuisadviseur, Verhuisbedrijf De Reus
- T
- 085 000 5647
- E
- info@verhuisbedrijfdereus.nl
- W
- www.verhuisbedrijfdereus.nl
- A
- Lau Mazirellaan 336, 2525 ZJ Den Haag
- Sterk in verhuizen. Zorgeloos geregeld.

**website-header.svg**  
Logo: dereus-beeldmerk-negatief, dereus-logo-zonder-tagline, dereus-favicon, dereus-logo

- 085 000 5647
- verhuisbedrijfdereus.nl
- Verhuisbedrijf De Reus
- info@verhuisbedrijfdereus.nl
- 4,9 uit 5 op Google
- Offerte aanvragen
- Diensten
- Kosten
- Werkwijze
- Over ons
- Contact
- Verhuisbedrijf in Den Haag
- De betrouwbare keuze voor
- een zorgeloze verhuizing
- Particulier of zakelijk, binnen Nederland of naar het buitenland:
- wij verhuizen het.
- Bel ons
- Vrijblijvende offerte
- Particulier en zakelijk
- 7 dagen per week bereikbaar

**social-post.svg**  
Logo: dereus-logo-zonder-tagline-negatief

- Het zware
- werk,
- met zorg
- gedaan.
- Offerte aanvragen
- verhuisbedrijfdereus.nl  ·  085 000 5647

**avatar.svg**  
Logo: dereus-beeldmerk-negatief


**verhuisdoos.svg**  
Logo: dereus-logo-1kleur-blauw

- DEZE KANT BOVEN
- KAMER
- INHOUD
- BREEKBAAR
- 085 000 5647

**werkkleding.svg**  
Logo: dereus-logo-negatief

- Voorkant
- Borstlogo links, 80 mm breed
- Achterkant
- Rugprint, 280 mm breed
- Detail borstlogo
- Negatief logo op koningsblauw

<!-- teksten:end -->

## Opnieuw genereren

De mockups komen uit één script. Kleuren, contactgegevens en logobestanden staan bovenaan in het blok TOKENS.

```
pip install uharfbuzz fonttools
python brandbook/assets/mockups/_bron/build_mockups.py
```

- Het script leest het logo uit `../logo/dereus-logo*.svg`, `dereus-beeldmerk*.svg` en `dereus-favicon.svg`. Het kleurt niets meer om: elke logoversie op een mockup is een bestaand bestand. Na een nieuwe logoversie volstaat een nieuwe run.
- Het menu van de websiteheader staat in `MENU` en de regel boven de kop in `EYEBROW`, vlak boven `build_web()`. Wijzigt de navigatie in `sitemap/SITEMAP.md`, pas het dan daar aan.
- De fonts staan in `_bron/fonts/` (Archivo en Inter als variabel font, SIL Open Font License 1.1, licentie ernaast).
- Zonder `uharfbuzz` valt het script terug op gewone `<text>` met de fontstack uit de tokens. Dan hangt de weergave af van de fonts op de computer van de lezer.
- De PNG's in `preview/` maak je met `python brandbook/assets/mockups/_bron/maak_previews.py`. Dat script zoekt Chrome of Edge, rendert elke SVG headless op 1600 px breed en heeft geen Python-pakketten nodig.
