"""Na uw bericht (/contact/, #na-bericht): de Diepblauwe band met dakrand, zoals "Na uw aanvraag" bij referentie A.
Links de kop, de tekst en twee knoppen; rechts de foto van de verhuisadviseur die terugbelt, met het huisvlak
uit het logo als vorm erachter (css/blok/na-bericht.css).

Kopij: contact.md, blok {#na-bericht}: label, kop, tekst (alinea's), knop.

Sinds 28-09-2026 is dit de vorm voor "wat er nu gebeurt" op elke pagina (de gebruiker: "5. What happens next:
A: Navy band with photo"). Dus ook /offerte/ (offerte.md {#na-aanvraag}: kop, intro, belregel, drie stappen) en
de bedanktpagina's (systeem.md {#offerte-bedankt} en {#contact-bedankt}: stappen, belregel, knoppen). Opties:
  paneel   de band als Diepblauwe plaat in een lichte sectie (grond, standaard wit), voor pagina's die direct
           op de footer eindigen
  kop      False laat de kopgroep weg (de bedanktpagina's: daar staat de kop al in de paginakop)
  vink     het gele vinkje bovenaan (bedankt)
  google   de Google-pil naast de belregel (/offerte/, voorheen in stappen-na-aanvraag)
  onder_beeld  belregel, WhatsApp en de Google-pil komen na de foto in plaats van in de tekstkolom; WhatsApp
           en de pil vormen daar samen een knoppenrij (/offerte/, 28-09-2026: "maybe add them below the
           image"). De plek per breedte staat in css/blok/na-bericht.css
  knoppen  "contact" (standaard: offerte aanvragen en mail ons), "bedankt" (bellen en terug) of None
  titel_h  het kopniveau van de stappen: h3 onder de kopgroep, h2 als er geen kopgroep is
  beeld    "bureau": de versie van Tugche (origin/main 9dbb9a8, 28-09-2026) voor /contact/. De adviseur aan
           haar bureau, zonder kamer erachter en met een grote Goudgele duim ernaast, zoals de contactkop van
           referentie A (BUREAU en DUIM hieronder, blok "Beeld bureau" in css/blok/na-bericht.css). Zonder
           deze optie de foto met het huisvlak en de uitsnede (FOTO en UITSNEDE).
Items van het kopijblok worden genummerde stappen.
"""

NAAM = "na-bericht"
CSS = True
JS = False

# de verhuisadviseur die terugbelt, in het huisvlak uit het logo (zelfde uitsnede-familie als de kop van /contact/)
FOTO = ("/img/contact-klantenservice-foto.webp", 1200, 800)
# dezelfde foto zonder achtergrond (_ai-beelden/contact-uitsnede.mjs). Die laag ligt over de foto
# en wordt aan de bovenkant niet afgesneden, dus zij komt met haar hoofd uit de lijst; de maten
# staan in css/blok/na-bericht.css. Zelfde paar als homecontact op de home.
UITSNEDE = ("/img/contact-klantenservice-uit.webp", 1200, 800)

# Optie beeld="bureau": de verhuisadviseur met bureau, kop, toetsenbord, telefoon en scherm; de kamer is weg
# (bron en werkwijze: _ai-beelden/na-bericht-bureau/). Onderaan loopt het bureau tot de rand door,
# die rand krijgt in de css ronde hoeken; boven is alles vrij.
BUREAU = ("/img/contact-klantenservice-bureau-uit.webp", 1060, 690)

# duim omhoog bij beeld="bureau": manchet links, hand met duim; egaal, de kleur komt uit de css
DUIM = ('<svg class="b-na-bericht__duim" viewBox="0 0 120 108" aria-hidden="true" focusable="false">'
        '<rect x="0" y="46" width="22" height="62" rx="2.5"/>'
        '<path d="M30 102V51L53 12C57 5 62 2 68 3C76 4 80 11 78 20L72 40H109C116 40 121 46 119.5 53'
        'L108.5 101C107.5 105.5 104 108 99.5 108H36C32.7 108 30 105.3 30 102Z"/></svg>')


def _stappen(ctx, k, h):
    if not k.items:
        return ""
    li = "".join(f'''<li class="b-{NAAM}__stap">
              <span class="b-{NAAM}__nr" aria-hidden="true">{i}</span>
              <div><{h} class="b-{NAAM}__titel">{ctx.inline(it.kop)}</{h}>{ctx.alineas(it.tekst)}</div>
            </li>''' for i, it in enumerate(k.items, 1))
    return f'<ol class="b-{NAAM}__stappen" role="list">{li}</ol>'


def _google(ctx):
    cfg = ctx.cfg
    return (f'<a class="b-{NAAM}__google" href="{ctx.esc(cfg.GOOGLE_PROFIEL)}" rel="noopener" target="_blank">'
            f'{ctx.icoon("google", klasse="ic b-" + NAAM + "__g")}{ctx.sterren(klasse="sterren b-" + NAAM + "__sterren")}'
            f'<span><strong>{ctx.esc(cfg.GOOGLE_SCORE)}</strong> uit 5 op Google</span>'
            f'<span class="vh"> (opent Google in een nieuw tabblad)</span></a>')


def _knoppen(ctx, k, soort):
    if soort == "contact":
        return (ctx.knop(k.veld("knop", "Offerte aanvragen"), "/offerte/", soort="cta")
                + ctx.knop("Mail ons", f"mailto:{ctx.mail}", soort="licht", icoon="mail", klasse="knop--icoon-voor"))
    if soort == "bedankt":
        # Eén WhatsApp-knop per band: die hangt achter de belregel, dus de belknop hier krijgt er geen.
        # Eerst stonden er twee in één kaart (belregel en belknop kregen elk hun eigen knop).
        bel = ctx.knop(f"Bel {ctx.tel}", ctx.telhref, soort="cta", icoon="telefoon", klasse="knop--icoon-voor",
                       attrs="data-geen-whatsapp")
        return bel + ctx.knop(k.veld("knop", "Terug naar de home"), k.veld("knop-link", "/"), soort="licht", icoon="pijl")
    return ""


def html(ctx, kopij, **opties) -> str:
    k = kopij
    paneel = opties.get("paneel", False)
    met_kop = opties.get("kop", True)
    sid = opties.get("id", k.id or "na-bericht")
    knoppen = _knoppen(ctx, k, opties.get("knoppen", "contact"))
    vink = (f'<span class="b-{NAAM}__vink" aria-hidden="true">{ctx.icoon("check")}</span>'
            if opties.get("vink") else "")
    onder = opties.get("onder_beeld", False)
    # onder de foto staat WhatsApp als knop in de rij, dus het nummer krijgt er geen eigen knop achter
    belregel = ctx.belregel(k.veld("belregel"), klasse=f"belregel b-{NAAM}__bel", whatsapp=not onder)
    google = _google(ctx) if opties.get("google") else ""
    na_beeld = ""
    if onder:
        # bel en rij onthullen elk apart: vanaf 1000 px is de voet display:contents en ziet de observer hem niet
        bel = belregel.replace("<p ", "<p data-reveal ", 1)
        na_beeld = (f'\n        <div class="b-{NAAM}__voet">{bel}'
                    f'<div class="b-{NAAM}__acties" data-reveal>{ctx.whatsapp()}{google}</div></div>')
        voet = ""
    else:
        voet = f'<div class="b-{NAAM}__voet">{belregel}{google}</div>' if (belregel or google) else ""
    delen = [vink + (ctx.kopgroep(k, klasse=f"b-{NAAM}__kop") if met_kop else ""),
             ctx.alineas(k.tekst),
             _stappen(ctx, k, opties.get("titel_h", "h3" if met_kop else "h2")),
             voet,
             f'<div class="knoppen">{knoppen}</div>' if knoppen else ""]
    inhoud = "\n          ".join(d for d in delen if d)
    bureau = opties.get("beeld") == "bureau"
    if bureau:
        figuur = f'''{DUIM}
          {ctx.beeld(BUREAU[0], "", BUREAU[1], BUREAU[2], klasse=f"b-{NAAM}__foto")}'''
    else:
        figuur = f'''<div class="b-{NAAM}__kader">
            {ctx.beeld(FOTO[0], "", FOTO[1], FOTO[2], klasse=f"b-{NAAM}__foto")}
          </div>
          <span class="b-{NAAM}__uit">{ctx.beeld(UITSNEDE[0], "", UITSNEDE[1], UITSNEDE[2])}</span>'''
    tekst = f'''<div class="b-{NAAM}__tekst" data-reveal>
          {inhoud}
        </div>
        <figure class="b-{NAAM}__beeld" data-reveal>
          {figuur}
        </figure>{na_beeld}'''
    # met kop wijst de sectie naar die kop; zonder kop (bedankt) krijgt zij een eigen naam en geen id,
    # want het kopijblok deelt zijn id met de paginakop
    naam = f' id="{sid}" aria-labelledby="{sid}-kop"' if met_kop else ' aria-label="Wat er nu gebeurt"'
    extra = (f" b-{NAAM}--onder-beeld" if onder else "") + (f" b-{NAAM}--bureau" if bureau else "")
    if paneel:
        return f'''<section class="b-{NAAM} b-{NAAM}--paneel{extra} sectie sectie--{opties.get("grond", "wit")}"{naam}>
      <div class="wrap">
        <div class="b-{NAAM}__in sectie--diep">
        {tekst}
        </div>
      </div>
    </section>'''
    return f'''<section class="b-{NAAM}{extra} sectie sectie--diep"{naam}>
      <div class="wrap b-{NAAM}__in">
        {tekst}
      </div>
    </section>'''
