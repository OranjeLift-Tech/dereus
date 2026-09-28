# Herkomst en licentie van beelden

Per bestand in `img/`: waar het vandaan komt en onder welke licentie. Begonnen op 23-09-2026 bij het
vervangen van twee stapfoto's in "Zo werkt het" (home). De header-achtergronden staan in
`img/headers/bronnen.json` en `img/headers/README.md`.

## img/stap-1-laptop.webp

- Stap 1, "Offerte aanvragen". Laptop, notitieblok en pen op een houten tafel. Geen personen.
- Bron: Wikimedia Commons, https://commons.wikimedia.org/wiki/File:Laptop_picture_with_notepad.jpg
- Oorspronkelijk: http://startupstockphotos.com/post/86510756626/, Eric Bailey, 21 mei 2014.
- Licentie: **CC0 1.0 Universal (Public Domain Dedication)**. Nagekeken door Commons-reviewer Achim55 op
  30 juli 2017. Geen naamsvermelding verplicht.
- Bewerkt: het merk op de pen (PILOT V5 PRECISE, FINE) is weggehaald door het drukwerk in te vullen vanuit
  het zwart van de pen (`website/review/stappen-foto-20260923/stap1-maak.py`); daarna bijgesneden tot
  1080x900 (y 110-1010), WebP q82. Origineel (1080x1080, md5 296cbe515fe52a2dc473e2808ab513ef) in
  `website/review/stappen-foto-20260923/bron/`.

## img/stap-2-contact.webp

- Stap 2, "Persoonlijk contact". Telefoon, notitieboek, potlood en bril op een wit bureau. Geen personen.
- Bron: Wikimedia Commons,
  https://commons.wikimedia.org/wiki/File:White_work_table_with_notes,_smartphone_and_laptop_(Unsplash).jpg
- Oorspronkelijk: https://unsplash.com/photos/pUAM5hPaCRI, JESHOOTS.COM (jeshoots), 8 maart 2017.
- Licentie: **CC0 1.0 Universal (Public Domain Dedication)**. Commons vermeldt dat de foto voor
  5 juni 2017 op Unsplash stond, toen Unsplash nog CC0 gebruikte. Geen naamsvermelding verplicht.
- Origineel (4600x3067, md5 fd559ba386e1ee4f7dbbcc279e836436) bewaard in
  `website/review/stappen-foto-20260923/bron/`. Uitsnede x 0-3680, volle hoogte, naar 1120x933, WebP q80.

## img/stap-5-bank-voordeur.webp

- Stap 5, "Verhuisdag". Twee verhuizers dragen een bank in dekens door de voordeur.
- Bron: zelf gegenereerd op 23-09-2026, versie 3 ("Bank door de voordeur") uit de ronde
  `website/review/home-header-werk-20260923/versie-3.png` (md5 4fa2ea5fe23752830c20b0ec23dbb299).
  Prompt in `prompts.md` en `ronde.json` van die ronde. Polo's zonder merk, geen logo in beeld.
- Licentie: eigen beeld, geen rechten van derden.
- Uitsnede x 0-2181, y 31-1511, naar 1120x760, WebP q80.

## img/verhuizer-doos-schouder-uit.webp

- Home, "Zo regelt u het in een paar minuten" (`_werk/blokken/aanvraag.py`, beeld), sinds 23-09-2026 in
  plaats van `img/aanvraag-foto-uit.webp`. Stond ook al als optie "doos-schouder" in `_werk/blokken/vragen.py`.
- Bron: zelf gegenereerd op 23-09-2026, ronde `website/review/verhuizer-uitsnede-20260923/`, versie 2
  "Doos op de schouder". De witte doos met merk is door nano banana pro bedrukt (ronde 3), het borstmerk
  gecomposit, vrijstaand gemaakt met rembg (isnet-general-use). Man, geen derden in beeld.
- Licentie: eigen beeld. Nog niet in git: moet mee in dezelfde commit als de wijziging in aanvraag.py.

## img/helpen-kantoor.webp

- /contact/, "Zo helpen wij u snel" (`_werk/paginas/contact.py`, formulier team=), sinds 23-09-2026 in plaats
  van `img/helpen-wij-u-snel.webp` (drie werknemers).
- Bron: `img/kaart-3d/kantoor.webp` (3D-render uit `_ai-beelden/kaart-3d/scene.html`, functie kantoor, commit
  968f82d), alleen bijgesneden op de alfarand en links, rechts en boven transparant aangevuld tot 844x422 (2:1),
  zodat het in de gereserveerde band onder de tekst past. Geen pixels van het gebouw veranderd.
- Merk op de gevel: VERHUISBEDRIJF over DE REUS, zonder naamregel, op 4x nagekeken.
- Licentie: eigen render.

## img/footer-wagen.webp

- Footer op elke pagina, de foto achter de intro (`.footer__wagen`, `_werk/navigatie.py`). Sinds 28-09-2026
  in plaats van de vorige foto van de bestelwagen; die staat als `voor-footer-wagen.webp`
  (md5 13f6e9c282a50f253d1e3d1218c43227) in `website/review/footer-truck-20260928/`.
- Bron: repo debresser, origin/main d432b94,
  `assets\img\ai-beelden\debresser-beeldbank\02-verhuizen\verhuisbedrijf-europa-2.jpg` (2752x1536,
  md5 470619fa27397867ef45a6e4555c5c93). Een AI-beeld uit de beeldbank van De Bresser, geen foto van hun
  echte wagenpark. Hetzelfde beeld staat in hun eigen footer (`assets\img\footer\vrachtwagen-snelweg-*.webp`).
  Paden in de debresser-repo staan hier met backslashes: met slashes leest de beeldcontrole
  (`_werk/controle-beelden.py --vangnet`) ze als sitepad `/img/...` van deze site.
- Bewerkt op 28-09-2026 met nano banana pro (gemini-3-pro-image-preview), twee rondes met een geometrieslot
  (uitvoer valt pixel voor pixel op de bron):
  1. het hele beeld: embleem, DE BRESSER, de groene blokken en het labeltje van de opbouwer van de bak
     gehaald, belettering uit `brandbook/assets/mockups/preview/verhuiswagen.png` erop (logo
     `brandbook/assets/logo/dereus-logo.png`, 085 000 5647, gouden streep en blauwe band met
     verhuisbedrijfdereus.nl);
  2. alleen de cabine: spoiler, paneel onder de voorruit en portier wit.
- Composiet (`website/review/footer-truck-20260928/werk/samenstel.py`): de bron, met ronde 1 alleen binnen
  de omtrek van de bak en ronde 2 alleen waar de oude letters op de cabine zaten; de cijfers op het kenteken
  zijn met kentekengeel dichtgezet. Daarbuiten is elke pixel de bron. Geen naam, nummer, adres of embleem van
  De Bresser meer in beeld, op 3x nagekeken (`controle/versie-1-merk-3x.png`).
- Uitsnede x 490-2590, y 54-1536 (`versie-1-klaar.png`, 2100x1482, md5 b300ebd4a26a119cf04a16b08b4d9ff8),
  naar 1200x847, WebP q78, md5 f26a9436617c9e43efab6d6968e41446 (`na-footer-wagen.webp`).
- Goedgekeurd op 28-09-2026 in de ronde `website/review/footer-truck-20260928/`, versie 1.
- Licentie: niet vastgelegd. Het bronbeeld is gegenereerd voor De Bresser, een andere klant. Hoe het daar
  gemaakt is, is niet nagekeken.

## img/clay/: klei-iconen

- Negentien vierkante, transparante WebP-iconen in kleistijl, elk in 144, 176, 240 en 480 px:
  particulier, zakelijk, nationaal, internationaal, verhuislift, opslag, montage, woningontruiming, headset,
  schild, trap, ster, vraagtekens, formulier, klembord, klok, telefoon, envelop en dozen. Geen mensen, geen
  tekst, geen merk.
- Sinds 28-09-2026 in de grote icoonvakken, in plaats van de 3D-renders uit `img/contact-3d/`, `img/kaart-3d/`
  en `img/kosten-3d/`: `waarom.py` (home), `vragen.py`, `css/blok/reviews-ster.css`, `opbouw.py` en
  `extradiensten.py` (/kosten/), `lijstplaat.py` en `lijstplaat.css` (en `lijstplaat-geel`), `namozaiek.py` (/werkwijze/) en
  `contactkaarten.py` (/contact/).
- Bron: zelf gegenereerd op 28-09-2026 met nano banana pro (gemini-3-pro-image-preview), ronde
  `website/review/clay-iconen-20260928/` (rondebestand `website/review/clay-iconen.json`, de prompts in
  `prompts.md` van die ronde). Als stijlvoorbeeld kreeg het model drie iconen uit de repo solargreen-www mee
  (`assets\img\3d\bel-176.webp`, `kalender-144.webp` en `schild-144.webp`), alleen voor materiaal, licht en
  camerahoek; onderwerp en kleur staan in de prompt.
- Vrijstaand gemaakt: het model levert JPEG op een magenta achtergrond; die is eruit gehaald met
  `werk/uitsnijden.py` in de rondemap (magenta weg, randpixels ontmengd, roze strooilicht eraf), bijgesneden
  op de alfarand en vierkant gemaakt met 2 procent marge aan elke kant. De bronnen op 512 px (PNG) staan in `bron/` van de
  ronde, niet in `img/`. 144, 176 en 240 komen uit `iconen/` van de ronde, 480 is uit de 512-bron verkleind;
  alles WebP q90.
- Goedgekeurd op 28-09-2026, alle negentien: "keep them all, use them when you need to use a large icon."
- Licentie: eigen beeld. Nog niet in git: moet mee in dezelfde commit als de blokken hierboven.

## Iconen: Solar, Bold Duotone

- Alle iconen van de site sinds 28-09-2026: de sprite in `_werk/kit.py` (`SOLAR`, de ster in `VOL`), de
  diensticonen (`DIENST_SOLAR`, inline via `ctx.dienst_icoon`), de telefoon in `_werk/blokken/formulier.py`
  en de iconen als CSS-masker in `css/blok/formulier.css`, `offertepil.css`, `vertrouwensrij.css`,
  `kosten-diepte.css`, `checklist.css` en `watwijdoen.css`. Geen losse bestanden in `img/`: de vormen staan
  als pad in de code. Gekozen door de gebruiker in `website/review/iconen-20260928/` (versie 2).
- Bron: Solar icon set door 480 Design, https://www.figma.com/community/file/1166831539721848736, via het
  npm-pakket `@iconify-json/solar` 1.2.13 (cdn.jsdelivr.net, opgehaald 28-09-2026). De vormen zijn niet
  bewerkt; de naam van het Solar-icoon staat per regel in `kit.py`.
- Licentie: **CC BY 4.0**, https://creativecommons.org/licenses/by/4.0/. Naamsvermelding verplicht: die
  staat op `/privacyverklaring/`, sectie Cookies (`website/content/privacyverklaring.md`).
- Uitzondering: de verhuislift (`DIENST_SOLAR["verhuislift"]`). Solar heeft er geen; zelf getekend op
  28-09-2026 in dezelfde stijl (24-raster, ladder in de tweede toon, onderstel, wielen en doos in de
  hoofdtoon). Eigen tekening, geen vorm uit een andere set.
- Niet van Solar: het Google-logo, het WhatsApp-glyph en het huisje uit het logo (`VOL` in `kit.py`).
- De vorige set: `img/iconen/icoon-*.svg` (iconenset v1, eigen tekening) wordt nergens meer gebruikt, maar
  `build.py` kopieert hem nog uit `brandbook/assets/imagery/`.

## img/helpen-drie-uit.webp

- /contact/, "Zo helpen wij u snel" (`_werk/paginas/contact.py`, formulier figuur=), de versie van Tugche van
  28-09-2026. Sinds de samenvoeging van 28-09-2026 staat daar live `img/verhuizer-doos-zijgreep-uit.webp`; deze
  staat in `contact.py` als regel om te wisselen.
- Samengesteld uit twee beelden die al in de repo stonden, geen nieuwe generatie: de adviseur uit
  `img/contact-adviseur-uit.webp` (commit f394ee1, teamgenoot) vooraan, en de man met de dozen en de blonde
  man met de deken uit `img/team/team-hero-1600.webp` erachter.
- Borstmerk van de adviseur: de door AI getekende print (geel, met verzonnen tekst) is weggehaald en vervangen
  door het echte `dereus-beeldmerk-negatief.svg`, volgens `_ai-beelden/gereedschap/MERK-OP-KLEDING.md`.
- Scripts en werkwijze: `_ai-beelden/helpen-drie/`. Licentie: zoals de twee bronbeelden.

## img/voorbereiding-kast-man.webp

- /werkwijze/ #voorbereiding ("Uw lijstje"): de verhuizer die uit de foto leunt (ontwerp 09 "Diepe plaat",
  28-09-2026, de versie van Tugche). Wordt precies op `img/voorbereiding-kast.webp` gelegd, zie UITSNEDE in
  `_werk/blokken/lijstplaat-geel.py`. Sinds de samenvoeging van 28-09-2026 staat live de Koningsblauwe plaat
  (`lijstplaat.py`); `lijstplaat-geel` staat in `werkwijze.py` als regel om te wisselen.
- Bron: `img/voorbereiding-kast.webp` zelf (versie 5 uit de ideeenronde van 23-09-2026, door ons gemaakt,
  zie `_werk/export-lijstplaat-kast.cjs`). Geen ander beeld, dus dezelfde herkomst.
- Bewerkt: achtergrond verwijderd met @imgly/background-removal-node (model medium), alfa hard gemaakt
  (onder 120 weg, boven 200 vol), de donkere kastrand naast de vingers van de opgeheven hand weggehaald.
  Zelfde formaat 1200x1030, WebP q88, alfa q92.

## img/offerte-figuur-uit.webp

- /offerte/, "Zo regelt u het in een paar minuten" (`_werk/paginas/offerte.py`, formulier figuur=), de versie van
  Tugche van 28-09-2026. Sinds de samenvoeging van 28-09-2026 staat daar live `img/verhuizer-doos-zijgreep-uit.webp`;
  deze staat in `offerte.py` als regel om te wisselen.
  Bewust niet een van de `verhuizer-*-uit.webp`: dat is steeds dezelfde man, ook die met de steekwagen bij
  "Zo gaat het verder" direct eronder.
- Bron: `img/over-verhuizer.webp` (in de repo sinds commit 5e39059; stockfoto waarvan het petrolgroene shirt
  koningsblauw is gemaakt en het borstzakje het logo kreeg, `_ai-beelden/kleding-logo.mjs`). De herkomst en
  licentie van de oorspronkelijke foto staan nergens vastgelegd: nog uitzoeken.
- Bewerkt: achtergrond en de doos linksonder verwijderd met @imgly/background-removal-node (model medium), alfa
  hard gemaakt (onder 120 weg, boven 200 vol), bijgesneden op de persoon: kruin tot y 800, de onderkant van het
  shirt op 78,7% van de hoogte. 435x752, WebP q90.

## Vervangen

`img/stap-2-bellen.webp` en `img/stap-5-verhuisdag.webp` staan niet meer in "Zo werkt het". Ze hebben
geen licentiespoor; stap-5 is een uitsnede van de hero van de oude Wix-site van de klant.
`stap-2-bellen.webp` is nog wel de bron van `img/headers/contact-bedankt.webp` (zie `bronnen.json`).

`img/helpen-kantoor.webp` staat sinds 28-09-2026 niet meer op /contact/: "Zo helpen wij u snel" gebruikt nu
`img/verhuizer-doos-zijgreep-uit.webp` (optie beeld), met `img/helpen-drie-uit.webp` (optie figuur in
`_werk/blokken/formulier.py`, zie hierboven) als versie van Tugche om te wisselen.
