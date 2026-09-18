# Client read: brand book De Reus

- **Reviewer:** the research session (read only; no brand book file was changed).
- **Reviewed state:** `index.html` of 18 September 2026 around 13:00, rendered with headless Chrome at 1440 × 900, as a full-length page (36,410 px) and per chapter. The Brocken book was rendered the same way for comparison.
- **Point of view:** the owner of Verhuisbedrijf De Reus reading his brand book for the first time, and the outside suppliers he will hand it to (printer, signwriter for the van, embroiderer, web developer).
- **Not repeated here:** tokens, contrast maths, print pagination, console errors, and the P1 items already in `qa-report-1.md` (price promise, business audience at `:146`, letterhead dummy data). Where a point touches one of those, it says so.
- **Evidence in this folder:**
  - `client-read-omslag.png`: cover at 1440 × 900
  - `client-read-icoonlabels.png`: broken icon captions
  - `client-read-papier-rij.png`: letterhead and envelope row

---

## Verdict

**This is a book the client can be shown.** It looks professional, modern and clearly his: blue and gold throughout, the new logo everywhere, and chapter 07 shows his brand on a van, boxes, polos and stationery. Those mockups are what will win him over.

It falls short in three ways:
1. **Supplier details:** it does not yet give a printer or signwriter everything they need.
2. **Unconfirmed facts:** a few sentences state things about his company that he has not confirmed.
3. **Length:** it is still long for a small moving company. It has 68% of Brocken's words (6,234 vs 9,212) and 76% of its page length. That is lighter, but not by as much as the user asked for.

The top 10 below fix most of this without redesigning anything.

---

## 1. First impression and comparison with Brocken

- **Cover:**
  - **What works:**
    - The logo, the big "MERKBOEK" in Archivo and four gold-edged fact cards: clean, confident and on-brand.
    - The facts are good ones (4,9 uit 5, 24 uur, 7 dagen, 1 vaste verhuisadviseur).
  - **Weakest element:**
    - The visual on the right is a small truck illustration inside two nested grey frames, with a lot of empty space above and below it.
    - Brocken puts a large team photo there. Next to that, ours reads as a placeholder, even though the truck itself is good.
  - **Clutter:** the sidebar on the first screen shows "Design tokens: tokens.css" and "Elk hoofdstuk begint op een nieuwe pagina.". Neither means anything to the owner.
- **Overall look:**
  - The components (chapter pills, cards, tables, do/don't tiles, mockup stages) are as polished as Brocken's. Lighter, not cheaper, holds for the design.
  - It is recognisably the same template as Brocken: same cover layout, same sidebar, same fact cards. The client will not see Brocken, so this is fine.
  - It gets more "template" where grids leave empty slots (see section 5).
- **Where it is not lighter than it should be:** chapters 01 (Merkverhaal, about 4,000 px) and 05 (Tone of voice, about 6,400 px). Chapter 05 alone is longer than Logo and Kleur together minus one screen.

## 2. Can suppliers work from this book alone?

| Supplier | What they get | What is missing |
|---|---|---|
| **Printer** (business cards, letterhead, envelopes) | Logo as SVG and PNG, HEX, RGB, CMYK (FOGRA39) and Pantone for all colours, font names, card and paper sizes | **Print-ready vector logos in CMYK and in Pantone (PDF or EPS).** The SVGs are RGB, so the printer has to convert. Bleed (3 mm), paper weight, and which side of the card is which. |
| **Signwriter** (van livery) | The van mockup and "groot logo, telefoonnummer en website" | Vinyl or RAL equivalents for koningsblauw and goudgeel. Logo size and position on the sides and back. Minimum height of the phone number. Which logo goes on the back (the horizontal one, according to ch02). Who approves the proof. |
| **Embroiderer** (workwear) | Polo mockup, the one-colour logo | Logo width on chest and back, the one- or two-colour decision, thread colours (Pantone is there, but no advice to use it) |
| **Web developer** | `tokens.css`, fonts, buttons, icon SVGs, favicon set, contrast | A link to the new `sitemap/` (page structure) so the header in the mockup matches the planned menu |
| **Everyone** | Company name, address, phone, e-mail | **Who approves.** Chapter 08 says "Vraag het ons eerst", but names no brand contact (open question 1.8). No KvK or BTW (1.1). No single download of all files (a zip). |

## 3. Length, repetition and jargon

- **Chapter 01 repeats itself.**
  - **Same sentences in two sections:** "Ons verhaal" (`:92-97`) and "Wie we zijn" (`:99-100`) share whole sentences word for word ("Ze pakken zorgvuldig in, dragen met beleid en zetten alles netjes neer", "één vaste verhuisadviseur, die met u meedenkt en uw verhuizing van begin tot eind regelt", "geen voorrijkosten … standaard verzekerd").
  - **Same five proof points in four places:** the cover cards, Kernwaarden "Zo merkt de klant het" (`:112-118`), Bewijspunten and every Doelgroepen card.
  - **Too many introductions:** Missie, Visie, Ons verhaal and Wie we zijn are four introductions to the same idea.
- **Chapter 05 has 13 subsections.**
  - "Ons ritme" (`:505`) repeats what the writing rules already show.
  - The campaign table (`:486`) offers four lines and then says only A and B work best.
  - Nine writing rules; 7, 8 and 9 (naam, leestekens, nalezen) fit in one.
- **Developer and designer terms in the main text** the owner will stumble over:
  - "Design tokens", `tokens.css`
  - WCAG 2.2 niveau AA, "18,66 px vet", "focusringen" (`:365-367`)
  - `--text-h5`, "Rootgrootte", H1 to H6 (`:431` and on)
  - hover, focus, "c-* classes", woff2, apple-touch-icon, manifest
  - "Coated FOGRA39", `--radius-card`, Lucide
  - the English words "Tone of voice", "pay-off" and "brand book" (`:486` row D says "de omslag van het brand book" in a Dutch book)
- **Sections the owner does not need in the main flow:**
  - the contrast table (`:365`)
  - the full type scale with token names (`:431`)
  - "Knoppen op de website" (`:801`)
  - the file table in chapter 08 (`:854`)

  All four are useful for the web developer. They belong in one appendix, "Voor de webbouwer".

## 4. Statements the owner could read as wrong about his company

1. **"Van inpakken tot uitpakken, inclusief montage."** (`:114` Kernwaarden Sterk, `:137` Particulieren)
   - **What the site says:** "Van inpakken tot uitpakken: alles is mogelijk".
   - **Why it is a problem:** montage is his separate Handymanservice. "Inclusief" reads as assembly being part of every quote at no extra cost.
   - **Suggested:** "Van inpakken tot uitpakken, ook montage is mogelijk."
2. **"Losse diensten en spoed"** (`:158-161`)
   - **What it says:** clients can book "alleen een verhuislift, tijdelijke opslag, een handyman" separately ("Heeft u maar één paar sterke handen nodig? Ook dan staat De Reus voor u klaar.").
   - **Why it is a problem:** that is exactly open question 2.4, and it is not confirmed.
   - **Also:** a standalone lift rental would compete with the user's own lift sites (see `sitemap/SITEMAP.md`, chapter 9).
3. **Boilerplates** (`:599-601`)
   - **What they say:** all three say "verhuist particulieren en bedrijven, binnen Nederland en internationaal".
   - **Why it is a problem:** these are the texts others copy word for word. "Wie we zijn" (`:100`) already says it correctly: "particulieren en kleine bedrijven, binnen Nederland en van en naar het buitenland".
   - **Related:** same issue as `qa-report-1.md` P1.3, but in a place that report does not list. The Missie (`:86`, "particulieren en bedrijven") is milder; the same fix makes it consistent.
4. **The mascot** (`:705-716`)
   - **What it says:** it is labelled "Huidige mascotte, in afbouw" and "hoort niet bij de nieuwe huisstijl".
   - **Why it is a problem:** it is the figure on the owner's current homepage. The book announces a decision that is his to make. The two options (a. afscheid nemen, b. laten hertekenen) are in `content/imagery.md` but not in the book.
5. **The cover truck** (`:65-66`)
   - **Why it is a problem:** it can be read as "your van". Whether De Reus has its own vans is open question 1.6.
   - **Suggested:** a one-word caption, "Voorstel", avoids that.
6. **Minor:** the website header mockup (`:781-783`, text inside `assets/mockups/website-header.svg`) says "Particulier of zakelijk". That is fine with the terms, but its menu (Home, Over ons, Diensten, Werkwijze, Contact) differs from the planned menu in `sitemap/SITEMAP.md` (Diensten, Kosten, Werkwijze, Werkgebied, Over ons, Contact).

## 5. Visual weak spots

- **Broken icon captions** (ch06 icon rows, `:676-695`; cause `book.css:364` `overflow-wrap: anywhere`): "Woningontruimi / ng", "Handymanservi / ce", "Verhuisliftservi / ce", in both the white and the blue row. It is the most visible glitch in the book. See `client-read-icoonlabels.png`.
- **Imagery chapter without a single positive image.**
  - **What is there:** the only photo in chapter 06 is the "Niet zo" stock shot; the "Wel" side is text only.
  - **Why it matters:** the chapter about imagery is the most text-heavy chapter after 05, and reads as unfinished.
- **Grids with an empty last slot:**
  - Doelgroepen (3 + 2, `:131`)
  - Wat niet mag (4 + 3, `:276`)
  - Envelop next to Briefpapier (`:775`). The envelope card is half empty and is the only card with no description sentence. See `client-read-papier-rij.png`.
- **Letterhead mockup too small** to read. It is where dummy data would be spotted (P1.4 in `qa-report-1.md`).
- **Kernwaarden** (`:112`): five narrow columns; the label "ZO MERKT DE KLANT HET" wraps to two lines in every card.
- **Tagline highlight** (`:80`): the gold `<mark>` under "te groot!" breaks across the line wrap ("TE" on line 1, "GROOT!" on line 2) and looks like a rendering error.
- **No ending.** The book stops on a version table followed by white space. Brocken closes with an appendix. A closing panel would make it feel finished: logo negative on koningsblauw, the pay-off, and the contact line.
- **Contradiction a careful supplier will notice:**
  - Kleur rule 1 (`:357`) says "Ook geen gele iconen op wit", and the contrast table (`:380`) says goudgeel op wit "Nooit, ook niet voor iconen".
  - Chapter 06 then shows every service icon in blue with a gold accent on white.

---

## Top 10 improvements, ranked by impact

| # | What | Where | Concrete suggestion |
|---|---|---|---|
| 1 | Three sentences state unconfirmed facts about the company | `:114`, `:137` (montage); `:158-161` (losse diensten); `:599-601` (boilerplates) | "inclusief montage" becomes "ook montage is mogelijk". Remove the "Losse diensten en spoed" card, or fold spoed into Particulieren, until open question 2.4 is answered. In all three boilerplates: "particulieren en kleine bedrijven, binnen Nederland en van en naar het buitenland". |
| 2 | The mascot is presented as a decision, not a question | `:705-716` | Change the tag to "Uw keuze". Add the two options from `content/imagery.md`: a. afscheid nemen, b. laten hertekenen in de stijl van het logo. Keep the interim rule (not next to the new logo). |
| 3 | Suppliers lack production specs | ch07 cards `:743-777`; ch02 Bestanden `:287` | Add a one-line "Specificaties" under each mockup, such as: bus = logo minimaal 60 cm breed op de zijkant, telefoonnummer minimaal 15 cm hoog, horizontaal logo achter, folie op Pantone 293 C en 123 C, proef ter goedkeuring; visitekaartje = 85 × 55 mm, 3 mm afloop, 350 g; polo = borstlogo 8 tot 9 cm breed, geborduurd in 2 kleuren. The numbers are suggestions for the builder to confirm. In Bestanden, add CMYK and Pantone PDF logos for print. |
| 4 | Nobody to ask, and no clean package | ch08 `:840-871` | Add "Aanspreekpunt merk: naam, telefoon, e-mail" (open question 1.8) and the sentence "Stuur elke proef eerst ter goedkeuring naar …". Add KvK and BTW rows marked "volgt" (1.1). Deliver the book as a zip of `index.html`, `tokens.css`, `book.css`, `book.js` and `assets/`, without `content/`, `research/` and `qa/`; remove those two rows from the file table. |
| 5 | Cover visual looks like a placeholder | `:65-66`, `.cover-visual` | Let the truck fill its card: drop the inner grey frame and scale it to the full card width. Or set it on a koningsblauw panel with a gold stripe, like the livery. Add the caption "Voorstel belettering". Move "Design tokens: tokens.css" and the print note (`:47`) out of the first screen, to chapter 08. |
| 6 | Chapters 01 and 05 are too long and repeat themselves | `:84-161`, `:486-601` | Chapter 01: merge Missie and Visie into one short "Waar we voor staan"; drop the third paragraph of "Ons verhaal" (it repeats "Wie we zijn"); drop "Zo merkt de klant het" (it repeats Bewijspunten). Chapter 05: remove "Ons ritme"; keep campaign lines A and B only; merge writing rules 7, 8 and 9. Target: about 4,500 words in total, half of Brocken. |
| 7 | Developer jargon in the owner's reading flow | `:365` Contrast, `:431` Typeschaal token names, `:801` Knoppen, `:854` file table, `:47` sidebar | Move these into one closing appendix, "Voor de webbouwer", linked from chapter 08. Keep the six colour rules and one line per type size in the main text. Rename "Tone of voice" to "Toon en schrijfstijl" and fix "brand book" in `:486` to "merkboek". |
| 8 | Icon captions break mid-word | `:676-695`, `book.css:364` | Replace `overflow-wrap: anywhere` with `overflow-wrap: normal; hyphens: manual`, and add soft hyphens: `Woning&shy;ontruiming`, `Handyman&shy;service`, `Verhuislift&shy;service`. Or use the short labels Ontruiming, Handyman, Verhuislift. |
| 9 | Colour rules contradict the icon set | `:357`, `:380` vs ch06 `:668` | Rule 1 becomes: "Geel nooit als tekst of als heel icoon op wit. Een geel accent binnen een blauw icoon mag, want de blauwe vorm draagt het icoon." Contrast table row: "Nooit voor tekst of losse iconen." |
| 10 | The imagery chapter has no positive visual | ch06 `:612-735` | Until there are photos, show what may be used: the van, box and polo mockups and the beeldmerk as the "Wel" image next to the "Niet zo" stock shot. Turn the 10-item shot list into a compact two-column list, so the chapter shows more pictures than text. |

## Also noted (lower priority)

- **Close the book with a back page** (logo negative on koningsblauw, pay-off, contact) after "Versies" (`:873`).
- **Fill or rebalance grids with an empty slot:**
  - Doelgroepen: either 3 + 3, or 2 + 2 + 1 full width.
  - Wat niet mag: add an eighth "niet", or use 4 + 4.
  - Envelop and Briefpapier: stack the envelope under the business card, and give the envelope a description line.
- **Enlarge the letterhead mockup,** or add a click-to-enlarge.
- **Fix the tagline highlight at `:80`:** keep "te groot!" on one line with a non-breaking space, or drop the `<mark>`.
- **Consider a quote (offerte) template** in "Op papier". It is the document a moving company sends most, and the brand promises "een heldere offerte vooraf".
- **Align the website header mockup menu** (`assets/mockups/website-header.svg`) with `sitemap/SITEMAP.md` once the sitemap is approved.
