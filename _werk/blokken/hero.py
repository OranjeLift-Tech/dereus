"""Hero van de home (#offerte). De H1 en het teambeeld staan gecentreerd boven elkaar.
De compacte offertekaart valt over de onderrand; de fotoachtergrond komt uit de routegebonden
headerbeeldenlijst. De oude stockachtergrond uit Wix wordt niet gebruikt.
Onder de tekst staat, in deze volgorde van voorrang:
  config.HERO_TEAM         de vrijstaande teamfoto (besluit gebruiker), de onderrand valt achter de offertekaart;
  config.MASCOTTE_IN_HERO  de blauwe mascotte;
  anders                   het negatieve beeldmerk.
Het teambeeld is het grootste element boven de vouw (LCP): geen lazy, fetchpriority high, en de home
preloadt de juiste maat (kit.HERO_SIZES).
"""
import kit

NAAM = "hero"
CSS = True
JS = False
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
    if getattr(cfg, "MASCOTTE_IN_HERO", False):
        beeld = ('<img class="hero__mascotte" src="/img/reus-verhuizer.webp" alt="" width="760" height="1140" '
                 'decoding="async" fetchpriority="low">')
    else:
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
    achter = (f'<div class="hero__foto"><img src="{ctx.esc(foto["src"])}" alt="" '
              f'width="{foto["width"]}" height="{foto["height"]}" '
              f'style="object-position:{ctx.esc(foto.get("position", "50% 50%"))}" '
              'decoding="async" fetchpriority="low"></div>')
    b, h = cfg.LOGO_MATEN["beeldmerk"]
    textuur = f'<img class="hero__textuur" src="{ctx.logo("beeldmerk-negatief")}" alt="" width="{b}" height="{h}" decoding="async">'
    intro = k.veld("intro")
    bel = (f'<p class="hero__bel">{ctx.bereikbaar("bereikbaar hero__status")}'
           f'<a href="{cfg.TELHREF}">{ctx.icoon("telefoon")}<span>Bel {ctx.tel}</span></a></p>')
    return f'''<section class="hero{" hero--foto" if foto else ""}" id="{ctx.esc(k.id or "offerte")}" aria-labelledby="hero-h1">
  <div class="hero__grond" aria-hidden="true">{achter}<span class="hero__waas"></span>{textuur}<span class="hero__korrel"></span></div>
  <div class="wrap hero__grid">
    <div class="hero__tekst">
      {ctx.label(k.veld("label"), "hero__label")}
      <h1 class="hero__h1" id="hero-h1">{ctx.inline(k.kop)}</h1>
      {f'<p class="hero__intro">{ctx.inline(intro)}</p>' if intro else ""}
      {bel}
    </div>
    {figuur(ctx)}
  </div>
</section>
<div class="hero-pil">
  <div class="wrap">{ctx.blok("offertepil", kopij_id=k.id or "offerte", variant="header")}</div>
</div>'''
