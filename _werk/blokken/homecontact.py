"""Contact uit main: één gegevenskaart met de kaart van Den Haag, en het berichtformulier onder een foto."""

NAAM = "homecontact"
CSS = True
JS = False
AFHANKELIJK = ["formulier", "wereld"]


def _kanalen(ctx, k):
    """Bellen (met WhatsApp er direct achter, zodat ctx.contactlinks er geen tweede bij zet),
    mailen en de bereikbaarheid, als drie rijen in één kaart."""
    c = ctx.cfg
    tijden = "".join(f'<li><span>{ctx.esc(t["kort"])}</span><span>{ctx.esc(t["van"])} tot {ctx.esc(t["tot"])} uur</span></li>'
                     for t in c.TIJDEN)
    return f'''<ul class="homecontact__kanalen" role="list">
              <li class="homecontact__kanaal">
                <span class="homecontact__ic" aria-hidden="true">{ctx.icoon('telefoon')}</span>
                <div class="homecontact__in">
                  <p class="homecontact__lbl">Bellen</p>
                  <a class="homecontact__nummer" href="{c.TELHREF}">{ctx.esc(c.TEL)}</a>{ctx.whatsapp(klasse="wa-link homecontact__wa")}
                </div>
              </li>
              <li class="homecontact__kanaal">
                <span class="homecontact__ic" aria-hidden="true">{ctx.icoon('mail')}</span>
                <div class="homecontact__in">
                  <p class="homecontact__lbl">Mailen</p>
                  <a class="homecontact__waarde" href="mailto:{c.MAIL}">{ctx.esc(c.MAIL)}</a>
                </div>
              </li>
              <li class="homecontact__kanaal">
                <span class="homecontact__ic" aria-hidden="true">{ctx.icoon('klok')}</span>
                <div class="homecontact__in">
                  <h3 class="homecontact__lbl">{ctx.esc(k.veld('tijden-kop'))}</h3>
                  <ul class="homecontact__tijden" role="list">{tijden}</ul>
                  {ctx.bereikbaar()}
                </div>
              </li>
            </ul>'''


def html(ctx, kopij, **opties):
    k = kopij
    c = ctx.cfg
    formulier = ctx.register["formulier"].html(
        ctx, ctx.kopij_van("contact").blok("formulier"),
        variant="contact", id="contact-formulier", prefix="bericht", zijkolom=False,
    )
    # De kaart gebruikt deze symbolen nadat de bezoeker de interactieve weergave opent.
    for icoon in ("pin", "wereld"):
        ctx.icoon(icoon)
    return f'''<section class="sectie sectie--wit b-homecontact" id="{k.id}" aria-labelledby="{k.id}-kop">
      <div class="wrap">
        {ctx.kopgroep(k, "kopgroep--midden")}
        <div class="homecontact">
          <div class="homecontact__gegevens">
            {_kanalen(ctx, k)}
            <div class="homecontact__plek">
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
            </div>
          </div>
          <div class="homecontact__bericht">
            <div class="homecontact__kaart">
              <div class="homecontact__beeld" aria-hidden="true">
                {ctx.beeld('/img/contact-klantenservice.webp', '', 1200, 800, klasse='homecontact__achter')}
                {ctx.beeld('/img/contact-uit.webp', '', 1200, 800, klasse='homecontact__uit')}
              </div>
              {formulier}
            </div>
          </div>
        </div>
      </div>
    </section>'''
