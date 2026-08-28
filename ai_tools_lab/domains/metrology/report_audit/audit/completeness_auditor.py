"""Flags missing required fields (report number, instrument info, conclusion, ...)."""
from __future__ import annotations

from ai_tools_lab.domains.metrology.report_audit.extraction.result import ExtractionResult
from ai_tools_lab.domains.metrology.report_audit.models.finding import AuditFinding
from ai_tools_lab.domains.metrology.report_audit.rules.rule_engine import check_required_fields
from ai_tools_lab.domains.metrology.report_audit.rules.rule_repository import (
    load_required_field_rules,
)


class CompletenessAuditor:
    def audit(self, extraction: ExtractionResult) -> list[AuditFinding]:
        return check_required_fields(extraction.report, load_required_field_rules())
