# CW_QUANTIFIED_BACKEND.py — V-semantics quantified solver for the closed-walk rescue.
# Historical Solver (PC_SOLVER_BACKEND) treats EXISTS transparently and splits bound vars at
# outer level, which is unsound under capture (e.g. NOT EXISTS z (z=1) wrongly SAT).
# QSolver is capture-safe WITHOUT touching history:
#   1. pin stripping: outer assumptions on bound names are capture (meaningless under
#      V-semantics); the intended target constraint already lives INSIDE the binder body
#      (X over QO2/QO/QM shares the binder). Stripped pins dangle harmlessly.
#   2. bound exclusion: bound vars are never split at outer level.
#   3. leaf sub-solving: at DPLL leaves, EXISTS nodes are decided by recursive sub-search
#      over their bound vars (shared caps; UNKNOWN on exhaustion — never a wrong claim).
# SAT claims rest on genuine sub-solve witnesses; UNSAT claims rest on exhaustive search.
# Returned models are best-effort on shadowed bound names; STATUS is authoritative.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_SOLVER_BACKEND import Solver, SAT, UNSAT, UNKNOWN

sys.setrecursionlimit(50000)


class QSolver(Solver):
    def bound_in(self, root):
        """Union of bound names over all EXISTS nodes in the cone."""
        d = self.d
        out = set()
        for m in d.topo([root]):
            k, t, a, e = d.nodes[m]
            if k == 'exists':
                out.update(e)
        return out

    def solve(self, root, assume=None):
        import time
        self.t0 = time.time()
        self.visits = 0
        bound = self.bound_in(root)
        env = {k: v for k, v in (assume or {}).items() if k not in bound}
        self._propagate_top(root, env)
        for k in [k for k in env if k in bound]:
            del env[k]
        sroot = self.d.simplify(root, env)
        free = self.d.vars_in(sroot) - set(env)
        if self.order is not None:
            splitvars = sorted((free - bound), key=self.order)
        else:
            splitvars = sorted(free - bound)
        doms = {}
        for v in free:
            lo, hi = self.domain(v, self.d.vars[v])
            doms[v] = [lo, hi]
        r, menv, stats = self._qsearch(sroot, env, doms, splitvars)
        stats = dict(stats)
        stats['simp_nodes'] = self.d.count()
        stats['qbound'] = len(bound & free)
        if r == SAT:
            full = dict(env)
            full.update(menv)
            return (r, full, stats)
        return (r, menv, stats)

    def _qsearch(self, root, env, doms, splitvars):
        import time
        self.visits += 1
        if self.visits > self.node_cap or time.time() - self.t0 > self.time_cap:
            return (UNKNOWN, dict(env), {'visits': self.visits})
        _, v = self.d.ev3_iter(root, env, doms)
        if v is True:
            full = dict(env)
            for w in splitvars:
                if w not in full:
                    full[w] = doms[w][0]
            wit = {}
            self._decide(root, full, doms, wit, {})
            full.update(wit)
            return (SAT, full, {'visits': self.visits})
        if v is False:
            return (UNSAT, None, {'visits': self.visits})
        w = None
        for c in splitvars:
            if c not in env:
                w = c
                break
        if w is None:
            wit, sub = {}, {}
            dv = self._decide(root, env, doms, wit, sub)
            if dv is True:
                full = dict(env)
                full.update(wit)
                return (SAT, full, {'visits': self.visits})
            if dv is False:
                return (UNSAT, None, {'visits': self.visits})
            if not sub and not self._has_exists(root):
                return (UNSAT, None, {'visits': self.visits})
            return (UNKNOWN, dict(env), {'visits': self.visits})
        lo, hi = doms[w]
        for val in range(lo, hi + 1):
            env[w] = val
            r = self._qsearch(root, env, doms, splitvars)
            del env[w]
            if r[0] in (SAT, UNKNOWN):
                return r
        return (UNSAT, None, {'visits': self.visits})

    def _has_exists(self, root):
        for m in self.d.topo([root]):
            if self.d.nodes[m][0] == 'exists':
                return True
        return False

    def _decide(self, root, env, doms, wit, sub):
        """3-valued eval with EXISTS decided by sub-solving. Mirrors ev3_iter semantics for
        all other ops (sound True/False only); EXISTS: SAT->True, UNSAT->False, else None."""
        d = self.d
        vals = {}
        for m in d.topo([root]):
            k, t, a, e = d.nodes[m]
            if k == 'const':
                vals[m] = (True, bool(e)) if t == 'bool' else (False, (e[0], e[0]))
            elif k == 'var':
                nm = e[1]
                if nm in env:
                    v = env[nm]
                    vals[m] = (True, bool(v)) if t == 'bool' else (False, (v, v))
                elif t == 'bool':
                    vals[m] = (True, None)
                else:
                    vals[m] = (False, tuple(doms[nm]))
            elif k == 'not':
                _, v = vals[a[0]]
                vals[m] = (True, None if v is None else (not v))
            elif k == 'and':
                _, x = vals[a[0]]
                _, y = vals[a[1]]
                if x is False or y is False:
                    vals[m] = (True, False)
                elif x is True and y is True:
                    vals[m] = (True, True)
                else:
                    vals[m] = (True, None)
            elif k == 'or':
                _, x = vals[a[0]]
                _, y = vals[a[1]]
                if x is True or y is True:
                    vals[m] = (True, True)
                elif x is False and y is False:
                    vals[m] = (True, False)
                else:
                    vals[m] = (True, None)
            elif k == 'xor':
                _, x = vals[a[0]]
                _, y = vals[a[1]]
                vals[m] = (True, None if x is None or y is None else (x != y))
            elif k == 'ite':
                _, c = vals[a[0]]
                ta, va = vals[a[1]]
                tb, vb = vals[a[2]]
                if c is True:
                    vals[m] = (ta, va)
                elif c is False:
                    vals[m] = (tb, vb)
                elif ta and tb:
                    if va is True and vb is True:
                        vals[m] = (True, True)
                    elif va is False and vb is False:
                        vals[m] = (True, False)
                    else:
                        vals[m] = (True, None)
                else:
                    (l1, h1), (l2, h2) = va, vb
                    vals[m] = (False, (min(l1, l2), max(h1, h2)))
            elif k in ('add', 'sub'):
                _, (l1, h1) = vals[a[0]]
                _, (l2, h2) = vals[a[1]]
                if k == 'add':
                    vals[m] = (False, (l1 + l2, h1 + h2))
                else:
                    vals[m] = (False, (l1 - h2, h1 - l2))
            elif k == 'eq':
                ta, va = vals[a[0]]
                tb, vb = vals[a[1]]
                if ta and tb:
                    vals[m] = (True, None if va is None or vb is None else (va == vb))
                else:
                    (l1, h1), (l2, h2) = va, vb
                    if h1 < l2 or h2 < l1:
                        vals[m] = (True, False)
                    elif l1 == h1 == l2 == h2:
                        vals[m] = (True, True)
                    else:
                        vals[m] = (True, None)
            elif k in ('lt', 'le'):
                _, (l1, h1) = vals[a[0]]
                _, (l2, h2) = vals[a[1]]
                if k == 'lt':
                    if h1 < l2:
                        vals[m] = (True, True)
                    elif l1 >= h2:
                        vals[m] = (True, False)
                    else:
                        vals[m] = (True, None)
                else:
                    if h1 <= l2:
                        vals[m] = (True, True)
                    elif l1 > h2:
                        vals[m] = (True, False)
                    else:
                        vals[m] = (True, None)
            elif k == 'exists':
                if m in sub:
                    vals[m] = (True, sub[m])
                    continue
                body = a[0]
                bset = set(e)
                if self.order is not None:
                    bvars = sorted((bset - set(env)), key=self.order)
                else:
                    bvars = sorted(bset - set(env))
                r, menv, _ = self._qsearch(body, dict(env), doms, bvars)
                if r == SAT:
                    sub[m] = True
                    for bk, bv in menv.items():
                        if bk in bset and bk not in env and bk not in wit:
                            wit[bk] = bv
                    vals[m] = (True, True)
                elif r == UNSAT:
                    sub[m] = False
                    vals[m] = (True, False)
                else:
                    vals[m] = (True, None)
            else:
                raise AssertionError(k)
        isb, v = vals[root]
        return v if isb else None
