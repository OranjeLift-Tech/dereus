"""Contactband (/over-ons/ #contact, en elke pagina die met "Kennismaken?" afsluit): een witte kaart op
Mist met links de kop, de tekst en de knoppen, rechts een Diepblauw paneel met telefoon, e-mail, adres,
openingstijden en de live bereikbaarheid. Licht van buiten, dus mag direct boven de footer.
Velden: label, kop, alinea's, knop (CTA-knop naar /offerte/), belregel.
De belregel staat in de witte kaart zonder WhatsApp-knop (belregel(whatsapp=False)): het
Diepblauwe paneel ernaast heeft er al een, direct onder het grote nummer, en de gebruiker vroeg de
linker weg te halen. Tot 23-09-2026 kon dat niet, omdat controle-layout.cjs naast elk nummer een
WhatsApp-knop eiste; toen is de hele regel met het nummer eruit gegaan. Sinds die eis een richtlijn
is, staat de regel terug en valt alleen de knop weg. Hij staat in de knoppenrij, naast de
offerteknop, zodat de band er waar het past geen regel hoger van wordt (de band is op verzoek krap).
Optie beeld: (pad, bestand_breed, bestand_hoog, x, y, w, h) zet een uitsnede rechtsonder in de
kaart, op een effen lichte plaat waar de figuur boven- en onderlangs overheen valt. De laatste vier
getallen zijn het deel van het bestand dat zichtbaar moet zijn (alfa-bbox); zie css/blok/uitsnede.css
voor hoe je die meet. Een andere uitsnede is dus die ene regel op de pagina, verder niets.
De pagina moet extra_css=("uitsnede",) hebben. Zonder de optie blijft de band zoals hij is.
Optie compact: "gematigd" of "krap" zet de band, de kaart en het paneel strakker; de maten
staan bovenin css/blok/contactband.css.
"""
import navigatie

NAAM = "contactband"
CSS = True
JS = False


def html(ctx, kopij, sectie="mist", compact=None, **opties):
    k = kopij
    cfg = ctx.cfg
    knoppen = []
    if k.veld("knop"):
        knoppen.append(ctx.knop(k.veld("knop"), "/offerte/"))
    tijden = "".join(f"<li>{ctx.esc(r)}</li>" for r in navigatie.tijden_regels())
    uit = ""
    if opties.get("beeld"):
        src, breed, hoog, ux, uy, uw, uh = opties["beeld"]
        # alt leeg: de uitsnede illustreert de tekst ernaast en voegt er niets aan toe
        beeld = ctx.beeld(src, "", breed, hoog, klasse="uitsnede__beeld cband__uit")
        maten = f"--uit-breed:{breed};--uit-hoog:{hoog};--uit-x:{ux};--uit-y:{uy};--uit-w:{uw};--uit-h:{uh}"
        uit = f'<div class="uitsnede cband__figuur" style="{maten}">{beeld}</div>' 
    if compact and compact not in ("gematigd", "krap"):
        raise ValueError(f"contactband: compact is 'gematigd' of 'krap', niet {compact!r}")
    klassen = "sectie sectie--" + sectie + " b-contactband"
    if compact:
        klassen += f" b-contactband--{compact}"
    return f'''<section class="{klassen}" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap">
    <div class="cband{" cband--beeld" if uit else ""}" data-reveal>
      <div class="cband__tekst">
        {ctx.kopgroep(k)}
        {ctx.alineas(k.tekst)}
        <div class="knoppen">{"".join(knoppen)}{ctx.belregel(k.veld("belregel"), whatsapp=False)}</div>
        {uit}
      </div>
      <div class="cband__paneel">
        {ctx.bereikbaar("bereikbaar cband__status")}
        <a class="cband__tel" href="{cfg.TELHREF}">{ctx.icoon("telefoon")}<span>{cfg.TEL}</span></a>
        <a class="cband__mail" href="mailto:{cfg.MAIL}">{ctx.icoon("mail")}<span>{cfg.MAIL}</span></a>
        <address class="cband__adres">{ctx.icoon("pin")}<span>{ctx.esc(cfg.STRAAT)}<br>{ctx.esc(cfg.POSTCODE)} {ctx.esc(cfg.PLAATS)}</span></address>
        <div class="cband__tijden">{ctx.icoon("klok")}<ul>{tijden}</ul></div>
      </div>
    </div>
  </div>
</section>'''
