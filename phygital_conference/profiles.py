# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only
"""Built-in country profiles for the phygital conference generator.

These are starting points, not claims: venues, funding bodies, and
organizations are the ones already on file for Spark AI NLP. A new country
copies one of these, fills in its own facts, and the generator validates it
before anything is written. Nothing here asserts a partnership, a booking,
or funding.
"""

BUILTIN_PROFILES = {
    "canada": {
        "country": "Canada",
        "languages": ["English", "French"],
        "cultural_authorities": [
            "First Nations communities",
            "Acadian communities",
            "local cultural organizations",
        ],
        "flagship_sectors": ["tourism", "museums", "hotels", "retail"],
        "venues": [
            "Delta Hotels Fredericton Grand Ballroom (booking and date blank)",
            "conference centres, museums, hotels",
        ],
        "funding_body": "ACOA - Regional Artificial Intelligence Initiative (RAII), Stream 2",
        "disability_organizations": [
            "local disability organizations (named per city)",
        ],
        "consent_law": "Canadian privacy and consent law; Indigenous data "
        "governance per community",
        "currency_note": "Quote in CAD in Canada and USD internationally.",
        "notes": "Home base. Fredericton flagship first; then Moncton-Dieppe, "
        "Saint John, Edmundston / Haut-Madawaska; then Atlantic Canada.",
    },
    "morocco": {
        "country": "Morocco",
        "languages": ["French", "Arabic", "Tamazight"],
        "cultural_authorities": [
            "Amazigh communities",
            "Arab communities",
            "local cultural organizations",
        ],
        "flagship_sectors": ["tourism", "crafts", "heritage sites", "hotels"],
        "venues": [
            "conference centres (urbanization conferences)",
            "museums, hotels",
        ],
        "funding_body": "To be confirmed with the Moroccan counterpart",
        "disability_organizations": [
            "local disability organizations (named per city)",
        ],
        "consent_law": "Moroccan data-protection law (Law 09-08); community "
        "consent per cultural authority",
        "currency_note": "Quote in USD internationally; local currency "
        "to be confirmed per event.",
        "notes": "Live conversation: a contact connected to the Morocco "
        "government who runs urbanization conferences. Casablanca leg in the "
        "WorldHoloBridge concept; Casa Holo is the separate community-centre "
        "concept for Casablanca. No partner, funding, or endorsement claimed.",
    },
    "germany": {
        "country": "Germany",
        "languages": ["German", "English"],
        "cultural_authorities": [
            "regional cultural organizations",
            "local community bodies",
        ],
        "flagship_sectors": ["museums", "tourism", "retail", "trade fairs"],
        "venues": ["conference centres", "museums", "trade-fair halls"],
        "funding_body": "To be confirmed with the German counterpart",
        "disability_organizations": [
            "local disability organizations (named per city)",
        ],
        "consent_law": "GDPR; community consent per cultural authority",
        "currency_note": "Quote in USD internationally; local currency "
        "to be confirmed per event.",
        "notes": "Poster country (German eagle). No partner or venue claimed.",
    },
    "france": {
        "country": "France",
        "languages": ["French", "English"],
        "cultural_authorities": [
            "regional cultural organizations",
            "local community bodies",
        ],
        "flagship_sectors": ["museums", "tourism", "retail", "culture"],
        "venues": ["conference centres", "museums", "cultural venues"],
        "funding_body": "To be confirmed with the French counterpart",
        "disability_organizations": [
            "local disability organizations (named per city)",
        ],
        "consent_law": "GDPR; community consent per cultural authority",
        "currency_note": "Quote in USD internationally; local currency "
        "to be confirmed per event.",
        "notes": "Poster country (Gallic rooster). No partner or venue claimed.",
    },
    "united-kingdom": {
        "country": "United Kingdom",
        "languages": ["English"],
        "cultural_authorities": [
            "regional cultural organizations",
            "local community bodies",
        ],
        "flagship_sectors": ["museums", "tourism", "retail", "culture"],
        "venues": ["conference centres", "museums", "cultural venues"],
        "funding_body": "To be confirmed with the UK counterpart",
        "disability_organizations": [
            "local disability organizations (named per city)",
        ],
        "consent_law": "UK GDPR; community consent per cultural authority",
        "currency_note": "Quote in USD internationally; local currency "
        "to be confirmed per event.",
        "notes": "Poster country (British bulldog). No partner or venue claimed.",
    },
}
