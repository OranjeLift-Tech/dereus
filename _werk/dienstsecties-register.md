# Pattern register: two extra sections per service page (test line)

Test line `test/diensten-paginas` only. Kept by **dereus-37**. Builders claim here through dereus-37 before building; only dereus-37 edits this file.

The user's words: "expand the 8 diensten pages with 2 more page specific sections in each page, use the section-library verified sections for this, add hover effects and clay icons to each one, make sure that the sections make sense in the page. make new ones if there is section style being used already using the section skill"

## Rules

- "Verified" means the 54 entries in `../section-library/catalog.json` at f6c2364. Folders that aren't in the catalog are unregistered drafts, not verified.
- Each of the 16 sections uses its own pattern. No pattern is used twice among the 16, and none may already be used on the site (main or the test line). A pattern counts as used when:
  - its id is named in the source;
  - the site's own section is what the library entry was extracted from;
  - a block on the site has the same layout idea (see "Same layout on the site").
- Claims are first come, first served, in the order they reach dereus-37.
- On a clash, the builder claims another free verified pattern (list at the bottom) or makes a new one with `/section`. A new pattern goes in the table as `new: <id>`.
- A free pattern may be claimed only if it really fits that page's content ("make sure that the sections make sense in the page"). If the best-fitting pattern is taken, that section goes to `/section`, not to a weaker free pattern (dereus-2f, 29-09-2026). Any section waiting on the user's approval of a `/section` preview is marked `waiting on preview` in the status column, so 2f can put them all to him at once. The `/section` skill's `register.py` refuses to write when catalog.json changed underneath it, so two sessions registering at once is safe. It still needs the user's approval of the preview.
- New `/section` patterns go into the test line right away, before his approval (dereus-2f, 29-09-2026 ~16:35: the skill gates only the catalog). He judges them on the page at :8001 and in the preview. `register.py` and the catalog wait for his approval; the previews stay in `_preview/`.
- Block names must be new (build.py refuses a duplicate `NAAM`). Existing names: see `_werk/blokken/*.py`.

## Where the sections go

- One file per page: `_werk/paginas/_dienstsecties_<sleutel>.py`, a list `SECTIES = [(blok, opties), ...]`, at most two entries. Only the named builder edits it.
- `dienstpaginas._blokken()` places them after the service panel and before the reviews.
- build.py doesn't load `_` files as pages, but it does include them in the cache fingerprint.

| page | file | builder |
|---|---|---|
| /diensten/particuliere-verhuizingen/ | _dienstsecties_particulier.py | dereus-28 |
| /diensten/zakelijke-verhuizingen/ | _dienstsecties_zakelijk.py | dereus-28 |
| /diensten/nationale-verhuizingen/ | _dienstsecties_nationaal.py | dereus-49 |
| /diensten/internationale-verhuizingen/ | _dienstsecties_internationaal.py | dereus-49 |
| /diensten/verhuislift/ | _dienstsecties_verhuislift.py | dereus-3e |
| /diensten/tijdelijke-opslag/ | _dienstsecties_opslag.py | dereus-3e |
| /diensten/montage/ | _dienstsecties_montage.py | dereus-ce |
| /diensten/woningontruiming/ | _dienstsecties_woningontruiming.py | dereus-ce |

## Claims (16)

Times: the site scan is a clock time (16:10). The decisions are numbered in the order they were made: step 1 around 16:20, step 8 before 16:31. Preview times are the file times.

Status step 8: all 16 settled, 9 library and 7 new. New `/section` patterns must also differ from each other. Three of them are step or route flows (#5, #11, #13), and they must stay distinct from each other, from branch-route-stops (#3) and from the step layouts on the site: stapkaarten, stappentrap, treden, kortestappen, tijdlijn. Each builder sends dereus-37 the layout idea before building the preview.

| # | page | section | pattern | library or new | block | builder | status |
|---|---|---|---|---|---|---|---|
| 1 | particuliere-verhuizingen | "Is mijn inboedel verzekerd tijdens de verhuizing?" | new: policy-card-folder-seal (replaces policy-card-folder-pocket, policy-card-shield-rise) | new (/section) | polis | 28 | idea cleared step 8 (a white polis card lying over a gold folder, nothing covering it; the clay shield stamped as a seal across the card's edge onto the folder). Earlier: folder-pocket = #8's construction, dereus-37's own suggestion, step 7; shield-rise = #14's depth, step 4; services-cutout-popout-cards = home tiles, step 2. certificate-list-card checked, doesn't fit three terms. Preview rendered 16:44, passes 32/0/0, root `.policy-folder`: section-library/_preview/policy-card-folder-seal/index.html. Checked by dereus-37: matches the cleared idea. The site copy must take its figures from algemene-voorwaarden.md: art. 13 (max €23.000 per inboedel, eigen risico €500) and art. 12 (schade direct op de verhuisdag melden, not a number of days), version 2025; bewakers.py refuses "volledig verzekerd" and "garantie"; waiting on his approval |
| 2 | particuliere-verhuizingen | "Wat u vooraf kunt regelen" | vacancy-detail-card | library (Solar Green) | voorbereidkaart | 28 | accepted step 1 |
| 3 | zakelijke-verhuizingen | "Zo pakken we het aan" | branch-route-stops | library (De Bresser) | routestops | 28 | accepted step 1 (3e released it) |
| 4 | zakelijke-verhuizingen | "Tips voor een soepele kantoorverhuizing" | text-benefit-cards | library (Solar Green) | tipkaarten | 28 | accepted step 2 |
| 5 | nationale-verhuizingen | two addresses: the old and the new address | new: two-addresses-seam-diptych | new (/section) | | 49 | idea cleared step 6 (a full-width diptych of the two ends of the move on a slanted seam, with an address plate under each photo); keep it away from about-then-now (a small tilted photo pair with a dashed arrow beside text); preview rendered 16:30, passes 30/0/0: section-library/_preview/two-addresses-seam-diptych/index.html; waiting on his approval |
| 6 | nationale-verhuizingen | "Wat kost een verhuizing door Nederland?" | price-tiers-table | library (Solar Green) | prijsopbouw-rijen | 49 | accepted step 2 |
| 7 | internationale-verhuizingen | "Zo gaat een verhuizing over de grens" | locations-plate-truck | library (De Bresser) | grensplaat | 49 | accepted step 2, see note |
| 8 | internationale-verhuizingen | "Regel dit op tijd" | new: tip-sheets-pocket | new (/section) | | 49 | idea cleared step 6 (four tip sheets rising out of a pocket front across the width). Preview rendered 16:33, passes 30/0/0, hover on the translate and rotate properties of an inner sheet (reveal on the li): section-library/_preview/tip-sheets-pocket/index.html. Checked by dereus-37: matches the cleared idea; site copy from diensten-internationaal.md #tips; waiting on his approval |
| 9 | verhuislift | "Wat uw verhuisadviseur met u bekijkt" | sustainability-tree-band | library (Solar Green) | | 3e | accepted step 1 |
| 10 | verhuislift | "Ruimte voor de lift op straat" | pay-after-stock-figure | library (Solar Green) | | 3e | accepted step 1 |
| 11 | tijdelijke-opslag | "Zo werkt opslag bij uw verhuizing" | new: door-shutter-steps (replaces steps-plate-door-figure) | new (/section) | | 3e | idea cleared step 7 (a half-rolled storage shutter with the adviser in the opening; steps as a list directly on the ground, no plate). Earlier idea sent back step 4 (= bandpaneel). Preview rendered 16:32, passes 32/0/0, root `.door-shutter-steps`, shutter hover `translate: 0 -10px` clipped by the door: section-library/_preview/door-shutter-steps/index.html. Checked by dereus-37: matches the cleared idea; the packing line is backed by diensten-opslag.md; waiting on his approval |
| 12 | tijdelijke-opslag | "Goed om te weten voor u opslaat" | vision-goals | library (Solar Green) | | 3e | accepted step 1 |
| 13 | montage | "Uit elkaar, en weer in elkaar" | new: assembly-manual-spread (replaces assembly-sheet-steps) | new (/section) | | ce | On the test line #uit-en-in. Idea cleared step 5 (an opened flat-pack manual across the width, two pages mirrored across the fold, no grid, no row). Condition met step 6: #13 now lies flat on a plain ground (no band, no tilt); #14 keeps its tilted blue panel. Earlier idea sent back step 3 (a heading beside a 2x2 grid = vision-goals, #12); waiting on preview |
| 14 | montage | "Wat kost montage bij een verhuizing?" | new: request-note-pinned | new (/section) | | ce | idea cleared step 3 (a sample "Opmerkingen" note pinned over the edge of a tilted blue panel). Preview rendered 16:44, passes 31/1/0 (warn: 3 rule blocks identical to ce's own house-section-factors, eyebrow svg and arrows): section-library/_preview/request-note-pinned/index.html. On the test line #kosten-montage. Checked by dereus-37: matches the cleared idea; the note's label is the form's real field "Opmerkingen (optioneel)" (offerte.md #opmerkingen); waiting on his approval. Its best fit, offerte-per-mail, is on the site |
| 15 | woningontruiming | "Eerst een rustig gesprek" | reply-dial-choices | library (De Bresser) | ontruimgesprek (#gesprek) | ce | accepted step 1 |
| 16 | woningontruiming | "Wat kost een woningontruiming?" | new: house-section-factors | new (/section) | ontruimkosten | ce | idea cleared step 3 (a house cross-section, one factor per floor). Preview rendered 16:42, passes 32/0/0: section-library/_preview/house-section-factors/index.html. On the test line: block ontruimkosten, #kosten-ontruiming. Checked by dereus-37: matches the cleared idea (gable, chimney, walls, floor slabs, clay slots in the left wall, tilted yellow ground band over the base); waiting on his approval |

Note on #7: the nationaal panel already shows a photo rising out of a dark panel (closing-panel-truck). What sets #7 apart is the slanted band with the white list plate over the truck's wheels; keep that clearly visible. The internationaal panel directly above is a full-width navy band (about-window-intro), so don't set another navy band straight underneath it.

## Rejected claims

| when | builder | pattern | why |
|---|---|---|---|
| step 1 | ce | vision-goals, pay-after-stock-figure, sustainability-tree-band | claimed earlier by 3e |
| step 1 | 28 | sustainability-tree-band, vision-goals | claimed earlier by 3e |
| step 1 | 28 (fallbacks) | quote-ways-stairs, key-figures-bar | same layout on the site (below) |
| step 1 | 3e | quote-ways-stairs | same layout on the site: three cards rising as stairs, a person behind a card top (`/kosten/` treden, `/werkwijze/` stappentrap) |
| step 2 | ce | offerte-per-mail (#14) | same layout on the site: a navy band, text and actions on the left, a light arch on the right with the people rising out of it = the internationaal panel (about-window-intro) on /diensten/ and /diensten/internationale-verhuizingen/ |
| step 2 | 28 | services-cutout-popout-cards (#1) | same layout on the site: the home #diensten tiles, where the photo's subject rises above the frame (dtegel__uit) and a clay icon hangs over the bottom corner (dtegel__icoon), with the same dienst photos and teaser lines |

## Already used on the site (main 3dc6f53 plus its uncommitted work, and the test line; scanned 29-09-2026 16:10)

Named in the source, or extracted from the site:

| pattern | where |
|---|---|
| services-grid | home #diensten (blok diensten), extracted from the site |
| benefits-photo-cards | home #waarom (blok waarom), extracted from the site |
| contact-map-form | extracted from the old home #contact |
| split-contact-cta | extracted from the old /over-ons/ #contact |
| reviews-team | blok reviews: home, /diensten/, /over-ons/ and the 8 service pages; extracted from the site |
| after-message-cta | /contact/ #na-bericht (blok na-bericht), extracted from the site |
| service-story-tabs, fixed-price-cards, closing-panel-truck, about-window-intro, text-photo-left, disc-callout-pills, careers-split-crew, two-col-checklist | blok dienstenpanelen, `data-vorm` (VORMEN): /diensten/ and each service page |
| about-address-team | blok over-ons (/over-ons/ #verhaal) |
| contact-direct-location | blok waardenblad (/over-ons/ #zo-werken-wij) |
| quote-block-form | blok formulier (the big form on every page) |
| steps-four-green | blok stapkaarten (home #werkwijze) |
| reviews-photo-wall | blok reviewrail (/werkwijze/ #reviews), from the same Solar Green reviews.html |
| opslag (De Kievit) | blok naband (/werkwijze/ #na-de-verhuizing): "naar het opslagblok van referentie A" = De Kievit's `section.opslag` |
| business-feature-rows | blok kernwaarden (in the source, not rendered today) |
| intro-route-band | blok routeband (in the source, not rendered today) |

Same layout on the site, so these count as used:

| pattern | where |
|---|---|
| quote-ways-stairs | /kosten/ treden (three cards as stairs), /werkwijze/ stappentrap (three cards rising as stairs, a person behind each card top) |
| key-figures-bar | blok actielijn (the figures bar on every page, also on the 8 service pages), /contact/ vertrouwensrij |
| home-hero-scan | the home hero (crew plus quote card) |
| form-card-crew-rise | blok formulier (the cutout rising above the form card) |
| offerte-per-mail | the internationaal panel (about-window-intro): navy band, text and actions, a light arch with people rising out of it |
| services-cutout-popout-cards | home #diensten tiles (blok diensten): cutout rising above the photo frame, clay icon over the bottom corner |

Drafts in use (not verified, can't be claimed): area-rows-map-mover (werkgebied, kaart), slanted-action-line (actielijn).

## Free verified patterns (not used, not claimed; step 2)

about-then-now, featured-news-list, team-profile-cards, group-portrait-nameplate, impact-ribbon-frame, milestone-tape-then-now, page-hero-green-band, certificate-list-card, location-address-panel, projects-gallery-groups, service-project-strip, savings-calculator, product-layers-popout, news-cards-pager, locations-dots, reviews-home-carousel, about-building-cutout
