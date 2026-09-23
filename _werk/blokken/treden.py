"""Drie kaarten als traptreden: klein, midden en groot. Zonder bedragen, tot de klant een indicatie geeft.

Pagina: /kosten/ (kopij_id "verhuizing"). Kopij: label, intro of tekst, drie items (titel, tekst, optioneel bedrag),
lijst (links naar de diensten) en knop.
"""

import kit

NAAM = "treden"
CSS = True
JS = False

# Optie figuren (/kosten/): verhuizers die de trap op gaan, en wat zij dragen loopt mee met de tekst
# eronder: een los meubel bij de studio, een bank bij de eengezinswoning, een stapel dozen bij het grote
# huis. Alle figuren lopen naar rechts (wens van de gebruiker) en hebben hun voeten compleet in beeld,
# want ze staan op een traprand. Vormgeving onderaan css/blok/kosten-diepte.css.
# Trede 1 was de verhuizer met de bureaustoel (treden/stoel-rechts.webp); die zette hij op 23-09-2026
# in zijn beeldinventaris op "delete". In de plaats staat de verhuizer met twee dozen uit de uitsnede-
# ronde van die dag. Let op: hij loopt naar de kijker toe en niet naar rechts; geen van de bestaande
# losse verhuizers loopt naar rechts.
# Naam, bron, breedte, hoogte.
FIGUREN = [
    ("twee-dozen", "/img/verhuizer-twee-dozen-uit.webp", 407, 1200),
    ("bank", "/img/treden/bank.webp", 640, 477),
    ("merk", "/img/logo/dereus-beeldmerk-negatief.svg", 1000, 509),
]
# Trede 3 hoort de verhuizer met dozen te zijn; het beeldmerk erboven is de terugval zolang dat beeld
# nog niet bestaat. Maken: _ai-beelden/PROMPTS-treden-dozen.txt, daarna treden-uitsnede.mjs en
# treden-export.cjs. Dat laatste script meldt de maat die hier hoort te staan.
DOZEN = ("dozen", "/img/treden/dozen.webp", 293, 440)


def figuren():
    """De drie figuren, met de dozenverhuizer op trede 3 zodra dat beeld er is."""
    lijst = list(FIGUREN)
    if (kit.WORTEL / DOZEN[1].lstrip("/")).exists():
        lijst[2] = DOZEN
    return lijst


def html(ctx, kopij, **opties) -> str:
    k = kopij
    treden = ""
    for i, it in enumerate(k.items[:3]):
        bedrag = f'<p class="b-{NAAM}__bedrag">{ctx.inline(it.veld("bedrag"))}</p>' if it.veld("bedrag") else ""
        fig = ""
        if opties.get("figuren") and i < len(FIGUREN):      # decoratie: wie er op de trede staat
            naam, src, b, h = figuren()[i]
            fig = (f'<span class="b-{NAAM}__fig b-{NAAM}__fig--{naam}" aria-hidden="true"><img src="{src}" alt="" '
                   f'width="{b}" height="{h}" loading="lazy" decoding="async"></span>')
        treden += (f'<li class="b-{NAAM}__trede b-{NAAM}__trede--{i + 1}">{fig}<h3 class="b-{NAAM}__tredekop">{ctx.inline(it.kop)}</h3>'
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
