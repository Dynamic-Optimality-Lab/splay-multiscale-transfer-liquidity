# S01_INCREMENTAL_ENGINE.py — compile-once registry + multi-query sessions.
# One compiled handle per root (structural sharing preserved; no rebuild per query).
# Sessions use push/pop around assumption groups; per-query assumptions go through
# check(*lits) so learned clauses survive across queries.
import sys, time
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
from S01_SOLVER_INTERFACE import ProductionSolver, SAT, UNSAT, UNKNOWN


class IncrementalEngine:
    def __init__(self, dag, **kw):
        self.ps = ProductionSolver(dag, **kw)
        self.sessions = 0

    def compile_once(self, root, tag):
        if tag in self.ps.handles:
            return self.ps.handles[tag]
        return self.ps.compile(root, tag)

    def query(self, tag, assumptions, timeout_ms=None):
        return self.ps.solve(self.ps.handles[tag], assumptions, timeout_ms)

    def session(self, tag):
        return _Session(self, tag)


class _Session:
    """push/pop group: shared pins asserted once, sub-queries vary the rest."""
    def __init__(self, eng, tag):
        self.eng = eng
        self.tag = tag

    def __enter__(self):
        h = self.eng.ps.handles[self.tag]
        h['solver'].push()
        self.eng.sessions += 1
        return self

    def __exit__(self, *a):
        self.eng.ps.handles[self.tag]['solver'].pop()
        return False

    def pin(self, assumptions):
        h = self.eng.ps.handles[self.tag]
        lits = self.eng.ps._lits(h, assumptions)
        for L in lits:
            h['solver'].add(L)

    def query(self, assumptions=None, timeout_ms=None):
        return self.eng.query(self.tag, assumptions, timeout_ms)
