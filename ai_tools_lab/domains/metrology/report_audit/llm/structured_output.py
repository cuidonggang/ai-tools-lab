"""Validates the LLM's structured JSON output and converts it into AuditFindings.

This is the primary anti-hallucination gate: findings whose cited evidence
can't be found verbatim in the text shown to the model are stripped or
down-weighted rather than trusted at face value.
"""
from __future__ import annotations

import json

from pydantic import BaseModel, Field, ValidationError

from ai_tools_lab.domains.metrology.report_audit.models.finding import (
    AuditFinding,
    Category,
    Evidence,
    Severity,
)


class LLMFindingItem(BaseModel):
    """Raw shape the LLM must return for a single finding, before conversion."""

    category: Category
    severity: Severity
    title: str
    description: str
    evidence_excerpts: list[str] = Field(default_factory=list)
    confidence: float = 0.5
    suggestion: str | None = None
    insufficient_evidence: bool = False


class LLMFindingsResponse(BaseModel):
    findings: list[LLMFindingItem] = Field(default_factory=list)


class LLMOutputValidationError(Exception):
    """Raised when the LLM's raw text isn't valid JSON matching the expected schema."""


def parse_llm_response(raw_text: str) -> LLMFindingsResponse:
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise LLMOutputValidationError(f"LLM 输出不是合法 JSON: {exc}") from exc
    try:
        return LLMFindingsResponse.model_validate(payload)
    except ValidationError as exc:
        raise LLMOutputValidationError(f"LLM 输出不符合预期 Schema: {exc}") from exc


def to_audit_findings(response: LLMFindingsResponse, source_text: str) -> list[AuditFinding]:
    """Convert validated LLM items into AuditFinding, dropping unverifiable evidence."""
    findings: list[AuditFinding] = []
    for item in response.findings:
        if item.insufficient_evidence:
            continue  # explicit "not enough evidence" -> no finding raised
        verified_excerpts = [excerpt for excerpt in item.evidence_excerpts if excerpt and excerpt in source_text]
        confidence = item.confidence if verified_excerpts else min(item.confidence, 0.3)
        findings.append(
            AuditFinding(
                category=item.category,
                severity=item.severity,
                title=item.title,
                description=item.description,
                evidence=[Evidence(excerpt=excerpt) for excerpt in verified_excerpts],
                source="llm",
                confidence=confidence,
                suggestion=item.suggestion,
                requires_human_review=True,
            )
        )
    return findings
