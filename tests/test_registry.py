"""Smoke tests ensuring all domain agents/tools register correctly."""
from ai_tools_lab import domains  # noqa: F401  (side effect: registers agents/tools)
from ai_tools_lab.core.registry import registry


def test_agents_registered_for_all_domains() -> None:
    agents = registry.list_agents()
    assert any(name.startswith("metrology.") for name in agents)
    assert any(name.startswith("engineering.") for name in agents)
    assert any(name.startswith("vision.") for name in agents)


def test_tools_registered_for_all_domains() -> None:
    tools = registry.list_tools()
    assert any(name.startswith("metrology.") for name in tools)
    assert any(name.startswith("engineering.") for name in tools)
    assert any(name.startswith("vision.") for name in tools)
