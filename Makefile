# Copyright (c) 2026 Jean-Francois Brisson (Spark AI NLP)
# SPDX-License-Identifier: AGPL-3.0-only
PYTHON ?= python3

.PHONY: test demo clean

test:
	$(PYTHON) -m pytest tests/ -q

demo:
	$(PYTHON) -m phygital_conference --country Morocco --output examples/morocco-conference-plan.md
	$(PYTHON) -m phygital_conference --country Canada --output examples/canada-conference-plan.md

clean:
	rm -rf .pytest_cache __pycache__ phygital_conference/__pycache__ tests/__pycache__
