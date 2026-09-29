"""Is mijn inboedel verzekerd tijdens de verhuizing? (/diensten/particuliere-verhuizingen/ #verzekering), sinds
29-09-2026 op de testlijn. Naar het nieuwe patroon policy-card-folder-seal (../section-library, gemaakt met /section,
nog niet geregistreerd): de vraag en het antwoord links, rechts een poliskaart met drie regels uit de algemene
voorwaarden op een gouden map, en het klei-schild als zegel over de rechterrand van de kaart. Geclaimd als #1 in
_werk/dienstsecties-register.md.

Kopij, alles al live of letterlijk uit de voorwaarden (dereus-2f: "Every insurance statement on that card [...] must be
traceable to website/content/algemene-voorwaarden.md (or text already live on the site)"):
- label: de titel van het punt "Standaard verzekerd" in home.md {#waarom};
- kop en intro: de vraag in home.md {#vragen}; de intro is zin 1 en 3 van het antwoord, zin 2 (de bedragen) en 4 (schade
  melden) staan op de kaart;
- de link: linktekst van kosten.md {#annuleren}, naar /algemene-voorwaarden/#artikel-13 (de schadevergoeding);
- de kaart: titel en versie uit algemene-voorwaarden.md {#kop}; de bedragen uit {#artikel-13}, de meldplicht uit
  {#artikel-12}. De bedragen worden uit de artikeltekst gelezen, dus de kaart volgt de voorwaarden of de build stopt.
Eigen tekst van dereus-28: de omschrijvingen "maximale vergoeding per inboedel" (de woorden van artikel 13), "eigen
risico" (idem) en "schade melden op de verhuisdag" (de woorden van artikel 12), en de waarde "Direct" (artikel 12).
"""
import re

NAAM = "polis"
CSS = True
JS = False

VRAAG = "Is mijn inboedel verzekerd tijdens de verhuizing?"
ZEGEL = "schild"


def _fout(bericht):
    raise ValueError(f"polis: {bericht}")


def _artikel(voorwaarden, nr):
    b = voorwaarden.blok(f"artikel-{nr}")
    return " ".join(b.tekst or []), f"Artikel {nr}"


def _regels(ctx):
    av = ctx.kopij_van("algemene-voorwaarden")
    t13, a13 = _artikel(av, 13)
    t12, a12 = _artikel(av, 12)
    m = re.search(r"Maximale vergoeding €\s?(\d{1,3}(?:\.\d{3})*) per inboedel", t13) or _fout(f"geen maximale vergoeding in artikel 13: {t13!r}")
    e = re.search(r"Eigen risico €\s?(\d{1,3}(?:\.\d{3})*)", t13) or _fout(f"geen eigen risico in artikel 13: {t13!r}")
    if "direct op de verhuisdag" not in t12:
        _fout(f"artikel 12 zegt niet meer 'direct op de verhuisdag': {t12!r}")
    return [(f"€ {m.group(1)}", "maximale vergoeding per inboedel", a13),
            (f"€ {e.group(1)}", "eigen risico", a13),
            ("Direct", "schade melden op de verhuisdag", a12)]


def html(ctx, kopij, id="verzekering", **opties):
    home = ctx.kopij_van("home")
    v = next((it for it in home.blok("vragen").items if it.titel == VRAAG), None) or _fout(f"{VRAAG!r} staat niet in home.md #vragen")
    antwoord = v.veld("tekst") or " ".join(v.tekst or [])
    zinnen = re.split(r"(?<=\.)\s+", antwoord.strip())
    if len(zinnen) != 4 or not zinnen[0].startswith("Ja,") or not zinnen[2].startswith("Wilt u"):
        _fout(f"het antwoord in home.md #vragen is veranderd, kies de zinnen opnieuw: {antwoord!r}")
    intro = f"{zinnen[0]} {zinnen[2]}"
    label = next((it.titel for it in home.blok("waarom").items if it.titel == "Standaard verzekerd"), None) or _fout("home.md #waarom mist 'Standaard verzekerd'")
    av = ctx.kopij_van("algemene-voorwaarden").blok("kop")
    link = ctx.kopij_van("kosten").blok("annuleren").veld("linktekst") or _fout("kosten.md #annuleren mist linktekst")
    regels = "".join(f'''
            <div class="polis__regel"><dt>{ctx.esc(omschr)}</dt><dd class="polis__waarde">{ctx.esc(waarde)}</dd><dd class="polis__artikel">{ctx.esc(art)}</dd></div>'''
                     for waarde, omschr, art in _regels(ctx))
    zegel = ctx.beeld(f"/img/clay/{ZEGEL}-144.webp", "", 144, 144, klasse="polis__zegel",
                      srcset=f"/img/clay/{ZEGEL}-144.webp 144w, /img/clay/{ZEGEL}-240.webp 240w",
                      sizes="(max-width: 560px) 4.25rem, 5.5rem")
    knop = ctx.knop(link, "/algemene-voorwaarden/#artikel-13", soort="link") if ctx.live("/algemene-voorwaarden/") else ""
    return f'''<section class="sectie sectie--wit b-{NAAM}" id="{ctx.esc(id)}" aria-labelledby="{ctx.esc(id)}-kop">
  <div class="wrap polis__raster">
    <div class="polis__kop" data-reveal>{ctx.label(label)}<h2 id="{ctx.esc(id)}-kop">{ctx.inline(VRAAG)}</h2><p class="intro">{ctx.inline(intro)}</p>{knop}</div>
    <div class="polis__fig" data-reveal>
      <div class="polis__map" aria-hidden="true"></div>
      <div class="polis__kaart">
        <div class="polis__kaartkop"><h3>{ctx.inline(av.kop)}</h3><p>{ctx.inline(av.veld("label"))}</p></div>
        <dl class="polis__regels">{regels}
        </dl>
      </div>
      {zegel}
    </div>
  </div>
</section>'''
