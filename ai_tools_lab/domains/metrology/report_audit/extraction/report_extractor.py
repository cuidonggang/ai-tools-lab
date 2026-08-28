"""Extracts a structured Report (+ raw field occurrences) from a RawDocument.

Uses simple "label: value" line matching plus a configurable table-column
mapper for the measurement-data table, rather than free-form NLP, to keep
extraction behavior predictable and testable.
"""
from __future__ import annotations

import re

from ai_tools_lab.domains.metrology.report_audit.extraction.alias_config import (
    build_label_lookup,
    load_field_aliases,
)
from ai_tools_lab.domains.metrology.report_audit.extraction.parsing import parse_date
from ai_tools_lab.domains.metrology.report_audit.extraction.result import ExtractionResult
from ai_tools_lab.domains.metrology.report_audit.extraction.table_extractor import (
    extract_measurement_rows,
)
from ai_tools_lab.domains.metrology.report_audit.models.raw_document import RawDocument
from ai_tools_lab.domains.metrology.report_audit.models.report import (
    DocumentInfo,
    FieldOccurrence,
    Instrument,
    Report,
    StandardInstrument,
)

_LABEL_LINE = re.compile(r"^\s*([^:：]{1,24})[:：]\s*(.+?)\s*$")


def _collect_occurrences(
    raw_document: RawDocument, label_lookup: dict[str, str]
) -> dict[str, list[FieldOccurrence]]:
    occurrences: dict[str, list[FieldOccurrence]] = {}
    for line, locator in raw_document.iter_lines():
        match = _LABEL_LINE.match(line)
        if not match:
            continue
        label, value = match.group(1).strip(), match.group(2).strip()
        canonical_path = label_lookup.get(label)
        if canonical_path is None:
            continue
        occurrences.setdefault(canonical_path, []).append(FieldOccurrence(value=value, locator=locator))
    return occurrences


def _first(occurrences: dict[str, list[FieldOccurrence]], path: str) -> str | None:
    values = occurrences.get(path)
    return values[0].value if values else None


def _all(occurrences: dict[str, list[FieldOccurrence]], path: str) -> list[str]:
    return [occ.value for occ in occurrences.get(path, [])]


def _build_standards(occurrences: dict[str, list[FieldOccurrence]]) -> list[StandardInstrument]:
    values = {
        "name": _first(occurrences, "standard.name"),
        "model": _first(occurrences, "standard.model"),
        "serial_number": _first(occurrences, "standard.serial_number"),
        "measurement_range": _first(occurrences, "standard.measurement_range"),
        "accuracy": _first(occurrences, "standard.accuracy"),
        "certificate_number": _first(occurrences, "standard.certificate_number"),
        "traceability_org": _first(occurrences, "standard.traceability_org"),
    }
    expiry_date = parse_date(_first(occurrences, "standard.expiry_date"))
    if not any(values.values()) and expiry_date is None:
        return []
    return [StandardInstrument(expiry_date=expiry_date, **values)]


def extract_report(raw_document: RawDocument) -> ExtractionResult:
    """Extract a structured Report + raw field occurrences from a RawDocument."""
    label_lookup = build_label_lookup(load_field_aliases())
    occurrences = _collect_occurrences(raw_document, label_lookup)

    report = Report(
        document_info=DocumentInfo(
            report_number=_first(occurrences, "document_info.report_number"),
            report_name=_first(occurrences, "document_info.report_name"),
            report_type=_first(occurrences, "document_info.report_type"),
            issue_date=parse_date(_first(occurrences, "document_info.issue_date")),
            measurement_date=parse_date(_first(occurrences, "document_info.measurement_date")),
        ),
        customer=_first(occurrences, "customer"),
        instrument=Instrument(
            name=_first(occurrences, "instrument.name"),
            manufacturer=_first(occurrences, "instrument.manufacturer"),
            model=_first(occurrences, "instrument.model"),
            serial_number=_first(occurrences, "instrument.serial_number"),
            asset_number=_first(occurrences, "instrument.asset_number"),
            measurement_range=_first(occurrences, "instrument.measurement_range"),
            resolution=_first(occurrences, "instrument.resolution"),
            accuracy_class=_first(occurrences, "instrument.accuracy_class"),
        ),
        technical_basis=_all(occurrences, "technical_basis"),
        standards=_build_standards(occurrences),
        measurement_data=extract_measurement_rows(raw_document),
        conclusion=_first(occurrences, "conclusion"),
    )
    return ExtractionResult(report=report, raw_document=raw_document, field_occurrences=occurrences)
