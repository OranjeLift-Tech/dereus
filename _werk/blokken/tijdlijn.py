"""De vijf stappen als trap naar de voordeur: vijf treden die van links naar rechts oplopen, elk met een
witte plaat en een 3D-render die boven de plaat uitkomt; het cijfer staat op het blauwe stootbord.
De zesde, gele trede is het slot: de echte voordeur in het huis uit het logo, de belofte en de knop,
met het team met de verhuisdozen erbovenop. De kop staat linksboven naast de trap.

Gekozen op 28-09-2026: ontwerp 03 uit _ontwerpen/werkwijze-stappen-varianten-2.html (de trap uit ronde 1
met de opzet van de werkwijzekop van referentie A: kop links, figuur rechts). Wat hieronder staat over
de stations en de lijn is de geschiedenis van de vorige vorm; de uitklap, het knippen en de renders
per stap zijn gebleven.

Pagina: /werkwijze/. Kopij: ## ... {#stappen} met label, intro, u-label en wij-label, en per stap een
###-item (stap-1 tot stap-5) met tekst, u en wij. Het slot onderaan komt uit einde-titel, einde-tekst,
einde-linktekst en einde-link.

Waarom deze vorm: de rail (stappenlang) zette vijf volle kaarten onder elkaar, waardoor het overzicht
pas ontstond na de hele sectie. Hier staan de vijf stations naast elkaar op een lijn, zodat de route in
een oogopslag te zien is. Boven 1180 px loopt de lijn horizontaal door de huisjes; daaronder kantelt
dezelfde lijn naar verticaal en staan de huisjes in de linkermarge, zodat de lijn tussen de platen door
zichtbaar blijft in plaats van erachter te verdwijnen. Op 1440 px scheelt dat ruim 650 px hoogte.
De bouw van een plaat komt van /contact/: zichtbare dikte, een schaduw naar rechtsonder, en een render
voor het gele huis langs. Alles staat stil.

Knippen gebeurt hier en niet in de kopij. De kolommen zijn smal, dus van tekst, u en wij staat alleen de
eerste zin op de kaart. Wil een redacteur een andere korte regel, dan zet hij die in het veld kort: bij
de stap; dat veld gaat voor. website/content/werkwijze.md houdt zo de volledige tekst.

Een stapknop vervalt als hij naar dezelfde plek wijst als de knop in het slot: een sectie krijgt een
primaire handeling (website/review/design-notes.md, A5). De knop naar /kosten/ bij stap 3 blijft dus
staan, die naar /offerte/ bij stap 1 niet.

Beeld per stap: de renders staan hier vast, zoals stappenlang de lijniconen vastlegde. Het veld beeld:
in de kopij doet in dit blok niets. Dat wees naar de stapfoto's, en die vielen af op A3 (geen
stockfoto's van onbekende mensen); einde-alt hoort bij dezelfde vervallen foto.
"""
import re

NAAM = "tijdlijn"
CSS = True
JS = False

# Per station een klei-icoon (img/clay/<naam>-144/240.webp, vierkant; website/review/clay-iconen-20260928/).
# Sinds de samenvoeging van 28-09-2026 ("with new clay icons") in plaats van de 3D-renders uit img/contact-3d/,
# img/kaart-3d/ en img/kosten-3d/. Dezelfde vijf als de stapkaarten die hier eerst stonden, voor dezelfde vijf
# stappen: het formulier bij de aanvraag, de telefoon bij het contact, de envelop bij de offerte, de klok bij de
# planning en de dozen op de verhuisdag.
VOORWERPEN = ["formulier", "telefoon", "envelop", "klok", "dozen"]

# Het slot: de echte voordeur (dezelfde foto als het eind van de weg op de home) in het huis uit het logo,
# en het team met de verhuisdozen dat bovenop de gele trede staat.
SLOTBEELD = ("/img/nieuw-huis.webp", 400, 450)
TEAM = ("/img/team/team-hero-dozen-700.webp", 700, 761)

_ZIN = re.compile(r"(.+?[.?!])(\s|$)")


def _eerste_zin(tekst):
    m = _ZIN.match(tekst or "")
    return m.group(1) if m else (tekst or "")


def _kort(blok, sleutel):
    """De korte regel: het veld kort: als de redacteur er een zet, anders de eerste zin."""
    if sleutel == "tekst" and blok.veld("kort"):
        return blok.veld("kort")
    if sleutel != "tekst" and blok.veld(sleutel + "-kort"):
        return blok.veld(sleutel + "-kort")
    return _eerste_zin(blok.veld(sleutel))


def _render(ctx, naam):
    beeld = ctx.beeld(f"/img/clay/{naam}-240.webp", "", 240, 240, klasse=f"b-{NAAM}__obj b-{NAAM}__obj--{naam}",
                      srcset=f"/img/clay/{naam}-144.webp 144w, /img/clay/{naam}-240.webp 240w", sizes="5.4rem")
    return f'<span class="b-{NAAM}__ic" aria-hidden="true">{beeld}</span>'


# Stappen waarvan het telefoonnummer geen WhatsApp-knop krijgt (data-geen-whatsapp; het nummer blijft
# een tel-link). Gevraagd voor stap 1 "Offerte aanvragen" op 23-09-2026. Het nummer wordt hier zelf een
# link, want kit.contactlinks() slaat alleen een tel-link met het attribuut over.
GEEN_WHATSAPP = {"stap-1"}


def _stap(ctx, k, it, nr):
    duo = ""
    for sleutel in ("u", "wij"):
        if it.veld(sleutel):
            dd = ctx.inline(_kort(it, sleutel))
            if it.id in GEEN_WHATSAPP:
                dd = dd.replace(ctx.tel, f'<a href="{ctx.telhref}" data-geen-whatsapp>{ctx.tel}</a>', 1)
            duo += (f'<div class="b-{NAAM}__wie b-{NAAM}__wie--{sleutel}"><dt>{ctx.inline(k.veld(sleutel + "-label"))}</dt>'
                    f'<dd>{dd}</dd></div>')
    duo = f'<dl class="b-{NAAM}__duo">{duo}</dl>' if duo else ""
    # de stapknop vervalt als hij hetzelfde doet als de slotknop (A5)
    link = ""
    href = it.veld("link")
    if href and href != k.veld("einde-link") and ctx.live(href):
        link = f'<p class="b-{NAAM}__meer">{ctx.knop(it.veld("linktekst"), href, soort="link")}</p>'
    if duo:
        # Wat u doet, wat wij doen en de stapknop staan achter een native details: bij het openen van
        # de pagina leest de bezoeker vijf titels met een regel, niet vijftien regels tegelijk. Geen
        # JS nodig, geen beweging, en de tekst blijft in de HTML staan voor zoekmachines en
        # voorleessoftware.
        #
        # Het paneel hangt in de CSS los onder de plaat (absoluut), dus openen en sluiten verandert
        # geen enkele hoogte: de sectie blijft even hoog en er schuift niets mee. Het paneel legt zich
        # zolang het openstaat over wat eronder staat, als een kaartje dat erboven ligt.
        # name= maakt er een uitklap van waarvan er maar een tegelijk openstaat, zonder JavaScript;
        # een browser die dat attribuut niet kent laat er meer tegelijk open en dat is ook goed.
        opschrift = f'{k.veld("u-label")} en {k.veld("wij-label")[0].lower()}{k.veld("wij-label")[1:]}'
        duo = (f'<details class="b-{NAAM}__uitklap" name="{ctx.esc(k.id or NAAM)}-uitklap">'
               f'<summary><span>{ctx.inline(opschrift)}</span>'
               f'<span class="b-{NAAM}__plus" aria-hidden="true">{ctx.icoon("plus")}</span></summary>'
               f'<div class="b-{NAAM}__paneel">{duo}{link}</div></details>')
        link = ""
    naam = VOORWERPEN[(nr - 1) % len(VOORWERPEN)]
    return f'''<li class="b-{NAAM}__stap" id="{ctx.esc(it.id)}" style="--i:{nr - 1}">
            <div class="b-{NAAM}__plaat">
              {_render(ctx, naam)}
              <h3 class="b-{NAAM}__titel"><span class="vh">{ctx.esc(k.veld("stap-woord", "Stap"))} {nr}: </span>{ctx.inline(it.titel)}</h3>
              <p class="b-{NAAM}__regel">{ctx.inline(_kort(it, "tekst"))}</p>
              {duo}
              {link}
            </div>
            <div class="b-{NAAM}__stoot" aria-hidden="true"><span class="b-{NAAM}__nr">{nr:02d}</span></div>
          </li>'''


def _slot(ctx, k):
    """De afsluitende balk: het huis, de belofte en de enige primaire knop van de sectie."""
    titel = k.veld("einde-titel")
    if not titel:
        return ""
    tekst = k.veld("einde-tekst")
    knop = ctx.knop(k.veld("einde-linktekst"), k.veld("einde-link"), klasse=f"b-{NAAM}__cta") if k.veld("einde-link") else ""
    src, breedte, hoogte = SLOTBEELD
    deur = ctx.beeld(src, "", breedte, hoogte)
    tsrc, tbreedte, thoogte = TEAM
    team = ctx.beeld(tsrc, "", tbreedte, thoogte, klasse=f"b-{NAAM}__team")
    return f'''<div class="b-{NAAM}__slot" style="--i:5">
          {team}
          <div class="b-{NAAM}__plaat">
            <span class="b-{NAAM}__deur" aria-hidden="true">{deur}</span>
            <div class="b-{NAAM}__slottekst"><b>{ctx.inline(titel)}</b>{f"<p>{ctx.inline(tekst)}</p>" if tekst else ""}</div>
            {knop}
          </div>
          <div class="b-{NAAM}__stoot" aria-hidden="true"></div>
        </div>'''


def html(ctx, kopij, **opties) -> str:
    k = kopij
    grond = "mist" if opties.get("grond", "mist") == "mist" else "wit"
    stappen = "".join(_stap(ctx, k, it, i) for i, it in enumerate(k.items, 1))
    # data-reveal-groep staat op de trap en niet op de lijst: de lijst heeft display:contents en dus geen
    # eigen vak, waardoor de IntersectionObserver in site.js hem nooit in beeld zag komen en de vijf treden
    # onzichtbaar bleven (28-09-2026). De treden zelf verschijnen nu zonder onthulling.
    return f'''<section class="b-{NAAM} sectie sectie--{grond}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop" data-b="{NAAM}">
      <div class="wrap">
        <div class="b-{NAAM}__trap" data-reveal-groep>
          {ctx.kopgroep(k, f"b-{NAAM}__kop")}
          <ol class="b-{NAAM}__lijst" role="list">{stappen}</ol>
          {_slot(ctx, k)}
        </div>
      </div>
    </section>'''
