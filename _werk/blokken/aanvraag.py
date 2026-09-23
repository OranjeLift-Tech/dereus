"""Het offerteblok uit main, met het gedeelde formulier en eigen veld-id's op de home."""
NAAM = "aanvraag"
CSS = False
JS = False
AFHANKELIJK = ["formulier"]


def html(ctx, kopij, **opties):
    return ctx.register["formulier"].html(
        ctx, ctx.kopij_van("offerte").blok("formulier"),
        id="aanvraag", prefix="aanvraag", beeld="/img/verhuizer-doos-zijgreep-uit.webp",
    )
