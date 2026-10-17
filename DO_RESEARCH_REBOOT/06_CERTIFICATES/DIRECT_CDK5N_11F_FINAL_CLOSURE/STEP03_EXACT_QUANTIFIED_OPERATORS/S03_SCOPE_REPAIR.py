# S03_SCOPE_REPAIR.py — corrected scope normalization (additive; Step-01/02 untouched).
# Step-01 privatize_binder_pass has a soundness bug on shared NON-LEAF scope-carrying
# nodes: newid is keyed by node id, so when a shared node is copied for inside use,
# outside occurrences (reached through rebuilt Anc ancestors) wrongly adopt the copy,
# dropping the outer free variable (observed: nested Pre(Post) lost outer Os_v).
# Fix: inside/outside edge distinction. Nodes in S use inside-versions; Anc ancestors
# use inside-versions ONLY for children on the path to m (children in Anc) and keep
# ORIGINAL ids otherwise; nodes outside S∪Anc stay identical. Nested-in-S binder
# records rename with the same fresh map (their bodies use inside-versions);
# Anc binder records (previously processed outer binders) are never touched.
# Pure alpha-renaming preserved (REPLACE-not-add, per-name uniform).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
from PC_TYPED_DAG import DAG, BOOL
from S01_SCOPED_BINDERS import outermost_binder, reachable_avoiding


def privatize_binder_pass_fixed(d, root, m, tag, ctr):
    k, t, a, e = d.nodes[m]
    assert k in ('exists', 'forall'), m
    bound = set(e)
    body = a[0]
    S = set(d.topo([body]))
    R = reachable_avoiding(d, root, m)
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
    newid_in = {}
    for n in cone:
        if n not in S and n not in Anc:
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
                newid_in[n] = r
            else:
                newid_in[n] = n
            continue
        if not aa:
            newid_in[n] = n
            continue
        if n in S:
            na = tuple(newid_in[x] for x in aa)
        elif n == m:
            # the binder itself: its body is inside by definition (use inside-versions)
            na = tuple(newid_in.get(x, x) for x in aa)
        else:  # n in Anc (outside S): inside-version only along the path to m
            na = tuple(newid_in[x] if x in Anc else x for x in aa)
        if n == m:
            ne = new_extra
        elif kk in ('exists', 'forall') and n in S:
            ne = tuple(fresh.get(x, x) for x in ee)
        else:
            ne = ee
        if na != aa or (kk in ('exists', 'forall') and ne != ee):
            newid_in[n] = d._mk(kk, tt, na, ne)
        else:
            newid_in[n] = n
    # idmap for skip-remapping: every cone node maps to its inside-version if rebuilt
    idmap = {n: newid_in.get(n, n) for n in cone}
    return idmap[root], idmap, copies


def normalize_fixed(d, root, tag='q'):
    """Alpha-normalize with the corrected pass. Same contract as S01 normalize."""
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
        cur, idmap, cps = privatize_binder_pass_fixed(d, cur, m, tag, ctr)
        copies.update(cps)
        skip = set(idmap.get(s, s) for s in skip)
        nm = idmap[m]
        skip.add(nm)
        _, _, _, ne = d.nodes[nm]
        binders.append({'kind': k, 'bound': sorted(ne), 'orig': sorted(e)})
    info = {'binders': binders, 'copies': copies, 'count': len(binders),
            'growth': d.count() - n0, 'fixed_pass': True}
    _validate(d, cur, info)
    return cur, info


def _validate(d, root, info):
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


def install_fixed_compile(ps):
    """Point a ProductionSolver at normalize_fixed + scoped compiler (additive)."""
    import types
    import z3 as _z3
    from S02_SEMANTIC_SAFETY_PATCH import compile_root_scoped

    def compile_fixed(self, root, tag='root'):
        from PC_TYPED_DAG import BOOL as _B
        if self.d.typ(root) != _B:
            raise AssertionError(('compile requires a Bool root', root))
        nroot, ninfo = normalize_fixed(self.d, root)
        comp = compile_root_scoped(self.d, nroot)
        s = _z3.Solver()
        s.set('random_seed', self.seed)
        if self.timeout_ms:
            s.set('timeout', self.timeout_ms)
        for b in comp['bounds']:
            s.add(b)
        s.add(comp['body'])
        h = {'solver': s, 'comp': comp, 'nroot': nroot, 'ninfo': ninfo,
             'free': sorted(free_names(self.d, nroot)),
             'bound': sorted(bound_names(self.d, nroot)), 'tag': tag,
             'compile_cpu_s': 0.0, '_session_stack': []}
        self.handles[tag] = h
        return h

    ps.compile = types.MethodType(compile_fixed, ps)
    return ps
