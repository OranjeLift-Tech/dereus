# QA report 3: brand book De Reus (pass 3, final)

- **Reviewer:** dereus-6e (read only).
- **Files written:** this report, the `qa3-*.png` evidence in this folder, and `brandbook/Merkboek-De-Reus-v1.0.pdf` as requested. No git commands were run.
- **Reviewed state:** the files had been stable since 13:33:55; I started at 13:36.
  - `index.html` 13:30:13 (894 lines), `book.css` 13:23:23 (472 lines), `tokens.css` and `book.js` 12:54.
  - Mockups 13:23, logo files and `druk/` 13:12 to 13:14.
  - Re-checked at 13:47: byte-identical to my snapshot.
- **Method:**
  - Headless Edge over the DevTools protocol at 1440, 768 and 390 px, collecting screenshots, console and network logs, image loading and distortion, heading outline, element positions and all visible text.
  - An A4 print PDF analysed page by page.
  - A full proofread of the visible text (about 5,100 words including interface labels).
  - HTML tag balance, duplicate-sentence and punctuation scans.
  - The generated mockup text list in `assets/mockups/README.md` checked against the book captions.
  - Two CMYK PDFs opened and their colour operators read.
  - The Bestanden table checked against the files on disk.
  - A dash grep over every text file under `brandbook\` except `research\`.
- **Evidence:** `qa3-desktop-1440.png`, `qa3-tablet-768.png`, `qa3-mobiel-390.png`, `qa3-print-p1-p2-p23-p51.png`, `qa3-logo-tegels.png`, `qa3-toepassingen.png`, `qa3-cmyk-pdfs.png`.

---

## Verdict: NOT YET. Three one-line fixes, then SHIP

The book is finished in substance. Every QA-2 item is fixed, and the new pieces are correct: rear van, offerte, CMYK PDFs, appendix, back page and the rebuilt cover. The 116 scripted replacements left no broken markup and no stray fragments except the one listed below.

Three small defects remain. Two of them show in the client PDF, and one breaks a book rule. Each is a single-line change of about 5 minutes. Once they are applied, the book can ship without another full pass: I only need to check those three lines and re-export the PDF, which takes about 3 minutes. The rest are v1.1 notes.

**About the PDF saved now:** `brandbook/Merkboek-De-Reus-v1.0.pdf` has 50 pages and shows the current state. I exported it without the blank page 2 (see P2-1), using the print API's page range `1,3-51`. It still contains the two text errors (P2-2 and P2-3), so export it once more after the fixes.

---

## Open items

### P2-1 A blank page 2 when printing from the browser
- **Where:** `book.css:462` (print) `.bb-cover { … min-height: 265mm; … break-after: page; }`, together with the screen padding on `.bb-cover` (`book.css:78`, `padding: var(--space-9) 0 var(--space-9)`).
- **Cause:** A4 minus the 14 mm margins leaves 269 mm; 265 mm plus the padding overflows it. The cover spills onto page 2, which then stays empty before the forced break. See `qa3-print-p1-p2-p23-p51.png`.
- **Fix:** in the print block, `.bb-cover { min-height: 0; height: 262mm; padding: 0; }`. Alternatively, keep `min-height` but set `padding: 0`.
- **Status in the PDF:** the exported file skips the blank page. Anyone who prints the book themselves ("Afdrukken of opslaan als PDF") still gets it.

### P2-2 Social post spec contradicts the one-slogan rule and the mockup
- **Where:** `index.html:731`, "Specificaties: 1080 × 1080 px. **Logo met tagline** minimaal 160 px breed."
- **Problem:** the post carries a campaign line ("Het zware werk, met zorg gedaan."), and the mockup uses `dereus-logo-zonder-tagline-negatief` (README text list). With the tagline logo there would be two slogans on one surface, against "één slogan per blok" (chapter 05).
- **Fix:** "Specificaties: 1080 × 1080 px. Logo zonder tagline, minimaal 100 px breed; op blauw de negatieve versie."

### P2-3 Broken phrase from the scripted replacements
- **Where:** `index.html:573` (Beeldtaal › Fotografie › Stijl) reads "Echte medewerkers, bezig met het werk of ontspannen **in de camera**." The verb is missing.
- **Cause:** the source `content/imagery.md:80` has "kijken ontspannen in de camera"; `content/wijzigingen-v2.md:1394` dropped "kijken".
- **Fix:** "Echte medewerkers, bezig met het werk of ontspannen in de camera kijkend. Geen duim omhoog." Update `content/microcopy.md:235` to match.

---

## v1.1 notes (P3, no blocker)

1. **"Drukke foto" tiles use the box mockup, which already carries the logo.**
   - **Where:** `book.css:169` `.dd-art.busy { background: url(assets/mockups/verhuisdoos.svg) … }`, used at `index.html:258` (Wel), `:263` and `:274` (Niet).
   - **Problem:** the "Wel" example shows the logo on a white card over another logo. Use a background without a logo, such as a crop of the empty side of the box, a plain photo texture, or the Mist gradient.
2. **Print, p.23:** the "Typeschaal" H3 and its one-line intro (`index.html:409`) end the page; the specimen starts on p.24. Add `.chapter h3 + p { break-after: avoid; }` to the print block.
3. **Print, p.21:** only the last row of the "Overgang" table ("Grijzen …") lands on its own page. Add `table.transition { break-inside: avoid; }` to the print block (the table is short).
4. **Button state demos:** `index.html:855-856` show three yellow buttons in one row, labelled "Hover" and "Focus". Colour rule 3 says "Geel als knopkleur is er alleen voor de hoofdactie “Offerte aanvragen”. Hooguit één gele knop per blok." Label them "Offerte aanvragen" with a small "hover" and "focus" caption underneath, or put them in a separate row titled "Toestanden van één knop".
5. **Mockup README captions are out of date:** the business card, letterhead and website header captions in `assets/mockups/README.md` ("Bestanden en bijschriften") differ from the book, which is the newer version. The note "deze twee bijschriften staan nog niet in content/microcopy.md" is also stale. Regenerate the README table from the book or from microcopy.md.
6. **Horizontal logo:** "Voorstel … Graag uw akkoord" (`index.html` logo chapter, Bestanden, rear van). Remove the tags once the client approves.
7. **Optional:** there is no one-colour white print PDF in `druk/`. `LEESMIJ.md` correctly explains how signmakers substitute white. Add `dereus-logo-1kleur-wit.pdf` only if a textile printer asks for it.
8. **PDF text layer:** some Archivo headings come out without word spaces when you copy or search in the PDF (for example "zo zeggenwe het"). The visual output is correct. This comes from how Chrome writes the text layer for tightly set text, and it doesn't affect print.

---

## QA-2 status

| Item | Status | Evidence |
|---|---|---|
| P1-1 misuse demo equal to the horizontal logo | Fixed | `index.html:273`: wordmark stacked above the beeldmerk (`column-reverse`), clearly different from the horizontal logo; caption points to the horizontal logo |
| P2-1 icon captions breaking mid-word | Fixed | `book.css:387` `overflow-wrap: normal; hyphens: manual`, 6 × `&shy;`. Renders "Woning-/ontruiming" at 1440 and 768 px, one line at 390 px |
| P2-2 koningsblauw box logo | Fixed | Official variant `dereus-logo-1kleur-blauw` (SVG, PNG, CMYK PDF), Bestanden row, rule text "of koningsblauw op karton" |
| P2-3 negative logo without tagline | Fixed | File present (SVG, PNG 2048 px, PDF), Bestanden row, used by the social post and the back page |
| P2-4 "onze wagens en de verhuislift" | Fixed | "onze verhuizers aan het werk, bij echte klanten" |
| P2-5 boilerplates "bedrijven" | Fixed | All three say "kleine bedrijven … van en naar het buitenland" |
| P2-6 "inclusief montage" | Fixed | "ook montage is mogelijk" |
| P2-7 "Losse diensten" card | Fixed | Card removed; spoed folded into Particulieren ("Spoedklussen pakken we ook op.") |
| P2-8 shot list stranded in print | Fixed | `.shotlist { break-inside: avoid }`; the whole list is on p.33 |
| P3-1 cover in print | Changed | The cover looks good on p.1 but causes the blank p.2, see P2-1 |
| P3-2 stock photo in a Wel tile | Changed | Replaced by the box mockup, see v1.1 note 1 |
| P3-3 labels below 14 px | Fixed | 0 `font-size` declarations below 14 px left |
| P3-4 short form of the hours | Fixed | "kort ma t/m za 08.00 tot 20.00 uur" in the writing rules |
| P3-5 "brand book" | Fixed | No longer in the text |
| P3-6 icon wording in the colour rules | Fixed | "Geel nooit als tekst of als heel icoon op wit; een geel accent binnen een blauw icoon mag." |
| P3-7 tagline highlight wrap | Fixed | `te&nbsp;groot!` |
| P3-8 "Voorstel belettering" | Fixed | On the cover, the van side and the van rear |
| P3-9 "ter goedkeuring" | Open by design | Now phrased "Voorstel, afgeleid van logo 02. Graag uw akkoord." |

## Regression check after the 116 replacements

- **Markup:** tags are balanced (parser check). The only empty elements are the ones book.js fills in (swatch chips, contrast cells, colour dots) and the hidden draft bar.
- **Text:**
  - No leftovers: VOLGT, TE BEVESTIGEN, brand book, pay-off, `{x}`, "n.t.b." all absent.
  - Punctuation is intact; the only "space before punctuation" hits are the intended ratio notation "4 : 3".
  - Four sentences occur twice, all on purpose: a type specimen, a rule restated in the appendix, a shared boilerplate sentence, and the van side and rear specs.
- **Structure:**
  - Every heading has content.
  - Doelgroepen is a clean 2 × 2 (1 column on mobile). "Wat niet mag" ends with a wide tile; nothing is orphaned.
  - No empty cards or grids.
- **Proofread:** the whole visible text is correct Dutch and uses u/uw throughout. There are no clichés or superlatives, and the numbers follow the rules (4,9 uit 5; 08.00 tot 20.00). The one exception is P2-3.

## Internal consistency

- **Logo variants vs misuse tiles:** consistent. The horizontal logo is approved as a proposal, and the misuse tile now shows a different, wrong layout. "Andere kleuren" (cyan and red) does not clash with the official koningsblauw one-colour logo.
- **One-colour rule vs the box:** consistent. The rule text, Bestanden, the CMYK PDF and the box mockup all use koningsblauw on karton.
- **Slogan rule vs every surface:**
  - Van side, box, workwear and business card front: logo with tagline, no second slogan.
  - Rear van: horizontal logo, no tagline.
  - Letterhead, offerte and e-mail: logo without tagline plus the afsluiter.
  - Envelope: logo without tagline only.
  - Website header: logo without tagline; the tagline appears only on the van illustration.
  - Back page: negative logo without tagline plus the afsluiter.
  - Social post: campaign line A with the logo without tagline. Only its spec text is wrong (P2-2).
- **Yellow rules vs icons and buttons:**
  - Icons are blue with one gold accent, as rule 1 now allows.
  - Every yellow button in the mockups is "Offerte aanvragen": website header (one in the nav, one in the hero, which are separate blocks), social post, and the button demos on blue.
  - Only the state demos break the rule's wording (v1.1 note 4).
- **Captions vs `assets/mockups/README.md`:** 9 of 12 match word for word. The business card, letterhead and website header captions in the README are older (v1.1 note 5).

## New pieces

- **CMYK PDFs** (`assets/logo/druk/`):
  - I opened `dereus-logo.pdf`, `dereus-logo-1kleur-blauw.pdf` and `dereus-logo-negatief.pdf`. All three are pure vector (6 path objects, no images), DeviceCMYK only, with no RGB, gray or spot colours.
  - Colours are exact: koningsblauw `0.97 0.77 0 0`, goudgeel `0 0.2 0.85 0`, and the white of the negative `0 0 0 0` (documented).
  - Sizes: 100 × 99 mm (100 × 88,5 mm without tagline). The renders are correct (`qa3-cmyk-pdfs.png`).
  - Missing ICC profile or output intent: documented in `LEESMIJ.md`, and correct for placeable logos.
- **Rear van:** horizontal logo plus phone number on the doors, marked as a proposal and awaiting approval. Correct.
- **Offerte:** logo without tagline, all amounts "€ 0,00" (no invented prices), "Deze offerte is vrijblijvend.", a signature block, and the same footer and afsluiter as the letterhead. Correct.
- **Back page:** negative logo without tagline, the afsluiter in goudgeel on koningsblauw (5,73 : 1, AA), and the contact line. Printed as the last page on its own sheet.
- **Appendix 09:** the file table, the type scale (all 12 tokens match `tokens.css`) and the contrast table (11 rows, values match my computed ratios). The button demo notes match the rules.
- **Bestanden table vs `assets/logo/`:**
  - Every listed file exists: 11 SVG and PNG variants, the favicon set (.ico, SVG, 16/32/48/180/512 px), the favicon with arms (180 and 512 px), and 9 PDFs in `druk/`.
  - The archive files are listed as archive.
  - Not listed, by design: `README.md`, `druk/LEESMIJ.md`, `druk/_bron/`.
  - Every logo PNG really is 2048 px wide with transparency.
- **Cover:** rebuilt with a large truck labelled "Voorstel belettering", 2 × 2 facts and no sidebar clutter.

## Rendering, facts, dashes

- **Rendering:** 1440, 768 and 390 px all have 0 console messages, 0 broken images (74 images, all with alt text), no horizontal overflow and no image distortion. The draft bar is gone.
- **Facts** are identical in the book and all mockups:
  - Phone 085 000 5647 (tel:+31850005647).
  - E-mail info@verhuisbedrijfdereus.nl.
  - Address Lau Mazirellaan 336, 2525 ZJ Den Haag.
  - Hours 08.00 tot 20.00 / 09.00 tot 17.00, with dots.
  - Score "4,9 uit 5".
- **Nothing unconfirmed is claimed as fact.** KvK and btw appear only in "vullen we aan zodra ze bekend zijn".
- **Dashes:** 0 em or en dashes in all 53 text files under `brandbook\` except `research\`.
- **Print:** 51 pages from the browser (50 in the exported PDF). The cover is on p.1, every chapter starts on a new page, the mockups print in chapter 07, and the back page is last. Apart from P2-1 and v1.1 notes 2 and 3, no page ends on a stranded heading.

---

## Verification after the fixes: SHIP

- **Reviewed state:** stable from 13:50:21; checked at 13:53 to 13:55. Snapshot byte-identical at export time. `assets/logo-v2/` was ignored, as agreed; v1.0 ships with logo 02.

| Item | Result |
|---|---|
| P2-1 blank page 2 | Fixed. Print cover `min-height: 0; height: 262mm; padding: 0; overflow: hidden`. The browser print has 50 pages and none is empty. The cover is complete on p.1 (logo, title, subtitle, 2 × 2 facts, truck with "Voorstel belettering"); nothing is clipped. |
| P2-2 social spec | Fixed: "Logo zonder tagline, minimaal 100 px breed; op blauw de negatieve versie." |
| P2-3 broken phrase | Fixed: "…ontspannen in de camera kijkend. Geen duim omhoog." ("Geen duim omhoog" appears once). Mirrored in `content/microcopy.md:235`. |
| Note 1 busy tiles | Fixed. A blurred photo-like gradient replaces the box mockup, so there's no logo over a logo. |
| Note 2 Typeschaal | Fixed. `.chapter h3 + p { break-after: avoid }`; "Typeschaal" starts p.23 together with its specimen. |
| Note 3 Overgang table | Fixed. `table.transition { break-inside: avoid }`; the whole table is on p.20. |
| Note 4 button states | Fixed. A separate "Toestanden van dezelfde gele knop" box (Normaal, Hover, Focus, all "Offerte aanvragen"); the "Op licht" row has one yellow button. |
| Mockup README captions | All 11 match the book word for word. |
| Regression scan | 1440, 768 and 390 px: 0 console messages, 0 broken images (74, all with alt text), no page overflow, 0 em or en dashes in the render and in every text file outside `research/` and `logo-v2/`. |

- **Final PDF:** `brandbook/Merkboek-De-Reus-v1.0.pdf`, **50 pages**, exported from the browser print without a page range at 13:55.
- **Remaining v1.1 notes:**
  - p.22 carries only the last row of the "Gewichten" cards (a page about 16 % full). Cosmetic.
  - Earlier notes 5 to 8 (captions now fixed; horizontal logo awaiting approval; optional white print PDF; PDF text-layer spacing).
