# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only
"""Holographic phygital conference plan generator.

One core, any country. The ACOA brief is the fixed content (phases,
holographic tiers, governance rules, demo tiers, the 90-day pilot); the
country profile is the variable content (languages, cultural authorities,
sectors, venues, funding body, disability organizations, consent law).

Standard library only. No framework, no cloud dependency, no account.

Usage:
    python -m phygital_conference --country Morocco --output plans/morocco.md
    python -m phygital_conference --country Canada --output plans/canada.md
    python -m phygital_conference --list-countries
    python -m phygital_conference --profile profiles/spain.json --output plans/spain.md
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .profiles import BUILTIN_PROFILES

COPYRIGHT = "Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)"
LICENSE = "AGPL-3.0-only"

# ---------------------------------------------------------------------------
# The fixed core (from the ACOA brief v2 and the WorldHoloBridge prototype).
# A country profile can never change these; it can only fill in its own
# fields around them.
# ---------------------------------------------------------------------------

PHASES = [
    ("0", "Country profile",
     "Languages, cultural authorities, flagship sectors, venues, funding "
     "body, disability organizations, consent law. Written down, not assumed.",
     "Profile complete and reviewed by a local contact"),
    ("1", "Discovery & consent",
     "Map the cultural authority for every story and persona. Set the "
     "sponsor firewall. Name the accessibility lead, the technical lead, "
     "and the privacy lead.",
     "Cultural authority named; firewall agreed in writing"),
    ("2", "Pilot demos",
     "Demos by appointment (Demo 1/2/3). One museum pilot and one publicity "
     "pilot, each small, each measured.",
     "Paid demand tested; delivery costs recorded"),
    ("3", "Flagship conference",
     "One day. Public educational session (60-75 minutes) plus 4-6 private "
     "briefings of 20-30 minutes for pre-qualified leads. Five zones.",
     "Targets set: 75-125 attendees, 4-6 briefings, 25+ leads, 3+ proposals, "
     "1-2 paid pilots in 6 months"),
    ("4", "Community Centre pilot",
     "90-day Country Node pilot. One room, one supervised AI persona, a "
     "defined host agreement. Evidence Passport at the end.",
     "Passport complete; stop rules respected"),
    ("5", "National node & region",
     "Repeat what worked. Establish service capacity. Only then consider "
     "the next country or region - stages, never a blitz.",
     "Contracts closing in the current country or the equivalent evidence"),
]

ZONES = [
    ("Welcome & proof", "The display working, in the open, with a person "
     "operating it. Visitors see it first, before any pitch."),
    ("Business demos", "The Demo tiers running. Pre-qualified briefings "
     "by appointment."),
    ("Museum corner", "A Hall of Memory station and a light-field artefact "
     "display."),
    ("Publicity corner", "A Cadre artistique frame with a live QR/NFC offer."),
    ("Governance corner", "The consent register, the audit log, and the "
     "Evidence Passport on display - governance you can point at."),
]

PILOT_STAGES = [
    ("Days 1-14, Preparation",
     "Approvals: cultural authority, accessibility lead, technical lead, "
     "privacy, governance firewall, AI persona lease, display and fan safety "
     "review. Evidence Passport created."),
    ("Days 15-30, Soft launch",
     "Controlled opening, mediator-led sessions, issues logged."),
    ("Days 31-75, Public pilot",
     "Public operation; participation and engagement measured in aggregate."),
    ("Days 76-90, Review",
     "Completed Country Node Evidence Passport: participation, accessibility, "
     "safety, governance, technical findings, lessons learned."),
]

PILOT_STOP_RULES = [
    "cultural-authority withdrawal",
    "a serious accessibility, privacy, or safety failure",
    "repeated harmful AI output",
    "a governance breach",
    "an unresolved hardware risk",
]

TIERS = [
    ("H1", "LED fan display",
     "A strip of LEDs spins fast enough that persistence of vision blends "
     "the lit points into a floating image. Simple steps, in the right "
     "order, very fast, with the eyes doing the last step.",
     "Every demo, every event. The workhorse.",
     "Flat plane, not a volume. No depth, occlusion, or parallax. Needs a "
     "dark background; weak in bright daylight."),
    ("H2", "Frame-art prototype",
     "Battery-powered, wall-mountable frame showing holographic-style art "
     "and offers, with NFC/QR. In development.",
     "Shops, hotel lobbies, visitor venues. Gift-card incentive and tourism "
     "interaction.",
     "Concept today. No launch date, no price promised. A real merchant "
     "offer and a tested QR/NFC destination come first."),
    ("H3", "Multi-fan wall",
     "Fans tiled into a wall (up to a 12-fan wall).",
     "Event-scale stages, atriums, flagship days.",
     "Same flat-plane limit as H1, at larger scale. Safety review before "
     "every public session."),
    ("H4", "Light-field display",
     "True depth to several viewers at once, no glasses or headset. Looking "
     "Glass sells 16, 27, and 86-inch units; Sony ELF-MN1 (6-inch, eye "
     "tracking, ~US$343) released in Japan December 11, 2026.",
     "Museum artefacts and premium pieces - objects too fragile to handle, "
     "shown in depth.",
     "Higher price; the Sony unit serves one viewer with a narrow content "
     "library."),
    ("H5", "Wavefront holography",
     "Reconstructing light fields with spatial light modulators, rather "
     "than showing a flat image.",
     "Research direction only.",
     "Development-stage technology, not a commercial product. Spark claims "
     "nothing in this tier."),
]

GOVERNANCE_RULES = [
    ("Consent first",
     "No story is shared without approval from the creators and communities "
     "authorized to grant it. Consent carries an expiry, a withdrawal path, "
     "and prohibited uses. Indigenous material only by a contributor flagged "
     "as an Indigenous governance authority, never for external AI training."),
    ("Cultural authority approves every story",
     "The authority controls story approval, persona scope, content removal, "
     "and sponsor visibility within cultural stories."),
    ("Sponsor firewall",
     "Sponsors may fund infrastructure, equipment, connectivity, translation, "
     "venue costs, or events. Sponsors may not approve, edit, veto, or "
     "control community stories."),
    ("Human oversight",
     "AI-generated advertising and community content is reviewed by a person "
     "before public display. No fully automated public content."),
    ("Honest avatars",
     "Every avatar is clearly labelled an AI representation, based on sourced "
     "material, correctable openly, and never presented as the real person. "
     "No avatars of living people without explicit consent."),
    ("Privacy by design",
     "Minimum personal information collected. Engagement measured in "
     "aggregate, not by surveillance or visitor tracking. Avatars do not "
     "retain personal conversations. Session memory is cleared at the end of "
     "every visit."),
    ("Honest claims",
     "No verified lower bound, no headline. Negative findings, denominators, "
     "and uncertainty are reported, not hidden."),
    ("Audit ledger",
     "Every approval, change, incident, and firewall check is recorded in an "
     "append-only log."),
    ("Guardrails cannot be disabled",
     "A property of the reference prototype; a governed deployment keeps it "
     "that way."),
    ("Accessibility is a gate, not a feature",
     "Four accessibility features required before publication. Target: WCAG "
     "2.2 AA. Disability-led, with people with disabilities on the team, "
     "not as an afterthought."),
    ("Defensive, human-gated, non-lethal",
     "The mission is AI for humanity. No autonomous lethal use, no "
     "targeting. Ever."),
    ("Open by default",
     "The prototype and the generator are open code. What is sold is "
     "deployment, customization, training, and the conference - not secrecy."),
]

DEMO_TIERS = [
    ("Demo 1 - HoloBridge Spotlight",
     "Up to 4 hours; 2 LED fans, 1 adjustable frame, 1 AI persona demo, "
     "1 NFC/QR story stop, 1 table or booth",
     "$2,000-$3,500"),
    ("Demo 2 - Country Node Experience",
     "Up to 8 hours; 5 LED fans, 2 frames, AI persona demo, 3 NFC/QR story "
     "stops, accessibility information station",
     "$5,000-$8,500"),
    ("Demo 3 - WorldHoloBridge Arena",
     "Up to 2 days; 10 LED fans, 3-4 frames, multi-fan wall, AI persona "
     "demo, 5 NFC/QR stops, guided community storytelling session, Evidence "
     "Passport and assurance display",
     "$11,000-$21,000"),
]

ONGOING_SERVICES = [
    ("Project contracts", "$2,000-$50,000 per project"),
    ("Monthly programming", "$1,500 per month, minimum term 3-6 months"),
    ("Event activations", "$3,500-$18,000"),
    ("Seasonal installations", "$8,000-$35,000+"),
]

REQUIRED_PROFILE_FIELDS = (
    "country", "languages", "cultural_authorities", "flagship_sectors",
    "venues", "funding_body", "disability_organizations", "consent_law",
    "currency_note",
)


@dataclass
class CountryProfile:
    """The variable content for one country. Everything else is the core."""

    country: str
    languages: list[str]
    cultural_authorities: list[str]
    flagship_sectors: list[str]
    venues: list[str]
    funding_body: str
    disability_organizations: list[str]
    consent_law: str
    currency_note: str
    notes: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "CountryProfile":
        missing = [f for f in REQUIRED_PROFILE_FIELDS if f not in data]
        if missing:
            raise ValueError(
                f"country profile is missing required fields: "
                f"{', '.join(missing)}"
            )
        return cls(
            country=data["country"],
            languages=list(data["languages"]),
            cultural_authorities=list(data["cultural_authorities"]),
            flagship_sectors=list(data["flagship_sectors"]),
            venues=list(data["venues"]),
            funding_body=data["funding_body"],
            disability_organizations=list(data["disability_organizations"]),
            consent_law=data["consent_law"],
            currency_note=data["currency_note"],
            notes=data.get("notes", ""),
        )

    @classmethod
    def from_json_file(cls, path: str | Path) -> "CountryProfile":
        with open(path, encoding="utf-8") as fh:
            return cls.from_dict(json.load(fh))

    @classmethod
    def builtin(cls, name: str) -> "CountryProfile":
        key = name.strip().lower().replace(" ", "-")
        for slug, data in BUILTIN_PROFILES.items():
            if slug == key or data["country"].lower() == name.strip().lower():
                return cls.from_dict(data)
        raise ValueError(
            f"no built-in profile for {name!r}; available: "
            f"{', '.join(sorted(BUILTIN_PROFILES))} "
            f"(or pass --profile with a JSON file)"
        )


def list_builtin_countries() -> list[str]:
    return sorted(d["country"] for d in BUILTIN_PROFILES.values())


def _bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def render_plan(profile: CountryProfile) -> str:
    """Render the full conference plan for one country as Markdown.

    The governance checklist is always emitted in full; a profile cannot
    silently drop a rule. Venue and date stay blank until confirmed.
    """
    langs = ", ".join(profile.languages)
    sectors = ", ".join(profile.flagship_sectors)
    authorities = ", ".join(profile.cultural_authorities)
    venues = ", ".join(profile.venues)
    orgs = ", ".join(profile.disability_organizations)

    phases = "\n".join(
        f"### Phase {num} - {name}\n\n{desc}\n\n**Gate:** {gate}\n"
        for num, name, desc, gate in PHASES
    )
    zones = "\n".join(f"{i}. **{t}.** {d}" for i, (t, d) in enumerate(ZONES, 1))
    pilot = "\n".join(
        f"- **{stage}.** {desc}" for stage, desc in PILOT_STAGES
    )
    stops = ", ".join(PILOT_STOP_RULES)
    tiers = "\n".join(
        f"### {code} - {tech}\n\n{what}\n\n**Fits:** {fits}\n\n"
        f"**Honest limit:** {limit}\n"
        for code, tech, what, fits, limit in TIERS
    )
    rules = "\n".join(
        f"{i}. **{title}.** {text}"
        for i, (title, text) in enumerate(GOVERNANCE_RULES, 1)
    )
    demos = "\n".join(
        f"| {name} | {contents} | {price} CAD |"
        for name, contents, price in DEMO_TIERS
    )
    services = "\n".join(
        f"- **{name}:** {price} CAD" for name, price in ONGOING_SERVICES
    )

    return f"""# WorldHoloBridge Conference Plan - {profile.country}

**Holographic Phygital Society · One conference, two engines**

Jean-François Brisson, Founder, Spark AI NLP
sparkainlpx.xyz | frederictonholograms.com | 506-478-1790 | frederictonholo@gmail.com

*Status: a working plan, not a promise. No partner, sponsor, funder, venue, or
endorsement is claimed unless confirmed in writing for a specific event.
Venue and date are blank until confirmed.*

---

## Country profile - {profile.country}

- **Languages:** {langs}
- **Cultural authorities:** {authorities}
- **Flagship sectors:** {sectors}
- **Venues:** {venues}
- **Funding body:** {profile.funding_body}
- **Disability organizations:** {orgs}
- **Consent law:** {profile.consent_law}
- **Currency:** {profile.currency_note}
{f"- **Notes:** {profile.notes}" if profile.notes else ""}

## 1. The idea

One conference, two engines. Engine 1 is holographic marketing for local
businesses; Engine 2 is a governed AI Community Centre where creators lead
the cultural design. The Spark AI Matrix is the platform
(doi.org/10.5281/zenodo.23644437); WorldHoloBridge is the program
(doi.org/10.5281/zenodo.23423941). Demos by appointment: people come, see
the display working with their own eyes, then decide.

## 2. The conference, phase by phase

{phases}
### The flagship day - five zones

{zones}

### The 90-day Country Node pilot

{pilot}

**Stop rules.** Pause or stop for {stops}.

## 3. Holographic technology, phase by phase

The hardware improves every year and falls in price. The durable layer is the
service around it. Spark builds no display hardware and claims no proprietary
display technology. Three holographies, kept distinct: optical wavefront
holography (research), membrane holographic memory (research models), and
LED fan display (what the conferences actually use).

{tiers}
## 4. Worked examples for {profile.country}

### 4.1 Museum - the Hall of Memory

One room, one supervised AI persona, a defined host agreement. An accessible
space where participants explore approved local history, ask questions, and
contribute stories through a consent-based process. Fragile objects are shown
on a light-field display (H4) in depth - seen, never handled. Everyday
objects are shown on the LED fan (H1). The first avatar in the pilot document
is Marie Curie; the figure is swappable per museum and per community, with
the community's approval. Flagship sectors here: {sectors}. Cultural
authorities: {authorities}.

### 4.2 Publicity - the Cadre artistique

A wall-mountable artistic frame with a holographic display and a QR code.
The frame carries the business's own art; the display carries the offer;
the QR code carries the promo and the gift card. A real merchant offer with
a real, tested QR/NFC destination - no invented discount, no fake QR.
Monthly programming keeps the offer fresh. Flagship sectors here: {sectors}.

## 5. AI governance - the twelve rules

{rules}

## 6. Money - the offer

All amounts are the adopted Canadian-dollar bands, per event, travel
excluded. {profile.currency_note}

| Package | What it includes | Price |
|---|---|---|
{demos}

Terms: 30% deposit to reserve the date, 50% before equipment shipment or
setup, 20% after the demo. Demo 1 has a $1,500 floor, local only.

**Ongoing services:**

{services}

Installations: 40% deposit to order hardware, 50% on delivery/installation,
10% on sign-off. The 12-fan wall is $1,500-$3,500 per event day, hardware
only - it is not a Demo 3, and it is not sold as one.

## 7. What we will not claim

- No partner, sponsor, funder, venue, or endorsement unless confirmed in
  writing for a specific event.
- No funding claimed until confirmed. An Expression of Interest submitted is
  a submission, not a grant.
- No signed customer claimed. Businesses in second-meeting discussion are
  exactly that - not clients.
- No "5x attention", no "+30% foot traffic", no invented discount, no fake
  QR. Numbers are measured or they are not stated.
- No launch date or price for the frame-art prototypes until a real merchant
  offer and a tested QR/NFC destination exist.
- No wavefront holography product. No proprietary display technology. No
  medical or therapeutic claim.

---

*{COPYRIGHT}. All rights reserved - shared for partnership discussion under
NDA on request.*
"""


def generate(profile: CountryProfile, output: str | Path) -> Path:
    """Validate the profile, render the plan, and write it. Returns the path."""
    text = render_plan(profile)
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    return out
