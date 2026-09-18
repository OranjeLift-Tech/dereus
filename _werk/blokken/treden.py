"""Drie kaarten als traptreden: klein, midden en groot. Zonder bedragen, tot de klant een indicatie geeft.

Pagina: /kosten/ (kopij_id "verhuizing"). Kopij: label, intro of tekst, drie items (titel, tekst, optioneel bedrag),
lijst (links naar de diensten) en knop.
"""

NAAM = "treden"
CSS = True
JS = False


def html(ctx, kopij, **opties) -> str:
    k = kopij
    treden = ""
    for i, it in enumerate(k.items[:3]):
        bedrag = f'<p class="b-{NAAM}__bedrag">{ctx.inline(it.veld("bedrag"))}</p>' if it.veld("bedrag") else ""
        treden += (f'<li class="b-{NAAM}__trede b-{NAAM}__trede--{i + 1}"><h3 class="b-{NAAM}__tredekop">{ctx.inline(it.kop)}</h3>'
                   f'{bedrag}{ctx.alineas(it.tekst)}</li>')
    links = "".join(f"<li>{ctx.inline(r)}</li>" for r in k.lijst)
    links = f'<ul class="b-{NAAM}__links">{links}</ul>' if links else ""
    knop = ctx.knop(k.veld("knop"), "/offerte/", soort="cta") if k.veld("knop") else ""
    intro = f'<p class="b-{NAAM}__intro">{ctx.inline(k.veld("intro"))}</p>' if k.veld("intro") else ""
    return f'''<section class="b-{NAAM} sectie sectie--wit" id="{k.id}" aria-labelledby="{k.id}-kop" data-b="{NAAM}">
      <div class="wrap b-{NAAM}__in">
        <div class="b-{NAAM}__kop" data-reveal>
          {ctx.label(k.veld("label"))}
          <h2 class="h2" id="{k.id}-kop">{ctx.inline(k.kop)}</h2>
          {intro}{ctx.alineas(k.tekst)}
          {links}
          <p class="b-{NAAM}__acties">{knop}</p>
        </div>
        <ol class="b-{NAAM}__trap" data-reveal-groep>{treden}</ol>
      </div>
    </section>'''
