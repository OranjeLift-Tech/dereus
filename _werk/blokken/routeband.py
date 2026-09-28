"""Zo werkt het op de home (#werkwijze): de inleiding op de Koningsblauwe band met dakrand naast een foto
van de ploeg bij de wagen met een losse verhuizer die erboven uitstapt, en de stappen als witte band die
de onderrand van foto en verhuizer afdekt. Naar het patroon intro-route-band uit ../section-library
(samengesteld voor De Bresser, 25-09-2026), de versie die de gebruiker op 28-09-2026 uit vijf hield
(website/review/zo-werkt-het-20260928/, versie 5). Vervangt het blok werkwijze (de uitklapbare stappen)
op de home; dat blok en zijn CSS blijven staan.

Kopij: een blok met label, kop, intro, knop (naar /offerte/), linktekst en link, en 3 tot 6 stappen als
###-items met een tekst:-veld. De stappen komen er letterlijk in; het item-id wordt het id van de stap.
Opties foto en uitsnede: (pad, breedte, hoogte). De foto is liggend en wordt 16:10 getoond. De uitsnede
is een losse verhuizer zonder achtergrond, strak uitgesneden (hoofd tegen de bovenrand, voeten tegen de
onderrand), want het blok zet zijn hoofd tegen de bovenkant van het beeldvak en laat de band zijn voeten
afdekken. Zie css/blok/routeband.css.
"""
NAAM = "routeband"
CSS = True
JS = False

# De ploeg bij de wagen (live als kop van /diensten/) en een verhuizer met twee dozen (live op /kosten/
# en /over-ons/). Allebei staan ze nog niet op de home; het team uit de hero staat daar al bovenaan.
FOTO = ("/img/headers/diensten.webp", 1600, 900)
UITSNEDE = ("/img/verhuizer-twee-dozen-uit.webp", 407, 1200)


def html(ctx, kopij, foto=FOTO, uitsnede=UITSNEDE, **opties):
    k = kopij
    if not 3 <= len(k.items) <= 6:
        raise ValueError(f"routeband: 3 tot 6 stappen, niet {len(k.items)}")
    stappen = []
    for i, it in enumerate(k.items, 1):
        sid = it.id or f"{k.id}-stap-{i}"
        stappen.append(f'''<li id="{ctx.esc(sid)}">
          <h3><span class="vh">Stap {i}: </span><span class="rb__titel">{ctx.inline(it.titel)}</span></h3>
          <p>{ctx.inline(it.veld("tekst"))}</p>
        </li>''')
    knoppen = []
    if k.veld("knop"):
        knoppen.append(ctx.knop(k.veld("knop"), "/offerte/"))
    if k.veld("linktekst"):
        knoppen.append(ctx.knop(k.veld("linktekst"), k.veld("link", "/werkwijze/"), soort="licht"))
    (fsrc, fb, fh), (usrc, ub, uh) = foto, uitsnede
    # alt leeg en het vak aria-hidden: foto en verhuizer illustreren de stappen en voegen er niets aan toe
    return f'''<section class="sectie sectie--blauw b-routeband" id="{ctx.esc(k.id)}" aria-labelledby="{ctx.esc(k.id)}-kop">
  <div class="wrap">
    <div class="rb">
      <div class="rb__tekst">{ctx.kopgroep(k)}</div>
      {f'<div class="knoppen rb__knoppen">{"".join(knoppen)}</div>' if knoppen else ""}
      <div class="rb__beeld" aria-hidden="true">
        <span class="rb__blok"></span>
        {ctx.beeld(fsrc, "", fb, fh, klasse="rb__foto")}
        {ctx.beeld(usrc, "", ub, uh, klasse="rb__uit")}
      </div>
      <div class="rb__band">
        <ol class="rb__stappen" role="list" data-reveal-groep>
        {"".join(stappen)}
        </ol>
      </div>
    </div>
  </div>
</section>'''
