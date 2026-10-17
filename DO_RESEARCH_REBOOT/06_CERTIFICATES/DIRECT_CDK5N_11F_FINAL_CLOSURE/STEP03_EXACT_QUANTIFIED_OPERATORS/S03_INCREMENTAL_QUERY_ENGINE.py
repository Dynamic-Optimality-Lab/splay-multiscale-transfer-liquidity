# S03_INCREMENTAL_QUERY_ENGINE.py — compile-once query cache (Gate H/G13).
# One handle per distinct operator/edge root; per-query Tier-1-first decisions;
# Tier-2 with caps only for leftovers; per-root statistics. No DAG rebuild per query.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
from S02_RESIDUAL_SOLVER import ResidualSolver

SAT, UNSAT, UNKNOWN = 'SAT', 'UNSAT', 'UNKNOWN'


class QueryEngine:
    def __init__(self, dag, seed=17, timeout_ms=120000):
        self.rs = ResidualSolver(dag, seed=seed, timeout_ms=timeout_ms)
        self.tags = {}

    def compile_root(self, root, tag):
        if tag not in self.tags:
            self.rs.handle(root, tag)
            self.tags[tag] = True
        return self.rs.eng.ps.handles[tag]

    def decide(self, root, pins, timeout_ms=None, tag=None):
        tg = tag or ('q%d' % len(self.tags))
        self.compile_root(root, tg)
        if timeout_ms is not None:
            return self.rs.search_residual(tg, pins, timeout_ms)
        return self.rs.verify(tg, pins)

    def stats(self):
        return dict(self.rs.stats, handles=len(self.tags),
                    queries=self.rs.eng.ps.query_count,
                    cpu_s=round(self.rs.eng.ps.cpu_s, 1))
