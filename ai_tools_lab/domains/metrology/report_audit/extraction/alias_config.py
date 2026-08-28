"""Loads the label/column alias maps that map raw report text onto Report fields.

Keeping these in YAML (rather than hard-coded in Python) lets each metrology
specialty extend field/column recognition without touching extraction code.
"""
from __future__ import annotations

from functools import lru_cache

from ai_tools_lab.core.config import load_yaml


@lru_cache(maxsize=1)
def load_field_aliases() -> dict[str, list[str]]:
    """Map: canonical Report field path -> list of raw-text labels referring to it."""
    data = load_yaml("metrology/report_audit/field_aliases.yaml")
    return data.get("fields", {})


@lru_cache(maxsize=1)
def load_column_aliases() -> dict[str, list[str]]:
    """Map: canonical MeasurementRow field name -> list of raw table header labels."""
    data = load_yaml("metrology/report_audit/column_aliases.yaml")
    return data.get("columns", {})


def build_label_lookup(aliases: dict[str, list[str]]) -> dict[str, str]:
    """Invert an alias map (canonical -> [labels]) into label -> canonical for O(1) lookup."""
    lookup: dict[str, str] = {}
    for canonical_path, labels in aliases.items():
        for label in labels:
            lookup[label] = canonical_path
    return lookup
