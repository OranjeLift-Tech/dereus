# Stijlanalyse: Brocken en De Kievit, en de richting voor De Reus

- **Versie:** 1.0, 18 september 2026
- **Doel:** de websites van Brocken Verhuizingen en De Kievit Verhuizingen uitpluizen, zodat de nieuwe site van Verhuisbedrijf De Reus hun moderne uitstraling kan overnemen zonder er een kloon van te worden. Dit document is zo geschreven dat je ermee kunt bouwen zonder die twee repo's te openen.
- **Bronnen (alleen gelezen, niets aangepast):**
  - Brocken: `C:\users\arnas\git_repos\brocken\site` (build van 17-09-2026)
  - De Kievit: `C:\users\arnas\git_repos\website-kieviet\site` (live op https://www.de-kievit.nl)
  - De Reus: `brandbook/tokens.css`, `brandbook/research/color-type-system.md`, `brandbook/research/website-brief.md`, `sitemap/SITEMAP.md` (versie 1.2, 7 pagina's)
- **Hoort erbij, in `website/referentie/`:**
  - 24 screenshots (zie hoofdstuk 4)
  - `bijlage-analyse-brocken.md` en `bijlage-analyse-dekievit.md`: de volledige code-analyse per site, met alle tokens, breakpoints en CSS letterlijk, plus `bestand:regel`-verwijzingen. Hoofdstuk 3 hieronder geeft per component de kern. Zoek je een regel die hier niet staat, kijk dan in de bijlage.

---

## 0. In het kort

1. **Brocken en De Kievit zijn twee versies van hetzelfde systeem.** Brocken is gebouwd op de bouwstraat van De Kievit, en De Kievit op een verhuis-landingspagina van een ander project. Dezelfde header, dezelfde hero, dezelfde offertepil, hetzelfde mobiele belbalkje en dezelfde toegankelijkheidsaanpak. Dat is de huisstijl van de gebruiker (hoofdstuk 5.1).
2. **Brocken is de volwassen versie.** Het heeft één lettertype, één doorlopende ondergrond met maximaal één donkere schuine band per pagina, CSS per blok en een strakke regel voor de signaalkleur. De Kievit is drukker, met meer vormen, drie lettertypes, losse decoraties en één CSS-bestand van 162 KB dat uit opeenvolgende patches bestaat.
3. **De Kievit wint op een paar onderdelen:** het reviewblok (uitgelichte review, scorepaneel, raster, zonder JS), de USP-kaartjes onder de offertepil, de kaart met adres op de contactpagina en de keuze om geen `aggregateRating` op te nemen.
4. **Advies voor De Reus: "Sterk en recht".** We nemen het skelet en de conversie-onderdelen van Brocken over en een paar blokken van De Kievit. Alles krijgt de De Reus-tokens: Koningsblauw, Diepblauw, Goudgeel als CTA met Diepblauwe tekst, Archivo Condensed 800 en Inter, pilknoppen en kaarten van 14 px. Eigen kenmerken maken het onderscheid: een dakrand in plaats van een schuine rand, een huisje uit het logo als label en als fotokader, zware smalle koppen en geen scheve kaartjes. Zie hoofdstuk 6.
5. **Er bestaat al een De Reus-site** (repo TugcheSezr/dereus, root van deze map, commit `504b21b`), met het skelet van deze huisstijl. Maar die gebruikt een eigen "Merkboek v2.0" (andere kleuren, Roboto, knoppen met hoeken, de mascotte in de hero, formulieren via `mailto:`). **Advies: verbeter die code met de lijst en de aliaslaag uit hoofdstuk 7, en bouw geen los prototype.** Hoofdstuk 6 is het doelbeeld.
6. **Grootste afhankelijkheid:** De Reus heeft geen eigen foto's van team, bus of lift. Beide voorbeeldsites halen hun "premium" gevoel uit echte mensen die uit het beeld stappen (uitgesneden foto's). Een fotoshoot staat bovenaan de open punten (6.8). Tot dan werkt het ontwerp met grafische vlakken en foto's van Den Haag.

---

## 1. Stack en opbouw

| | Brocken | De Kievit |
|---|---|---|
| **HTML** | Statisch, één `index.html` per map, adressen op `/` | Idem |
| **Generator** | Python 3, alleen standaardbibliotheek, in `site/_werk/`. `build_brocken.py` maakt de home, `build_paginas.py` de rest. | Idem: `build_kievit.py` (home) en `build_paginas.py` (34 pagina's) |
| **Gedeelde header en footer** | Bij de build in elk HTML-bestand gekopieerd. Header en drawer uit `navigatie.py`; footer, mobiele balk, offertepil en formulier worden met regexen uit de gebouwde home geknipt. **De home is de componentenbibliotheek.** | Precies hetzelfde |
| **Menu, titels, telefoon, score** | Eén bron: `_werk/navigatie.py` | Idem |
| **CSS** | `style.css` (953 regels, kern) + 56 blokbestanden `_werk/blokken/<naam>.css`. `css_min.py` maakt `style.min.css` (kern + de 3 blokken die overal staan) en per blok een eigen `.min.css`, die **alleen geladen wordt op pagina's met dat blok**. Kern ± 26 KB gzip. | Eén `style.css` van 2045 regels (162 KB), chronologisch opgebouwd uit patches: een latere regel wint. `style.min.css` ± 21 KB gzip. |
| **Kritieke CSS** | Geen. Bewust render-blocking, omdat asynchrone CSS op De Kievit layoutverschuiving (CLS) gaf. | Idem |
| **JS** | Vanilla, `defer`. `brocken.js` (23 KB kern: offertepil, formulier, adresaanvulling, menu, reviewrail, FAQ) + 25 kleine blokscripts, elk met één interactie. | Eén `kievit.js` (21 KB): offertepil, formulier, dozencalculator, adresaanvulling, menu |
| **Lettertypes** | Alleen **Sora** (variabel, 100 tot 800), zelf gehost, latin en latin-ext, 1 preload | **Poppins** 700 (koppen), **Noto Sans** variabel (tekst), **Zilla Slab** 700 (cijfers en citaten), 2 preloads |
| **Formulieren** | Web3Forms via `fetch`, honeypot, foutoverzicht, PDOK-adresaanvulling | Idem |
| **Hosting** | Vercel, `trailingSlash: true`, www naar kaal domein, 27 redirects van WordPress, `noindex` op elk ander domein, 1 jaar cache op `/assets/`, beveiligingsheaders plus een CSP (report-only) | Vercel, `trailingSlash: true`, **kaal domein naar www**, `noindex` op andere domeinen, zelfde headers |
| **Tokens** | `style.css:27-44` met oude namen (`--goud` is bordeaux), plus schone bloktokens `--b-*` in `_werk/blokken/_basis.css:5-20`. Bron van waarheid: `brand-book/tokens.css`. | Alleen `style.css:24-39`, met misleidende namen (`--goud` is teal, `.btn--groen` is geel) |
| **Bewakers bij de build** | Build faalt op em- en en-dashes, op restanten van sjablonen, op een ontbrekende skiplink en op beschrijvingen van meer dan 158 tekens | Controle dat de blokstructuur niet verandert als tekstschrijvers woorden vervangen |
| **Live** | **Nee.** brockenverhuizingen.nl toont nog de oude WordPress-site. De screenshots komen van een lokale server. | Ja, https://www.de-kievit.nl |

**Wat dit betekent voor De Reus:** de bouwstraat is beproefd en past ook op 7 pagina's. Neem het idee over: één `navigatie.py` als bron voor menu en footer, header en footer bij de build kopiëren, CSS per blok, sprite per pagina snoeien en de dash-bewaker. Neem de oude tokennamen niet over. De Reus gebruikt de namen uit `brandbook/tokens.css`.

---

## 2. Het ontwerpsysteem

### 2.1 Raster en breedtes

| | Brocken | De Kievit |
|---|---|---|
| Container | `.wrap{max-width:1200px;margin-inline:auto;padding-inline:clamp(16px,4vw,40px)}` | Identiek |
| Rasters | Bijna alles 2 kolommen met **ongelijke** verhoudingen (7/5, 5/7, 1.1/.9, .72/1.28), `gap:clamp(2rem,4.5vw,5rem)` | Vooral `1fr 1fr` en `repeat(3 of 4,1fr)` |
| Uitlopen tot de rand | `margin:calc(-1 * max(var(--pad),(100vw - var(--maxw)) / 2 + var(--pad)))` of `left:calc(50% - 50dvw)` | `margin-right:calc((min(100vw,var(--maxw)) - 100vw)/2)` |
| Zoom-bestendig | Alle `vw` in de bron worden `calc(N * var(--vw))` met `--vw:min(1dvw,14.4px)`: niets groeit voorbij de opmaak van 1440 px | Nee |
| Hoofdbreekpunten | 1024 (menu naar hamburger), 1000/999 (blokken stapelen), 900, 760 (offertepil stapelt), 767.98 (mobiele belbalk), 620, 480 | 1024, 900/901, 860, 767.98, 760, 620, 560/520 |

### 2.2 Ruimte

- **Brocken:** sectiepadding `--b-ruimte: clamp(4rem,2.8rem + 5vw,7.5rem)` (64 tot 120 px). Staan er twee lichte blokken achter elkaar, dan krijgt het tweede de halve padding aan de bovenkant. Kopgroep naar inhoud: `clamp(2rem,1.4rem + 2vw,3.25rem)`.
- **De Kievit:** `.sectie{padding-block:clamp(3.5rem,7vw,6rem)}` (56 tot 96 px), met dezelfde halveringsregel. Geen vaste schaal, wel steeds dezelfde `clamp()`-waarden.

### 2.3 Radius, schaduw en randen

| | Brocken | De Kievit |
|---|---|---|
| Radius | invoervelden 8, kaarten 15, beeld 20, offertebox 22 tot 28, alles wat klikt `999px` | standaard 18, grote conversiepanelen 28, panelen 24, reviews en velden 12, dienstkaarten **vierkant** |
| Schaduw | altijd twee lagen, een haarlijn en een lange zachte schaduw met negatieve spreiding: `0 1px 2px rgba(10,10,10,.05),0 18px 40px -24px rgba(10,10,10,.32)` | `--schaduw-kaart:0 1px 2px rgba(29,29,27,.05),0 14px 34px -22px rgba(29,29,27,.28)`, `--schaduw:0 18px 50px -22px …`, `--schaduw-lg:0 40px 90px -40px …` |
| Randen | haarlijnen van 1 px in de lichtste merktint, velden 1.5 px grijs, feitenlijsten met een zwarte bovenrand van 2 px, stippellijnen als route | haarlijnen van 1 px `#C4E4E4`, accentranden van 6 px links of onder |
| Uitgesneden foto's | `filter:drop-shadow(0 18px 16px rgba(10,10,10,.28))` | idem |

### 2.4 Typografie

| | Brocken | De Kievit |
|---|---|---|
| Kop H2 | `.b-kop{font:700 clamp(2rem,1.25rem + 2.7vw,3.3rem)/1.06 'Sora';letter-spacing:-.028em;text-wrap:balance}` | `.kop{font-size:clamp(2.05rem,3.6vw,2.95rem)}`, Poppins 700, donker teal |
| Nadruk in kop | `<em>` rechtop, in bordeaux | geen; wel een markeerstreep onder één woord in de hero |
| Label boven de kop | roze pil met oranje stip: `.b-label{padding:.46rem .82rem .42rem;border-radius:999px;background:#FFF4F4;color:#79242F;font:600 .74rem/1 'Sora';letter-spacing:.1em;text-transform:uppercase}` + `::before` stip van .45rem | `.eyebrow{font:700 .76rem/1.3;letter-spacing:.18em;text-transform:uppercase}` met een haarlijn van 2rem ervoor |
| Lopende tekst | `font:400 1.09rem/1.6`, `p{line-height:1.72}` | idem |
| Cijfers | Sora 700, tabelcijfers, `letter-spacing:-.045em` | Zilla Slab 700 (schreef), voor stapnummers, scores en jaartallen |
| Knoppen | 600, .95rem, **zinsnaamval** | 700, .8rem, **HOOFDLETTERS met .1em spatiëring** |
| Hoofdletters | alleen labels, veldlabels en kolomkoppen in de footer | idem, plus knoppen |

### 2.5 Sectieritme

**De Kievit: banden die elkaar afwisselen.** Crème (`#F6F4EC`) en licht teal (`#E5F3F3`) wisselen elkaar af, met navy (`#22314E`) voor gewicht. Per sectie komt er een eigen vorm bij: een reuzenring (`.ring::before`, cirkel van 900 px met een witte rand van 2 px), een schuine teal band (`skewY(-5deg)`), een boogvenster, verschoven kleurvlakken achter foto's, polaroids en losse decoraties (bij, honingraat, pijlen). Die decoraties staan absoluut in procenten en verdwijnen onder 1280 px.

**Brocken: één doorlopende ondergrond.** Alle lichte secties zijn transparant op één gebroken wit (`#F7F7F6`). Daarachter liggen zeer lichte lijnmotieven en een stippenraster dat uitvloeit (`body::before/::after`). Kleur zit ín de blokken, niet in de banden. Per pagina is er maximaal één donkere sectie, met schuine boven- en onderrand, getekend met achtergrondverlopen:

```css
/* brocken _werk/blokken/_basis.css:58-66 */
.b-sectie:is(.b-grond--donker,.b-grond--bordeaux){
  --b-schuin:clamp(1.25rem,4.4vw,4.75rem);
  padding-block:calc(var(--b-ruimte) + var(--b-schuin));
  background:
    linear-gradient(to top left,var(--b-grond) 50%,transparent calc(50% + 1px)) top/100% var(--b-schuin) no-repeat,
    linear-gradient(to bottom right,var(--b-grond) 50%,transparent calc(50% + 1px)) bottom/100% var(--b-schuin) no-repeat,
    linear-gradient(var(--b-grond),var(--b-grond)) center/100% calc(100% - 2 * var(--b-schuin) + 2px) no-repeat}
```

Brocken hanteert twee ontwerpregels (`_werk/blokken/ONTWERP.md`):
1. **Elk blok heeft één lijn die niet recht is.** Dat kan een schuin bijgesneden foto zijn, een kaart die 1 tot 3 graden kantelt, twee platen die verschoven op elkaar liggen, een reuzencijfer als omtrek of de boog uit het logo. Twee buurblokken gebruiken nooit hetzelfde middel.
2. **Diepte in drie lagen:** achter een vorm, in het midden een foto of uitgesneden persoon, voor een kaart die over de rand van het midden valt.

### 2.6 Kleurgebruik

Beide sites houden één verzadigde kleur vrij voor de actie:
- **De Kievit:** geel `#FFD500` met donkere tekst (11,9:1), één keer per sectie, met een donkergele rand van 1 px omdat geel op crème maar 1,3:1 haalt.
- **Brocken:** splitst oranje in twee rollen.
  - **Signaaloranje `#FF5100`:** alleen voor vormen, stippen, bogen, sterren en cijfers vanaf 24 px, nooit voor kleine tekst.
  - **Actie-oranje `#D24204`:** voor knoppen, met witte tekst (4,64:1).

Beide meten elk tekst- en achtergrondpaar en leggen dat vast in `_werk/contrast.txt`.

---

## 3. Componenten

Per component: wat beide sites doen, de kern-CSS en welke versie De Reus neemt. Alle regelnummers wijzen naar `style.css` van de betreffende site, tenzij er een ander bestand staat. Meer staat in de bijlagen.

### 3.1 Header

Bij beide vrijwel identiek:
- De header staat altijd `position:fixed` en is transparant boven de hero, met wit logo en witte links.
- Een donker verloop onder de header houdt witte tekst leesbaar op een foto.
- Na 40 px scrollen krijgt de header `.is-stuck`:
  - een matglazen balk (`backdrop-filter`);
  - het logo wisselt naar de gekleurde versie en krimpt van 101 naar 62 px;
  - de links worden donker;
  - er schuift een reviewbadge in (1 ster en het cijfer).

```css
/* Brocken style.css:98-121 (De Kievit 101-132 is gelijk op kleuren na) */
.topbar{position:fixed;inset:0 0 auto 0;z-index:50;padding:.9rem 0;transition:background .35s var(--ease),box-shadow .35s var(--ease),padding .35s var(--ease)}
.topbar .wrap{display:flex;align-items:center;justify-content:space-between;gap:1rem}
.topbar__logo img{height:101px;width:auto;transition:opacity .35s var(--ease),height .35s var(--ease)}
.topbar__logo img+img{position:absolute;left:0;top:50%;transform:translateY(-50%);opacity:0}
.topbar.is-stuck .topbar__logo img{opacity:0}
.topbar.is-stuck .topbar__logo img+img{opacity:1}
.topbar.is-stuck{background:rgba(247,247,246,.92);backdrop-filter:saturate(1.4) blur(12px);-webkit-backdrop-filter:saturate(1.4) blur(12px);box-shadow:0 2px 10px rgba(10,10,10,.06);padding:.4rem 0}
.topbar.is-stuck .topbar__logo img,.topbar.is-stuck .topbar__logo img+img{height:62px}
@media(min-width:1024px){
  .topbar::before{content:"";position:absolute;inset:0 0 auto 0;height:150px;z-index:-1;pointer-events:none;
    background:linear-gradient(180deg,rgba(10,10,10,.42) 0%,rgba(10,10,10,.40) 42%,rgba(10,10,10,0) 100%);transition:opacity .35s var(--ease)}
  .topbar.is-stuck::before{opacity:0}}
.topbar__reviews{display:none}
.topbar.is-stuck .topbar__reviews{display:inline-flex;animation:topbar-in .35s var(--ease)}
@keyframes topbar-in{from{opacity:0;transform:translateY(-4px)}}
.nav__links>li>a,.nav__trigger{display:inline-flex;align-items:center;gap:.3rem;font:600 .9rem/1 var(--font-kop);color:#fff;text-decoration:none;white-space:nowrap;padding:.55rem 0}
.topbar.is-stuck .nav__links>li>a,.topbar.is-stuck .nav__trigger{color:var(--ant)}
@media(max-width:1199.98px){.topbar__tel{display:none}}
@media(max-width:1023.98px){.nav{display:none}.nav-toggle{display:inline-flex}}
```

**Topbalk:** geen van beide heeft een aparte balk erboven. De sitemap van De Reus vraagt er wel een (telefoon, e-mail, 4,9 op Google). Zie 6.7 voor een topbalk die verdwijnt zodra de header vast komt te staan.

### 3.2 Megamenu en mobiel menu

Bij beide gelijk. Dit is de volledige code, die je direct kunt overnemen:
- **Megamenu:**
  - een wit paneel onder het menu-item, `border-radius:18px`, `box-shadow:var(--schaduw-lg)`;
  - een onzichtbare brug van 14 px zodat hover niet wegvalt;
  - opent op `mouseenter` en `focusin`, sluit 140 ms na `mouseleave`, bij een klik erbuiten en bij Escape;
  - `aria-expanded` op de trigger. De trigger linkt zelf nog naar de hubpagina.
- **Drawer:**
  - een paneel dat van rechts inschuift (`width:min(420px,100%)`, `translateX(100%)` naar 0 in .32 s) met een scherm erachter;
  - groepen zijn `<details class="drawer__group">` met een CSS-pijltje;
  - onderaan de CTA en het telefoonnummer;
  - `role="dialog" aria-modal="true"`, focus blijft in het paneel, Escape sluit, de focus gaat terug naar de knop;
  - de body scrollt niet en `.mcta` is verborgen zolang de drawer open is.
- **Code:** Brocken `style.css:435-551` en `brocken.js:231-285`, De Kievit `style.css:1324-1427`. Letterlijk in de bijlagen, hoofdstuk 4.2 en 4.3.

### 3.3 Hero

**Home (bij beide gelijk):**
- een volledig breed beeld (`<picture>` met een aparte staande uitsnede voor mobiel);
- op desktop eventueel een video: Vimeo bij Brocken, mp4 bij De Kievit;
- een waas, bestaande uit een radiaal en een lineair verloop;
- filmkorrel (SVG-ruis op 5 %);
- een **uitgesneden teamfoto** die onderaan midden in beeld staat;
- in het midden: label, H1 met ondertitel, en **één woord met een markeerstreep eronder**.

```css
/* Brocken style.css:131-152; De Kievit 135-180 idem */
.hero{position:relative;min-height:min(92vh,860px);display:grid;align-items:stretch;overflow:hidden;isolation:isolate;background:var(--ant-diep)}
.hero__bg{position:absolute;inset:0;z-index:-3;display:block}
.hero__bg img{width:100%;height:100%;object-fit:cover;object-position:center top}
.hero__veil{position:absolute;inset:0;z-index:-2;pointer-events:none;background:
  radial-gradient(120% 90% at 70% 18%,rgba(10,10,10,0) 30%,rgba(10,10,10,.55) 100%),
  linear-gradient(180deg,rgba(10,10,10,.62) 0%,rgba(10,10,10,.18) 26%,rgba(10,10,10,.3) 58%,rgba(10,10,10,.92) 100%)}
.hero__grain{position:absolute;inset:0;z-index:-1;opacity:.05;pointer-events:none;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
.hero__content{position:relative;z-index:1;padding-block:5.35rem 9rem;max-width:56rem;margin-inline:auto;text-align:center;color:#fff}
.hero__title{font-size:clamp(2.5rem,4.7vw,3.55rem);font-weight:700;line-height:1.05;letter-spacing:-.02em;color:#fff;text-shadow:0 4px 30px rgba(0,0,0,.35);margin:0}
.hero__title__sub{display:block;margin-top:.45rem;font-size:.52em;line-height:1.15}
.hero__title em{font-style:normal;white-space:nowrap;background:linear-gradient(180deg,transparent 62%,rgba(255,81,0,.9) 62%);padding-inline:.06em}
.hero__person{position:absolute;left:50%;transform:translateX(-50%);bottom:calc(clamp(56px,7.5vw,104px) - 80px);height:min(420px,54%);width:auto;filter:drop-shadow(0 12px 22px rgba(0,0,0,.3))}
@media(max-width:1080px){.hero{display:flex;flex-direction:column;justify-content:flex-end;min-height:min(84vh,760px)}
  .hero__pic{position:static;order:2;min-height:min(calc(92vw / 1.747573),clamp(200px,32vw,340px))}  /* ruimte vasthouden tegen CLS */
  .hero__person{position:static;transform:none;max-height:clamp(200px,32vw,340px);max-width:92%;margin:0 auto}}
```

- **Details die het verschil maken:**
  - De hero-elementen starten nooit op `opacity:0`. Dat beschermt de LCP.
  - De video krijgt pas na `load` een bron, alleen vanaf 761 px en alleen zonder `prefers-reduced-motion`. Er is een ronde pauzeknop (WCAG 2.2.2).
- **Hero voor overige pagina's (`.hero--pagina`):**
  - korter (`min-height:498px` vanaf 1080 px), zonder video en zonder uitgesneden persoon;
  - kruimelpad gecentreerd boven de H1, één regel intro eronder.
  - Brocken legt een zacht radiaal scherm achter de titel (`.hero--pagina .hero__title::before`).
- **Kop zonder foto (`.pk`):**
  - een donker blok waarvan de bovenpadding gelijk is aan de gemeten headerhoogte;
  - Brocken geeft het een schuine onderrand, een stuk van de logoboog en een streep van 4 px onder de H1.

### 3.4 Offertepil over de rand van de hero (het handtekeningonderdeel)

Een gekleurde box met ronde hoeken schuift met een negatieve marge over de onderrand van de hero:
- **Rechtsboven:** een glazen pil met keurmerken: score, Erkende Verhuizers en het aantal beoordelingen.
- **Midden:** titel en subregel.
- **Formulier:** een **witte pil in de stijl van de zoekbalk van Airbnb** met Van | Naar | Wanneer | Soort, gescheiden door haarlijnen, en een CTA in de accentkleur.
- **Versturen** kopieert de waarden naar het grote formulier onderaan de pagina en scrolt daarheen.

```css
/* Brocken style.css:176-211 */
.offerte-overlay{position:relative;z-index:6;padding:0 clamp(16px,4vw,40px) 60px;display:flow-root}
.of-wrap{position:relative;max-width:var(--maxw);margin:clamp(-104px,-7.5vw,-56px) auto 0}
.of-box{position:relative;z-index:2;background:var(--teal-paneel);color:#fff;border-radius:28px;padding:clamp(28px,3.4vw,44px) clamp(28px,4vw,52px);box-shadow:0 24px 60px -10px rgba(121,36,47,.38)}
.of-trust{position:absolute;top:20px;right:24px;z-index:5}
.of-title{font-weight:600;letter-spacing:-.02em;line-height:1.05;font-size:clamp(1.6rem,2.6vw,2.1rem);margin:0 0 8px;color:#fff}
.of-pill{display:grid;grid-template-columns:.8fr 1px .8fr 1px 1fr 1px 1.2fr auto;background:#fff;border-radius:999px;overflow:hidden;padding:8px;box-shadow:0 8px 24px rgba(10,10,10,.18)}
.of-field{display:flex;flex-direction:column;justify-content:center;padding:8px 18px;min-width:0;cursor:text}
.of-field span{font:600 11px/1 var(--font-kop);color:var(--ant);letter-spacing:.06em;margin:0 0 4px;text-transform:uppercase;opacity:.78}
.of-field input,.of-field select{border:none;outline:none;background:none;font-size:16px;color:var(--ant);width:100%;padding:0;line-height:1.4;appearance:none}
.of-divider{background:rgba(10,10,10,.12);width:1px;align-self:center;height:38px}
.of-cta{display:inline-flex;align-items:center;gap:10px;background:var(--oranje);color:#fff;border:none;border-radius:2rem;padding:15px 26px;font:600 15px/1.2 var(--font-kop);cursor:pointer;white-space:nowrap}
.keurmerken{display:flex;align-items:center;width:max-content;max-width:100%;padding:5px 6px;background:rgba(0,0,0,.22);border:1px solid rgba(255,255,255,.18);border-radius:999px}
.keurmerk{width:96px;height:52px;padding:9px;display:grid;place-items:center;color:#fff}
.keurmerk+.keurmerk{border-left:1px solid rgba(255,255,255,.24)}
.keurmerk--kv img{filter:brightness(0) invert(1)}   /* logo van een derde wit maken */
@media(min-width:761px) and (max-width:1139px){.of-pill{grid-template-columns:1fr 1fr;border-radius:22px;gap:4px}.of-divider{display:none}.of-cta{grid-column:1/-1;justify-content:center;border-radius:14px}}
@media(max-width:760px){.of-pill{grid-template-columns:1fr;border-radius:18px;gap:6px}.of-divider{display:none}.of-field{padding:10px 16px;border-bottom:1px solid rgba(10,10,10,.08)}.of-cta{justify-content:center;border-radius:14px}}
```

**Op subpagina's van Brocken** staat bij "Soort offerte" de dienst al ingevuld. Op mobiel klapt de box in tot titel, badges en één knop (`.offerte-overlay--kort`).

### 3.5 USP-rijen en vertrouwensbalken

| Patroon | Waar | Kern |
|---|---|---|
| **Vertrouwenskaarten** (De Kievit `.trust`, 242-255) | Direct onder de offertepil | 4 witte kaarten met een icoontegel van 56 px (radius 15) in een lichte merktint, met een tweekleurig SVG-icoon. Titel vet, eronder de toelichting. |
| **Belofte aan een spanband** (Brocken `b-belofte`) | Home, "Waarom Brocken" | 6 kaartjes hangen aan een oranje spanband met gesp. Ze kantelen om en om, zwaaien bij hover met een verende `linear()`-easing en hun iconen tekenen zichzelf. Heel eigen voor Brocken: **niet overnemen.** |
| **Feitenrij met grote cijfers** (Brocken `b-liftspot__feiten`) | Blokken met cijfers | 3 kolommen, elk met een zwarte bovenrand van 2 px, een groot cijfer (700, tabelcijfers) en een toelichting in grijs |
| **USP's met icoon** (De Kievit `.usps--rij`) | In donkere panelen | Icoon in een cirkel van 44 px, h3 en p, 4 kolommen |

```css
/* De Kievit .trust (242-255) */
.trust__in{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem}
.trust__item{display:flex;align-items:center;gap:.85rem;font-size:.98rem;line-height:1.4;color:var(--ant-zacht);background:var(--wit);border:1px solid var(--lijn);border-radius:var(--r);padding:1rem;box-shadow:var(--schaduw-kaart)}
.trust__item b{display:block;color:var(--ant);font-weight:700;font-size:1.09rem;line-height:1.25;margin-bottom:.15rem;text-wrap:balance}
.trust__ico{flex:none;width:56px;height:56px;border-radius:15px;background:var(--goud-licht);border:1px solid var(--zand);display:grid;place-items:center}
/* Brocken feitenrij (liftspot.css:9-12) */
.b-liftspot__feiten{list-style:none;margin:1.8rem 0 0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem}
.b-liftspot__feiten li{padding-top:.9rem;border-top:2px solid var(--b-inkt)}
.b-liftspot__feiten b{display:block;font:700 clamp(1.8rem,1.35rem + 1.3vw,2.5rem)/1 var(--font-titel);letter-spacing:-.03em;font-variant-numeric:tabular-nums;color:var(--b-bordeaux)}
```

### 3.6 Diensten

**De Kievit, tegels (`.diensten`, 258-269):**
- vierkante teal tegels met een foto bovenaan (760/435) en een geel nummerlipje in schreef;
- bij hover komt de kaart 3 px omhoog, zoomt de foto naar 1.05 en schuift het pijltje in de titel.
- **Vraagt 6 goede foto's.**

**Brocken, genummerde lijst (`b-diensten`):**
- links rijen met een nummer, de dienstnaam groot (`clamp(1.35rem,.9rem + 1.5vw,2.15rem)`), één regel uitleg en een ronde pijlknop;
- een oranje streep veegt onder de actieve rij in;
- rechts een plakkend fotokader dat bij hover van foto wisselt.
- **De lijst werkt ook zonder foto's.**

```css
/* Brocken diensten.css:5-44 (kern) */
.b-diensten__lijst{list-style:none;margin:0;padding:0;border-top:1px solid var(--b-lijn)}
.b-diensten__rij{border-bottom:1px solid var(--b-lijn)}
.b-diensten__link{position:relative;display:grid;grid-template-columns:2.6rem minmax(0,1fr) auto;align-items:center;gap:1.1rem;padding:1.35rem .2rem;color:var(--b-inkt);text-decoration:none}
.b-diensten__link::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:var(--b-signaal);transform:scaleX(0);transform-origin:0 50%;transition:transform .55s var(--b-ease)}
.b-diensten__naam{margin:0;font:600 clamp(1.35rem,.9rem + 1.5vw,2.15rem)/1.12 var(--font-titel);letter-spacing:-.022em}
.b-diensten__pijl{display:grid;place-items:center;width:3rem;height:3rem;border-radius:50%;border:1.5px solid var(--b-lijn);color:var(--b-bordeaux);transition:transform .45s var(--b-ease)}
.b-diensten__rij.is-actief .b-diensten__link::after{transform:scaleX(1)}
.b-diensten__rij.is-actief .b-diensten__pijl{transform:translateX(6px);border-color:var(--b-signaal)}
```

**Brocken, diensten met ankernavigatie (`b-plaatsdiensten`, de stadspagina's).** Dit is precies het patroon dat `/diensten/` van De Reus nodig heeft:
- **Links:** een plakkende inhoudsopgave met een rail van 2 px en een **oranje wijzer die meeschuift** (scroll-spy met IntersectionObserver).
- **Rechts:** panelen met ankers, de foto om en om links en rechts, schuin bijgesneden, met een rond dienst-icoon als zegel op de schuine kant.
- Het paneel dat `:target` is, wordt een witte kaart met een streep van 4 px links.

```css
/* Brocken plaatsdiensten.css (kern) */
.b-plaatsdiensten__in{display:grid;grid-template-columns:minmax(0,.72fr) minmax(0,1.28fr);gap:clamp(2rem,5vw,5rem);align-items:start}
.b-plaatsdiensten__zij{position:sticky;top:6.5rem}
.b-plaatsdiensten__index ol{list-style:none;margin:0;padding:0;border-left:2px solid var(--b-lijn)}
.b-plaatsdiensten__wijzer{position:absolute;left:0;top:0;width:4px;height:3.4rem;margin-left:-1px;border-radius:2px;background:var(--b-signaal);opacity:0;transform:translateY(calc(var(--i) * 3.4rem));transition:transform .55s var(--b-ease),opacity .3s var(--b-ease)}
.b-plaatsdiensten__paneel{position:relative;display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:clamp(1.4rem,3vw,2.6rem);align-items:center;padding:clamp(1.1rem,2.2vw,1.7rem);border-radius:var(--b-r-media);scroll-margin-top:6.5rem;transition:background-color .4s var(--b-ease),box-shadow .4s var(--b-ease)}
.b-plaatsdiensten__paneel:target{background:#fff;box-shadow:var(--b-schaduw),inset 4px 0 0 var(--b-signaal)}
.b-plaatsdiensten__kader{overflow:hidden;border-radius:var(--b-r-media);clip-path:polygon(0 0,100% 0,86% 100%,0 100%)}
.b-plaatsdiensten__paneel:nth-child(even) .b-plaatsdiensten__kader{clip-path:polygon(14% 0,100% 0,100% 100%,0 100%)}
@media(max-width:999px){.b-plaatsdiensten__zij{position:static}.b-plaatsdiensten__index ol{display:flex;flex-wrap:wrap;gap:.5rem;border-left:0}.b-plaatsdiensten__wijzer{display:none}}
```

De scroll-spy (`plaatsdiensten.js`) gebruikt `rootMargin:'-35% 0px -55% 0px'` en zet `--i` op de wijzer.

### 3.7 Reviews

**De Kievit (`.reviews`, 347-406), alles statisch:**
- **Links boven:** één **uitgelichte review** als groot citaat.
- **Rechts:** een **scorepaneel** in navy met een groot geel cijfer, feiten en keurmerken op witte tegels.
- **Daaronder:** een raster van 4 compacte kaarten, afgekapt op 6 regels.
- Halve sterren doe je door te knippen. Er is geen JS nodig.

```css
.reviews__hoofd{display:grid;grid-template-columns:1fr 21rem;gap:1.6rem;margin-bottom:1.1rem}
.uitgelicht{margin:0;background:var(--wit);border:1px solid #D1D5DB;border-radius:16px;padding:clamp(1.4rem,3vw,2.2rem)}
.uitgelicht blockquote{margin:1rem 0 1.4rem;font:700 clamp(1.3rem,2.1vw,1.72rem)/1.45 var(--font-display)}
.scorepaneel{background:var(--bruin);color:var(--wit);border-radius:16px;padding:1.4rem}
.scorepaneel__cijfer b{font:700 3.6rem/1 var(--font-display);color:var(--geel)}
.rgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:1.1rem;list-style:none;margin:0;padding:0}
.review{display:flex;flex-direction:column;background:var(--wit);border:1px solid #D1D5DB;border-radius:12px;padding:1.15rem 1.2rem}
.review__tekst{margin:0 0 .9rem;font-size:.93rem;line-height:1.62;display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:6;overflow:hidden}
.review__wie{display:flex;flex-direction:column;margin:auto 0 0;padding-top:.8rem;border-top:1px solid #E4E8EE;font-size:.82rem}
.sterren__s{position:relative;display:block;width:1em;height:1em}
.sterren__s--half .sterren__vol{clip-path:inset(0 50% 0 0)}
@media(max-width:1099.98px){.reviews__hoofd{grid-template-columns:1fr}.rgrid{grid-template-columns:1fr 1fr}}
@media(max-width:640px){.rgrid{grid-template-columns:1fr}}
```

**Brocken (`b-stemmen`):**
- **Links:** twee afgeronde platen die schuin verschoven op elkaar liggen, een uitgesneden verhuizer en een witte schijf met het cijfer in een **oranje ring die zichzelf tekent** tot 96 % van de omtrek.
- **Rechts:** een horizontale **rail met scroll-snap** die tot de schermrand doorloopt, met knoppen voor vorige en volgende, een voortgangsbalk en "Lees verder".

```css
/* Brocken stemmen.css (kern) */
.b-stemmen__boog{position:relative;display:grid;place-items:center;width:10.5rem;aspect-ratio:1;border-radius:50%;background:var(--b-wit);box-shadow:var(--b-schaduw);text-align:center}
.b-stemmen__ring{position:absolute;inset:.45rem;width:calc(100% - .9rem);height:calc(100% - .9rem);transform:rotate(-62deg);overflow:visible}
.b-stemmen__ring circle{fill:none;stroke:var(--b-signaal);stroke-width:5;stroke-linecap:round;transition:stroke-dashoffset 1.5s var(--b-ease)}
/* <circle cx="60" cy="60" r="54" pathLength="100" stroke-dasharray="96 100"/> ; .is-wacht zet stroke-dashoffset:96 */
.b-stemmen__kaarten{display:flex;gap:1.15rem;margin:0;padding:.9rem .25rem 1.4rem;list-style:none;overflow-x:auto;scroll-snap-type:x mandatory;overscroll-behavior-x:contain}
.b-stemmen__kaart{flex:0 0 min(22.5rem,84%);display:flex;flex-direction:column;scroll-snap-align:start;padding:1.35rem 1.45rem 1.25rem;border-radius:var(--b-r-kaart);background:var(--b-wit);box-shadow:0 1px 2px rgba(10,10,10,.05),0 14px 28px -22px rgba(10,10,10,.3)}
.b-stemmen__kaart::before{content:"\201C" / "";display:block;height:2.2rem;margin:-.35rem 0 .45rem -.15rem;font:700 4.6rem/1 var(--font-titel);color:var(--b-signaal)}
```

**Bron bij beide:** letterlijke reviews van Klantenvertellen, met voornaam, plaats, `<time>`-datum en cijfer. Geen widgets of iframes.

### 3.8 Werkwijze in stappen

- **De Kievit (`.stappen`, 272-278):**
  - 4 stappen op een half doorzichtig wit paneel (radius 24), gescheiden door haarlijnen;
  - grote nummers "01" in schreef;
  - rechts boven het blok een uitgesneden vrachtwagen.
- **Brocken (`b-stappen`):**
  - een **schuine bordeaux band over de volle breedte** met een stippenraster;
  - daarop een rij witte kaarten, elk met een oranje nummerschijf op een **stippellijn als route** die door alle nummers loopt;
  - de nummers kleuren één voor één oranje als de rij in beeld komt.
  - Op mobiel wordt de route verticaal.

```css
/* Brocken stappen.css (kern) */
.b-stappen__baan{position:relative;isolation:isolate;padding-block:calc(var(--bs-schuin) + 1.2rem) calc(var(--bs-schuin) + 1.6rem)}
.b-stappen__baan::before{content:"";position:absolute;z-index:-2;top:0;bottom:0;left:calc(50% - 50dvw);right:calc(50% - 50dvw);
  background:linear-gradient(100deg,var(--b-bordeaux-800),var(--b-bordeaux) 55%,var(--b-bordeaux-800));
  clip-path:polygon(0 var(--bs-schuin),100% 0,100% calc(100% - var(--bs-schuin)),0 100%)}
.b-stappen__rij{position:relative;margin:0;padding:0;list-style:none;display:grid;grid-auto-flow:column;grid-auto-columns:minmax(0,1fr);gap:clamp(1rem,2vw,1.5rem);counter-reset:b-stap}
.b-stappen__rij::before{content:"";position:absolute;left:-1.5rem;right:-1.5rem;top:calc(var(--bs-nr) / 2 - 1px);border-top:2px dashed rgba(244,204,205,.75)}
.b-stappen__stap{position:relative;z-index:1;counter-increment:b-stap;padding-top:calc(var(--bs-nr) / 2)}
.b-stappen__stap::before{content:counter(b-stap) / "";position:absolute;z-index:2;top:0;left:1.2rem;width:var(--bs-nr);height:var(--bs-nr);display:grid;place-items:center;border-radius:50%;
  background:var(--b-signaal);color:var(--b-inkt);font:700 1rem/1 var(--font-kop);box-shadow:0 0 0 4px var(--b-inkt)}
.b-stappen__kaart{display:flex;flex-direction:column;height:100%;padding:calc(var(--bs-nr) / 2 + 1rem) 1.25rem 1.3rem;border-radius:var(--b-r-kaart);background:var(--b-wit);box-shadow:0 1px 2px rgba(10,10,10,.08),0 22px 40px -24px rgba(0,0,0,.6)}
@media(max-width:999px){.b-stappen__rij{grid-auto-flow:row;grid-template-columns:repeat(2,minmax(0,1fr))}.b-stappen__rij::before{display:none}}
@media(max-width:640px){.b-stappen__rij{grid-template-columns:1fr}.b-stappen__rij::before{display:block;left:calc(1.2rem + var(--bs-nr) / 2 - 1px);right:auto;top:.5rem;bottom:.5rem;border-top:0;border-left:2px dashed rgba(244,204,205,.75)}}
```

### 3.9 Prijzen

**Geen van beide toont prijzen.** De Kievit legt in de FAQ uit waarom niet en heeft twee rekenhulpen: een dozencalculator met een navy uitkomstpaneel en een m³-calculator met een plakkend overzicht. De uitkomst gaat mee in het offerteformulier. Brocken beantwoordt prijsvragen in de FAQ.

Bruikbare patronen voor `/kosten/` van De Reus:
- **Brocken `b-maten`:** drie kaarten die als traptreden oplopen. Ze worden steeds hoger en donkerder, van licht via bordeaux naar donker, met een lipje van 5 px bovenop. Zie 6.6.
- **Brocken `b-doos__menu`:** een lijst "Altijd" / "Als u wilt" met een bovenrand van 2 px.
- **De Kievit calculatorkaart:** velden links en een donker uitkomstpaneel rechts, met een groot cijfer. Voor later, als De Reus rekenhulpen wil.

```css
/* Brocken maten.css:51-59: kaarten als traptreden */
.b-maten__maat{--hoog:11.5rem;position:relative;display:flex;flex-direction:column;justify-content:space-between;gap:1.2rem;min-height:var(--hoog);padding:1.5rem 1.35rem 1.35rem;border-radius:var(--b-r-kaart);background:var(--b-roze-100);color:var(--b-inkt);box-shadow:0 1px 2px rgba(10,10,10,.06),0 30px 50px -32px rgba(10,10,10,.55)}
.b-maten__maat--2{--hoog:14.5rem;background:var(--b-bordeaux);color:#fff}
.b-maten__maat--3{--hoog:17.5rem;background:var(--b-donker);color:#fff}
.b-maten__maat::before{content:"";position:absolute;top:0;left:1.35rem;width:2.5rem;height:5px;border-radius:0 0 4px 4px;background:var(--b-signaal)}
.b-maten__getal b{font:700 clamp(2.5rem,1.7rem + 2.2vw,3.6rem)/.9 var(--font-titel);letter-spacing:-.035em;font-variant-numeric:tabular-nums}
```

### 3.10 Veelgestelde vragen (accordeon)

Beide gebruiken native `<details>/<summary>`, dus geen JS.
- **De Kievit (539-555):** rijen over de volle breedte met haarlijnen ertussen, nummers "01" via een CSS-teller en een plus die wegdraait.
- **Brocken (`b-vragen`):**
  - **Links:** de kop plakt, met erachter een reuzen-"?" als omtrek en een belregel ("Staat uw vraag er niet bij? Bel …").
  - **Rechts:** witte vraagkaarten met oranje nummers en een ronde "+" die een "×" wordt. Het antwoord staat ingesprongen naast een rond monogram, alsof Brocken antwoordt.
  - `<details name="…">` zorgt dat er maar één tegelijk open staat.

```css
/* Brocken vragen.css (kern) */
.b-vragen__in{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);column-gap:clamp(2rem,.8rem + 4.6vw,5.5rem);align-items:start}
.b-vragen__kop{position:sticky;top:6.5rem;max-width:30rem}
.b-vraag{position:relative;margin:0;border-radius:var(--b-r-kaart);background:var(--b-wit);box-shadow:0 1px 2px rgba(10,10,10,.04),0 12px 26px -22px rgba(10,10,10,.3);counter-increment:b-vraag}
.b-vraag__v{position:relative;display:block;min-height:3.9rem;padding:1.05rem 4.2rem 1.05rem 3.5rem;border-radius:var(--b-r-kaart);font:600 1.04rem/1.45 var(--font-kop);cursor:pointer;list-style:none}
.b-vraag__v::-webkit-details-marker{display:none}
.b-vraag__v::before{content:counter(b-vraag,decimal-leading-zero);position:absolute;left:1.35rem;top:1.47rem;color:var(--b-signaal);font:700 .78rem/1 var(--font-titel)}
.b-vraag__v::after{content:"";position:absolute;right:1rem;top:1.95rem;width:2.2rem;height:2.2rem;margin-top:-1.1rem;border-radius:50%;background:var(--b-roze) url("data:image/svg+xml,…plus…") center/1rem no-repeat;transition:transform .35s var(--b-ease)}
.b-vraag[open]>.b-vraag__v::after{background-color:var(--b-bordeaux);transform:rotate(45deg)}
.b-vraag::before{content:"";position:absolute;z-index:1;left:0;top:.9rem;bottom:.9rem;width:4px;border-radius:0 4px 4px 0;background:var(--b-signaal);transform:scaleY(0);transition:transform .35s var(--b-ease)}
.b-vraag[open]::before{transform:scaleY(1)}
.b-vraag__a{position:relative;margin:0 1.35rem;padding:1rem 0 1.35rem 3.1rem;border-top:1px solid var(--b-lijn);font-size:1rem;line-height:1.7}
.b-vraag[open]>.b-vraag__a{animation:b-vraag-in .4s var(--b-ease) both}
@keyframes b-vraag-in{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
@media(max-width:900px),(max-height:820px){.b-vragen__kop{position:static}}
```

### 3.11 Offerteformulier

- **De Kievit (`.leadblock`, 558-618):**
  - een kaart met links een foto (cover) en rechts een teal paneel met verloop;
  - in het paneel: label, H2, een reviewchip en een compact formulier in 2 kolommen (witte velden, witte labels in hoofdletters);
  - een uitklapbare dozenschatter.
- **Brocken (`b-offerte`, aan het eind van elke pagina):**
  - een witte kaart (radius 20) op een achtergrond die schuin in licht en donker is gesplitst;
  - links een roze kolom met een uitgesneden verhuizer die boven de kaart uitsteekt, 3 genummerde stappen ("wat gebeurt er nu") en een grote belknop;
  - rechts het formulier. **De eerste rij, Van → Naar, is vormgegeven als een verzendlabel:** een rand van 2 px, een harde verschoven schaduw, een gestippelde deellijn, een ronde pijl in het midden en grote labels.

```css
/* Brocken offerte.css: het verzendlabel */
.b-offerte .lf>.lf__row:first-of-type{position:relative;gap:0;border:2px solid var(--b-inkt);border-radius:12px;background:var(--b-wit);box-shadow:5px 5px 0 var(--b-roze-100)}
.b-offerte .lf>.lf__row:first-of-type::after{content:"";position:absolute;left:50%;top:.95rem;width:2.5rem;height:2.5rem;margin-left:-1.25rem;border-radius:50%;background:var(--b-signaal) url("data:image/svg+xml,…pijl…") center/1.15rem no-repeat;pointer-events:none}
.b-offerte .lf__adres+.lf__adres{border-left:2px dashed var(--b-lijn);padding-left:2rem}
.b-offerte .lf__adres>label[for]{font:700 clamp(1.45rem,1.15rem + 1vw,1.95rem)/1 var(--font-titel);letter-spacing:-.025em}
.b-offerte .lf__adres input:not([type=checkbox]){border:0;border-bottom:2px solid var(--b-lijn-grijs);border-radius:0;padding:.55rem 0;font-size:1.06rem}
.b-offerte .lf__field input:not([type=checkbox]),.b-offerte .lf__field select{min-height:48px;border:1.5px solid var(--b-lijn-grijs);border-radius:var(--b-r-control);background:var(--b-wit);font-weight:500;padding:.6rem .85rem}
.b-offerte__tel{display:inline-flex;align-items:center;gap:.7rem;padding:.55rem 1rem .55rem .6rem;border:2px solid var(--b-signaal);border-radius:var(--b-r-control);background:var(--b-wit);font:700 clamp(1.4rem,1.1rem + .9vw,1.8rem)/1.1 var(--font-titel);font-variant-numeric:tabular-nums;text-decoration:none;min-height:44px}
```

**Gedrag bij beide:**
- Web3Forms met een honeypot. `novalidate` alleen als JS draait.
- Na een mislukte verzending komt er een foutoverzicht (`role="alert"`) met links naar de velden, dat de focus krijgt. Velden krijgen `aria-invalid` en `aria-describedby`.
- **Adresaanvulling via de PDOK Locatieserver** (gratis, van de overheid), als ARIA combobox/listbox.
- Datum en "Weet ik nog niet" sluiten elkaar uit.
- Na verzenden vervangt een succesblok het formulier.

### 3.12 CTA-banden

- **De Kievit `.venster`:**
  - een navy band met tekst links;
  - rechts een crème **boogvenster** (`border-radius:999px 999px 0 0` met een ingesprongen rand van 2 px) waarin twee uitgesneden mensen staan die buiten de boog uitsteken;
  - een watermerk op 12 %.
- **De Kievit `.opslag`:** een schuine teal band met een navy streep; de uitgesneden verhuizers zijn onder dezelfde hoek afgesneden.
- **Brocken `b-bord`:** een donker schuin blok met een weg in perspectief, een vrachtwagen die binnenrijdt en mijlpalen.
- **Bij beide** is de footerclaim de CTA-band voor de hele site: label, H2, het telefoonnummer groot en twee knoppen.

### 3.13 Footer

- **De Kievit:**
  - een foto van een vrachtwagen 's avonds achter een navy verloop;
  - claim, groot telefoonnummer en 2 knoppen, gevolgd door 4 kolommen links;
  - een rij witte keurmerklogo's (82 %, bij hover 100 %) en een donkere balk met de juridische links.
- **Brocken:**
  - een **uitgesneden vrachtwagen op een schuin bordeaux paneel** met een ring en een oranje stip;
  - de wagen schuift bij hover op de claim 14 px naar voren;
  - claim, 4 kolommen en de logorij.

```css
/* Brocken style.css:257-339 (kern) */
.footer{position:relative;isolation:isolate;display:grid;grid-template-columns:minmax(0,1fr);background:var(--bruin-diep);color:#fff;font-size:.95rem;overflow-x:clip}
.footer>*{grid-column:1}
.footer__media{grid-row:1;position:relative;z-index:-1;pointer-events:none;clip-path:inset(0 0 -40px 0)}
.footer>.wrap{grid-row:1;width:100%}
.footer__media::before{content:"";position:absolute;inset:0 0 0 auto;width:52%;background:linear-gradient(165deg,var(--bordeaux-800) 0%,var(--bruin) 78%);clip-path:polygon(24% 0,100% 0,100% 100%,0 100%)}
.footer__media img{position:absolute;z-index:1;bottom:0;right:max(var(--pad),calc((100% - var(--maxw)) / 2 + var(--pad)));width:min(42%,560px);height:auto;filter:drop-shadow(0 16px 14px rgba(20,2,6,.55));transition:transform .7s var(--ease)}
.footer:has(.footer__claim:hover) .footer__media img{transform:translateX(-14px)}
.footer__claim{max-width:44rem;padding-block:clamp(1.6rem,3vw,2.5rem) clamp(1.2rem,2vw,1.6rem)}
.footer__tel{display:inline-flex;align-items:center;gap:.8rem;font:600 clamp(1.15rem,1.9vw,1.45rem)/1 var(--font-kop);color:#fff;text-decoration:none;margin-bottom:.8rem}
.footer__rooster{border-top:1px solid rgba(255,255,255,.16);display:grid;grid-template-columns:repeat(4,1fr);gap:1.6rem 2rem;padding-block:1.9rem}
.footer__rooster h2{font:600 .85rem/1.3 var(--font-kop);letter-spacing:.12em;text-transform:uppercase;margin:0 0 .6rem}
.footer__balk{color:rgba(255,255,255,.58);font-size:.82rem}
@media(max-width:900px){.footer__rooster{grid-template-columns:1fr 1fr}}
```

### 3.14 Stadspagina (alleen Brocken)

Per plaats verandert alleen de data. De blokken in volgorde:
1. afstand (een boog rond het aantal kilometers over de weg);
2. diensten met ankernavigatie (3.6);
3. reviews uit die plaats;
4. routekaart uit OpenStreetMap;
5. wijken en postcodes met CBS-cijfers;
6. vragen per plaats;
7. 3 schuine foto's van de stad;
8. een donkere liniaal met de buurplaatsen;
9. het offerteformulier.

Voor De Reus **nu niet nodig**: de sitemap (versie 1.2) heeft geen plaatspagina's. Het blok "diensten met ankernavigatie" gebruiken we wel, op `/diensten/`.

### 3.15 Knoppen, kruimelpad, badges, kaarten

- **Knoppen:**
  - Pil (`border-radius:2rem`), het icoon via `order:2` achter het label (een driehoekje `#i-caret` of een pijl).
  - Knoppen zelf hebben geen transitie. Bij Brocken schuift het pijltje in blokken 4 px op bij hover.
  - Per sectie precies één primaire knop, in de accentkleur. De tweede is licht en is meestal het telefoonnummer.
- **Kruimelpad:** `nav.pk__kruim > ol > li` met een "/" via CSS en `aria-current="page"`, midden in de hero. Voor De Reus niet nodig, want alle pagina's hangen direct onder de home.
- **Badges:**
  - De Kievit: glazen keurmerkpil, witte tegels in het scorepaneel en een logorij in de footer.
  - Brocken: een zwarte pil met een oranje stip voor feiten (`.b-diensten__feit`), een certificaatblad met een stempel die één keer "neerkomt", en een reviewbadge in de header.
- **Kaarten:** geen enkele Google Maps-embed.
  - Brocken tekent een SVG-radarkaart (ringen rond de vestiging; bij hover een oranje route) en statische OpenStreetMap-SVG's.
  - De Kievit heeft op `/contact/` een statische OSM-kaart van Venlo in een afgeronde kaart, met een adrespil linksboven en een knop "Route plannen".

```css
/* De Kievit /contact/, kaart met adrespil (inline CSS) */
.ct-adres .ct-kaart{position:relative;align-self:stretch;width:100%;min-height:19rem;border-radius:var(--r);overflow:hidden;background:#F2F0E6;box-shadow:0 26px 54px -34px rgba(34,49,78,.5)}
.ct-kaart__map{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:54% 30%}
.ct-kaart__pill{position:absolute;left:.9rem;top:.9rem;z-index:3;margin:0;display:inline-flex;align-items:center;gap:.45rem;background:rgba(255,255,255,.94);border:1px solid var(--lijn);border-radius:999px;padding:.5rem .9rem;font:700 .78rem/1.2 var(--font-kop);color:var(--bruin)}
```

### 3.16 Iconen, beeld, beweging, donkere secties, mobiel

- **Iconen:**
  - Een inline SVG-sprite met `<symbol>`s bovenaan de `<body>`, per pagina gesnoeid, gebruikt als `<svg aria-hidden="true"><use href="#i-phone"/></svg>`.
  - Lijniconen op 24×24 met streken van 2 px en ronde uiteinden; een paar gevulde (telefoon, ster, driehoekje).
  - Dienst-iconen staan altijd in een witte cirkel met schaduw (het "zegel").
  - Geen iconfont.
- **Beeld:**
  - Alles WebP, 2 of 3 breedtes per plek, `srcset` met precieze `sizes`, altijd `width` en `height`. Onder de vouw `loading="lazy" decoding="async"`, de hero `fetchpriority="high"`.
  - Het hero-beeld wordt voorgeladen, gesplitst per media query.
  - `object-fit:cover` met `object-position` per foto.
  - Uitgesneden mensen en wagens met `drop-shadow`.
  - Brocken controleert dat een bronfoto maar één keer per pagina voorkomt.
- **Beweging:**
  - Eén easing, `cubic-bezier(.22,.61,.36,1)`.
  - Onthulling bij scrollen met IntersectionObserver (`threshold:.16, rootMargin:'0px 0px -8% 0px'`): `translateY(22px)` en opacity 0 naar zichtbaar in .7 s. In groepen verspringt het 70 ms per kind.
  - **Valkuil:** de groepsobserver stond op `threshold:.12`. Wordt een groep op een telefoon hoger dan ongeveer 6 schermen (een kolom kaarten onder elkaar), dan komt er nooit 12 % tegelijk in beeld en blijft de hele groep op `opacity:0`. De Kievit heeft dat opgelost in commit `91f7b4a` (14-09-2026, groepsdrempel naar `0`), die lokaal nog niet is binnengehaald. **Brocken heeft de fout nog** (`_werk/build_paginas.py:275`, `threshold:.12`). Gebruik voor De Reus de gecorrigeerde versie uit 6.7: de lange home en de 8 blokken op `/diensten/` zijn precies het geval dat misging.
  - Hover alleen binnen `@media (hover:hover)` en gespiegeld met `:focus-visible`.
  - Alleen `transform` en `opacity`.
  - Onder `prefers-reduced-motion` alles uit, en alles blijft zichtbaar zonder JS (`.js [data-reveal]`).
- **Donkere secties:** tekst wit of 72 tot 86 % wit, labels in een lichte merktint, knoppen worden oranje of geel, de focusring wordt wit.
- **Mobiel:**
  - Een hamburger van 44 px onder 1024 px.
  - Een **plakkende belbalk onderaan** onder 768 px: Bellen + Offerte, matglas, rekening houdend met de safe area, verborgen zolang de drawer open is. `scroll-padding-bottom` zorgt dat de focus er niet achter verdwijnt.
  - De offertepil stapelt.
  - Foto's komen boven de tekst in `aspect-ratio:4/5`.

```css
/* bij beide gelijk */
.mcta{position:fixed;left:0;right:0;bottom:0;z-index:60;display:none;grid-template-columns:1fr 1fr;gap:.5rem;padding:.55rem var(--pad) calc(.55rem + env(safe-area-inset-bottom));background:rgba(247,247,246,.96);backdrop-filter:blur(8px);border-top:1px solid var(--lijn)}
.mcta .btn{width:100%;padding:.78rem .5rem;font-size:.9rem}
@media(max-width:767.98px){.mcta{display:grid}.footer__balk .wrap{padding-bottom:6.5rem}html{scroll-padding-bottom:calc(6rem + env(safe-area-inset-bottom))}}
.js [data-reveal]{opacity:0;transform:translateY(22px);transition:opacity .7s var(--ease),transform .7s var(--ease)}
.js [data-reveal].in{opacity:1;transform:none}
.js .hero [data-reveal]{opacity:1;transform:translateY(14px)}   /* hero nooit onzichtbaar: LCP */
@media(prefers-reduced-motion:reduce){.js [data-reveal],.js .hero [data-reveal]{opacity:1;transform:none;transition:none}}
```

---

## 4. Screenshots, en waarom het modern voelt

Genomen met headless Edge op 18-09-2026, via een lokale server over elke `site/`-map. Brocken is nog niet live en De Kievit staat live in dezelfde build. Elke pagina is eerst helemaal gescrold, zodat de onthullingen en lazy images geladen zijn. Per pagina en breedte zijn er twee bestanden: `-fold.png` (het eerste scherm) en `-full.jpg` (de hele pagina).

| Site | Pagina | 1440 px | 390 px |
|---|---|---|---|
| Brocken | Home `/` | `brocken-home-1440-*` | `brocken-home-390-*` |
| Brocken | Dienst `/diensten/particulier-verhuizingen/` | `brocken-dienst-particulier-1440-*` | `brocken-dienst-particulier-390-*` |
| Brocken | Stad `/werkgebied/tilburg/` | `brocken-stad-tilburg-1440-*` | `brocken-stad-tilburg-390-*` |
| De Kievit | Home `/` | `dekievit-home-1440-*` | `dekievit-home-390-*` |
| De Kievit | Dienst `/particulier-verhuizen/` | `dekievit-dienst-particulier-1440-*` | `dekievit-dienst-particulier-390-*` |
| De Kievit | Contact `/contact/` (er zijn geen stadspagina's; dit komt het dichtst in de buurt) | `dekievit-contact-1440-*` | `dekievit-contact-390-*` |
| De Reus, huidige site (hoofdstuk 7) | Home `/` (root van deze repo, commit `504b21b`) | `dereus-huidig-home-1440-*` | `dereus-huidig-home-390-*` |

**Let op bij de mobiele versies van de hele pagina:** vaste elementen (header, belbalk) staan soms midden of onderaan in beeld. Dat komt door de manier van vastleggen, niet door de site.

**Wat je ziet, en waarom het modern voelt:**
1. **Eén groot beeld met echte mensen.** Het eerste scherm is een echte foto van het eigen team voor de eigen wagen, met een donkere waas. Daarover staat een grote kop van één of twee regels met één gemarkeerd woord. Geen stockfoto's, geen carrousel.
2. **Diepte door overlap.** De offertebox valt over de onderrand van de hero. Uitgesneden mensen staan vóór vlakken en kaarten vallen over foto's. Zo lijkt de pagina uit lagen te bestaan in plaats van platte banden.
3. **Conversie die aanvoelt als een product.** De offertepil lijkt op de zoekbalk van een boekingssite en de score staat er direct naast. Bij Brocken ziet de Van → Naar-rij eruit als een verzendlabel. Bij De Kievit rekenen de calculators live.
4. **Rust en ruimte.** Een container van 1200 px, secties van 64 tot 120 px hoog, één verzadigde accentkleur, zachte lange schaduwen, radii van 14 tot 28 px en pillen voor alles wat klikt.
5. **Redactionele details.** Labels met een haarlijn of stip, genummerde lijsten (01, 02), grote cijfers in stapnummers, scores en m³, en letterlijke reviews met naam, plaats en datum.
6. **Beweging die je nauwelijks merkt.** Blokken glijden in bij scrollen, de header wordt matglas, foto's zoomen 5 % bij hover en ringen tekenen zichzelf. Nooit afleidend, en altijd uit bij "minder beweging".
7. **Op mobiel onder de duim.** Een plakkende balk Bellen / Offerte, een drawer met uitklapgroepen en een offertebox die stapelt tot één kolom.

**Brocken voelt rustiger en duurder:** één ondergrond, één donkere band, één lettertype. **De Kievit voelt voller en speelser:** meer vormen en decoraties, twee achtergrondkleuren die elkaar afwisselen en drie lettertypes.

---

## 5. Vergelijking

### 5.1 De gedeelde huisstijl in 5 punten

1. **Zelfde fundament:** statische HTML uit een Python-bouwstraat, Vercel met `trailingSlash`, header en footer bij de build gekopieerd, de home als bron voor gedeelde blokken, Nederlandse BEM-namen, zelf gehoste fonts, Web3Forms met PDOK-adresaanvulling.
2. **Zelfde bovenkant:** een transparante vaste header die bij scrollen matglas wordt (het logo wisselt en krimpt, er schuift een scorebadge in), een foto-hero met waas en korrel, uitgesneden team onderaan, label met haarlijn, H1 met één gemarkeerd woord.
3. **Zelfde conversie:** een gekleurde offertebox die over de hero valt, met een glazen keurmerkpil en een witte pil Van | Naar | Wanneer | Soort. Het grote formulier staat onderaan elke pagina (`#offerte`), met een foutoverzicht en een succesblok. Onderaan op mobiel een plakkende balk Bellen / Offerte.
4. **Zelfde vormtaal:**
   - gebroken witte ondergrond met één verzadigde accentkleur, alleen voor de belangrijkste actie;
   - pilknoppen met een pijltje en radii van 14 tot 28 px;
   - lange zachte schaduwen met negatieve spreiding;
   - container van 1200 px, `clamp()` voor maten en ruimte, `text-wrap:balance` op koppen.
5. **Zelfde discipline:**
   - vertrouwen als component: de score staat in header, pil, reviews, formulier en footer, met letterlijke reviews;
   - `<details>` voor de FAQ, en een drawer met focus-trap;
   - skiplink en focusring van 3 px;
   - contrast per paar gemeten;
   - beweging alleen met transform en opacity, uit bij `prefers-reduced-motion`;
   - JSON-LD als `@graph` in de `<head>`.

### 5.2 Waar ze verschillen, en wie het beter doet

| Onderwerp | De Kievit | Brocken | Beter |
|---|---|---|---|
| Sectieritme | afwisselend crème en licht teal, veel vormen per sectie, losse decoraties | één ondergrond, maximaal één donkere schuine band, één niet-rechte lijn per blok | **Brocken**: rustiger en duurder |
| Lettertypes | 3 (Poppins, Noto Sans, Zilla Slab) | 1 (Sora) | **Brocken**: samenhangend. De Reus heeft er 2, vastgelegd in het merkboek. |
| Knoppen | kleine hoofdletters met spatiëring | zinsnaamval, 600 | **Brocken**: beter leesbaar voor een oudere doelgroep |
| Accentkleur | geel voor actie, met donkere tekst | signaaloranje voor vormen, donker actie-oranje voor knoppen | **Brocken** voor de regel, **De Kievit** voor geel met donkere tekst (dat is ook de CTA van De Reus) |
| CSS-opbouw | één bestand van 162 KB met patches op volgorde | kern + CSS per blok, alleen geladen waar nodig | **Brocken** |
| Diensten op de home | fototegels (6 foto's nodig) | genummerde lijst + plakkende foto (werkt ook zonder foto) | **Brocken**, zeker zonder eigen foto's |
| Reviews | uitgelichte review + scorepaneel + raster, zonder JS | platen + scorering + rail met JS | **De Kievit** voor De Reus: 4 reviews passen in een raster, een rail met 4 kaarten is leeg |
| USP's onder de pil | 4 witte vertrouwenskaarten | geen (keurmerkpil in de box) | **De Kievit** |
| Werkwijze | paneel met 4 stappen en een schreefcijfer | schuine band met een route door de nummers | **Brocken** |
| FAQ | rijen met haarlijnen | kaarten + plakkende kop + belregel + exclusief open | **Brocken** |
| Offerteformulier | foto + teal paneel + calculator | verzendlabel + stappen + belknop + uitgesneden verhuizer | **Brocken** (rekenhulp van De Kievit later) |
| Contact en kaart | statische OSM-kaart met adrespil | radarkaart met ringen | **De Kievit** voor één vestiging |
| Video | mp4 van 10 MB, zelf gehost | Vimeo, pas na `load` | **Brocken** |
| Open Graph | alleen op de home | op elke pagina, met Twitter-kaart | **Brocken** |
| `aggregateRating` | bewust niet (risico van zelf toegekende reviews) | wel, 9,6 uit 640 | **De Kievit** |
| `lastmod` in de sitemap | geen | hash van de inhoud, zodat de datum alleen verandert als de inhoud verandert | **Brocken** |
| Zoom en brede schermen | geen begrenzing | `--vw` begrensd op 1440 | **Brocken** |

### 5.3 Prestaties, toegankelijkheid en SEO: wat we overnemen

| Patroon | Bron | Overnemen |
|---|---|---|
| Eén render-blocking kernstylesheet van ± 25 KB gzip, geen kritieke CSS (voorkomt CLS) | beide | ja |
| CSS en JS per blok, alleen geladen op pagina's met dat blok | Brocken | ja, al levert het bij 7 pagina's weinig op. Houd het simpel: kern + 2 of 3 blokbestanden. |
| `?v=`-cachebuster + `Cache-Control: immutable` op `/assets/` | beide | ja |
| Font-preload (1 of 2 bestanden), `font-display:swap`, latin en latin-ext los | beide | ja: `archivo-condensed-latin.woff2` en `inter-latin.woff2` voorladen |
| Hero voorladen met `imagesrcset`, gesplitst per media query, en `fetchpriority="high"` | beide | ja |
| WebP in 2 of 3 breedtes, altijd `width`/`height`, lazy onder de vouw | beide | ja; AVIF kan erbij |
| Video pas na `load`, alleen op desktop, met pauzeknop | beide | pas als er eigen beeld is |
| Hero-inhoud nooit `opacity:0` (LCP) en ruimte vasthouden voor beeld (CLS) | beide | ja |
| Skiplink naar `<main id="top" tabindex="-1">`, focusring van 3 px, drawer met focus-trap, `aria-expanded`, `<details>` | beide | ja |
| Foutoverzicht met `role="alert"` en links naar velden, `aria-invalid`, combobox-ARIA bij de adressen | beide | ja |
| Aanraakdoelen van minstens 44 px, `scroll-padding-bottom` voor de belbalk | beide | ja (De Reus-knoppen zijn 48 px) |
| Hover binnen `(hover:hover)`, gespiegeld met `:focus-visible` | Brocken | ja |
| Onthullen bij scrollen, met **drempel 0** voor groepen, een terugvaloptie zonder IntersectionObserver en `beforeprint` | De Kievit na commit `91f7b4a` (Brocken nog niet) | ja, zie 6.7. De oude drempel van `.12` laat lange kaartgroepen op mobiel onzichtbaar. |
| JSON-LD `@graph` in de `<head>`: bedrijf één keer als `#bedrijf`, overal met `@id` naar verwezen, `WebPage` per pagina | beide | ja |
| `Service`-knooppunten per dienst | Brocken | ja, op `/diensten/` (8 diensten in `hasOfferCatalog`) |
| Geen `aggregateRating` | De Kievit | ja: de score van De Reus staat op Google zelf |
| `FAQPage` alleen op één pagina | Brocken | hooguit op `/kosten/`. Google toont FAQ-resultaten sinds 2023 bijna niet meer voor bedrijven, dus weinig winst. |
| Open Graph + Twitter op elke pagina | Brocken | ja |
| `X-Robots-Tag: noindex` op elk ander domein dan productie | beide | ja |
| Kaal domein naar www (308) | De Kievit | ja, De Reus houdt www |
| Build faalt op em- en en-dashes | Brocken | ja, dat is ook de projectregel |
| `lastmod` alleen bij een inhoudelijke wijziging | Brocken | ja |

---

## 6. Advies voor De Reus

> **Lees dit samen met hoofdstuk 7.** Er is al een De Reus-site in deze repo. Dit hoofdstuk beschrijft het doelbeeld; de route ernaartoe is die bestaande code verbeteren (7.5 en 7.6), niet een nieuw prototype bouwen.

### 6.1 Richting: "Sterk en recht"

We nemen het skelet en de conversie-onderdelen van de huisstijl over, want die werken. Maar De Reus krijgt een eigen karakter dat uit het logo komt: **de reus staat recht.**
- **Zwaar en smal:** koppen in Archivo Condensed 800, groot, met korte regels.
- **Recht met één hoek:** geen gekantelde kaartjes, geen scheve foto's. De enige hoek is de **dakhelling van het huis in het logo**.
- **Het huisje uit het logo** als label, als fotokader en als badge.
- **Blauw draagt, geel doet:**
  - Koningsblauw voor koppen, iconen en de blauwe band;
  - Diepblauw voor gewicht;
  - Goudgeel alleen als vlak: de CTA, nummerschijven, sterren en een markering. Nooit als lijn of tekst op licht.

### 6.2 Randvoorwaarden uit het merkboek en de brief

- **Kleur:** 60 % licht, 30 % blauw, 10 % geel. Geen gele tekst of iconen op wit (1,51:1). Geen Koningsblauw op Diepblauw (1,77:1). Het logo in full colour alleen op Wit, Mist of blauw-50; op blauw altijd de negatieve versie.
- **Typografie:**
  - Archivo Condensed (breedte 75) voor koppen, Inter voor alles wat gelezen of aangeklikt wordt, lopende tekst 18 px.
  - Hoofdletters alleen in display-regels van hoogstens 5 woorden en in H6-labels.
  - Geen cursief: nadruk met 600.
- **Knoppen:** pil, Inter 700 op 17 px, minstens 48 px hoog.
  - CTA: Goudgeel `#FFCC33` met Diepblauwe tekst `#0B2352`, hover `#F7B817`.
  - Secundair: Koningsblauw met witte tekst, hover `#123780`.
- **Vertrouwen, alleen wat vaststaat:**
  - "4,9 uit 5 op Google", zonder aantal (open vraag 1.4).
  - **Geen keurmerken**: Erkende Verhuizers en dergelijke zijn niet bevestigd (open vraag 1.5).
  - "Standaard verzekerd", nooit "volledig verzekerd".
  - Beloftes uit de brief: binnen 24 uur gebeld, offerte dezelfde dag, geen voorrijkosten, één vaste verhuisadviseur, 7 dagen per week, geen studenten maar vakmensen.
- **Toon:** altijd "u". Kort, geruststellend, zonder hype.
- **Beeld:** er zijn geen eigen foto's (6.8).

### 6.3 Van huisstijlrol naar De Reus-token

| Rol in de huisstijl | Brocken | De Kievit | **De Reus** |
|---|---|---|---|
| Ondergrond | `#F7F7F6` | `#F6F4EC` crème | **Mist `--off-white` #F6F7F9** (koel, niet warm) |
| Kaarten en panelen | wit | wit | **Wit**, op Mist |
| Lichte merktint (labels, icoontegels) | `#FFF4F4` roze | `#E5F3F3` licht teal | **`--primary-50` #F3F7FE** en **`--primary-100` #E6EFFF** |
| Haarlijnen | `#F4CCCD` | `#C4E4E4` | **Zilvergrijs `--grey-300` #D3D7DE** (alleen decoratief); randen van velden **Staalgrijs `--grey-400`** |
| Merkkleur (koppen, links, focus) | bordeaux `#79242F` | donker teal `#006C68` | **Koningsblauw `--brand-primary` #1746A2** |
| Offertebox en blauwe band | bordeaux | teal `#00807A` | **Koningsblauw** |
| Donker (de ene band, footer, `.pk`) | `#450A14` / `#32060E` | navy `#22314E` / `#1A2540` | **Diepblauw `--brand-secondary` #0B2352**; onderste balk van de footer **#091938** (blauw 900) |
| Actie (primaire knop) | actie-oranje `#D24204`, witte tekst | geel `#FFD500`, donkere tekst | **Goudgeel `--color-cta` #FFCC33, Diepblauwe tekst** |
| Signaal (stippen, nummers, bogen) | signaaloranje `#FF5100` | geel of teal | **op licht: Koningsblauw. Op blauw of donker: Goudgeel.** Nummerschijven: gele schijf met Diepblauw cijfer. |
| Sterren | oranje | `#FFB612` | **Goudgeel**, altijd met de score als tekst erbij |
| Tekst / gedempte tekst | `#0A0A0A` / `#676767` | `#1D1D1B` / `#4B4B49` | **Inkt `--ink` #0E1A33** / **Leisteen `--grey-600` #5E6675** |
| Koppen | Sora 700 | Poppins 700 | **Archivo Condensed 800** (H3 700) |
| Tekst, knoppen, labels | Sora | Noto Sans | **Inter** 400/600/700 |
| Cijfers | Sora 700 tabelcijfers | Zilla Slab 700 | **Archivo Condensed 800**, `font-variant-numeric:tabular-nums` |
| Radius | 8 / 15 / 20 / 999 | 12 / 18 / 24 / 28 / 999 | **8 / 14 / 20 / 24 / 999** (`--radius-control`, `--radius-card`, `--radius-media`, 24 voor grote panelen, `--radius-button`) |
| Schaduw | twee lagen, lang en negatief | idem | idem, getint met Inkt: `rgba(14,26,51,…)` |
| Easing | `cubic-bezier(.22,.61,.36,1)` | idem | idem; `--ease-out` uit tokens.css voor kleine UI-overgangen |

### 6.4 Wat we van welke repo nemen

| Onderdeel | Bron | Aanpassing voor De Reus |
|---|---|---|
| Bouwstraat (`navigatie.py`, header en footer kopiëren, CSS minify, sprite snoeien, dash-bewaker, `lastmod`-hash) | Brocken | Tokennamen uit `brandbook/tokens.css`, geen oude namen |
| `vercel.json` | De Kievit (www) + Brocken (CSP report-only) | Kaal domein naar www, `noindex` buiten productie |
| Header, megamenu, drawer | beide (gelijk) | + een topbalk die wegvalt als de header vast staat (6.7); horizontaal logo |
| Hero home | beide | Tekst **links uitgelijnd**, waas getint met Diepblauw, geen uitgesneden team tot er foto's zijn, het gemarkeerde woord in **Goudgeel als tekstkleur** (geen balk achter witte letters: wit op geel haalt 1,51:1) |
| Offertepil | beide | Koningsblauwe box, **radius 24**, geen keurmerkpil maar een Google-pil (4,9 · standaard verzekerd · binnen 24 uur gebeld). **Verstuurt met GET naar `/offerte/`**, dat de velden invult (werkt zonder JS). |
| Vertrouwenskaarten | De Kievit `.trust` | Voor `#waarom`: 4 kaarten met een gele huisbadge in plaats van een icoontegel |
| Dienstenlijst (home) | Brocken `b-diensten` | 8 rijen in **2 kolommen**, zonder plakkende foto. De nummers in Archivo Koningsblauw. De pijlknop wordt geel bij hover. Links naar de ankers op `/diensten/`. |
| Diensten met ankernavigatie | Brocken `b-plaatsdiensten` | Voor `/diensten/`: 8 panelen, de wijzer in Koningsblauw, **fotokader in huisvorm** in plaats van een schuine rand |
| Werkwijze | Brocken `b-stappen` | Koningsblauwe band met **dakrand**, 5 stappen, gele schijven met Diepblauw cijfer, gestippelde route in wit op 50 % |
| Reviews | De Kievit `.reviews` | Uitgelichte Google-review + Diepblauw scorepaneel met "4,9" in Goudgeel + 3 kaarten. Label "Geverifieerde Google-review". Link naar het Google-profiel. |
| FAQ | Brocken `b-vragen` | Nummers en open-streep in Koningsblauw, het monogram-avatar wordt het favicon-huisje, belregel 085 000 5647 |
| Offerteformulier | Brocken `b-offerte` | Verzendlabel met een Koningsblauwe rand en een **gele** ronde pijl, stappen "Wat er na uw aanvraag gebeurt", belknop met een gele rand |
| Prijsopbouw | Brocken `b-maten` | Kaarten als traptreden voor woningtypes op `/kosten/#verhuizing` (Mist, Koningsblauw, Diepblauw), met een geel lipje |
| Contact en kaart | De Kievit `.ct-kaart` | Statische OSM-kaart van de omgeving rond de Lau Mazirellaan, adrespil, knop "Route plannen" |
| Footer | Brocken (opbouw) + De Kievit (claim) | Diepblauw, claim "Sterk in verhuizen. Zorgeloos geregeld." Geen logorij (geen keurmerken); wel het negatieve logo. |
| Mobiele belbalk, onthullingen, reduced motion | beide | Ongewijzigd, met De Reus-tokens |

### 6.5 Wat we anders doen, zodat het geen kloon wordt

| Van de huisstijl | Bij De Reus |
|---|---|
| Schuine rand (Brocken) of schuine band (De Kievit) | **Dakrand:** de ene donkere of blauwe band per pagina krijgt bovenaan een lage **nok**, als het dak van het huis: `clip-path:polygon(0 var(--dak),50% 0,100% var(--dak),100% 100%,0 100%)` |
| Oranje stip of haarlijn voor het label | **Huisje** uit het logo (met deur) als glyph van 1 em voor het label |
| Schuin bijgesneden foto's, kantelende kaarten, polaroids, spanband, reuzenwoorden op -8° | **Recht.** Foto's en panelen krijgen een **huisvormig kader** (het huis zonder deur als `mask`), één keer per pagina. Kaarten staan recht. |
| Sora of Poppins, 700, `-.028em` | **Archivo Condensed 800**, groter en smaller. Mag in hoofdletters voor één display-regel ("STERK IN VERHUIZEN."). |
| Gecentreerde hero-tekst | **Links uitgelijnd.** De offertepil blijft over de rand vallen. |
| Uitgesneden team in de hero | Tot de fotoshoot: geen mensen. Daarna: team links naast de tekst. |
| Warme crème ondergrond | **Koele Mist** met witte kaarten |
| Keurmerkpil | **Google-pil:** G-icoon, 4,9 uit 5, standaard verzekerd, binnen 24 uur gebeld |
| Slabcijfers (De Kievit) | Cijfers in Archivo Condensed 800 |
| Decoraties zoals bij, honingraat of motieven in de body | Geen. Hooguit een heel licht stippenraster in Koningsblauw op 10 % achter de hero-overgang. |

### 6.6 Paginasjablonen (sitemap 1.2)

#### Gedeeld op elke pagina

1. **Topbalk** (Diepblauw, 36 px, alleen desktop): 085 000 5647 · info@verhuisbedrijfdereus.nl · ★ 4,9 uit 5 op Google (naar `/#reviews`).
2. **Header:**
   - Links het logo horizontaal: negatief op de hero, full colour als hij vast staat. 56 px hoog, vast 44 px; de minimale hoogte van het logo is 28 px.
   - Menu:
     - **Diensten** (megamenu met 2 kolommen van 4 ankers + "Alle diensten");
     - **Kosten**;
     - **Werkwijze** (`/#werkwijze`);
     - **Over ons** (Over ons, Reviews, Veelgestelde vragen);
     - **Contact**.
   - Rechts de knop **Offerte aanvragen** (geel).
   - De telefoon staat in de topbalk, dus niet nog eens in de header.
3. **Footer** (Diepblauw):
   - claim met het negatieve logo, groot telefoonnummer, knoppen Offerte aanvragen + Mail ons;
   - kolommen **Diensten** (8 ankers), **De Reus** (Werkwijze, Over ons, Reviews, Veelgestelde vragen, Kosten) en **Contact** (adres, telefoon, e-mail, openingstijden);
   - onderste balk met Algemene voorwaarden · Privacyverklaring (en later het KvK-nummer).
4. **Mobiel:** de drawer in dezelfde volgorde en `.mcta` Bellen / Offerte aanvragen.

#### Home `/`, één lange pagina (H1 "Verhuisbedrijf in Den Haag")

| # | Anker | Blok (component, bron) | Ondergrond | Inhoud |
|---|---|---|---|---|
| 1 | `#offerte` | **Hero** (beide) + **offertepil** (beide) | foto, Diepblauw waas | Label "Verhuisbedrijf De Reus". H1 "Verhuisbedrijf in Den Haag" met ondertitel in de H1: "voor een **zorgeloze** verhuizing" (het gemarkeerde woord in Goudgeel). Subregel "Professionele verhuizers. Heldere prijzen. Altijd service op niveau." Pil: titel "Binnen 24 uur uw offerte", Google-pil, velden Van, Naar, Wanneer, Soort verhuizing en de knop Offerte aanvragen. |
| 2 | `#diensten` | **Dienstenlijst** (Brocken `b-diensten`, 2 kolommen) | Mist | Label "Onze diensten". H2 "Welke verhuizing u ook plant". 8 rijen: 01 Particulier ... 08 Woningontruiming, elk met één regel, naar `/diensten/#…`. Belregel onder de lijst: "Twijfelt u welke dienst past? Bel 085 000 5647." |
| 3 | `#waarom` | **Bewijskaarten** (De Kievit `.trust`, gele huisbadge) | Wit | H2 "Dit mag u van ons verwachten". 4 kaarten: één vaste verhuisadviseur, geen voorrijkosten, standaard verzekerd, 7 dagen per week. |
| 4 | `#werkwijze` | **Stappenband** (Brocken `b-stappen`) | **Koningsblauw met dakrand** | H2 "Zo werkt het, in 5 stappen": Offerte aanvragen, Persoonlijk contact, Offerte ontvangen, Planning bevestigen, Verhuisdag (teksten uit de brief). Knop Offerte aanvragen. |
| 5 | `#reviews` | **Reviews** (De Kievit) | Mist | Uitgelichte review, Diepblauw scorepaneel "4,9 uit 5 op Google" met een link naar het profiel, 3 kaarten (de 4 reviews uit de brief). |
| 6 | `#over-ons` | **Tekst + huisvenster** (De Kievit `.blok` met De Reus-kader) | Wit | Wie De Reus is: één vaste verhuisadviseur, vakmensen en geen studenten. Rechts de teamfoto in het huisvormige kader. Tot de fotoshoot: een Koningsblauw huisvlak met het negatieve beeldmerk en "STERK IN VERHUIZEN." |
| 7 | `#werkgebied` | **Kaart + 3 kaarten** (De Kievit-kaart met pin) | **Diepblauw met dakrand** (de enige donkere band) | Kaart van Nederland in lijnen (blauw 300) met een pil "Den Haag, hoofdkantoor" en een gele stip. 3 kaarten: Hoofdkantoor Den Haag (adres, tijden), Door heel Nederland (`/diensten/#nationaal`), Internationaal (`/diensten/#internationaal`). Wijkchips alleen als de klant ze bevestigt. |
| 8 | `#vragen` | **FAQ** (Brocken `b-vragen`) | Mist | 6 algemene vragen, plakkende kop met belregel. Prijsvragen staan op `/kosten/#vragen`. |
| 9 | | **Footer** | Diepblauw | Zie boven. Er staat geen donkere band direct boven de footer. |

**Regel voor de ondergrond:** per pagina hoogstens één Koningsblauwe band en één Diepblauwe band met dakrand, die nooit aan elkaar grenzen. De rest is Mist en Wit.

#### Diensten `/diensten/` (H1 "Onze diensten")

1. **Kop zonder foto (`.pk`)** in Diepblauw: H1, intro en een rij met 8 ankerchips (op mobiel horizontaal scrollbaar).
2. **Diensten met ankernavigatie** (Brocken `b-plaatsdiensten`):
   - **Links:** een plakkende index met 8 regels (icoon in een wit zegel + naam) en een Koningsblauwe wijzer die meeschuift.
   - **Rechts:** 8 panelen `#particulier #zakelijk #nationaal #internationaal #verhuislift #opslag #montage #woningontruiming`. Per paneel:
     - H2, 3 tot 5 alinea's;
     - de link "Wat kost dit?" naar `/kosten/#…`;
     - de knop "Offerte aanvragen" naar `/offerte/?dienst=…`.
   - **Beeld per paneel:** om en om links en rechts, in een **huisvormig kader** met een zegel. Tot er foto's zijn: een Koningsblauw-50 huisvlak met een groot lijnicoon.
   - `#internationaal` is het sterkste zoekwoord: dat paneel is breder en heeft ruimte voor H3's per land zodra de klant de landen bevestigt.
   - Een paneel dat `:target` is, wordt een witte kaart met een Koningsblauwe streep van 4 px links.
3. **Reviews, compact:** 2 kaarten + score.
4. **Offertepil als afsluiter** (zonder hero, als losse box).
5. Footer.

#### Kosten `/kosten/` (vraag vooraf, H1 "Wat kost een verhuisbedrijf?")

1. **Kop zonder foto (`.pk`)** in Diepblauw, met de H1 en een gele streep van 4 px eronder.
2. **Direct antwoord:** een witte kaart met een Koningsblauwe rand van 6 px links (De Kievit `.blok--paneel`). Het antwoord in 2 of 3 zinnen, zodat Google het als uitgelicht fragment kan tonen. Daaronder de ankerchips `#opbouw #verhuizing #opslag #verhuislift #montage #woningontruiming #annuleren #vragen`.
3. **`#opbouw`:** 3 kaarten naast elkaar: All-in prijs · Regieprijs · Geen voorrijkosten, betalen op de verhuisdag (volgens de voorwaarden, art. 5 en 7). Elke kaart met een grote Archivo-kop en een lijstje in de stijl "Altijd / Als u wilt" (Brocken `b-doos__menu`).
4. **`#verhuizing`:** 3 **kaarten als traptreden** (Brocken `b-maten`): studio of appartement (Mist), eengezinswoning (Koningsblauw), groot huis of kantoor (Diepblauw). Met een indicatie "vanaf €" **alleen als de klant die geeft** (beslissing 10.1); anders de factoren (m³, verdieping of lift, afstand, inpakken). Eén regel over Den Haag.
5. **`#opslag #verhuislift #montage #woningontruiming`:** een raster van 2×2 kaarten, elk met een H2, korte uitleg, "Meer over deze dienst" naar `/diensten/#…` en een offertelink.
6. **`#annuleren`:** een crème tipvak (`--accent-50`) met een Koningsblauwe rand: € 250 tot twee weken vooraf (art. 8). "Kosteloos wijzigen" alleen na bevestiging.
7. **`#vragen`:** het FAQ-accordeon (Brocken `b-vragen`) met prijsvragen.
8. **Offertepil als afsluiter**, dan de footer.

#### Offerte `/offerte/`

1. **Kop zonder foto (`.pk`):** H1 "Offerte aanvragen" en een subregel "Binnen 24 uur gebeld, dezelfde dag uw offerte".
2. **Formulierkaart** (Brocken `b-offerte`), gevuld vanuit `?van=&naar=&datum=&dienst=`:
   - **Links**, op blauw-50: "Wat er na uw aanvraag gebeurt", 3 stappen met gele cijfers, en een grote belknop 085 000 5647.
   - **Rechts:**
     - de Van → Naar-rij als verzendlabel met PDOK-aanvulling;
     - Wanneer (+ "weet ik nog niet"), soort verhuizing en woning;
     - naam, telefoon, e-mail en opmerkingen;
     - de knop "Aanvraag verzenden" (geel);
     - een regel over privacy met links naar de privacyverklaring en de algemene voorwaarden.
3. Een Google-pil onder de kaart. `/offerte/bedankt/` (noindex) met "U wordt binnen 24 uur gebeld".

#### Contact `/contact/`

- `.pk`, dan twee kolommen:
  - **links:** contactkaarten (telefoon groot, e-mail, adres, openingstijden: ma t/m za 08.00 tot 20.00, zo 09.00 tot 17.00);
  - **rechts:** het contactformulier, met dezelfde veldstijl als de offerte.
- Daaronder de **kaart met adrespil** (De Kievit) en "Route plannen".
- `/contact/bedankt/` (noindex).

#### Juridisch en systeem

- **Juridische pagina's:** `.pk` + één tekstkolom van 68ch, inhoudsopgave als pilchips (De Kievit `.jurtoc`), knop "Pdf downloaden" op de voorwaarden.
- **404:** `.pk` + links naar Diensten, Offerte en Contact.

### 6.7 Startlaag CSS (klaar om te bouwen)

Laad eerst `brandbook/tokens.css`. Kopieer de `@font-face`-regels en de fontbestanden naar `website/assets/fonts/` en pas de paden aan. Dit bestand (`assets/css/basis.css`) legt de huisstijl op de De Reus-tokens. Neem daarna de blok-CSS uit hoofdstuk 3 en de bijlagen over en vervang de oude variabelen volgens 6.3: `--b-bordeaux` wordt `--brand-primary`, `--b-signaal` wordt `--brand-primary` op licht en `--brand-accent` op donker, `--b-actie` wordt `--color-cta`, enzovoort.

```css
/* =====================================================================
   De Reus website: basislaag v0.1 (uit website/STIJLANALYSE.md, 6.7)
   Vereist brandbook/tokens.css (kleuren, fonts, typeschaal, radius).
   ===================================================================== */
:root{
  --maxw:1200px;
  --pad:var(--gutter);                               /* clamp(1rem,.5rem + 2vw,2.5rem) */
  --ruimte:clamp(4rem,2.8rem + 5vw,7.5rem);          /* sectiepadding, 64 tot 120 px */
  --dak:clamp(1.25rem,3.6vw,3.25rem);                /* hoogte van de nok op de dakrand */
  --r-paneel:24px;
  --ease:cubic-bezier(.22,.61,.36,1);
  --schaduw-kaart:0 1px 2px rgba(14,26,51,.05),0 14px 34px -22px rgba(14,26,51,.28);
  --schaduw:0 1px 2px rgba(14,26,51,.05),0 18px 40px -24px rgba(14,26,51,.32);
  --schaduw-lg:0 40px 90px -40px rgba(14,26,51,.55);
  /* Het huis uit het logo: met deur (glyph) en zonder deur (kader, badge) */
  --huisje:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 535.3 509.8'%3E%3Cpath d='M267.6 7.8L320.9 53.2V0H356.8V83.9L535.3 236.2H457.6V509.8H326.2V384.1H209.1V509.8H77.7V236.2H0Z'/%3E%3C/svg%3E");
  --huisvlak:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 535.3 509.8'%3E%3Cpath d='M267.6 7.8L320.9 53.2V0H356.8V83.9L535.3 236.2H457.6V509.8H77.7V236.2H0Z'/%3E%3C/svg%3E");
}

/* ---- Basis ---------------------------------------------------------- */
html{scroll-behavior:smooth;scroll-padding-top:110px}
body{margin:0;background:var(--off-white);color:var(--color-text);font:var(--weight-regular) var(--text-body)/var(--leading-body) var(--font-sans);overflow-x:clip}
h1,h2,h3{margin:0 0 .6em;font-family:var(--font-display);font-stretch:var(--font-display-stretch);font-weight:var(--weight-display);line-height:var(--leading-heading);color:var(--color-heading);overflow-wrap:break-word;text-wrap:balance}
h1{font-size:var(--text-h1);line-height:var(--leading-tight)}
h2{font-size:var(--text-h2)}
h3{font-size:var(--text-h3);font-weight:var(--weight-bold)}
h4{margin:0 0 .5em;font:var(--weight-bold) var(--text-h4)/var(--leading-snug) var(--font-sans);letter-spacing:-.01em;color:var(--graphite)}
p{margin:0 0 1.1em}
a{color:var(--color-link);text-underline-offset:3px}
a:hover{color:var(--color-link-hover)}
img{max-width:100%;height:auto}
:focus-visible{outline:var(--focus-ring);outline-offset:var(--focus-offset)}
:is(.hero,.pk,.footer,.sectie--donker,.sectie--blauw,.of-box,.topbar:not(.is-stuck)) :focus-visible{outline-color:var(--color-focus-on-brand)}
.wrap{max-width:var(--maxw);margin-inline:auto;padding-inline:var(--pad)}
.vh{position:absolute;width:1px;height:1px;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
.skiplink{position:fixed;top:0;left:max(12px,env(safe-area-inset-left));z-index:70;transform:translateY(-140%);background:var(--brand-secondary);color:var(--white);font:var(--weight-bold) 1rem/1 var(--font-sans);padding:.85rem 1.4rem;border-radius:0 0 12px 12px;text-decoration:none;transition:transform .18s var(--ease)}
.skiplink:focus{transform:translateY(0)}
main[tabindex="-1"]:focus{outline:none}

/* ---- Secties: Mist en Wit, plus hoogstens één blauwe en één donkere band met dakrand ---- */
.sectie{position:relative;padding-block:var(--ruimte)}
.sectie:not(.sectie--donker,.sectie--blauw) + .sectie:not(.sectie--donker,.sectie--blauw){padding-top:calc(var(--ruimte) * .5)}
.sectie--wit{background:var(--white)}
.sectie--donker,.sectie--blauw{isolation:isolate;color:var(--white);padding-block:calc(var(--ruimte) + var(--dak)) var(--ruimte)}
.sectie--donker{--grond:var(--brand-secondary)}
.sectie--blauw{--grond:var(--brand-primary)}
.sectie--donker::before,.sectie--blauw::before{content:"";position:absolute;inset:0;z-index:-1;background:var(--grond);
  clip-path:polygon(0 var(--dak),50% 0,100% var(--dak),100% 100%,0 100%)}   /* de nok van het dak */
:is(.sectie--donker,.sectie--blauw) :is(h2,h3){color:var(--white)}
:is(.sectie--donker,.sectie--blauw) p{color:rgba(255,255,255,.88)}
.sectie--donker a:not(.btn){color:var(--primary-300)}                  /* 8,12:1 op Diepblauw */
.sectie--blauw a:not(.btn){color:var(--white)}

/* ---- Kopgroep: label met huisje, kop, intro ---- */
.kopgroep{max-width:46rem;margin-bottom:clamp(2rem,1.4rem + 2vw,3.25rem)}
.kopgroep--midden{margin-inline:auto;text-align:center}
.label{display:inline-flex;align-items:center;gap:.6rem;margin:0 0 1rem;color:var(--brand-primary);font:var(--weight-bold) var(--text-h6)/1 var(--font-sans);letter-spacing:var(--tracking-eyebrow);text-transform:uppercase}
.label::before{content:"";flex:none;width:1.05em;height:1em;background:currentColor;-webkit-mask:var(--huisje) center/contain no-repeat;mask:var(--huisje) center/contain no-repeat}
:is(.hero,.pk,.footer,.sectie--donker,.sectie--blauw) .label{color:var(--brand-accent)}   /* 10,13:1 op Diepblauw, 5,73:1 op Koningsblauw */
.kop{margin:0}
.kop em,h1 em{font-style:normal;background:linear-gradient(180deg,transparent 62%,var(--accent-200) 62%);padding-inline:.05em}   /* op licht: zachte gele markeerstift achter Koningsblauw (7,5:1) */
:is(.hero,.pk,.sectie--donker,.sectie--blauw) :is(h1,h2,.kop) em{background:none;padding:0;color:var(--brand-accent)}   /* op donker: het woord zelf in Goudgeel */
.lead{margin:1rem 0 0;max-width:58ch;font-size:var(--text-lead);line-height:var(--leading-text);color:var(--color-text-muted);text-wrap:pretty}
:is(.sectie--donker,.sectie--blauw,.pk) .lead{color:rgba(255,255,255,.88)}
.display{font-family:var(--font-display);font-stretch:var(--font-display-stretch);font-weight:var(--weight-display);font-size:var(--text-display);line-height:var(--leading-tight);text-transform:uppercase}   /* hoogstens 5 woorden */

/* ---- Knoppen ---- */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:.6rem;min-height:48px;padding:.8rem 1.5rem;border:1px solid transparent;border-radius:var(--radius-button);font:var(--weight-bold) var(--text-button)/1.2 var(--font-sans);text-decoration:none;text-align:center;cursor:pointer}
.btn svg{order:2;flex:none;width:12px;height:12px;transition:transform .35s var(--ease)}
.btn--cta{background:var(--color-cta);color:var(--color-cta-text);box-shadow:inset 0 0 0 1px rgba(11,35,82,.18)}   /* rand geeft houvast op Wit en Mist */
.btn--cta:hover{background:var(--color-cta-hover);color:var(--color-cta-text)}
.btn--blauw{background:var(--color-button);color:var(--white)}
.btn--blauw:hover{background:var(--color-button-hover);color:var(--white)}
.btn--licht{background:var(--white);border-color:var(--grey-300);color:var(--brand-primary)}
.btn--licht:hover{background:var(--primary-50);border-color:var(--primary-200);color:var(--brand-primary)}
:is(.hero,.pk,.footer,.sectie--donker,.sectie--blauw) .btn--licht{background:transparent;border-color:rgba(255,255,255,.6);color:var(--white)}
:is(.hero,.pk,.footer,.sectie--donker,.sectie--blauw) .btn--licht:hover{background:rgba(255,255,255,.12)}
@media(hover:hover){.btn:hover svg{transform:translateX(4px)}}
.knoppen{display:flex;flex-wrap:wrap;gap:.75rem;margin-top:1.6rem}
@media(max-width:620px){.knoppen .btn{flex:1 1 100%}}

/* ---- Header met topbalk ---- */
.topbar{position:fixed;inset:0 0 auto;z-index:50;color:var(--white);transition:background .35s var(--ease),box-shadow .35s var(--ease)}
.topbar__util{overflow:hidden;max-height:40px;background:var(--brand-secondary);font:var(--weight-semibold) var(--text-xs)/1 var(--font-sans);transition:max-height .35s var(--ease)}
.topbar__util .wrap{display:flex;justify-content:flex-end;align-items:center;gap:1.5rem;min-height:36px}
.topbar__util a{color:var(--white);text-decoration:none}
.topbar__util a:hover{text-decoration:underline}
.topbar__main .wrap{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding-block:.9rem;transition:padding .35s var(--ease)}
.topbar__logo{position:relative;display:block}
.topbar__logo img{display:block;height:56px;width:auto;transition:opacity .35s var(--ease),height .35s var(--ease)}   /* dereus-logo-horizontaal-negatief.svg */
.topbar__logo img+img{position:absolute;left:0;top:0;opacity:0}                                                  /* dereus-logo-horizontaal.svg */
.topbar.is-stuck{background:rgba(246,247,249,.92);-webkit-backdrop-filter:saturate(1.4) blur(12px);backdrop-filter:saturate(1.4) blur(12px);box-shadow:0 2px 10px rgba(14,26,51,.08);color:var(--color-text)}
.topbar.is-stuck .topbar__util{max-height:0}
.topbar.is-stuck .topbar__main .wrap{padding-block:.5rem}
.topbar.is-stuck .topbar__logo img{height:44px;opacity:0}
.topbar.is-stuck .topbar__logo img+img{opacity:1}
@media(min-width:1024px){
  .topbar::before{content:"";position:absolute;inset:0 0 auto;height:180px;z-index:-1;pointer-events:none;background:linear-gradient(180deg,rgba(11,35,82,.55) 0%,rgba(11,35,82,.4) 45%,rgba(11,35,82,0) 100%);transition:opacity .35s var(--ease)}
  .topbar.is-stuck::before{opacity:0}}
@media(max-width:767.98px){.topbar__util{display:none}}
@media(max-width:620px){.topbar__logo img{height:40px}.topbar.is-stuck .topbar__logo img{height:36px}.topbar__main .btn--cta{min-height:44px;padding:.55rem 1rem}}   /* ruimte voor logo, knop en hamburger op 390 px */
/* nav, megamenu en drawer: neem 3.2 over; de hoverkleur van links op de hero wordt var(--accent-200), en vast var(--brand-primary) */

/* ---- Hero ---- */
.hero{position:relative;isolation:isolate;overflow:hidden;display:grid;align-items:end;min-height:min(88vh,820px);background:var(--brand-secondary);color:var(--white)}
.hero__bg{position:absolute;inset:0;z-index:-3}
.hero__bg img{width:100%;height:100%;object-fit:cover;object-position:center 40%}
.hero__veil{position:absolute;inset:0;z-index:-2;pointer-events:none;background:
  linear-gradient(90deg,rgba(11,35,82,.78) 0%,rgba(11,35,82,.45) 45%,rgba(11,35,82,.1) 75%),
  linear-gradient(180deg,rgba(11,35,82,.55) 0%,rgba(11,35,82,0) 30%,rgba(11,35,82,.25) 65%,rgba(11,35,82,.9) 100%)}   /* donker aan de tekstkant (links) */
.hero__grain{position:absolute;inset:0;z-index:-1;opacity:.05;pointer-events:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
.hero__content{max-width:44rem;padding-block:12rem calc(clamp(56px,7.5vw,104px) + 3.5rem)}
.hero h1{margin:0;color:var(--white);font-size:var(--text-display);text-shadow:0 4px 30px rgba(0,0,0,.3)}
.hero h1 .sub{display:block;margin-top:.35rem;font-size:.55em;line-height:1.1}
.hero__sub{margin:1.1rem 0 0;max-width:38rem;font-size:var(--text-lead);color:rgba(255,255,255,.92)}
.hero--pagina{min-height:min(60vh,520px)}
@media(max-width:760px){.hero__content{padding-top:9rem}}

/* ---- Offertepil (verstuurt met GET naar /offerte/) ---- */
.offerte-overlay{position:relative;z-index:6;padding:0 var(--pad) clamp(2.5rem,4vw,3.75rem);display:flow-root}
.of-wrap{position:relative;max-width:calc(var(--maxw) - 2 * var(--pad));margin:clamp(-104px,-7.5vw,-56px) auto 0}
.of-box{position:relative;border-radius:var(--r-paneel);background:var(--brand-primary);color:var(--white);padding:clamp(22px,2.6vw,34px) clamp(22px,3vw,40px);box-shadow:0 24px 60px -12px rgba(23,70,162,.45)}
.of-title{margin:0 0 .25rem;font:var(--weight-display) clamp(1.5rem,1.2rem + 1vw,2rem)/1.1 var(--font-display);font-stretch:var(--font-display-stretch);color:var(--white)}
.of-sub{margin:0 0 1rem;color:rgba(255,255,255,.88);font-size:var(--text-small)}
.of-google{position:absolute;top:18px;right:22px;display:flex;align-items:center;gap:.9rem;padding:.45rem .9rem;border-radius:999px;background:rgba(11,35,82,.35);border:1px solid rgba(255,255,255,.2);font:var(--weight-semibold) .875rem/1.2 var(--font-sans)}
.of-google b{font:var(--weight-display) 1.35rem/1 var(--font-display);font-stretch:var(--font-display-stretch);color:var(--brand-accent)}
.of-pill{display:grid;grid-template-columns:1fr 1px 1fr 1px .75fr 1px 1fr auto;align-items:stretch;padding:6px;border-radius:999px;background:var(--white);box-shadow:0 8px 24px rgba(14,26,51,.18)}
.of-field{display:flex;flex-direction:column;justify-content:center;min-width:0;padding:8px 18px}
.of-field span{margin:0 0 4px;font:var(--weight-bold) .75rem/1 var(--font-sans);letter-spacing:var(--tracking-eyebrow);text-transform:uppercase;color:var(--grey-600)}
.of-field input,.of-field select{width:100%;padding:0;border:0;outline:0;background:none;appearance:none;font:var(--weight-regular) 1rem/1.4 var(--font-sans);color:var(--color-text)}
.of-field:focus-within{border-radius:999px;box-shadow:inset 0 0 0 2px var(--brand-primary)}
.of-divider{align-self:center;width:1px;height:38px;background:var(--grey-300)}
.of-pill .btn--cta{border-radius:999px;white-space:nowrap}
@media(min-width:761px) and (max-width:1139px){.of-pill{grid-template-columns:1fr 1fr;gap:4px;border-radius:22px}.of-divider{display:none}.of-pill .btn--cta{grid-column:1/-1;border-radius:14px}}
@media(max-width:880px){.of-google{position:static;width:max-content;max-width:100%;margin-bottom:.9rem}}
@media(max-width:760px){.of-wrap{margin-top:-48px}.of-pill{grid-template-columns:1fr;gap:6px;border-radius:18px;padding:8px}.of-divider{display:none}.of-field{padding:10px 14px;border-bottom:1px solid var(--grey-300)}.of-pill .btn--cta{border-radius:14px}}

/* ---- Huisvenster: foto of vlak in de vorm van het huis (één keer per pagina) ---- */
.huisvenster{position:relative;aspect-ratio:535.3/509.8;-webkit-mask:var(--huisvlak) center/contain no-repeat;mask:var(--huisvlak) center/contain no-repeat;background:var(--primary-100)}
.huisvenster img{width:100%;height:100%;object-fit:cover}
.huisbadge{display:grid;place-items:end center;width:3.6rem;aspect-ratio:535.3/509.8;padding-bottom:.35rem;background:var(--brand-accent);color:var(--brand-secondary);-webkit-mask:var(--huisvlak) center/contain no-repeat;mask:var(--huisvlak) center/contain no-repeat}
.huisbadge svg{width:1.5rem;height:1.5rem}

/* ---- Kop zonder foto (diensten, kosten, offerte, contact, juridisch) ---- */
.pk{position:relative;overflow:hidden;isolation:isolate;background:var(--brand-secondary);color:var(--white);padding-block:calc(var(--pk-bar,150px) + 1.5rem) clamp(2.5rem,4vw,3.5rem)}
.pk::before{content:"";position:absolute;z-index:-1;right:-3rem;bottom:-2rem;width:clamp(12rem,24vw,20rem);aspect-ratio:535.3/509.8;background:rgba(255,255,255,.06);-webkit-mask:var(--huisje) center/contain no-repeat;mask:var(--huisje) center/contain no-repeat}
.pk h1{margin:0;color:var(--white);font-size:var(--text-h1)}
.pk h1::after{content:"";display:block;width:3.2rem;height:4px;margin-top:.9rem;border-radius:4px;background:var(--brand-accent)}
@media(max-width:767.98px){.pk{--pk-bar:96px}}

/* ---- Mobiele belbalk ---- */
.mcta{position:fixed;left:0;right:0;bottom:0;z-index:60;display:none;grid-template-columns:1fr 1fr;gap:.5rem;padding:.55rem var(--pad) calc(.55rem + env(safe-area-inset-bottom));background:rgba(246,247,249,.96);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);border-top:1px solid var(--grey-300)}
.mcta .btn{width:100%;padding:.7rem .5rem}
body.drawer-open .mcta{display:none}
@media(max-width:767.98px){.mcta{display:grid}html{scroll-padding-bottom:calc(6rem + env(safe-area-inset-bottom))}.footer{padding-bottom:5.5rem}}

/* ---- Onthullen en minder beweging ---- */
.js [data-reveal]{opacity:0;transform:translateY(22px);transition:opacity .7s var(--ease),transform .7s var(--ease)}
.js [data-reveal].in{opacity:1;transform:none}
.js [data-reveal-groep]>*{opacity:0;transform:translateY(16px);transition:opacity .55s var(--ease),transform .55s var(--ease)}
.js [data-reveal-groep]>*.in{opacity:1;transform:none}
.js .hero [data-reveal]{opacity:1;transform:translateY(14px)}
.js .hero [data-reveal].in{transform:none}
@media(prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .js [data-reveal],.js [data-reveal-groep]>*,.js .hero [data-reveal]{opacity:1;transform:none;transition:none}
  *,*::before,*::after{animation-duration:.001ms!important;transition-duration:.001ms!important}}
```

**Onthullen bij scrollen, de gecorrigeerde versie.** Zet dit onderaan elke pagina of in het kernscript, samen met `<script>document.documentElement.className+=' js'</script>` in de `<head>`:

```js
// Onthullen zodra een blok in beeld komt. Drempel 0 voor zowel losse blokken als groepen:
// een groep kaarten die op een telefoon hoger is dan ongeveer 6 schermen haalt nooit 12 % zichtbaarheid
// en zou dan onzichtbaar blijven (fout in de oude huisstijl, opgelost in De Kievit 91f7b4a).
// De rootMargin onderaan zorgt dat het blok toch pas iets in beeld komt voordat het verschijnt.
(function(){
  var el=document.querySelectorAll('[data-reveal]'),gr=document.querySelectorAll('[data-reveal-groep]');
  function aan(){
    [].forEach.call(el,function(e){e.classList.add('in')});
    [].forEach.call(gr,function(g){[].forEach.call(g.children,function(k){k.classList.add('in')})});
  }
  // Terugvaloptie: geen IntersectionObserver of minder beweging gewenst, dan alles direct tonen
  if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches){aan();return}
  var io=new IntersectionObserver(function(es){es.forEach(function(x){
    if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}
  })},{threshold:0,rootMargin:'0px 0px -8% 0px'});
  [].forEach.call(el,function(e){io.observe(e)});
  var ioG=new IntersectionObserver(function(es){es.forEach(function(x){
    if(!x.isIntersecting)return;
    [].forEach.call(x.target.children,function(k,i){k.style.transitionDelay=Math.min(i*70,560)+'ms';k.classList.add('in')});
    ioG.unobserve(x.target);
  })},{threshold:0,rootMargin:'0px 0px -6% 0px'});
  [].forEach.call(gr,function(g){ioG.observe(g)});
  addEventListener('beforeprint',aan);   // wie de pagina afdrukt, ziet alles
})();
```

Regels erbij:
- Zet `data-reveal` op losse blokken van normale hoogte (een kopgroep, een kaart, een foto), **nooit op een hele lijst of een lange container**. Een lijst krijgt `data-reveal-groep`.
- De hero krijgt nooit `opacity:0` (LCP): de CSS in 6.7 regelt dat.
- **Testen:** controleer op 390×664 dat elke sectie zichtbaar wordt, ook bij snel scrollen en bij binnenkomst via een anker (`/diensten/#opslag`).

**Aanwijzingen bij de rest van de blokken (vervang de oude tokens):**
- **Dienstenlijst (home):**
  - Brocken `b-diensten__lijst` in `display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:clamp(2rem,4vw,4rem)`, zonder `__beeld`;
  - het nummer via `counter()` in Archivo 800, 1.5rem, Koningsblauw;
  - de veegstreep 3 px Koningsblauw;
  - de pijlknop bij hover `background:var(--brand-accent);border-color:var(--brand-accent);color:var(--brand-secondary)`;
  - de naam in Archivo 700 `clamp(1.35rem,1rem + 1vw,1.75rem)` en `color:var(--graphite)`.
- **Bewijskaarten:** De Kievit `.trust__item`, met de icoontegel vervangen door `.huisbadge`. 4 kolommen, 2 onder 900 px, 1 onder 520 px.
- **Stappenband:** Brocken `b-stappen`, met deze aanpassingen:
  - `.b-stappen__baan::before` wordt `background:var(--brand-primary)` met de dak-`clip-path` van `.sectie--blauw` (nok bovenaan, vlakke onderkant);
  - route `border-top:2px dashed rgba(255,255,255,.5)`;
  - nummerschijf `background:var(--brand-accent);color:var(--brand-secondary);box-shadow:0 0 0 4px var(--brand-secondary)`, cijfer in Archivo 800;
  - `--bs-nr:2.8rem`, en 5 kolommen vanaf 1000 px.
- **Reviews:** De Kievit `.reviews`, met deze aanpassingen:
  - `.scorepaneel{background:var(--brand-secondary)}`;
  - `.scorepaneel__cijfer b` in Archivo 800 `3.6rem` en `var(--brand-accent)`;
  - het citaat in Inter 600 `clamp(1.2rem,1.05rem + .6vw,1.45rem)/1.5` (geen Archivo in lopende tekst);
  - kaarten `border:1px solid var(--grey-300);border-radius:var(--radius-card)`;
  - sterren `color:var(--brand-accent)` met de score als tekst ernaast.
- **FAQ:** Brocken `b-vragen`, met deze aanpassingen:
  - nummers en open-streep in `var(--brand-primary)`;
  - plus-schijf `var(--primary-50)` en open `var(--brand-primary)` met een wit kruis;
  - `.b-vraag__a::before` wordt een wit rondje met het favicon-huisje;
  - de telefoonlijn onderstreept met `var(--brand-accent)` op 3 px, onder de tekst (een decoratieve lijn, de tekst zelf blijft Inkt).
- **Offerteformulier:** Brocken `b-offerte`, met deze aanpassingen:
  - labelrij `border:2px solid var(--brand-secondary);box-shadow:5px 5px 0 var(--primary-100)`;
  - ronde pijl `var(--brand-accent)` met een Diepblauwe pijl;
  - linkerkolom `var(--primary-50)`;
  - velden `border:1.5px solid var(--grey-400)` (3,27:1 op Mist), focus `3px solid var(--brand-primary)`.
- **Kaarten als traptreden (`/kosten/`):** Brocken `b-maten__maat`, de treden in `var(--white)` (met `--schaduw`), `var(--brand-primary)` en `var(--brand-secondary)`, met een lipje van 5 px in `var(--brand-accent)`.

### 6.8 Beeld: de grootste open vraag

Beide voorbeeldsites halen hun uitstraling voor de helft uit **eigen foto's met echte mensen**. Ze zijn uitgesneden en staan vóór vlakken. De Reus heeft nu één stockfoto, dus:

1. **Fotoshoot (advies, vóór de lancering).** Liefst op één dag in Den Haag, met team en materieel in de nieuwe huisstijl:
   - hero: 3 of 4 verhuizers in een Koningsblauwe polo voor de bus, in een herkenbare Haagse straat. Liggend 1920×1280 en staand 900×1200.
   - bus met belettering (zijkant en driekwart) en de verhuislift aan een bovenwoning;
   - per dienst één foto (8): een bank op de trap, kratten op kantoor, een bus op de snelweg, een bus met een buitenlands kenteken of veerpont, de lift aan de gevel, opslag, een kast monteren en een lege, rustige kamer (woningontruiming);
   - portret van de verhuisadviseur (voor `#over-ons` en contact) en iemand aan de telefoon;
   - **uitgesneden versies** (transparant) van de teamgroep, van één verhuizer met doos, van de persoon aan de telefoon en van de bus. Die zijn nodig voor de hero, het formulier en de footer.
2. **Tot die tijd:**
   - Geen stockfoto's met gezichten; die kosten geloofwaardigheid.
   - Wel foto's van Den Haag (Wikimedia Commons met naamsvermelding, zoals Brocken dat voor steden doet) voor de hero en het werkgebied.
   - Verder grafische composities die zonder mensen werken: Koningsblauwe huisvlakken met lijniconen, grote Archivo-cijfers en de dienstenlijst zonder foto's.
3. **Iconen:** één set lijniconen (24×24, streep 2 px, ronde uiteinden, zoals beide sites) in de sprite. De brief zegt dat de huidige set van De Reus gevulde en lijniconen mengt, dus maak die gelijk.
4. **Video:** pas met eigen beeld, en dan zoals Brocken: na `load`, alleen op desktop, met pauzeknop.

### 6.9 Techniek en SEO voor de bouw

- **Head, in volgorde:**
  1. `<script>document.documentElement.className+=' js'</script>`;
  2. preload `archivo-condensed-latin.woff2` en `inter-latin.woff2`;
  3. preload van het hero-beeld (`imagesrcset`, gesplitst per media, `fetchpriority="high"`);
  4. `tokens.css` en `basis.css` (samen geminificeerd);
  5. `defer`-scripts.
- **JSON-LD** als `@graph` in de `<head>`:
  - home: `MovingCompany` `#bedrijf` met naam, url, telefoon, e-mail, adres Lau Mazirellaan 336, 2525 ZJ Den Haag, `openingHoursSpecification` (ma t/m za 08.00 tot 20.00, zo 09.00 tot 17.00), `areaServed` (Den Haag, Nederland), logo en afbeelding;
  - verder `WebSite` en per pagina `WebPage` met `about:#bedrijf`;
  - `/diensten/`: `hasOfferCatalog` met 8 `Service`-knooppunten die naar de ankers verwijzen.
  - **Geen `aggregateRating`.** Geen `BreadcrumbList`: er zijn geen niveaus.
- **Open Graph en Twitter** op elke pagina (`og.jpg` 1200×630, met het logo op een Koningsblauw vlak tot er een foto is). `theme-color` `#1746A2`.
- **Formulieren:**
  - Web3Forms, honeypot, foutoverzicht, PDOK-aanvulling;
  - de offertepil verstuurt met `method="get" action="/offerte/"` en `/offerte/` leest `URLSearchParams`, dus werkt het zonder JS;
  - `?dienst=` kiest het type vooraf.
- **`vercel.json`:** `trailingSlash:true`, kaal domein naar www (308), `noindex` op elk ander domein, `immutable` op `/assets/`, beveiligingsheaders zoals beide sites. Een CSP (report-only) mag Web3Forms en PDOK toestaan.
- **Bewakers bij de build:** geen em- en en-dashes, geen restanten van sjablonen, een skiplink en `<main tabindex="-1">` op elke pagina, beschrijvingen van hoogstens 158 tekens.

### 6.10 Open punten

1. **Fotoshoot** (6.8): zonder eigen beeld blijft het ontwerp een stap onder de voorbeelden.
2. **Prijsindicaties** voor `/kosten/#verhuizing` (sitemap 10.1): de traptreden werken met en zonder bedragen.
3. **Wijken** voor `#werkgebied`: alleen als de klant ze bevestigt.
4. **Namen van teamleden** (Dennis, Jack, Vincent, Omar in de reviews): alleen noemen als de klant dat goedkeurt.
5. **Horizontaal logo in de header:** dat is een afgeleide van logo 02 en de klant moet het nog goedkeuren (`brandbook/assets/logo/README.md`). Valt het af, dan komt het staande logo zonder tagline in de header, 64 px hoog.
6. **Rekenhulpen** (dozen, m³) zoals De Kievit: nuttig voor `/kosten/`, maar pas in een volgende fase.

---

## 7. Bestaande De Reus-site (repo TugcheSezr/dereus)

- **Bron (alleen gelezen):** `index.html`, `css/` (`style.css`, `hero.css`, `3d.css`, `rit.css`, `werkwijze.css`) en `js/` in de root van `C:\users\arnas\git_repos\dereus`, commit `504b21b` van 18-09-2026 ("Homepage De Reus vernieuwd in merkboekstijl"). Gebouwd door een teamgenoot, publieke repo.
- **Screenshots:** `referentie/dereus-huidig-home-1440-fold.png`, `-1440-full.jpg`, `-390-fold.png`, `-390-full.jpg`.

### 7.1 Wat het is

- **Techniek:**
  - Eén lange pagina, met de hand geschreven: 39 KB HTML, 5 CSS-bestanden (65 KB samen) en 4 kleine scripts. Zonder bouwstap.
  - Geen `vercel.json`, `robots.txt` of `sitemap.xml`.
- **Tokens:** eigen tokens met het voorvoegsel `--dr-` (`css/style.css:4-47`), "volgens Merkboek v2.0 (september 2026)". **Ons merkboek is versie 1.0** (`brandbook/index.html`) en bevat geen van de afwijkende waarden. Er zijn nu dus twee bronnen van waarheid.
- **Lettertypes:** via het Google Fonts-CDN: Roboto Condensed 600 tot 900, Roboto 400/500/700 en Nunito 900. Nunito wordt geladen maar nergens gebruikt.
- **Blokken, van boven naar onder:**
  1. utilitybalk (3 USP's + "4,9/5 op Google");
  2. header;
  3. hero met foto, mascotte, zwevende 3D-dozen, chip "Standaard verzekerd" en offertekaart;
  4. `#over-ons`;
  5. `#offerte` (formulier);
  6. `#diensten` (8 tegels in twee groepen);
  7. "Dit mag u van ons verwachten" + spoedkaart;
  8. een schuine gele cijferband (4,9/5 · 7/7 · 24 uur · € 0);
  9. `#reviews` (4 kaarten);
  10. `#werkwijze` (5 stappen met foto's op blauw);
  11. `#aanvraag` (donker blok met een tweede offerteformulier);
  12. `#contact` (kaarten, formulier en een live status "Nu bereikbaar");
  13. footer, en de mobiele belbalk.

### 7.2 Wat het al overneemt van De Kievit en Brocken

| Onderdeel | In de site | Oordeel |
|---|---|---|
| Transparante header die vast wordt, logo wit en daarna in kleur (beide) | `.header.is-vast` zodra de utilitybalk uit beeld is | goed |
| Foto-hero met waas, label met dakje, H1 met markering (beide) | ja | goed, maar de H1 staat helemaal in kapitalen (7.4) |
| Figuur onderaan in de hero (het team bij beide) | de oude mascotte | wijkt af van het merkboek (7.4) |
| Offertekaart over de rand van de hero, met een vertrouwenspil en een pilformulier (beide) | ja: Google 4,9 · inboedel verzekerd · 7 dagen; velden Van, Naar, Datum | goed; soort verhuizing ontbreekt |
| Dienstentegels (De Kievit, maar zonder foto's) | 8 tegels met een icoon in twee groepen | goed; iconen wijken af |
| Schuine band (De Kievit `.opslag`) | gele cijferband met een blauwe rand | goed, één gele band per pagina |
| Reviewraster (De Kievit `.rgrid`) | 4 kaarten met sterren, naam en "Geverifieerde Google-review" | goed; scorepaneel en link naar alle reviews ontbreken |
| Stappen met route (Brocken `b-stappen`) | 5 genummerde fotokaarten op blauw met een gestippelde lijn | goed; de foto's zijn stock |
| Donker formulierblok (De Kievit `.leadblock`) | `#aanvraag` | tweede offerteformulier op dezelfde pagina |
| Drawer met focus-trap en Escape, mobiele belbalk, skiplink, focusring, `aria-invalid` (beide) | ja | goed |
| Eigen vondst | live status "Nu bereikbaar" in Nederlandse tijd (`main.js`), 3D-lagen (`3d.css`) en een rit met een vrachtwagen die meerijdt bij scrollen (`rit.css`, `rit.js`, maar **niet gekoppeld** in `index.html`) | de bereikbaarheidsstatus is sterk: houden |

### 7.3 Wat nog ontbreekt ten opzichte van beide

1. **De pagina's uit sitemap 1.2:**
   - `/diensten/` (8 blokken met ankernavigatie), `/kosten/`, `/offerte/` + bedankt, `/contact/` + bedankt, de juridische pagina's en een 404;
   - op de home de blokken `#werkgebied` en `#vragen`; `#waarom` heeft geen id.
   - De volgorde op de home wijkt af van `#offerte #diensten #waarom #werkwijze #reviews #over-ons #werkgebied #vragen`.
2. **Echte formulieren:**
   - Alle 3 formulieren sturen via `mailto:` met `enctype="text/plain"`. Dat opent het mailprogramma van de bezoeker; op veel telefoons en werkplekken gebeurt er dan niets.
   - Er is geen bevestigingspagina en geen meting.
   - Beide voorbeeldsites gebruiken Web3Forms met een honeypot, een foutoverzicht, PDOK-adresaanvulling en een succesblok.
   - Er staan twee offerteformulieren op één pagina (`#offerte` en `#aanvraag`).
3. **Lettertypes zelf hosten** in plaats van via het Google Fonts-CDN, met een preload. Beide voorbeeldsites doen dat. Het CDN stuurt het IP-adres van de bezoeker naar Google, wat onder de AVG gevoelig ligt.
4. **Beeld:**
   - `srcset` en `sizes` (nu één keer op de pagina) en `fetchpriority="high"` op de hero;
   - een `og:image`;
   - canonical met schuine streep, volgens de conventie van de sitemap.
5. **Livegang:** `vercel.json` (`trailingSlash`, kaal domein naar www, headers, `noindex` op previews), `robots.txt` en `sitemap.xml`.
6. **Gedeelde header en footer voor 7 pagina's:** een kleine bouwstap zoals `navigatie.py` bij beide voorbeeldsites, of een eenvoudige include.
7. **Reviews:** een scorepaneel en een link naar het Google-profiel voor alle reviews.
8. **JSON-LD:** het bestaande `MovingCompany` (goed, zonder `aggregateRating`) uitbreiden tot een `@graph` met `@id`, `WebPage` per pagina en `Service` op `/diensten/`.
9. **Onthullen bij scrollen:** de site heeft het niet, en dat is prima. Komt het er wel, gebruik dan de gecorrigeerde versie uit 6.7.

### 7.4 Waar het afwijkt van ons merkboek

| # | Onderwerp | In de site | Merkboek (bron) | Wat te doen |
|---|---|---|---|---|
| 1 | Kleuren | diepblauw `#0F2D6B`, mist `#F4F6FA`, inkt `#141A26`, lijn `#D5DBE6`, steengrijs `#5B6475`, ijsblauw `#E8EEF8` (ook als sectiekleur), zonlicht `#FFF3CC`, goud-hover `#F2B90F`, goed `#1B7F46`, fout `#C62828` | `brandbook/tokens.css`: Diepblauw `#0B2352`, Mist `#F6F7F9` (de kleur voor afwisselende secties), Inkt `#0E1A33`, Zilvergrijs `#D3D7DE`, Leisteen `#5E6675`, blauw 50 `#F3F7FE` (tegels), goud 100 `#FFF3D1`, CTA-hover `#F7B817`, Succes `#1E7A3C`, Fout `#B42318` | aliaslaag uit 7.6 |
| 2 | Lettertypes | Roboto Condensed, Roboto, Nunito | Archivo Condensed 800/700 voor koppen, Inter voor tekst; "Geen derde lettertype" (`color-type-system.md` 7 en 9) | zelf hosten uit `brandbook/assets/fonts/` |
| 3 | H1 | "DE BETROUWBARE KEUZE VOOR EEN ZORGELOZE VERHUIZING", 8 woorden in kapitalen, gewicht 900 | kapitalen alleen in display-regels van hoogstens 5 woorden (`color-type-system.md` 9); H1 van de home is "Verhuisbedrijf in Den Haag" (`SITEMAP.md` 4.2); de openingszin mag als kop blijven (`copy.md:155`) | H1 "Verhuisbedrijf in Den Haag" in zinsnaamval; de openingszin als subregel |
| 4 | Knoppen | radius 8 px; de knop in de header in Roboto Condensed-kapitalen | pilvormig (`--radius-button: 999px`), Inter 700 17 px, zinsnaamval, hooguit één gele knop per blok (`brandbook/index.html` Knoppen) | `.knop{border-radius:var(--radius-button);font-family:var(--font-sans);text-transform:none}` |
| 5 | Gele markering | in **elke** H2 (`<mark>`) | "één markering per scherm" (Goudgeel, `brandbook/index.html`) | alleen in de hero en hooguit één andere kop per scherm |
| 6 | Label-dakje | goudgeel driehoekje, ook op wit | geen gele iconen of lijnen op wit (1,51:1, `color-type-system.md` 9) | Koningsblauw op licht, Goudgeel op blauw (zoals `.label` in 6.7) |
| 7 | Logo in de header | eigen trace `img/de-reus-logo-02.svg` (47 KB, hele logo als pad), **met tagline**, 96 tot 104 px hoog (± 100 px breed), vast 60 px, mobiel 52 tot 64 px | header: "Logo zonder tagline, minimaal 100 px breed" (`microcopy.md:285`); het logo met tagline pas vanaf 160 px breed (`brandbook/assets/logo/README.md`) | officiële bestanden: `dereus-logo-horizontaal-negatief.svg` / `dereus-logo-horizontaal.svg` in de header (56 px, minimaal 28 px), favicon-set uit dezelfde map |
| 8 | Mascotte | in de hero, op een blauwe foto, in hetzelfde scherm als het nieuwe logo | "Zet de mascotte nooit naast het nieuwe logo"; op de huidige site alleen op Wit of Mist, tot de nieuwe site live gaat; open vraag aan de klant (`imagery.md`, Mascotte) | uit de hero; wachten op het besluit van de klant |
| 9 | Slogans | in de footer het logo **met tagline** direct boven "Sterk in verhuizen. Zorgeloos geregeld." | "Eén slogan per blok" (`copy.md:155`) | footer: logo zonder tagline + de pay-off |
| 10 | "Zonder verrassingen" | 3 keer, waaronder "zonder verrassingen achteraf" (werkwijze, stap 3) | "een heldere offerte vooraf", nooit "zonder verrassingen achteraf" (`copy.md:103`, algemene voorwaarden art. 5) | tekst aanpassen |
| 11 | Score | "4,9/5" (6 keer) | "4,9 uit 5 op Google", met komma en bron (`copy.md:104`) | tekst aanpassen |
| 12 | Iconen | lijn, één kleur ("merkboek 5.2") | gevuld, twee kleuren (Koningsblauw + één goudgeel onderdeel), raster van 48 px (`imagery.md`, Iconen); de set staat klaar in `brandbook/assets/imagery/icoon-*.svg` | de 8 dienst-iconen vervangen |
| 13 | Stockfoto's | 5 stockfoto's in de werkwijze (laptop, man aan de telefoon, pen, agenda, verhuizers) | "Tot er een eigen fotoshoot is: gebruik liever iconen of het beeldmerk dan stockfoto's" (`imagery.md`); niet "stockfoto's met onbekende verhuizers" (`microcopy.md`) | stapnummers en merkiconen tot de fotoshoot |
| 14 | Lopende tekst | 17 px, regelhoogte 1.65 | 18 px, 1.6 (`--text-body`, `--leading-body`) | via de aliaslaag |
| 15 | Focus op donker | ring in Goudgeel | wit op Koningsblauw en Diepblauw (`color-type-system.md` 4) | via de aliaslaag |

**Twee punten die niet in het merkboek staan, maar wel aandacht vragen:**
- **Reviewfoto's.** `img/avatar-*.webp` zijn gekopieerde profielfoto's van echte Google-gebruikers. Zonder hun toestemming is dat een privacyrisico. Google toont zelf initialen als er geen foto is: doe dat ook (de M en de D staan er al zo).
- **AI-beelden.** `_ai-beelden/gen.mjs` maakt fotorealistische beelden van "De Reus"-verhuizers, een verhuisadviseur, het team en een wagen met belettering die er (nog) niet is. Ze staan nog niet op de site. Publiceer ze niet alsof het echt de mensen en wagens van De Reus zijn: dat misleidt klanten en gaat in tegen de keuze van het merkboek voor een eigen fotoshoot. Als briefing voor die fotoshoot zijn ze wel bruikbaar.

### 7.5 Advies: verbeter deze code en bouw geen nieuw prototype

**Ja, het advies wordt een verbeterlijst voor deze codebase.**
- De site heeft het skelet van de huisstijl al: header, hero met offertekaart, drawer, belbalk, reviews, stappen en toegankelijkheid. De inhoud staat erin en de code is overzichtelijk.
- Een los prototype van de home zou een derde versie opleveren naast de site en het merkboek.
- **Doe het in overleg met de eigenaar van de repo (TugcheSezr):** het is haar publieke repo.
- Hoofdstuk 3 en 6 van dit document zijn het **doelbeeld**. De lijst hieronder is de route ernaartoe.
- Blijft dereus-f0 aan een prototype werken, dan liefst als **aftakking van deze code** en niet vanaf nul.

**Prioriteit 1: merk en afspraken (klein werk, groot effect)**
1. **Kleuren:** laad `tokens.css` en vervang de `:root` in `css/style.css` door de aliaslaag uit 7.6. Daarmee kloppen alle kleuren in één keer.
2. **Lettertypes:** host Archivo Condensed en Inter zelf (kopieer `brandbook/assets/fonts/*.woff2` naar de site; `brandbook/` zelf wordt niet gevolgd in git). Preload beide `-latin`-bestanden. Haal de Google Fonts-link en Nunito weg. Zet `font-stretch:var(--font-display-stretch)` op elke plek waar `--dr-font-kop` gebruikt wordt, en zet labels en knoppen op Inter.
3. **Logo's:**
   - header: `dereus-logo-horizontaal-negatief.svg` / `dereus-logo-horizontaal.svg`;
   - footer: `dereus-logo-zonder-tagline-negatief.svg` met de pay-off;
   - favicon: `dereus-favicon.ico`, `-32.png` en `-180.png` (apple-touch).
   - Alle bestanden staan in `brandbook/assets/logo/`.
4. **Teksten:**
   - H1 "Verhuisbedrijf in Den Haag" + de openingszin als subregel, in zinsnaamval;
   - "4,9 uit 5 op Google";
   - "een heldere offerte vooraf" in plaats van "zonder verrassingen";
   - één slogan per blok.
5. **Beeld:** mascotte uit de hero, stockfoto's uit de werkwijze (stapnummers of merkiconen), initialen in plaats van profielfoto's.
6. **Knoppen:** pilvormig, Inter 700 in zinsnaamval, één gele knop per blok.
7. **Formulieren:**
   - Web3Forms (of een andere backend) in plaats van `mailto:`, met honeypot, foutoverzicht en `/offerte/bedankt/`;
   - voeg `#offerte` en `#aanvraag` samen tot één formulier.

**Prioriteit 2: structuur volgens sitemap 1.2**
8. **Opsplitsen in 7 pagina's:**
   - de home met de blokken in de volgorde uit 6.6;
   - `/diensten/` met de ankernavigatie van Brocken (6.6) en de merkiconen;
   - `/kosten/`;
   - `/offerte/`, gevuld via de URL;
   - `/contact/`: het huidige blok `#contact` kan er vrijwel zo naartoe, met de bereikbaarheidsstatus;
   - de juridische pagina's en een 404.
9. **Gedeelde header en footer via een kleine bouwstap:** één `navigatie.py` of één include, zoals bij beide voorbeeldsites.
10. **Livegang:**
    - `vercel.json`, `robots.txt`, `sitemap.xml`;
    - canonical met schuine streep, `og:image`;
    - JSON-LD als `@graph` (6.9).
11. **Nieuwe blokken op de home:** `#werkgebied` (kaart en 3 kaarten) en `#vragen` (FAQ, 3.10); een scorepaneel bij de reviews.

**Prioriteit 3: afwerking**
12. **Iconen:** de gevulde tweekleurige iconen uit `brandbook/assets/imagery/` in de dienstentegels.
13. **Markeringen:** één gele markering per scherm; het label-dakje in Koningsblauw op licht.
14. **Dakrand:** de dakrand (6.5) voor de ene donkere band is optioneel. De schuine gele cijferband mag blijven (één gele band per pagina).
15. **Fotoshoot** (6.8). Daarna kan de mascotteplek in de hero naar het echte team.
16. **Houden:**
    - de live bereikbaarheidsstatus;
    - de drawer en de belbalk;
    - de 3D-dozen, als ze in het palet blijven;
    - de rit, als die gekoppeld wordt: die respecteert `prefers-reduced-motion` al.

### 7.6 Aliaslaag: de `--dr-`-tokens naar ons merkboek

Laad `tokens.css` vóór `style.css` en vervang het `:root`-blok bovenaan `css/style.css` door dit blok. De rest van de CSS blijft werken en haalt zijn waarden dan uit het merkboek.

```css
/* Verhuisbedrijf De Reus · de --dr-tokens van de site wijzen naar brandbook/tokens.css (merkboek 1.0) */
:root{
  /* merk */
  --dr-koningsblauw:var(--brand-primary);      /* #1746A2, gelijk */
  --dr-goudgeel:var(--brand-accent);           /* #FFCC33, gelijk */
  --dr-diepblauw:var(--brand-secondary);       /* was #0F2D6B, wordt #0B2352 */
  --dr-ijsblauw:var(--primary-50);             /* was #E8EEF8, wordt #F3F7FE (tegels en hover); secties worden Mist, zie onder */
  --dr-zonlicht:var(--accent-100);             /* was #FFF3CC, wordt #FFF3D1 */
  --dr-goud-hover:var(--color-cta-hover);      /* was #F2B90F, wordt #F7B817 */
  --dr-goud-actief:var(--color-cta-hover);     /* #D9A400 staat niet in het merkboek; goud 700 is alleen voor illustraties */
  /* neutraal */
  --dr-wit:var(--white);
  --dr-mist:var(--off-white);                  /* was #F4F6FA, wordt #F6F7F9 */
  --dr-lijn:var(--grey-300);                   /* was #D5DBE6, wordt #D3D7DE; randen van velden: var(--grey-400) */
  --dr-steengrijs:var(--grey-600);             /* was #5B6475, wordt #5E6675 */
  --dr-inkt:var(--ink);                        /* was #141A26, wordt #0E1A33 */
  /* signaal */
  --dr-goed:var(--success);                    /* was #1B7F46, wordt #1E7A3C */
  --dr-fout:var(--error);                      /* was #C62828, wordt #B42318 */
  /* vorm */
  --dr-radius-s:var(--radius-control);         /* 8 px voor velden; knoppen apart naar var(--radius-button) */
  --dr-radius-m:var(--radius-card);            /* was 12, wordt 14 */
  --dr-radius-l:var(--radius-media);           /* 20, gelijk */
  --dr-schaduw:var(--shadow-raised);
  --dr-schaduw-hoog:0 1px 2px rgba(14,26,51,.05),0 18px 40px -24px rgba(14,26,51,.32);
  --dr-focus:0 0 0 3px var(--color-focus);
  --dr-focus-donker:0 0 0 3px var(--color-focus-on-brand);   /* merkboek: wit op blauw */
  /* typografie */
  --dr-font-kop:var(--font-display);           /* altijd samen met font-stretch:var(--font-display-stretch); gewicht 900 wordt 800 */
  --dr-font:var(--font-sans);
  --dr-fs-display:var(--text-display);
  --dr-fs-h2:var(--text-h2);
  --dr-fs-h3:var(--text-h3);
  --dr-fs-intro:var(--text-lead);
  --dr-fs-body:var(--text-body);               /* 17 wordt 18 px */
  --dr-lh-body:var(--leading-body);            /* 1.65 wordt 1.6 */
  /* ruimte en beweging (schaal van 4 px, gelijk) */
  --dr-space-1:4px; --dr-space-2:8px; --dr-space-3:12px; --dr-space-4:16px;
  --dr-space-5:24px; --dr-space-6:32px; --dr-space-7:48px; --dr-space-8:64px; --dr-space-9:96px;
  --dr-sectie:var(--section-padding);
  --dr-max:1200px;
  --dr-duur:var(--duration-base);
  --dr-ease:var(--ease-out);
}
/* aanvullend, direct onder het blok */
.display,.h2,.h3,h3{font-stretch:var(--font-display-stretch)}
.display{font-weight:var(--weight-display);text-transform:none}   /* of kapitalen bij hoogstens 5 woorden */
.label,.knop,.groepkop,.footer__kop,.gegevens__lbl{font-family:var(--font-sans)}   /* labels (H6) en knoppen in Inter 700 */
.knop{border-radius:var(--radius-button);text-transform:none;letter-spacing:0}
.header .knop{text-transform:none;letter-spacing:0;font-size:1rem}   /* was kapitalen op 14 px */
.sectie--ijs{background:var(--off-white)}                          /* merkboek: Mist voor secties, blauw 50 alleen voor tegels */
.label::before{background:currentColor}                            /* het dakje in de labelkleur: Koningsblauw op licht */
.sectie--diep .label::before,.hero .label::before,.footer .label::before{background:var(--brand-accent)}
```

**Let op bij `tokens.css` in de site:** de `@font-face`-regels verwijzen naar `assets/fonts/…`, relatief aan het CSS-bestand. Kopieer `tokens.css` naar `css/` en de fonts naar een map die daarbij past (bijvoorbeeld `fonts/`), en pas de `src`-paden aan.
