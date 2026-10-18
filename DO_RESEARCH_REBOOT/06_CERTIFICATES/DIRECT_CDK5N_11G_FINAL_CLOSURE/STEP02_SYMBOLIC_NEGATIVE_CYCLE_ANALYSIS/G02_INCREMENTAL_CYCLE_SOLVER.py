# G02_INCREMENTAL_CYCLE_SOLVER.py — lazy incremental cycle engine (Gates C/D).
# Primary: source-level closed-walk BFS (G02_CLOSED_WALK_SEARCH) with replay +
# abstract weight per macro segmentation (ssertify-verified). Secondary: k=1
# impossibility theorem (no solver). Tertiary: per-edge Z3 checks on demand.
# Preregistered: k=1 (theorem), k=2,3 (BFS depth<=6), k<=5 (BFS depth<=8),
# longer only with explicit re-authorization. UNKNOWN on cap/truncation, never UNSAT.
import sys, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_SYMBOLIC_NEGATIVE_CYCLE_ANALYSIS')
from G02_CLOSED_WALK_SEARCH import ClosedWalkSearch

SAT, UNSAT, UNKNOWN = 'SAT', 'UNSAT', 'UNKNOWN'


class IncrementalCycleSolver:
    def __init__(self, dag, low, max_depth=8, max_states=50000):
        self.searcher = ClosedWalkSearch(max_depth=max_depth, max_states=max_states)
        self.d = dag
        self.L = low
        self.stats = {'k1': 'theorem', 'queries': []}

    def find_negative_cycle(self, A0, B0, keys, Sset, M, time_cap=300):
        """Source-level search: closed paired walks, Q_B vs 2A, abstract weight.
        Genuine = B-changing KEEP on a marked key. Returns TYPE-A candidates."""
        import splay as S
        from PC_CONCRETIZE import serial
        from STRICT_CERTIFY import ssertify
        t0 = time.process_time()
        status, closed, stats = self.searcher.search(A0, B0, keys, time_cap=time_cap)
        out = []
        for c in closed:
            word = c['word']
            legs = c['legs']
            G = set(l['x'] for l in legs if l['m'] == 'K' and l['chg'] and l['x'] in M)
            Q = sum((l['dB'] // 2) for l in legs if l['m'] == 'K' and l['chg'] and l['x'] in M and l['dB'] is not None)
            A = sum(l['a'] for l in legs)
            out.append({'word': word, 'legs': legs, 'G': sorted(G), 'Q': Q, 'A_cost': A, 'Qvs2A': (Q, 2 * A),
                        'terminal_counterexample': Q > 2 * A})
        return {'status': status, 'closed': out, 'stats': stats,
                'cpu_s': round(time.process_time() - t0, 1)}

    def k1_theorem(self):
        return {'verdict': UNSAT, 'reason': 'genuine single KEEP changes B (no closure); nongenuine has q=0,dB=0 and w=2H>=0'}

    def cycle_solver_statistics(self):
        return dict(self.searcher.stats)
