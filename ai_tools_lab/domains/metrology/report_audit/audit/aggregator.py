"""Combines findings from all auditors into the final AuditResult."""
from __future__ import annotations

from ai_tools_lab.domains.metrology.report_audit.models.audit_result import (
    AuditResult,
    AuditTrailMeta,
)
from ai_tools_lab.domains.metrology.report_audit.models.finding import AuditFinding


def aggregate_findings(
    source_path: str,
    file_hash: str,
    findings: list[AuditFinding],
    llm_status: str = "not_run",
) -> AuditResult:
    return AuditResult(
        source_path=source_path,
        audit_trail=AuditTrailMeta(file_hash=file_hash, llm_status=llm_status),
        findings=findings,
    )
