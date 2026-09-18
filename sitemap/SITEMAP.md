# Sitemap verhuisbedrijfdereus.nl

**Paginastructuur voor de nieuwe website van Verhuisbedrijf De Reus**
Versie 1.2, 18 september 2026: zo compact mogelijk. De eerdere varianten staan in bijlage A.

| Bestand | Inhoud |
|---|---|
| `SITEMAP.md` | Dit document |
| `sitemap.xml` | Concept voor de 7 pagina's, klaar om bij de lancering te plaatsen |
| `robots.txt` | Concept dat bij `sitemap.xml` hoort |
| `sitemap-visual.html` | De boom als plaat voor de klant, in de huisstijl |

---

## 1. Samenvatting

**Regel: samenvoegen is de standaard.** Een pagina bestaat alleen als hij minstens één van deze toetsen haalt:
- **(a) Wettelijk of functioneel nodig.**
- **(b) Een zoekwoord met echt volume en een reële kans om te scoren, dat niet als blok op een andere pagina kan.**
- **(c) Een duidelijke conversiefunctie.**

"Zo'n pagina hebben andere sites ook" telt niet.

| | Aantal |
|---|---|
| **Pagina's in Google** | **7**: `/`, `/diensten/`, `/kosten/`, `/offerte/`, `/contact/`, `/algemene-voorwaarden/`, `/privacyverklaring/` |
| **Systeempagina's, niet in Google** | 3: `/offerte/bedankt/`, `/contact/bedankt/`, 404 |
| **Fase 2 en later** | Geen vaste pagina's meer. Een blok wordt alleen een pagina volgens de promotieregel in bijlage A. |

```
Home  /    (Den Haag · diensten · werkwijze · reviews · over ons · werkgebied · vragen)
├── Diensten  /diensten/   (8 blokken, zie 4.2)
├── Kosten  /kosten/
├── Offerte aanvragen  /offerte/    └── Bedankt  /offerte/bedankt/   [noindex]
├── Contact  /contact/              └── Bedankt  /contact/bedankt/   [noindex]
├── Algemene voorwaarden  /algemene-voorwaarden/
└── Privacyverklaring  /privacyverklaring/
404 [noindex] · /sitemap.xml · /robots.txt
```

Alle acht diensten blijven zichtbaar in het menu en de footer, via ankers op `/diensten/`.

**Wat de compressie kost in Google:**
- **Diensten:** zakelijk en internationaal ("internationaal verhuisbedrijf", 300) en opslag ("verhuisbedrijf met opslag" en "inboedel opslaan", 150 en 150, KD 1 tot 5) concurreren nu als blok, niet als eigen pagina. Reken op lagere posities voor juist de beste dienstkansen.
- **Home:** de home kiest voor "verhuisbedrijf den haag" en laat het landelijke "verhuisbedrijf" (3.100) los. Dat was met KD 68 toch geen reële kans.
- **Geen plaats- of landenpagina's:** extra plaatsen of landen vragen later weer nieuwe pagina's.
- **Wat het oplevert:** geen dunne pagina's, alle kracht op 3 sterke adressen, en minder bouw- en onderhoudswerk.

---

## 2. Wat er nu is

De huidige site is één Wix-pagina.
- **Adres:** `https://www.verhuisbedrijfdereus.nl`.
- **Sitemap:** `sitemap.xml` is een index naar `pages-sitemap.xml`, met alleen de home.
- **Robots:** `robots.txt` is de standaard van Wix.
- **Menu:** de menulinks (Over ons, Diensten, Werkwijze, Contact) zijn scrollankers op die ene pagina, geen adressen.
- **Pdf:** het enige andere adres is de pdf met de algemene voorwaarden: `/_files/ugd/03c52e_6264876606274b28a8cfdeb6721704cb.pdf`.
- **De nieuwe home lijkt daardoor op wat de eigenaar nu kent:** één lange pagina met blokken, maar sterker en met drie pagina's ernaast.

## 3. Conventies

We volgen `brocken/site/`, bevestigd door `website-kieviet/site/`:
- **Adresvorm:** map met `index.html`, adressen met een schuine streep aan het eind, geen `.html`, `trailingSlash: true` in `vercel.json`.
- **Robots:** `robots.txt` met `Allow: /`, `Disallow: /_werk/` en een sitemapregel.
- **Bedanktpagina's:** `noindex`.
- **Domein:** we houden www, want dat is nu de canonical.
- **Nesting:** geen, want alle pagina's hangen direct onder de home.
- **Slugs en ankers:** Nederlands, kleine letters, koppeltekens.

---

## 4. De pagina's

### 4.1 Wat overblijft, en waarom

| URL | Toets | Waarom deze pagina zelfstandig blijft | Primair zoekwoord | Hoofd-CTA |
|---|---|---|---|---|
| `/` | b, c | Het beste reële zoekwoord van de site. De home heeft de meeste kracht en de link vanuit Google Bedrijfsprofiel, dus een aparte Den Haag-pagina zou alleen concurreren. | **verhuisbedrijf den haag (1.100, KD 42)** | Offerte aanvragen |
| `/diensten/` | b, c | Draagt de dienstzoekwoorden die niet op de home passen zonder de Den Haag-focus te verwateren: internationaal verhuisbedrijf (300, KD 27) en verhuisbedrijf met opslag (150, KD 1). Plus een offerteknop per dienst. | per blok, zie 4.2 | Offerte aanvragen (met `?dienst=`) |
| `/kosten/` | b | "Wat kost een verhuisbedrijf" (1.200, KD 8), met kosten verhuisbedrijf (700) en verhuisbedrijf kosten (600, KD 2): ruim 3.000 per maand met lage KD. Dit is een vraag, geen aankoop, en Google toont daarop pagina's die de vraag beantwoorden. Een blok op home of diensten scoort daar niet op. | **wat kost een verhuisbedrijf** | Offerte aanvragen |
| `/offerte/` | a, c | Het offerteformulier, de hoofdknop op elke pagina. Vangt ook "offerte verhuisbedrijf" (150). | offerte verhuisbedrijf (150, KD 45) | Offerte aanvragen |
| `/contact/` | a | Contactformulier, adres, openingstijden, telefoon. Vaste plek voor vragen die geen offerte zijn. | merknaam (inferred) | Bel 085 000 5647 |
| `/algemene-voorwaarden/` | a | Wettelijk: de voorwaarden (Versie 2025) leesbaar en als pdf, gelinkt bij elk formulier | geen | Pdf downloaden |
| `/privacyverklaring/` | a | Wettelijk (AVG): de site verzamelt gegevens via twee formulieren en heeft nu geen privacyverklaring. Met een korte cookieparagraaf. | geen | geen |
| `/offerte/bedankt/`, `/contact/bedankt/` | a | Bevestiging en meting van aanvragen; noindex, niet in de sitemap | geen | Terug naar de home |
| 404 | a | Nette foutpagina met links naar diensten, offerte en contact; noindex | geen | Offerte aanvragen |

### 4.2 Blokken per pagina

**Home `/`** (H1 "Verhuisbedrijf in Den Haag"; volgorde zoals op de huidige site)

| Anker | Blok | Zoekwoord of doel |
|---|---|---|
| `#offerte` | Hero met kort offerteformulier en 4,9 uit 5 | conversie |
| `#diensten` | 8 tegels, elk naar zijn blok op `/diensten/` | interne links |
| `#waarom` | Bewijspunten: één vaste verhuisadviseur, geen voorrijkosten, standaard verzekerd, 7 dagen per week | vertrouwen |
| `#werkwijze` | Zo werkt het, in 5 stappen | wat doet een verhuisbedrijf (100, KD 0) |
| `#reviews` | Google-reviews, link naar het Google-profiel voor alle reviews | beste en betrouwbaar verhuisbedrijf den haag (30 en 30) |
| `#over-ons` | Wie De Reus is, het team | merknaam |
| `#werkgebied` | Hoofdkantoor Den Haag, wijken (alleen als de klant ze bevestigt; Scheveningen 150), heel Nederland en internationaal, met links naar `/diensten/#nationaal` en `#internationaal` | lokale varianten |
| `#vragen` | Veelgestelde vragen, algemeen | hoe lang van tevoren verhuisbedrijf regelen (20) |

**Diensten `/diensten/`** (H1 "Onze diensten". Title bijvoorbeeld "Verhuizen, opslag en internationaal verhuizen \| Verhuisbedrijf De Reus".)

Elk blok heeft:
- een H2
- 3 tot 5 alinea's
- een link naar het eigen blok op `/kosten/`
- een knop Offerte aanvragen met de dienst ingevuld

| Anker | Blok (H2) | Zoekwoord |
|---|---|---|
| `#particulier` | Particuliere verhuizingen | particulier verhuisbedrijf (30) |
| `#zakelijk` | Zakelijke verhuizingen, voor kantoren en kleine bedrijven | zakelijk verhuisbedrijf (100, KD 64), verhuisbedrijf voor kantoor (20) |
| `#nationaal` | Verhuizen door heel Nederland | verhuisbedrijf nederland (200, KD 55) |
| `#internationaal` | Internationale verhuizingen, van en naar Nederland | internationaal verhuisbedrijf (300, KD 27) |
| `#verhuislift` | Verhuizen met de verhuislift | verhuisbedrijf met lift (30), verhuisbedrijf met verhuislift (10); **niet** "verhuislift huren" |
| `#opslag` | Tijdelijke opslag | verhuisbedrijf met opslag (150, KD 1), inboedel opslaan bij verhuisbedrijf (150, KD 5) |
| `#montage` | Handymanservice: montage en kleine klussen | meubelmontage bij verhuizing (inferred) |
| `#woningontruiming` | Woningontruiming, extra rustig en tactvol geschreven | woningontruiming den haag (inferred) |

**Kosten `/kosten/`**

| Anker | Blok |
|---|---|
| `#opbouw` | Hoe de prijs tot stand komt: all-in of regieprijs, geen voorrijkosten, betalen op de verhuisdag |
| `#verhuizing` | Wat een verhuizing kost, met een regel over Den Haag ("verhuisbedrijf den haag kosten", 20) |
| `#opslag`, `#verhuislift`, `#montage`, `#woningontruiming` | Per aanvullende dienst; "kosten opslag inboedel verhuisbedrijf" (80) valt onder `#opslag` |
| `#annuleren` | Annuleren en wijzigen, volgens de voorwaarden |
| `#vragen` | Veelgestelde vragen over de prijs |

---

## 5. Was en wordt (versie 1.1 naar 1.2)

| Was | Samengevoegd in | Waarom geen eigen pagina |
|---|---|---|
| `/diensten/particuliere-verhuizingen/` | `/diensten/#particulier` | Keuze van de gebruiker; 30 zoekopdrachten |
| `/diensten/zakelijke-verhuizingen/` | `/diensten/#zakelijk` | 100 zoekopdrachten met KD 64: een nieuwe, kleine site haalt daar geen top 10. Het blok vangt de long tail (kantoor, bedrijven). |
| `/diensten/internationale-verhuizingen/` | `/diensten/#internationaal` | Keuze van de gebruiker. Het zoekwoord (300) is het sterkste dienstwoord en wordt het hoofdblok van `/diensten/`. |
| `/diensten/tijdelijke-opslag/` (fase 2) | `/diensten/#opslag` | Een blok kan het aan; promotie alleen volgens bijlage A |
| `/diensten/` als hub met 4 blokken | `/diensten/` met alle 8 blokken | Eén pagina voor alle diensten |
| `/werkgebied/` | `/#werkgebied` | Een hub met één plaats heeft geen functie |
| Nationale verhuizingen (`/werkgebied/#heel-nederland`) | `/diensten/#nationaal` | Het is een dienst, dus het hoort bij de diensten |
| `/werkgebied/den-haag/` | `/` (de home neemt het zoekwoord over) | De home kan "verhuisbedrijf den haag" beter dragen dan een losse pagina: meer kracht, de Bedrijfsprofiel-link, en de home had geen reëel alternatief zoekwoord |
| `/werkwijze/` | `/#werkwijze` | 100 zoekopdrachten, past als blok, staat nu ook op de home |
| `/reviews/` | `/#reviews` (+ link naar het Google-profiel) | Geen zoekvolume; de reviews staan op Google zelf |
| `/veelgestelde-vragen/` | `/#vragen` en `/kosten/#vragen` | 20 zoekopdrachten; vragen staan beter bij het onderwerp |
| `/over-ons/` | `/#over-ons` | Geen zoekvolume, geen eigen functie |
| `/sitemap/` (HTML) | vervalt | Bij 7 pagina's toont de footer alles al |
| `/werkgebied/{plaats}/`, `/diensten/internationale-verhuizingen/{land}/` | vervalt als vaste plek | Alleen via de promotieregel (bijlage A) |

Resultaat:
- **Versie 1.2:** 7 pagina's in Google.
- **Eerdere versies:** 17 (versie 1.1) en 21 (versie 1.0).
- **Redirects:** geen van de vervallen adressen is online geweest, dus er zijn geen redirects nodig.

---

## 6. Navigatie en interne links

**Header:**
- **Topbalk:** 085 000 5647 · info@verhuisbedrijfdereus.nl · 4,9 uit 5 op Google (naar `/#reviews`).
- **Menu:**
  - **Diensten**, met een uitklap van alle 8 diensten: Particulier `/diensten/#particulier`, Zakelijk `#zakelijk`, Door heel Nederland `#nationaal`, Internationaal `#internationaal`, Verhuislift `#verhuislift`, Tijdelijke opslag `#opslag`, Handymanservice `#montage`, Woningontruiming `#woningontruiming`.
  - **Kosten**
  - **Werkwijze** (`/#werkwijze`)
  - **Over ons**, met een uitklap: Over ons `/#over-ons`, Reviews `/#reviews`, Veelgestelde vragen `/#vragen`.
  - **Contact**
- **Knop:** **Offerte aanvragen** (goudgeel met Diepblauwe tekst).

**Footer:**
- **Diensten:** de 8 ankers.
- **De Reus:** Werkwijze, Over ons, Reviews, Veelgestelde vragen, Kosten.
- **Contact:** adres, telefoon, e-mail, openingstijden, knop.
- **Onderste regel:** Algemene voorwaarden · Privacyverklaring. Het KvK-nummer komt hier na open vraag 1.1.

**Kruimelpad:** niet nodig. Alle pagina's hangen direct onder de home.

**Interne links:**
1. **Home** linkt met de 8 dienstentegels naar de blokken op `/diensten/`, en verder naar `/kosten/` en `/offerte/`.
2. **Elk blok op `/diensten/`** linkt naar zijn blok op `/kosten/` en naar `/offerte/?dienst=…`.
3. **`/kosten/`** linkt per blok terug naar de dienst op `/diensten/` en naar de offerte.
4. **Ankerteksten:** het zoekwoord van een pagina of blok gebruikt u als ankertekst alleen voor links naar die pagina of dat blok. Voorbeelden: "verhuisbedrijf in Den Haag" altijd naar `/`, "verhuisbedrijf met opslag" altijd naar `/diensten/#opslag`.

---

## 7. Zoekwoorden: één eigenaar per zoekwoord

| Zoekwoord (volume) | Eigenaar | Let op |
|---|---|---|
| verhuisbedrijf den haag (1.100) | `/` | Alleen de home heeft het in title en H1 |
| verhuisbedrijf (3.100) | `/` (secundair) | KD 68, niet reëel; geen andere pagina richt zich erop |
| wat kost een verhuisbedrijf (1.200), kosten verhuisbedrijf (700), verhuisbedrijf kosten (600) | `/kosten/` | Andere pagina's geven hooguit één zin en linken door |
| internationaal verhuisbedrijf (300) | `/diensten/#internationaal` | Landen (Spanje 200, Frankrijk 200, Duitsland 100) eerst als H3 in dit blok, na bevestiging door de klant |
| verhuisbedrijf met opslag (150), inboedel opslaan (150) | `/diensten/#opslag` | `/kosten/#opslag` gebruikt "kosten opslag inboedel" (80) |
| zakelijk verhuisbedrijf (100) | `/diensten/#zakelijk` | |
| verhuisbedrijf met lift (30) | `/diensten/#verhuislift` | |
| wat doet een verhuisbedrijf (100) | `/#werkwijze` | |
| offerte verhuisbedrijf (150) | `/offerte/` | |
| erkend verhuisbedrijf (200) | **niemand** | Geen lidmaatschap bevestigd (open vraag 1.5) |
| verhuislift huren (4.400), verhuislift huren den haag (80) | **niet op deze site** | Domein van de eigen liftsites OranjeLift en VerhuisliftHuren. De Reus spreekt van "verhuizen met de verhuislift". |

**Portfolio:** Verhuisbedrijf.nl richt zich mogelijk ook op "verhuisbedrijf den haag" en "wat kost een verhuisbedrijf". Voor een klantsite is dat geen blokkade, maar het is een bewuste keuze van de eigenaar van beide sites (10.2).

---

## 8. Voorwaarden en beloftes

- **Zakelijk:** "voor kantoren en kleine bedrijven" (art. 2.1: klein zakelijk).
- **Internationaal:** "van en naar Nederland, over de weg" (art. 2.1). Geen zee- of luchtvracht.
- **Verhuislift, opslag, montage, woningontruiming:**
  - geen beloftes over verzekering of vaste prijzen (open vraag 2.4)
  - niet "los te boeken" tot 2.4 beantwoord is
  - eigen opslag en eigen lift pas na 1.6
- **Kosten:**
  - "standaard verzekerd", nooit "volledig" (art. 3.3 tegen 13)
  - all-in of regieprijs (art. 5), betalen op de verhuisdag (art. 7)
  - annuleren € 250 tot twee weken vooraf (art. 8)
  - "kosteloos wijzigen" alleen na bevestiging (2.1)
- **Reviews:** 4,9 uit 5 op Google, zonder aantal tot 1.4 beantwoord is.

---

## 9. Migratie

| Oud | Nieuw | Hoe |
|---|---|---|
| `https://www.verhuisbedrijfdereus.nl` | `https://www.verhuisbedrijfdereus.nl/` | Dezelfde pagina, canonical met `/` |
| `https://verhuisbedrijfdereus.nl/…` | `https://www.verhuisbedrijfdereus.nl/…` | 301 op host, zoals De Kievit |
| `/_files/ugd/03c52e_6264876606274b28a8cfdeb6721704cb.pdf` | `/algemene-voorwaarden/` | 301; het pdf-adres kan in oude offertes en mails staan |
| `/pages-sitemap.xml` | `/sitemap.xml` | 301 |

- **Na de lancering:**
  - Google Bedrijfsprofiel naar `/` laten linken.
  - `sitemap.xml` indienen in Search Console.
  - Staging en preview `noindex`, zoals Brocken en De Kievit.

---

## 10. Beslissingen

### 10.1 Voor de klant

1. **Prijzen:** mag `/kosten/` prijsindicaties noemen? Zonder bedragen scoort de pagina slechter op "wat kost een verhuisbedrijf" (1.200).
2. **Landen:** naar welke landen verhuist De Reus, over de weg? Dat vult `#internationaal`.
3. **Opslag:** heeft De Reus eigen opslag, waar en onder welke voorwaarden (1.6 en 2.4)? Dat vult `#opslag`.
4. **Verhuislift:** alleen bij een verhuizing, of ook los? En is de lift van De Reus zelf (2.4, 1.6)?
5. **Woningontruiming en handymanservice:** wat valt eronder (2.4)?
6. **Wijken:** in welke Haagse wijken en welke plaatsen buiten Den Haag werkt De Reus (1.3)? Dat vult `/#werkgebied`.
7. **Privacyverklaring:** wie levert de tekst?

### 10.2 Voor het team

1. **Den Haag op de home.** Dit vervangt de keuze uit versie 1.0 (een eigen Den Haag-pagina zoals bij Brocken). Google Bedrijfsprofiel linkt naar `/`.
2. **Portfolio:** overlap met Verhuisbedrijf.nl op "verhuisbedrijf den haag" en "kosten". Is dat akkoord?
3. **Verhuislift:** De Reus blijft weg van "verhuislift huren". Is dat akkoord?

---

## Bijlage A: terugdraaien en uitbreiden

**Promotieregel.** Een blok wordt pas een eigen pagina als beide gelden:
- **Er zijn genoeg bevestigde feiten** voor een volledige pagina (foto's, voorwaarden, prijzen).
- **Het blok staat 3 tot 6 maanden na de lancering op pagina 2 van Google** voor zijn zoekwoord (Search Console).

De sterkste kandidaten zijn:
1. `#opslag` naar `/diensten/tijdelijke-opslag/`: 400 per maand, KD 1 tot 5.
2. `#internationaal` naar `/diensten/internationale-verhuizingen/`: 300 per maand, KD 27, plus landen.
3. `/#werkgebied` naar `/werkgebied/{plaats}/`, alleen voor bevestigde plaatsen met eigen inhoud.

Bij promotie blijft het blok staan als korte samenvatting met een link. `sitemap.xml` krijgt de nieuwe regel erbij.

**Versie 1.1, compacte diensten (17 pagina's):**
- **Diensten:** `/diensten/` met 4 blokken (verhuislift, opslag, montage, ontruiming) plus eigen pagina's voor particulier, zakelijk en internationaal.
- **Losse pagina's:** `/werkgebied/` met `/werkgebied/den-haag/`, `/werkwijze/`, `/over-ons/`, `/reviews/`, `/veelgestelde-vragen/` en `/sitemap/`.

**Versie 1.0, uitgebreid (21 pagina's):** als 1.1, maar met ook een eigen pagina voor verhuislift, tijdelijke opslag, handymanservice en woningontruiming.

**Terugdraaien:** de adressen uit tabel 5 kunnen zo weer pagina's worden. De ankers blijven dan als samenvatting staan.
