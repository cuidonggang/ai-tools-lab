"""Deterministic rule checks: required-field presence and named date-consistency checks.

Intentionally data-driven (severity/message come from YAML) rather than a
general expression DSL, so behavior stays predictable, simple, and testable
without a real LLM.
"""
from __future__ import annotations

from typing import Any

from ai_tools_lab.domains.metrology.report_audit.models.finding import (
    AuditFinding,
    Category,
    Evidence,
)
from ai_tools_lab.domains.metrology.report_audit.models.report import Report
from ai_tools_lab.domains.metrology.report_audit.rules.rule_models import (
    DateCheckRule,
    RequiredFieldRule,
)


def _resolve_path(report: Report, path: str) -> Any:
    value: Any = report
    for part in path.split("."):
        if value is None:
            return None
        value = getattr(value, part, None)
    return value


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, list):
        return len(value) == 0
    return False


def check_required_fields(report: Report, rules: list[RequiredFieldRule]) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    for rule in rules:
        if _is_missing(_resolve_path(report, rule.path)):
            findings.append(
                AuditFinding(
                    category=Category.COMPLETENESS,
                    severity=rule.severity,
                    title=f"缺少必要字段：{rule.path}",
                    description=rule.message,
                    evidence=[Evidence(field=rule.path, value=None)],
                    rule_id=f"required_field:{rule.path}",
                    source="completeness",
                    suggestion="请补充该字段后重新审核",
                )
            )
    return findings


def _measurement_date_before_issue_date(report: Report, rule: DateCheckRule) -> AuditFinding | None:
    info = report.document_info
    if info.measurement_date is None or info.issue_date is None:
        return None
    if info.measurement_date > info.issue_date:
        return AuditFinding(
            category=Category.FORMAT,
            severity=rule.severity,
            title="检测日期晚于报告签发日期",
            description=rule.message,
            evidence=[
                Evidence(field="document_info.measurement_date", value=str(info.measurement_date)),
                Evidence(field="document_info.issue_date", value=str(info.issue_date)),
            ],
            rule_id=rule.id,
            source="rule",
        )
    return None


def _standard_not_expired(report: Report, rule: DateCheckRule) -> list[AuditFinding]:
    info = report.document_info
    if info.measurement_date is None:
        return []
    findings: list[AuditFinding] = []
    for index, standard in enumerate(report.standards):
        if standard.expiry_date is not None and standard.expiry_date < info.measurement_date:
            findings.append(
                AuditFinding(
                    category=Category.TRACEABILITY,
                    severity=rule.severity,
                    title="标准器在检测日期时已过期",
                    description=rule.message,
                    evidence=[
                        Evidence(
                            field="document_info.measurement_date", value=str(info.measurement_date)
                        ),
                        Evidence(
                            field=f"standards[{index}].expiry_date", value=str(standard.expiry_date)
                        ),
                    ],
                    rule_id=rule.id,
                    source="rule",
                )
            )
    return findings


_DATE_CHECKS = {
    "measurement_date_before_issue_date": lambda report, rule: (
        [finding] if (finding := _measurement_date_before_issue_date(report, rule)) else []
    ),
    "standard_not_expired": _standard_not_expired,
}


def check_date_rules(report: Report, rules: dict[str, DateCheckRule]) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    for rule_id, rule in rules.items():
        if not rule.enabled:
            continue
        check_fn = _DATE_CHECKS.get(rule_id)
        if check_fn is None:
            continue
        findings.extend(check_fn(report, rule))
    return findings
