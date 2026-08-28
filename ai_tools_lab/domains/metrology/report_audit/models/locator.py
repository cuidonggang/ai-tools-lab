"""Location/traceability pointer back to the original document for a piece of data."""
from __future__ import annotations

from pydantic import BaseModel


class SourceLocator(BaseModel):
    """Points back to where a value was found in the source document."""

    page: int | None = None
    section: str | None = None
    table_index: int | None = None
    row: int | None = None
    column: str | None = None

    def describe(self) -> str:
        """Human-readable location string for display during human review."""
        parts: list[str] = []
        if self.page is not None:
            parts.append(f"page {self.page}")
        if self.section:
            parts.append(self.section)
        if self.table_index is not None:
            parts.append(f"table {self.table_index}")
        if self.row is not None:
            parts.append(f"row {self.row}")
        if self.column:
            parts.append(f"column {self.column}")
        return ", ".join(parts) if parts else "unknown location"
