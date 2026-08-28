"""Confirms ReportAuditAgent is registered and wired to AuditService."""
from __future__ import annotations

from pathlib import Path

from ai_tools_lab import domains  # noqa: F401  (side effect: registers agents/tools)
from ai_tools_lab.core.agent_base import AgentContext
from ai_tools_lab.core.registry import registry

FIXTURES = Path(__file__).parent / "fixtures"


def test_report_audit_agent_runs_end_to_end() -> None:
    agent_cls = registry.get_agent("metrology.report_audit")
    result = agent_cls().run(AgentContext(input=FIXTURES / "good_report.txt"))
    assert result.success
    assert result.metadata["summary"]["error"] == 0
