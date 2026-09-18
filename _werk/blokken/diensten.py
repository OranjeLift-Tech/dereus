"""Diensten op de home (#diensten): acht tegels met het gevulde merkicoon, titel, één zin en een link
naar het paneel op /diensten/. Eén presentatie, geen genummerde lijst ernaast (review dereus-70, D2).
"""
NAAM = "diensten"
CSS = True
JS = False


def html(ctx, kopij, **opties):
    k = kopij
    tegels = []
    for it in k.items:
        sleutel = it.id
        link = it.veld("link") or f"/diensten/#{sleutel}"
        titel = ctx.inline(it.titel)
        tegels.append(f'''<li class="dtegel">
        <span class="dtegel__icoon">{ctx.dienst_icoon(sleutel)}</span>
        <h3 class="dtegel__titel"><a href="{ctx.esc(link)}">{titel}</a></h3>
        <p class="dtegel__tekst">{ctx.inline(it.veld("tekst"))}</p>
        <span class="dtegel__pijl" aria-hidden="true">{ctx.icoon("pijl")}</span>
      </li>''')
    alle = ctx.knop(k.veld("linktekst", "Bekijk alle diensten"), "/diensten/", soort="link")
    return f'''<section class="sectie sectie--mist b-diensten" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap">
    <div class="kopbalk">{ctx.kopgroep(k)}<div class="kopbalk__eind">{alle}</div></div>
    <ul class="dtegels" role="list" data-reveal-groep>
      {"".join(tegels)}
    </ul>
    {ctx.belregel(k.veld("belregel"))}
  </div>
</section>'''
