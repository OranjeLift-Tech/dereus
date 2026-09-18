# QA report 2: brand book De Reus (final pass)

- **Reviewer:** dereus-6e (read only; the only files written are this report, the `qa2-*.png` evidence, and `brandbook/Merkboek-De-Reus-v1.0.pdf` as requested)
- **Reviewed state:**
  - `index.html` 12:56:25, `book.css`, `book.js` and `tokens.css` 12:54:11, all mockups and `assets/logo/README.md` about 12:54.
  - Rendered at 12:59. Re-checked at 13:08: only `OPEN-VRAGEN.md` had changed since, and it is not part of the rendered book.
  - Line numbers refer to that `index.html` (888 lines) and `book.css` (426 lines).
- **Method:**
  - Headless Edge over the DevTools protocol at 1440, 768 and 390 px: full-page screenshots, console and network logs, the fonts actually used, image loading and distortion, tile backgrounds, heading outline, and all visible text.
  - A4 `printToPDF` (53 pages), rendered page by page, with fill and last-line analysis for stranded headings.
  - Mockup texts checked against the generated list in `assets/mockups/README.md` ("Alle teksten per mockup"), plus every PNG in `assets/mockups/preview/`.
  - Facts extracted from the rendered text and the mockup texts. Dashes grepped across `brandbook\` except `research\`.
- **Evidence** in this folder:
  - `qa2-desktop-1440.png`, `qa2-tablet-768.png`, `qa2-mobiel-390.png`
  - `qa2-print-p01-30.png`, `qa2-print-p31-53.png`
  - `qa2-horizontaal-vs-misbruik.png`, `qa2-iconen-afbreking.png`
  - `qa2-tablet-mobiel-logo-mockups.png`
- **PDF:** `brandbook/Merkboek-De-Reus-v1.0.pdf` (53 pages, A4, title "Verhuisbedrijf De Reus · Merkboek", no browser header or footer). **It shows the 12:56 state, so it must be exported again after the fixes below.** One run of the same script does it.

---

## Verdict: NOT YET. Ship after 1 P1 and 8 P2 fixes

The book is in good shape.
- **Everything from report 1 that affects the client is fixed.**
- **Rendering is clean at every width:** 0 console errors, 0 broken images, no overflow, and no em or en dashes anywhere.
- **Facts are identical** everywhere.
- **Print** keeps the cover on one page and no longer strands H3 headings.
- **The mockups** are strong and follow the one-slogan rule.

What is left is one contradiction in the logo rules (P1), one layout glitch, three places where the book states more than the company has confirmed, two logo-file gaps and one print break (P2). All of it is text or CSS; nothing needs a redesign. My estimate is under an hour of work, then re-export the PDF.

---

## Status of report 1

| Item | Status | Evidence |
|---|---|---|
| P1.1 do/don't tiles on white | Fixed | Tile backgrounds render as Diepblauw, Koningsblauw and Goudgeel (computed style) |
| P1.2 "zonder verrassingen achteraf" | Fixed | The phrase now appears only inside the rule that forbids it; `:101` "Geen gedoe, wel…" |
| P1.3 Bedrijven scope | Fixed | "Kantoren en kleine bedrijven die verhuizen." |
| P1.4 mockup dummy data | Fixed | No KvK, IBAN or BTW in the mockup texts; the letter says "in ons telefoongesprek" and "het transport naar uw nieuwe adres"; checked visually in the previews |
| P2.1 print pagination | Fixed | `break-after: avoid` on headings, cover `break-after: page`, orphans and widows set; no H3 is the last line of any page. One new case: see P2-8 |
| P2.2 preload console errors | Fixed | Preload lines removed; 0 console messages at all three widths |
| P2.3 TOC logo with tagline | Fixed | `dereus-logo-zonder-tagline.svg` |
| P2.4 heading order | Fixed | Missie and Visie are now H3 |
| P2.5 story vs copy.md | Fixed | "Daar is De Reus voor. … Voor een reus is geen verhuizing te groot." |
| P2.6 "Pantone n.t.b." | Fixed | "geen, alleen scherm"; Wit shows "papierwit" |
| P2.7 dashes in logo files | Fixed | README and all 11 SVG `<title>` elements are dash-free |
| P2.8 two slogans on letterhead | Fixed | Letterhead uses the logo without tagline, plus the pay-off |
| P3.1 orphaned grid items | Fixed | Cover facts 2 × 2, Persoonlijkheid 5 across, Doelgroepen 3 + 2 |
| P3.2 anatomy markers on the letters | Fixed | Markers 3 and 4 at `left:-4%` |
| P3.3 labels below 14 px | **Open** (P3) | See P3-3 |
| P3.4 exclamation-mark exception | Fixed | "De tagline in het logo is de enige vaste uitzondering." |
| P3.5 `<q>` quote marks | Fixed | `quotes: "\201C" "\201D"` |
| P3.6 all-inprijs | Fixed | |
| P3.7 version labels | Fixed | 1.0 everywhere |
| P3.8 demo links, skip link | Fixed | Demos are `<span>` elements; a skip link was added |
| P3.9 unreadable swatch labels | Fixed | Only pairs of at least 3 : 1 are shown |
| P3.10 heavy mascot file | Fixed | The book uses `assets/boek/mascotte-de-reus-480.webp` (60 KB) |
| P3.11 "zinsnaamval" | Fixed in the book; still in my own `research/color-type-system.md` (not published) | |

---

## P1: must fix

### P1-1 The "Niet" demo for moving parts shows the approved horizontal logo
- **Where:** `index.html:282`, the misuse tile "Onderdelen verplaatsen". It builds beeldmerk left and wordmark right, which is visually the same as the approved variant "Horizontaal" (`index.html:225-230`, `dereus-logo-horizontaal.svg`). See `qa2-horizontaal-vs-misbruik.png`.
- **Why P1:** the logo chapter now gives two opposite instructions for the same composition. A printer or signwriter cannot tell whether the horizontal logo is allowed. It also undermines the "ter goedkeuring" status of the horizontal variant.
- **Fix:** replace the demo with a rearrangement that is clearly wrong and not an approved variant. For example, the wordmark above the beeldmerk, or the house lifted out from between the arms:
  ```html
  <div style="display:flex;flex-direction:column-reverse;align-items:center;gap:4px">…beeldmerk…wordmark…</div>
  ```
  Extend the caption: "…niet verplaatsen, weglaten of los schalen. **Voor een brede plek is er het horizontale logo.**"

---

## P2: should fix before the client sees it

### P2-1 Icon captions break mid-word
- **Where:** `book.css:364` `.icon-grid figcaption { … overflow-wrap: anywhere; }`, with the captions at `index.html:677-684` and `:687-694`. See `qa2-iconen-afbreking.png`.
- **Effect:** at 1440 and 768 px, "Woningontruimi|ng", "Handymanservi|ce" and "Verhuisliftservi|ce" split in both rows. At 390 px they fit. This is the most visible glitch in the book, and the research session's client read found it too.
- **Fix:** `overflow-wrap: normal; hyphens: manual;` in `book.css:364`, plus soft hyphens in the six long labels: `Woning&shy;ontruiming`, `Handyman&shy;service`, `Verhuislift&shy;service` (also `Internationale` and `Particuliere` stay intact this way).

### P2-2 Moving box uses a logo colour the rules do not allow
- **Where:**
  - `assets/mockups/verhuisdoos.svg` (README: "dereus-logo-1kleur in koningsblauw"). The alt text at `index.html:752` says "logo in koningsblauw".
  - The rules allow one-colour only in black or white (`index.html:211`, and the Bestanden rows `:296-297`), and "Andere kleuren" is a listed misuse (`:279`).
- **Fix (recommended):** make it an official variant, because a koningsblauw one-colour logo is the right choice for kraft cardboard and flexo printing.
  - Add `dereus-logo-1kleur-blauw.svg/png` to `assets/logo/`.
  - Add a row to Bestanden: "Eén kleur, koningsblauw | Karton, flexodruk, één drukgang in blauw".
  - Extend `:211`: "…of in koningsblauw op karton."
- **Fix (alternative):** regenerate the box with the black one-colour logo.

### P2-3 Social post uses a logo variant that is not delivered
- **Where:** `assets/mockups/social-post.svg`. README: "dereus-logo-zonder-tagline, negatief (blauw wordt wit)". The script recolours the logo on the fly, so no such file exists in `assets/logo/`, and the Bestanden table (`index.html:291-304`) doesn't list it. The website footer on blue will need the same file.
- **Fix:** export `dereus-logo-zonder-tagline-negatief.svg/png` to `assets/logo/`. Add it to the Bestanden table ("Zonder tagline, negatief | Kleine formaten op blauw: social, footer") and to the logo README.

### P2-4 Imagery principle states owned vans and a lift as fact
- **Where:** `index.html:614` "We laten onze eigen mensen zien: onze verhuizers, **onze wagens en de verhuislift** aan het werk." Owning vans and a lift is unconfirmed (copy.md open point 6; `OPEN-VRAGEN.md`). The source is `content/imagery.md`.
- **Fix:** "We laten onze eigen mensen zien: onze verhuizers aan het werk, bij echte klanten. Geen stockfoto's, geen modellen. …". The shot list already carries the right caveat ("Fotografeer alleen wat echt van De Reus is…"); keep that. Apply the same edit to `content/imagery.md`.

### P2-5 Boilerplates promise "bedrijven" without the small-business limit
- **Where:** `index.html:599`, `:600` and `:601` "verhuist particulieren en bedrijven". This is verbatim from copy.md lines 260, 264 and 268. It conflicts with the book's own "Wie we zijn" (`:100`, "particulieren en kleine bedrijven") and the Bedrijven card (`:146`), which follow the algemene voorwaarden ("klein zakelijk").
- **Why P2:** boilerplates are the text third parties copy word for word.
- **Fix:** "verhuist particulieren en kleine bedrijven, binnen Nederland en van en naar het buitenland" in all three, and in copy.md.

### P2-6 "inclusief montage" overstates what is included
- **Where:** `index.html:114` (Kernwaarden, Sterk) and `:137` (Particulieren), verbatim from copy.md lines 37 and 205.
- **Problem:** the site says "Van inpakken tot uitpakken: alles is mogelijk", and montage is sold as the separate Handymanservice. "inclusief" reads as assembly being part of every quote.
- **Fix:** "Van inpakken tot uitpakken, ook montage is mogelijk." Apply it in copy.md too.

### P2-7 "Losse diensten" card claims standalone booking that is unconfirmed
- **Where:** `index.html:157-161`, "Mensen die maar een deel willen uitbesteden. Alleen een verhuislift, tijdelijke opslag, een handyman…" and "Heeft u maar één paar sterke handen nodig?".
- **Problem:** copy.md §6 marks exactly this `[TE BEVESTIGEN]` (open point 8: can the lift and storage be booked without a move?). The book removed the marker but kept the claim.
- **Fix:**
  - **Option 1:** rename the card "Spoed" and keep only what is confirmed: "7 dagen per week bereikbaar, spoedklussen zijn welkom" and "Snelle en flexibele planning".
  - **Option 2:** drop the card until the client confirms.

### P2-8 Print: shot-list title stranded at the foot of p.37
- **Where:** `index.html:621-622` (`.shotlist` with the title "Eigen fotografie volgt"). The title and the top edge of the box end page 37; the ten items start on page 38. The print block (`book.css` about `:420`) protects `.shotlist li` but not the box.
- **Fix:** add `.shotlist { break-inside: avoid; }` to the print block. The box fits on one A4 page. Also add `.shotlist .head { break-after: avoid; }` as a fallback.

---

## P3: nice to have

1. **Cover in print** (`book.css:419`, `.bb-cover { grid-template-columns: 1fr 1fr }`):
   - **Problem:** the cover fits on page 1, but the truck is small in the top right and the bottom third is empty. I suggested that two-column rule in report 1; a single column works better on A4.
   - **Fix:**
     ```css
     .bb-cover { grid-template-columns: 1fr; min-height: 265mm; align-content: space-between; }
     .bb-cover .cover-visual { margin-top: 8mm; }
     ```
     This puts the truck full width under the facts. On screen, the client read suggests dropping the inner grey frame (`book.css:380`) so the truck fills its card.
2. **Stock photo in a "Wel" tile:** `index.html:267` uses `foto-niet-generiek-stockbeeld.jpg` as the positive example "Over een foto". Chapter 06 says stock photos are not used, and the licence of this Wix stock image for a client PDF is unknown. Use a flat koningsblauw-to-diepblauw background or a mockup crop instead. Keep the stock photo only as the "Niet zo" example (`:721`), if its licence allows.
3. **Labels below the book's own 14 px minimum:** `book.css:40` (11 px), `:175` and `:179` (13 px), `:226`, `:237` (13 px), `:292` (12 px), `:321` (13 px), `:355`. Raise them to `var(--text-xs)` where the layout allows.
4. **Short form of the opening hours:** the book writes "Maandag tot en met zaterdag 08.00 tot 20.00 uur"; the mockups write "Ma t/m za 08.00 tot 20.00 uur". Both are fine, and the times are identical with dots everywhere. To make the short form official, add to the numbers rule (chapter 04 rule 5 or chapter 05 rule 8): "Kort: ma t/m za 08.00 tot 20.00 uur".
5. **English in a Dutch book:** `index.html:494` "de omslag van het brand book" should read "het merkboek" (from copy.md line 186).
6. **Colour rule vs the icon set:** `:357` and `:380` say "geen gele iconen op wit", while the service icons are blue with a gold accent on white. That isn't a real conflict, but a supplier may read it as one. Change `:357` to: "Geel nooit als tekst of als heel icoon op wit. Een geel accent binnen een blauw icoon mag." Change the `:380` usage cell to: "Nooit voor tekst of losse iconen."
7. **Tagline highlight:** at `index.html:80` the gold underline of "te groot!" breaks across two lines at 1440 px. Put a non-breaking space in "te&nbsp;groot!".
8. **Mockups read as proposals:** the cover truck (`:65`) and the chapter 07 van could be read as "your current van". Add "Voorstel belettering" to the captions.
9. **Horizontal logo "ter goedkeuring":** remove the tag at `:230` and `:298` once the client approves.

---

## Checked and correct

- **Logo chapter:**
  - **Variants:** primair, zonder tagline, negatief, één kleur (zwart and wit), beeldmerk (licht and negatief), favicon (16/32/48 and app icon) and horizontaal (licht and negatief). All load as the final SVG and PNG files and show on the correct backgrounds.
  - **Anatomy:** 4 markers, positioned from the README coordinates.
  - **Clear space:** 11,7 % (and 21,7 % of the height for the horizontal logo). The demo uses `--cs-x: 0.117`.
  - **Minimum sizes:** 160 px / 40 mm, 100 px / 25 mm, 28 px high, 32 px / 12 mm and 16 px, in both the table and the size demo.
  - **Misuse demos:** all render, apart from P1-1.
  - **Favicon links:** `.ico`, 32 px PNG and a 180 px apple-touch-icon, all present.
- **Chapter 05:**
  - **Tagline:** "Geen verhuizing te groot!" (in the logo, always with "!").
  - **Pay-off:** "Sterk in verhuizen. Zorgeloos geregeld." (footer, quotes, mails, never next to the tagline logo).
  - **Campaign lines:** A to D, with the advice to use A and B. All consistent with copy.md §5.
- **Chapter 06:**
  - **Icons:** 8 icons on light and on koningsblauw, plus the checkmark demo.
  - **Mascot:** shown alone in its own block, tagged "in afbouw", with the rule never to place it next to the new logo. In print it sits on p.42 with no logo on the page.
  - **Shot list:** carries the caveat to photograph only what really belongs to De Reus.
- **Chapter 07:**
  - **Mockups:** van, box, workwear, business card (front and back), letterhead, envelope, website header, e-mail signature, social post and avatar. All load with descriptive alt texts.
  - **Aspect ratios:** card 85 : 55, A4 210 : 297, envelope DL 220 : 110, social and avatar 1 : 1, all exact.
  - **White pieces:** visible on the Mist stage, with a shadow, at all widths.
  - **One slogan per surface:** van, card and workwear use the logo with tagline and no pay-off. Letterhead and e-mail use the logo without tagline plus the pay-off. The social post uses campaign line A with the logo without tagline. The website header shows the tagline only on the van illustration.
- **Mockup wording** (README list): no unconfirmed claims left. "Naam Achternaam" is a clear placeholder. "4,9 uit 5 op Google" is correct. Saturday 3 October 2026 is indeed a Saturday.
- **Chapter 08:**
  - **Bedrijfsgegevens:** match the site.
  - **Print note:** "Afdrukken of opslaan als PDF kan op A4. Elk hoofdstuk begint op een nieuwe pagina."
  - **Version table:** 1.0.
- **Facts across the book and the mockups:**
  - Phone is only "085 000 5647" (tel:+31850005647). E-mail is only info@verhuisbedrijfdereus.nl. The address is only "Lau Mazirellaan 336, 2525 ZJ Den Haag".
  - Times are only 08.00 tot 20.00 and 09.00 tot 17.00, with dots and "tot", never a colon.
  - The score is only "4,9 uit 5". No KvK, BTW, IBAN, founding year or keurmerk. "volledig verzekerd" and "zonder verrassingen achteraf" appear only inside the rules that forbid them.
- **Dashes:** 0 em or en dashes in every text file under `brandbook\` except `research\` (html, css, js, md, svg, json). " - " appears only in code and in the OFL licence texts.
- **Rendering:**
  - 0 console messages, 0 broken images, 0 horizontal overflow and no image distortion at 1440, 768 and 390 px.
  - The fonts actually rendered are Archivo Condensed and Inter.
  - tokens.css still matches color-type-system.md.
- **Print:** 53 A4 pages. The cover fits on one page, every chapter starts on a new page, the mockups print on pp.44 to 50, and no page ends on a heading, apart from P2-8.

## Relation to the client read

`research/qa/client-read.md` (research session, 13:08) reviews the book from the owner's and suppliers' side.
- **Same finding:** P2-1 (icon captions).
- **Findings I confirmed and rated:** P2-5 (boilerplates), P2-6 (montage), P2-7 (losse diensten), P3-1 (cover) and P3-5 to P3-8.
- **Not QA defects:** its supplier-spec, length and appendix suggestions are editorial choices, so I have not rated them.
- **Decision for the coordinator or user:** the client read suggests showing the mascot as "Uw keuze" (a. afscheid nemen, b. laten hertekenen) instead of "in afbouw". The brief for this pass treats "in afbouw" as intended. Both work; it is a positioning choice, not an error.
