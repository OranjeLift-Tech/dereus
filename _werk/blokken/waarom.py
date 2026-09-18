"""Waarom De Reus (#waarom): links de kop, de knop en de bevestigde cijfers (uit #cijfers, die geen eigen
band meer krijgt: besluit dereus-28), rechts vier kaarten met een goudgeel huisje als badge.
"""
NAAM = "waarom"
CSS = True
JS = False

# Icoon per kaart, op volgorde van de kopij
ICONEN = ["persoon", "doos", "euro", "schild"]


def feiten(ctx):
    """Hoogstens drie cijfers uit ## ... {#cijfers}. Geen voorrijkosten staat al als kaart, dus die valt weg."""
    blok = ctx.kopij.blok_of_leeg("cijfers")
    items = [it for it in blok.items if "voorrijkosten" not in it.veld("tekst")][:3]
    if not items:
        return ""
    li = "".join(f'<li><b>{ctx.inline(it.titel)}</b><span>{ctx.inline(it.veld("tekst"))}</span></li>' for it in items)
    return f'<ul class="wfeiten" role="list">{li}</ul>'


def html(ctx, kopij, **opties):
    k = kopij
    kaarten = []
    for i, it in enumerate(k.items):
        icoon = ICONEN[i % len(ICONEN)]
        kaarten.append(f'''<li class="wkaart">
        <span class="huisbadge">{ctx.icoon(icoon)}</span>
        <h3 class="wkaart__titel">{ctx.inline(it.titel)}</h3>
        <p>{ctx.inline(it.veld("tekst"))}</p>
      </li>''')
    knop = ctx.knop(k.veld("knop", "Offerte aanvragen"), "/offerte/") if k.veld("knop") else ""
    if k.veld("linktekst") and ctx.live(k.veld("link", "/kosten/")):
        knop += ctx.knop(k.veld("linktekst"), k.veld("link", "/kosten/"), soort="link")
    return f'''<section class="sectie sectie--wit b-waarom" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap waarom">
    <div class="waarom__kop" data-reveal>
      {ctx.kopgroep(k)}
      {f'<div class="knoppen">{knop}</div>' if knop else ""}
      {feiten(ctx)}
    </div>
    <ul class="wkaarten" role="list" data-reveal-groep>
      {"".join(kaarten)}
    </ul>
  </div>
</section>'''
