"""Na uw bericht (/contact/, #na-bericht): de Diepblauwe band met dakrand, zoals "Na uw aanvraag" bij referentie A.
Links de kop, de tekst en twee knoppen; rechts de verhuisadviseur die terugbelt, aan haar bureau, zonder
kamer erachter en met een grote Goudgele duim ernaast, zoals de contactkop van referentie A
(css/blok/na-bericht.css).

Kopij: contact.md, blok {#na-bericht}: label, kop, tekst (alinea's), knop.
"""

NAAM = "na-bericht"
CSS = True
JS = False

# de verhuisadviseur met bureau, kop, toetsenbord, telefoon en scherm; de kamer is weg
# (bron en werkwijze: _ai-beelden/na-bericht-bureau/). Onderaan loopt het bureau tot de rand door,
# die rand krijgt in de css ronde hoeken; boven is alles vrij.
FOTO = ("/img/contact-klantenservice-bureau-uit.webp", 1060, 690)

# duim omhoog: manchet links, hand met duim; egaal, de kleur komt uit de css
DUIM = ('<svg class="b-na-bericht__duim" viewBox="0 0 120 108" aria-hidden="true" focusable="false">'
        '<rect x="0" y="46" width="22" height="62" rx="2.5"/>'
        '<path d="M30 102V51L53 12C57 5 62 2 68 3C76 4 80 11 78 20L72 40H109C116 40 121 46 119.5 53'
        'L108.5 101C107.5 105.5 104 108 99.5 108H36C32.7 108 30 105.3 30 102Z"/></svg>')


def html(ctx, kopij, **opties) -> str:
    k = kopij
    sid = opties.get("id", k.id or "na-bericht")
    knoppen = (ctx.knop(k.veld("knop", "Offerte aanvragen"), "/offerte/", soort="cta")
               + ctx.knop("Mail ons", f"mailto:{ctx.mail}", soort="licht", icoon="mail", klasse="knop--icoon-voor"))
    return f'''<section class="b-{NAAM} sectie sectie--diep" id="{sid}" aria-labelledby="{sid}-kop">
      <div class="wrap b-{NAAM}__in">
        <div class="b-{NAAM}__tekst" data-reveal>
          {ctx.kopgroep(k, klasse=f"b-{NAAM}__kop")}
          {ctx.alineas(k.tekst)}
          <div class="knoppen">{knoppen}</div>
        </div>
        <figure class="b-{NAAM}__beeld" data-reveal>
          {DUIM}
          {ctx.beeld(FOTO[0], "", FOTO[1], FOTO[2], klasse=f"b-{NAAM}__foto")}
        </figure>
      </div>
    </section>'''
