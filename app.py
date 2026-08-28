"""Application entry point for AI Tools Lab.

Importing `ai_tools_lab.domains` registers all agents/tools for the three
supported business domains (metrology, engineering, vision) into the shared
registry, which this CLI can then introspect.
"""
from __future__ import annotations

import argparse

from ai_tools_lab import domains  # noqa: F401  (side effect: registers agents/tools)
from ai_tools_lab.core.registry import registry


def list_agents() -> None:
    print("Registered agents:")
    for agent_name in registry.list_agents():
        print(f"  - {agent_name}")


def list_tools() -> None:
    print("Registered tools:")
    for tool_name in registry.list_tools():
        print(f"  - {tool_name}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AI Tools Lab - 面向计量检测/工程管理/视觉检测的 AI 工具与 Agent 平台"
    )
    parser.add_argument("--list-tools", action="store_true", help="列出已注册的 Tool")
    args = parser.parse_args()

    list_agents()
    if args.list_tools:
        list_tools()


if __name__ == "__main__":
    main()

