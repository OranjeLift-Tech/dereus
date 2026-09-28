"""Hero van de home (#offerte). De H1 en het teambeeld staan gecentreerd boven elkaar.
De compacte offertekaart valt over de onderrand; de fotoachtergrond komt uit de routegebonden
headerbeeldenlijst. De oude stockachtergrond uit Wix wordt niet gebruikt.
Onder de tekst staat, in deze volgorde van voorrang:
  config.HERO_TEAM         de vrijstaande teamfoto (besluit gebruiker), de onderrand valt achter de offertekaart;
  anders                   het negatieve beeldmerk.
Het teambeeld is het grootste element boven de vouw (LCP): geen lazy, fetchpriority high, en de home
preloadt de juiste maat (kit.HERO_SIZES). Op de telefoon is toch de achtergrondfoto het LCP-element (Lighthouse
28-09-2026, LCP 4,6 s), maar fetchpriority high op die foto maakt het erger: 4,89 s tegen 4,60 s, drie runs
elk, omdat hij dan met het teambeeld om de bandbreedte vecht. Hij blijft op low.
Met een veld slogan: krijgt de H1 twee regels: de kop klein erboven (wie en waar), de slogan groot, en met
wissel: (woorden met komma's) wisselt het laatste woord van de slogan (js/blok/hero.js, sinds 28-09-2026).
"""
import kit

NAAM = "hero"
CSS = True
JS = True
AFHANKELIJK = ["offertepil"]


def doos(klasse):
    vlakken = "".join(f'<span class="doos__v doos__v--{v}"></span>' for v in ("voor", "achter", "links", "rechts", "boven", "onder"))
    return f'<span class="doos {klasse}" aria-hidden="true"><span class="doos__in">{vlakken}</span></span>'


def team(ctx):
    cfg = ctx.cfg
    r = ctx.responsief(cfg.HERO_TEAM)
    alt = ctx.esc(getattr(cfg, "HERO_TEAM_ALT", "") or "")
    return (f'<picture class="hero__team"><source type="image/webp" srcset="{r["srcset"]}" sizes="{kit.HERO_SIZES}">'
            f'<img src="{r["src"]}" alt="{alt}" width="{r["breedte"]}" height="{r["hoogte"]}" fetchpriority="high" decoding="async">'
            f'</picture>')


def figuur(ctx):
    cfg = ctx.cfg
    if getattr(cfg, "HERO_TEAM", None):
        # geen huisvlak achter drie mensen (te druk); een zachte gloed in de CSS
        return f'''<div class="hero__figuur hero__figuur--team">
      {team(ctx)}
    </div>'''
    b, h = cfg.LOGO_MATEN["beeldmerk"]
    beeld = f'<img class="hero__beeldmerk" src="{ctx.logo("beeldmerk")}" alt="" width="{b}" height="{h}" decoding="async">'
    return f'''<div class="hero__figuur" aria-hidden="true">
      <span class="hero__huis"></span>
      {doos("doos--a")}
      {doos("doos--b")}
      {beeld}
    </div>'''


def html(ctx, kopij, **opties):
    k = kopij
    cfg = ctx.cfg
    foto = kit.headerbeeld(ctx.pagina.pad)
    # sinds 28-09-2026 is de foto uit de headerbeeldenlijst het eerste beeld van een bewegende collage (herocollage.py)
    achter = ctx.blok("herocollage", kopij=None, foto=foto)
    b, h = cfg.LOGO_MATEN["beeldmerk"]
    textuur = f'<img class="hero__textuur" src="{ctx.logo("beeldmerk-negatief")}" alt="" width="{b}" height="{h}" decoding="async">'
    intro = k.veld("intro")
    h1 = ctx.inline(k.kop)
    slogan = k.veld("slogan")
    if slogan:
        woorden = [w.strip() for w in k.veld("wissel").split(",") if w.strip()]
        wissel = (f' <em class="hero__wissel" data-woorden="{ctx.esc("|".join(woorden))}">{ctx.esc(woorden[0])}</em>'
                  if woorden else "")
        h1 = (f'<span class="hero__boven">{h1}</span><span class="vh">. </span>'
              f'<span class="hero__slogan">{ctx.inline(slogan)}{wissel}</span>')
    bel = (f'<p class="hero__bel">{ctx.bereikbaar("bereikbaar hero__status", tijden_id="hero-tijden")}'
           f'<a href="{cfg.TELHREF}">{ctx.icoon("telefoon")}<span>Bel {ctx.tel}</span></a></p>')
    return f'''<section class="hero{" hero--foto" if foto else ""}" id="{ctx.esc(k.id or "offerte")}" aria-labelledby="hero-h1">
  <div class="hero__grond" aria-hidden="true">{achter}<span class="hero__waas"></span>{textuur}<span class="hero__korrel"></span></div>
  <div class="wrap hero__grid">
    <div class="hero__tekst">
      {ctx.label(k.veld("label"), "hero__label")}
      <h1 class="hero__h1" id="hero-h1">{h1}</h1>
      {f'<p class="hero__intro">{ctx.inline(intro)}</p>' if intro else ""}
      {bel}
    </div>
    {figuur(ctx)}
  </div>
  {ctx.blok("herocollage", kopij=None, deel="knop")}
</section>
<div class="hero-pil">
  <div class="wrap">{ctx.blok("offertepil", kopij_id=k.id or "offerte", variant="header")}</div>
</div>'''
