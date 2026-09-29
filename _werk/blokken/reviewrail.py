"""Reviews als rail met een scorepodium (/werkwijze/, #reviews "Zo gaat het in de praktijk").

Gevraagd op 28-09-2026: het reviewblok van referentie B (_blokken/reviews.html + assets/css/blokken/reviews.css,
klassen sgr__) in de huisstijl van De Reus. Links het podium: twee verschoven platen (Koningsblauw naar Diepblauw
achter, blauw 50/100 ervoor), een verhuizer die er bovenuit steekt en een witte schijf met de Google-score en
een Koningsblauwe ring. Daaronder de knop naar het Google-profiel. Rechts de reviews als rail die tot de
schermrand doorloopt, met knoppen en een voortgangsbalk (js/blok/reviewrail.js). Zonder JS scrollt de rail
gewoon en staat elke tekst er helemaal.

Anders dan bij referentie B: geen foto's van klanten (die zijn er niet; namen letterlijk, avatars als
initialen, zie reviews.py) en geen datum (Google-periodes zijn niet vastgelegd). De ring tekent zich niet:
de site staat stil, alleen de rail schuift op een klik.

Kopij: kop, label en intro van de eigen pagina; de reviews zelf uit home.md {#reviews}, zoals bij reviews.py.
Optie accent: een stuk van de kop dat de gele streep krijgt, zoals het groene woord bij referentie B.
"""
NAAM = "reviewrail"
CSS = True
JS = True

AVATAR = ["a", "b", "c", "d"]

# De verhuizer op het podium: de uitsnede met de doos op de schouder. De CSS toont hem tot halverwege het
# bovenbeen (--snede in reviewrail.css), de rest valt weg onder de rand van het podium.
FIGUUR = ("/img/verhuizer-doos-schouder-uit.webp", 489, 1200)


def _cijfer(score):
    """'4,9' -> 4.9; bij iets onleesbaars de volle vijf, zodat de ring nooit leeg staat."""
    try:
        return max(0.0, min(5.0, float(str(score).replace(",", "."))))
    except ValueError:
        return 5.0


def _kaart(ctx, it, i, initialen):
    naam = it.titel
    return f'''<li class="b-reviewrail__kaart">
          <p class="b-reviewrail__cijfer"><span class="vh">5 van de 5 sterren</span>{ctx.sterren(5, klasse="sterren b-reviewrail__sterren")}</p>
          <blockquote class="b-reviewrail__tekst"><p>{ctx.esc(it.veld("tekst"))}</p></blockquote>
          <p class="b-reviewrail__wie"><span class="b-reviewrail__avatar b-reviewrail__avatar--{AVATAR[i % len(AVATAR)]}" aria-hidden="true">{ctx.esc(initialen(naam))}</span><span><b>{ctx.esc(naam)}</b><small>{ctx.icoon("google", "ic ic--google")}Review op Google</small></span></p>
        </li>'''


def html(ctx, kopij, sectie="wit", accent="", **opties):
    k = kopij
    home = ctx.kopij_van("home").blok_of_leeg("reviews")
    items = list(k.items) if k.items else list(home.items)      # eigen reviews van de pagina gaan voor
    uit = [it for it in items if it.veld("uitgelicht").lower() in ("ja", "true", "1")]
    volgorde = uit + [it for it in items if it not in uit]
    initialen = ctx.register["reviews"].initialen
    kid = ctx.esc(k.id or "reviews")

    kop = ctx.kopgroep(k, klasse="b-reviewrail__kop")
    if accent:
        a = ctx.esc(accent)
        kop = kop.replace(f"{a}</h2>", f"<em>{a}</em></h2>", 1)

    score = ctx.cfg.GOOGLE_SCORE
    ring = round(_cijfer(score) / 5 * 100, 1)
    link = home.veld("profiel-linktekst", "Bekijk alle reviews op Google")
    src, b, h = FIGUUR
    persoon = ctx.beeld(src, "", b, h)
    kaarten = "".join(_kaart(ctx, it, i, initialen) for i, it in enumerate(volgorde))
    pijl = ctx.icoon("pijl")

    return f'''<section class="sectie sectie--{sectie} b-reviewrail" id="{kid}" aria-labelledby="{kid}-kop">
  <div class="wrap b-reviewrail__in">
    {kop}
    <div class="b-reviewrail__score">
      <div class="b-reviewrail__podium">
        <span class="b-reviewrail__stapel" aria-hidden="true"></span>
        <span class="b-reviewrail__persoon" aria-hidden="true">{persoon}</span>
        <div class="b-reviewrail__boog">
          <svg class="b-reviewrail__ring" viewBox="0 0 120 120" aria-hidden="true" focusable="false"><circle cx="60" cy="60" r="54" pathLength="100" stroke-dasharray="{ring:g} 100"/></svg>
          <p class="b-reviewrail__getal"><span class="vh">{score} van de 5 sterren op Google</span><span aria-hidden="true"><b>{score}</b>{ctx.sterren(klasse="sterren b-reviewrail__gemiddeld")}</span></p>
        </div>
      </div>
      <a class="b-reviewrail__profiel" href="{ctx.esc(ctx.cfg.GOOGLE_PROFIEL)}" rel="noopener" target="_blank">{ctx.icoon("google", "ic ic--google")}<span>{ctx.inline(link)}</span>{ctx.icoon("extern")}<span class="vh"> (opent Google in een nieuw tabblad)</span></a>
    </div>
    <div class="b-reviewrail__rail">
      <ul class="b-reviewrail__kaarten" role="list" tabindex="0" aria-label="Reviews van klanten, letterlijk van Google">
        {kaarten}
      </ul>
      <div class="b-reviewrail__nav" hidden>
        <button type="button" class="b-reviewrail__knop b-reviewrail__knop--terug" aria-label="Vorige reviews">{pijl}</button>
        <span class="b-reviewrail__voortgang" aria-hidden="true"><i></i></span>
        <button type="button" class="b-reviewrail__knop b-reviewrail__knop--verder" aria-label="Volgende reviews">{pijl}</button>
      </div>
    </div>
  </div>
</section>'''
