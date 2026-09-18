"""De vijf stappen voluit, als verticale tijdlijn. Familie van het blok werkwijze op de home: dezelfde goudgele
genummerde schijven, dezelfde gestippelde route en hetzelfde busje, hier van boven naar beneden.

Pagina: /werkwijze/. Kopij: ## ... {#stappen} met label, intro, u-label en wij-label, en per stap een ###-item
(stap-1 tot stap-5) met tekst, u, wij en optioneel linktekst en link.
Op desktop wisselen de kaarten van kant; op mobiel staat alles in één kolom met de route links.
"""

NAAM = "stappenlang"
CSS = True
JS = False

# dezelfde lijniconen als het blok werkwijze op de home, in dezelfde volgorde
ICONEN = ["document", "telefoon", "mail", "kalender", "vrachtwagen"]


def _stap(ctx, k, it, nr):
    icoon = ICONEN[(nr - 1) % len(ICONEN)]
    duo = ""
    for sleutel in ("u", "wij"):
        if it.veld(sleutel):
            duo += (f'<div class="b-{NAAM}__wie b-{NAAM}__wie--{sleutel}"><dt>{ctx.inline(k.veld(sleutel + "-label"))}</dt>'
                    f'<dd>{ctx.inline(it.veld(sleutel))}</dd></div>')
    duo = f'<dl class="b-{NAAM}__duo">{duo}</dl>' if duo else ""
    link = ctx.knop(it.veld("linktekst"), it.veld("link"), soort="link") if it.veld("link") else ""
    link = f'<p class="b-{NAAM}__acties">{link}</p>' if link else ""
    return f'''<li class="b-{NAAM}__stap" id="{ctx.esc(it.id)}">
        <span class="b-{NAAM}__schijf" aria-hidden="true"><b>{nr}</b></span>
        <article class="b-{NAAM}__kaart" data-reveal>
          <span class="b-{NAAM}__icoon" aria-hidden="true">{ctx.icoon(icoon)}</span>
          <h3 class="b-{NAAM}__titel"><span class="vh">{ctx.esc(k.veld("stap-woord", "Stap"))} {nr}: </span>{ctx.inline(it.titel)}</h3>
          {ctx.alineas(it.tekst)}
          {duo}
          {link}
        </article>
      </li>'''


def html(ctx, kopij, **opties) -> str:
    k = kopij
    stappen = "".join(_stap(ctx, k, it, i) for i, it in enumerate(k.items, 1))
    return f'''<section class="b-{NAAM} sectie sectie--mist" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop" data-b="{NAAM}">
      <div class="wrap">
        {ctx.kopgroep(k, "kopgroep--midden")}
        <div class="b-{NAAM}__baan">
          <div class="b-{NAAM}__route" aria-hidden="true"><span class="b-{NAAM}__bus">{ctx.icoon("vrachtwagen")}</span></div>
          <ol class="b-{NAAM}__lijst" role="list">{stappen}</ol>
        </div>
      </div>
    </section>'''
