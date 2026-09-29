"""Tipraster: wat u regelt voor uw spullen de opslag in gaan, op /diensten/tijdelijke-opslag/ (#voor-u-opslaat).
Links de kop, de alinea's en onderaan een tekstlink; rechts een kleine kop en vier kaarten (###-items, alleen een kop)
in een raster van twee bij twee, elk met een klei-icoon dat boven de kaart uitsteekt. De laatste kaart is geel.
Bron: section-library/vision-goals. Testlijn test/diensten-paginas, dereus-3e, 29-09-2026.

Kopij: een ##-blok met label, kaartenkop, linktekst, link, alinea's, en ###-items met icoon: (een naam uit
img/clay/). Opties: kopij_van=(document, id), en dan geeft de pagina "kopij": None mee; sectie (standaard "mist").
Vormgeving: css/blok/tipraster.css.
"""

NAAM = "tipraster"
CSS = True
JS = False


def _klei(naam):
    # 4 rem op het scherm, 3,25 rem op een telefoon (tipraster.css); 144 dekt 2x, 240 een telefoon op 3x
    return (f'<img class="b-{NAAM}__klei" src="/img/clay/{naam}-144.webp" srcset="/img/clay/{naam}-144.webp 144w, '
            f'/img/clay/{naam}-240.webp 240w" sizes="(max-width: 559.98px) 3.25rem, 4rem" alt="" width="144" height="144" '
            f'loading="lazy" decoding="async">')


def html(ctx, kopij, sectie="mist", **opties) -> str:
    k = kopij
    if opties.get("kopij_van"):
        document, kid = opties["kopij_van"]
        k = ctx.kopij_van(document).blok(kid)
    sid = ctx.esc(k.id)
    items = list(k.items)
    kaarten = "".join(f'''
            <li class="b-{NAAM}__kaart{f" b-{NAAM}__kaart--uitgelicht" if i == len(items) - 1 else ""}">{_klei(it.veld("icoon") or "dozen")}<h3>{ctx.inline(it.titel)}</h3></li>'''
                      for i, it in enumerate(items))
    link = ctx.knop(k.veld("linktekst"), k.veld("link"), soort="link") if k.veld("linktekst") and k.veld("link") else ""
    return f'''<section class="b-{NAAM} sectie sectie--{sectie}" id="{sid}" aria-labelledby="{sid}-kop">
      <div class="wrap b-{NAAM}__raster">
        <div class="b-{NAAM}__tekst" data-reveal>
          {ctx.kopgroep(k)}
          {ctx.alineas(k.tekst)}
          {link}
        </div>
        <div class="b-{NAAM}__rechts">
          <h3 id="{sid}-kaarten" data-reveal>{ctx.inline(k.veld("kaartenkop"))}</h3>
          <ul class="b-{NAAM}__kaarten" role="list" aria-labelledby="{sid}-kaarten" data-reveal-groep>{kaarten}
          </ul>
        </div>
      </div>
    </section>'''
