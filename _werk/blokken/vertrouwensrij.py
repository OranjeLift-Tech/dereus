"""Vertrouwensrij (/contact/, #vertrouwen): vier compacte kaarten met een icoontegel, zoals de rij met
kerncijfers onder de offertepil bij De Kievit. Alleen bevestigde feiten (geen keurmerken, geen jaartal).

Kopij: contact.md, blok {#vertrouwen}: de kop is alleen voor schermlezers; vier ###-items (titel + tekst).
Het icoon volgt uit de titel: Google, verzekerd, adviseur, bereikbaar; anders een vinkje.
"""

NAAM = "vertrouwensrij"
CSS = True
JS = False

ICOON = [("google", "google"), ("verzeker", "schild"), ("adviseur", "persoon"), ("bereikbaar", "klok"),
         ("per week", "klok"), ("voorrijkosten", "euro"), ("24 uur", "klok")]


def _icoon(titel):
    t = titel.lower()
    for sleutel, naam in ICOON:
        if sleutel in t:
            return naam
    return "check"


def html(ctx, kopij, **opties) -> str:
    k = kopij
    sid = opties.get("id", k.id or "vertrouwen")
    kaarten = "".join(f'''<li class="b-{NAAM}__kaart">
              <span class="b-{NAAM}__ic{" b-" + NAAM + "__ic--google" if _icoon(it.kop) == "google" else ""}" aria-hidden="true">{ctx.icoon(_icoon(it.kop))}</span>
              <p><b>{ctx.inline(it.kop)}</b>{f"<span>{ctx.inline(it.veld('tekst') or ' '.join(it.tekst))}</span>" if (it.veld('tekst') or it.tekst) else ""}</p>
            </li>''' for it in k.items)
    return f'''<section class="b-{NAAM} sectie sectie--mist" id="{sid}" aria-labelledby="{sid}-kop">
      <div class="wrap">
        <h2 class="vh" id="{sid}-kop">{ctx.inline(k.kop or "Waarom De Reus")}</h2>
        <ul class="b-{NAAM}__rij" role="list" data-reveal-groep>{kaarten}</ul>
      </div>
    </section>'''
