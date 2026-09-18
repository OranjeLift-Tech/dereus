"""JSON-LD per pagina (eigenaar: dereus-e7).

De build roept voor(pagina, ctx) aan en zet het resultaat als <script type="application/ld+json"> in de <head>.
Geeft None terug voor pagina's zonder JSON-LD (noindex: bedankt en 404).

Alleen bevestigde feiten (research/website-brief.md en OPEN-VRAGEN.md):
- naam, telefoon, e-mail, adres, openingstijden, werkgebied Den Haag en Nederland;
- coördinaten van het adres volgens de PDOK Locatieserver;
- GEEN aggregateRating: het aantal reviews is onbekend (open vraag 1.4) en Google toont geen sterren voor
  beoordelingen die een bedrijf over zichzelf op de eigen site zet;
- GEEN BreadcrumbList: de kruimels zijn niet zichtbaar op de pagina's (sitemap 1.3, BOUWPLAN 5);
- geen btw, keurmerken, prijzen of sameAs: niet bevestigd. KvK en oprichtingsjaar komen er pas bij als ze in
  config.FEITEN staan (BOUWPLAN 12).

Conceptpagina's (BOUWPLAN 12): een plaats komt pas in areaServed, en een dienstpagina krijgt pas een eigen
Service-knoop, als die pagina in deze build zit (kit.ZICHTBAAR). In de gewone build zijn dat alleen de live
pagina's; in de voorvertoning (--concept, _voorbeeld/, noindex en nooit online) alles, zodat u daar ziet hoe
de JSON-LD eruitziet zodra een concept aan staat.
"""
import json
import re

# Vaste feiten die niet in config.py staan
GEO = (52.0596297, 4.29913794)            # PDOK Locatieserver, Lau Mazirellaan 336, 2525 ZJ 's-Gravenhage
WERKDAGEN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# Paginatype per adres; wat niet in de lijst staat is een gewone WebPage
TYPE = {"/contact/": "ContactPage", "/over-ons/": "AboutPage"}

# Dienstblokken op /diensten/ met een eigen (concept)pagina. Staat die pagina live, dan wijst de Service-knoop
# daarheen in plaats van naar het anker.
DIENST_PAGINA = {
    "particulier": "/diensten/particuliere-verhuizingen/",
    "zakelijk": "/diensten/zakelijke-verhuizingen/",
    "internationaal": "/diensten/internationale-verhuizingen/",
    "opslag": "/diensten/tijdelijke-opslag/",
}
INTERNATIONAAL = "/diensten/internationale-verhuizingen/"

# Plaatspagina's /werkgebied/{slug}/ (sitemap 1.3, hoofdstuk 11). Gemeenten met meer kernen als AdministrativeArea.
PLAATSEN = {
    "rijswijk": ("City", "Rijswijk"),
    "delft": ("City", "Delft"),
    "zoetermeer": ("City", "Zoetermeer"),
    "leidschendam-voorburg": ("AdministrativeArea", "Leidschendam-Voorburg"),
    "westland": ("AdministrativeArea", "Westland"),
    "wassenaar": ("City", "Wassenaar"),
    "pijnacker-nootdorp": ("AdministrativeArea", "Pijnacker-Nootdorp"),
    "leiden": ("City", "Leiden"),
    "lansingerland": ("AdministrativeArea", "Lansingerland"),
    "voorschoten": ("City", "Voorschoten"),
}
LANDEN = {"spanje": "Spanje", "frankrijk": "Frankrijk", "duitsland": "Duitsland", "belgie": "België"}
_PLAATS_PAD = re.compile(r"^/werkgebied/([a-z0-9-]+)/$")
_LAND_PAD = re.compile(r"^/diensten/internationale-verhuizingen/([a-z0-9-]+)/$")

# De acht diensten, als terugval als diensten.md (nog) niet te lezen is. Namen zoals op de huidige site.
DIENSTEN = [
    ("particulier", "Particuliere verhuizingen"),
    ("zakelijk", "Zakelijke verhuizingen"),
    ("nationaal", "Verhuizen door heel Nederland"),
    ("internationaal", "Internationale verhuizingen"),
    ("verhuislift", "Verhuislift"),
    ("opslag", "Tijdelijke opslag"),
    ("montage", "Handymanservice"),
    ("woningontruiming", "Woningontruiming"),
]


def _cfg(ctx, naam, standaard=None):
    return getattr(getattr(ctx, "cfg", None), naam, standaard)


def _domein(ctx):
    return (_cfg(ctx, "DOMEIN", "https://www.verhuisbedrijfdereus.nl") or "").rstrip("/")


def _veld(pagina, naam, ctx=None):
    """titel en beschrijving: de pagina gaat voor, anders de voorkant van het kopijbestand (ctx.kopij.meta)."""
    waarde = getattr(pagina, naam, None)
    if waarde:
        return waarde
    meta = getattr(getattr(ctx, "kopij", None), "meta", None) or {}
    return meta.get(naam)


def _zichtbaar():
    """Paden die in deze build zitten (kit.ZICHTBAAR); leeg als kit er (nog) niet is."""
    try:
        import kit
        return set(getattr(kit, "ZICHTBAAR", set()) or set())
    except Exception:
        return set()


def _feit(ctx, naam):
    """Ruwe waarde uit config.FEITEN (lijsten blijven lijsten), of None."""
    waarde = (_cfg(ctx, "FEITEN", {}) or {}).get(naam)
    return None if waarde in (None, "", [], ()) else waarde


def _plaats(slug):
    soort, naam = PLAATSEN.get(slug, ("City", slug.replace("-", " ").title()))
    return {"@type": soort, "name": naam}


def gebied(ctx):
    """Den Haag en Nederland, plus elke plaats waarvan de pagina /werkgebied/{slug}/ in deze build zit."""
    uit = [{"@type": "City", "name": "Den Haag"}]
    for pad in sorted(_zichtbaar()):
        m = _PLAATS_PAD.match(pad)
        if m:
            uit.append(_plaats(m.group(1)))
    uit.append({"@type": "Country", "name": "Nederland"})
    return uit


def bedrijf(ctx):
    d = _domein(ctx)
    knoop = {
        "@type": "MovingCompany",
        "@id": f"{d}/#bedrijf",
        "name": "Verhuisbedrijf De Reus",
        "url": f"{d}/",
        "telephone": "+31850005647",
        "email": _cfg(ctx, "MAIL", "info@verhuisbedrijfdereus.nl"),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Lau Mazirellaan 336",
            "postalCode": "2525 ZJ",
            "addressLocality": "Den Haag",
            "addressCountry": "NL",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": WERKDAGEN, "opens": "08:00", "closes": "20:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "09:00", "closes": "17:00"},
        ],
        "areaServed": gebied(ctx),
        "logo": {"@type": "ImageObject", "url": f"{d}/img/logo/dereus-logo.png", "width": 2048, "height": 2027},
        "image": f"{d}/img/og.jpg",
        "knowsLanguage": "nl",
    }
    # Pas als de klant ze heeft aangeleverd (config.FEITEN, open vragen 1.1 en 1.2)
    jaar = _feit(ctx, "OPRICHTINGSJAAR")
    if jaar:
        knoop["foundingDate"] = str(jaar)
    kvk = _feit(ctx, "KVK")
    if kvk:
        knoop["identifier"] = {"@type": "PropertyValue", "propertyID": "KvK", "value": str(kvk)}
    return knoop


def website(ctx):
    d = _domein(ctx)
    return {
        "@type": "WebSite",
        "@id": f"{d}/#website",
        "url": f"{d}/",
        "name": "Verhuisbedrijf De Reus",
        "inLanguage": "nl-NL",
        "publisher": {"@id": f"{d}/#bedrijf"},
    }


def webpagina(pagina, ctx):
    d = _domein(ctx)
    pad = getattr(pagina, "pad", "/")
    knoop = {
        "@type": TYPE.get(pad, "WebPage"),
        "@id": f"{d}{pad}#pagina",
        "url": f"{d}{pad}",
        "isPartOf": {"@id": f"{d}/#website"},
        "about": {"@id": f"{d}/#bedrijf"},
        "inLanguage": "nl-NL",
    }
    titel, beschrijving = _veld(pagina, "titel", ctx), _veld(pagina, "beschrijving", ctx)
    if titel:
        knoop["name"] = titel
    if beschrijving:
        knoop["description"] = beschrijving
    if pad == "/":
        knoop["primaryImageOfPage"] = {"@type": "ImageObject", "url": f"{d}/img/og.jpg"}
    return knoop


def _kopij(pagina, ctx):
    """Het gelezen kopijbestand van de pagina (kit.Ctx.kopij, een kopij.Document)."""
    return getattr(ctx, "kopij", None)


def _blok(document, blok_id):
    """Blok met deze id uit het document, of None."""
    if document is None or not hasattr(document, "heeft") or not document.heeft(blok_id):
        return None
    return document.blok(blok_id)


def _platte_tekst(t):
    """Opmaak uit de kopij weghalen: **vet**, ==markering== en [tekst](link)."""
    import re
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    return t.replace("**", "").replace("==", "").strip()


def vragen(pagina, ctx):
    """FAQPage uit het blok ## vragen van de pagina: dezelfde vragen en antwoorden als op het scherm."""
    b = _blok(_kopij(pagina, ctx), "vragen")
    items = getattr(b, "items", None) if b is not None else None
    if not items:
        return None
    d = _domein(ctx)
    pad = getattr(pagina, "pad", "/")
    vragenlijst = []
    for it in items:
        vraag = getattr(it, "kop", None) or (it.veld("titel") if hasattr(it, "veld") else None)
        antwoord = " ".join(getattr(it, "tekst", []) or [])
        if vraag and antwoord:
            vragenlijst.append({
                "@type": "Question",
                "name": _platte_tekst(vraag),
                "acceptedAnswer": {"@type": "Answer", "text": _platte_tekst(antwoord)},
            })
    if not vragenlijst:
        return None
    return {"@type": "FAQPage", "@id": f"{d}{pad}#vragen", "isPartOf": {"@id": f"{d}{pad}#pagina"},
            "mainEntity": vragenlijst}


def _dienst_adres(d, sleutel, zichtbaar):
    """(@id, url) van een dienst: de eigen pagina als die in deze build zit, anders het anker op /diensten/."""
    pad = DIENST_PAGINA.get(sleutel)
    if pad and pad in zichtbaar:
        return f"{d}{pad}#dienst", f"{d}{pad}"
    return f"{d}/diensten/#{sleutel}", f"{d}/diensten/#{sleutel}"


def diensten(pagina, ctx):
    """Service-knooppunten op /diensten/, elk met het anker van zijn blok (of zijn eigen pagina, als die live is)."""
    d = _domein(ctx)
    namen = dict(DIENSTEN)
    k = _kopij(pagina, ctx)
    for sleutel, _ in DIENSTEN:
        b = _blok(k, sleutel)
        kop = getattr(b, "kop", None) if b is not None else None
        if kop:
            namen[sleutel] = _platte_tekst(kop)
    zichtbaar = _zichtbaar()
    uit = []
    for sleutel, _ in DIENSTEN:
        id_, url = _dienst_adres(d, sleutel, zichtbaar)
        uit.append({
            "@type": "Service",
            "@id": id_,
            "name": namen[sleutel],
            "url": url,
            "provider": {"@id": f"{d}/#bedrijf"},
            "areaServed": {"@type": "Country", "name": "Nederland"},
        })
    return uit


def _h1(pagina, ctx):
    """De H1 uit de kopij zonder opmaak, of de titel. Een kop met een nog niet ingevuld {FEIT} telt niet."""
    doc = _kopij(pagina, ctx)
    kop = getattr(getattr(doc, "h1", None), "kop", None)
    if kop and "{" not in kop:
        return _platte_tekst(kop)
    titel = _veld(pagina, "titel", ctx) or ""
    return titel.split("|")[0].strip() or None


def dienstpagina(pagina, ctx):
    """Eén Service-knoop voor een eigen dienst-, doelgroep-, landen- of plaatspagina; None voor andere pagina's.
    Het @id is gelijk aan dat op /diensten/, zodat beide pagina's naar dezelfde dienst wijzen."""
    d = _domein(ctx)
    pad = getattr(pagina, "pad", "/")
    plaats, land = _PLAATS_PAD.match(pad), _LAND_PAD.match(pad)
    is_dienst = pad.startswith("/diensten/") and pad != "/diensten/" and pad.count("/") == 3
    if not (plaats or land or is_dienst):
        return None
    knoop = {
        "@type": "Service",
        "@id": f"{d}{pad}#dienst",
        "url": f"{d}{pad}",
        "provider": {"@id": f"{d}/#bedrijf"},
        "mainEntityOfPage": {"@id": f"{d}{pad}#pagina"},
    }
    naam, beschrijving = _h1(pagina, ctx), _veld(pagina, "beschrijving", ctx)
    if naam:
        knoop["name"] = naam
    if beschrijving:
        knoop["description"] = beschrijving
    if plaats:
        knoop["areaServed"] = _plaats(plaats.group(1))
    elif land:
        slug = land.group(1)
        knoop["areaServed"] = {"@type": "Country", "name": LANDEN.get(slug, slug.title())}
    elif pad == INTERNATIONAAL:
        # alleen landen die de klant heeft bevestigd (config.FEITEN LANDEN, open vraag 5.1)
        landen = _feit(ctx, "LANDEN") or []
        knoop["areaServed"] = [{"@type": "Country", "name": "Nederland"}] + [
            {"@type": "Country", "name": str(l)} for l in landen]
    else:
        knoop["areaServed"] = {"@type": "Country", "name": "Nederland"}
    return knoop


def voor(pagina, ctx):
    """De JSON-LD van een pagina als dict, of None."""
    if getattr(pagina, "noindex", False):
        return None
    graaf = [bedrijf(ctx), website(ctx), webpagina(pagina, ctx)]
    pad = getattr(pagina, "pad", "/")
    if pad == "/diensten/":
        graaf += diensten(pagina, ctx)
    dienst = dienstpagina(pagina, ctx)
    if dienst:
        graaf.append(dienst)
    faq = vragen(pagina, ctx)
    if faq:
        graaf.append(faq)
    return {"@context": "https://schema.org", "@graph": graaf}


def als_script(obj):
    """Veilig serialiseren voor in de <head>: geen </script> of <!-- in de uitvoer."""
    if not obj:
        return ""
    tekst = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    tekst = tekst.replace("</", "<\\/").replace("<!--", "<\\!--")
    return f'<script type="application/ld+json">{tekst}</script>'
