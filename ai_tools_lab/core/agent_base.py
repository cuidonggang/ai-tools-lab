"""Base classes for AI agents used across all business domains."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentContext:
    """Runtime context passed to an agent when it is invoked."""

    input: Any
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    """Standardized result returned by an agent."""

    output: Any
    success: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """Common contract every domain agent must implement."""

    name: str = "base_agent"
    description: str = ""

    @abstractmethod
    def run(self, context: AgentContext) -> AgentResult:
        """Execute the agent's task and return a result."""
        raise NotImplementedError
