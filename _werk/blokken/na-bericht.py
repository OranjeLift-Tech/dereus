"""Na uw bericht (/contact/, #na-bericht): de Diepblauwe band met dakrand, zoals "Na uw aanvraag" bij De Kievit.
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
    tekst = f'''<div class="b-{NAAM}__tekst" data-reveal>
          {inhoud}
        </div>
        <figure class="b-{NAAM}__beeld" data-reveal>
          <div class="b-{NAAM}__kader">
            {ctx.beeld(FOTO[0], "", FOTO[1], FOTO[2], klasse=f"b-{NAAM}__foto")}
          </div>
          <span class="b-{NAAM}__uit">{ctx.beeld(UITSNEDE[0], "", UITSNEDE[1], UITSNEDE[2])}</span>
        </figure>{na_beeld}'''
    # met kop wijst de sectie naar die kop; zonder kop (bedankt) krijgt zij een eigen naam en geen id,
    # want het kopijblok deelt zijn id met de paginakop
    naam = f' id="{sid}" aria-labelledby="{sid}-kop"' if met_kop else ' aria-label="Wat er nu gebeurt"'
    extra = f" b-{NAAM}--onder-beeld" if onder else ""
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
