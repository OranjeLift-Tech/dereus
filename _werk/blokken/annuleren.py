"""Annuleren en wijzigen: een tipvak met de regels uit de algemene voorwaarden.

Pagina: /kosten/. Kopij: ## ... {#annuleren} met label, intro, lijst, slot, linktekst en link.
"""

NAAM = "annuleren"
CSS = True
JS = False


def html(ctx, kopij, **opties) -> str:
    k = kopij
    regels = "".join(f"<li>{ctx.inline(r)}</li>" for r in k.lijst)
    regels = f'<ul class="b-{NAAM}__regels">{regels}</ul>' if regels else ""
    intro = f"<p>{ctx.inline(k.veld('intro'))}</p>" if k.veld("intro") else ""
    slot = f'<p class="b-{NAAM}__slot">{ctx.inline(k.veld("slot"))}</p>' if k.veld("slot") else ""
    link = ctx.knop(k.veld("linktekst"), k.veld("link"), soort="link") if k.veld("link") else ""
    return f'''<section class="b-{NAAM} sectie sectie--wit" id="{k.id}" aria-labelledby="{k.id}-kop" data-b="{NAAM}">
      <div class="wrap">
        <div class="b-{NAAM}__vak b-{NAAM}__vak--kalender" data-reveal>
          <div class="b-{NAAM}__kopdeel">
            {ctx.label(k.veld("label"))}
            <h2 class="h2" id="{k.id}-kop">{ctx.inline(k.kop)}</h2>
          </div>
          <div class="b-{NAAM}__beeld" aria-hidden="true"><img class="b-{NAAM}__kal" src="/img/kosten-kalender/bureau.webp" alt="" width="769" height="720" loading="lazy" decoding="async"></div>
          <div class="b-{NAAM}__tekst">{intro}{ctx.alineas(k.tekst)}{regels}{slot}<p class="b-{NAAM}__acties">{link}</p></div>
        </div>
      </div>
    </section>'''
