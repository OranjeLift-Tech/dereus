"""Vijf fototreden op weg naar het nieuwe huis, met de bestaande werkwijze-kopij."""
NAAM = "werkwijze"
CSS = True
JS = True

FOTOS = [
    "stap-1-formulier.webp",
    "stap-2-bellen.webp",
    "stap-3-offerte.webp",
    "stap-4-planning.webp",
    "stap-5-verhuisdag.webp",
]


def html(ctx, kopij, **opties):
    k = kopij
    stappen = []
    for i, it in enumerate(k.items, 1):
        foto = FOTOS[(i - 1) % len(FOTOS)]
        stappen.append(f'''<li class="verhuistrap__trede" id="{ctx.esc(it.id)}">
        <div class="verhuistrap__kaart" data-reveal>
          <div class="verhuistrap__stapfoto"><img src="/img/{foto}" alt="" width="560" height="380" loading="lazy" decoding="async"></div>
          <span class="verhuistrap__nr" aria-hidden="true">{i}</span>
          <div class="verhuistrap__tekst">
            <h3><span class="vh">Stap {i}: </span>{ctx.inline(it.titel)}</h3>
            <p>{ctx.inline(it.veld("tekst"))}</p>
          </div>
        </div>
      </li>''')
    knoppen = []
    if k.veld("knop"):
        knoppen.append(ctx.knop(k.veld("knop"), "/offerte/"))
    if k.veld("linktekst"):
        knoppen.append(ctx.knop(k.veld("linktekst"), k.veld("link", "/kosten/"), soort="licht"))
    return f'''<section class="sectie sectie--blauw b-werkwijze" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap">
    {ctx.kopgroep(k, "kopgroep--midden")}
    <div class="verhuistrap">
      <ol class="verhuistrap__lijst" role="list">
        {"".join(stappen)}
      </ol>
      <div class="verhuistrap__huis" aria-hidden="true">
        <div class="verhuistrap__huisvorm">
          <div class="verhuistrap__huisfoto"><img src="/img/nieuw-huis.webp" alt="" width="400" height="450" loading="lazy" decoding="async"></div>
          <svg class="verhuistrap__dak" viewBox="0 0 190 214" focusable="false">
            <path d="M5 97 95 15l90 82" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
            <g class="verhuistrap__sleutel"><circle cx="95" cy="-12" r="8" fill="none" stroke="currentColor" stroke-width="4"/><path d="M95 -4v16M95 6h6M95 11h5" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/></g>
          </svg>
        </div>
        <span class="verhuistrap__bestemming">Uw nieuwe huis</span>
      </div>
    </div>
    {f'<div class="knoppen knoppen--midden">{"".join(knoppen)}</div>' if knoppen else ""}
  </div>
</section>'''
