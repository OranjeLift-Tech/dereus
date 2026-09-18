# Brand-facts brief: Verhuisbedrijf De Reus (website research)

- **Source:** https://www.verhuisbedrijfdereus.nl/ (crawled 2026-09-18)
- **Method:** raw HTML and inline CSS pulled with curl, colors counted in the site CSS, pixel samples taken from headless-Chrome screenshots, and the Algemene Voorwaarden PDF read in full.
- **Inferred items** are marked **(inferred)**. Everything else is quoted or measured from the live site.

> **Important scope note:** the site is a **single-page Wix Studio site**. `sitemap.xml` lists only the homepage. The nav items (Home, Over ons, Diensten, Werkwijze, Contact) are anchor links to sections on that one page. There are **no** separate pages for diensten, over ons, prijzen/tarieven, werkgebied or reviews. The only other document is the Algemene Voorwaarden PDF:
> https://www.verhuisbedrijfdereus.nl/_files/ugd/03c52e_6264876606274b28a8cfdeb6721704cb.pdf
>
> Reference copies of the key images and a full desktop screenshot are in `brandbook/research/img/`.

---

## 1. COMPANY FACTS

| Field | Value (as shown on site) |
|---|---|
| Trading name | **Verhuisbedrijf De Reus**. Spelled "Verhuisbedrijf de Reus" (lower-case *de*) in the `<title>` and the og:site_name. Body copy uses "De Reus". |
| Legal entity / legal form / KvK / BTW | **Not shown** anywhere: not on the site, not in the JSON-LD, and not in the Algemene Voorwaarden. The AV only uses the trading name "Verhuisbedrijf De Reus" and defines it as "de opdrachtnemer die beroepsmatig consumenten en bedrijven verhuizingen verzorgt" (Art. 1.2). No B.V., V.O.F. or eenmanszaak is named. **Ask the client** (see section 8). |
| Founding year | **Not shown.** The AV gives no founding or registration details either. The AV is "Versie 2025" and the footer says "© 2025", so the website probably dates from 2025 **(inferred)**. |
| Address | "Lau Mazirellaan 336, 2525 ZJ Den Haag" labelled **"(hoofdkantoor)"**. The JSON-LD has the same address: LocalBusiness, addressRegion "ZH". |
| Service area | HQ in Den Haag. Services cover **national and international** moves ("Nationale Verhuizingen", "Internationale Verhuizingen"; meta: "binnenlandse en internationale verhuizingen"). No werkgebied page or city list. The main market is probably Den Haag / Zuid-Holland **(inferred)**. |
| Phone | **085 000 5647** (tel: link; a national 085 number) |
| Email | **info@verhuisbedrijfdereus.nl**. ⚠ The contact-section mailto link is broken: `mailto:nfo@verhuisbedrijfdereus.nl` (the "i" sits in a separate span). |
| Opening hours | "Maandag t/m zaterdag van 08:00 - 20:00" · "Zondag van 09:00 tot 17:00". Also "7 dagen per week beschikbaar" and "Ons team staat 7 dagen per week voor u klaar." |
| Certifications / memberships | **None shown**, on the site or in the AV. No Erkende Verhuizers, OVB, Keurmerk, ISO, geschillencommissie or similar. The brand book should **not** claim any of these unless the client confirms them. |
| Review score | **4,9/5 on Google.** It appears as "4,9/5" in the hero and footer and as "4.9/5" in headings. Each review card is labelled "Geverifieerde Google-review". The number of reviews is **not shown**. |
| Key stats / promises | "binnen **24 uur** gebeld" · offerte "**dezelfde dag**" · "Reactie binnen 24 uur" · "**Geen voorrijkosten**" · "**één vaste verhuisadviseur**" · inboedel "standaard verzekerd" |
| Terms (AV "Versie 2025") | All-in price or regieprijs (Art. 5.1). Payment "op de verhuisdag" (Art. 7). Cancellation up to 2 weeks before: **€ 250** (Art. 8.2). Maximum compensation **€ 23.000 per inboedel**, eigen risico **€ 500** (Art. 13). Damage must be reported on the moving day itself (Art. 12). Dutch law applies (Art. 14, 15). Full analysis in **section 8**. |
| Insurance (what "standaard verzekerd" means) | Goods are "automatisch volledig verzekerd" during the move (Art. 3.3), **but** compensation is capped at € 23.000 per inboedel with a € 500 eigen risico (Art. 13). The customer arranges any extra cover themselves (Art. 3.4). No insurer or policy is named. |
| Complaints / disputes | No complaint procedure and no geschillencommissie. Damage must be reported "direct op de verhuisdag" (Art. 12). Dutch law applies (Art. 14). |
| AV document | "Algemene voorwaarden Verhuisbedrijf De Reus, Versie 2025". A 3-page PDF generated with the ReportLab library, created 24 Feb 2026, last changed on the server 5 Aug 2026. Local copy: `brandbook/research/algemene-voorwaarden-dereus-2025.pdf`. |
| Website built by | "© 2025 by WebMelt Services MDA" (web agency credit in the footer) |
| Favicon | None. The site uses the default Wix favicon (`static.parastorage.com/client/pfavico.ico`). |

---

## 2. SERVICES

The site lists **8 services as icon tiles with titles only**. There are no per-service descriptions and no subpages. Titles are quoted exactly. The one-line descriptions are **(inferred)** and put together from wording elsewhere on the site.

| # | Service (exact site title) | One-liner |
|---|---|---|
| 1 | **Particuliere Verhuizingen** | Moving households, "van inpakken tot uitpakken" **(inferred)** |
| 2 | **Zakelijke Verhuizingen** | Office and business moves; the AV mentions "klein zakelijk" **(inferred)** |
| 3 | **Nationale Verhuizingen** | Moves within the Netherlands ("binnenlandse verhuizingen") **(inferred)** |
| 4 | **Internationale Verhuizingen** | Moves abroad ("internationale verhuizingen") **(inferred)** |
| 5 | **Woningontruiming** | Clearing out a home **(inferred)** |
| 6 | **Tijdelijke opslag** | Short-term storage of the inboedel **(inferred)** |
| 7 | **Handymanservice** | Assembly and odd jobs; one review praises "De montage liep vlekkeloos" **(inferred)** |
| 8 | **Verhuisliftservice** | Moving/furniture lift (the icon shows a scissor-lift trolley) **(inferred)** |

Section copy: **"Onze diensten"** / "Welke verhuizing u ook plant, bij De Reus vindt u de juiste service."

Related capability phrases used on the site:
- "Van inpakken tot uitpakken: alles is mogelijk."
- "Van spoedklussen tot kosteloos wijzigen van uw verhuisdatum."
- "Wij zorgen voor persoonlijk, betaalbaar en zorgeloos verhuizen van A tot Z." (meta description)

Typos on the live site (don't copy these into the brand book):
- "Hnadymanservice" (mobile tile)
- "Verhuislitservice" (footer)
- "Zakelijke  Verhuizingen" / "Nationale  Verhuizingen" (double spaces)

---

## 3. USPs / TAGLINES / CTAs (quoted exactly)

**Primary headline (H1)**
- "De betrouwbare keuze voor een zorgeloze verhuizing"

**Hero subline** (two variants)
- Desktop: "Professionele verhuizers. Heldere prijzen. Altijd service op niveau."
- Mobile: "Professionele verhuizers, heldere prijzen en altijd service op niveau."

**Brand line / slogan (footer)**
- **"Sterk in verhuizen. Zorgeloos geregeld."**
- It plays on the name *De Reus* ("the giant"), which means strength **(inferred)**. This is the best candidate for the official tagline.

**USP bar (under the header, italic grey)**
- "7 dagen per week beschikbaar"
- "Echte professionals geen studenten"
- "Vrijblijvende offerte & verhuisadvies"
- "Inbdoel standaard verzekerd" (sic: should read *Inboedel*)

**"Dit mag u van ons verwachten"**, with the intro line "Alles voor een zorgeloos en geregelde verhuizing."
- **Volledige ontzorging:** "Van inpakken tot uitpakken: alles is mogelijk."
- **Geen voorrijkosten:** "Altijd een helder en eerlijk tarief, zonder verrassingen."
- **Standaard verzekerd:** "Uw inboedel is automatisch gedekt tijdens de verhuizing."
- **Ervaren professionals:** "Geen studenten, maar vakmensen met jaren ervaring."
- **Snelle & flexibele planning:** "Van spoedklussen tot kosteloos wijzigen van uw verhuisdatum."

**Intro / positioning paragraph**
- "Bij Verhuisbedrijf De Reus krijgt u één vaste verhuisadviseur die met u meekijkt, meedenkt en uw verhuizing van begin tot eind organiseert."
- "Onze ervaren vakmensen werken zorgvuldig, transparant en leveren de kwaliteit die u mag verwachten, zonder verrassingen."

**Quote block bullets:** "Gratis" · "Vrijblijvend" · "Persoonlijk verhuisadvies van verhuisexperts" · "Reactie binnen 24 uur"

**CTAs**

| Where | Exact CTA text |
|---|---|
| Header button | "Offerte aanvragen" |
| Hero button | "Gratis offerte aanvragen" |
| Section buttons | "Offerte aanvragen" |
| Phone prompt | "Wilt u direct contact of heeft u een spoedklus? Bel ons dan op!" → "085 000 5647" |
| Closing CTA | "Klaar om uw verhuizing zorgeloos te regelen?" / "Vraag vrijblijvend een offerte aan." |
| Hero lead form (mobile) | "Ontvang gratis verhuisadvies en een vrijblijvende offerte op maat" / "Ontvang binnen 24 uur na aanvraag uw persoonlijke verhuisofferte:" / button "Aanvraag verzenden" |
| Quote section | "Vraag een offerte aan" / "Laat uw gegevens achter en wij nemen persoonlijk contact met u op om uw wensen voor de verhuizing te bespreken." |
| Quote form | "Vraag hier uw verhuisofferte aan:" / button "Verzenden" |
| Other form copy | "Ontvang een gratis en vrijblijvende offerte op maat" / "Laat uw gegevens achter en word binnen 24 uur gebeld door een van onze ervaren verhuisexperts." / "Wij denken met u mee, beantwoorden al uw vragen en stellen dezelfde dag een vrijblijvende offerte op maat voor u op." |
| Contact | "Wilt u iets bespreken of heeft u vragen over uw verhuizing?" / "Heeft u vragen of wilt u iets bespreken? Ons team staat voor u klaar!" / "Vul het contactformulier in en ontvang binnen 24 uur een reactie." |

**Social proof**
- "Klanten beoordelen ons met een 4.9/5"
- "Onze klanten zijn tevreden en daar zijn wij trots op. Dat is geen toeval, maar het resultaat van hard en zorgvuldig werken."

**Werkwijze (5 steps):** "Zo werkt het boeken van uw verhuizing:"
1. Offerte aanvragen: "Via het formulier laat u uw gegevens en verhuisdatum achter."
2. Persoonlijk contact: "Een van onze verhuisexperts neemt persoonlijk contact met u op om uw wensen en inboedel te bespreken."
3. Offerte ontvangen: "U ontvangt een duidelijke en vrijblijvende offerte, zonder verrassingen achteraf."
4. Planning bevestigen: "Na uw akkoord bevestigen wij de planning en regelen wij de rest."
5. Verhuisdag: "U kunt onze verhuizers verwachten op het afgesproken tijdstip. Wij verzorgen een professionele en zorgeloze verhuizing."

---

## 4. TONE OF VOICE

**Form of address:** always the formal **"u / uw"**. The site uses "u" 28 times and "uw" 23 times, with **zero** "je/jij". The company speaks as **"wij / ons / onze"**.

**Sentence style**
- Short, declarative, reassuring sentences.
- Headlines are often **tricolons or short fragments with full stops**: "Professionele verhuizers. Heldere prijzen. Altijd service op niveau." and "Sterk in verhuizen. Zorgeloos geregeld."
- Heavy use of **"Van X tot Y"** constructions and **title + colon/explanation** pairs.
- **Contrast framing:** "Geen studenten, maar vakmensen…" and "Dat is geen toeval, maar…"
- Benefit-first; no humour, no slang, no exclamation-heavy hype. The exceptions are "Bel ons dan op!" and "Ons team staat voor u klaar!".

**Typical words (with counts on the page)**
- zorgeloos/zorgeloze (11×)
- vrijblijvend (9×)
- persoonlijk (7×)
- professioneel/professionals (6×)
- ervaren (5×)
- helder / eerlijk / zonder verrassingen (5× each)
- zorgvuldig (4×)
- Also: vakmensen, verhuisexperts, ontzorging, op maat, transparant, betrouwbaar, "service op niveau"
- "offerte" appears 22×

**Real sentences (quoted)**
1. "De betrouwbare keuze voor een zorgeloze verhuizing."
2. "Sterk in verhuizen. Zorgeloos geregeld."
3. "Bij Verhuisbedrijf De Reus krijgt u één vaste verhuisadviseur die met u meekijkt, meedenkt en uw verhuizing van begin tot eind organiseert."
4. "Onze ervaren vakmensen werken zorgvuldig, transparant en leveren de kwaliteit die u mag verwachten, zonder verrassingen."
5. "Geen studenten, maar vakmensen met jaren ervaring."
6. "Altijd een helder en eerlijk tarief, zonder verrassingen."
7. "Onze klanten zijn tevreden en daar zijn wij trots op. Dat is geen toeval, maar het resultaat van hard en zorgvuldig werken."
8. "Na uw akkoord bevestigen wij de planning en regelen wij de rest."
9. "Wij denken met u mee, beantwoorden al uw vragen en stellen dezelfde dag een vrijblijvende offerte op maat voor u op."
10. "Wilt u direct contact of heeft u een spoedklus? Bel ons dan op!"

**Characterization:** polite, formal-but-warm Dutch service copy built around **reassurance** ("zorgeloos", "zonder verrassingen") and **trust through competence** ("professionals, geen studenten", "ervaren vakmensen", "betrouwbaar"). It is personal: one fixed adviser, personal contact, a team that "staat voor u klaar". The copy is plain and practical rather than witty. The "giant/strong" metaphor appears only in the footer line and the mascot, which leaves room for the brand book to lean into it **(inferred)**.

**Copy hygiene issues to fix in any new material**
- Typos: "Inbdoel", "Hnadymanservice", "Verhuislitservice", "verassingen" (a duplicate of step 3), "Klaar om u verhuizing" (duplicate block).
- Grammar: "een zorgeloos en geregelde verhuizing" should be "een zorgeloze en geregelde verhuizing".
- Spacing: stray spaces before punctuation, as in "verwachten , zonder".

---

## 5. CURRENT VISUAL IDENTITY

### Colors (exact values from the site CSS; usage confirmed by pixel-sampling the rendered page)

| Role | HEX | RGB | Wix token | Where it is used |
|---|---|---|---|---|
| **Primary / brand navy** | **#054A76** | 5,74,118 | `--color_20` | Header and footer background, all headings, body text, form submit button, CTA hover state. It is the most-used color in the site CSS (163 occurrences). |
| **CTA green** | **#319C5A** | 49,156,90 | `--color_24` | All "Offerte aanvragen" pill buttons and the full background of the quote form panel |
| Accent blue | **#287EDC** | 40,126,220 | `--color_22` | Filled check-circle icons in "Dit mag u van ons verwachten"; hover state of the header CTA |
| Light blue-grey (surface) | **#E2E8EF** | 226,232,239 | `--color_30` | Service tile cards; background of the reviews section |
| Light grey (section bg) | **#F0F0F0** | 240,240,240 | `--color_12` | USP bar, intro, "Dit mag u…" and quote sections (alternating with white) |
| Pale blue (lines/blobs) | **#CBDCE9** | 203,220,233 | n/a | Menu/item dividers. The illustration blob renders around #CCD7E6. |
| White | **#FFFFFF** | 255,255,255 | `--color_11` | Page background, text on navy and green, review cards, form inputs |
| Grey text | **#6E6E6E** | 110,110,110 | n/a | Italic USP-bar text |
| Black | **#000000** | 0,0,0 | n/a | Review body text, button hover borders |
| Star yellow (image) | ~#FFDE45 | n/a | n/a | Google 5-star rating graphic |
| Icon navy (raster icons) | ~#045185 | n/a | n/a | Service and process icons (PNG, close to the primary) |
| Mascot palette (illustration) | navy #055285 / cardboard #CA9C4E / skin #E4AC67 | n/a | n/a | The "De Reus" mover mascot |

Wix theme defaults such as #1A6AFF, #116DFF and #2B5672 also appear in the CSS. They belong to unused platform widgets (gallery and menu defaults) and are **not** brand colors.

### Typography

| Use | Font | Weights / sizes | Source |
|---|---|---|---|
| Headings (H1/H2, card titles, reviewer names) | **Wix Madefor Display** (theme font `madefor-display-bold`) | Bold. H2 is about 33px at a 1280px viewport, #054A76. H1 in the hero is white. | Wix-hosted; free on Google Fonts as "Wix Madefor Display" |
| Body copy, bullets, form intro | **Almarai** | 300 / 400 / 700 / 800 loaded; body is 400 at about 18 to 20px (desktop), #054A76; sub-heads are 700 | Google Fonts (served via the Wix font cache) |
| Buttons and some form labels | **Wix Madefor Text** (`madefor-text`) | 700 at 18px (section CTAs); 400 at 14px (header CTA) | Wix-hosted / Google Fonts "Wix Madefor Text" |
| Theme defaults (not visibly used) | DIN Next W01 Light | n/a | Wix theme default **(inferred: unused)** |
| Logo wordmark | Raster PNG, not live text. All-caps geometric sans with very wide tracking: "VERHUISBEDRIJF" bold, "DE REUS" light. | n/a | The file name "Jouw alineatekst.png" suggests it was made in Canva; the typeface looks like **Glacial Indifference** **(inferred)**. |

### Buttons

- **Primary CTA:**
  - Pill shape (`border-radius: 300px`), fill **#319C5A**, white text in Wix Madefor Text Bold 18px.
  - No border, 8px padding, about 42 to 50px high.
  - Hover: background changes to **#054A76** (header CTA: #287EDC) and a 1px black border appears; `transition: all 0.2s ease`.
- **Form submit** ("Verzenden" in the green panel): navy **#054A76** pill with white text.
- **Mobile lead-form submit** ("Aanvraag verzenden"): green pill.

### Radius, shadow and surfaces

- Cards use rounded corners of about 10 to 16px at a 1280px viewport. The radius scales with the viewport (0.8 to 1.3vw).
- The quote-form panel has about 15px radius; the green panel holds white inputs.
- **Review cards:** white, rounded, `box-shadow: 0 1px 4px rgba(0,0,0,.6)`.
- **Service tiles:** flat #E2E8EF, rounded, with no shadow.
- **Section rhythm:** alternating white, #F0F0F0 and #E2E8EF bands between a navy header and a navy footer.

### Imagery style

- **One photo only:** the hero is an aerial stock shot of two movers unloading boxes from an **unbranded white van** on paving, darkened with an overlay. The file name "Delivery Truck Movers Moving Furniture Loading Van_edited.jpg" suggests stock **(inferred)**.
- **Illustrations carry the brand:**
  - **Mascot "De Reus":** a muscular, faceless-ish cartoon mover in a navy cap, navy polo with the wordmark on the chest, navy work trousers and belt, carrying a cardboard box. Flat vector with dark outlines and soft shading.
  - Semi-3D render of moving boxes with a plant and a navy guitar on a pale-blue organic blob.
  - Isometric map with a route line and two navy location pins (in the Werkwijze section).
- **Not on the site:** no real photos of the team, the trucks/livery or the verhuislift.

### Icon style

- Single-color **navy** icons (raster PNG sprites).
- Service tiles: **solid/filled** glyphs (house, office building, map pin, globe with dashed orbit).
- Extra-service tiles: **outline/line** icons (broom and bucket, warehouse with boxes, crossed wrench and screwdriver, scissor-lift trolley).
- Werkwijze: **thin line** icons (web form, phone, document, handshake, fast truck, headset agent).
- Benefits: white check marks in filled **#287EDC circles**.
- The filled and line styles are mixed, so the icon set is **inconsistent**; the brand book should standardize it **(inferred recommendation)**.

### Current logo

1. **Header logo:** a text-only wordmark in **white** on navy. "VERHUISBEDRIJF" sits on one line in bold, widely tracked caps, with "DE REUS" centered below in light, widely tracked caps. It is a raster PNG with no symbol.
2. **Mascot lock-up:** the mascot stands above the same two-line white wordmark (file "De Reus logo shirt witte letters kopie.png"). The mascot's shirt and box also carry the small wordmark, and the box has a round house-and-truck badge.
3. No favicon or app icon exists.
4. A new logo is being introduced (session dereus-70).

---

## 6. TARGET AUDIENCE

- **Private households** moving in and from **Den Haag / Zuid-Holland**. "Particuliere Verhuizingen" comes first, and the forms ask for "Woonplaats" and "Toekomstige woonplaats" **(inferred)**.
- People who want everything taken off their hands: they value "zorgeloos", "volledige ontzorging", "één vaste verhuisadviseur" and a fixed, transparent price **(inferred)**.
- The formal "u", the focus on insurance and the **Woningontruiming** service suggest older customers, families and relatives clearing a parent's home **(inferred)**.
- **Small businesses and offices** ("Zakelijke Verhuizingen"; the AV mentions "klein zakelijk") **(inferred)**.
- **International movers** ("Internationale Verhuizingen") **(inferred)**.
- **Urgent moves:** "spoedklus", availability 7 days a week and up to 20:00 **(inferred)**.
- Reviews come from a mix of customers; one is written in informal Dutch ("Bedankt jongens") **(inferred)**.

---

## 7. OTHER

**Brand story / history**
- **None published.** The "Over ons" nav item points to the intro paragraph ("één vaste verhuisadviseur … ervaren vakmensen"). There is no founder story, no founding year and no "about" page.
- The name "De Reus" (the giant) plus the muscular mascot and "Sterk in verhuizen" form the implicit story: **strength and reliability** **(inferred)**.

**Team**
- No team page or photos.
- Reviews name movers **"Dennis", "Jack", "Vincent"** and **"Omar"**, for example "Dennis jack en Vincent. Bedankt voor de goede verhuizing." and "…maar Omar bleef altijd positief, vrolijk en professioneel." These names probably belong to crew members **(inferred)**.

**Reviews shown** (all 5★, "Geverifieerde Google-review")
- **Daniëlle Van haaften:** "…Zeer netjes gewerkt. Alles netjes neergezet. De montage liep vlekkeloos. Zeker een aanrader."
- **Charlie K:** "Deze jongens zijn de hardstwerkende, eerlijkste en liefste mensen die ik ooit had kunnen vinden…"
- **Mick Versnel:** "Verhuisbedrijf de Reus, absoluut top!! Netjes, voorzichtig en respectvol met m'n spullen! Een aanrader!"
- **Dennis Strijk:** "Goede en duidelijke communicatie, hele fijne samenwerking… Top professional en zou dit bedrijf zeker weer inhuren voor een volgende verhuizing!"

**Vehicles / livery**
- None shown. The only vehicle is the generic white van in the stock hero photo.
- The mascot's uniform (navy cap, polo and trousers with a white wordmark) is the only "uniform/livery" reference on the site.

**Social links**
- **None.** No Facebook, Instagram, LinkedIn, TikTok or WhatsApp.
- The only external link is Google reviews: `https://www.google.com/search?q=reviews+voor+verhuisbedrijf+de+reus` (Google local listing id `rldimm=11352664177406900012`).

**Structured data:** JSON-LD `LocalBusiness` (name, url, address, telephone) plus `WebSite`.

**Website issues worth knowing**
- The contact email link is broken ("nfo@").
- The site uses the default Wix favicon.
- Most images have the placeholder alt text "Pink Poppy Flowers".
- Five hidden Wix template stock photos (`8bb438_…`: lamp post, portraits, a tube, a landscape) are loaded but are not brand imagery.

### Usable image URLs (original resolution)

Local copies are in `brandbook/research/img/`.

| What | URL | Size | Local copy |
|---|---|---|---|
| **Current wordmark** (white, transparent PNG) | https://static.wixstatic.com/media/03c52e_5f26a841cdda40719722c5c6d0bb57ad~mv2.png | 1313×1313 | current-wordmark-white.png |
| **Mascot + wordmark lock-up** (white text, transparent) | https://static.wixstatic.com/media/03c52e_26016d0f0dab428cad88ef592fe5fd61~mv2.png | 1250×1250 | current-mascot-with-wordmark.png |
| **Mascot "De Reus"** (large, transparent) | https://static.wixstatic.com/media/03c52e_3278c64c0e954a5d8347b1cc7fbaea81~mv2.png | 1024×1536 | mascot-de-reus.png |
| Mascot's box (overlay piece) | https://static.wixstatic.com/media/03c52e_c82e673b49d948cfb61faac1ce516c8d~mv2.png | 625×625 | n/a |
| **Hero photo:** movers unloading a white van, aerial (stock) | https://static.wixstatic.com/media/03c52e_7844288c416946a2882ab7b4ba0abda9~mv2.jpg | 2710×1582 | hero-photo-movers-van.jpg |
| Illustration: boxes + plant + guitar on blob | https://static.wixstatic.com/media/03c52e_6bd73b3502e34b6e972f8e5ed0cbe96c~mv2.png | 813×813 | illustration-boxes-plant-guitar.png |
| Illustration: isometric map route with pins | https://static.wixstatic.com/media/03c52e_1726d49c4ad149d1a108678426538ea9~mv2.png | 1000×1000 | illustration-map-route.png |
| Icon sprite: 4 main services (house, building, pin, globe) | https://static.wixstatic.com/media/03c52e_18a05ced3b74448cbb99b8d10e0e8991~mv2.png | 563×563 | icons-services-main.png |
| Icon sprite: 4 extra services (broom, storage, tools, lift) | https://static.wixstatic.com/media/03c52e_1ac0961ebf9440c8ba0ef7bd3cb98adf~mv2.png | 500×500 | icons-services-extra.png |
| Icon sprite: werkwijze (form, phone, doc, handshake, truck, agent) | https://static.wixstatic.com/media/03c52e_16c8a7feab864d0dad50fc5ebde2d80d~mv2.png | 500×500 | icons-werkwijze.png |
| Google 5-star badge | https://static.wixstatic.com/media/03c52e_921116e61307416194a6a568d007bdf2~mv2.png | 1667×318 | n/a |
| Full-page desktop screenshot (1440px wide, captured 2026-09-18) | n/a | 1440×6732 | screenshot-desktop-2026-09-18.png |

**Imagery gap:** the site has **no real photos of trucks, the team or the verhuislift**. If the brand book needs these, the client must supply them; otherwise use clearly labelled stock or illustration **(inferred recommendation)**.

---

## 8. ALGEMENE VOORWAARDEN

- **Source:** "Algemene voorwaarden Verhuisbedrijf De Reus", **Versie 2025**. It is linked in the footer as "Algemene Voorwaarden":
  https://www.verhuisbedrijfdereus.nl/_files/ugd/03c52e_6264876606274b28a8cfdeb6721704cb.pdf
- **Local copy:** `brandbook/research/algemene-voorwaarden-dereus-2025.pdf`
- **The document:**
  - 3 pages and 15 articles.
  - It opens with "Op al onze offertes en overeenkomsten zijn deze voorwaarden van toepassing."
- **PDF metadata:**
  - Created 2026-02-24 by the ReportLab PDF Library, which suggests it was generated from code or a template rather than drafted by a lawyer **(inferred)**.
  - Author "(anonymous)". Server last-modified 2026-08-05.
- **Likely template:** the article titles and order (Definities, Werkingssfeer, Vooraf verstrekken van informatie, Gevaarlijke voorwerpen, Verhuisprijs, … , Nakomingsgarantie) follow the standard Dutch sector terms "Algemene Voorwaarden voor Verhuizingen". Most articles are cut down to one line **(inferred)**.

### 8.1 Company information in the AV

| Item | Found in AV? | Detail |
|---|---|---|
| Legal entity name | Partly | Only the trading name "Verhuisbedrijf De Reus", defined as "de opdrachtnemer die beroepsmatig consumenten en bedrijven verhuizingen verzorgt" (Art. 1.2) |
| Legal form (B.V., V.O.F., eenmanszaak) | **No** | n/a |
| KvK number | **No** | n/a |
| BTW number | **No** | n/a |
| Registered / postal address | **No** | The only address is the one on the website: Lau Mazirellaan 336, 2525 ZJ Den Haag |
| Founding or registration date | **No** | n/a |
| Other trade names | **No** | n/a |
| Memberships / certifications / keurmerk | **No** | No Erkende Verhuizers, OVB or geschillencommissie is named. Art. 15 is titled "NAKOMINGSGARANTIE" but contains no guarantee; its only text is "Op alle overeenkomsten is Nederlands recht van toepassing." |
| Insurer / policy | **No** | Coverage is described (Art. 3.3, Art. 13) but no insurer is named |
| Complaint procedure | **No** | Only "Schade moet direct op de verhuisdag worden gemeld." (Art. 12) |
| Applicable law | Yes | "Nederlands recht is van toepassing." (Art. 14, repeated in Art. 15) |
| Version / date | Yes | "Versie 2025" (cover); PDF created 2026-02-24 |

**Conclusion:** the AV fills **none** of the legal-identity gaps from section 1. KvK number, BTW number, legal form and founding year must come from the client or a KvK register lookup.

### 8.2 Key terms per article

| Art. | Title | What it says (quoted or close paraphrase) |
|---|---|---|
| 1 | ALGEMEEN/DEFINITIES | Defines klant, Verhuisbedrijf De Reus, verhuisovereenkomst ("goederenvervoer … binnen een gebouw en/of over de weg"), verhuisgoederen, inboedel, bedrijf |
| 2.1 | WERKINGSSFEER | Applies to "consumentenverhuizingen en klein zakelijk", within a building and/or "vervoer uitsluitend over de weg", "binnen, vanuit of naar Nederland" |
| 2.2 | WERKINGSSFEER | Not for uithuiszettingen |
| 3.1 and 3.2 | VOORAF VERSTREKKEN VAN INFORMATIE | De Reus estimates distance, volume and weight, and learns about "de aard van de verhuizing" |
| 3.3 | idem | "Verhuisbedrijf De Reus wijst de klant erop dat de verhuisgoederen tijdens de verhuizing automatisch volledig verzekerd zijn." |
| 3.4 | idem | "Indien de klant het nodig acht, is hij zelf verantwoordelijk voor een aanvullende verzekering." |
| 3.5 | idem | The customer must report all relevant details |
| 4 | GEVAARLIJKE VOORWERPEN OF PRODUCTEN | Dangerous goods must be reported in advance; unreported ones are refused; costs and damage are for the customer; "Gasleidingen worden niet af- of aangesloten."; "Dieren worden niet verhuisd." |
| 5 | VERHUISPRIJS | "all-in prijs of regieprijs"; "Meer- en minderwerk wordt verrekend."; "Extra kosten worden doorbelast." |
| 6 | SLUITEN VAN DE OVEREENKOMST | The contract starts on "acceptatie van de offerte of feitelijke aanvang" |
| 7 | BETALING | "Betaling geschiedt op de verhuisdag, tenzij anders overeengekomen." |
| 8 | WIJZIGEN, ANNULEREN, OPZEGGEN | Cancelling up to 2 weeks before costs "€ 250,-"; within 2 weeks "aanvullende kosten … conform deze voorwaarden" (no amounts are given anywhere). Despite the title, **changing** the date is not covered. |
| 9 | VERPLICHTINGEN | "Zorgvuldige en tijdige uitvoering van de verhuizing." |
| 10 | AANSPRAKELIJKHEID | "Aansprakelijkheid is beperkt conform deze voorwaarden." |
| 11 | AANSPRAKELIJKHEID VAN DE KLANT | The customer is liable for wrong information or negligence |
| 12 | SCHADEMELDING | "Schade moet direct op de verhuisdag worden gemeld." |
| 13 | SCHADEVERGOEDING | "Maximale vergoeding €23.000 per inboedel. Eigen risico €500." |
| 14 | GESCHILLEN | "Nederlands recht is van toepassing." No geschillencommissie or court is named. |
| 15 | NAKOMINGSGARANTIE | Only repeats Dutch law; no actual guarantee |

### 8.3 Website promises checked against the AV

| Website promise (exact) | AV | Verdict | Honest phrasing for the brand book |
|---|---|---|---|
| "Inbdoel standaard verzekerd" / "Uw inboedel is automatisch gedekt tijdens de verhuizing." | Art. 3.3 says "automatisch volledig verzekerd", **but** Art. 13 caps it at € 23.000 per inboedel with € 500 eigen risico; Art. 3.4 makes extra cover the customer's job; Art. 12 requires reporting on the day | **Limited.** "Volledig" is not accurate: there is a cap and a deductible. The AV also contradicts itself. | "Uw inboedel is standaard verzekerd tijdens de verhuizing (tot € 23.000, eigen risico € 500)." Avoid "volledig verzekerd". |
| "Geen voorrijkosten" / "Altijd een helder en eerlijk tarief, zonder verrassingen." | Voorrijkosten are not mentioned (so not contradicted), but Art. 5.2 "Meer- en minderwerk wordt verrekend." and Art. 5.3 "Extra kosten worden doorbelast." | **Limited.** "Zonder verrassingen" holds only for an all-in price; with a regieprijs, or when extra work comes up, costs can rise. | "Geen voorrijkosten. U krijgt vooraf een heldere prijs; meerwerk bespreken wij altijd eerst met u." The last clause is only true if the client confirms it **(inferred)**. |
| "U ontvangt een duidelijke en vrijblijvende offerte, zonder verrassingen achteraf." | Art. 6: the contract starts on acceptance; Art. 5.2 and 5.3 as above | **Partly limited.** The offerte is vrijblijvend (OK), but "zonder verrassingen achteraf" conflicts with Art. 5.3. | Keep "vrijblijvende offerte"; soften "zonder verrassingen achteraf" or pair it with an all-in price. |
| "Snelle & flexibele planning: Van spoedklussen tot kosteloos wijzigen van uw verhuisdatum." | Art. 8 is titled "WIJZIGEN, ANNULEREN, OPZEGGEN" but only regulates cancellation: € 250 even when cancelling more than 2 weeks ahead, plus unspecified extra costs within 2 weeks | **Unclear / at risk.** Free rescheduling is not guaranteed in the AV, and customers may confuse rescheduling with cancelling, which is never free. | Only keep "kosteloos wijzigen" if the client confirms it and adds it to Art. 8. Otherwise use "flexibel meedenken bij het wijzigen van uw verhuisdatum". **Open question for client.** |
| "Volledige ontzorging: Van inpakken tot uitpakken: alles is mogelijk." | Art. 4.2 (unreported dangerous goods refused), 4.4 (no gas connections), 4.5 (no animals) | **Limited.** "Alles is mogelijk" is not literally true. | "Van inpakken tot uitpakken: wij regelen het voor u." |
| "Reactie binnen 24 uur" / "binnen 24 uur gebeld" / offerte "dezelfde dag" | Not in the AV | **Service promise only, not contractual.** Fine to use if the business can deliver it **(inferred)**. | Keep as is; make sure operations can meet it. |
| "Vrijblijvende offerte & verhuisadvies" / "Gratis" | Art. 6: no contract until acceptance or actual start | **Consistent.** | Keep. |
| "Internationale Verhuizingen" | Art. 2.1: the AV only covers moves "binnen, vanuit of naar Nederland" and "vervoer uitsluitend over de weg" | **Consistent for road moves to and from NL.** Sea or air transport and moves between two foreign countries fall outside these terms **(inferred)**. | "Internationale verhuizingen van en naar Nederland." |
| "Zakelijke Verhuizingen" | Art. 2.1 covers only "klein zakelijk" | **Limited.** Large office relocations are not covered by these terms **(inferred)**. | Position as "verhuizingen voor kantoren en kleine bedrijven" unless the client has separate B2B terms. |
| "Tijdelijke opslag", "Woningontruiming", "Handymanservice", "Verhuisliftservice" | Not covered: the AV only regulates the verhuisovereenkomst (transport of goods, Art. 1.3) | **Gap.** No terms exist for storage (liability, duration, insurance), clearance or handyman work **(inferred)**. | Brand book can list the services, but make no guarantees (insurance, prices) for them until the client has terms. |
| "Ervaren professionals" / "zorgvuldig" | Art. 9: "Zorgvuldige en tijdige uitvoering van de verhuizing." | **Consistent.** | Keep. |
| Payment | Art. 7: payment on the moving day | Not on the website | Could be stated as a transparency point, e.g. "U betaalt pas op de verhuisdag." **(inferred suggestion)** |

### 8.4 Open questions for the client (from the AV)

1. What is the legal entity and legal form? What are the KvK and BTW numbers? These are needed for the footer, invoices and the brand book colophon.
2. Which insurer covers the inboedel, and is the cover really "volledig" or capped at € 23.000 (Art. 3.3 vs Art. 13)?
3. Is changing the moving date really free ("kosteloos wijzigen")? If so, add it to Art. 8.
4. What are the "aanvullende kosten" for cancelling within 2 weeks (Art. 8.3)? The AV gives no amounts.
5. Is there a complaint procedure or a geschillencommissie? Art. 15 "Nakomingsgarantie" is empty.
6. Are there separate terms for opslag, woningontruiming, handyman work and large business moves?
7. Any memberships or keurmerken (for example Erkende Verhuizers) that the brand may mention? The AV names none.
