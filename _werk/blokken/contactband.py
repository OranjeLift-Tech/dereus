"""Contactband (/over-ons/ #contact, en elke pagina die met "Kennismaken?" afsluit): een witte kaart op
Mist met links de kop, de tekst en de knoppen, rechts een Diepblauw paneel met telefoon, e-mail, adres,
openingstijden en de live bereikbaarheid. Licht van buiten, dus mag direct boven de footer.
Velden: label, kop, alinea's, knop (CTA-knop naar /offerte/), belregel.
Optie beeld: ("/img/...-uit.webp", breedte, hoogte) zet een staande uitsnede naast de tekst, met de
voeten op de onderrand van de kaart. Zonder die optie blijft de band zoals hij is.
"""
import navigatie

NAAM = "contactband"
CSS = True
JS = False


def html(ctx, kopij, sectie="mist", **opties):
    k = kopij
    cfg = ctx.cfg
    knoppen = []
    if k.veld("knop"):
        knoppen.append(ctx.knop(k.veld("knop"), "/offerte/"))
    tijden = "".join(f"<li>{ctx.esc(r)}</li>" for r in navigatie.tijden_regels())
    uit = ""
    if opties.get("beeld"):
        src, breed, hoog = opties["beeld"]
        uit = ctx.beeld(src, "", breed, hoog, klasse="cband__uit")
    return f'''<section class="sectie sectie--{sectie} b-contactband" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap">
    <div class="cband{" cband--beeld" if uit else ""}" data-reveal>
      <div class="cband__tekst">
        {ctx.kopgroep(k)}
        {ctx.alineas(k.tekst)}
        <div class="knoppen">{"".join(knoppen)}</div>
        {ctx.belregel(k.veld("belregel"))}{uit}
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
