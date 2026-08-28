"""Tools used by engineering management agents (工程管理)."""
from __future__ import annotations

from typing import Any

from ...core.registry import registry
from ...core.tool_base import BaseTool


@registry.register_tool
class MilestoneRiskTool(BaseTool):
    """Flags a milestone as at-risk when remaining slack is below a threshold."""

    name = "engineering.milestone_risk"
    description = "根据剩余时差判断里程碑是否存在延期风险"

    def execute(self, remaining_days: int, threshold_days: int = 3, **kwargs: Any) -> bool:
        return remaining_days <= threshold_days
