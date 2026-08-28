"""Unit tests for cross-field consistency detection."""
from __future__ import annotations

from ai_tools_lab.domains.metrology.report_audit.audit.consistency_auditor import (
    ConsistencyAuditor,
)
from ai_tools_lab.domains.metrology.report_audit.extraction.result import ExtractionResult
from ai_tools_lab.domains.metrology.report_audit.models.raw_document import RawDocument, RawPage
from ai_tools_lab.domains.metrology.report_audit.models.report import FieldOccurrence, Report


def _extraction(occurrences: dict[str, list[FieldOccurrence]]) -> ExtractionResult:
    raw_document = RawDocument(source_path="test", file_hash="x", pages=[RawPage(index=0, text="")])
    return ExtractionResult(report=Report(), raw_document=raw_document, field_occurrences=occurrences)


def test_conflicting_model_values_are_flagged() -> None:
    occurrences = {
        "instrument.model": [FieldOccurrence(value="ABC-100"), FieldOccurrence(value="ABC-200")]
    }
    findings = ConsistencyAuditor().audit(_extraction(occurrences))
    assert len(findings) == 1
    assert findings[0].evidence[0].value in {"ABC-100", "ABC-200"}


def test_consistent_model_values_are_not_flagged() -> None:
    occurrences = {
        "instrument.model": [FieldOccurrence(value="ABC-100"), FieldOccurrence(value="ABC-100")]
    }
    assert ConsistencyAuditor().audit(_extraction(occurrences)) == []


def test_unwatched_field_is_never_flagged() -> None:
    occurrences = {"conclusion": [FieldOccurrence(value="合格"), FieldOccurrence(value="基本合格")]}
    assert ConsistencyAuditor().audit(_extraction(occurrences)) == []
