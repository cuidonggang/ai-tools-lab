"""Registry for discovering agents and tools across domains."""
from __future__ import annotations

from .agent_base import BaseAgent
from .tool_base import BaseTool


class Registry:
    """Keeps track of registered agents and tools by name."""

    def __init__(self) -> None:
        self._agents: dict[str, type[BaseAgent]] = {}
        self._tools: dict[str, type[BaseTool]] = {}

    def register_agent(self, agent_cls: type[BaseAgent]) -> type[BaseAgent]:
        """Class decorator that registers an agent under its `name`."""
        self._agents[agent_cls.name] = agent_cls
        return agent_cls

    def register_tool(self, tool_cls: type[BaseTool]) -> type[BaseTool]:
        """Class decorator that registers a tool under its `name`."""
        self._tools[tool_cls.name] = tool_cls
        return tool_cls

    def get_agent(self, name: str) -> type[BaseAgent]:
        return self._agents[name]

    def get_tool(self, name: str) -> type[BaseTool]:
        return self._tools[name]

    def list_agents(self) -> list[str]:
        return sorted(self._agents)

    def list_tools(self) -> list[str]:
        return sorted(self._tools)


# Process-wide singleton used by domain modules to self-register.
registry = Registry()
