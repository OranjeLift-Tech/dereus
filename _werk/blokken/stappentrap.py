"""Van aanvraag tot verhuisdag in drie stappen: drie witte kaarten die als een trap van links naar rechts
oplopen, elk met een medewerker die achter de bovenrand van zijn kaart staat, boven een Goudgele band. Links
staan de kop, de intro, de belofte (einde-titel en einde-tekst) en de enige knop van de sectie met de belregel.

Gevraagd op 29-09-2026: de klant vond vijf stappen te veel, drie leest rustiger; de trap moest blijven, in de
opzet van het blok "Bel ons, videobel ons of kom langs" van referentie B (.sgm: .sgm__tekst links met eyebrow,
kop, intro en .sgm__acties; rechts .sgm__beeld met .sgm__band en .sgm__kaarten, waarin kaart 2 en 3 telkens een
trede hoger staan en .sgm__figuur achter de bovenrand van .sgm__doos staat; in .sgm__boven een 3D-icoon en een
pil). Overgenomen met de tokens, kopij en beelden van De Reus: de pil zegt "Stap n", het icoon is klei, de band
is Goudgeel, de kaart heeft de plaatrand en de groene neonhover van /contact/.

Pagina: /werkwijze/ (#stappen). Kopij: ## ... met label, intro, u-label, wij-label, einde-titel, einde-tekst,
einde-linktekst, einde-link en belregel, en precies drie ###-items met tekst (of kort:), u: en wij:.
Van de tekst staat alleen de eerste zin op de kaart, of het veld kort: als de redacteur dat zet; u: en wij:
staan heel op de kaart, zoals bij stapkaarten. Een stapknop vervalt als hij naar dezelfde plek wijst als de
knop links (een sectie heeft een primaire handeling, website/review/design-notes.md, A5).

De figuren staan hier vast, drie verschillende mensen die nog niet elders op /werkwijze/ staan (dus geen
tweede uit de reeks img/verhuizer-*-uit, die al in de voorbereiding staat): de klantenservice met headset bij
de aanvraag en het gesprek, de verhuisadviseur van /offerte/ bij de offerte, en de ploeg met de dozen op de
verhuisdag. De snede werkt als bij stapkaarten: x0 en x1 zijn de randen van het deel dat in beeld komt, y0 de
bovenkant, snede de heup, alles als deel van de breedte of hoogte van het bestand; hoogte schaalt de figuur
ten opzichte van de andere twee, zodat de hoofden ongeveer even groot zijn.
"""
import re

NAAM = "stappentrap"
CSS = True
JS = False

# (pad, breedte, hoogte, naam, x0, x1, y0, snede, hoogte)
FIGUREN = [
    ("/img/contact-klantenservice-uit.webp", 1200, 800, "klantenservice", .11, .75, .06, .80, 1.0),
    ("/img/offerte-figuur-uit.webp", 435, 752, "adviseur", 0, 1, 0, .78, .9),
    ("/img/team/team-hero-dozen-700.webp", 700, 761, "ploeg", 0, 1, 0, .52, 1.0),
]

# Het klei-icoon per stap (img/clay/<naam>-144/240.webp): de telefoon van het gesprek, de offerte in de mail en
# de dozen van de verhuisdag. Het huis staat bij de belofte links.
KLEI = ["telefoon", "envelop", "dozen"]
SLOTKLEI = "particulier"

# Stappen waarvan het telefoonnummer geen WhatsApp-knop krijgt (data-geen-whatsapp; het nummer blijft een
# tel-link). Gevraagd voor stap 1 op 23-09-2026, zo overgenomen uit de tijdlijn en stapkaarten.
GEEN_WHATSAPP = {"stap-1"}

_ZIN = re.compile(r"(.+?[.?!])(\s|$)")


def _eerste_zin(tekst):
    m = _ZIN.match(tekst or "")
    return m.group(1) if m else (tekst or "")


def _kort(it, sleutel):
    """Het veld kort: (of u-kort:, wij-kort:) als de redacteur er een zet, anders bij de tekst de eerste zin en
    bij u: en wij: het hele veld."""
    eigen = it.veld("kort" if sleutel == "tekst" else sleutel + "-kort")
    if eigen:
        return eigen
    return _eerste_zin(it.veld(sleutel)) if sleutel == "tekst" else it.veld(sleutel)


def _figuur(ctx, fig):
    pad, b, h, naam, x0, x1, y0, snede, schaal = fig
    bw, bh = x1 - x0, snede - y0
    stijl = (f"--fig-ar:{b * bw / (h * bh):.4f};--fig-b:{100 / bw:.2f}%;"
             f"--fig-l:{-100 * x0 / bw:.2f}%;--fig-t:{-100 * y0 / bh:.2f}%;--fig-h:{schaal}")
    beeld = ctx.beeld(pad, "", b, h, klasse=f"b-{NAAM}__foto")
    return f'<span class="b-{NAAM}__fig b-{NAAM}__fig--{naam}" style="{stijl}" aria-hidden="true">{beeld}</span>'


def _klei(naam, klasse, sizes):
    return (f'<img class="{klasse}" src="/img/clay/{naam}-144.webp" srcset="/img/clay/{naam}-144.webp 144w, '
            f'/img/clay/{naam}-240.webp 240w" sizes="{sizes}" alt="" width="144" height="144" loading="lazy" decoding="async">')


def _duo(ctx, k, it):
    """Wat u doet en wat wij doen, als twee regels."""
    regels = ""
    for sleutel in ("u", "wij"):
        if it.veld(sleutel) and k.veld(sleutel + "-label"):
            dd = ctx.inline(_kort(it, sleutel))
            if it.id in GEEN_WHATSAPP:
                dd = dd.replace(ctx.tel, f'<a href="{ctx.telhref}" data-geen-whatsapp>{ctx.tel}</a>', 1)
            regels += (f'<div class="b-{NAAM}__wie"><dt>{ctx.inline(k.veld(sleutel + "-label"))}</dt>'
                       f'<dd>{dd}</dd></div>')
    return f'<dl class="b-{NAAM}__duo">{regels}</dl>' if regels else ""


def _kaart(ctx, k, it, i, woord):
    sid = it.id or f"{k.id}-stap-{i}"
    href, meer = it.veld("link"), ""
    if href and it.veld("linktekst") and href != k.veld("einde-link") and ctx.live(href):
        meer = f'<p class="b-{NAAM}__meer">{ctx.knop(it.veld("linktekst"), href, soort="link")}</p>'
    klei = KLEI[(i - 1) % len(KLEI)]
    return f'''<li class="b-{NAAM}__kaart" id="{ctx.esc(sid)}" style="--i:{i - 1}">
            {_figuur(ctx, FIGUREN[(i - 1) % len(FIGUREN)])}
            <div class="b-{NAAM}__doos">
              <div class="b-{NAAM}__boven" aria-hidden="true">{_klei(klei, f"b-{NAAM}__klei", "2.9rem")}<span class="b-{NAAM}__pil">{ctx.esc(woord)} {i}</span></div>
              <h3 class="b-{NAAM}__titel"><span class="vh">{ctx.esc(woord)} {i}: </span>{ctx.inline(it.titel)}</h3>
              <p class="b-{NAAM}__regel">{ctx.inline(_kort(it, "tekst"))}</p>
              {_duo(ctx, k, it)}
              {meer}
            </div>
          </li>'''


def _links(ctx, k):
    """Onder de intro: de belofte met het huis, dan de knop en de belregel."""
    titel, tekst = k.veld("einde-titel"), k.veld("einde-tekst")
    slot = ""
    if titel:
        slot = (f'<p class="b-{NAAM}__slot">{_klei(SLOTKLEI, f"b-{NAAM}__slotklei", "3.75rem")}'
                f'<span><b>{ctx.inline(titel)}</b>{f" {ctx.inline(tekst)}" if tekst else ""}</span></p>')
    knop = ctx.knop(k.veld("einde-linktekst"), k.veld("einde-link"), klasse=f"b-{NAAM}__cta") if k.veld("einde-link") else ""
    bel = ctx.belregel(k.veld("belregel"), klasse=f"belregel b-{NAAM}__bel")
    acties = f'<div class="b-{NAAM}__acties">{knop}{bel}</div>' if knop or bel else ""
    return slot + acties


def html(ctx, kopij, **opties) -> str:
    k = kopij
    if len(k.items) != 3:
        raise ValueError(f"stappentrap: precies drie stappen, niet {len(k.items)}")
    grond = "wit" if opties.get("grond") == "wit" else "mist"
    woord = k.veld("stap-woord", "Stap")
    kaarten = "".join(_kaart(ctx, k, it, i, woord) for i, it in enumerate(k.items, 1))
    return f'''<section class="b-{NAAM} sectie sectie--{grond}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop" data-b="{NAAM}">
      <div class="wrap b-{NAAM}__binnen">
        {ctx.kopgroep(k, f"b-{NAAM}__kop", extra=_links(ctx, k))}
        <div class="b-{NAAM}__beeld">
          <div class="b-{NAAM}__band" aria-hidden="true"></div>
          <ol class="b-{NAAM}__kaarten" role="list" data-reveal-groep>{kaarten}</ol>
        </div>
      </div>
    </section>'''
