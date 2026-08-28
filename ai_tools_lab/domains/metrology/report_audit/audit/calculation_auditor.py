"""Verifies measurement-table arithmetic and flags data/conclusion contradictions.

All numeric computation happens here in plain Python -- calculation must never
be delegated to the LLM.
"""
from __future__ import annotations

from ai_tools_lab.domains.metrology.report_audit.extraction.result import ExtractionResult
from ai_tools_lab.domains.metrology.report_audit.models.finding import (
    AuditFinding,
    Category,
    Evidence,
    Severity,
)
from ai_tools_lab.domains.metrology.report_audit.models.report import MeasurementRow

_EPSILON = 0.01
_QUALIFIED_KEYWORDS = ("合格",)
_UNQUALIFIED_KEYWORDS = ("不合格", "超差")


def _is_marked_qualified(row: MeasurementRow, report_conclusion: str | None) -> bool | None:
    verdict = row.verdict or report_conclusion
    if not verdict:
        return None
    if any(keyword in verdict for keyword in _UNQUALIFIED_KEYWORDS):
        return False
    if any(keyword in verdict for keyword in _QUALIFIED_KEYWORDS):
        return True
    return None


class CalculationAuditor:
    def audit(self, extraction: ExtractionResult) -> list[AuditFinding]:
        findings: list[AuditFinding] = []
        report = extraction.report
        for row_index, row in enumerate(report.measurement_data):
            findings.extend(self._check_error_calculation(row, row_index))
            findings.extend(self._check_mpe_conclusion(row, row_index, report.conclusion))
        return findings

    def _check_error_calculation(self, row: MeasurementRow, row_index: int) -> list[AuditFinding]:
        if row.standard_value is None or row.indicated_value is None or row.error is None:
            return []
        expected_error = row.indicated_value - row.standard_value
        if abs(expected_error - row.error) > _EPSILON:
            return [
                AuditFinding(
                    category=Category.CALCULATION,
                    severity=Severity.ERROR,
                    title=f"第 {row_index + 1} 行误差计算错误",
                    description=(
                        f"报告误差为 {row.error}，按 示值-标准值 计算应为 "
                        f"{expected_error:.3f}，两者不一致。"
                    ),
                    evidence=[
                        Evidence(
                            field=f"measurement_data[{row_index}].error",
                            value=str(row.error),
                            locator=row.locator,
                        ),
                        Evidence(
                            field=f"measurement_data[{row_index}].standard_value",
                            value=str(row.standard_value),
                            locator=row.locator,
                        ),
                        Evidence(
                            field=f"measurement_data[{row_index}].indicated_value",
                            value=str(row.indicated_value),
                            locator=row.locator,
                        ),
                    ],
                    rule_id="calculation:error_mismatch",
                    source="calculation",
                    suggestion="核实示值/标准值/误差三者的原始记录",
                )
            ]
        return []

    def _check_mpe_conclusion(
        self, row: MeasurementRow, row_index: int, report_conclusion: str | None
    ) -> list[AuditFinding]:
        if row.error is None or row.mpe is None:
            return []
        if abs(row.error) <= abs(row.mpe) + _EPSILON:
            return []
        if _is_marked_qualified(row, report_conclusion) is not True:
            return []
        return [
            AuditFinding(
                category=Category.CONCLUSION,
                severity=Severity.CRITICAL,
                title=f"第 {row_index + 1} 行数据超差但结论判定合格",
                description=(
                    f"实际误差 {row.error} 超出最大允许误差 ±{abs(row.mpe)}，但判定结果为合格，"
                    "数据与结论可能矛盾。"
                ),
                evidence=[
                    Evidence(
                        field=f"measurement_data[{row_index}].error",
                        value=str(row.error),
                        locator=row.locator,
                    ),
                    Evidence(
                        field=f"measurement_data[{row_index}].mpe", value=str(row.mpe), locator=row.locator
                    ),
                    Evidence(
                        field=f"measurement_data[{row_index}].verdict",
                        value=row.verdict,
                        locator=row.locator,
                    ),
                ],
                rule_id="calculation:exceeds_mpe_but_qualified",
                source="calculation",
                suggestion="核实该测量点判定结果，确认是否应判定为不合格",
            )
        ]
