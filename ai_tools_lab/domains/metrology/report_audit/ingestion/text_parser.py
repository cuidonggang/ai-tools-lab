"""Parses plain-text report dumps into a RawDocument.

Used by tests and for quickly trying the pipeline without a real PDF/DOCX file.
Supports a simple embedded-table convention: a block starting with a line
containing only "TABLE:" and ending at the next blank line, where each row is
"|"-delimited (first row is the header), e.g.::

    TABLE:
    测量点|标准值|示值|误差
    1|0|0.1|0.1
"""
from __future__ import annotations

from pathlib import Path

from ai_tools_lab.domains.metrology.report_audit.models.raw_document import (
    RawDocument,
    RawPage,
    RawTable,
)


def parse_text(path: str | Path, file_hash: str) -> RawDocument:
    lines = Path(path).read_text(encoding="utf-8").splitlines()

    body_lines: list[str] = []
    tables: list[RawTable] = []
    index = 0
    table_index = 0
    while index < len(lines):
        line = lines[index]
        if line.strip() == "TABLE:":
            index += 1
            rows: list[list[str | None]] = []
            while index < len(lines) and lines[index].strip():
                rows.append([cell.strip() for cell in lines[index].split("|")])
                index += 1
            tables.append(RawTable(index=table_index, page=0, rows=rows))
            table_index += 1
        else:
            body_lines.append(line)
            index += 1

    page = RawPage(index=0, text="\n".join(body_lines), tables=tables)
    return RawDocument(source_path=str(path), file_hash=file_hash, pages=[page])
