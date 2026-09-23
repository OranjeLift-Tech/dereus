# Bouwplan website Verhuisbedrijf De Reus

- **Versie:** 1.0, 18 september 2026. Eigenaar: dereus-55 (hoofdbouwer).
- **Basis:** de site van de teamgenoot in de root van deze repo (commit `504b21b`), omgebouwd volgens `website/STIJLANALYSE.md` (hoofdstuk 6 is het doelbeeld, 7.5 de verbeterlijst) en `sitemap/SITEMAP.md` v1.2.
- **Git:** branch `feature/rebuild-huisstijl` (lokaal, de repo is publiek). **Niemand** draait `git add`, `commit`, `push`, `checkout`, `stash`, `reset` of `clean`. Alleen dereus-28 doet git. Wij bewerken alleen bestanden.
- **Regel nummer 1:** elke sessie schrijft alleen in de bestanden die hieronder (hoofdstuk 5) aan haar zijn toegewezen. Iets nodig in een bestand van een ander? Stuur een bericht aan de eigenaar.

---

## 1. Architectuur in het kort

- **Statische site**, één `index.html` per map, adressen met een schuine streep aan het eind (`/diensten/`). `vercel.json` met `trailingSlash: true`.
- **Bouwstap in Python 3, alleen standaardbibliotheek**, in `_werk/`. Eén commando: `python _werk/build.py`. Het schrijft alle pagina's naar de root (`index.html`, `diensten/index.html`, ...), zodat de huidige deploy-root blijft werken.
- **Eén bron voor menu en footer:** `_werk/navigatie.py`. Header, topbalk, drawer, footer en mobiele belbalk worden bij elke build in elke pagina gezet (zoals Brocken).
- **Blokken als componenten:** elk blok is een Python-functie die HTML teruggeeft, met eigen CSS en eventueel eigen JS. Een pagina is een lijst blokken. De build laadt per pagina alleen de CSS en JS van de blokken die erop staan.
  - **Anders dan Brocken:** Brocken knipt gedeelde stukken met regexen uit de gebouwde home. Wij doen dat niet: elk gedeeld stuk is een gewone functie. Dat is voorspelbaar met vijf sessies tegelijk en breekt niet als iemand de home aanpast.
- **Tokens:** `css/tokens.css` is een kopie van `brandbook/tokens.css` (waarden 1-op-1, alleen de fontpaden aangepast). Nooit linken naar `brandbook/`: die map gaat niet mee naar productie.
- **Tekst:** alle zichtbare tekst komt uit `website/content/*.md` (dereus-4e), in het formaat van hoofdstuk 7. Geen tekst hard in de Python, behalve vaste gegevens uit `config.py` (telefoon, adres, tijden).
- **JS:** vanilla, `defer`, geen frameworks, geen bundler. Eén kernscript plus kleine blokscripts.
- **Lettertypes:** zelf gehost in `fonts/`: Archivo (breedte 75, gewicht 700 tot 800) en Inter, latin en latin-ext, woff2. Twee preloads (de twee `-latin`-bestanden). Geen Google Fonts-link.

## 2. Mappen en bestanden

```
/                              root = deploy-root
├── index.html                 GEBOUWD (home)
├── diensten/index.html        GEBOUWD
├── kosten/index.html          GEBOUWD
├── offerte/index.html         GEBOUWD
├── offerte/bedankt/index.html GEBOUWD (noindex)
├── contact/index.html         GEBOUWD
├── contact/bedankt/index.html GEBOUWD (noindex)
├── algemene-voorwaarden/index.html   GEBOUWD
├── privacyverklaring/index.html      GEBOUWD
├── 404.html                   GEBOUWD (noindex)
├── robots.txt  sitemap.xml    GEBOUWD (door _werk/seo.py)
├── vercel.json  .vercelignore HANDWERK (dereus-e7)
├── css/
│   ├── tokens.css             kopie merkboek (dereus-55)
│   ├── style.css              kernlaag (dereus-55)
│   ├── blok/<naam>.css        één bestand per blok (eigenaar van het blok)
│   └── min/                   GEBOUWD: site.min.css (tokens + kern) en <naam>.min.css per blok
├── js/
│   ├── site.js                kernscript (dereus-55)
│   ├── blok/<naam>.js         optioneel, één per blok (eigenaar van het blok)
│   └── min/                   GEBOUWD (alleen gekopieerd, niet verkleind)
├── fonts/                     woff2 (dereus-55)
├── img/                       bestaande beelden van de basis-site (niet hernoemen)
│   ├── logo/                  GEBOUWD: kopie uit brandbook/assets/logo(-v2)/
│   ├── iconen/                GEBOUWD: kopie van brandbook/assets/imagery/icoon-*.svg
│   └── og.jpg                 1200 x 630 (dereus-55)
├── _werk/                     bouwstraat, gaat NIET naar productie (.vercelignore)
│   ├── build.py               ingang (dereus-55)
│   ├── config.py              vaste gegevens en schakelaars (dereus-55)
│   ├── navigatie.py           menu, footer, topbalk, drawer (dereus-55)
│   ├── kit.py                 hulpfuncties voor alle blokken (dereus-55)
│   ├── kopij.py               leest website/content/*.md (dereus-55)
│   ├── bewakers.py            controles, build faalt bij een fout (dereus-55)
│   ├── seo.py                 sitemap.xml en robots.txt (dereus-e7)
│   ├── jsonld.py              JSON-LD per pagina (dereus-e7)
│   ├── paginas/<naam>.py      één module per pagina (eigenaar van de pagina)
│   └── blokken/<naam>.py      één module per blok (eigenaar van het blok)
└── website/content/*.md       alle teksten (dereus-4e)
```

De oude bestanden van de basis-site zijn verwijderd. De gebruiker besloot op 21-09-2026 dat de dode CSS in de wortel van `css/` weg mocht en bevestigde daarna hetzelfde voor de dode JS. Daarmee gingen ook de bestanden weg die hier eerder met name stonden: `css/hero.css`, `css/3d.css`, `css/rit.css`, `css/werkwijze.css`, `js/3d.js`, `js/hero.js`, `js/rit.js` en `js/main.js`. In totaal veertien CSS en acht JS. In de wortels staan nu alleen nog `css/style.css`, `css/tokens.css` en `js/site.js`; al het andere hoort in `css/blok/` en `js/blok/`. Hierover staat dus niets meer open.

`img/avatar-*.webp` stond in dezelfde regel maar valt hierbuiten. Die vier beelden staan er nog en daarover is niets besloten. **Niet verwijderen**: dat beslist de gebruiker, via dereus-28.

## 3. De build-API

### 3.1 Een pagina declareren (`_werk/paginas/<naam>.py`)

```python
from kit import Pagina

PAGINA = Pagina(
    pad="/diensten/",              # adres, met schuine streep; bestand wordt diensten/index.html
    kopij="diensten",              # website/content/diensten.md
    header="transparant",          # "transparant" (over een donkere kop of hero) of "vast"
    noindex=False,                 # True voor bedankt en 404
    in_sitemap=True,
    body_klasse="p-diensten",
    preload_beeld=None,            # of {"src": "/img/...", "srcset": "...", "sizes": "..."} voor de hero
    blokken=[
        ("kop", {"id": "top"}),                    # (bloknaam, opties)
        ("dienstenpanelen", {}),
        ("reviews", {"variant": "compact"}),
        ("offertepil", {"variant": "los"}),
    ],
)
```

- `titel` en `beschrijving` komen uit de voorkant van het kopijbestand (hoofdstuk 7). De bewaker controleert de lengte.
- De build zet om de blokken heen: `<head>`, skiplink, topbalk, header, drawer, `<main id="inhoud" tabindex="-1">`, footer, mobiele belbalk, de icoonsprite (alleen de gebruikte iconen) en de scripts.
- JSON-LD: de build roept `jsonld.voor(pagina, ctx)` aan (dereus-e7). Geeft die `None`, dan komt er geen JSON-LD.

### 3.2 Een blok maken (`_werk/blokken/<naam>.py`)

```python
NAAM = "dienstenpanelen"          # gelijk aan de bestandsnaam
CSS = True                        # css/blok/dienstenpanelen.css bestaat
JS = True                         # js/blok/dienstenpanelen.js bestaat (anders False)
AFHANKELIJK = ["formulier"]       # optioneel: andere blokken waarvan de CSS/JS ook mee moet

def html(ctx, kopij, **opties) -> str:
    """kopij = het blok uit het kopijbestand met dezelfde id (of opties["kopij_id"])."""
    k = kopij
    return f'''<section class="b-{NAAM} sectie sectie--mist" id="{k.id}" aria-labelledby="{k.id}-kop">
      <div class="wrap">
        {ctx.label(k.veld("label"))}
        <h2 class="h2" id="{k.id}-kop">{ctx.inline(k.kop)}</h2>
        ...
      </div>
    </section>'''
```

- **`ctx`** (uit `kit.py`) geeft: `ctx.cfg` (config), `ctx.pagina`, `ctx.esc(tekst)`, `ctx.inline(tekst)` (vet, links, markering), `ctx.alineas(lijst)`, `ctx.label(tekst, op_donker=False)`, `ctx.knop(tekst, href, soort="cta"|"blauw"|"wit"|"link")`, `ctx.icoon(naam, klasse="")` (lijnicoon uit de sprite; registreert gebruik), `ctx.dienst_icoon(sleutel, inline=False)` (gevuld tweekleurig icoon uit `img/iconen/`), `ctx.beeld(src, alt, b, h, lui=True, sizes=None, srcset=None)` (altijd `width`, `height`, `loading="lazy"` en `decoding="async"` behalve als `lui=False`), `ctx.logo(variant)` (pad uit de logovariabele), `ctx.tel`, `ctx.telhref`, `ctx.mail`.
- **Kopij-object:** `k.id`, `k.kop` (de tekst van de `#`- of `##`-kop; bij een item de `###`-titel, ook als `k.veld("titel")`), `k.veld(naam, standaard=None)`, `k.tekst` (lijst alinea's), `k.lijst` (lijst regels), `k.items` (lijst kopij-objecten voor `###`-items), `k.item(id)`. Een verplicht veld dat ontbreekt geeft een duidelijke bouwfout met bestand en blok.
- **Een blok op meer pagina's:** hetzelfde blok, andere `opties` en andere kopij. Voorbeeld: `("vragen", {"kopij_id": "vragen"})` op `/kosten/` leest `## vragen` uit `kosten.md`.

### 3.3 Draaien

- `python _werk/build.py` bouwt alles en draait daarna de bewakers. Faalt een bewaker, dan stopt de build met een foutcode en een lijst. Is er sinds de vorige build niets aan de invoer en niets aan de uitvoer veranderd, dan meldt hij "niets te doen" en stopt in 0,11 seconde. Een volledige build duurt 0,37 seconde.
- `python _werk/build.py --alleen /diensten/` bouwt één pagina (plus de gedeelde bestanden).
- `python _werk/build.py --alles` negeert de cache en bouwt alles opnieuw.
- `python _werk/build.py --droog` rendert alles en draait de bewakers, maar schrijft niets; het sluit af met de lijst bestanden die een echte build zou aanraken. Het neemt geen slot, dus dit mag altijd.
- **Naast andere sessies bouwen mag sinds 22-09-2026.** Een slot in `_werk/.build.lock` met de sessienaam erin houdt twee builds uit elkaar: de tweede stopt met exitcode 3 en noemt de houder. Elk bestand gaat atomair naar schijf (tijdelijk bestand plus hernoemen), zodat een gelijktijdige lezer nooit een halve pagina ziet. Identieke inhoud wordt niet herschreven, ook niet bij het kopiëren van de logo's en iconen. En de build onthoudt in `_werk/.bouwcache.json` wat hij zelf geschreven heeft; staat een bestand daarna anders op schijf, met de hand gespliced bijvoorbeeld, dan noemt hij dat bestand bij naam voordat hij het overschrijft.
- **De generator blijft de bron.** Een build draait handwerk in de gebouwde HTML altijd terug, hij zegt het nu alleen hardop. Zet een wijziging dus in `_werk/blokken/` of `_werk/paginas/` en niet in de uitvoer. Zo ging het mis met de teamfoto op `/contact/` (commit 7fe41fb): die stond alleen in `contact/index.html` en niet in `formulier.py`, en was bij de eerstvolgende build verdwenen.
- `python _werk/build.py --serve` bouwt en start een lokale server op http://127.0.0.1:8000 (met `trailingSlash`-gedrag).
- Screenshots: headless Edge (`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`), 1440 en 390 px. **Kijk naar je screenshots.**

### 3.4 Controleren

`node _werk/controle.cjs` draait de hele keten: layout, headers, wereld, werkwijze en `controle-beelden.py`. Het start zelf een server op een vrije poort, zoekt zelf Playwright en deelt één browser, dus er hoeft niets klaargezet te worden.

- `node _werk/controle.cjs layout headers` doet alleen die checks; `--snel` neemt twee breedtes in plaats van vijf; `--serie` draait ze achter elkaar in plaats van tegelijk; `--basis http://127.0.0.1:8012` gebruikt een server die al draait.
- Elk script draait ook los, met dezelfde argumenten als altijd: `node _werk/controle-layout.cjs [pad-naar-playwright] [basis-url]`. Beide argumenten mogen nu weg.
- **Een run stopt niet bij de eerste fout.** De asserts zijn zacht (`_werk/controle-kit.cjs`): een fout wordt opgeschreven met de eenheid waarin hij viel en de sweep loopt door, zodat één run de hele lijst geeft in plaats van alleen het eerste geval. De afsluitcode is nog steeds 1 zodra er iets rood is.
- Raakt een verandering een klassenaam waar `controle-layout.cjs` op toetst, werk dat script dan in dezelfde verandering bij en draai het groen voordat je oplevert.

## 4. Naamgeving en conventies

- **Taal:** Nederlands in bestandsnamen, classes, variabelen en commentaar (zoals Brocken en De Kievit).
- **Classes:** kernlaag zonder voorvoegsel (`.wrap`, `.sectie`, `.knop`, `.label`, `.kaart`, `.h2`); blokken met `b-<naam>` en BEM: `.b-reviews`, `.b-reviews__kaart`, `.b-reviews__kaart--uitgelicht`. Paginaclasses op `<body>`: `p-<naam>`. Toestanden: `.is-open`, `.is-vast`, `.is-actief`.
- **Kleuren alleen via tokens** (`var(--brand-primary)`, `var(--color-cta)`, ...). Geen losse hex-waarden in blok-CSS; de bewaker waarschuwt.
- **Ondergrond per sectie:** `.sectie--wit`, `.sectie--mist`, `.sectie--blauw` (Koningsblauw), `.sectie--diep` (Diepblauw). Per pagina hoogstens één blauwe en één diepblauwe band met `.dakrand`, en die grenzen nooit aan elkaar.
- **Koppen:** Archivo Condensed 800 in zinsnaamval (H3 700). Hoofdletters alleen in één display-regel van hoogstens 5 woorden en in labels. Eén H1 per pagina.
- **Knoppen:** pil, Inter 700, 17 px, minstens 48 px hoog. De CTA-knop (`.knop--cta`, groen met witte tekst, besluit gebruiker) alleen voor "Offerte aanvragen", hooguit één per blok. Kleuren alleen via `--color-cta`, `--color-cta-text`, `--color-cta-hover` en `--color-cta-active`; op Koningsblauw en Diepblauw krijgt de knop een lichte ring (`--color-cta-rand`). Goudgeel is alleen accent: markering, labelhuisje, schijven, sterren, strepen. Gebruik voor een accent nooit `--color-cta`, maar `--color-highlight` / `--brand-accent`.
- **Markering:** hooguit één gemarkeerd woord per scherm (`==woord==` in de kopij). Op donker in Goudgeel als tekstkleur, op licht als onderstreepbalk.
- **Iconen:** lijniconen (24, streep 2, Lucide) voor bediening; gevulde tweekleurige merkiconen voor diensten en beloftes. Nooit door elkaar in één rij.
- **Beeld:** altijd `width` en `height`; lui laden onder de vouw; hero met `fetchpriority="high"` en preload. Geen AI-gegenereerde "medewerkers" als echt voorgesteld. Reviewavatars zijn **initialen**, geen foto's.
- **Beweging:** onthullen bij scrollen alleen met de gecorrigeerde aanpak (hoofdstuk 6): drempel 0 voor groepen, terugval zonder IntersectionObserver, alles zichtbaar bij `beforeprint`, en uit bij `prefers-reduced-motion`.
- **Geen em- en en-dashes**, nergens: HTML, CSS, JS, Python, Markdown en commentaar. De bewaker faalt erop.
- **Commentaar:** kort en in het Nederlands, zoals de rest van de code.

## 5. Taakverdeling (eigenaar = enige die het bestand bewerkt)

### dereus-55 (hoofdbouwer): fundament en home
- `_werk/build.py`, `config.py`, `navigatie.py`, `kit.py`, `kopij.py`, `bewakers.py`
- `css/tokens.css`, `css/style.css`, `js/site.js`, `fonts/`, `img/og.jpg`, het kopiëren van `img/logo/` en `img/iconen/`
- **Gedeelde onderdelen:** topbalk, header met megamenu, drawer met focus-trap, footer, mobiele belbalk, skiplink, icoonsprite, bereikbaarheidsstatus ("Nu bereikbaar"), onthullen bij scrollen.
- **Gedeelde blokken:**
  - `kop`: de kop zonder foto (`.pk`) voor alle subpagina's (H1, intro, optionele ankerchips en belregel);
  - `offertepil`: het pilformulier (Van, Naar, Wanneer, Soort), GET naar `/offerte/`; variant `hero` op de home en `los` als afsluiter op andere pagina's;
  - `reviews` (varianten `volledig` en `compact`);
  - `vragen` (FAQ met `details`/`summary`, herbruikbaar met andere kopij).
  - `contactband` (witte kaart met een Diepblauw gegevenspaneel, licht boven de footer);
  - `kernwaarden` (genummerde kaarten op de blauwe band).
- **Home `/`** en al zijn blokken: `hero` (#offerte, met offertepil), `diensten` (#diensten), `waarom` (#waarom, met de cijfers en de link naar /kosten/), `werkwijze` (#werkwijze, teaser met de route en een link naar /werkwijze/), `reviews` (#reviews), `over-ons` (#over-ons, teaser met een link naar /over-ons/), `werkgebied` (#werkgebied), `vragen` (#vragen). Geen cijferband meer (besluit dereus-28).
- **`/over-ons/`** (`_werk/paginas/over_ons.py`): `kop`, `offertepil` (los, over de kop), `over-ons` (#verhaal, met feiten), `kernwaarden` (#zo-werken-wij), `reviews`, `werkgebied` (#den-haag), `contactband` (#contact).
- `_werk/paginas/home.py`, de conceptpagina-ondersteuning in de build (hoofdstuk 12).

### dereus-b4: diensten, kosten, werkwijze en het offerteformulier
- `_werk/paginas/diensten.py`, `_werk/paginas/kosten.py`, `_werk/paginas/werkwijze.py` (`/werkwijze/`, blokken `stappenlang`, `checklist`, `verhuisdag`) en de sjablonen voor de conceptpagina's (hoofdstuk 12).
- Blokken voor `/diensten/`: `dienstenpanelen` (plakkende index met wijzer, 8 panelen, huisvormig kader, `:target`-stijl).
- Blokken voor `/kosten/`: `antwoord` (direct antwoord + ankerchips), `opbouw`, `treden` (traptreden), `extradiensten` (2x2), `annuleren`.
- **`formulier`**: de gedeelde formuliercomponent. Veldstijlen, verzendlabel Van → Naar met PDOK-aanvulling, foutoverzicht, `aria-invalid`, honeypot, verzenden via Web3Forms (`fetch`), doorsturen naar de bedanktpagina, leest `URLSearchParams` (`van`, `naar`, `datum`, `dienst`). Twee varianten: `offerte` en `contact`. De access key komt uit `config.WEB3FORMS_KEY` (placeholder zolang er geen key is; dan toont het formulier een nette melding met telefoon en e-mail).
  - Bestanden: `_werk/blokken/formulier.py`, `css/blok/formulier.css`, `js/blok/formulier.js`.

### dereus-e7: overige pagina's, SEO en livegang
- `_werk/paginas/offerte.py` (kop + `formulier` variant `offerte` + "Wat er na uw aanvraag gebeurt" + Google-pil), `offerte_bedankt.py`, `contact.py` (contactkaarten met de bereikbaarheidsstatus, `formulier` variant `contact`, kaart met adrespil en "Route plannen"), `contact_bedankt.py`, `niet_gevonden.py` (404), `algemene_voorwaarden.py`, `privacyverklaring.py`
- Blokken: `contactkaarten`, `kaart`, `stappen-na-aanvraag`, `juridisch` (tekstkolom van 68ch met inhoudsopgave als pilchips), `bedankt`, `niet-gevonden`.
- `_werk/jsonld.py` (functie `voor(pagina, ctx)`, `@graph` volgens STIJLANALYSE 6.9, **geen** `aggregateRating`), `_werk/seo.py` (functie `schrijf(paginas, cfg)` voor `sitemap.xml` en `robots.txt`).
- `vercel.json` (trailingSlash, www als canonical, noindex buiten productie, cache op `/fonts/`, `/css/min/`, `/js/min/`, `/img/`, beveiligingsheaders, CSP report-only met Web3Forms en PDOK) en `.vercelignore` (minstens: `_werk/`, `website/`, `brandbook/`, `sitemap/`, `logo-opties/`, `_bron/`, `_ai-beelden/`, `_ontwerpen/`, `logo_try.jpeg`, `*.md`).

### dereus-4e: alle teksten
- `website/content/gedeeld.md` (met `#menu`), `home.md`, `diensten.md`, `kosten.md`, `offerte.md`, `contact.md`, `over-ons.md`, `werkwijze.md`, `algemene-voorwaarden.md`, `privacyverklaring.md`, `systeem.md` (404 en de twee bedanktpagina's), en de kopij van de conceptpagina's.

### dereus-28 (coördinator)
- Git, besluiten, en de volgorde van oplevering.

## 6. Vaste gegevens en schakelaars (`_werk/config.py`)

| Naam | Waarde | Waarom |
|---|---|---|
| `DOMEIN` | `https://www.verhuisbedrijfdereus.nl` | canonical met www (sitemap 3) |
| `TEL`, `TELHREF` | `085 000 5647`, `tel:+31850005647` | |
| `MAIL` | `info@verhuisbedrijfdereus.nl` | |
| `ADRES` | Lau Mazirellaan 336, 2525 ZJ Den Haag | |
| `TIJDEN` | ma t/m za 08.00 tot 20.00 uur, zo 09.00 tot 17.00 uur | ook voor de bereikbaarheidsstatus |
| `GOOGLE_SCORE` | `4,9` (altijd als "4,9 uit 5 op Google") | geen aantal |
| `GOOGLE_PROFIEL` | link naar de reviews op Google | |
| `WEB3FORMS_KEY` | `"VUL-HIER-DE-WEB3FORMS-KEY-IN"` | nog geen key |
| `LOGO_BRON` | `"brandbook/assets/logo-v2"` | logo v2 is goedgekeurd; terug naar het oude logo is **één regel** |
| `MASCOTTE_IN_HERO` | `True` | de basis-site heeft hem; het merkboek laat het aan de klant |
| `BUSTER` | automatisch: korte hash van de CSS en JS | cachebreker op `?v=` |

## 7. Kopijcontract (`website/content/*.md`)

### 7.1 Opbouw van een bestand

```markdown
---
titel: Verhuisbedrijf Den Haag | Verhuisbedrijf De Reus
beschrijving: Hoogstens 158 tekens, zonder dashes.
---
<!-- commentaar voor de bouwer mag, komt niet op de site -->

# Verhuisbedrijf in Den Haag {#offerte}
label: Verhuisbedrijf De Reus
visueel: De betrouwbare keuze voor een ==zorgeloze== verhuizing
intro: Eén vaste verhuisadviseur, ervaren verhuizers en een heldere offerte vooraf.
Notitie: regels die zo beginnen zijn voor de bouwer en komen niet op de site.

## Onze diensten {#diensten}
label: Onze diensten
intro: Welke verhuizing u ook plant, bij De Reus regelt u het met één aanspreekpunt.
belregel: Twijfelt u welke dienst past? Bel 085 000 5647.

### Particuliere verhuizingen {#particulier}
tekst: Wij doen het zware werk, u houdt het overzicht.
link: /diensten/#particulier
```

**Regels:**
1. **Voorkant** tussen twee regels `---`: `titel` (hoogstens 60 tekens) en `beschrijving` (hoogstens 158 tekens). Optioneel `og-titel`.
2. **`# Kop {#id}`** opent het blok met de H1 (één per bestand). **`## Kop {#id}`** opent een blok; de kop wordt de H2. De id tussen `{# }` is het anker of de bloknaam uit hoofdstuk 8. Kleine letters, koppeltekens.
3. **`### Titel {#id}`** opent een item binnen dat blok (dienst, stap, review, vraag, kaart); de titel wordt het veld `titel`. De `{#id}` mag weg, dan nummert de build (`item-1`, `item-2`, ...). Items staan in de volgorde van het bestand.
4. **Velden:** `sleutel: waarde` op één regel, direct onder de kop. Sleutels in kleine letters met koppeltekens. Géén `**Vet label:**`-vorm en geen tabellen: de build leest alleen `sleutel:`.
5. **Lopende tekst:** gewone regels zonder `sleutel:` worden alinea's van het veld `tekst`. Een lege regel begint een nieuwe alinea.
6. **Lijsten:** regels die met `- ` beginnen worden het veld `lijst`.
7. **Opmaak binnen tekst, alleen dit:** `**vet**`, `[linktekst](/pad/#anker)` en `==woord==` voor de ene gele markering. Geen HTML in de tekst.
8. **Genegeerd:** regels die met `Notitie:` beginnen en `<!-- commentaar -->`.
9. **Geen em- of en-dashes**, geen `[TE BEVESTIGEN]` (zulke punten horen in `OPEN-VRAGEN.md`, niet in de kopij), "4,9 uit 5" met een komma, altijd "u".
10. **Vaste gegevens** (telefoon, e-mail, adres, tijden) mogen letterlijk in de tekst staan, maar knoppen en links vult de build zelf in vanuit `config.py`.
11. **Titles en descriptions** staan in de voorkant van elk bestand, niet in een apart `meta.md`. De FAQ van een pagina staat in het eigen bestand als `## Veelgestelde vragen {#vragen}` met `###`-items (de vraag is de titel, het antwoord de tekst), niet in een apart `faq.md`.

### 7.2 Velden die elk blok kan hebben

| Veld | Betekenis |
|---|---|
| `label` | het kleine label boven de kop (met het huisje) |
| (de kop zelf) | staat in de `#`/`##`-regel, niet als veld: `#` wordt de H1 (één per pagina), `##` een H2 |
| `visueel` | een grotere display-regel naast of onder de H1 (alleen hero en kop) |
| `intro` | één alinea onder de kop |
| `tekst` | lopende tekst (alinea's) |
| `lijst` | opsomming |
| `knop` / `knop-link` | tekst en doel van de knop van dit blok |
| `belregel` | regel met het telefoonnummer onder het blok |

Items gebruiken meestal hun `###`-titel plus `tekst`, `link` en `linktekst`. Reviews: `### Naam`, dan de reviewtekst als `tekst` en `uitgelicht: ja` voor de uitgelichte. Vragen: `### De vraag?` met het antwoord als `tekst`. Cijfers: `### 4,9 uit 5` met `tekst: op Google`.

## 8. Blokken per pagina (anker = `##`-id in het kopijbestand)

| Pagina | Kopijbestand | Blokken in volgorde (`##`-id) | Eigenaar |
|---|---|---|---|
| Gedeeld | `gedeeld.md` | `topbalk`, `menu` (alleen labels die afwijken van de sitemap), `footer` (claim, kolomkoppen, knopteksten), `belbalk`, `bereikbaar` (teksten voor open en dicht) | 55 |
| `/` | `home.md` | `offerte` (hero + pil, met `#`-kop = H1), `diensten` (8 items: `particulier` `zakelijk` `nationaal` `internationaal` `verhuislift` `opslag` `montage` `woningontruiming`), `waarom` (4 items), `cijfers` (4 items met `waarde`), `werkwijze` (5 items `stap-1` tot `stap-5`, plus `knop`), `reviews` (4 items, één met `uitgelicht: ja`), `over-ons`, `werkgebied` (3 items: `hoofdkantoor` `nederland` `internationaal`), `vragen` (6 items) | 55 |
| `/diensten/` | `diensten.md` | `kop`, 8 dienstblokken met de ankers uit de sitemap (`particulier` ... `woningontruiming`), elk met `h2`, `tekst`, `kosten-link`, `knop`; `reviews` (compact), `offertepil` | b4 |
| `/kosten/` | `kosten.md` | `kop`, `antwoord`, `opbouw` (3 items), `verhuizing` (3 items), `opslag`, `verhuislift`, `montage`, `woningontruiming`, `annuleren`, `vragen` | b4 |
| `/offerte/` | `offerte.md` | `kop`, `formulier` (veldlabels, hulpteksten, foutteksten, verzendknop, privacyregel), `na-aanvraag` (3 items) | e7 (formulier: b4) |
| `/contact/` | `contact.md` | `kop`, `contactkaarten`, `formulier`, `kaart` | e7 (formulier: b4) |
| Juridisch | `algemene-voorwaarden.md`, `privacyverklaring.md` | `kop`, daarna één `##` per artikel of paragraaf (de id wordt het anker in de inhoudsopgave) | e7 |
| Systeem | `systeem.md` | `offerte-bedankt`, `contact-bedankt`, `niet-gevonden` | e7 |

Heeft een eigenaar een extra veld nodig, dan spreekt hij dat af met dereus-4e en zet het in de tabel van zijn pagina hierboven.

## 9. Bewakers (`_werk/bewakers.py`)

De build faalt als:
1. er ergens een em- of en-dash staat (gebouwde HTML, CSS, JS, `_werk/`, `website/content/`);
2. een pagina geen skiplink, geen `<main id="inhoud" tabindex="-1">` of niet precies één `<h1>` heeft;
3. `titel` langer is dan 60 of `beschrijving` langer dan 158 tekens;
4. een interne link of anker nergens op uitkomt;
5. een `<img>` geen `width`, `height` of `alt` heeft;
6. er een verboden woord in de zichtbare tekst staat: "zonder verrassingen", "volledig verzekerd", "alles is mogelijk", "garantie", "4,9/5", "4.9", "KvK" (tot de klant het nummer geeft), "gecertificeerd", "erkend", "sinds 19", "sinds 20";
7. er nog een link naar `fonts.googleapis.com` of een `img/avatar-` in staat;
8. `WEB3FORMS_KEY` een echte key lijkt en toch in een publiek bestand terechtkomt (alleen de placeholder mag in de repo).

Waarschuwingen (build gaat door): losse hex-waarden in blok-CSS, beelden boven 250 KB, een pagina met meer dan één CTA-knop per blok.

## 10. Kwaliteitslat

- Minstens zo verzorgd als Brocken op 1440 en 390 px. Screenshots maken en bekijken.
- Lighthouse: geen verschuiving door lettertypes (preload + `font-display: swap` met passende fallback), beelden met `width`/`height`, lui laden onder de vouw, `prefers-reduced-motion` zet beweging uit.
- Toegankelijk: skiplink, zichtbare focusring (Koningsblauw op licht, wit op blauw), drawer met focus-trap en Escape, FAQ met `details`/`summary`, formulieren met labels, `aria-invalid` en een foutoverzicht.
- Volgorde van oplevering: eerst het fundament (dereus-55, stap 2), dan bouwen b4 en e7 hun pagina's erop. Tot het fundament er is, kunnen b4 en e7 hun blok-HTML en -CSS al schrijven tegen de API uit hoofdstuk 3.

## 11. Bijgewerkt tijdens de bouw (dereus-55)

- **JS** staat ongeminificeerd in `/js/site.js` en `/js/blok/<naam>.js` (met `?v=hash`), niet in `js/min/`. De cache-regel in `vercel.json` geldt voor `/js/`.
- **CSS verkleinen:** alleen spaties ná een dubbele punt vallen weg. `a :hover` (met spatie) blijft een andere selector dan `a:hover`.
- **Laden:** blokken en pagina's laden onder een unieke modulenaam (`blokken_diensten`, `paginas_diensten`), dus dezelfde bestandsnaam in beide mappen mag. Een pagina zonder `PAGINA` en een dubbele blok-`NAAM` zijn een bouwfout. Hulpmodules met een `_` ervoor worden niet als blok geladen.
- **Kopij:** `k.veld("tekst")` geeft de alinea's als één regel als er geen apart veld is (een `tekst:`-regel komt in `k.tekst`).
- **Nieuw in `ctx`:**
  - `ctx.blok(naam, **opties)` rendert een blok binnen een blok, en de CSS en JS gaan mee;
  - `ctx.kopgroep(blok, klasse="", h="h2")` geeft label, kop (id `<blok-id>-kop`) en intro;
  - `ctx.belregel(tekst)` maakt van het telefoonnummer in de zin een tel-link met icoon.
- **`Pagina(letterlijk=True)`** slaat de controle op verboden woorden over (alleen de juridische pagina's). Dashes en links blijven gecontroleerd.
- **Gedeelde blokken:**
  - `kop` met de opties `kopij_id`, `chips=[(tekst, href)]`, `streep=True`, `belregel=True/False` (standaard alleen bij blok `kop`) en `id`. Rendert nooit `lijst`, `knop` of `lijstkop`;
  - `vragen` met de opties `sectie` en `open`;
  - `reviews` met de opties `variant="volledig"|"compact"` en `sectie`, waarbij de items altijd uit `home.md` komen;
  - `offertepil` met `variant="hero"|"los"`. Een kortere placeholder voor de pil kan als `placeholder-kort:` bij het item in `offerte.md`.
- **Besluiten van dereus-28:**
  - mascotte aan (`MASCOTTE_IN_HERO`);
  - `HERO_BEELD = None` geeft een grafische hero;
  - geen foto's van onbekende herkomst op de nieuwe pagina's; de bestanden in `img/` blijven staan;
  - geen cijferband: de cijfers staan in `#waarom` en in de pil.
- **Banden op de home:** Mist, Wit, Blauw met dakrand (werkwijze), Mist, Wit, Diep met dakrand (werkgebied), Mist. Na een witte sectie krijgt de dakrand witte hoeken.

- **Hoofdmenu (besluit gebruiker):** Over ons, Diensten (met megamenu), Werkwijze, Contact, plus de CTA-knop. Kosten staat niet in het menu, wel in de footer, in `#waarom` op de home en op `/diensten/`. Volgorde en labels komen uit `gedeeld.md` `#menu`. Het actieve menu-item krijgt `aria-current="page"`, ook in de lade.
- **Negen pagina's die geïndexeerd worden:** `/`, `/over-ons/`, `/diensten/`, `/werkwijze/`, `/kosten/`, `/offerte/`, `/contact/`, `/algemene-voorwaarden/`, `/privacyverklaring/`. Noindex zijn `/offerte/bedankt/`, `/contact/bedankt/` en `/404.html`.

## 12. Conceptpagina's en feiten

Pagina's die op feiten van de klant wachten, bouwen we nu al af. Eén regel in `config.py` zet ze live.

**Pagina:** `Pagina(pad=..., concept=True, wacht_op="Opslaglocatie en termijnen (open vraag 1.6)", feiten=("OPSLAG_LOCATIE",), ...)`. De property `p.live` is True voor gewone pagina's en voor concepten die aan staan.

**Aanzetten:** `config.PUBLICEER = {"/diensten/tijdelijke-opslag/": True}`. Menu, megamenu (`navigatie.DIENST_PAGINA`), lade, footer (`navigatie.FOOTER_EXTRA`), hubblokken en `sitemap.xml` volgen vanzelf. Zet u hem weer uit, dan haalt de volgende build het oude bestand uit de root.

**Zolang een concept uit staat:**
- de gewone build schrijft het niet;
- het staat niet in `sitemap.xml` en niet in menu of footer;
- een link ernaar vanaf een live pagina is een bouwfout ("link naar conceptpagina ... staat nog uit").

**Voorbeeld bekijken:** `python _werk/build.py --concept --serve --poort 8001`. Dat schrijft alles, ook de concepten, naar `_voorbeeld/` (staat in `.vercelignore`, gaat nooit mee in de deploy). Conceptpagina's krijgen een gele balk. Op `/_concept/` staat een overzicht van alle concepten met hun status, waar ze op wachten en welke feiten bekend zijn. De server haalt css, js, img en fonts uit de root.

**In blokken:**
- `ctx.live(href)`: mag deze link in deze build staan? False voor een concept dat uit staat en voor een pagina die (nog) niet bestaat. Bestanden, mailto, tel en externe links zijn altijd True.
- `ctx.href(pagina, terugval)`: de pagina als die live is, anders de terugval (bijvoorbeeld het anker op `/diensten/`).
- `ctx.feit("NAAM")` geeft de waarde of None. `ctx.feit("NAAM", "Zin met {}.")` geeft de zin, of "" als het feit onbekend is. Een lijst wordt "a, b en c".

**In de kopij** (`website/content/*.md`, voorstel dereus-4e):
- `{NAAM}` in een alinea, een veldwaarde, een lijstregel of de voorkant wordt ingevuld. Is het feit onbekend (None, False, leeg), dan valt die alinea, dat veld of die regel weg.
- `als: NAAM` of `tenzij: NAAM` geldt voor de volgende alinea, `tekst:`-regel of lijstregel.
- `alleen-als: NAAM` op een `##`-blok of `###`-item laat het hele blok of item weg. Een weggevallen blok slaat de pagina stil over.
- Een onbekende NAAM is een bouwfout.

**Feiten:** `config.FEITEN`, met None als onbekend. De sleutels komen van dereus-4e en hebben het nummer van de open vraag erbij. Zodra `KVK` of `OPRICHTINGSJAAR` een waarde heeft, mag het woord KvK of "sinds 20xx" in de tekst. `TEAM_BEELD` zet een echte teamfoto in het huisvenster op `/over-ons/`. `HERO_BEELD` (los in config) doet hetzelfde voor de hero.

**Bewaker:** `[...]`, `None` of een overgebleven `{NAAM}` in zichtbare tekst is een bouwfout.
