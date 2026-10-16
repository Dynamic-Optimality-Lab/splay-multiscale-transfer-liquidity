# S01_SCOPED_BINDERS.py — capture-safe, scope-aware binder normalization (additive frontend).
# Gives every existential/universal binder an unambiguous bound-variable identity BEFORE
# compilation. Method: privatize boundary-shared scope-carrying nodes. A var node whose
# name is bound by B but which is ALSO reachable from outside B's body (node sharing
# across the scope boundary) gets a privately-owned renamed copy for the inside path;
# purely-inside occurrences keep their nodes. After processing, every bound-named var
# node occurs only within its binder's body cone (validated), so one Z3 declaration per
# name is scope-correct. Free occurrences outside all binders keep original names and
# stay independently addressable. No global name-stripping as semantics.
# Supports 'exists' (authoritative DAG kind) and 'forall' (frozen frontend extension for
# Q4/Q5 regression formulas only; built via DAG._mk, no historical modification).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_TYPED_DAG import DAG, BOOL, prefix_rename


def forall(d, varnames, body):
    """Frontend-only universal binder (Q4/Q5). Same structural contract as EXISTS."""
    assert d.typ(body) == BOOL, body
    return d._mk('forall', BOOL, (body,), tuple(sorted(varnames)))


def outermost_binder(d, root, skip):
    """First exists/forall node in parents-before-children order, excluding processed ids."""
    for m in reversed(d.topo([root])):
        k, t, a, e = d.nodes[m]
        if k in ('exists', 'forall') and m not in skip:
            return m
    return None


def reachable_avoiding(d, root, avoid):
    """Nodes reachable from root via paths that never pass through node `avoid`."""
    seen = set()
    stack = [root]
    while stack:
        n = stack.pop()
        if n in seen or n == avoid:
            continue
        seen.add(n)
        _, _, a, _ = d.nodes[n]
        stack.extend(a)
    return seen


def privatize_binder_pass(d, root, m, tag, ctr):
    """One binder step. Returns (new_root, idmap, copies) where copies={fresh: orig}."""
    k, t, a, e = d.nodes[m]
    assert k in ('exists', 'forall'), m
    bound = set(e)
    body = a[0]
    S = set(d.topo([body]))
    R = reachable_avoiding(d, root, m)
    # hasB[n]: cone(n) contains a B-bound var occurrence (within S; S is cone-closed)
    hasB = {}
    for n in d.topo([body]):
        kk, tt, aa, ee = d.nodes[n]
        h = (kk == 'var' and ee[1] in bound)
        if not h:
            for x in aa:
                if hasB.get(x, False):
                    h = True
                    break
        hasB[n] = h
    C = set(n for n in S if hasB.get(n, False) and n in R)
    # Uniformity: one var node per name, so per (binder, name) either ALL interior
    # occurrences are boundary-shared (node in C -> REPLACE in record) or none (KEEP).
    # REPLACE-not-add keeps this a pure alpha-renaming (no weakening, ever).
    renamed_names = set()
    for n in C:
        kk, tt, aa, ee = d.nodes[n]
        if kk == 'var' and ee[1] in bound:
            renamed_names.add(ee[1])
    fresh = {}
    for v in sorted(renamed_names):
        ctr[0] += 1
        fresh[v] = '%s#%s%d' % (v, tag, ctr[0])
    copies = {fresh[v]: v for v in fresh}
    new_extra = tuple(sorted(fresh.get(x, x) for x in e))
    # ancestors of m within the cone (must be relinked to the rebuilt binder)
    children_of = {}
    cone = d.topo([root])
    for n in cone:
        _, _, aa, _ = d.nodes[n]
        for x in aa:
            children_of.setdefault(x, []).append(n)
    Anc = set()
    stack = [m]
    inset = set(cone)
    while stack:
        n = stack.pop()
        if n in Anc or n not in inset:
            continue
        Anc.add(n)
        stack.extend(children_of.get(n, []))
    newid = {}
    for n in cone:
        if n not in S and n not in Anc:
            newid[n] = n
            continue
        kk, tt, aa, ee = d.nodes[n]
        if kk == 'var':
            if n in C and ee[1] in bound:
                nv = fresh[ee[1]]
                if tt == BOOL:
                    r = d.var_bool(nv)
                else:
                    w = ee[2]
                    sg = ee[3] if len(ee) > 3 else False
                    r = d.var_int(nv, w, sg)
                newid[n] = r
            else:
                newid[n] = n
            continue
        if not aa:
            newid[n] = n
            continue
        na = tuple(newid[x] for x in aa)
        if n == m:
            ne = new_extra
        elif kk in ('exists', 'forall') and n in S:
            ne = tuple(fresh.get(x, x) for x in ee)
        else:
            ne = ee
        if na != aa or (kk in ('exists', 'forall') and ne != ee):
            r = d._mk(kk, tt, na, ne)
            newid[n] = r
        else:
            newid[n] = n
    return newid[root], newid, copies


def cone_subst(d, root, mp):
    """Raw whole-cone rename (no scope gating). Only for alpha-equivalence test scaffolding."""
    newid = {}
    for n in d.topo([root]):
        kk, tt, aa, ee = d.nodes[n]
        if kk == 'var' and ee[1] in mp:
            new = mp[ee[1]]
            if tt == BOOL:
                r = d.var_bool(new)
            else:
                w = ee[2]
                sg = ee[3] if len(ee) > 3 else False
                r = d.var_int(new, w, sg)
            newid[n] = r
            continue
        if not aa:
            newid[n] = n
            continue
        na = tuple(newid[x] for x in aa)
        if kk in ('exists', 'forall'):
            ne = tuple(prefix_rename(x, mp) for x in ee)
            r = d._mk(kk, tt, na, ne)
        else:
            r = d._mk(kk, tt, na, ee)
        newid[n] = r
    return newid[root]


def normalize(d, root, tag='q'):
    """Alpha-normalize all binders in cone(root). Returns (new_root, info).
    info: binders=[{kind, bound:[current...], orig:[...]}], copies={fresh: orig},
    growth=new nodes added. Pure alpha-renaming: no weakening, ever."""
    cur = root
    skip = set()
    binders = []
    copies = {}
    ctr = [0]
    n0 = d.count()

    while True:
        m = outermost_binder(d, cur, skip)
        if m is None:
            break
        k, t, a, e = d.nodes[m]
        cur, idmap, cps = privatize_binder_pass(d, cur, m, tag, ctr)
        copies.update(cps)
        skip = set(idmap.get(s, s) for s in skip)
        nm = idmap[m]
        skip.add(nm)
        _, _, _, ne = d.nodes[nm]
        binders.append({'kind': k, 'bound': sorted(ne), 'orig': sorted(e)})
    info = {'binders': binders, 'copies': copies, 'count': len(binders),
            'growth': d.count() - n0}
    _validate(d, cur, info)
    return cur, info


def _validate(d, root, info):
    """Structural scope validation (FAIL CLOSED on violation)."""
    seen = set()
    for b in info['binders']:
        for v in b['bound']:
            assert v not in seen, ('shared bound name', v)
            seen.add(v)
    body_of = {}
    for m in d.topo([root]):
        k, t, a, e = d.nodes[m]
        if k in ('exists', 'forall'):
            body_of[m] = set(d.topo([a[0]]))
    var_nodes = [(n, d.nodes[n]) for n in d.topo([root]) if d.nodes[n][0] == 'var']
    for m, bodies in body_of.items():
        mine = set(d.nodes[m][3])
        for n, (kk, tt, aa, ee) in var_nodes:
            if ee[1] in mine and n not in bodies:
                raise AssertionError(('bound name escapes binder', ee[1]))
    return True


def bound_names(d, root):
    out = set()
    for m in d.topo([root]):
        k, t, a, e = d.nodes[m]
        if k in ('exists', 'forall'):
            out.update(e)
    return out


def free_names(d, root):
    return d.vars_in(root) - bound_names(d, root)
