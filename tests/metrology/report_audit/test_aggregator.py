"""Unit test for finding aggregation into an AuditResult with severity summary."""
from __future__ import annotations

from ai_tools_lab.domains.metrology.report_audit.audit.aggregator import aggregate_findings
from ai_tools_lab.domains.metrology.report_audit.models.finding import (
    AuditFinding,
    Category,
    Severity,
)


def test_aggregate_findings_produces_summary_counts() -> None:
    findings = [
        AuditFinding(
            category=Category.COMPLETENESS, severity=Severity.ERROR, title="a", description="a", source="rule"
        ),
        AuditFinding(
            category=Category.CONSISTENCY,
            severity=Severity.WARNING,
            title="b",
            description="b",
            source="consistency",
        ),
    ]
    result = aggregate_findings("report.pdf", "hash123", findings)
    assert result.summary["error"] == 1
    assert result.summary["warning"] == 1
    assert result.summary["critical"] == 0
    assert result.audit_trail.file_hash == "hash123"
    assert result.audit_trail.llm_status == "not_run"
