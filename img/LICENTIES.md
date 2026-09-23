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

## Vervangen

`img/stap-2-bellen.webp` en `img/stap-5-verhuisdag.webp` staan niet meer in "Zo werkt het". Ze hebben
geen licentiespoor; stap-5 is een uitsnede van de hero van de oude Wix-site van de klant.
`stap-2-bellen.webp` is nog wel de bron van `img/headers/contact-bedankt.webp` (zie `bronnen.json`).
