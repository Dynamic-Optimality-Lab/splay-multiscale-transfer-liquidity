# S02_RESIDUAL_SOLVER.py — frozen-Z3 residual engine (Gate F infrastructure).
# Patched compile (in-scope bounds) + session-aware Tier-1 + Tier-2 incremental Z3.
# Compile-once per relation tag; per-candidate Tier-1 verification reuses the handle
# (no rebuild). Tier-2 with caps for genuinely under-constrained residuals.
# UNSAT learning: Tier-1 pin-sets recorded; duplicate skeletons skipped by signature.
import sys, time
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
from S01_SOLVER_INTERFACE import ProductionSolver, SAT, UNSAT, UNKNOWN
from S01_INCREMENTAL_ENGINE import IncrementalEngine
from S02_SEMANTIC_SAFETY_PATCH import install_scoped_compile


class ResidualSolver:
    def __init__(self, dag, seed=17, timeout_ms=120000):
        self.eng = IncrementalEngine(dag, seed=seed, timeout_ms=timeout_ms)
        install_scoped_compile(self.eng.ps)
        self.dag = dag
        self.tried = set()  # skeleton signatures already decided (dedup = learning)
        self.stats = {'tier1_sat': 0, 'tier1_unsat': 0, 'tier2_sat': 0, 'tier2_unsat': 0,
                      'tier2_unknown': 0, 'skipped_dup': 0}

    def handle(self, root, tag):
        return self.eng.compile_once(root, tag)

    def verify(self, tag, pins):
        """Tier-1-first verification on the shared handle. Returns result dict."""
        r = self.eng.query(tag, pins)
        rs = r['status']
        if rs == SAT and r.get('reason', '').startswith('tier1'):
            self.stats['tier1_sat'] += 1
        elif rs == UNSAT and r.get('reason', '').startswith('tier1'):
            self.stats['tier1_unsat'] += 1
        elif rs == SAT:
            self.stats['tier2_sat'] += 1
        elif rs == UNSAT:
            self.stats['tier2_unsat'] += 1
        else:
            self.stats['tier2_unknown'] += 1
        return r

    def search_residual(self, tag, pins, timeout_ms):
        """Tier-2 on under-constrained residual (fallback path)."""
        return self.eng.query(tag, pins, timeout_ms=timeout_ms)

    def model(self, tag, result):
        return self.eng.ps.extract_model(self.eng.ps.handles[tag], result)
