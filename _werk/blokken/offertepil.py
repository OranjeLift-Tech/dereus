"""Offertepil: kort formulier (Van, Naar, Wanneer, Soort) dat met GET naar /offerte/ gaat.

Werkt zonder JS: /offerte/ leest van, naar, datum en dienst uit de adresbalk (blok formulier, dereus-b4).
Varianten:
  hero  over de onderrand van de hero (home); kopij = het hero-blok (#offerte in home.md)
  los   als afsluiter op andere pagina's; kopij = ## ... {#offertepil} van die pagina.
        Opties dienst="opslag" (selecteert de soort), van="Rijswijk", naar="Rijswijk" (vullen vooraf in).
        Met over_kop=True staat hij direct onder de paginakop en valt hij over de onderrand ervan
        (zoals de pil op de home en op de contactpagina van De Kievit).
Veldlabels en placeholders komen uit offerte.md #formulier (items van, naar, datum, dienst).
"""
import navigatie

NAAM = "offertepil"
CSS = True
JS = False


def _veld(ctx, naam, label_std, placeholder_std=""):
    it = ctx.formulierveld(naam)
    label = (it.titel if it else "") or label_std
    # De pil is smal: een kortere placeholder (placeholder-kort in offerte.md) gaat voor
    ph = (it.veld("placeholder-kort") or it.veld("placeholder") if it else "") or placeholder_std
    return label, ph


def pil(ctx, knoptekst, id_, dienst=None, van="", naar=""):
    van_l, van_p = _veld(ctx, "van", "Van", "Postcode of plaats")
    naar_l, naar_p = _veld(ctx, "naar", "Naar", "Postcode of plaats")
    dat_l, _ = _veld(ctx, "datum", "Wanneer")
    it, opties = ctx.dienst_opties()
    dienst_l = (it.titel if it else "") or "Soort verhuizing"
    if not opties:
        opties = [(sl, naam) for sl, naam, _ in navigatie.DIENSTEN]
    kies = "Kies een type"
    opt = "".join(f'<option value="{ctx.esc(w)}"{" selected" if w == dienst else ""}>{ctx.esc(t)}</option>' for w, t in opties)
    van_w = f' value="{ctx.esc(van)}"' if van else ""
    naar_w = f' value="{ctx.esc(naar)}"' if naar else ""
    e = ctx.esc
    return f'''<form class="of-pil" action="/offerte/" method="get" aria-label="Offerte aanvragen">
      <label class="of-veld of-veld--adres" for="{id_}-van"><span>{e(van_l)}</span><input id="{id_}-van" name="van" type="text" placeholder="{e(van_p)}" autocomplete="address-level2"{van_w}></label>
      <span class="of-streep" aria-hidden="true"></span>
      <label class="of-veld of-veld--adres" for="{id_}-naar"><span>{e(naar_l)}</span><input id="{id_}-naar" name="naar" type="text" placeholder="{e(naar_p)}"{naar_w}></label>
      <span class="of-streep" aria-hidden="true"></span>
      <label class="of-veld of-veld--datum" for="{id_}-datum"><span>{e(dat_l)}</span><input id="{id_}-datum" name="datum" type="date"></label>
      <span class="of-streep" aria-hidden="true"></span>
      <label class="of-veld of-veld--dienst" for="{id_}-dienst"><span>{e(dienst_l)}</span><select id="{id_}-dienst" name="dienst"><option value="">{kies}</option>{opt}</select></label>
      <button class="knop knop--cta of-knop" type="submit"><span>{e(knoptekst)}</span>{ctx.icoon("pijl")}</button>
    </form>'''


def google(ctx, klasse="of-google"):
    return (f'<a class="{klasse}" href="{ctx.esc(ctx.cfg.GOOGLE_PROFIEL)}" rel="noopener" target="_blank">'
            f'{ctx.icoon("google", "ic ic--google")}<b>{ctx.cfg.GOOGLE_SCORE}</b>'
            f'<span>{ctx.sterren(5)}<small>uit 5 op Google</small></span></a>')


def html(ctx, kopij, variant="hero", over_kop=False, dienst=None, van="", naar="", **opties):
    if over_kop:
        # Alle paginakoppen bevatten nu zelf dezelfde compacte offertekaart.
        return ""
    vooraf = {"dienst": dienst, "van": van, "naar": naar}   # optioneel: dienst selecteren, van of naar invullen
    k = kopij
    if variant in ("hero", "header"):
        k = k or ctx.kopij_van("home").blok_of_leeg("offerte")
        titel = "Vraag uw offerte aan" if variant == "header" else k.veld("pil-titel", "Binnen 24 uur uw offerte")
        onder = k.veld("pil-onder", "")
        knop = k.veld("pil-knop", "Offerte aanvragen")
        vinken = ctx.lijst(k.lijst, "of-vinken vinklijst")
        prefix = "header-of" if variant == "header" else "of"
        return f'''<div class="of-wrap" id="{prefix}-kaart">
    <div class="of-box of-box--hero{" of-box--header" if variant == "header" else ""}">
      <div class="of-kop">
        <h2 class="of-titel">{ctx.inline(titel)}</h2>
        {google(ctx)}
      </div>
      {pil(ctx, knop, prefix, **vooraf)}
      <div class="of-voet">
        {vinken}
        {f'<p class="of-onder">{ctx.inline(onder)}</p>' if onder else ""}
      </div>
    </div>
  </div>'''

    # los: eigen sectie als afsluiter
    home = ctx.kopij_van("home").blok_of_leeg("offerte")
    if k is None:                          # ("offertepil", {"variant": "los", "kopij": None}): alles van de home
        import kopij as _kopij
        k = _kopij.Leeg("home", "offertepil")
    titel = k.kop or home.veld("pil-titel", "Binnen 24 uur uw offerte")
    intro = k.veld("intro") or home.veld("pil-onder")
    knop = home.veld("pil-knop", "Offerte aanvragen")
    bel = k.veld("belregel")
    belhtml = (f'<p class="of-bel">{ctx.icoon("telefoon")}<a href="{ctx.telhref}">{ctx.inline(bel)}</a></p>' if bel else "")
    klasse = "sectie sectie--mist b-offertepil" + (" b-offertepil--over" if over_kop else "")
    onthul = "" if over_kop else " data-reveal"      # boven de vouw niet laten invliegen
    return f'''<section class="{klasse}" id="{ctx.esc(k.id or "offertepil")}" aria-labelledby="of-los-kop">
  <div class="wrap">
    <div class="of-box of-box--los"{onthul}>
      <div class="of-kop">
        <div>
          {ctx.label(k.veld("label"))}
          <h2 class="of-titel" id="of-los-kop">{ctx.inline(titel)}</h2>
          {f'<p class="of-sub">{ctx.inline(intro)}</p>' if intro else ""}
        </div>
        {google(ctx)}
      </div>
      {pil(ctx, knop, "ofl", **vooraf)}
      {belhtml}
    </div>
  </div>
</section>'''
