"""Registry for independent conclusion-building rules."""

from typing import Protocol

from reasoning.context import ReasoningContext


class ReasoningRule(Protocol):
    name: str
    def apply(self, context: ReasoningContext) -> None:
        """Add justified conclusions to a reasoning context."""


class ReasoningRegistry:
    def __init__(self):
        self._rules: dict[str, ReasoningRule] = {}

    def register(self, rule: ReasoningRule) -> None:
        self._rules[rule.name] = rule

    def rules(self) -> tuple[ReasoningRule, ...]:
        return tuple(self._rules.values())
