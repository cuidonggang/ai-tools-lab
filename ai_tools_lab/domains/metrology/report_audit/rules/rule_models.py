"""Config-backed rule definitions loaded from configs/metrology/report_audit/rules.yaml."""
from __future__ import annotations

from pydantic import BaseModel

from ai_tools_lab.domains.metrology.report_audit.models.finding import Severity


class RequiredFieldRule(BaseModel):
    """Declares that a Report field path must be present (non-empty) for completeness."""

    path: str
    severity: Severity
    message: str


class DateCheckRule(BaseModel):
    """Enables/configures one of the named date-consistency checks implemented in code."""

    id: str
    enabled: bool = True
    severity: Severity
    message: str
