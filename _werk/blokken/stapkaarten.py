"""De stappen als kaarten met een verhuizer die er bovenuit komt. Naar het patroon steps-four-green uit
../section-library (Solar Green, _pages/bedrijven.html#werkwijze), optie A uit
website/review/zowerkthet-bibliotheek-20260928/, die de gebruiker op 28-09-2026 koos ("Step cards with a
mover rising out of each"). Overgenomen via AGENTS.md, dus met de tokens, kopij en beelden van De Reus.
Op /werkwijze/ (#stappen) vervangt het de tijdlijn; dat blok en zijn CSS blijven staan.

Per stap een witte kaart. Bovenin een paneel in lichtblauw naar goud; daarin staat een uitsnede die in de
CSS op de heup is afgesneden, met de snijlijn precies op de onderrand van het paneel, en het hoofd komt
--sk-uit boven de kaart uit. Linksonder in het paneel staat een klei-icoon op de rand, als voorgrond. Op het wit
eronder de bovenregel "Stap n", de titel en een regel tekst; tot 28-09-2026 stond "Stap n" als pil in het
paneel, over de figuur ("the stap 1 - 5 should be replaced with something that does not cover the images"). Figuur groter en klei erbij op 28-09-2026: "Zo werkt
het - make the worker cutout be larger, add clay icons somewhere".

Kopij: een blok met label, kop en intro, en 3 tot 6 stappen als ###-items met een tekst (veld of alinea).
Het item-id wordt het id van de stap (stap-1 tot stap-5). Van de tekst staat alleen de eerste zin op de
kaart, want de kolommen zijn smal; een veld kort: bij de stap gaat voor. De kopij houdt zo de hele tekst.
Heeft het blok u-label en wij-label en de stap u: en wij:, dan staan die als twee korte regels onder de
tekst ("Wat u doet", "Wat wij doen"), elk met de hele tekst van het veld (of u-kort:, wij-kort:). Op de
tijdlijn zaten ze achter een uitklap; hier staan ze open, zodat er bij openen en sluiten niets kan verschuiven.
Tot 28-09-2026 ook hier alleen de eerste zin; daarmee viel bij stap 3 "Wilt u iets aanpassen, dan laat u het
uw verhuisadviseur weten." weg, en die zin moest terug ("sure").
Een stap met link: en linktekst: krijgt een tekstlink, behalve als die naar dezelfde plek wijst als de
slotknop: een sectie heeft een primaire handeling (website/review/design-notes.md, A5).
Onder de kaarten: met einde-titel een slotbalk (einde-titel, einde-tekst, en de knop einde-linktekst naar
einde-link), anders de knoppen knop (naar /offerte/) en linktekst met link, zoals op de home.
Optie grond: mist (standaard), wit of blauw.

De figuren staan hier vast, een per stap, allemaal al live op de site. De snede per figuur: x0 en x1 zijn
de randen van het deel dat in beeld komt, y0 de bovenkant (het hoofd), snede de heup, alles als deel van
de breedte of hoogte van het bestand. html() rekent daar de maat van het vak en de plaats van het beeld
erin uit; die gaan als custom properties in een style-attribuut, zoals --pop en --knip bij de diensten.
"""
import re

NAAM = "stapkaarten"
CSS = True
JS = False

# (pad, breedte, hoogte, naam, x0, x1, y0, snede). Stap 2 is het bellen: de klantenservice met headset
# (live op /contact/ en /offerte/). Stap 5, de verhuisdag, is de ploeg: het trio uit de hero, tot de knie,
# want tot de heup is het te breed voor een kaart. De andere drie zijn de losse verhuizers.
FIGUREN = [
    ("/img/verhuizer-twee-dozen-uit.webp", 407, 1200, "twee-dozen", 0, 1, 0, .545),
    ("/img/contact-klantenservice-uit.webp", 1200, 800, "klantenservice", .12, .70, .06, .97),
    ("/img/verhuizer-doos-zijgreep-uit.webp", 489, 1200, "zijgreep", 0, 1, 0, .56),
    ("/img/verhuizer-doos-deken-uit.webp", 698, 1200, "deken", 0, .77, 0, .53),
    ("/img/team/team-hero-dozen-700.webp", 700, 761, "ploeg", .02, .98, 0, .90),
]

# Het klei-icoon per stap (img/clay/<naam>-144/240.webp, vierkant; website/review/clay-iconen-20260928/): het
# formulier, de telefoon, de offerte in de mail, de klok van de planning en de dozen van de verhuisdag (niet de
# wagen: die staat op de home al rechtsboven in deze sectie, als naadicoon). Het huis staat in de slotbalk,
# waar vroeger het 3D-huis van de tijdlijn stond.
KLEI = ["formulier", "telefoon", "envelop", "klok", "dozen"]
SLOTKLEI = "particulier"

# Stappen waarvan het telefoonnummer geen WhatsApp-knop krijgt (data-geen-whatsapp; het nummer blijft een
# tel-link). Gevraagd voor stap 1 "Offerte aanvragen" op 23-09-2026, en zo overgenomen uit de tijdlijn.
GEEN_WHATSAPP = {"stap-1"}

_ZIN = re.compile(r"(.+?[.?!])(\s|$)")


def _eerste_zin(tekst):
    m = _ZIN.match(tekst or "")
    return m.group(1) if m else (tekst or "")


def _kort(it, sleutel):
    """De korte regel: het veld kort: (of u-kort:, wij-kort:) als de redacteur er een zet, anders bij de tekst
    de eerste zin en bij u: en wij: het hele veld."""
    eigen = it.veld("kort" if sleutel == "tekst" else sleutel + "-kort")
    if eigen:
        return eigen
    return _eerste_zin(it.veld(sleutel)) if sleutel == "tekst" else it.veld(sleutel)


def _figuur(ctx, fig):
    pad, b, h, naam, x0, x1, y0, snede = fig
    bw, bh = x1 - x0, snede - y0
    stijl = (f"--fig-ar:{b * bw / (h * bh):.4f};--fig-b:{100 / bw:.2f}%;"
             f"--fig-l:{-100 * x0 / bw:.2f}%;--fig-t:{-100 * y0 / bh:.2f}%")
    beeld = ctx.beeld(pad, "", b, h, klasse=f"b-{NAAM}__foto")
    return f'<span class="b-{NAAM}__fig b-{NAAM}__fig--{naam}" style="{stijl}">{beeld}</span>'


def _klei(naam, klasse):
    return (f'<img class="{klasse}" src="/img/clay/{naam}-144.webp" srcset="/img/clay/{naam}-144.webp 144w, '
            f'/img/clay/{naam}-240.webp 240w" sizes="4.5rem" alt="" width="144" height="144" loading="lazy" decoding="async">')


def _duo(ctx, k, it):
    """Wat u doet en wat wij doen, als twee regels."""
    regels = ""
    for sleutel in ("u", "wij"):
        if it.veld(sleutel) and k.veld(sleutel + "-label"):
            dd = ctx.inline(_kort(it, sleutel))
            if it.id in GEEN_WHATSAPP:
                dd = dd.replace(ctx.tel, f'<a href="{ctx.telhref}" data-geen-whatsapp>{ctx.tel}</a>', 1)
            regels += (f'<div class="b-{NAAM}__wie b-{NAAM}__wie--{sleutel}"><dt>{ctx.inline(k.veld(sleutel + "-label"))}</dt>'
                       f'<dd>{dd}</dd></div>')
    return f'<dl class="b-{NAAM}__duo">{regels}</dl>' if regels else ""


def _slot(ctx, k):
    """De slotbalk: de belofte en de enige primaire knop van de sectie."""
    titel, tekst = k.veld("einde-titel"), k.veld("einde-tekst")
    knop = ctx.knop(k.veld("einde-linktekst"), k.veld("einde-link"), klasse=f"b-{NAAM}__cta") if k.veld("einde-link") else ""
    return f'''<div class="b-{NAAM}__slot" data-reveal>
      <span class="b-{NAAM}__slotbeeld" aria-hidden="true">{_klei(SLOTKLEI, f"b-{NAAM}__slotklei")}</span>
      <p class="b-{NAAM}__slottekst"><b>{ctx.inline(titel)}</b>{f" {ctx.inline(tekst)}" if tekst else ""}</p>
      {knop}
    </div>'''


def html(ctx, kopij, figuren=FIGUREN, **opties) -> str:
    k = kopij
    if not 3 <= len(k.items) <= 6:
        raise ValueError(f"stapkaarten: 3 tot 6 stappen, niet {len(k.items)}")
    grond = opties.get("grond", "mist")
    woord = k.veld("stap-woord", "Stap")
    stappen = []
    for i, it in enumerate(k.items, 1):
        sid = it.id or f"{k.id}-stap-{i}"
        # de stapknop vervalt als hij hetzelfde doet als de slotknop (A5)
        href, meer = it.veld("link"), ""
        if href and it.veld("linktekst") and href != k.veld("einde-link") and ctx.live(href):
            meer = f'<p class="b-{NAAM}__meer">{ctx.knop(it.veld("linktekst"), href, soort="link")}</p>'
        stappen.append(f'''<li class="b-{NAAM}__stap" id="{ctx.esc(sid)}">
          <div class="b-{NAAM}__kaart">
            <div class="b-{NAAM}__paneel" aria-hidden="true">{_figuur(ctx, figuren[(i - 1) % len(figuren)])}{_klei(KLEI[(i - 1) % len(KLEI)], f"b-{NAAM}__klei b-{NAAM}__klei--{KLEI[(i - 1) % len(KLEI)]}")}</div>
            <span class="b-{NAAM}__nr" aria-hidden="true">{ctx.esc(woord)} {i}</span>
            <h3 class="b-{NAAM}__titel"><span class="vh">{ctx.esc(woord)} {i}: </span>{ctx.inline(it.titel)}</h3>
            <p class="b-{NAAM}__tekst">{ctx.inline(_kort(it, "tekst"))}</p>
            {_duo(ctx, k, it)}
            {meer}
          </div>
        </li>''')
    if k.veld("einde-titel"):
        onder = _slot(ctx, k)
    else:
        knoppen = []
        if k.veld("knop"):
            knoppen.append(ctx.knop(k.veld("knop"), "/offerte/"))
        if k.veld("linktekst"):
            # op een donkere band de lichte knop, zoals de routeband had; op een lichte band een tekstlink
            soort = "licht" if grond in ("blauw", "diep") else "link"
            knoppen.append(ctx.knop(k.veld("linktekst"), k.veld("link", "/werkwijze/"), soort=soort))
        onder = f'<div class="knoppen b-{NAAM}__knoppen">{"".join(knoppen)}</div>' if knoppen else ""
    return f'''<section class="sectie sectie--{grond} b-{NAAM}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap">
    {ctx.kopgroep(k)}
    <ol class="b-{NAAM}__lijst" role="list" data-reveal-groep>
    {"".join(stappen)}
    </ol>
    {onder}
  </div>
</section>'''
