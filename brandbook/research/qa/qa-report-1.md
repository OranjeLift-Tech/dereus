# QA report 1: brand book De Reus (first pass)

- **Reviewer:** dereus-6e (read only; the builder dereus-55 makes all fixes)
- **Reviewed state:** snapshot taken at 12:45 on 18 September 2026 (`index.html` 12:45:37, `book.css` 12:42:32, `tokens.css` 12:35:37, `book.js` 12:05:59). The book changed several times during the review. Anything fixed before 12:45 is listed under "Fixed during review" and not repeated below.
- **Method:** headless Edge through the DevTools protocol at 1440 px and 390 px, with full-page screenshots, console and network logs, the fonts the browser actually used (`CSS.getPlatformFontsForNode`), and a `printToPDF` A4 run rendered page by page. Copy was checked sentence by sentence against `content/copy.md` and `content/microcopy.md`. Dashes, typos, markers and claims were grepped across all of `brandbook\` except `research\`. The same probe was run on the Brocken book for comparison.
- **Re-checked against the 12:49 files:** P1.1 is resolved. Every other P1 and P2 finding is still present.
- **Out of scope for this pass:** placeholders marked VOLGT (8 left: dereus-70 ×1, dereus-f0 ×7).
- **Evidence** in this folder: `qa1-achtergronden-tegels.png`, `qa1-desktop-1440-omslag.png`, `qa1-mobiel-390-omslag.png`, `qa1-print-a4-p01-30.png`, `qa1-print-a4-p31-49.png`, `qa1-mockup-briefpapier-voet.png`.

---

## P1: must fix

### P1.1 Logo background examples showed the wrong thing (RESOLVED at 12:49, verified)
- **Was:** `book.css:156` `.dd .dd-art { … background: var(--white) }` outranked `.on-brand`, `.on-accent` and `.on-dark`. As a result the "Wel, negatief logo" tile (`index.html:252`) showed white on white, and both "Niet" tiles (`:256-257`) showed a correct logo on white. See `qa1-achtergronden-tegels.png`.
- **Now:** in the 12:49 `book.css` the background is removed from `.dd .dd-art`. No action needed. Re-check visually at the final pass.

### P1.2 Forbidden price promise "zonder verrassingen achteraf" is still printed
copy.md (the "Feiten" table, algemene voorwaarden artikel 5) allows extra work to be charged, so it says never to write "zonder verrassingen achteraf". "Een heldere offerte vooraf" is allowed.
- `index.html:101` "Geen verrassingen achteraf, wel een verhuizing die gewoon goed geregeld is." → per copy.md §1: **"Geen gedoe, wel een verhuizing die gewoon goed geregeld is."**
- `index.html:148` (Bedrijven) "Een heldere offerte vooraf, zonder verrassingen achteraf." → per copy.md §6: **"Een heldere offerte vooraf."**
- `index.html:525` (Beloftes table, Prijs row) currently tells writers to use "zonder verrassingen". Change the middle cell to: **"een heldere offerte vooraf", nooit "zonder verrassingen achteraf" en geen vaste eindprijs**. The "Waarom" cell stays.

### P1.3 Business audience is broader than the terms allow
- **Where:** `index.html:146` "Ondernemers en organisaties die hun kantoor of bedrijfsruimte verhuizen."
- **Problem:** copy.md §6 narrowed this to small businesses, because the algemene voorwaarden only cover "klein zakelijk".
- **Fix:** **"Kantoren en kleine bedrijven die verhuizen."** Leave out copy.md's `[TE BEVESTIGEN]` note.

### P1.4 Letterhead mockup prints made-up company data
This is not placed in the book yet, but the SVG has been generated and chapter 07 will pick it up.
- **Where:** `assets/mockups/briefpapier.svg`, from `assets/mockups/_bron/build_mockups.py:517`. See `qa1-mockup-briefpapier-voet.png`.
- **Footer** shows "KvK 00000000", "IBAN NL00 BANK 0000 0000 00" and "BTW NL000000000B00". copy.md open point 2 says no KvK, BTW or legal form is known, and the brief says: no KvK. Zero-filled numbers read as real data once printed.
- **Letter body** (`build_mockups.py:479-482`):
  - "met onze eigen verhuiswagen": owning vans or a lift is unconfirmed (copy.md open point 6).
  - "Zoals besproken tijdens de bezichtiging": a site visit is not part of the published five-step process (persoonlijk contact, not a visit).
- **Fix (dereus-f0, or the builder):**
  - Replace the third footer column with confirmed facts, e.g. "Ma t/m za 08.00 tot 20.00 uur" / "Zo 09.00 tot 17.00 uur" / "4,9 uit 5 op Google", or drop the column.
  - Letter: "Zoals besproken in ons telefoongesprek…" and "…het transport naar uw nieuwe adres."
  - Check `visitekaartje*.svg` and `e-mailhandtekening.svg` for the same pattern. Their text is outlined, so grep can't see it; they need a visual check.

---

## P2: should fix

### P2.1 Print pagination (49 A4 pages)
See `qa1-print-a4-p01-30.png` and `qa1-print-a4-p31-49.png`.
- **Cover split across two pages:** p.1 has the logo, title and facts; p.2 holds only the cover visual. At print width the 900 px media query stacks the cover into one column.
- **Near-empty page:** p.8 carries a single bullet ("Snelle en flexibele planning, ook bij spoed.").
- **H3 headings stranded at the bottom of a page, cut off from their content:** p.12 Achtergronden, p.20 Contrast, p.23 Gewichten, p.29 Wij zeggen u, p.32 Zo schrijven we, p.33 Standaardteksten, p.38 De mascotte, p.39 Wel en niet, p.43 Digitaal, p.46 Knoppen op de website.
- **Fix:** add to the print block (`book.css:393-403`):
  ```css
  .chapter-head, .chapter h3, .chapter h4 { break-after: avoid; }
  .bb-cover { grid-template-columns: 1fr 1fr; gap: 10mm; break-after: page; }
  .audience, .values .panel, .traits > div, .principles li { break-inside: avoid; }
  p, li { orphans: 3; widows: 3; }
  ```
  Re-print afterwards to confirm; I can run the PDF check again on request.
- **Same topic, wrong claim:** `index.html:52` ("geeft één hoofdstuk per pagina") and `index.html:804` ("één hoofdstuk per A4") are not true, because chapters run to 3 to 8 pages. Replace both with **"Elk hoofdstuk begint op een nieuwe pagina."**

### P2.2 Console errors when the book is opened from disk
- **Where:** `index.html:9-10`, `<link rel="preload" … as="font" crossorigin>` for Inter and Archivo.
- **Effect:** under `file://` the CORS-mode preload fails (origin null). Each load logs 4 errors and 2 "preload not used" warnings. The fonts still render, because `@font-face` loads them separately, so this is only noise.
- **Fix:** remove both preload lines. The book is used from a folder, where preloading gains nothing.

### P2.3 The table-of-contents logo breaks the book's own minimum size
- **Where:** `index.html:41` uses `dereus-logo.svg` (with tagline) at 120 px (`book.css:55`).
- **Problem:** the logo chapter sets a 160 px minimum for the version with tagline. At 120 px the tagline is about 6 px tall.
- **Fix:** `src="assets/logo/dereus-logo-zonder-tagline.svg" width="1000" height="885"`.

### P2.4 Heading order skips a level
- **Where:** `index.html:90` and `:92`, where `<h4>Missie</h4>` and `<h4>Visie</h4>` come straight after the chapter `<h2>`, with no h3 in between.
- **Fix:** make them `<h3>` and keep the look with a class (e.g. `<h3 class="as-h4">` plus `.chapter h3.as-h4 { font: inherit of h4 }`), or add an `<h3>Missie en visie</h3>` above the panel.

### P2.5 Story paragraph lags behind copy.md §1
- **Where:** `index.html:99` "Daar staat onze naam voor."
- **Fix:** use copy.md's wording **"Daar is De Reus voor."** and add copy.md's closing sentence **"Voor een reus is geen verhuizing te groot."**, which ties the story to the new tagline. (Line 101 is covered by P1.2.)

### P2.6 "Pantone n.t.b." on the Mist swatch
- **Where:** `tokens.css:87` `--off-white-pantone: "";`. book.js renders an empty value as "n.t.b.", which reads as "still to be decided".
- **Problem:** "no Pantone" is a deliberate choice (color-type-system.md: screen only).
- **Fix:** `--off-white-pantone: "geen, alleen scherm";`. Optionally add `--white-pantone: "papierwit";` so the Wit card has a Pantone row too.

### P2.7 En dashes in delivered logo files
- **`assets/logo/README.md`:** 10 en dashes, in the title on line 1 and in the coordinate ranges on lines 27-34. Fix: title "Logo · Verhuisbedrijf De Reus"; ranges "0 tot 389".
- **The `<title>` of all 7 logo SVGs**, e.g. "Verhuisbedrijf De Reus [en dash] Geen verhuizing te groot!". Screen readers read this title and browsers show it as a tooltip. Fix: "Verhuisbedrijf De Reus: Geen verhuizing te groot!" and "Verhuisbedrijf De Reus, beeldmerk".
- **Not findings:** " - " in `book.js:80` and in `build_mockups.py` is arithmetic. The OFL licence texts must not be edited. The hits in `content/imagery.md` are markdown list markers. `index.html`, `book.css`, `tokens.css` and `content/*.md` have zero em or en dashes.

### P2.8 Letterhead shows two slogans on one sheet
- **Where:** `briefpapier.svg` puts the logo with tagline at the top and the pay-off band "Sterk in verhuizen. Zorgeloos geregeld." at the bottom.
- **Problem:** copy.md §5 says "Eén slogan per blok" and never to put the pay-off with the tagline logo. The script's own comment (`build_mockups.py:72`) says the pay-off only goes where the logo is used without tagline.
- **Fix:** use `dereus-logo-zonder-tagline` on the letterhead, or drop the pay-off band.

---

## P3: nice to have

1. **Orphaned grid items:**
   - Cover facts wrap 3 + 1 at 1440 px (`book.css:86`). Use `grid-template-columns: repeat(2, 1fr)` in the cover, or 4 across on wide screens.
   - The same happens with Persoonlijkheid (4 + 1) and Doelgroepen (4 + 1, `.cols-3`). A fixed `repeat(3, 1fr)` above 1100 px gives 3 + 2, which is how Brocken does it.
2. **Anatomy markers 3 and 4** (`index.html:186-187`, left 3 % and 2.5 %) sit on top of the first letters "V" and "G". Move them just outside the artwork (`left: -4%`).
3. **The book breaks its own 14 px minimum** in several labels: `book.css:40` (11 px), `:211` (12), `:215` (13), `:221` (13), `:222` (12), `:277` (11), `:306` (12). Raise them to `var(--text-xs)` (14 px) where the layout allows, and to at least 12 px elsewhere.
4. **Exclamation-mark rule:** `index.html:485` ("Hooguit één uitroepteken per pagina, liefst geen") should note the exception from copy.md §5. Add: **"De tagline Geen verhuizing te groot! is de enige uitzondering."**
5. **Quote marks:** `<q>` renders as ‘…’ (the browser default for `nl`), while the rest of the book uses “…” (`index.html:474-476`). Fix: `.rhythm q { quotes: "“" "”"; }` (`book.css:311`).
6. **Spelling:** "all-in prijs" should be **"all-inprijs"** (Woordenlijst). This is in `index.html:525` and also in copy.md.
7. **Version labels disagree:** the topbar says "werkversie" (`index.html:34`) while the Versies table and tokens.css say 1.0. Settle this at the final pass.
8. **Button demos:** the "Hover" and "Focus" demo buttons are live links to `#toepassingen` (`index.html:752-753`); make them `<span>` elements. There is also no skip link past the TOC. Add `<a class="skip" href="#top">Naar de inhoud</a>`, visible on focus.
9. **Swatch chips** print both "met wit" and "met inkt" labels even where one is unreadable by design (white on Mist or Wit). Either show only the passing pair, or add the pass/fail pill used in the contrast table.
10. **Heavy mascot file:** `assets/imagery/mascotte-de-reus.png` is 2.3 MB. For the book, export about 1200 px wide (WebP or optimised PNG, around 200 KB).
11. **Own wording fix:** my `research/color-type-system.md` uses "zinsnaamval" for sentence case, which is a calque ("naamval" means grammatical case). It isn't in the book at the moment. If it gets copied, write instead: "Koppen schrijven we als een gewone zin: alleen het eerste woord en namen met een hoofdletter." I can correct my file if the coordinator agrees.

---

## Checked and correct

- **tokens.css matches color-type-system.md exactly:**
  - Brand colours, with CMYK and Pantone as quoted text tokens.
  - `--grey-400: #838996`.
  - CTA: `--color-cta` #FFCC33, `--color-cta-text` #0B2352, `--color-cta-hover` #F7B817.
  - Fonts: Archivo width 75 at 700 to 800, Inter at 400 to 800, self-hosted.
  - `--text-body: 1.125rem` (18 px), `--radius-button: 999px`, `--radius-card: 14px`.
- **Swatch cards:** all 12 show the right HEX, RGB, CMYK and Pantone.
- **Runtime contrast table:** all 11 rows match my own computed ratios (17,29 · 5,39 · 8,63 · 8,63 · 15,26 · 10,13 · 8,59 · 10,13 · 3,51 · 1,51 · 1,77).
- **Rendering:**
  - The browser really uses Archivo Condensed for the h1, h2, h3, statements and facts, and Inter for body text and buttons.
  - Body text is 18 px. The CTA renders #FFCC33 with #0B2352 text, a 999 px radius and 17 px type.
  - No horizontal overflow at 1440 px or 390 px.
  - 0 broken images, and every logo points to the final `dereus-logo*.svg` files.
- **Copy:**
  - No KvK number, founding year or keurmerk anywhere in the book.
  - "standaard verzekerd" is used throughout; "volledig verzekerd" appears only inside the rule that forbids it.
  - u/uw is used throughout. "je/jij" appears only where the book explains that reviews are quoted as written.
  - No `[TE BEVESTIGEN]` marker is printed.
  - None of the live site's typos (Inbdoel, Hnadymanservice, Verhuislitservice, nfo@) appear. The mailto links go to info@.
  - The boilerplates match copy.md word for word.
- **Accessibility:**
  - `lang="nl"`.
  - Every content image has an alt text. Do/don't tiles use `alt=""` with a caption, which is correct.
  - The ratio bar has `role="img"` with an up-to-date label.
  - `:focus-visible` shows a 3 px ring, turning white on blue rows.
  - Icons are `aria-hidden`.

## Fixed during the review (12:37 to 12:45), no action needed

- CTA buttons were transparent, because `book.css` still used the removed `--color-action*` tokens.
- `.statement mark` rendered #F7B817 text on white (1,78:1).
- H3 was set in Inter.
- 20 logo images and the favicon returned 404 after the temporary PNGs were removed.
- The type-scale labels were stale (36 to 52, 17 px, 15 px).
- The clear-space ratio was 0.14 and is now 0.117.
- Diepblauw and Staalgrijs swatches were missing, and the neutral names are now aligned.

## Compared with the Brocken brand book

| | Brocken | De Reus (12:45) |
|---|---|---|
| Chapters | 13 | 8 |
| Words in index.html | 11 500 | 5 900 |
| Print pages (A4) | 75 | 49 |
| Images, broken | 69, 0 | logo set complete, 0 |
| Console errors | 0 | 4 errors + 2 warnings (P2.2) |

- **Lighter, as the user asked.** Ours has half the text and two thirds of the pages, with the same frame: sticky TOC, cover facts, swatch cards, live contrast table, do/don't tiles, specimen blocks and reference buttons.
- **Where Brocken is still ahead on polish:**
  - A real cover photograph (ours is waiting on dereus-f0).
  - Real photography with a caption on every image (waiting on dereus-e7 and the client).
  - Tidy grids without single leftover cards (P3.1).
  - Clean print output (P2.1).
- **Conclusion:** with P1 and P2 fixed and the mockups in place, the book will match Brocken's quality at the lighter scope.
