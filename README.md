# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only
# Holographic Phygital Conference Plan Generator

One core, any country. A small, standard-library Python program that
generates a WorldHoloBridge conference plan for one country from a country
profile. The ACOA brief is the fixed content (phases, holographic tiers,
governance rules, demo tiers, the 90-day pilot); the country profile is the
variable content (languages, cultural authorities, sectors, venues,
funding body, disability organizations, consent law).

## Run it

```bash
python -m phygital_conference --country Morocco --output examples/morocco-conference-plan.md
python -m phygital_conference --country Canada --output examples/canada-conference-plan.md
python -m phygital_conference --list-countries
```

Example plans for Morocco and Canada are already generated in `examples/`.

## Add a country

Copy `profiles/canada.json`, fill in the fields, and run it:

```bash
python -m phygital_conference --profile profiles/spain.json --output examples/spain-conference-plan.md
```

No code change. A profile is validated before anything is written: every
required field must be present, and the governance checklist is always
emitted in full — a profile cannot silently drop a rule. Venue and date
stay blank in every generated plan until confirmed.

## Built-in profiles

Canada, Morocco, Germany, France, United Kingdom — the five poster
countries. The profiles are starting points, not claims: they name the
counterparts and venues already on file, and say "to be confirmed" where
nothing is confirmed.

## Tests

```bash
python -m pytest tests/ -q
```

Every generated plan is checked for all six phases, all five holographic
tiers, both worked examples (Hall of Memory museum, Cadre artistique
publicity), the full twelve-rule governance checklist, and the demo tiers
at the adopted prices. A plan that fails any of those checks is not
written.

## What it sells

The code is open (AGPL-3.0). What is sold is deployment, customization,
training, and the conference itself: hosted plan generation as a service,
a per-country customization, training for the local team, and the
conference delivered with the generated plan. See the companion plan,
`docs/holographic-phygital-society-plan.md`, for the full framework — the
sellable software and the AI governance rules.

## Provenance — only sparkainlp-x ideas

All ideas in this package are sparkainlp-x's own, from the ACOA brief,
the WorldHoloBridge governance prototype, and the Spark AI Matrix. The
only outside names in the code and docs are third-party products stated
as products (Looking Glass light-field displays, the Sony ELF-MN1) and
the Marie Curie example figure in the Hall of Memory — named as a
product and an example, never claimed as an idea. No other author's
theory, model, or concept is imported. `CITATION.cff` lists Brisson as
the sole author.

## Related

- WorldHoloBridge governance reference prototype — DOI 10.5281/zenodo.23423941
- Spark AI Matrix — DOI 10.5281/zenodo.23644437
- sparkainlpx.xyz

## License

Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP).
SPDX-License-Identifier: AGPL-3.0-only
