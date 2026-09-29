"""Meldtegels: wat u in uw aanvraag meldt voor een verhuizing met de verhuislift, op /diensten/verhuislift/
(#vooraf-melden). Een lichtblauwe kaart met links de kop, een alinea en een link naar het formulier, rechts drie
witte tegels (###-items) met een klei-icoon dat boven de tegel uitsteekt.
Bron: section-library/sustainability-tree-band. Testlijn test/diensten-paginas, dereus-3e, 29-09-2026.

Kopij: een ##-blok met label, linktekst, link, een alinea, en ###-items met icoon: (een naam uit img/clay/) en een
korte regel. Opties: kopij_van=(document, id), en dan geeft de pagina "kopij": None mee; sectie (standaard "wit").
Vormgeving: css/blok/meldtegels.css.
"""

NAAM = "meldtegels"
CSS = True
JS = False


def _klei(naam):
    # 4,5 rem op het scherm, 3,75 rem op een telefoon (meldtegels.css); 144 dekt 2x, 240 een telefoon op 3x
    return (f'<img class="b-{NAAM}__klei" src="/img/clay/{naam}-144.webp" srcset="/img/clay/{naam}-144.webp 144w, '
            f'/img/clay/{naam}-240.webp 240w" sizes="(max-width: 559.98px) 3.75rem, 4.5rem" alt="" width="144" height="144" '
            f'loading="lazy" decoding="async">')


def html(ctx, kopij, sectie="wit", **opties) -> str:
    k = kopij
    if opties.get("kopij_van"):
        document, kid = opties["kopij_van"]
        k = ctx.kopij_van(document).blok(kid)
    sid = ctx.esc(k.id)
    tegels = "".join(f'''
            <li><div class="b-{NAAM}__tegel">{_klei(it.veld("icoon") or "dozen")}<h3>{ctx.inline(it.titel)}</h3>{ctx.alineas(it.tekst)}</div></li>'''
                     for it in k.items)
    # Een tekstlink en geen tweede knop: het formulier staat twee secties lager, en de knop "Offerte aanvragen"
    # staat al in het paneel erboven en in de sectie hierna.
    link = ctx.knop(k.veld("linktekst"), k.veld("link") or "#aanvraag", soort="link") if k.veld("linktekst") else ""
    return f'''<section class="b-{NAAM} sectie sectie--{sectie}" id="{sid}" aria-labelledby="{sid}-kop">
      <div class="wrap">
        <div class="b-{NAAM}__kaart">
          <div class="b-{NAAM}__tekst" data-reveal>
            {ctx.kopgroep(k)}
            {ctx.alineas(k.tekst)}
            {link}
          </div>
          <ul class="b-{NAAM}__tegels" role="list" data-reveal-groep>{tegels}
          </ul>
        </div>
      </div>
    </section>'''
