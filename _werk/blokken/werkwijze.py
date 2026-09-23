"""Werkwijze optie 5: vijf uitklapbare stappen links, het bijbehorende beeld rechts."""
NAAM = "werkwijze"
CSS = True
JS = True

FOTOS = [
    "stap-1-laptop.webp", "stap-2-contact.webp", "stap-3-offerte.webp",
    "stap-4-planning.webp", "stap-5-bank-voordeur.webp",
]


def html(ctx, kopij, **opties):
    k = kopij
    stappen, beelden = [], []
    for i, it in enumerate(k.items, 1):
        sid = it.id or f"{k.id}-stap-{i}"
        foto = f"/img/{FOTOS[(i - 1) % len(FOTOS)]}"
        titel = ctx.inline(it.titel)
        stappen.append(f'''<li id="{ctx.esc(sid)}">
        <details class="werkwijze__stap"{' open' if i == 1 else ''}>
          <summary id="{ctx.esc(sid)}-knop" aria-controls="{ctx.esc(sid)}-inhoud">
            <span class="werkwijze__nummer" aria-hidden="true">{i:02d}</span>
            <h3><span class="vh">Stap {i}: </span>{titel}</h3>
            <span class="werkwijze__plus" aria-hidden="true">{ctx.icoon("plus")}</span>
          </summary>
          <div class="werkwijze__antwoord" id="{ctx.esc(sid)}-inhoud">
            <div class="werkwijze__antwoord-in">
              <p>{ctx.inline(it.veld("tekst"))}</p>
              <div class="werkwijze__mobielbeeld">{ctx.beeld(foto, "", 560, 380)}</div>
            </div>
          </div>
        </details>
      </li>''')
        beelden.append(f'''<div class="werkwijze__beeldlaag{' is-actief' if i == 1 else ''}" data-stap-beeld="{i - 1}">
          {ctx.beeld(foto, "", 560, 380)}
          <p class="werkwijze__bijschrift">{i:02d} · {titel}</p>
        </div>''')
    knoppen = []
    if k.veld("knop"):
        knoppen.append(ctx.knop(k.veld("knop"), "/offerte/"))
    if k.veld("linktekst"):
        knoppen.append(ctx.knop(k.veld("linktekst"), k.veld("link", "/kosten/"), soort="licht"))
    return f'''<section class="sectie sectie--mist b-werkwijze" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap">
    {ctx.kopgroep(k, "kopgroep--midden")}
    <div class="werkwijze" data-werkwijze>
      <ol class="werkwijze__stappen" role="list">{"".join(stappen)}</ol>
      <div class="werkwijze__beeld" aria-hidden="true">{"".join(beelden)}<span class="beeldaccent werkwijze__accent" aria-hidden="true"></span></div>
    </div>
    {f'<div class="knoppen knoppen--midden">{"".join(knoppen)}</div>' if knoppen else ""}
  </div>
</section>'''
