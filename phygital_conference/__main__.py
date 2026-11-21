# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only
"""Command line for the phygital conference plan generator.

    python -m phygital_conference --country Morocco --output plans/morocco.md
    python -m phygital_conference --country Canada --output plans/canada.md
    python -m phygital_conference --list-countries
    python -m phygital_conference --profile profiles/spain.json --output plans/spain.md
"""

from __future__ import annotations

import argparse
import sys

from .generator import CountryProfile, generate, list_builtin_countries


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="phygital_conference",
        description="Generate a WorldHoloBridge conference plan for one country.",
    )
    parser.add_argument("--country", help="Built-in country profile to use")
    parser.add_argument("--profile", help="Path to a custom country profile (JSON)")
    parser.add_argument("--output", "-o", help="Where to write the plan (Markdown)")
    parser.add_argument("--list-countries", action="store_true",
                        help="List the built-in country profiles and exit")
    args = parser.parse_args(argv)

    if args.list_countries:
        for name in list_builtin_countries():
            print(name)
        return 0

    if args.profile:
        profile = CountryProfile.from_json_file(args.profile)
    elif args.country:
        profile = CountryProfile.builtin(args.country)
    else:
        parser.error("pass --country or --profile (or --list-countries)")

    if not args.output:
        parser.error("--output is required to write the plan")

    out = generate(profile, args.output)
    print(f"Wrote {out} ({profile.country})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
