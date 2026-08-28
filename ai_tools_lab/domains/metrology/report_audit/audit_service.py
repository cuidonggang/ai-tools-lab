"""Orchestrates the full report-audit pipeline: parse -> extract -> audit -> aggregate."""
from __future__ import annotations

from pathlib import Path

from ai_tools_lab.core.llm_client import LLMProvider
from ai_tools_lab.domains.metrology.report_audit.audit.aggregator import aggregate_findings
from ai_tools_lab.domains.metrology.report_audit.audit.calculation_auditor import (
    CalculationAuditor,
)
from ai_tools_lab.domains.metrology.report_audit.audit.completeness_auditor import (
    CompletenessAuditor,
)
from ai_tools_lab.domains.metrology.report_audit.audit.consistency_auditor import (
    ConsistencyAuditor,
)
from ai_tools_lab.domains.metrology.report_audit.audit.llm_auditor import LLMAuditor
from ai_tools_lab.domains.metrology.report_audit.audit.rule_auditor import RuleAuditor
from ai_tools_lab.domains.metrology.report_audit.extraction.report_extractor import extract_report
from ai_tools_lab.domains.metrology.report_audit.ingestion.document_loader import load_document
from ai_tools_lab.domains.metrology.report_audit.models.audit_result import AuditResult


class AuditService:
    """Entry point for auditing a single report file end to end.

    LLM semantic auditing is only run when an `llm_provider` is supplied,
    keeping the deterministic stages usable (and testable) without any
    external model dependency.
    """

    def __init__(self, llm_provider: LLMProvider | None = None) -> None:
        self._llm_provider = llm_provider
        self._completeness_auditor = CompletenessAuditor()
        self._rule_auditor = RuleAuditor()
        self._consistency_auditor = ConsistencyAuditor()
        self._calculation_auditor = CalculationAuditor()

    def audit_file(self, path: str | Path) -> AuditResult:
        raw_document = load_document(path)
        extraction = extract_report(raw_document)

        findings = []
        findings += self._completeness_auditor.audit(extraction)
        findings += self._rule_auditor.audit(extraction)
        findings += self._consistency_auditor.audit(extraction)
        findings += self._calculation_auditor.audit(extraction)

        llm_status = "not_run"
        if self._llm_provider is not None:
            llm_auditor = LLMAuditor(self._llm_provider)
            findings += llm_auditor.audit(extraction, existing_findings=findings)
            llm_status = llm_auditor.last_status

        return aggregate_findings(str(path), raw_document.file_hash, findings, llm_status)
