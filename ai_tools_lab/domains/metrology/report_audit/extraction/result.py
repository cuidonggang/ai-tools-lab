"""Bundles everything downstream auditors need after extraction."""
from __future__ import annotations

from pydantic import BaseModel

from ai_tools_lab.domains.metrology.report_audit.models.raw_document import RawDocument
from ai_tools_lab.domains.metrology.report_audit.models.report import FieldOccurrence, Report


class ExtractionResult(BaseModel):
    """The structured report, every raw label occurrence (for consistency checks),
    and the parsed raw document (for LLM evidence excerpts)."""

    report: Report
    raw_document: RawDocument
    field_occurrences: dict[str, list[FieldOccurrence]] = {}
