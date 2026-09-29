"""Bandpaneel (/offerte/, #na-aanvraag): wat er gebeurt nadat u het formulier verstuurt.

Een Goudgele band van rand tot rand met een schuine onderkant, met daarin de klantenservicemedewerker groot aan
haar bureau, en een wit paneel in de rechterkolom dat over de band valt en eronder uithangt. In het paneel staat
alles van het blok: de kop, de drie stappen, de belregel, WhatsApp en de Google-pil.

Gekozen op 29-09-2026: ontwerp 15 uit _ontwerpen/offerte-na-aanvraag-varianten.html (bron in
_ontwerpen/_bron-na-aanvraag-ref/), naar het eerste blok op /contact/ van referentie C: een beeld van rand tot rand
met een schuine onderkant (clip-path met --hoek), en een wit paneel in grid-column 2, grid-row 2 tot 4.

Kopij: offerte.md, blok {#na-aanvraag}: intro, belregel en drie ###-items (titel + tekst), dezelfde kopij als
stappen-na-aanvraag en na-bericht; die twee blokken blijven bestaan (wisselregels in _werk/paginas/offerte.py).

Het beeld is img/offerte-klantenservice-uit.webp (850x730): de medewerker zonder kamer, met bureau, schrijfblok en
kop, waarvan het bureau rechts zacht uitloopt (_ontwerpen/_bron-na-aanvraag-ref/uitsnede.cjs, uit
img/contact-klantenservice-boog-uit.webp). Het uiteinde van het bureau valt onder het paneel (css/blok/bandpaneel.css).
"""

NAAM = "bandpaneel"
CSS = True
JS = False

BEELD = ("/img/offerte-klantenservice-uit.webp", 850, 730)


def _stappen(ctx, k):
    li = "".join(f'''<li class="b-{NAAM}__stap">
              <span class="b-{NAAM}__nr" aria-hidden="true">{i}</span>
              <div><h3 class="b-{NAAM}__titel">{ctx.inline(it.kop)}</h3>{ctx.alineas(it.tekst)}</div>
            </li>''' for i, it in enumerate(k.items, 1))
    return f'<ol class="b-{NAAM}__stappen" role="list">{li}</ol>' if li else ""


def _google(ctx):
    cfg = ctx.cfg
    return (f'<a class="b-{NAAM}__google" href="{ctx.esc(cfg.GOOGLE_PROFIEL)}" rel="noopener" target="_blank">'
            f'{ctx.icoon("google", klasse="ic b-" + NAAM + "__g")}{ctx.sterren(klasse="sterren b-" + NAAM + "__sterren")}'
            f'<span><strong>{ctx.esc(cfg.GOOGLE_SCORE)}</strong> uit 5 op Google</span>'
            f'<span class="vh"> (opent Google in een nieuw tabblad)</span></a>')


def html(ctx, kopij, **opties) -> str:
    k = kopij
    sid = opties.get("id", k.id)
    grond = opties.get("grond", "mist")
    src, breedte, hoogte = BEELD
    # WhatsApp staat als knop in de rij eronder, dus het nummer in de belregel krijgt er geen eigen knop achter
    belregel = ctx.belregel(k.veld("belregel"), klasse=f"belregel b-{NAAM}__bel", whatsapp=False)
    return f'''<section class="b-{NAAM} sectie sectie--{grond}" id="{sid}" aria-labelledby="{sid}-kop">
      <div class="b-{NAAM}__in">
        <div class="b-{NAAM}__band" aria-hidden="true">
          <div class="b-{NAAM}__binnen">{ctx.beeld(src, "", breedte, hoogte, klasse=f"b-{NAAM}__persoon")}</div>
        </div>
        <div class="b-{NAAM}__paneel" data-reveal>
          {ctx.kopgroep(k, klasse=f"b-{NAAM}__kop")}
          {_stappen(ctx, k)}
          <div class="b-{NAAM}__voet">{belregel}<div class="b-{NAAM}__acties">{ctx.whatsapp()}{_google(ctx)}</div></div>
        </div>
      </div>
    </section>'''
