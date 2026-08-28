"""Aggregated audit output for a single report, plus the audit-trail metadata
needed to answer "who/what produced this finding, based on which rules/model".
"""
from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, Field

from ai_tools_lab.domains.metrology.report_audit.models.finding import AuditFinding, Severity


class AuditTrailMeta(BaseModel):
    file_hash: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    llm_status: str = "not_run"  # not_run | ok | failed
    rules_version: str = "v1"


class AuditResult(BaseModel):
    source_path: str
    audit_trail: AuditTrailMeta
    findings: list[AuditFinding] = []

    @property
    def summary(self) -> dict[str, int]:
        counts = {severity.value: 0 for severity in Severity}
        for finding in self.findings:
            counts[finding.severity.value] += 1
        return counts
