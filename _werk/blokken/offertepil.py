"""Offertepil: kort formulier (Van, Naar, Wanneer, Soort) dat met GET naar /offerte/ gaat.

Werkt zonder JS: /offerte/ leest van, naar, datum en dienst uit de adresbalk (blok formulier, dereus-b4).
Varianten:
  hero  over de onderrand van de hero (home); kopij = het hero-blok (#offerte in home.md)
  los   als afsluiter op andere pagina's; kopij = ## ... {#offertepil} van die pagina.
        Opties dienst="opslag" (selecteert de soort), van="Rijswijk", naar="Rijswijk" (vullen vooraf in).
        Met over_kop=True staat hij direct onder de paginakop en valt hij over de onderrand ervan
        (zoals de pil op de home en op de contactpagina van referentie A).
        In de blauwe kopband staat een verhuizer die er bovenaan uitsteekt (keuze van de gebruiker,
        28-09-2026). Optie beeld=(pad, breedte, hoogte) kiest een andere uitsnede, beeld=None laat hem weg.
Veldlabels en placeholders komen uit offerte.md #formulier (items van, naar, datum, dienst).
"""
import navigatie

NAAM = "offertepil"
CSS = True
JS = False

FIGUUR = ("/img/verhuizer-twee-dozen-uit.webp", 407, 1200)


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
            f'<span>{ctx.sterren()}<small>uit 5 op Google</small></span></a>')


# Rechts in de kopband van de headerkaart: één donkere pil met drie vakken, zoals de keurmerkpil van
# referentie A (gebruiker, 29-09-2026). Daar staan een reviewcijfer, een branchekeurmerk en een aantal
# beoordelingen; hier alleen wat voor De Reus vaststaat:
#   1. de Google-score (config.GOOGLE_SCORE),
#   2. het schild (sinds 28-09-2026 een losse witte pil, de tekst staat zo op /contact/ #vertrouwen;
#      geen bedrag, dat hoort bij het eigen risico in de FAQ),
#   3. de reactietijd uit "De Reus in cijfers" (home.md #cijfers).
# Geen keurmerk dat de klant niet bevestigd heeft (zie de bewakers). Zodra FEITEN["AANTAL_REVIEWS"]
# bekend is, neemt dat aantal vak 3 over, net als in het voorbeeld.
SCHILD = "Standaard verzekerd"
REACTIE = ("24 uur", "tot wij u bellen")


def keurmerken(ctx):
    aantal = ctx.feit("AANTAL_REVIEWS")
    kop, onder = (str(aantal), "beoordelingen op Google") if aantal else REACTIE
    e = ctx.esc
    return (f'<div class="of-keurmerken" role="group" aria-label="Beoordeling en zekerheden">'
            f'<a class="of-keurmerk of-keurmerk--google" href="{e(ctx.cfg.GOOGLE_PROFIEL)}" rel="noopener" '
            f'target="_blank" aria-label="{e(ctx.score)}">{ctx.icoon("google", "ic ic--google")}'
            f'<b>{ctx.cfg.GOOGLE_SCORE}</b><span class="of-keurmerk__onder">{ctx.sterren()}<small>uit 5 op Google</small></span></a>'
            f'<span class="of-keurmerk of-keurmerk--schild">{ctx.icoon("schild")}<b>{e(SCHILD)}</b></span>'
            f'<span class="of-keurmerk of-keurmerk--tekst"><b>{e(kop)}</b><small>{e(onder)}</small></span>'
            f'</div>')


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
        merken = keurmerken(ctx) if variant == "header" else google(ctx)
        return f'''<div class="of-wrap" id="{prefix}-kaart">
    <div class="of-box of-box--hero{" of-box--header" if variant == "header" else ""}">
      <div class="of-kop">
        <h2 class="of-titel">{ctx.inline(titel)}</h2>
        {merken}
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
    belhtml = ""
    if bel:
        # Op 320 px past de belregel niet op één regel; hij mag daar afbreken (css), maar het
        # telefoonnummer nooit middenin. Vandaar dit omhulsel, na inline() want die escapet.
        tekst = ctx.inline(bel).replace(ctx.cfg.TEL, f'<span class="of-bel__nr">{ctx.cfg.TEL}</span>', 1)
        belhtml = f'<p class="of-bel"><a href="{ctx.telhref}">{ctx.icoon("telefoon")}{tekst}</a></p>'
    klasse = "sectie sectie--mist b-offertepil" + (" b-offertepil--over" if over_kop else "")
    onthul = "" if over_kop else " data-reveal"      # boven de vouw niet laten invliegen
    beeld = opties.get("beeld", FIGUUR)
    figuur = (f'<span class="of-figuur" aria-hidden="true"><img src="{ctx.esc(beeld[0])}" alt="" '
              f'width="{beeld[1]}" height="{beeld[2]}" loading="lazy" decoding="async"></span>') if beeld else ""
    boxklasse = "of-box of-box--los" + (" of-box--figuur" if beeld else "")
    return f'''<section class="{klasse}" id="{ctx.esc(k.id or "offertepil")}" aria-labelledby="of-los-kop">
  <div class="wrap">
    <div class="{boxklasse}"{onthul}>
      <div class="of-kop">{figuur}
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
