"""Alias lookup adapter backed by a knowledge-source query."""

from intelligence.matchers.exact_matcher import ExactMatcher


class AliasMatcher(ExactMatcher):
    """Names the alias-matching role while sharing exact lookup mechanics."""
