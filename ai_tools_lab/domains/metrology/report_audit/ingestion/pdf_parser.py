"""Parses text-based PDF reports into a RawDocument using pdfplumber.

Scanned (image-only) PDFs are out of scope for now; OCR support is a planned
extension point (a future `ocr_pdf_parser.py` producing the same RawDocument
shape).
"""
from __future__ import annotations

from pathlib import Path

import pdfplumber

from ai_tools_lab.domains.metrology.report_audit.models.raw_document import (
    RawDocument,
    RawPage,
    RawTable,
)


def parse_pdf(path: str | Path, file_hash: str) -> RawDocument:
    """Extract per-page text and tables from a text-based PDF."""
    pages: list[RawPage] = []
    with pdfplumber.open(path) as pdf:
        for page_index, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            tables = [
                RawTable(index=table_index, page=page_index, rows=table_rows)
                for table_index, table_rows in enumerate(page.extract_tables())
            ]
            pages.append(RawPage(index=page_index, text=text, tables=tables))
    return RawDocument(source_path=str(path), file_hash=file_hash, pages=pages)
