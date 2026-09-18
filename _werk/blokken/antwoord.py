"""Het directe antwoord op de vraag van de pagina, in een kaart met een Koningsblauwe rand, plus de ankerchips.

Pagina: /kosten/. Kopij: ## ... {#antwoord} met tekst, knop, belregel en (pas als de klant hem geeft) indicatie.
Opties: chips = lijst met blok-id's van deze pagina; de chiptekst is het veld label van dat blok, anders de kop.
"""

NAAM = "antwoord"
CSS = True
JS = False


def _met_tel(ctx, tekst):
    """Opgemaakte tekst, met het telefoonnummer als tel-link (handig op een telefoon)."""
    t = ctx.inline(tekst)
    return t.replace(ctx.tel, f'<a href="{ctx.telhref}">{ctx.tel}</a>', 1) if ctx.tel in t else t


def html(ctx, kopij, **opties) -> str:
    k = kopij
    chips = ""
    for cid in opties.get("chips", []):
        if not ctx.kopij.heeft(cid):
            continue
        b = ctx.kopij.blok(cid)
        chips += f'<li><a href="#{cid}">{ctx.esc(ctx.zonder_opmaak(b.veld("label") or b.kop))}</a></li>'
    if chips:
        chips = (f'<nav class="b-{NAAM}__chips" aria-label="{ctx.esc(opties.get("chipsnaam", "Op deze pagina"))}">'
                 f"<ul>{chips}</ul></nav>")
    indicatie = f'<p class="b-{NAAM}__indicatie">{ctx.inline(k.veld("indicatie"))}</p>' if k.veld("indicatie") else ""
    knop = ctx.knop(k.veld("knop"), "/offerte/", soort="cta") if k.veld("knop") else ""
    bel = f'<span class="b-{NAAM}__bel">{_met_tel(ctx, k.veld("belregel"))}</span>' if k.veld("belregel") else ""
    return f'''<section class="b-{NAAM} sectie sectie--wit" id="{k.id}" aria-labelledby="{k.id}-kop" data-b="{NAAM}">
      <div class="wrap b-{NAAM}__in">
        <div class="b-{NAAM}__kaart" data-reveal>
          <h2 class="b-{NAAM}__kop" id="{k.id}-kop">{ctx.inline(k.kop)}</h2>
          {ctx.alineas(k.tekst)}
          {indicatie}
          <p class="b-{NAAM}__acties">{knop}{bel}</p>
        </div>
        {chips}
      </div>
    </section>'''
