# PC_SOLVER_BACKEND.py — exact finite-domain solver over PC_TYPED_DAG (systematic search).
# Complete: SAT iff model exists within domains; UNSAT iff search exhausts; UNKNOWN only on cap.
# Deterministic (fixed var order) => rerunnable (V12/V15). Dinic hook for inventory subproblems.
import sys, time
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_TYPED_DAG import DAG, BOOL, INT

SAT, UNSAT, UNKNOWN = 'SAT', 'UNSAT', 'UNKNOWN'


def struct_order(tag):
    """Splitting order: counts -> structure (present/parent/side/depth) -> labels -> paths ->
    B-trace -> bounds -> hidden-S -> allocation -> ranks last (loosest)."""
    def key(v):
        s = v[len(tag):] if v.startswith(tag) else v
        if s in ('_H', '_w', '_nev', '_q'):
            return (0, s)
        if '_p' in s and s.split('_p')[-1].isdigit():
            return (1, s)
        if any(k in s for k in ('_par', '_side', '_dep', '_kl', '_kr', '_cl', '_cr')):
            return (2, s)
        if any(k in s for k in ('_isS', '_sidx', '_eK', '_eT', '_ed')):
            return (3, s)
        if any(k in s for k in ('_ep', '_edir', '_bT', '_bd', '_bp', '_bdir')):
            return (4, s)
        if any(k in s for k in ('_lo', '_hi', '_blo', '_bhi', '_bkl', '_bkr', '_brl', '_brr', '_broot')):
            return (5, s)
        if '_hs' in s:
            return (6, s)
        if '_z' in s or '_sg' in s or '_sig' in s:
            return (7, s)
        if '_rank' in s:
            return (9, s)
        return (8, s)
    return key


class Solver:
    def __init__(self, dag, domains=None, node_cap=2000000, time_cap=600, order=None):
        self.d = dag
        self.dom = dict(domains) if domains else {}
        self.node_cap = node_cap
        self.time_cap = time_cap
        self.order = order  # optional key function for var splitting order
        self.visits = 0
        self.t0 = 0
        self._memo = {}
        self._eqs = None

    def domain(self, name, nid):
        if name in self.dom:
            lo, hi = self.dom[name]
            return (lo, hi)
        k, t, a, e = self.d.nodes[nid]
        if t == BOOL:
            return (0, 1)
        w = self.d.width_of(nid)
        signed = e[3] if (k == 'var' and len(e) > 3) else False
        if signed:
            return (-(1 << (w - 1)), (1 << (w - 1)) - 1)
        return (0, (1 << w) - 1)

    def solve(self, root, assume=None):
        self.t0 = time.time()
        self.visits = 0
        self._memo = {}
        env = dict(assume) if assume else {}
        # top-level EQ propagation: EQ(var, const) and EQ(var, var) along the AND spine
        self._propagate_top(root, env)
        # assumption-based simplification (constant folding): shrinks the search DAG
        sroot = self.d.simplify(root, env)
        free = self.d.vars_in(sroot) - set(env)
        if self.order is not None:
            varnames = sorted(free, key=self.order)
        else:
            varnames = sorted(free)
        doms = {}
        for v in varnames:
            lo, hi = self.domain(v, self.d.vars[v])
            doms[v] = [lo, hi]
        r, menv, stats = self._search(sroot, env, doms, varnames, 0)
        stats = dict(stats)
        stats['simp_nodes'] = self.d.count()
        if r == SAT:
            full = dict(env)
            full.update(menv)
            return (r, full, stats)
        return (r, menv, stats)

    def _propagate_top(self, root, env):
        """Pin unconditional EQ(var,const) along the AND spine into env.
        Sound: only top-level AND conjuncts (must-hold). Fixpoint over spine-found EQs only."""
        d = self.d
        eqs = []
        stack = [root]
        while stack:
            n = stack.pop()
            k, t, a, e = d.nodes[n]
            if k == 'and':
                stack.extend(a)
            elif k == 'eq':
                eqs.append((a[0], a[1]))
        for _ in range(10):
            changed = False
            for x, y in eqs:
                if self._prop_eq(x, y, env):
                    changed = True
            if not changed:
                break

    def _prop_eq(self, x, y, env):
        d = self.d
        vx = self._as_varconst(x, env)
        vy = self._as_varconst(y, env)
        if vx is None or vy is None:
            return False
        (kx, vx), (ky, vy) = vx, vy
        if kx == 'const' and ky == 'var' and vy not in env:
            env[vy] = vx
            return True
        if kx == 'var' and ky == 'const' and vx not in env:
            env[vx] = vy
            return True
        return False

    def _as_varconst(self, n, env):
        k, t, a, e = self.d.nodes[n]
        if k == 'const':
            return ('const', bool(e) if t == BOOL else e[0])
        if k == 'var':
            if e[1] in env:
                v = env[e[1]]
                return ('const', bool(v) if t == BOOL else v)
            return ('var', e[1])
        return None

    def _interval(self, n, env, doms):
        """Returns (lo,hi) bounding value. Memoized per search visit (self._memo cleared per visit)."""
        if n in self._memo:
            return self._memo[n]
        r = self._interval_raw(n, env, doms)
        self._memo[n] = r
        return r

    def _interval_raw(self, n, env, doms):
        k, t, a, e = self.d.nodes[n]
        if k == 'const':
            v = bool(e) if t == BOOL else e[0]
            return (int(v), int(v))
        if k == 'var':
            name = e[1]
            if name in env:
                return (env[name], env[name])
            return tuple(doms[name])
        if k in ('not', 'and', 'or', 'xor', 'eq', 'lt', 'le'):
            v = self._bool(n, env, doms)
            return (1, 1) if v is True else ((0, 0) if v is False else (0, 1))
        if k == 'ite':
            c = self._bool(a[0], env, doms)
            if c is True:
                return self._interval(a[1], env, doms)
            if c is False:
                return self._interval(a[2], env, doms)
            l1, h1 = self._interval(a[1], env, doms)
            l2, h2 = self._interval(a[2], env, doms)
            return (min(l1, l2), max(h1, h2))
        if k == 'add':
            l1, h1 = self._interval(a[0], env, doms)
            l2, h2 = self._interval(a[1], env, doms)
            return (l1 + l2, h1 + h2)
        if k == 'sub':
            l1, h1 = self._interval(a[0], env, doms)
            l2, h2 = self._interval(a[1], env, doms)
            return (l1 - h2, h1 - l2)
        if k == 'exists':
            v = self._bool(a[0], env, doms)
            return (1, 1) if v is True else ((0, 0) if v is False else (0, 1))
        raise AssertionError(k)

    def _bool(self, n, env, doms):
        key=('b',n)
        if key in self._memo:
            return self._memo[key]
        r=self._bool_raw(n, env, doms)
        self._memo[key]=r
        return r
    def _bool_raw(self, n, env, doms):
        k, t, a, e = self.d.nodes[n]
        if k == 'const':
            return bool(e) if t == BOOL else None
        if k == 'var':
            name = e[1]
            if t == BOOL:
                return None if name not in env else bool(env[name])
            return None
        if k == 'not':
            v = self._bool(a[0], env, doms)
            return None if v is None else (not v)
        if k == 'and':
            x, y = self._bool(a[0], env, doms), self._bool(a[1], env, doms)
            if x is False or y is False:
                return False
            if x is True and y is True:
                return True
            return None
        if k == 'or':
            x, y = self._bool(a[0], env, doms), self._bool(a[1], env, doms)
            if x is True or y is True:
                return True
            if x is False and y is False:
                return False
            return None
        if k == 'xor':
            x, y = self._bool(a[0], env, doms), self._bool(a[1], env, doms)
            return None if x is None or y is None else (x != y)
        if k == 'ite':
            c = self._bool(a[0], env, doms)
            if c is True:
                return self._bool(a[1], env, doms)
            if c is False:
                return self._bool(a[2], env, doms)
            x, y = self._bool(a[1], env, doms), self._bool(a[2], env, doms)
            if x is True and y is True:
                return True
            if x is False and y is False:
                return False
            return None
        if k == 'eq':
            if self.d.typ(a[0]) == BOOL:
                x, y = self._bool(a[0], env, doms), self._bool(a[1], env, doms)
                return None if x is None or y is None else (x == y)
            l1, h1 = self._interval(a[0], env, doms)
            l2, h2 = self._interval(a[1], env, doms)
            if h1 < l2 or h2 < l1:
                return False
            if l1 == h1 == l2 == h2:
                return True
            return None
        if k in ('lt', 'le'):
            l1, h1 = self._interval(a[0], env, doms)
            l2, h2 = self._interval(a[1], env, doms)
            if k == 'lt':
                if h1 < l2:
                    return True
                if l1 >= h2:
                    return False
                return None
            if h1 <= l2:
                return True
            if l1 > h2:
                return False
            return None
        if k == 'exists':
            return self._bool(a[0], env, doms)
        # int node in bool position
        return None

    def _search(self, root, env, doms, varnames, idx):
        self.visits += 1
        if self.visits > self.node_cap or time.time() - self.t0 > self.time_cap:
            return (UNKNOWN, dict(env), {'visits': self.visits})
        _, v = self.d.ev3_iter(root, env, doms)
        if v is True:
            # complete remaining vars arbitrarily (first values) to full witness
            full = dict(env)
            for w in varnames:
                if w not in full:
                    full[w] = doms[w][0]
            return (SAT, full, {'visits': self.visits})
        if v is False:
            return (UNSAT, None, {'visits': self.visits})
        # pick next unassigned var (deterministic order)
        w = None
        for c in varnames:
            if c not in env:
                w = c
                break
        if w is None:
            return (UNSAT, None, {'visits': self.visits})
        lo, hi = doms[w]
        # try values lo..hi (deterministic)
        for val in range(lo, hi + 1):
            env[w] = val
            self._memo = {}  # env changed: invalidate visit memo (soundness)
            r = self._search(root, env, doms, varnames, idx + 1)
            del env[w]
            if r[0] in (SAT, UNKNOWN):
                return r
        return (UNSAT, None, {'visits': self.visits})


def freshen(dag, names, prefix):
    """Capture-safe renaming: copy variable names with prefix (for shadowed binders, V12)."""
    mp = {v: prefix + v for v in names}
    return mp
