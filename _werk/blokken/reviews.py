"""Reviews (#reviews). De review-items staan altijd in home.md; kop, label en intro komen van de eigen pagina.
Namen letterlijk, avatars als initialen (geen foto's). Nooit een aantal reviews noemen (open vraag 1.4).

Varianten:
  volledig  (home)  scorepaneel in Diepblauw, de uitgelichte review groot, daaronder de andere drie
  compact   (/diensten/)  drie reviews in een rij met de score erboven
Optie sectie: "mist" of "wit" (standaard mist bij volledig, wit bij compact).
"""
import re

NAAM = "reviews"
CSS = True
JS = False

AVATAR = ["a", "b", "c", "d"]


def initialen(naam):
    delen = [d for d in re.split(r"\s+", naam.strip()) if d]
    if not delen:
        return "?"
    if len(delen) == 1:
        return delen[0][:2].upper()
    return (delen[0][0] + delen[-1][0]).upper()


def kaart(ctx, it, i, groot=False):
    naam = it.titel
    tekst = it.veld("tekst")
    klasse = "rkaart rkaart--groot" if groot else "rkaart"
    return f'''<li class="{klasse}">
        <figure>
          <div class="rkaart__kop">{ctx.sterren(5)}<span class="vh">5 van 5 sterren</span>{ctx.icoon("quote", "ic rkaart__quote")}</div>
          <blockquote><p>{ctx.esc(tekst)}</p></blockquote>
          <figcaption class="rkaart__wie">
            <span class="avatar avatar--{AVATAR[i % len(AVATAR)]}" aria-hidden="true">{ctx.esc(initialen(naam))}</span>
            <span><b>{ctx.esc(naam)}</b><small>{ctx.icoon("google", "ic ic--google")}Review op Google</small></span>
          </figcaption>
        </figure>
      </li>'''


def paneel(ctx, home_blok, eigen):
    score_tekst = eigen.veld("score-tekst") or home_blok.veld("score-tekst") or ctx.score
    link = eigen.veld("profiel-linktekst") or home_blok.veld("profiel-linktekst", "Bekijk alle reviews op Google")
    return f'''<li class="rpaneel">
        <span class="rpaneel__g">{ctx.icoon("google", "ic ic--google")}</span>
        <p class="rpaneel__score"><b>{ctx.cfg.GOOGLE_SCORE}</b><span>uit 5<small>op Google</small></span></p>
        {ctx.sterren(5, "sterren rpaneel__sterren")}
        {"" if ctx.cfg.GOOGLE_SCORE in score_tekst else f'<p class="rpaneel__tekst">{ctx.inline(score_tekst)}</p>'}
        <a class="knop knop--licht rpaneel__link" href="{ctx.esc(ctx.cfg.GOOGLE_PROFIEL)}" rel="noopener" target="_blank"><span>{ctx.inline(link)}</span>{ctx.icoon("extern")}<span class="vh"> (opent Google in een nieuw tabblad)</span></a>
      </li>'''


def html(ctx, kopij, variant="volledig", sectie=None, **opties):
    k = kopij
    home = ctx.kopij_van("home").blok_of_leeg("reviews")
    items = list(k.items) if k.items else list(home.items)      # eigen reviews van de pagina gaan voor
    uit = [it for it in items if it.veld("uitgelicht").lower() in ("ja", "true", "1")]
    rest = [it for it in items if it not in uit]
    kid = ctx.esc(k.id or "reviews")

    if variant == "compact":
        grond = sectie or "wit"
        rij = (uit + rest)[:3]
        kaarten = "".join(kaart(ctx, it, i) for i, it in enumerate(rij))
        link = home.veld("profiel-linktekst", "Bekijk alle reviews op Google")
        return f'''<section class="sectie sectie--{grond} b-reviews b-reviews--compact" id="{kid}" aria-labelledby="{kid}-kop">
  <div class="wrap">
    <div class="kopbalk">{ctx.kopgroep(k)}
      <div class="kopbalk__eind"><a class="rscore" href="{ctx.esc(ctx.cfg.GOOGLE_PROFIEL)}" rel="noopener" target="_blank">{ctx.icoon("google", "ic ic--google")}<b>{ctx.cfg.GOOGLE_SCORE}</b>{ctx.sterren(5)}<span>{ctx.inline(link)}</span><span class="vh"> (opent Google in een nieuw tabblad)</span></a></div>
    </div>
    <ul class="rraster rraster--compact" role="list" data-reveal-groep>{kaarten}</ul>
  </div>
</section>'''

    grond = sectie or "mist"
    volgorde = uit[:1] + rest if uit else items
    delen = [paneel(ctx, home, k)]
    for i, it in enumerate(volgorde):
        delen.append(kaart(ctx, it, i, groot=(i == 0 and bool(uit))))
    drie = " rraster--drie" if len(volgorde) == 3 and uit else ""
    return f'''<section class="sectie sectie--{grond} b-reviews" id="{kid}" aria-labelledby="{kid}-kop">
  <div class="wrap">
    {ctx.kopgroep(k)}
    <ul class="rraster{drie}" role="list" data-reveal-groep>{"".join(delen)}</ul>
  </div>
</section>'''
