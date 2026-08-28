"""Unit tests for the deterministic rule engine (no parsing/extraction involved)."""
from __future__ import annotations

from datetime import date

from ai_tools_lab.domains.metrology.report_audit.models.finding import Severity
from ai_tools_lab.domains.metrology.report_audit.models.report import (
    DocumentInfo,
    Report,
    StandardInstrument,
)
from ai_tools_lab.domains.metrology.report_audit.rules.rule_engine import (
    check_date_rules,
    check_required_fields,
)
from ai_tools_lab.domains.metrology.report_audit.rules.rule_models import (
    DateCheckRule,
    RequiredFieldRule,
)


def test_required_field_missing_is_flagged() -> None:
    report = Report()
    rules = [RequiredFieldRule(path="document_info.report_number", severity=Severity.ERROR, message="缺失")]
    findings = check_required_fields(report, rules)
    assert len(findings) == 1
    assert findings[0].severity == Severity.ERROR


def test_required_field_present_is_not_flagged() -> None:
    report = Report(document_info=DocumentInfo(report_number="JL-001"))
    rules = [RequiredFieldRule(path="document_info.report_number", severity=Severity.ERROR, message="缺失")]
    assert check_required_fields(report, rules) == []


def test_measurement_date_after_issue_date_is_flagged() -> None:
    report = Report(
        document_info=DocumentInfo(measurement_date=date(2026, 8, 25), issue_date=date(2026, 8, 20))
    )
    rules = {
        "measurement_date_before_issue_date": DateCheckRule(
            id="measurement_date_before_issue_date", severity=Severity.ERROR, message="日期矛盾"
        )
    }
    findings = check_date_rules(report, rules)
    assert len(findings) == 1
    assert findings[0].severity == Severity.ERROR


def test_expired_standard_is_flagged_as_critical() -> None:
    report = Report(
        document_info=DocumentInfo(measurement_date=date(2026, 8, 25)),
        standards=[StandardInstrument(name="标准器", expiry_date=date(2026, 7, 31))],
    )
    rules = {
        "standard_not_expired": DateCheckRule(
            id="standard_not_expired", severity=Severity.CRITICAL, message="标准器过期"
        )
    }
    findings = check_date_rules(report, rules)
    assert len(findings) == 1
    assert findings[0].severity == Severity.CRITICAL


def test_disabled_date_rule_is_skipped() -> None:
    report = Report(
        document_info=DocumentInfo(measurement_date=date(2026, 8, 25), issue_date=date(2026, 8, 20))
    )
    rules = {
        "measurement_date_before_issue_date": DateCheckRule(
            id="measurement_date_before_issue_date",
            enabled=False,
            severity=Severity.ERROR,
            message="日期矛盾",
        )
    }
    assert check_date_rules(report, rules) == []
