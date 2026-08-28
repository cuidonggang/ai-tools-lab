"""Extracts the measurement-data table from a RawDocument using configurable column aliases.

The first table whose header row matches at least two known column aliases is
treated as the measurement-data table; unrelated tables (e.g. environment
conditions) are simply skipped.
"""
from __future__ import annotations

from ai_tools_lab.domains.metrology.report_audit.extraction.alias_config import (
    build_label_lookup,
    load_column_aliases,
)
from ai_tools_lab.domains.metrology.report_audit.extraction.parsing import parse_float
from ai_tools_lab.domains.metrology.report_audit.models.locator import SourceLocator
from ai_tools_lab.domains.metrology.report_audit.models.raw_document import RawDocument
from ai_tools_lab.domains.metrology.report_audit.models.report import MeasurementRow

_TEXT_FIELDS = {"point", "verdict"}


def extract_measurement_rows(raw_document: RawDocument) -> list[MeasurementRow]:
    header_lookup = build_label_lookup(load_column_aliases())

    for page in raw_document.pages:
        for table in page.tables:
            header = [str(cell).strip() if cell else "" for cell in table.header()]
            column_map = {
                col_index: header_lookup[cell]
                for col_index, cell in enumerate(header)
                if cell in header_lookup
            }
            if len(column_map) < 2:
                continue  # not the measurement-data table

            rows: list[MeasurementRow] = []
            for row_index, raw_row in enumerate(table.data_rows(), start=1):
                values: dict[str, object] = {
                    "locator": SourceLocator(page=page.index, table_index=table.index, row=row_index)
                }
                for col_index, field_name in column_map.items():
                    if col_index >= len(raw_row):
                        continue
                    cell_value = raw_row[col_index]
                    if field_name in _TEXT_FIELDS:
                        values[field_name] = cell_value.strip() if cell_value else None
                    else:
                        values[field_name] = parse_float(cell_value)
                rows.append(MeasurementRow(**values))
            return rows
    return []
