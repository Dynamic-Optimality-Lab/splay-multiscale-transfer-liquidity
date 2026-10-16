# S01_INDEPENDENT_ORACLE.py — scope-correct finite-domain reference evaluator.
# Lexical binders (innermost wins); EXISTS/FORALL decided by bounded enumeration.
# Out-of-scope (domain product above cap, or unconfirmed witness) returns None — NEVER
# a guessed truth value. `witness_check` confirms claimed ground witnesses (True/None).
import sys, itertools
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_TYPED_DAG import BOOL


def _dom(d, nid):
    k, t, a, e = d.nodes[nid]
    if t == BOOL:
        return (0, 1)
    w = e[2]
    sg = e[3] if len(e) > 3 else False
    return (-(1 << (w - 1)), (1 << (w - 1)) - 1) if sg else (0, (1 << w) - 1)


def scoped_truth(d, n, env, scope=None, cap=65536):
    """('b', True/False/None) or ('i', (lo,hi)). env: free assignments; scope: active binders."""
    scope = dict(scope) if scope else {}
    vals = {}

    def supp(m):
        """Bound-var support needed below m (for enum budgeting): names bound in cone."""
        out = set()
        for x in d.topo([m]):
            kk, tt, aa, ee = d.nodes[x]
            if kk in ('exists', 'forall'):
                out.update(ee)
        return out

    for m in d.topo([n]):
        k, t, a, e = d.nodes[m]
        if k == 'const':
            vals[m] = ('b', bool(e)) if t == BOOL else ('i', (e[0], e[0]))
        elif k == 'var':
            nm = e[1]
            if nm in scope:
                v = scope[nm]
                vals[m] = ('b', bool(v)) if t == BOOL else ('i', (v, v))
            elif nm in env:
                v = env[nm]
                vals[m] = ('b', bool(v)) if t == BOOL else ('i', (v, v))
            elif t == BOOL:
                vals[m] = ('b', None)
            else:
                vals[m] = ('i', tuple(_dom(d, m)))
        elif k == 'not':
            _, v = vals[a[0]]
            vals[m] = ('b', None if v is None else (not v))
        elif k == 'and':
            _, x = vals[a[0]]
            _, y = vals[a[1]]
            vals[m] = ('b', False if (x is False or y is False) else (True if (x is True and y is True) else None))
        elif k == 'or':
            _, x = vals[a[0]]
            _, y = vals[a[1]]
            vals[m] = ('b', True if (x is True or y is True) else (False if (x is False and y is False) else None))
        elif k == 'xor':
            _, x = vals[a[0]]
            _, y = vals[a[1]]
            vals[m] = ('b', None if x is None or y is None else (x != y))
        elif k == 'ite':
            _, c = vals[a[0]]
            ta, va = vals[a[1]]
            tb, vb = vals[a[2]]
            if c is True:
                vals[m] = (ta, va)
            elif c is False:
                vals[m] = (tb, vb)
            elif ta and tb:
                vals[m] = ('b', True if (va is True and vb is True) else (False if (va is False and vb is False) else None))
            else:
                (l1, h1), (l2, h2) = va, vb
                vals[m] = ('i', (min(l1, l2), max(h1, h2)))
        elif k in ('add', 'sub'):
            _, (l1, h1) = vals[a[0]]
            _, (l2, h2) = vals[a[1]]
            vals[m] = ('i', (l1 + l2, h1 + h2)) if k == 'add' else ('i', (l1 - h2, h1 - l2))
        elif k == 'eq':
            ta, va = vals[a[0]]
            tb, vb = vals[a[1]]
            if ta and tb:
                vals[m] = ('b', None if va is None or vb is None else (va == vb))
            else:
                (l1, h1), (l2, h2) = va, vb
                if h1 < l2 or h2 < l1:
                    vals[m] = ('b', False)
                elif l1 == h1 == l2 == h2:
                    vals[m] = ('b', True)
                else:
                    vals[m] = ('b', None)
        elif k in ('lt', 'le'):
            _, (l1, h1) = vals[a[0]]
            _, (l2, h2) = vals[a[1]]
            if k == 'lt':
                r = True if h1 < l2 else (False if l1 >= h2 else None)
            else:
                r = True if h1 <= l2 else (False if l1 > h2 else None)
            vals[m] = ('b', r)
        elif k in ('exists', 'forall'):
            body = a[0]
            # fast path: env's own values for the bound names (claimed witness)
            wcombo = {v: env[v] for v in e if v in env}
            if len(wcombo) == len(e):
                sub0 = dict(scope)
                sub0.update(wcombo)
                r0 = scoped_truth(d, body, env, sub0, cap)
                if r0[0] == 'b':
                    if k == 'exists' and r0[1] is True:
                        vals[m] = ('b', True)
                        continue
                    if k == 'forall' and r0[1] is False:
                        vals[m] = ('b', False)
                        continue
            doms = []
            for v in e:
                nid = d.vars.get(v)
                if nid is None:
                    assert v not in d.vars_in(body), ('bound name occurs but undeclared', v)
                    doms.append([0, 1])  # vacuous: any nonempty domain preserves truth
                    continue
                lo, hi = _dom(d, nid)
                doms.append(list(range(lo, hi + 1)))
            total = 1
            for dd in doms:
                total *= len(dd)
                if total > cap:
                    break
            if total > cap:
                vals[m] = ('b', None)
                continue
            decided = None
            complete = True  # True iff every combo decided against the quantifier
            for combo in itertools.product(*doms):
                sub = dict(scope)
                sub.update(dict(zip(e, combo)))
                r2 = scoped_truth(d, body, env, sub, cap)
                bv = r2[1] if r2[0] == 'b' else None
                if k == 'exists' and bv is True:
                    decided = True
                    break
                if k == 'forall' and bv is False:
                    decided = False
                    break
                if bv is None:
                    complete = False
            if decided is True:
                vals[m] = ('b', True)
            elif decided is False:
                vals[m] = ('b', False)
            elif complete:
                vals[m] = ('b', False) if k == 'exists' else ('b', True)
            else:
                vals[m] = ('b', None)
        else:
            raise AssertionError(('oracle: unsupported kind', k))
    return vals[n]


def witness_check(d, root, env):
    """Confirm a claimed ground witness. True = confirmed; None = NOT confirmed (never False)."""
    try:
        missing = [v for v in d.vars_in(root) if v not in env]
        if missing:
            return None
        r = scoped_truth(d, root, env, {}, cap=1 << 60)
    except AssertionError:
        return None
    if r[0] == 'b' and r[1] is True:
        return True
    return None
