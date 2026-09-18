"""Paginakop (.pk) voor alle subpagina's: label, H1, optioneel de display-regel (visueel) en de intro,
ankerchips en de belregel. Altijd precies één H1, ook als de kopij een ##-blok is (systeem.md).
Zelfde grond als de hero van de home (Diepblauw naar Koningsblauw, beeldmerk als textuur), zonder foto.

Opties:
  kopij_id  welk blok (standaard "kop")
  chips     lijst van (tekst, href) voor ankernavigatie, bijvoorbeeld [("Particulier", "#particulier"), ...]
  streep    True: een goudgele streep onder de H1 (kosten)
  belregel  True of False; standaard alleen bij het blok "kop" (bedankt en 404 tonen hem zelf)
  id        id van de sectie (standaard het kopij-id)
  icoon     sleutel van een dienst ("opslag"): het gevulde merkicoon in een wit zegel boven de H1
  knop      True: toon het veld knop: uit de kopij. Staat het telefoonnummer erin, dan de belknop,
            anders de CTA-knop naar /offerte/ (met ?dienst=<dienst> als die optie er is)
  dienst    waarde voor ?dienst= in de knop
"""
NAAM = "kop"
CSS = True
JS = False


def html(ctx, kopij, chips=None, streep=False, belregel=None, id=None, icoon=None, knop=False, dienst=None, **opties):
    k = kopij
    cfg = ctx.cfg
    sid = ctx.esc(id or k.id or "kop")
    if belregel is None:
        belregel = (k.id == "kop")
    b, h = cfg.LOGO_MATEN["beeldmerk"]
    visueel = k.veld("visueel")
    intro = k.veld("intro")
    delen = []
    if icoon:
        delen.append(f'<span class="pk__zegel" aria-hidden="true">{ctx.dienst_icoon(icoon, klasse="pk__icoon")}</span>')
    delen.append(ctx.label(k.veld("label"), "pk__label"))
    delen.append(f'<h1 class="pk__h1" id="{sid}-h1">{ctx.inline(k.kop)}</h1>')
    if streep:
        delen.append('<span class="pk__streep" aria-hidden="true"></span>')
    if visueel:
        delen.append(f'<p class="pk__visueel">{ctx.inline(visueel)}</p>')
    if intro:
        delen.append(f'<p class="intro pk__intro">{ctx.inline(intro)}</p>')
    if knop and k.veld("knop"):
        tekst = k.veld("knop")
        if ctx.tel in tekst:
            delen.append(f'<div class="knoppen">{ctx.belknop("licht", tekst)}</div>')
        else:
            doel = f"/offerte/?dienst={dienst}" if dienst else "/offerte/"
            delen.append(f'<div class="knoppen">{ctx.knop(tekst, doel)}</div>')
    if belregel and k.veld("belregel"):
        delen.append(ctx.belregel(k.veld("belregel"), "belregel pk__bel"))
    chiphtml = ""
    if chips:
        li = "".join(f'<li><a class="pk__chip" href="{ctx.esc(href)}">{ctx.inline(tekst)}</a></li>' for tekst, href in chips)
        chiphtml = f'<nav class="pk__chips" aria-label="Op deze pagina"><ul role="list">{li}</ul></nav>'
    return f'''<section class="pk{" pk--chips" if chips else ""}" id="{sid}" aria-labelledby="{sid}-h1">
  <div class="pk__grond" aria-hidden="true"><img class="pk__textuur" src="{ctx.logo("beeldmerk-negatief")}" alt="" width="{b}" height="{h}" decoding="async"></div>
  <div class="wrap pk__wrap">
    <div class="pk__tekst">{"".join(delen)}</div>
    {chiphtml}
  </div>
</section>'''
