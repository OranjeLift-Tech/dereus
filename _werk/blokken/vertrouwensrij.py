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


# Per icoon het 3D-voorwerp in img/contact-3d/: bestandsnaam, breedte en hoogte
# (bron: _ai-beelden/contact-3d/scene-vertrouwen.html). Zonder voorwerp blijft het lijnicoon in het goudgele huis staan.
VOORWERP = {
    "google": ("score", 411, 320),
    "schild": ("schild", 251, 320),
    "persoon": ("headset", 287, 320),
    "klok": ("klok", 279, 320),
}


def _beeld(ctx, icoon):
    if icoon in VOORWERP:
        naam, b, h = VOORWERP[icoon]
        return (f'<span class="b-{NAAM}__ic b-{NAAM}__ic--3d" aria-hidden="true"><img class="b-{NAAM}__obj b-{NAAM}__obj--{naam}" '
                f'src="/img/contact-3d/{naam}.webp" alt="" width="{b}" height="{h}" decoding="async"></span>')
    google = f" b-{NAAM}__ic--google" if icoon == "google" else ""
    return f'<span class="b-{NAAM}__ic{google}" aria-hidden="true">{ctx.icoon(icoon)}</span>'


def html(ctx, kopij, **opties) -> str:
    k = kopij
    sid = opties.get("id", k.id or "vertrouwen")
    grond = opties.get("grond", "mist")
    kaarten = "".join(f'''<li class="b-{NAAM}__kaart">
              {_beeld(ctx, _icoon(it.kop))}
              <p><b>{ctx.inline(it.kop)}</b>{f"<span>{ctx.inline(it.veld('tekst') or ' '.join(it.tekst))}</span>" if (it.veld('tekst') or it.tekst) else ""}</p>
            </li>''' for it in k.items)
    return f'''<section class="b-{NAAM} sectie sectie--{grond}" id="{sid}" aria-labelledby="{sid}-kop">
      <div class="wrap">
        <h2 class="vh" id="{sid}-kop">{ctx.inline(k.kop or "Waarom De Reus")}</h2>
        <ul class="b-{NAAM}__rij" role="list" data-reveal-groep>{kaarten}</ul>
      </div>
    </section>'''
