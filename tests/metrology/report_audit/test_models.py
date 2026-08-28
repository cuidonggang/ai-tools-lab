"""Smoke tests for Pydantic model serialization round-trips."""
from __future__ import annotations

from ai_tools_lab.domains.metrology.report_audit.models.finding import (
    AuditFinding,
    Category,
    Severity,
)
from ai_tools_lab.domains.metrology.report_audit.models.report import Report


def test_report_round_trip() -> None:
    report = Report(customer="某单位")
    restored = Report.model_validate_json(report.model_dump_json())
    assert restored.customer == "某单位"


def test_finding_requires_category_and_severity() -> None:
    finding = AuditFinding(
        category=Category.CALCULATION,
        severity=Severity.ERROR,
        title="t",
        description="d",
        source="rule",
    )
    assert finding.id
    assert finding.review_state.value == "ai_detected"
