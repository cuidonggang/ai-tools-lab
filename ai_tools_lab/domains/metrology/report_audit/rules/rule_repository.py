"""Loads required-field and date-check rule configuration from YAML."""
from __future__ import annotations

from functools import lru_cache

from ai_tools_lab.core.config import load_yaml
from ai_tools_lab.domains.metrology.report_audit.rules.rule_models import (
    DateCheckRule,
    RequiredFieldRule,
)


@lru_cache(maxsize=1)
def load_required_field_rules() -> list[RequiredFieldRule]:
    data = load_yaml("metrology/report_audit/rules.yaml")
    return [RequiredFieldRule(**item) for item in data.get("required_fields", [])]


@lru_cache(maxsize=1)
def load_date_check_rules() -> dict[str, DateCheckRule]:
    data = load_yaml("metrology/report_audit/rules.yaml")
    rules = [DateCheckRule(**item) for item in data.get("date_checks", [])]
    return {rule.id: rule for rule in rules}
