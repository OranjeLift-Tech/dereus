"""De vijf stappen voluit, als liggende rail. Familie van het blok werkwijze op de home: dezelfde goudgele
genummerde schijven en dezelfde gestippelde route, hier van links naar rechts in plaats van als hoge tijdlijn.

Pagina: /werkwijze/. Kopij: ## ... {#stappen} met label, intro, u-label en wij-label, en per stap een ###-item
(stap-1 tot stap-5) met tekst, u, wij en optioneel beeld, linktekst en link.

Waarom een rail en geen tijdlijn meer: de vijf stappen zijn kort en horen bij elkaar. Als rail staan ze in één
oogopslag naast elkaar en scheelt dat op een breed scherm ruim duizend pixels hoogte. Het medaillon boven elke
schijf toont een voorwerp, geen mensen: daardoor leest de rij als schema en niet als fotostrook. Dat is de hele
reden dat deze vorm gekozen is, dus zet er geen portretten in.

Beeld per stap: het veld beeld: in de kopij, bijvoorbeeld "beeld: /img/stap-doos.webp". Staat dat er niet, dan
toont het medaillon het merkicoon van die stap. Zo kan de rij vandaag al staan en kunnen de foto's later komen
zonder dat hier iets verandert.

Op smal wordt de rail weer een kolom: medaillon en schijf links, tekst rechts, met het duo eronder. Dat is korter
dan vijf volle kaarten onder elkaar.
"""

NAAM = "stappenlang"
CSS = True
JS = False

# dezelfde lijniconen als het blok werkwijze op de home, in dezelfde volgorde
ICONEN = ["document", "telefoon", "mail", "kalender", "vrachtwagen"]

# het eind van de route: een echte voordeur in het huisvlak uit het logo
HUIS = ("/img/nieuw-huis.webp", 400, 450)


def _medaillon(ctx, it, nr):
    """Het ronde vlak boven de schijf: een voorwerp uit de kopij, anders het merkicoon van deze stap.

    Het medaillon is bewust rond en klein. Een vierkante foto op ware grootte zou van de rij een fotostrook
    maken, en juist omdat het een schema blijft kan de sectie zo kort zijn.
    """
    beeld = it.veld("beeld")
    if beeld:
        binnen = ctx.beeld(beeld, "", 320, 320, klasse=f"b-{NAAM}__foto")
    else:
        binnen = f'<span class="b-{NAAM}__icoon">{ctx.icoon(ICONEN[(nr - 1) % len(ICONEN)])}</span>'
    return f'<span class="b-{NAAM}__medaillon" aria-hidden="true">{binnen}</span>'


def _stap(ctx, k, it, nr):
    duo = ""
    for sleutel in ("u", "wij"):
        if it.veld(sleutel):
            duo += (f'<div class="b-{NAAM}__wie b-{NAAM}__wie--{sleutel}"><dt>{ctx.inline(k.veld(sleutel + "-label"))}</dt>'
                    f'<dd>{ctx.inline(it.veld(sleutel))}</dd></div>')
    duo = f'<dl class="b-{NAAM}__duo">{duo}</dl>' if duo else ""
    link = ctx.knop(it.veld("linktekst"), it.veld("link"), soort="link") if it.veld("link") else ""
    link = f'<p class="b-{NAAM}__acties">{link}</p>' if link else ""
    return f'''<li class="b-{NAAM}__stap" id="{ctx.esc(it.id)}" data-reveal>
        <div class="b-{NAAM}__boven">
          {_medaillon(ctx, it, nr)}
          <span class="b-{NAAM}__schijf" aria-hidden="true"><b>{nr}</b></span>
          <h3 class="b-{NAAM}__titel"><span class="vh">{ctx.esc(k.veld("stap-woord", "Stap"))} {nr}: </span>{ctx.inline(it.titel)}</h3>
          {ctx.alineas(it.tekst)}
        </div>
        <div class="b-{NAAM}__onder">
          {duo}
          {link}
        </div>
      </li>'''


def _einde(ctx, k):
    """Het eind van de route: de schijf met het huisje, de foto van de nieuwe voordeur en de stap naar de offerte."""
    titel = k.veld("einde-titel")
    if not titel:
        return ""
    tekst = k.veld("einde-tekst")
    knop = ctx.knop(k.veld("einde-linktekst"), k.veld("einde-link")) if k.veld("einde-link") else ""
    src, breedte, hoogte = HUIS
    beeld = ctx.beeld(src, k.veld("einde-alt", "Een voordeur van een woning"), breedte, hoogte)
    return f'''<div class="b-{NAAM}__einde" data-reveal>
          <span class="b-{NAAM}__vlag" aria-hidden="true"></span>
          <figure class="b-{NAAM}__huis">
            <span class="b-{NAAM}__huisfoto"><span class="huisvenster">{beeld}</span></span>
            <figcaption><b>{ctx.inline(titel)}</b>{f"<p>{ctx.inline(tekst)}</p>" if tekst else ""}{knop}</figcaption>
          </figure>
        </div>'''


def html(ctx, kopij, **opties) -> str:
    k = kopij
    stappen = "".join(_stap(ctx, k, it, i) for i, it in enumerate(k.items, 1))
    einde = _einde(ctx, k)
    return f'''<section class="b-{NAAM} sectie sectie--mist" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop" data-b="{NAAM}">
      <div class="wrap">
        {ctx.kopgroep(k, "kopgroep--midden")}
        <div class="b-{NAAM}__baan">
          <div class="b-{NAAM}__route" aria-hidden="true"><span class="b-{NAAM}__bus">{ctx.icoon("vrachtwagen")}</span></div>
          <ol class="b-{NAAM}__lijst" role="list">{stappen}</ol>
        </div>
        {einde}
      </div>
    </section>'''
