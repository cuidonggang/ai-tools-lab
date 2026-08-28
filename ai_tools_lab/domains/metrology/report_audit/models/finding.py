"""Unified audit finding model produced by every auditor in the pipeline."""
from __future__ import annotations

import uuid
from enum import Enum

from pydantic import BaseModel, Field

from ai_tools_lab.domains.metrology.report_audit.models.locator import SourceLocator


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class Category(str, Enum):
    COMPLETENESS = "completeness"
    FORMAT = "format"
    CONSISTENCY = "consistency"
    CALCULATION = "calculation"
    TRACEABILITY = "traceability"
    STANDARD = "standard"
    MEASUREMENT = "measurement"
    UNCERTAINTY = "uncertainty"
    CONCLUSION = "conclusion"
    SEMANTIC = "semantic"
    COMPLIANCE = "compliance"


class ReviewState(str, Enum):
    """Human-in-the-loop review status. Every finding starts as AI_DETECTED."""

    AI_DETECTED = "ai_detected"
    HUMAN_CONFIRMED = "human_confirmed"
    HUMAN_REJECTED = "human_rejected"
    HUMAN_MODIFIED = "human_modified"
    RESOLVED = "resolved"


class Evidence(BaseModel):
    """A piece of proof backing a finding: either a structured field or a text excerpt."""

    field: str | None = None
    value: str | None = None
    locator: SourceLocator | None = None
    excerpt: str | None = None


class AuditFinding(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    category: Category
    severity: Severity
    title: str
    description: str
    evidence: list[Evidence] = []
    rule_id: str | None = None
    source: str  # "completeness" | "rule" | "consistency" | "calculation" | "llm"
    confidence: float = 1.0
    suggestion: str | None = None
    requires_human_review: bool = True
    review_state: ReviewState = ReviewState.AI_DETECTED
