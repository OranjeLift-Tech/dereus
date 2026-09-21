"""Persoonlijk contact (/contact/, #contactkaarten), opgezet zoals "Even persoonlijk contact" bij De Kievit:
boven links de kop, de tekst en twee knoppen; rechts in plaats van een foto een Koningsblauwe belkaart met
de bereikbaarheidsstatus. Daaronder vier kanaalkaarten: bellen, mailen, een bericht sturen, een offerte.

Kopij: contact.md, blok {#contactkaarten}: label, kop, intro, en vier ###-items (titel, tekst, linktekst)
in deze volgorde: bellen, mailen, bericht, offerte. De links vult het blok zelf in.
Geen WhatsApp en geen "kom langs": die zijn niet bevestigd.
"""

NAAM = "contactkaarten"
CSS = True
JS = False

# Per positie: icoon, link en standaard linktekst
KANALEN = [
    ("telefoon", "tel", None),
    ("mail", "mail", None),
    ("document", "#formulier", "Naar het formulier"),
    ("doos", "/offerte/", "Offerte aanvragen"),
]

# Per icoon het 3D-voorwerp in img/contact-3d/: bestandsnaam, breedte en hoogte (bron: _ai-beelden/contact-3d/)
VOORWERP = {
    "telefoon": ("telefoon", 208, 400),
    "mail": ("envelop", 347, 400),
    "document": ("formulier", 346, 400),
    "doos": ("doos", 425, 400),
}


def _kanaal(ctx, i, it):
    icoon, doel, std = KANALEN[i] if i < len(KANALEN) else ("pijl", "/contact/", "Meer")
    if doel == "tel":
        href, std = ctx.telhref, ctx.tel
    elif doel == "mail":
        href, std = f"mailto:{ctx.mail}", ctx.mail
    else:
        href = doel
    linktekst = it.veld("linktekst") or std
    if icoon in VOORWERP:                  # een echt voorwerp dat uit de kaart steekt, in plaats van het lijnicoon
        naam, b, h = VOORWERP[icoon]
        beeld = (f'<span class="b-{NAAM}__ic b-{NAAM}__ic--3d" aria-hidden="true"><img class="b-{NAAM}__obj b-{NAAM}__obj--{naam}" '
                 f'src="/img/contact-3d/{naam}.webp" alt="" width="{b}" height="{h}" loading="lazy" decoding="async"></span>')
    else:
        beeld = f'<span class="b-{NAAM}__ic" aria-hidden="true">{ctx.icoon(icoon)}</span>'
    return f'''<li class="b-{NAAM}__kanaal">
              {beeld}
              <h3 class="b-{NAAM}__titel">{ctx.inline(it.kop)}</h3>
              {ctx.alineas(it.tekst)}
              <a class="b-{NAAM}__link" href="{ctx.esc(href)}"><span>{ctx.esc(linktekst).replace("@", "@<wbr>")}</span>{ctx.icoon("pijl")}</a>
            </li>'''


def _belkaart(ctx):
    c = ctx.cfg
    regels = "".join(f'<li><span>{ctx.esc(t["kort"])}</span><span>{ctx.esc(t["van"])} tot {ctx.esc(t["tot"])}</span></li>'
                     for t in c.TIJDEN)
    return f'''<div class="b-{NAAM}__belkaart" data-reveal>
          <span class="b-{NAAM}__belic" aria-hidden="true">{ctx.icoon("telefoon")}</span>
          <p class="b-{NAAM}__status">{ctx.bereikbaar("bereikbaar")}</p>
          <a class="b-{NAAM}__nummer" href="{c.TELHREF}">{ctx.esc(c.TEL)}</a>
          <ul class="b-{NAAM}__uren" role="list">{regels}</ul>
        </div>'''


def html(ctx, kopij, **opties) -> str:
    k = kopij
    sid = opties.get("id", k.id)
    kanalen = "".join(_kanaal(ctx, i, it) for i, it in enumerate(k.items))
    return f'''<section class="b-{NAAM} sectie sectie--wit" id="{sid}" aria-labelledby="{sid}-kop">
      <div class="wrap">
        <div class="b-{NAAM}__boven">
          <div class="b-{NAAM}__tekst" data-reveal>
            {ctx.kopgroep(k, klasse=f"b-{NAAM}__kop")}
            {ctx.alineas(k.tekst, klasse=f"b-{NAAM}__alinea")}
          </div>
          {_belkaart(ctx)}
        </div>
        {f'<ul class="b-{NAAM}__kanalen" role="list" data-reveal-groep>{kanalen}</ul>' if kanalen else ""}
      </div>
    </section>'''
