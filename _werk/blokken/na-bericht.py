"""Na uw bericht (/contact/, #na-bericht): de Diepblauwe band met dakrand, zoals "Na uw aanvraag" bij De Kievit.
Links de kop, de tekst en twee knoppen; rechts in plaats van een foto het huisvenster in Koningsblauw met
het negatieve beeldmerk (hetzelfde motief als #over-ons op de home, tot er eigen foto's zijn).

Kopij: contact.md, blok {#na-bericht}: label, kop, tekst (alinea's), knop.
"""

NAAM = "na-bericht"
CSS = True
JS = False


def html(ctx, kopij, **opties) -> str:
    k = kopij
    sid = opties.get("id", k.id or "na-bericht")
    b, h = getattr(ctx.cfg, "LOGO_MATEN", {}).get("beeldmerk", (1000, 509))
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
          <div class="b-{NAAM}__huis">
            <img class="b-{NAAM}__merk" src="{ctx.logo("beeldmerk-negatief")}" alt="" width="{b}" height="{h}" loading="lazy" decoding="async">
          </div>
        </figure>
      </div>
    </section>'''
