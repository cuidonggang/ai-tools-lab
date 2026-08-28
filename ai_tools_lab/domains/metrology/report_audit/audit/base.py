"""Common interface every deterministic auditor implements."""
from __future__ import annotations

from typing import Protocol

from ai_tools_lab.domains.metrology.report_audit.extraction.result import ExtractionResult
from ai_tools_lab.domains.metrology.report_audit.models.finding import AuditFinding


class Auditor(Protocol):
    def audit(self, extraction: ExtractionResult) -> list[AuditFinding]:
        ...
