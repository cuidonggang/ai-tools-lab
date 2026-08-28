"""Parser-agnostic representation of a document produced by the ingestion layer."""
from __future__ import annotations

from collections.abc import Iterator

from pydantic import BaseModel

from ai_tools_lab.domains.metrology.report_audit.models.locator import SourceLocator


class RawTable(BaseModel):
    """A table extracted from a page, as a simple grid of cell text (row 0 = header)."""

    index: int
    page: int | None
    rows: list[list[str | None]]

    def header(self) -> list[str | None]:
        return self.rows[0] if self.rows else []

    def data_rows(self) -> list[list[str | None]]:
        return self.rows[1:] if len(self.rows) > 1 else []


class RawPage(BaseModel):
    """A single page (or, for paginated-less formats, one logical section)."""

    index: int
    text: str
    tables: list[RawTable] = []


class RawDocument(BaseModel):
    """Common output of every document parser (PDF/DOCX/plain text)."""

    source_path: str
    file_hash: str
    pages: list[RawPage]

    def full_text(self) -> str:
        return "\n".join(page.text for page in self.pages)

    def iter_lines(self) -> Iterator[tuple[str, SourceLocator]]:
        """Yield (line_text, locator) pairs across all pages, skipping blank lines."""
        for page in self.pages:
            for line in page.text.splitlines():
                if line.strip():
                    yield line, SourceLocator(page=page.index)
