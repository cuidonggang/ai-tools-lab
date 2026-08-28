"""Tools used by metrology agents (计量检测)."""
from __future__ import annotations

from typing import Any

from ...core.registry import registry
from ...core.tool_base import BaseTool


@registry.register_tool
class ToleranceCheckTool(BaseTool):
    """Checks whether a measured value falls within a given tolerance range."""

    name = "metrology.tolerance_check"
    description = "校验测量值是否在允许公差范围内"

    def execute(self, value: float, nominal: float, tolerance: float, **kwargs: Any) -> bool:
        return abs(value - nominal) <= tolerance
