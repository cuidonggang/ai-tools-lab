"""End-to-end test of the deterministic audit pipeline (no LLM) against two fixture reports."""
from __future__ import annotations

from pathlib import Path

from ai_tools_lab.domains.metrology.report_audit.audit_service import AuditService
from ai_tools_lab.domains.metrology.report_audit.models.finding import Category, Severity

FIXTURES = Path(__file__).parent / "fixtures"


def test_good_report_has_no_deterministic_findings() -> None:
    result = AuditService().audit_file(FIXTURES / "good_report.txt")
    assert result.findings == []
    assert result.audit_trail.llm_status == "not_run"


def test_bad_report_flags_all_expected_issues() -> None:
    result = AuditService().audit_file(FIXTURES / "bad_report.txt")
    rule_ids = {f.rule_id for f in result.findings}
    categories = {f.category for f in result.findings}
    severities = {f.severity for f in result.findings}

    assert "required_field:document_info.report_number" in rule_ids
    assert "required_field:technical_basis" in rule_ids
    assert "measurement_date_before_issue_date" in rule_ids
    assert "standard_not_expired" in rule_ids
    assert "calculation:error_mismatch" in rule_ids
    assert "calculation:exceeds_mpe_but_qualified" in rule_ids
    assert any(f.rule_id and f.rule_id.startswith("consistency:instrument.model") for f in result.findings)

    assert Severity.CRITICAL in severities
    assert Severity.ERROR in severities
    assert Severity.WARNING in severities
    assert Category.CALCULATION in categories
