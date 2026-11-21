# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only
"""Holographic phygital conference plan generator.

One core, any country. See generator.py for the fixed ACOA core and
profiles.py for the built-in country profiles.
"""

from .generator import (
    CountryProfile,
    generate,
    list_builtin_countries,
    render_plan,
)

__all__ = [
    "CountryProfile",
    "generate",
    "list_builtin_countries",
    "render_plan",
]
