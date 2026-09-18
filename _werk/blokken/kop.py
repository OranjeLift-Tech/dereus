"""Paginakop (.pk) voor alle subpagina's: label, H1, korte intro en belmogelijkheid boven een foto.
Altijd precies één H1, ook als de kopij een ##-blok is (systeem.md). De route heeft een eigen foto;
alle pagina's delen dezelfde compacte offertekaart. Ankerchips volgen onder die kaart.

Opties:
  kopij_id  welk blok (standaard "kop")
  chips     lijst van (tekst, href) voor ankernavigatie, bijvoorbeeld [("Particulier", "#particulier"), ...]
  streep    True: een goudgele streep onder de H1 (kosten)
  belregel  True of False; standaard alleen bij het blok "kop" (bedankt en 404 tonen hem zelf)
  id        id van de sectie (standaard het kopij-id)
  icoon, knop, belregel  oude sjabloonopties blijven geaccepteerd; de kop gebruikt nu één vaste indeling
  dienst    voorkeuze voor de soort verhuizing in de offertekaart
"""
import kit

NAAM = "kop"
CSS = True
JS = False
AFHANKELIJK = ["offertepil"]


def html(ctx, kopij, chips=None, streep=False, belregel=None, id=None, icoon=None, knop=False, dienst=None, **opties):
    k = kopij
    cfg = ctx.cfg
    sid = ctx.esc(id or k.id or "kop")
    if belregel is None:
        belregel = (k.id == "kop")
    foto = kit.headerbeeld(ctx.pagina.pad)
    intro = k.veld("intro-kort") or k.veld("intro")
    delen = []
    delen.append(ctx.label(k.veld("label"), "pk__label"))
    delen.append(f'<h1 class="pk__h1" id="{sid}-h1">{ctx.inline(k.kop)}</h1>')
    if streep:
        delen.append('<span class="pk__streep" aria-hidden="true"></span>')
    if intro:
        delen.append(f'<p class="intro pk__intro">{ctx.inline(intro)}</p>')
    # De compacte offertekaart vervangt de losse offerteknop; telefoon blijft direct bereikbaar.
    delen.append(f'<p class="pk__bel"><a href="{ctx.telhref}">{ctx.icoon("telefoon")}<span>Bel {ctx.tel}</span></a></p>')
    chiphtml = ""
    if chips:
        li = "".join(f'<li><a class="pk__chip" href="{ctx.esc(href)}">{ctx.inline(tekst)}</a></li>' for tekst, href in chips)
        chiphtml = f'<nav class="pk__chips" aria-label="Op deze pagina"><ul role="list">{li}</ul></nav>'
    return f'''<section class="pk{" pk--chips" if chips else ""}" id="{sid}" aria-labelledby="{sid}-h1">
  <div class="pk__grond" aria-hidden="true"><img class="pk__foto" src="{ctx.esc(foto["src"])}" alt="" width="{foto["width"]}" height="{foto["height"]}" style="object-position:{ctx.esc(foto.get("position", "50% 50%"))}" decoding="async" fetchpriority="high"><span class="pk__waas"></span></div>
  <div class="wrap pk__wrap">
    <div class="pk__tekst">{"".join(delen)}</div>
  </div>
</section>
<div class="pk-pil"><div class="wrap">{ctx.blok("offertepil", kopij=None, variant="header", dienst=dienst)}</div></div>
{f'<div class="wrap pk__ankers">{chiphtml}</div>' if chiphtml else ""}'''
