"""Flags fields that were mentioned multiple times in the report with different values.

E.g. the instrument model stated as "ABC-100" on page 1 and "ABC-200" in the
measurement-data section. Only a curated set of identity-like fields are
checked; free-text fields (like the conclusion) legitimately get rephrased.
"""
from __future__ import annotations

from ai_tools_lab.domains.metrology.report_audit.extraction.result import ExtractionResult
from ai_tools_lab.domains.metrology.report_audit.models.finding import (
    AuditFinding,
    Category,
    Evidence,
    Severity,
)

_WATCHED_FIELDS = (
    "document_info.report_number",
    "instrument.name",
    "instrument.model",
    "instrument.serial_number",
    "instrument.measurement_range",
    "standard.serial_number",
)


class ConsistencyAuditor:
    def audit(self, extraction: ExtractionResult) -> list[AuditFinding]:
        findings: list[AuditFinding] = []
        for field_path in _WATCHED_FIELDS:
            occurrences = extraction.field_occurrences.get(field_path, [])
            distinct_values = {occ.value.strip() for occ in occurrences if occ.value}
            if len(distinct_values) <= 1:
                continue
            findings.append(
                AuditFinding(
                    category=Category.CONSISTENCY,
                    severity=Severity.WARNING,
                    title=f"字段前后不一致：{field_path}",
                    description=f"报告中 {field_path} 出现了 {len(distinct_values)} 种不同取值，请核实实际值。",
                    evidence=[
                        Evidence(field=field_path, value=occ.value, locator=occ.locator)
                        for occ in occurrences
                    ],
                    rule_id=f"consistency:{field_path}",
                    source="consistency",
                    suggestion="确认报告中该字段的真实取值，修正不一致之处",
                )
            )
        return findings
