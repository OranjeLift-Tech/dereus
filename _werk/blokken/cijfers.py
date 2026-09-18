"""Een eigen cijferband met uitsluitend de bestaande feiten uit de homepagekopij."""
NAAM = "cijfers"
CSS = True
JS = False


def html(ctx, kopij, **opties):
    k = kopij
    items = "".join(
        f'<li><strong>{ctx.inline(it.titel)}</strong><span>{ctx.inline(it.veld("tekst"))}</span></li>'
        for it in k.items
    )
    return f'''<section class="b-cijfers" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap">
    <h2 class="vh" id="{ctx.esc(k.id)}-kop">{ctx.inline(k.kop)}</h2>
    <ul class="cijferlijst" role="list" data-reveal-groep>{items}</ul>
  </div>
</section>'''
