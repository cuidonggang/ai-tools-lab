"""Agents for engineering / project management (工程管理)."""
from __future__ import annotations

from ...core.agent_base import AgentContext, AgentResult, BaseAgent
from ...core.registry import registry


@registry.register_agent
class ProjectScheduleAgent(BaseAgent):
    """Tracks project schedule progress and flags at-risk milestones."""

    name = "engineering.project_schedule"
    description = "跟踪工程项目进度，识别延期风险的里程碑"

    def run(self, context: AgentContext) -> AgentResult:
        raise NotImplementedError("TODO: implement schedule tracking logic")


@registry.register_agent
class DocumentReviewAgent(BaseAgent):
    """Reviews engineering documents (drawings, specs) for completeness/compliance."""

    name = "engineering.document_review"
    description = "审查工程图纸/技术文档的完整性与合规性"

    def run(self, context: AgentContext) -> AgentResult:
        raise NotImplementedError("TODO: implement document review logic")
