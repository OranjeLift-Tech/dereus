# Inventarisatie: welke secties kunnen een beeld dragen

Opgesteld 21 september 2026. Dit is een voorstel, niet uitgevoerd. Er is niets gegenereerd en niets aan de site gekoppeld.

Buiten beschouwing gelaten, daar wordt nu aan gewerkt: de acht dienstsecties op /diensten/, de hero en alle paginakoppen (`hero`, `kop`), de footer, op /werkwijze/ de blokken `stappenlang` en `checklist`, en het WhatsApp-icoon.

## Wat de randvoorwaarden toelaten

`website/review/design-notes.md` A3 legt vast: geen stockfoto's met onbekende mensen, nergens. A2 laat zien wat dat kost, de oude herofoto is om precies die reden afgekeurd. Voor alles met mensen erin zijn er dus twee routes:

- **gegenereerd**, kan deze week. De teamuitsnede staat er al (`img/team/team-hero-1600.webp`) en sinds vandaag ook vijf klantenservicebeelden in `beeld-opties/klantenservice-20260921/`.
- **fotoshoot**, die nog niet heeft plaatsgevonden. Alles wat de echte mensen, het echte kantoor of de echte wagen moet tonen, wacht daarop.

Gewichtsbudget: `_werk/bewakers.py` waarschuwt boven 250 KB per beeld. Drie dienstfoto's zitten daar nu boven (`dienst-verhuislift.webp` 450 KB, `dienst-particulier.webp` 334 KB, `dienst-internationaal.webp` 277 KB), alle drie op een pagina die buiten deze inventarisatie valt. `verwachten-inpakken.webp` zit met 243 KB vlak tegen de grens aan. Elk nieuw beeld moet dus eerst door de exportroute naar webp op maat. De vijf nieuwe klantenservicebeelden zijn 2,4 tot 3,0 MB als bron-jpg, die kunnen er niet rechtstreeks op.

## De korte lijst: vijf plekken die het verdienen

Dit is waar ik zelf mee zou beginnen. De rest van de tabel legt uit waarom de andere secties het niet verdienen.

| # | Plek | Wat het is | Route |
|---|---|---|---|
| 1 | home `#contact`, blok `homecontact` | Vervangen, niet toevoegen. Hier staat nu `img/contact-klantenservice.webp`, een stockfoto van een onbekende vrouw met headset. Dat is precies wat A3 verbiedt en het staat live op de homepage. | gegenereerd, kan nu |
| 2 | /over-ons/ `#verhaal`, blok `over-ons` | Het huisvenster toont nu het beeldmerk omdat `config.FEITEN["TEAM_BEELD"]` op `None` staat. Een overonspagina zonder enig beeld van het bedrijf is het grootste gat op de site. De schakelaar ligt klaar. | gegenereerd nu, echte teamfoto na de shoot |
| 3 | /offerte/ `#formulier`, blok `formulier` | De zijkolom heeft al een beeldslot (`_zijkolom`, parameter `beeld`). Op de home is het gevuld met `aanvraag-foto-uit.webp`, op /offerte/ zelf blijft het leeg. Eén regel in `_werk/paginas/offerte.py`. | gegenereerd, kan nu |
| 4 | /contact/ `#formulier`, blok `formulier` | Zelfde slot, zelfde leegte. Controleer wel of de kopij een `zij-kop` heeft, zonder dat veld valt de hele zijkolom weg. | gegenereerd, kan nu |
| 5 | /kosten/ `#opbouw`, blok `opbouw` | /kosten/ is de enige pagina die onder de kop geen enkel beeld heeft. Dit blok is ook het langste en droogste van de site. Maar let op: dit vraagt geen foto. Zie de toelichting hieronder. | geen beeldproductie nodig |

### Toelichting per plek

**1. homecontact.** Liggend, 3:2, mensen in beeld. Wat het moet tonen: een De Reus-medewerker met headset aan het bureau, de persoon die de klant aan de lijn krijgt. Het beeld zit rechtsboven het contactformulier, boven het bericht, in een compositie met een tweede laag (`contact-uit.webp`) en een geel accent. Past zonder verbouwing, de markup is er al en werkt met twee lagen. Van de vijf nieuwe kandidaten sluiten `01-telefoon-aannemen` en `05-klantenservice-werkplek` hier het beste op aan. De uitsnedelaag moet dan opnieuw gemaakt worden.

**2. over-ons #verhaal.** Staand tot vierkant, ongeveer 1200 x 1140, mensen in beeld. Wat het moet tonen: het team, of een deel ervan, herkenbaar in bedrijfskleding. Het staat rechts naast de tekst in een huisvormig venster met daaronder de adresregel. Past zonder verbouwing: zet `TEAM_BEELD` op een pad en `over-ons.py` schakelt zelf van beeldmerk naar foto. Belangrijk: het blok noemt het beeld "Het team van De Reus". Zolang het een gegenereerd beeld is, claimt dat een teamidentiteit die niet op een echte foto berust. Dat is een keuze die de gebruiker bewust moet maken, niet iets dat ik stilletjes inschakel.

**3 en 4. De formulierzijkolommen.** Staand, 640 x 954, mensen in beeld. Wat het moet tonen: één medewerker, rustig, geen actie, want het beeld staat naast een lijstje vinkjes en een telefoonnummer. Op /offerte/ past de adviseur die de aanvraag leest, op /contact/ dezelfde persoon of de collega aan de telefoon. Past zonder enige verbouwing, alleen een pad meegeven. Dit is de goedkoopste winst op de hele lijst.

**5. kosten #opbouw.** Hier zou ik geen foto plaatsen. Een foto legt geen prijs uit. Wat dit blok mist is geen sfeer maar houvast: de prijsfactoren staan nu als genummerde kaarten zonder enig symbool, terwijl de site al een complete iconenset heeft die elders wel gebruikt wordt (`waarom`, `kernwaarden`, `vertrouwensrij`). Een icoon per factor, of een klein schema bij het duo all-in tegenover regie, doet wat een foto hier niet kan. Kost niets aan bandbreedte en vraagt geen productie. Wil de gebruiker er per se een foto bij, dan is `02-offerte-doornemen` uit de nieuwe reeks de enige die inhoudelijk klopt, liggend 3:2, boven het blok in een eigen witte strook. Dat vraagt wel nieuwe CSS.

## De volledige tabel

| Pagina | Blok | Heeft al beeld | Helpt een beeld | Waarom |
|---|---|---|---|---|
| home | `waarom` | ja, `verwachten-inpakken.webp` | n.v.t. | Staat er al, 243 KB, vlak tegen het budget. Niet aanraken, wel in de gaten houden bij een herexport. |
| home | `cijfers` | nee | **nee** | Een smalle cijferband die in één oogopslag gelezen wordt. Een beeld erin breekt precies het ritme dat het blok zijn werk laat doen. |
| home, /diensten/, /over-ons/ | `reviews` | nee, avatars zijn initialen | **nee, uitdrukkelijk** | De avatars zijn bewust letters en geen foto's (`reviews.py`, regel 2). Een gezicht bij een met naam genoemde klant is erger dan stock: het plakt een verzonnen gezicht op een echt persoon. Niet doen, ook niet gegenereerd. |
| home | `over-ons` (teaser) | ja, tweelaagse compositie | nee | Al gevuld en het verwijst door naar /over-ons/, waar het echte beeld hoort. |
| home, /over-ons/, /werkgebied/, plaatspagina's | `werkgebied` | ja, `kaart-den-haag.svg` | nee | De kaart ís het beeld, en hij is licht. Een foto erbij maakt het blok tweekoppig. |
| home | `aanvraag` (formulier) | ja, `aanvraag-foto-uit.webp` | nee | Slot al gevuld. |
| home | `homecontact` | ja, maar fout | **ja, vervangen** | Zie plek 1. |
| /werkwijze/ | `verhuisdag` | nee | **nee** | Direct erboven staat `stappenlang` met vijf stapbeelden. Nog een foto maakt van de pagina een fotostrip. Bovendien is dit een Koningsblauwe band met dakrand, een foto daarbinnen vecht met de band. De gouden stippenroute doet het visuele werk al. |
| home, /werkwijze/, /kosten/, /contact/, dienstpagina's | `vragen` | nee | **nee** | Details en summary, bedoeld om te scannen. De linkerkolom draagt al de belkaart met de bereikbaarheidsstatus. Een beeld duwt de vragen omlaag zonder iets toe te voegen. |
| /kosten/ | `antwoord` | nee | **nee** | Dit is het directe antwoord op de vraag van de pagina, in een kaart met ankerchips. Het moet in twee seconden gelezen zijn. |
| /kosten/ | `opbouw` | nee | **ja, maar geen foto** | Zie plek 5. |
| /kosten/ | `treden` | nee | **nee** | Drie traptreden klein, midden en groot. De trapvorm is zelf de illustratie. Drie foto's erbij is drie keer het budget, en één foto die "klein, midden en groot" eerlijk laat zien bestaat niet. |
| /kosten/ | `annuleren` | nee | **nee** | Een tipvak met regels uit de algemene voorwaarden. Beeld bij voorwaarden leidt af van tekst die precies gelezen moet worden. |
| /over-ons/ | `over-ons` (`#verhaal`) | alleen het beeldmerk | **ja** | Zie plek 2. |
| /over-ons/ | `kernwaarden` | nee, wel iconen | **nee** | Koningsblauwe band met genummerde kaarten en merkiconen. Vol genoeg, en een foto in een gekleurde band werkt hier net zo slecht als bij `verhuisdag`. |
| /over-ons/, /contact/ | `contactband`, `na-bericht` | huisvenster met beeldmerk | nee, maar let op | Beide gebruiken het beeldmerkmotief als vervanger tot er eigen foto's zijn. Komt er een shoot, dan zijn dit de eerste kandidaten om het motief te vervangen. Nu niet, anders staat hetzelfde gezicht op vier plekken. |
| /contact/ | `vertrouwensrij` | nee, wel iconen | **nee** | Vier compacte kaarten met icoontegels, direct onder de kop. Dit blok moet licht en snel zijn. |
| /contact/ | `kaart` | ja, `kaart-den-haag.svg` | nee | De kaart is het beeld. |
| /contact/ | `contactkaarten` | nee, wel iconen | **nee** | Kanaalkaarten met telefoon, mail en adres. Iconen zijn hier functioneel, een foto zou de scanbaarheid verpesten. |
| /contact/ | `formulier` | nee, slot leeg | **ja** | Zie plek 4. |
| /offerte/ | `formulier` | nee, slot leeg | **ja** | Zie plek 3. |
| /offerte/ | `stappen-na-aanvraag` | nee | **nee** | Drie korte stappen plus de Google-pil, onderaan de pagina na een lang formulier. Wie hier is, is klaar. Niet nog iets laden. |
| dienstpagina's | `watwijdoen` | ja, merkicoon in huiskader | **nee** | Het icoon in het huisvormige kader is het eigen systeem van de site. Er een foto van maken dupliceert de dienstfoto's die op /diensten/ al staan, en dat zijn net de drie zwaarste bestanden. |
| plaats- en landpagina's | `feitenkaart` | nee | **nee** | Een tabel met lokale feiten en links naar de gemeente. Data, geen sfeer. |
| dienst-, plaats- en landpagina's | `verwant` | nee, wel diensticonen | **nee** | Een rij doorverwijskaarten met iconen. Vier foto's in een rij die alleen maar wegwijst, is vier keer laden voor niets. |

## Wat dit bij elkaar betekent

Vier plekken waar een beeld echt iets toevoegt, plus één plek die iconen nodig heeft in plaats van een foto. Drie van die vier kunnen deze week, met wat er al ligt, en bij twee ervan is het één regel in een paginabestand.

De rest van de site is niet beeldloos uit luiheid, maar omdat de iconenset, de kaarten en de gekleurde banden dat werk al doen. Op elke sectie een foto plakken maakt de site niet interessanter, alleen zwaarder en rommeliger, en het zou ook het enige echte probleem verdoezelen dat deze ronde aan het licht kwam: er staat nog een stockfoto van een onbekende op de homepage.
