"""Het gedeelde formulier: offerteaanvraag (/offerte/) en contactbericht (/contact/).

Opties: variant = "offerte" of "contact"; id (standaard "formulier"); beeld = pad naar een uitsneefoto
bovenin de zijkolom; merk = naam van een logovariant, als er nog geen eigen foto is.
Kopij: het blok {#formulier} van de pagina. Blokvelden: knop, privacy, fout-kop, fout-versturen, bezig,
zij-kop en lijst (de drie vinkjes in de zijkolom; zonder zij-kop vervalt de zijkolom).
Per veld een ###-item met de veldnaam als id: de titel is het label, met hulp, placeholder, fout,
fout-onjuist en onbekend (het vinkje naast Naar en Wanneer). Bij dienst is de lijst de keuzelijst,
in de vorm "- particulier = Particuliere verhuizing".

Het formulier werkt zonder JavaScript (gewone POST naar Web3Forms). Met JavaScript: invullen vanuit het
adres (?van=&naar=&datum=&dienst=), adressuggesties van PDOK, een foutoverzicht en doorsturen naar de
bedanktpagina. Zie js/blok/formulier.js.
"""

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

TELEFOON_SVG = ('<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" '
                'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M22 16.92v3a2 2 0 0 1-2.18 '
                '2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 '
                '1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>')


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


def _velden(ctx, k, variant):
    # haakjes en het streepje met een backslash: Chrome leest het patroon met de v-vlag en negeert het anders
    tel = ' autocomplete="tel" inputmode="tel" pattern="[0-9+ \\(\\)\\-]{8,}"'
    persoon = (f'<div class="b-{NAAM}__rij">'
               + _veld(ctx, k.item("naam"), "text", True, ' autocomplete="name"')
               + _veld(ctx, k.item("telefoon"), "tel", True, tel) + "</div>"
               + _veld(ctx, k.item("email"), "email", True, ' autocomplete="email"', breed=True))
    if variant == "contact":
        return persoon + _veld(ctx, k.item("bericht"), "textarea", True, breed=True)
    label = (f'<div class="b-{NAAM}__label">' + _adres(ctx, k.item("van"), True) + _adres(ctx, k.item("naar"), False) + "</div>")
    wanneer = (f'<div class="b-{NAAM}__rij">' + _veld(ctx, k.item("datum"), "date", False)
               + _veld(ctx, k.item("dienst"), "select", False) + "</div>")
    return label + wanneer + persoon + _veld(ctx, k.item("opmerkingen"), "textarea", False, breed=True)


def _bovenaan(ctx, beeld, merk):
    """Bovenin de zijkolom: een uitsneefoto (beeld) of het beeldmerk (merk), voor pagina's zonder eigen foto."""
    if beeld:
        return ctx.beeld(beeld, "", 640, 954, klasse=f"b-{NAAM}__beeld")
    if merk:
        breed, hoog = ctx.cfg.LOGO_MATEN["beeldmerk"]
        return ctx.beeld(ctx.logo(merk), "", breed, hoog, klasse=f"b-{NAAM}__merk")
    return ""


def _zijkolom(ctx, k, beeld=None, merk=None):
    if not k.veld("zij-kop"):
        return ""
    vinkjes = "".join(f"<li>{ctx.inline(r)}</li>" for r in k.lijst)
    return f'''<aside class="b-{NAAM}__zij"><div class="b-{NAAM}__zijin">
      {_bovenaan(ctx, beeld, merk)}
      <p class="b-{NAAM}__zijkop">{ctx.inline(k.veld("zij-kop"))}</p>
      <ul class="b-{NAAM}__vinkjes">{vinkjes}</ul>
      <a class="b-{NAAM}__tel" href="{ctx.telhref}">{TELEFOON_SVG}<span>{ctx.esc(ctx.tel)}</span></a>
    </div></aside>'''


def html(ctx, kopij, **opties) -> str:
    variant = opties.get("variant", "offerte")
    v = VARIANTEN[variant]
    k = kopij
    sid = opties.get("id", k.id)
    sleutel = getattr(ctx.cfg, "WEB3FORMS_KEY", "")
    zonder_sleutel = _is_placeholder(sleutel)
    zij = _zijkolom(ctx, k, opties.get("beeld"), opties.get("merk")) if opties.get("zijkolom", True) else ""
    prefix = ctx.esc(opties.get("prefix", "f"))
    bereik = (f'<a href="{ctx.telhref}">{ctx.esc(ctx.tel)}</a> <span aria-hidden="true">·</span> '
              f'<a href="mailto:{ctx.esc(ctx.mail)}">{ctx.esc(ctx.mail)}</a>')
    html = f'''<section class="b-{NAAM} b-{NAAM}--{variant} sectie sectie--mist" id="{sid}" aria-labelledby="{sid}-kop" data-b="{NAAM}">
      <div class="wrap">
        <div class="b-{NAAM}__kaart{"" if zij else " b-" + NAAM + "__kaart--smal"}">
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
              {_velden(ctx, k, variant)}
              <div class="b-{NAAM}__foutlijst" role="alert" tabindex="-1" hidden>
                <p>{ctx.inline(k.veld("fout-kop"))}</p>
                <ul></ul>
              </div>
              <p class="b-{NAAM}__fout" role="alert" hidden>{ctx.inline(k.veld("fout-versturen"))} <span class="b-{NAAM}__bereik">{bereik}</span></p>
              <div class="b-{NAAM}__acties">
                <button class="knop knop--cta" type="submit">{ctx.esc(k.veld("knop"))}</button>
                <p class="b-{NAAM}__privacy">{ctx.inline(k.veld("privacy"))}</p>
              </div>
            </form>
          </div>
        </div>
      </div>
    </section>'''
    # Beide formulieren kunnen op de home staan. Elk krijgt eigen id's en labelverwijzingen.
    return html.replace('="f-', f'="{prefix}-')
