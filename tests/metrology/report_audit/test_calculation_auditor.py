"""Unit tests for pure-Python numeric checks in CalculationAuditor."""
from __future__ import annotations

from ai_tools_lab.domains.metrology.report_audit.audit.calculation_auditor import (
    CalculationAuditor,
)
from ai_tools_lab.domains.metrology.report_audit.extraction.result import ExtractionResult
from ai_tools_lab.domains.metrology.report_audit.models.finding import Category, Severity
from ai_tools_lab.domains.metrology.report_audit.models.raw_document import RawDocument, RawPage
from ai_tools_lab.domains.metrology.report_audit.models.report import MeasurementRow, Report


def _extraction(report: Report) -> ExtractionResult:
    raw_document = RawDocument(source_path="test", file_hash="x", pages=[RawPage(index=0, text="")])
    return ExtractionResult(report=report, raw_document=raw_document, field_occurrences={})


def test_correct_error_calculation_is_not_flagged() -> None:
    report = Report(
        measurement_data=[MeasurementRow(standard_value=10, indicated_value=10.1, error=0.1, mpe=0.5)]
    )
    assert CalculationAuditor().audit(_extraction(report)) == []


def test_wrong_error_calculation_is_flagged() -> None:
    report = Report(
        measurement_data=[MeasurementRow(standard_value=10, indicated_value=10.1, error=0.5, mpe=0.5)]
    )
    findings = CalculationAuditor().audit(_extraction(report))
    assert any(f.category == Category.CALCULATION and f.severity == Severity.ERROR for f in findings)


def test_exceeds_mpe_but_qualified_is_critical() -> None:
    report = Report(
        conclusion="合格",
        measurement_data=[
            MeasurementRow(
                standard_value=10, indicated_value=10.62, error=0.62, mpe=0.5, verdict="合格"
            )
        ],
    )
    findings = CalculationAuditor().audit(_extraction(report))
    assert any(f.severity == Severity.CRITICAL for f in findings)


def test_exceeds_mpe_but_unqualified_is_not_flagged() -> None:
    report = Report(
        measurement_data=[
            MeasurementRow(
                standard_value=10, indicated_value=10.62, error=0.62, mpe=0.5, verdict="不合格"
            )
        ],
    )
    findings = CalculationAuditor().audit(_extraction(report))
    assert not any(f.rule_id == "calculation:exceeds_mpe_but_qualified" for f in findings)
