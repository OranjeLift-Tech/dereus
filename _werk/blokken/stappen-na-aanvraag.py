"""Stappen na de aanvraag (/offerte/): wat er gebeurt nadat u het formulier verstuurt, plus de Google-pil.

Kopij: offerte.md, blok {#na-aanvraag}: intro, belregel en drie ###-items (titel + tekst).
De Google-pil gebruikt de score uit config.py ("4,9 uit 5 op Google", zonder aantal).
"""

NAAM = "stappen-na-aanvraag"
CSS = True
JS = False


def html(ctx, kopij, **opties) -> str:
    k = kopij
    sid = opties.get("id", k.id)
    stappen = "".join(
        f'''<li class="b-{NAAM}__stap">
              <span class="b-{NAAM}__nr" aria-hidden="true">{i}</span>
              <h3 class="b-{NAAM}__titel">{ctx.inline(it.kop)}</h3>
              {ctx.alineas(it.tekst)}
            </li>''' for i, it in enumerate(k.items, 1))
    belregel = k.veld("belregel")
    # eindpunt van de route: het beeldmerk (sterke armen), alleen versiering; opmaak in css/blok/offerte-diepte.css
    eind = (f'<li class="b-{NAAM}__eind" aria-hidden="true">'
            f'{ctx.beeld("/img/logo/dereus-beeldmerk.svg", "", 1000, 509)}</li>')
    return f'''<section class="b-{NAAM} sectie sectie--wit" id="{sid}" aria-labelledby="{sid}-kop">
      <div class="wrap">
        {ctx.kopgroep(k, klasse=f"b-{NAAM}__kop")}
        <ol class="b-{NAAM}__rij" role="list" data-reveal-groep>{stappen}{eind}</ol>
        <div class="b-{NAAM}__voet">
          <p class="b-{NAAM}__google">{ctx.icoon("google", klasse="ic b-" + NAAM + "__g")}{ctx.sterren(klasse="sterren b-" + NAAM + "__sterren")}<span><strong>{ctx.esc(ctx.cfg.GOOGLE_SCORE)}</strong> uit 5 op Google</span></p>
          {ctx.belregel(belregel, klasse=f"belregel b-{NAAM}__bel")}
        </div>
      </div>
    </section>'''
