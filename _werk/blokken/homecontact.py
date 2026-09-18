"""Contact uit main: adreskaart, klantenservicebeeld en het gedeelde contactformulier."""
import navigatie

NAAM = "homecontact"
CSS = True
JS = False
AFHANKELIJK = ["formulier", "wereld"]


def html(ctx, kopij, **opties):
    k = kopij
    c = ctx.cfg
    formulier = ctx.register["formulier"].html(
        ctx, ctx.kopij_van("contact").blok("formulier"),
        variant="contact", id="contact-formulier", prefix="bericht", zijkolom=False,
    )
    tijden = "".join(f"<li>{ctx.esc(r)}</li>" for r in navigatie.tijden_regels())
    # De kaart gebruikt deze symbolen nadat de bezoeker de interactieve weergave opent.
    for icoon in ("pin", "wereld"):
        ctx.icoon(icoon)
    return f'''<section class="sectie sectie--wit b-homecontact" id="{k.id}" aria-labelledby="{k.id}-kop">
      <div class="wrap">
        {ctx.kopgroep(k, "kopgroep--midden")}
        <div class="homecontact">
          <div class="homecontact__gegevens">
            <div class="wereld" data-wereld data-lat="{c.GEO[0]}" data-lng="{c.GEO[1]}">
              {ctx.beeld('/img/kaart-den-haag.svg', 'Kaart van Den Haag', 1400, 933, klasse='wereld__terugval')}
              <button class="wereld__start knop knop--licht" type="button" data-wereld-start>{ctx.icoon('wereld')}{ctx.esc(k.veld('kaart-knop'))}</button>
              <p class="wereld__melding vh" role="status" data-wereld-melding></p>
              <div class="wereld__info"><span class="wereld__ic">{ctx.icoon('pin')}</span><div>
                <address class="wereld__adres">{ctx.esc(c.STRAAT)}<br>{ctx.esc(c.POSTCODE)} {ctx.esc(c.PLAATS)}</address>
                <a class="wereld__route" href="{c.ROUTE}" rel="noopener">{ctx.esc(k.veld('route'))}{ctx.icoon('pijl')}</a>
              </div></div>
            </div>
            <p class="homecontact__bron">Kaartgegevens: <a href="https://www.openstreetmap.org/copyright">OpenStreetMap-bijdragers</a>.</p>
            <div class="homecontact__kanalen">
              <a href="{c.TELHREF}">{ctx.icoon('telefoon')}<span>{c.TEL}</span></a>
              <a href="mailto:{c.MAIL}">{ctx.icoon('mail')}<span>{c.MAIL}</span></a>
            </div>
            <h3>{ctx.esc(k.veld('tijden-kop'))}</h3><ul class="homecontact__tijden">{tijden}</ul>
            {ctx.bereikbaar()}
          </div>
          <div class="homecontact__bericht">
            <div class="homecontact__beeld" aria-hidden="true">
              {ctx.beeld('/img/contact-klantenservice.webp', '', 1200, 800, klasse='homecontact__achter')}
              {ctx.beeld('/img/contact-uit.webp', '', 1200, 800, klasse='homecontact__uit')}
            </div>
            {formulier}
          </div>
        </div>
      </div>
    </section>'''
