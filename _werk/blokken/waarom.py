"""Waarom De Reus: vier afspraken naast een foto van twee verhuizers die samen een bank dragen."""
NAAM = "waarom"
CSS = True
JS = False

# Per kaart het klei-icoon, op volgorde van de kopij (img/clay/<naam>-144/176.webp, vierkant). Goedgekeurd op
# 28-09-2026 als vervanging van de 3D-renders (website/review/clay-iconen-20260928/). Het vak blijft 5.4 x 4.6 rem
# met object-fit contain (waarom.css), dus het icoon staat op 74 px; 176 dekt 2x.
VOORWERP = [
    "headset",     # één vaste verhuisadviseur
    "trap",        # vakmensen: de kast veilig de trap af
    "nationaal",   # geen voorrijkosten: de verhuiswagen
    "schild",      # standaard verzekerd
]

# Ondergrond per kaart, op dezelfde volgorde. Vier lichte tinten uit het palet die net van elkaar
# verschillen; zie waarom.css.
ONDERGROND = ["blauw", "creme", "mint", "mist"]


def html(ctx, kopij, **opties):
    k = kopij
    kaarten = []
    for i, it in enumerate(k.items):
        naam = VOORWERP[i % len(VOORWERP)]
        grond = ONDERGROND[i % len(ONDERGROND)]
        kaarten.append(f'''<li class="wkaart wkaart--{grond}">
        <span class="wkaart__voorwerp" aria-hidden="true"><img class="wkaart__obj wkaart__obj--{naam}" src="/img/clay/{naam}-144.webp" srcset="/img/clay/{naam}-144.webp 144w, /img/clay/{naam}-176.webp 176w" sizes="4.6rem" alt="" width="176" height="176" loading="lazy" decoding="async"></span>
        <h3 class="wkaart__titel">{ctx.inline(it.titel)}</h3>
        <p>{ctx.inline(it.veld("tekst"))}</p>
      </li>''')
    # Eén knop, en dus één doorverwijzing die een handeling is. De sleutels linktekst en link zijn
    # hier ook uit home.md gehaald, zodat er geen veld staat dat niets doet. Zie design-notes A5.
    knop = ctx.knop(k.veld("knop", "Offerte aanvragen"), "/offerte/") if k.veld("knop") else ""
    return f'''<section class="sectie sectie--wit b-waarom" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap waarom">
    <div class="waarom__kop" data-reveal>
      {ctx.kopgroep(k)}
    </div>
    <div class="waarom__inhoud">
      <figure class="waarom__beeld" data-reveal>
        <span class="waarom__kader">{ctx.beeld("/img/verhuisdag-dragen-stoep.webp", "Twee verhuizers dragen samen een bank, ingepakt in een deken met spanbanden, naast een open witte bus in een straat met bakstenen huizen", 1400, 1050, klasse="waarom__foto")}</span>
        <span class="waarom__uit" aria-hidden="true">{ctx.beeld("/img/verhuisdag-dragen-stoep-uit.webp", "", 1400, 1050)}</span>
      </figure>
      <ul class="wkaarten" role="list" data-reveal-groep>{"".join(kaarten)}</ul>
    </div>
    {f'<div class="knoppen waarom__knoppen">{knop}</div>' if knop else ""}
  </div>
</section>'''
