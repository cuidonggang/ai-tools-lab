"""Base class for tools that agents can call."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """Common contract every tool must implement."""

    name: str = "base_tool"
    description: str = ""

    @abstractmethod
    def execute(self, **kwargs: Any) -> Any:
        """Run the tool with the given arguments."""
        raise NotImplementedError
