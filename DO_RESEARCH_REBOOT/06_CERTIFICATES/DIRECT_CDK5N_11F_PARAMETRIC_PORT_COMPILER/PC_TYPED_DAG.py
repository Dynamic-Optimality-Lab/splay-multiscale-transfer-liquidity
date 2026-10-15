# PC_TYPED_DAG.py — hash-consed typed symbolic DAG (Bool + finite-domain Int).
# Nodes are shared structurally (canonical identities). Widths fixed per use; exact
# (wrap-free) arithmetic inside proved ranges (see WIDTHS in PC_AZ_REPORT.md).
import itertools


def prefix_rename(name, mp):
    return mp.get(name, name)

BOOL, INT = 'bool', 'int'


class DAG:
    def __init__(self):
        self.tab = {}   # key -> nid
        self.nodes = []  # nid -> (kind, type, args, extra)
        self.vars = {}   # name -> nid

    def _mk(self, kind, typ, args, extra=None):
        key = (kind, typ, tuple(args), extra if extra is None or isinstance(extra, (int, str, tuple)) else str(extra))
        if isinstance(extra, list):
            extra = tuple(extra)
            key = (kind, typ, tuple(args), extra)
        n = self.tab.get(key)
        if n is not None:
            return n
        n = len(self.nodes)
        self.nodes.append((kind, typ, tuple(args), extra))
        self.tab[key] = n
        return n

    # ---- leaves ----
    def const_bool(self, v):
        return self._mk('const', BOOL, (), 1 if v else 0)

    def const_int(self, v, width, signed=False):
        assert -(1 << (width - 1)) <= v < (1 << width) if signed else 0 <= v < (1 << width), (v, width, signed)
        return self._mk('const', INT, (), (v, width, signed))

    def var_bool(self, name):
        if name in self.vars:
            return self.vars[name]
        n = self._mk('var', BOOL, (), ('b', name))
        self.vars[name] = n
        return n

    def var_int(self, name, width, signed=False, lo=None, hi=None):
        if name in self.vars:
            return self.vars[name]
        n = self._mk('var', INT, (), ('i', name, width, signed))
        self.vars[name] = n
        return n

    # ---- bool ----
    def NOT(self, a):
        self._t(BOOL, a)
        return self._mk('not', BOOL, (a,))

    def AND(self, *a):
        for x in a:
            self._t(BOOL, x)
        if len(a) == 0:
            return self.const_bool(True)
        if len(a) == 1:
            return a[0]
        n = a[0]
        for x in a[1:]:
            n = self._mk('and', BOOL, (n, x))
        return n

    def OR(self, *a):
        for x in a:
            self._t(BOOL, x)
        if len(a) == 0:
            return self.const_bool(False)
        if len(a) == 1:
            return a[0]
        n = a[0]
        for x in a[1:]:
            n = self._mk('or', BOOL, (n, x))
        return n

    def XOR(self, a, b):
        self._t(BOOL, a)
        self._t(BOOL, b)
        return self._mk('xor', BOOL, (a, b))

    def ITE(self, c, a, b):
        self._t(BOOL, c)
        ta = self.typ(a)
        assert ta == self.typ(b), (ta, self.typ(b))
        return self._mk('ite', ta, (c, a, b))

    # ---- int (all args INT; widths tracked, exact in proved ranges) ----
    def ADD(self, a, b, width):
        self._t(INT, a)
        self._t(INT, b)
        return self._mk('add', INT, (a, b), width)

    def SUB(self, a, b, width):
        self._t(INT, a)
        self._t(INT, b)
        return self._mk('sub', INT, (a, b), width)

    def EQ(self, a, b):
        assert self.typ(a) == self.typ(b)
        return self._mk('eq', BOOL, (a, b))

    def LT(self, a, b):
        self._t(INT, a)
        self._t(INT, b)
        return self._mk('lt', BOOL, (a, b))

    def LE(self, a, b):
        self._t(INT, a)
        self._t(INT, b)
        return self._mk('le', BOOL, (a, b))

    def EXISTS(self, varnames, body):
        """Existential binder (structure for Pre/Post/MinPre + witness xi). Solver eliminates by search."""
        self._t(BOOL, body)
        return self._mk('exists', BOOL, (body,), tuple(sorted(varnames)))

    # ---- introspection ----
    def typ(self, n):
        return self.nodes[n][1]

    def _t(self, t, n):
        assert self.typ(n) == t, (n, self.nodes[n], t)

    def count(self):
        return len(self.nodes)

    def width_of(self, n):
        k, t, a, e = self.nodes[n]
        if t == BOOL:
            return 1
        if k == 'const':
            return e[1]
        if k == 'var':
            return e[2]
        return e  # add/sub carry width

    def ev(self, n, env, _memo=None):
        raise AssertionError('recursive ev removed; use ev_iter')

    def vars_in(self, n):
        out = set()
        for m in self.topo([n]):
            k, t, a, e = self.nodes[m]
            if k == 'var':
                out.add(e[1])
        return out

    def subst(self, n, mp):
        """Rename variables by mp {oldname: newname}. Iterative over node ids (children < parents)."""
        newid = {}
        for m in range(len(self.nodes)):
            k, t, a, e = self.nodes[m]
            if k == 'var' and e[1] in mp:
                new = mp[e[1]]
                if t == BOOL:
                    r = self.var_bool(new)
                else:
                    w = e[2]
                    sg = e[3] if len(e) > 3 else False
                    r = self.var_int(new, w, sg)
                newid[m] = r
                continue
            if k == 'var' or not a:
                newid[m] = m
                continue
            na = tuple(newid[x] for x in a)
            if k == 'exists':
                ne = tuple(prefix_rename(x, mp) for x in e)
                r = self._mk(k, t, na, ne)
            else:
                r = self._mk(k, t, na, e)
            newid[m] = r
        return newid[n]

    def simplify(self, n, pins, _memo=None):
        """Partial evaluation under pins. ITERATIVE over node ids (children < parents always).
        Constant-folds ITEs/EQs/arith/bool connectives. Returns new root (same DAG)."""
        newid = {}
        for m in range(len(self.nodes)):
            k, t, a, e = self.nodes[m]
            if k == 'var' and e[1] in pins:
                v = pins[e[1]]
                newid[m] = self.const_bool(bool(v)) if t == BOOL else self.const_int(v, e[2], e[3] if len(e) > 3 else False)
                continue
            if k == 'var' or k == 'const':
                newid[m] = m
                continue
            na = tuple(newid[x] for x in a)
            nc = [self.nodes[x] for x in na]
            r = None
            if k == 'not' and nc[0][0] == 'const':
                r = self.const_bool(not nc[0][3])
            elif k == 'and':
                if any(x[0] == 'const' and not x[3] for x in nc):
                    r = self.const_bool(False)
                elif all(x[0] == 'const' for x in nc):
                    r = self.const_bool(True)
                elif nc[0][0] == 'const':
                    r = na[1]
                elif nc[1][0] == 'const':
                    r = na[0]
            elif k == 'or':
                if any(x[0] == 'const' and x[3] for x in nc):
                    r = self.const_bool(True)
                elif all(x[0] == 'const' for x in nc):
                    r = self.const_bool(False)
                elif nc[0][0] == 'const':
                    r = na[1]
                elif nc[1][0] == 'const':
                    r = na[0]
            elif k == 'xor' and all(x[0] == 'const' for x in nc):
                r = self.const_bool(bool(nc[0][3]) != bool(nc[1][3]))
            elif k == 'ite' and nc[0][0] == 'const':
                r = na[1] if nc[0][3] else na[2]
            elif k in ('add', 'sub') and all(x[0] == 'const' for x in nc):
                v0, v1 = nc[0][3][0], nc[1][3][0]
                v = v0 + v1 if k == 'add' else v0 - v1
                w = max(e if isinstance(e, int) else 16, abs(v).bit_length() + 2)
                r = self.const_int(v, w, v < 0)
            elif k in ('eq', 'lt', 'le'):
                ta = self.nodes[na[0]]
                tb = self.nodes[na[1]]
                if ta[0] == 'const' and tb[0] == 'const':
                    va = bool(ta[3]) if ta[1] == BOOL else ta[3][0]
                    vb = bool(tb[3]) if tb[1] == BOOL else tb[3][0]
                    if k == 'eq':
                        r = self.const_bool(va == vb)
                    elif k == 'lt':
                        r = self.const_bool(va < vb)
                    else:
                        r = self.const_bool(va <= vb)
            if r is None:
                r = self._mk(k, t, na, e)
            newid[m] = r
        return newid[n]

    def topo(self, roots):
        """Iterative postorder (children before parents). No recursion."""
        order = []
        seen = set()
        stack = [(r, False) for r in roots]
        while stack:
            n, done = stack.pop()
            if n in seen:
                continue
            if done:
                seen.add(n)
                order.append(n)
                continue
            stack.append((n, True))
            _, _, a, _ = self.nodes[n]
            for x in a:
                if x not in seen:
                    stack.append((x, False))
        return order

    def ev_iter(self, n, env):
        """Iterative exact evaluation (ground env). Bool-normalized."""
        vals = {}
        for m in self.topo([n]):
            k, t, a, e = self.nodes[m]
            if k == 'const':
                vals[m] = bool(e) if t == BOOL else e[0]
            elif k == 'var':
                vals[m] = env[e[1]]
            elif k == 'not':
                vals[m] = not vals[a[0]]
            elif k == 'and':
                vals[m] = vals[a[0]] and vals[a[1]]
            elif k == 'or':
                vals[m] = vals[a[0]] or vals[a[1]]
            elif k == 'xor':
                vals[m] = vals[a[0]] != vals[a[1]]
            elif k == 'ite':
                vals[m] = vals[a[1]] if vals[a[0]] else vals[a[2]]
            elif k == 'add':
                vals[m] = vals[a[0]] + vals[a[1]]
            elif k == 'sub':
                vals[m] = vals[a[0]] - vals[a[1]]
            elif k == 'eq':
                vals[m] = vals[a[0]] == vals[a[1]]
            elif k == 'lt':
                vals[m] = vals[a[0]] < vals[a[1]]
            elif k == 'le':
                vals[m] = vals[a[0]] <= vals[a[1]]
            elif k == 'exists':
                vals[m] = vals[a[0]]
            else:
                raise AssertionError(k)
        r = vals[n]
        return bool(r) if self.nodes[n][1] == BOOL else r

    def ev_ground(self, n, env):
        """Grounded evaluation: requires TOTAL env (all vars assigned); EXISTS = body value."""
        vs = self.vars_in(n)
        missing = [v for v in vs if v not in env]
        if missing:
            raise AssertionError(('partial env', missing[:5]))
        return self.ev_iter(n, env)

    def ev3_iter(self, n, env, doms):
        """Iterative 3-valued/interval evaluation for partial env.
        Returns (is_bool, value): True/False/None for bool; (lo,hi) for int."""
        vals = {}
        for m in self.topo([n]):
            k, t, a, e = self.nodes[m]
            if k == 'const':
                vals[m] = (True, bool(e)) if t == BOOL else (False, (e[0], e[0]))
            elif k == 'var':
                nm = e[1]
                if nm in env:
                    v = env[nm]
                    vals[m] = (True, bool(v)) if t == BOOL else (False, (v, v))
                elif t == BOOL:
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
                vals[m] = vals[a[0]]
            else:
                raise AssertionError(k)
        return vals[n]
