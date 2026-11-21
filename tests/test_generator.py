# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the phygital conference plan generator.

The generator's contract: every plan it writes contains all six phases,
all five holographic tiers, both worked examples, the full twelve-rule
governance checklist, and the demo tiers at the adopted prices. A plan
that fails any of those checks is not written.
"""

import json

import pytest

from phygital_conference import CountryProfile, generate, render_plan
from phygital_conference.generator import (
    DEMO_TIERS,
    GOVERNANCE_RULES,
    PHASES,
    TIERS,
)


def test_all_builtin_profiles_are_valid():
    for name in ["Canada", "Morocco", "Germany", "France", "United Kingdom"]:
        profile = CountryProfile.builtin(name)
        assert profile.country == name
        assert profile.languages
        assert profile.cultural_authorities
        assert profile.flagship_sectors


def test_unknown_country_raises():
    with pytest.raises(ValueError, match="no built-in profile"):
        CountryProfile.builtin("Atlantis")


def test_missing_profile_field_raises():
    data = CountryProfile.builtin("Canada").__dict__.copy()
    del data["funding_body"]
    with pytest.raises(ValueError, match="missing required fields"):
        CountryProfile.from_dict(data)


def test_custom_json_profile_round_trips(tmp_path):
    data = {
        "country": "Spain",
        "languages": ["Spanish", "English"],
        "cultural_authorities": ["regional cultural organizations"],
        "flagship_sectors": ["tourism", "museums"],
        "venues": ["conference centres", "museums"],
        "funding_body": "To be confirmed with the Spanish counterpart",
        "disability_organizations": ["local disability organizations"],
        "consent_law": "GDPR; community consent per cultural authority",
        "currency_note": "Quote in USD internationally.",
    }
    path = tmp_path / "spain.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    profile = CountryProfile.from_json_file(path)
    assert profile.country == "Spain"
    text = render_plan(profile)
    assert "Spain" in text
    assert "Spanish" in text
    assert "tourism" in text


@pytest.mark.parametrize("country", ["Canada", "Morocco"])
def test_plan_contains_all_six_phases(country):
    text = render_plan(CountryProfile.builtin(country))
    for num, name, _, _ in PHASES:
        assert f"Phase {num} - {name}" in text


@pytest.mark.parametrize("country", ["Canada", "Morocco"])
def test_plan_contains_all_five_holographic_tiers(country):
    text = render_plan(CountryProfile.builtin(country))
    for code, tech, _, _, _ in TIERS:
        assert f"{code} - {tech}" in text


@pytest.mark.parametrize("country", ["Canada", "Morocco"])
def test_plan_contains_both_worked_examples(country):
    text = render_plan(CountryProfile.builtin(country))
    assert "Hall of Memory" in text
    assert "Cadre artistique" in text
    assert "Marie Curie" in text


@pytest.mark.parametrize("country", ["Canada", "Morocco"])
def test_plan_contains_the_full_governance_checklist(country):
    text = render_plan(CountryProfile.builtin(country))
    assert len(GOVERNANCE_RULES) == 12
    for i, (title, _) in enumerate(GOVERNANCE_RULES, 1):
        assert f"{i}. **{title}.**" in text
    assert "Sponsor firewall" in text
    assert "Guardrails cannot be disabled" in text


@pytest.mark.parametrize("country", ["Canada", "Morocco"])
def test_plan_contains_demo_tiers_at_adopted_prices(country):
    text = render_plan(CountryProfile.builtin(country))
    for name, _, price in DEMO_TIERS:
        assert name in text
        assert price in text
    assert "$2,000-$3,500" in text
    assert "$5,000-$8,500" in text
    assert "$11,000-$21,000" in text


@pytest.mark.parametrize("country", ["Canada", "Morocco"])
def test_plan_names_the_country_and_its_languages(country):
    profile = CountryProfile.builtin(country)
    text = render_plan(profile)
    assert profile.country in text
    for lang in profile.languages:
        assert lang in text


@pytest.mark.parametrize("country", ["Canada", "Morocco"])
def test_plan_leaves_venue_and_date_blank(country):
    text = render_plan(CountryProfile.builtin(country))
    assert "blank until confirmed" in text


def test_generate_writes_the_plan(tmp_path):
    out = generate(CountryProfile.builtin("Morocco"), tmp_path / "morocco.md")
    assert out.exists()
    assert "Morocco" in out.read_text(encoding="utf-8")
