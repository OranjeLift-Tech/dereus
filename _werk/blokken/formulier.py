"""Het gedeelde formulier: offerteaanvraag (/offerte/) en contactbericht (/contact/).

Opties: variant = "offerte" of "contact"; id (standaard "formulier"); beeld = uitsneefoto bovenin de
zijkolom; team = groepsfoto onderaan de zijkolom, tegen de onderrand; merk = het beeldmerk
onderaan het meeschuivende blok (tot 28-09-2026 op /offerte/); figuur = uitsnede (pad, of (pad, breedte, hoogte)) boven
een blauw paneel, de opzet van het offerteblok van referentie B (/contact/ en /offerte/, zie _paneel). beeld, team en figuur sluiten
elkaar in de praktijk uit.
Kopij: het blok {#formulier} van de pagina. Blokvelden: knop, privacy, fout-kop, fout-versturen, bezig,
zij-kop en lijst (de drie vinkjes in de zijkolom; zonder zij-kop vervalt de zijkolom), bel-zin (de regel
boven de belknop, alleen met figuur).
Per veld een ###-item met de veldnaam als id: de titel is het label, met hulp, placeholder, fout,
fout-onjuist en onbekend (het vinkje naast Naar en Wanneer). Bij dienst is de lijst de keuzelijst,
in de vorm "- particulier = Particuliere verhuizing".

Het formulier werkt zonder JavaScript (gewone POST naar Web3Forms). Met JavaScript: invullen vanuit het
adres (?van=&naar=&datum=&dienst=), adressuggesties van PDOK, een foutoverzicht en doorsturen naar de
bedanktpagina. Zie js/blok/formulier.js.
"""

from kit import SOLAR, SOLAR_VIEWBOX

NAAM = "formulier"
CSS = True
JS = True

EINDPUNT = "https://api.web3forms.com/submit"
KIES = "Kies wat u nodig heeft"            # de lege keuze, gelijk aan de offertepil; placeholder: in de kopij gaat voor
VARIANTEN = {
    "offerte": {"bedankt": "/offerte/bedankt/", "onderwerp": "Nieuwe offerteaanvraag via verhuisbedrijfdereus.nl",
                "afzender": "Offerteformulier Verhuisbedrijf De Reus"},
    "contact": {"bedankt": "/contact/bedankt/", "onderwerp": "Nieuw bericht via verhuisbedrijfdereus.nl",
                "afzender": "Contactformulier Verhuisbedrijf De Reus"},
}
# De naam van een veld is de regel in de e-mail die bij De Reus binnenkomt
MAILNAAM = {"van": "Verhuizen van", "naar": "Verhuizen naar", "datum": "Gewenste datum", "dienst": "Dienst",
            "naam": "Naam", "telefoon": "Telefoon", "email": "E-mail", "opmerkingen": "Opmerkingen",
            "bericht": "Bericht", "naar-onbekend": "Bestemming nog onbekend", "datum-onbekend": "Datum nog onbekend"}

# De telefoon in de gele cirkel van de zijkolom: het Solar-icoon uit kit (28-09-2026), met eigen maat en
# hetzelfde ingezoomde tekenvlak als de sprite.
TELEFOON_SVG = (f'<svg viewBox="{SOLAR_VIEWBOX}" width="24" height="24" overflow="visible" fill="currentColor" aria-hidden="true" focusable="false">'
                + SOLAR["telefoon"] + '</svg>')


def _is_placeholder(sleutel):
    return (not sleutel) or sleutel.upper().startswith("VUL-")


def _attrs(ctx, it, verplicht):
    """Gedeelde attributen: verplicht, foutteksten voor het script en de koppeling met de hulptekst."""
    a = ""
    if verplicht:
        a += " required"
    if it.veld("fout"):
        a += f' data-fout="{ctx.esc(it.veld("fout"))}"'
    if it.veld("fout-onjuist"):
        a += f' data-fout-onjuist="{ctx.esc(it.veld("fout-onjuist"))}"'
    if it.veld("placeholder"):
        a += f' placeholder="{ctx.esc(it.veld("placeholder"))}"'
    if it.veld("hulp"):
        a += f' aria-describedby="f-{it.id}-hulp"'
    return a


def _hulp(ctx, it):
    return f'<span class="b-{NAAM}__hulp" id="f-{it.id}-hulp">{ctx.inline(it.veld("hulp"))}</span>' if it.veld("hulp") else ""


def _vinkje(ctx, it, doel):
    """Het vinkje "nog onbekend" naast Naar en Wanneer."""
    tekst = it.veld("onbekend")
    if not tekst:
        return ""
    return (f'<label class="b-{NAAM}__optie"><input type="checkbox" id="f-{it.id}-onbekend" name="{MAILNAAM[it.id + "-onbekend"]}" '
            f'value="ja" data-onbekend-voor="{doel}"><span>{ctx.esc(tekst)}</span></label>')


def _adres(ctx, it, verplicht):
    """Van of Naar op het verzendlabel: een tekstveld met een lijst suggesties van PDOK eronder."""
    return f'''<div class="b-{NAAM}__adres">
      <label for="f-{it.id}">{ctx.esc(it.kop)}</label>
      <div class="b-{NAAM}__adresveld">
        <input type="text" id="f-{it.id}" name="{MAILNAAM[it.id]}" autocomplete="off" data-adres role="combobox"
          aria-expanded="false" aria-autocomplete="list" aria-controls="f-{it.id}-keuzes"{_attrs(ctx, it, verplicht)}>
        <ul class="b-{NAAM}__keuzes" id="f-{it.id}-keuzes" role="listbox" aria-label="{ctx.esc(it.kop)}" hidden></ul>
      </div>
      {_hulp(ctx, it)}{_vinkje(ctx, it, "f-" + it.id)}
    </div>'''


def _veld(ctx, it, soort, verplicht, extra="", breed=False):
    klasse = f"b-{NAAM}__veld" + (f" b-{NAAM}__veld--breed" if breed else "")
    if soort == "textarea":
        invoer = f'<textarea id="f-{it.id}" name="{MAILNAAM[it.id]}" rows="4"{_attrs(ctx, it, verplicht)}></textarea>'
    elif soort == "select":
        opties = ""
        for regel in it.lijst:
            waarde, _, tekst = regel.partition(" = ")
            if not tekst:
                waarde, tekst = regel, regel
            opties += f'<option value="{ctx.esc(waarde.strip())}">{ctx.esc(tekst.strip())}</option>'
        leeg = f'<option value="">{ctx.esc(it.veld("placeholder") or KIES)}</option>'
        kenmerken = _attrs(ctx, it, verplicht).replace(f' placeholder="{ctx.esc(it.veld("placeholder", ""))}"', "")
        invoer = (f'<span class="b-{NAAM}__keuzelijst"><select id="f-{it.id}" name="{MAILNAAM[it.id]}"{kenmerken}>'
                  f'{leeg}{opties}</select></span>')
    else:
        invoer = f'<input type="{soort}" id="f-{it.id}" name="{MAILNAAM[it.id]}"{extra}{_attrs(ctx, it, verplicht)}>'
    vinkje = _vinkje(ctx, it, "f-" + it.id) if it.id == "datum" else ""
    return f'<div class="{klasse}"><label for="f-{it.id}">{ctx.esc(it.kop)}</label>{invoer}{_hulp(ctx, it)}{vinkje}</div>'


def _velden(ctx, k, variant, drie=False):
    # haakjes en het streepje met een backslash: Chrome leest het patroon met de v-vlag en negeert het anders
    tel = ' autocomplete="tel" inputmode="tel" pattern="[0-9+ \\(\\)\\-]{8,}"'
    naam = _veld(ctx, k.item("naam"), "text", True, ' autocomplete="name"')
    telefoon = _veld(ctx, k.item("telefoon"), "tel", True, tel)
    if drie:
        # naam, telefoon en e-mail naast elkaar, zoals op referentie B; smal worden het er twee en een
        email = _veld(ctx, k.item("email"), "email", True, ' autocomplete="email"')
        persoon = f'<div class="b-{NAAM}__rij b-{NAAM}__rij--drie">{naam}{telefoon}{email}</div>'
    else:
        persoon = (f'<div class="b-{NAAM}__rij">{naam}{telefoon}</div>'
                   + _veld(ctx, k.item("email"), "email", True, ' autocomplete="email"', breed=True))
    if variant == "contact":
        return persoon + _veld(ctx, k.item("bericht"), "textarea", True, breed=True)
    label = (f'<div class="b-{NAAM}__label">' + _adres(ctx, k.item("van"), True) + _adres(ctx, k.item("naar"), False) + "</div>")
    # met het paneel staat Wanneer op een derde en Soort verhuizing op twee derde, gelijk met naam, telefoon en e-mail
    wanneer = (f'<div class="b-{NAAM}__rij{f" b-{NAAM}__rij--wanneer" if drie else ""}">' + _veld(ctx, k.item("datum"), "date", False)
               + _veld(ctx, k.item("dienst"), "select", False) + "</div>")
    return label + wanneer + persoon + _veld(ctx, k.item("opmerkingen"), "textarea", False, breed=True)


def _maat(pad, terugval):
    """Werkelijke afmetingen van een beeldbestand, met een terugval als het niet te lezen is.

    width en height bestaan om de browser de juiste verhouding te geven voordat de CSS geladen is.
    Een vaste maat voor elk beeld doet precies het omgekeerde: het blok kreeg 640x954 mee terwijl
    aanvraag.py er een liggende 720x540 in hangt. De CSS zet beide maten daarna vast, dus je ziet het
    niet, maar de verhouding die de browser vooraf krijgt klopt dan niet.
    PIL is geen harde afhankelijkheid van de build, vandaar de import hier en de terugval.
    """
    try:
        from PIL import Image
        from kit import WORTEL
        with Image.open(WORTEL / pad.lstrip("/")) as im:
            return im.size
    except Exception:
        return terugval


def _onderaan(ctx, team):
    """Onderaan de zijkolom, buiten __zijin: de teamfoto tegen de onderrand van de kolom (/contact/).

    Buiten __zijin en niet erin, want dat blok is sticky en schuift mee terwijl de bezoeker invult;
    de foto hoort juist aan de kolom vast te zitten. b-formulier__zij--team maakt onderin ruimte vrij
    en b-formulier__team legt hem daar neer, allebei in css/blok/formulier.css.
    """
    if not team:
        return ""
    breed, hoog = _maat(team, (900, 462))
    return "\n    " + ctx.beeld(team, "", breed, hoog, klasse=f"b-{NAAM}__team")


def _bovenaan(ctx, beeld):
    """Bovenin de zijkolom: de uitsneefoto van de pagina, als die er is.

    Hier stond ook een tak voor het beeldmerk, van voor de samenvoeging. Die vervalt: merk is nu een
    ja/nee, en het beeldmerk hoort onderaan de zijkolom (zie MERK hieronder), niet bovenaan.
    """
    if not beeld:
        return ""
    breed, hoog = _maat(beeld, (640, 954))
    return ctx.beeld(beeld, "", breed, hoog, klasse=f"b-{NAAM}__beeld")


# Optie merk: het beeldmerk als laatste onderdeel van de zijkolom (/offerte/ tot 28-09-2026, nu figuur). Het staat binnen __zijin, zodat het
# meeloopt met het blok dat tijdens het invullen in beeld blijft. Vormgeving: css/blok/offerte-diepte.css.
MERK = ('<img class="b-formulier__merk" src="/img/logo/dereus-beeldmerk-negatief.svg" alt="" width="1000" height="509" '
        'loading="lazy" decoding="async">')


def _paneel(ctx, k, figuur):
    """Zijkolom met figuur (/contact/ en /offerte/, 28-09-2026): het offerteblok van referentie B in het merkboek.

    Bovenin staat de uitgeknipte medewerker, die boven de kaart uitsteekt; daaronder een Koningsblauw
    paneel met een schuine bovenkant dat over zijn onderlichaam valt, met de kop, de drie vinkjes en de
    belknop. De WhatsApp-knop zet contactlinks() achter de bellink, dus binnen __bellen.
    Vormgeving: het blok "Paneel met figuur" onderaan css/blok/formulier.css.
    """
    if isinstance(figuur, (tuple, list)):   # (pad, breedte, hoogte): de maat staat al vast
        figuur, breed, hoog = figuur
    else:
        breed, hoog = _maat(figuur, (640, 954))
    punten = "".join(f"<li>{ctx.inline(r)}</li>" for r in k.lijst)
    belzin = f'\n        <p class="b-{NAAM}__belzin">{ctx.inline(k.veld("bel-zin"))}</p>' if k.veld("bel-zin") else ""
    return f'''<aside class="b-{NAAM}__zij b-{NAAM}__zij--paneel">
      <div class="b-{NAAM}__beeldvak">{ctx.beeld(figuur, "", breed, hoog, klasse=f"b-{NAAM}__figuur")}</div>
      <div class="b-{NAAM}__paneel">
        <p class="b-{NAAM}__zijkop">{ctx.inline(k.veld("zij-kop"))}</p>
        <ul class="b-{NAAM}__punten">{punten}</ul>{belzin}
        <div class="b-{NAAM}__bellen"><a class="b-{NAAM}__tel" href="{ctx.telhref}"><span class="b-{NAAM}__telico">{TELEFOON_SVG}</span><span>{ctx.esc(ctx.tel)}</span></a></div>
      </div>
    </aside>'''


def _zijkolom(ctx, k, beeld=None, merk=False, team=None, figuur=None):
    if not k.veld("zij-kop"):
        return ""
    if figuur:
        return _paneel(ctx, k, figuur)
    vinkjes = "".join(f"<li>{ctx.inline(r)}</li>" for r in k.lijst)
    variant = f" b-{NAAM}__zij--team" if team else ""
    tekst = f'''<p class="b-{NAAM}__zijkop">{ctx.inline(k.veld("zij-kop"))}</p>
      <ul class="b-{NAAM}__vinkjes">{vinkjes}</ul>
      <a class="b-{NAAM}__tel" href="{ctx.telhref}">{TELEFOON_SVG}<span>{ctx.esc(ctx.tel)}</span></a>
      {MERK if merk else ""}'''
    if beeld:
        # Sinds 28-09-2026 steekt de uitsnede boven de kaart uit (section-library quote-block-form): het
        # podium draagt het beeld, het paneel de tekst en valt met zijn schuine bovenkant over de benen.
        tekst = (f'<div class="b-{NAAM}__podium">{_bovenaan(ctx, beeld)}</div>\n'
                 f'      <div class="b-{NAAM}__paneel">{tekst}</div>')
    return f'''<aside class="b-{NAAM}__zij{variant}"><div class="b-{NAAM}__zijin">
      {tekst}
    </div>{_onderaan(ctx, team)}</aside>'''


def html(ctx, kopij, **opties) -> str:
    variant = opties.get("variant", "offerte")
    v = VARIANTEN[variant]
    k = kopij
    sid = opties.get("id", k.id)
    grond = opties.get("grond", "mist")
    sleutel = getattr(ctx.cfg, "WEB3FORMS_KEY", "")
    zonder_sleutel = _is_placeholder(sleutel)
    figuur = opties.get("figuur")
    zij = (_zijkolom(ctx, k, opties.get("beeld"), opties.get("merk", False), opties.get("team"), figuur)
           if opties.get("zijkolom", True) else "")
    paneel = bool(figuur and zij)
    # met het paneel: de knop met een pijl, zoals op referentie B
    pijl = ctx.icoon("pijl") if paneel else ""
    prefix = ctx.esc(opties.get("prefix", "f"))
    bereik = (f'<a href="{ctx.telhref}">{ctx.esc(ctx.tel)}</a> <span aria-hidden="true">·</span> '
              f'<a href="mailto:{ctx.esc(ctx.mail)}">{ctx.esc(ctx.mail)}</a>')
    html = f'''<section class="b-{NAAM} b-{NAAM}--{variant}{f" b-{NAAM}--paneel" if paneel else ""} sectie sectie--{grond}" id="{sid}" aria-labelledby="{sid}-kop" data-b="{NAAM}">
      <div class="wrap">
        <div class="b-{NAAM}__kaart{"" if zij else " b-" + NAAM + "__kaart--smal"}{" b-" + NAAM + "__kaart--beeld" if zij and opties.get("beeld") else ""}">
          {zij}
          <div class="b-{NAAM}__hoofd">
            <h2 class="b-{NAAM}__kop" id="{sid}-kop">{ctx.inline(k.kop)}</h2>
            <form class="b-{NAAM}__form" action="{EINDPUNT}" method="POST" data-formulier="{variant}" data-prefix="{prefix}" data-bedankt="{v["bedankt"]}"
              data-bezig="{ctx.esc(k.veld("bezig", ""))}"{' data-zonder-sleutel' if zonder_sleutel else ''}>
              <input type="hidden" name="access_key" value="{"" if zonder_sleutel else ctx.esc(sleutel)}">
              <input type="hidden" name="subject" value="{v["onderwerp"]}">
              <input type="hidden" name="from_name" value="{v["afzender"]}">
              <input type="hidden" name="redirect" value="{ctx.cfg.DOMEIN}{v["bedankt"]}">
              <label class="b-{NAAM}__hp" aria-hidden="true"><input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off"></label>
              {_velden(ctx, k, variant, drie=paneel)}
              <div class="b-{NAAM}__foutlijst" role="alert" tabindex="-1" hidden>
                <p>{ctx.inline(k.veld("fout-kop"))}</p>
                <ul></ul>
              </div>
              <p class="b-{NAAM}__fout" role="alert" hidden>{ctx.inline(k.veld("fout-versturen"))} <span class="b-{NAAM}__bereik">{bereik}</span></p>
              <div class="b-{NAAM}__acties">
                <button class="knop knop--cta" type="submit">{ctx.esc(k.veld("knop"))}{pijl}</button>
                <p class="b-{NAAM}__privacy">{ctx.inline(k.veld("privacy"))}</p>
              </div>
            </form>
          </div>
        </div>
      </div>
    </section>'''
    # Beide formulieren kunnen op de home staan. Elk krijgt eigen id's en labelverwijzingen.
    return html.replace('="f-', f'="{prefix}-')
