"""Applies deterministic date-consistency rules (expired standards, date ordering, ...)."""
from __future__ import annotations

from ai_tools_lab.domains.metrology.report_audit.extraction.result import ExtractionResult
from ai_tools_lab.domains.metrology.report_audit.models.finding import AuditFinding
from ai_tools_lab.domains.metrology.report_audit.rules.rule_engine import check_date_rules
from ai_tools_lab.domains.metrology.report_audit.rules.rule_repository import (
    load_date_check_rules,
)


class RuleAuditor:
    def audit(self, extraction: ExtractionResult) -> list[AuditFinding]:
        return check_date_rules(extraction.report, load_date_check_rules())
