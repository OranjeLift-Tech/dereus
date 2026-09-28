"""Persoonlijk contact (/contact/, #contactkaarten), opgezet zoals "Even persoonlijk contact" bij De Kievit:
boven links de kop, de tekst en twee knoppen; rechts in plaats van een foto een Koningsblauwe belkaart met
de bereikbaarheidsstatus. Daaronder vier kanaalkaarten: bellen, mailen, een bericht sturen, een offerte.

Kopij: contact.md, blok {#contactkaarten}: label, kop, intro, en vier ###-items (titel, tekst, linktekst)
in deze volgorde: bellen, mailen, bericht, offerte. De links vult het blok zelf in.
Geen WhatsApp en geen "kom langs": die zijn niet bevestigd.

Het nummer op de kaart "Bel ons" krijgt geen WhatsApp-knop (data-geen-whatsapp): de belkaart erboven
draagt er al een, direct onder het grote nummer. Gevraagd door de gebruiker, en sinds 23-09-2026
mag dat, want naast elk nummer WhatsApp is een richtlijn en geen eis meer (zie kit.contactlinks).

Optie figuur: (pad, bestand_breed, bestand_hoog, x, y, w, h) zet een verhuizer tussen de kop en de
belkaart, in lagen voor diepte: achter hem de plaat en het huis van .uitsnede (css/blok/uitsnede.css),
voor hem optie voorgrond. De laatste vier getallen zijn de alfa-bbox. De pagina moet dan
extra_css=("uitsnede",) hebben.
Optie voorgrond: (pad, bestand_breed, bestand_hoog), een uitsnede die voor de benen van de figuur staat.
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

# Per icoon het voorwerp: sinds 28-09-2026 het klei-icoon in img/clay/<naam>-240/480.webp (vierkant,
# website/review/clay-iconen-20260928/) in plaats van de 3D-render uit img/contact-3d/. Naam, breedte, hoogte.
VOORWERP = {
    "telefoon": ("telefoon", 240, 240),
    "mail": ("envelop", 240, 240),
    "document": ("formulier", 240, 240),
    "doos": ("dozen", 240, 240),
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
    geen_wa = " data-geen-whatsapp" if doel == "tel" else ""   # de belkaart erboven heeft de knop al
    if icoon in VOORWERP:                  # een echt voorwerp dat uit de kaart steekt, in plaats van het lijnicoon
        naam, b, h = VOORWERP[icoon]
        beeld = (f'<span class="b-{NAAM}__ic b-{NAAM}__ic--3d" aria-hidden="true"><img class="b-{NAAM}__obj b-{NAAM}__obj--{naam}" '
                 f'src="/img/clay/{naam}-240.webp" srcset="/img/clay/{naam}-240.webp 240w, /img/clay/{naam}-480.webp 480w" '
                 f'sizes="10rem" alt="" width="{b}" height="{h}" loading="lazy" decoding="async"></span>')
    else:
        beeld = f'<span class="b-{NAAM}__ic" aria-hidden="true">{ctx.icoon(icoon)}</span>'
    return f'''<li class="b-{NAAM}__kanaal">
              {beeld}
              <h3 class="b-{NAAM}__titel">{ctx.inline(it.kop)}</h3>
              {ctx.alineas(it.tekst)}
              <a class="b-{NAAM}__link" href="{ctx.esc(href)}"{geen_wa}><span>{ctx.esc(linktekst).replace("@", "@<wbr>")}</span>{ctx.icoon("pijl")}</a>
            </li>'''


def _belkaart(ctx):
    c = ctx.cfg
    regels = "".join(f'<li><span>{ctx.esc(t["kort"])}</span><span>{ctx.esc(t["van"])} tot {ctx.esc(t["tot"])}</span></li>'
                     for t in c.TIJDEN)
    return f'''<div class="b-{NAAM}__belkaart" data-reveal>
          <p class="b-{NAAM}__status">{ctx.bereikbaar("bereikbaar")}</p>
          <a class="b-{NAAM}__nummer" href="{c.TELHREF}">{ctx.esc(c.TEL)}</a>
          <ul class="b-{NAAM}__uren" role="list">{regels}</ul>
        </div>'''


def html(ctx, kopij, **opties) -> str:
    k = kopij
    sid = opties.get("id", k.id)
    kanalen = "".join(_kanaal(ctx, i, it) for i, it in enumerate(k.items))
    figuur = ""
    if opties.get("figuur"):
        src, breed, hoog, ux, uy, uw, uh = opties["figuur"]
        # alt leeg: de figuur illustreert de kop ernaast en voegt er niets aan toe
        beeld = ctx.beeld(src, "", breed, hoog, klasse="uitsnede__beeld")
        if opties.get("voorgrond"):
            vsrc, vbreed, vhoog = opties["voorgrond"]
            beeld += ctx.beeld(vsrc, "", vbreed, vhoog, klasse=f"b-{NAAM}__voorgrond")
        maten = f"--uit-breed:{breed};--uit-hoog:{hoog};--uit-x:{ux};--uit-y:{uy};--uit-w:{uw};--uit-h:{uh}"
        figuur = f'<div class="uitsnede b-{NAAM}__figuur" style="{maten}" aria-hidden="true">{beeld}</div>'
    return f'''<section class="b-{NAAM} sectie sectie--wit" id="{sid}" aria-labelledby="{sid}-kop">
      <div class="wrap">
        <div class="b-{NAAM}__boven">
          <div class="b-{NAAM}__tekst" data-reveal>
            {ctx.kopgroep(k, klasse=f"b-{NAAM}__kop")}
            {ctx.alineas(k.tekst, klasse=f"b-{NAAM}__alinea")}
          </div>
          {figuur}{_belkaart(ctx)}
        </div>
        {f'<ul class="b-{NAAM}__kanalen" role="list" data-reveal-groep>{kanalen}</ul>' if kanalen else ""}
      </div>
    </section>'''
