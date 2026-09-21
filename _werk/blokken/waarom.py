"""Waarom De Reus: vier afspraken naast de inpakillustratie uit de visuele homepage."""
NAAM = "waarom"
CSS = True
JS = False

# Icoon per kaart, op volgorde van de kopij
ICONEN = ["persoon", "doos", "euro", "schild"]

# Kleuraccent van de badge per kaart, op dezelfde volgorde. Twee vlakken maal twee pictogramkleuren
# geeft vier herkenbare badges zonder dat er een kleur buiten het palet bij komt.
# Goudgeel draagt hier een pictogram op donker; het staat nergens als tekst op wit.
ACCENTEN = ["diep-goud", "koning-wit", "diep-wit", "koning-goud"]


def html(ctx, kopij, **opties):
    k = kopij
    kaarten = []
    for i, it in enumerate(k.items):
        icoon = ICONEN[i % len(ICONEN)]
        accent = ACCENTEN[i % len(ACCENTEN)]
        kaarten.append(f'''<li class="wkaart wkaart--{accent}">
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
    </div>
    <div class="waarom__inhoud">
      <figure class="waarom__beeld" data-reveal>
        {ctx.beeld("/img/verwachten-inpakken.webp", "Illustratie van het zorgvuldig inpakken van een verhuizing", 720, 540)}
      </figure>
      <ul class="wkaarten" role="list" data-reveal-groep>{"".join(kaarten)}</ul>
    </div>
    {f'<div class="knoppen waarom__knoppen">{knop}</div>' if knop else ""}
  </div>
</section>'''
