"""Kernwaarden als gedrag (/over-ons/ #zo-werken-wij): de Koningsblauwe band met dakrand, kop in het midden
en de items als genummerde kaarten (3 per rij, de laatste rij in het midden). Werkt voor 3 tot 8 items.
Tekst per item als tekst:-veld of als losse alinea's onder de ###-titel.
Iconen volgen de kernwaarden uit het merkboek via het item-id (sterk, zorgvuldig, betrouwbaar, eerlijk, betrokken).
"""
NAAM = "kernwaarden"
CSS = True
JS = False

ICONEN = {"sterk": "doos", "zorgvuldig": "schild", "betrouwbaar": "klok", "eerlijk": "euro", "betrokken": "persoon"}


def html(ctx, kopij, sectie="blauw", **opties):
    k = kopij
    kaarten = []
    for i, it in enumerate(k.items, 1):
        kaarten.append(f'''<li class="kw">
        <div class="kw__kop"><span class="kw__nr" aria-hidden="true">{i:02d}</span><span class="kw__icoon" aria-hidden="true">{ctx.icoon(ICONEN.get(it.id, "check"))}</span></div>
        <h3 class="kw__titel">{ctx.inline(it.titel)}</h3>
        {ctx.alineas(it.tekst)}
      </li>''')
    return f'''<section class="sectie sectie--{sectie} b-kernwaarden" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap">
    {ctx.kopgroep(k, "kopgroep--midden")}
    <ul class="kwlijst" role="list" data-reveal-groep>
      {"".join(kaarten)}
    </ul>
  </div>
</section>'''
