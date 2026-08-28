"""Dispatches to the right parser based on file extension and computes a stable hash."""
from __future__ import annotations

import hashlib
from pathlib import Path

from ai_tools_lab.domains.metrology.report_audit.ingestion.docx_parser import parse_docx
from ai_tools_lab.domains.metrology.report_audit.ingestion.pdf_parser import parse_pdf
from ai_tools_lab.domains.metrology.report_audit.ingestion.text_parser import parse_text
from ai_tools_lab.domains.metrology.report_audit.models.raw_document import RawDocument

_PARSERS = {
    ".pdf": parse_pdf,
    ".docx": parse_docx,
    ".txt": parse_text,
}


def load_document(path: str | Path) -> RawDocument:
    """Load a report file into a RawDocument, dispatching by file extension."""
    path = Path(path)
    parser = _PARSERS.get(path.suffix.lower())
    if parser is None:
        raise ValueError(f"Unsupported report file type: {path.suffix or '(none)'}")
    file_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    return parser(path, file_hash)
