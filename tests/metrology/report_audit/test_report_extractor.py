"""Tests the label/table based structured extraction against fixture text files."""
from __future__ import annotations

from pathlib import Path

from ai_tools_lab.domains.metrology.report_audit.extraction.report_extractor import extract_report
from ai_tools_lab.domains.metrology.report_audit.ingestion.text_parser import parse_text

FIXTURES = Path(__file__).parent / "fixtures"


def test_extract_report_from_good_fixture() -> None:
    raw_document = parse_text(FIXTURES / "good_report.txt", file_hash="x")
    extraction = extract_report(raw_document)

    assert extraction.report.document_info.report_number == "JL-2026-0001"
    assert extraction.report.instrument.model == "ABC-100"
    assert len(extraction.report.measurement_data) == 3
    assert extraction.report.measurement_data[0].error == 0.1
    assert extraction.report.standards[0].serial_number == "STD-001"


def test_extract_report_records_conflicting_occurrences() -> None:
    raw_document = parse_text(FIXTURES / "bad_report.txt", file_hash="x")
    extraction = extract_report(raw_document)

    model_values = {occ.value for occ in extraction.field_occurrences["instrument.model"]}
    assert model_values == {"ABC-100", "ABC-200"}
