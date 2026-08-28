"""Tests PdfParser's transformation logic against a faked pdfplumber page (no real PDF needed)."""
from __future__ import annotations

from unittest.mock import patch

from ai_tools_lab.domains.metrology.report_audit.ingestion import pdf_parser


class _FakePage:
    def __init__(self, text: str, tables: list[list[list[str]]]) -> None:
        self._text = text
        self._tables = tables

    def extract_text(self) -> str:
        return self._text

    def extract_tables(self) -> list[list[list[str]]]:
        return self._tables


class _FakePdf:
    def __init__(self, pages: list[_FakePage]) -> None:
        self.pages = pages

    def __enter__(self) -> "_FakePdf":
        return self

    def __exit__(self, *args: object) -> None:
        return None


def test_parse_pdf_maps_pages_and_tables() -> None:
    fake_pdf = _FakePdf(
        pages=[_FakePage(text="报告编号: JL-1", tables=[[["标准值", "示值"], ["0", "0.1"]]])]
    )
    with patch.object(pdf_parser.pdfplumber, "open", return_value=fake_pdf):
        document = pdf_parser.parse_pdf("fake.pdf", file_hash="abc")

    assert document.pages[0].text == "报告编号: JL-1"
    assert document.pages[0].tables[0].rows == [["标准值", "示值"], ["0", "0.1"]]
    assert document.file_hash == "abc"
