"""Small, deterministic plan optimization rules."""

from query.engine.planner import QueryPlan


class QueryOptimizer:
    def optimize(self, plan: QueryPlan) -> QueryPlan:
        """Remove repeated object identities while preserving transaction order."""
        seen: set[int] = set()
        seed = tuple(item for item in plan.seed if not (id(item) in seen or seen.add(id(item))))
        return QueryPlan(seed=seed, index_used=plan.index_used)
