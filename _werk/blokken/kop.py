"""Paginakop (.pk) voor alle subpagina's: label, H1, korte intro en belmogelijkheid boven een foto.
Altijd precies één H1, ook als de kopij een ##-blok is (systeem.md). De route heeft een eigen foto;
alle pagina's delen dezelfde compacte offertekaart. Ankerchips volgen onder die kaart.

Sinds 28-09-2026 is de kop op elke subpagina dezelfde, op de foto na (besluit gebruiker: "the rest
should be the same except for the image"). Er is dus geen optie meer die de kop zelf verandert; alleen
de home heeft een eigen, grotere opening (hero.py).

Opties:
  kopij_id  welk blok (standaard "kop")
  chips     lijst van (tekst, href) of (tekst, href, dienstsleutel) voor ankernavigatie onder de offertekaart,
            buiten de kop zelf; met een dienstsleutel krijgt de chip het Solar-dienstikoon (sinds 28-09-2026)
  id        id van de sectie (standaard het kopij-id)
  dienst    voorkeuze voor de soort verhuizing in de offertekaart
  streep, icoon, knop, belregel  oude opties; ze worden geaccepteerd en genegeerd
"""
import kit

NAAM = "kop"
CSS = True
JS = False
AFHANKELIJK = ["offertepil"]


def _chip(ctx, tekst, href, icoon=None):
    """Eén ankerchip. Met icoon (een sleutel uit kit.DIENST_SOLAR) staat het Solar-dienstikoon voor de tekst in plaats
    van het huisje; de tekst blijft de naam van de link."""
    ic = ctx.dienst_icoon(icoon, klasse="pk__chip-ic") if icoon else ""
    klasse = "pk__chip pk__chip--icoon" if icoon else "pk__chip"
    return f'<li><a class="{klasse}" href="{ctx.esc(href)}">{ic}{ctx.inline(tekst)}</a></li>'


def html(ctx, kopij, chips=None, id=None, dienst=None, **opties):
    k = kopij
    sid = ctx.esc(id or k.id or "kop")
    foto = kit.headerbeeld(ctx.pagina.pad)
    intro = k.veld("intro-kort") or k.veld("intro")
    delen = []
    delen.append(ctx.label(k.veld("label"), "pk__label"))
    delen.append(f'<h1 class="pk__h1" id="{sid}-h1">{ctx.inline(k.kop)}</h1>')
    if intro:
        delen.append(f'<p class="intro pk__intro">{ctx.inline(intro)}</p>')
    # De compacte offertekaart vervangt de losse offerteknop; telefoon blijft direct bereikbaar.
    delen.append(f'<p class="pk__bel"><a href="{ctx.telhref}">{ctx.icoon("telefoon")}<span>Bel {ctx.tel}</span></a></p>')
    chiphtml = ""
    if chips:
        li = "".join(_chip(ctx, *chip) for chip in chips)
        chiphtml = f'<nav class="pk__chips" aria-label="Op deze pagina"><ul role="list">{li}</ul></nav>'
    return f'''<section class="pk" id="{sid}" aria-labelledby="{sid}-h1">
  <div class="pk__grond" aria-hidden="true"><img class="pk__foto" src="{ctx.esc(foto["src"])}" alt="" width="{foto["width"]}" height="{foto["height"]}" style="object-position:{ctx.esc(foto.get("position", "50% 50%"))}" decoding="async" fetchpriority="high"><span class="pk__waas"></span></div>
  <div class="wrap pk__wrap">
    <div class="pk__tekst">{"".join(delen)}</div>
  </div>
</section>
<div class="pk-pil"><div class="wrap">{ctx.blok("offertepil", kopij=None, variant="header", dienst=dienst)}</div></div>
{f'<div class="wrap pk__ankers">{chiphtml}</div>' if chiphtml else ""}'''
