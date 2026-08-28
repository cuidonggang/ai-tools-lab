"""Structured representation of a metrology inspection/calibration/verification report."""
from __future__ import annotations

from datetime import date

from pydantic import BaseModel

from ai_tools_lab.domains.metrology.report_audit.models.locator import SourceLocator


class FieldOccurrence(BaseModel):
    """One occurrence of a labeled field value found somewhere in the document.

    Extraction keeps every occurrence (not just the first) so the consistency
    auditor can detect the same field being stated differently in two places.
    """

    value: str
    locator: SourceLocator | None = None


class DocumentInfo(BaseModel):
    report_number: str | None = None
    report_name: str | None = None
    report_type: str | None = None  # 检定 / 校准 / 检测
    issue_date: date | None = None
    measurement_date: date | None = None
    page_count: int | None = None


class Instrument(BaseModel):
    name: str | None = None
    manufacturer: str | None = None
    model: str | None = None
    serial_number: str | None = None
    asset_number: str | None = None
    measurement_range: str | None = None
    resolution: str | None = None
    accuracy_class: str | None = None


class StandardInstrument(BaseModel):
    name: str | None = None
    model: str | None = None
    serial_number: str | None = None
    measurement_range: str | None = None
    accuracy: str | None = None
    certificate_number: str | None = None
    expiry_date: date | None = None
    traceability_org: str | None = None


class MeasurementRow(BaseModel):
    """One row of the measurement-data table. Fields are optional because
    different metrology specialties populate different columns."""

    point: str | None = None
    standard_value: float | None = None
    indicated_value: float | None = None
    correction: float | None = None
    error: float | None = None
    repeatability: float | None = None
    mpe: float | None = None  # 最大允许误差
    uncertainty: float | None = None
    verdict: str | None = None
    locator: SourceLocator | None = None


class Report(BaseModel):
    document_info: DocumentInfo = DocumentInfo()
    customer: str | None = None
    instrument: Instrument = Instrument()
    environment: dict[str, str] = {}
    technical_basis: list[str] = []
    standards: list[StandardInstrument] = []
    measurement_data: list[MeasurementRow] = []
    conclusion: str | None = None
    signatures: list[str] = []
