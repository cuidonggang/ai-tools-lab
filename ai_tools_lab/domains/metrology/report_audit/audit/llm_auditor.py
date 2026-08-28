"""Runs the LLM semantic auditor with retries and evidence verification.

This is the only auditor that calls out to an external model; every other
auditor in the pipeline is pure Python and requires no network access.
"""
from __future__ import annotations

from ai_tools_lab.core.llm_client import LLMProvider
from ai_tools_lab.domains.metrology.report_audit.extraction.result import ExtractionResult
from ai_tools_lab.domains.metrology.report_audit.llm.prompts import build_semantic_audit_prompt
from ai_tools_lab.domains.metrology.report_audit.llm.structured_output import (
    LLMOutputValidationError,
    parse_llm_response,
    to_audit_findings,
)
from ai_tools_lab.domains.metrology.report_audit.models.finding import AuditFinding


class LLMAuditor:
    def __init__(self, provider: LLMProvider, max_retries: int = 2) -> None:
        self._provider = provider
        self._max_retries = max_retries
        self.last_status = "not_run"

    def audit(
        self, extraction: ExtractionResult, existing_findings: list[AuditFinding]
    ) -> list[AuditFinding]:
        source_excerpt = extraction.raw_document.full_text()
        prompt = build_semantic_audit_prompt(extraction.report, source_excerpt, existing_findings)

        for _ in range(self._max_retries + 1):
            raw_text = self._provider.complete(prompt)
            try:
                response = parse_llm_response(raw_text)
            except LLMOutputValidationError as exc:
                prompt = (
                    build_semantic_audit_prompt(extraction.report, source_excerpt, existing_findings)
                    + f"\n\n你上一次的输出无法通过校验，错误信息：{exc}\n请修正后只输出合法 JSON。"
                )
                continue
            self.last_status = "ok"
            return to_audit_findings(response, source_excerpt)

        # All retries exhausted: skip semantic audit rather than fabricate a result.
        self.last_status = "failed"
        return []
