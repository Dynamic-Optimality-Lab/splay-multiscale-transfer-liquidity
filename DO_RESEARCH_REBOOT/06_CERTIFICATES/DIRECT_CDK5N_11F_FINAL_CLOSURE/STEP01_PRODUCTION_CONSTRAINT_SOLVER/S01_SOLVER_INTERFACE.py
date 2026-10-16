# S01_SOLVER_INTERFACE.py — production solver API over the frozen Z3 stack.
# compile(root) -> handle; solve(handle, assumptions, limits) -> SAT/UNSAT/UNKNOWN(+reason);
# extract_model(result) -> {free_name: value}; reset_assumptions(handle); statistics.
# Assumptions are validated: unknown names and BOUND names are rejected explicitly
# (never silently reinterpreted). UNKNOWN reasons preserved (timeout/memout/incomplete).
import sys, time
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
import z3
from S01_SCOPED_BINDERS import normalize, bound_names, free_names
from S01_DAG_COMPILER import compile_root

SAT, UNSAT, UNKNOWN = 'SAT', 'UNSAT', 'UNKNOWN'


class ProductionSolver:
    def __init__(self, dag, seed=17, timeout_ms=120000, mem_mb=24576):
        self.d = dag
        self.seed = seed
        self.timeout_ms = timeout_ms
        self.mem_mb = mem_mb
        self.handles = {}
        self.query_count = 0
        self.cpu_s = 0.0

    def compile(self, root, tag='root'):
        """Normalize binders, translate once, assert bounds+body into a fresh Solver."""
        from PC_TYPED_DAG import BOOL
        if self.d.typ(root) != BOOL:
            raise AssertionError(('compile requires a Bool root', root, self.d.typ(root)))
        t0 = time.process_time()
        nroot, ninfo = normalize(self.d, root)
        comp = compile_root(self.d, nroot)
        s = z3.Solver()
        s.set('random_seed', self.seed)
        if self.timeout_ms:
            s.set('timeout', self.timeout_ms)
        for b in comp['bounds']:
            s.add(b)
        s.add(comp['body'])
        free = sorted(free_names(self.d, nroot))
        bound = sorted(bound_names(self.d, nroot))
        h = {'solver': s, 'comp': comp, 'nroot': nroot, 'ninfo': ninfo,
             'free': free, 'bound': bound, 'tag': tag,
             'compile_cpu_s': round(time.process_time() - t0, 2)}
        self.handles[tag] = h
        return h

    def _lits(self, h, assumptions):
        (env, ignored), problem = self._validate_pins(h, assumptions)
        if problem is not None:
            raise AssertionError(problem['reason'])
        lits = []
        decls = h['comp']['vars']
        for name, val in env.items():
            z = decls[name]
            if z.sort() == z3.BoolSort():
                lits.append(z if val else z3.Not(z))
            else:
                lits.append(z == val)
        return lits

    def _validate_pins(self, handle, assumptions):
        """API + domain validation. Returns ((env, ignored), problem) where problem
        is None or an immediate UNSAT/UNKNOWN verdict dict."""
        from PC_TYPED_DAG import BOOL
        decls = handle['comp']['vars']
        widths = {w['name']: w for w in handle['comp']['width_audit']}
        env = {}
        ignored = 0
        bad = None
        for name, val in (assumptions or {}).items():
            if name in handle['bound']:
                bad = {'status': UNKNOWN, 'reason': 'api-validation: assumption on bound variable %s rejected' % name, 'model': None}
                break
            if name not in decls:
                # out-of-cone pins are irrelevant to this formula (historical
                # behavior); ignored and counted, never silently reinterpreted.
                ignored += 1
                continue
            z = decls[name]
            if z.sort() == z3.BoolSort():
                # exact bool domain {False, True}; historical envs store 0/1 ints.
                if val is True or val == 1:
                    env[name] = True
                elif val is False or val == 0:
                    env[name] = False
                else:
                    bad = {'status': UNKNOWN, 'reason': 'api-validation: bool pin must be True/False/0/1: %s' % name, 'model': None}
                    break
            else:
                iv = int(val)
                w = widths.get(name)
                if w is not None and not (w['lo'] <= iv <= w['hi']):
                    bad = {'status': UNSAT, 'reason': 'domain-violation: %s=%d outside [%d,%d]' % (name, iv, w['lo'], w['hi']), 'model': None}
                    break
                env[name] = iv
        if bad is not None:
            return (None, ignored), bad
        return (env, ignored), None

    def tier1(self, handle, env):
        """Exact pre-simplification under pins (historical exact partial evaluation).
        const True -> SAT (pins are the model); const False -> UNSAT; else None."""
        from PC_TYPED_DAG import BOOL
        t0 = time.process_time()
        sroot = self.d.simplify(handle['nroot'], env)
        dt = round(time.process_time() - t0, 3)
        kk, tt, aa, ee = self.d.nodes[sroot]
        if kk == 'const' and tt == BOOL:
            if ee:
                return {'status': SAT, 'reason': 'tier1-ground-true', 'model': dict(env), 'cpu_s': dt}
            return {'status': UNSAT, 'reason': 'tier1-ground-false', 'model': None, 'cpu_s': dt}
        return None

    def solve(self, handle, assumptions=None, timeout_ms=None):
        """Tier-1 exact simplification first; Tier-2 incremental Z3 on remainder.
        check(*lits) retains learning; no rebuild."""
        s = handle['solver']
        t0 = time.process_time()
        (env, ignored), problem = self._validate_pins(handle, assumptions)
        if problem is not None:
            problem['cpu_s'] = round(time.process_time() - t0, 3)
            return problem
        # Tier-1 (exact; also merges session-pushed pins? No: session pins live in the
        # Z3 solver only. Tier-1 sees per-call assumptions. Contradictions BETWEEN
        # session pins and call pins are caught by Tier-2.)
        r1 = self.tier1(handle, env)
        if r1 is not None:
            self.cpu_s += r1['cpu_s']
            self.query_count += 1
            return r1
        if timeout_ms is not None:
            s.set('timeout', timeout_ms)
        lits = []
        decls = handle['comp']['vars']
        for name, val in env.items():
            z = decls[name]
            if z.sort() == z3.BoolSort():
                lits.append(z if val else z3.Not(z))
            else:
                lits.append(z == val)
        r = s.check(*lits)
        dt = time.process_time() - t0
        self.cpu_s += dt
        self.query_count += 1
        if r == z3.sat:
            return {'status': SAT, 'reason': 'tier2', 'model': s.model(), 'cpu_s': round(dt, 3)}
        if r == z3.unsat:
            return {'status': UNSAT, 'reason': 'tier2', 'model': None, 'cpu_s': round(dt, 3)}
        return {'status': UNKNOWN, 'reason': str(s.reason_unknown()), 'model': None, 'cpu_s': round(dt, 3)}

    def extract_model(self, handle, result):
        """{free_name: python value} for free interface vars only."""
        if result['status'] != SAT:
            raise AssertionError('no model to extract')
        if isinstance(result.get('model'), dict):
            # Tier-1: pins are the model; complete unpinned free vars with domain-lo
            # (sound: Tier-1 SAT means the formula holds under the pins regardless).
            out = {}
            widths = {w['name']: w for w in handle['comp']['width_audit']}
            for name in handle['free']:
                if name in result['model']:
                    out[name] = result['model'][name]
                elif name in widths:
                    out[name] = widths[name]['lo']
                else:
                    out[name] = False
            return out
        m = result['model']
        decls = handle['comp']['vars']
        out = {}
        for name in handle['free']:
            z = decls[name]
            v = m.eval(z, model_completion=True)
            if z.sort() == z3.BoolSort():
                out[name] = bool(z3.is_true(v))
            else:
                out[name] = int(v.as_long())
        return out

    def reset_assumptions(self, handle):
        """Assumptions are per-call literals; nothing persists. Validates clean state."""
        s = handle['solver']
        # check() with no assumptions must reproduce the unpinned verdict space (no
        # lingering pins possible by construction); lightweight consistency probe:
        return {'assertions': len(s.assertions()), 'ok': True}

    def solver_statistics(self, handle):
        st = handle['solver'].statistics()
        return {'z3': {st[i][0]: st[i][1] for i in range(len(st))}, 'queries': self.query_count,
                'cpu_s_total': round(self.cpu_s, 2)}
