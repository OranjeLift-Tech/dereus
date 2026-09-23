"""Kernwaarden als gedrag (/over-ons/ #zo-werken-wij): de Koningsblauwe band met dakrand, kop in het midden
en de items als genummerde kaarten (3 per rij, de laatste rij in het midden). Werkt voor 3 tot 8 items.
Tekst per item als tekst:-veld of als losse alinea's onder de ###-titel.
Iconen volgen de kernwaarden uit het merkboek via het item-id (sterk, zorgvuldig, betrouwbaar, eerlijk, betrokken).
Optie beeld: (pad, bestand_breed, bestand_hoog, x, y, w, h) zet de kop links en een uitsnede rechts,
met een gekantelde plaat en het huissilhouet erachter. Zonder die optie blijft de kop gecentreerd.
Optie compact: "gematigd" of "krap" zet de band, de beeldkolom en de kaarten strakker. De overlap
van de plaat blijft in beide gevallen staan; de maten staan bovenin css/blok/kernwaarden.css.
"""
NAAM = "kernwaarden"
CSS = True
JS = False

ICONEN = {"sterk": "doos", "zorgvuldig": "schild", "betrouwbaar": "klok", "eerlijk": "euro", "betrokken": "persoon"}


def html(ctx, kopij, sectie="blauw", beeld=None, compact=None, **opties):
    k = kopij
    kaarten = []
    for i, it in enumerate(k.items, 1):
        kaarten.append(f'''<li class="kw">
        <div class="kw__kop"><span class="kw__nr" aria-hidden="true">{i:02d}</span><span class="kw__icoon" aria-hidden="true">{ctx.icoon(ICONEN.get(it.id, "check"))}</span></div>
        <h3 class="kw__titel">{ctx.inline(it.titel)}</h3>
        {ctx.alineas(it.tekst)}
      </li>''')
    if beeld:
        src, breed, hoog, ux, uy, uw, uh = beeld
        # alt leeg: de uitsnede illustreert de tekst ernaast en voegt er niets aan toe
        uit = ctx.beeld(src, "", breed, hoog, klasse="uitsnede__beeld kwbeeld__uit")
        maten = f"--uit-breed:{breed};--uit-hoog:{hoog};--uit-x:{ux};--uit-y:{uy};--uit-w:{uw};--uit-h:{uh}"
        hoofd = f'''<div class="kwhoofd">
      {ctx.kopgroep(k, "kwhoofd__tekst")}
      <div class="uitsnede kwbeeld" style="{maten}" data-reveal>{uit}</div>
    </div>'''
    else:
        hoofd = ctx.kopgroep(k, "kopgroep--midden")
    if compact and compact not in ("gematigd", "krap"):
        raise ValueError(f"kernwaarden: compact is 'gematigd' of 'krap', niet {compact!r}")
    klassen = "sectie sectie--" + sectie + " b-kernwaarden"
    if beeld:
        klassen += " b-kernwaarden--beeld"
        if compact:
            klassen += f" b-kernwaarden--{compact}"
    return f'''<section class="{klassen}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap">
    {hoofd}
    <ul class="kwlijst" role="list" data-reveal-groep>
      {"".join(kaarten)}
    </ul>
  </div>
</section>'''
