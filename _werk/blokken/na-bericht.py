"""Na uw bericht (/contact/, #na-bericht): de Diepblauwe band met dakrand, zoals "Na uw aanvraag" bij De Kievit.
Links de kop, de tekst en twee knoppen; rechts de foto van de verhuisadviseur die terugbelt, met het huisvlak
uit het logo als vorm erachter (css/blok/na-bericht.css).

Kopij: contact.md, blok {#na-bericht}: label, kop, tekst (alinea's), knop.
"""

NAAM = "na-bericht"
CSS = True
JS = False

# de verhuisadviseur die terugbelt, in het huisvlak uit het logo (zelfde uitsnede-familie als de kop van /contact/)
FOTO = ("/img/contact-klantenservice.webp", 1200, 800)
# dezelfde foto zonder achtergrond (_ai-beelden/contact-uitsnede.mjs). Die laag ligt over de foto
# en wordt aan de bovenkant niet afgesneden, dus zij komt met haar hoofd uit de lijst; de maten
# staan in css/blok/na-bericht.css. Zelfde paar als homecontact op de home.
UITSNEDE = ("/img/contact-uit.webp", 1200, 800)


def html(ctx, kopij, **opties) -> str:
    k = kopij
    sid = opties.get("id", k.id or "na-bericht")
    knoppen = (ctx.knop(k.veld("knop", "Offerte aanvragen"), "/offerte/", soort="cta")
               + ctx.knop("Mail ons", f"mailto:{ctx.mail}", soort="licht", icoon="mail", klasse="knop--icoon-voor"))
    return f'''<section class="b-{NAAM} sectie sectie--diep" id="{sid}" aria-labelledby="{sid}-kop">
      <div class="wrap b-{NAAM}__in">
        <div class="b-{NAAM}__tekst" data-reveal>
          {ctx.kopgroep(k, klasse=f"b-{NAAM}__kop")}
          {ctx.alineas(k.tekst)}
          <div class="knoppen">{knoppen}</div>
        </div>
        <figure class="b-{NAAM}__beeld" data-reveal>
          <div class="b-{NAAM}__kader">
            {ctx.beeld(FOTO[0], "", FOTO[1], FOTO[2], klasse=f"b-{NAAM}__foto")}
          </div>
          <span class="b-{NAAM}__uit">{ctx.beeld(UITSNEDE[0], "", UITSNEDE[1], UITSNEDE[2])}</span>
        </figure>
      </div>
    </section>'''
