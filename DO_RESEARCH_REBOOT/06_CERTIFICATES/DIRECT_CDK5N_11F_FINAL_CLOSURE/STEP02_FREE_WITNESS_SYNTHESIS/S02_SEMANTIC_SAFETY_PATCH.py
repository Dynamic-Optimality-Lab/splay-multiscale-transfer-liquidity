# S02_SEMANTIC_SAFETY_PATCH.py — additive Gate-B repairs (NO Step-01/historical modification).
# B1: finite-domain bounds INSIDE quantified scopes. Step-01 compile_root asserts bounds
#     only at top level, leaving bound occurrences effectively unbounded (confirmed:
#     EXISTS x in {0,1} (x=3) wrongly SAT; FORALL x in {0,1} (x<=1) wrongly UNSAT).
#     Repair: compile Exists(B,F) as Exists(B, AND(D(B),F)) and Forall(B,F) as
#     Forall(B, IMPLIES(AND(D(B)),F)) with per-binder domain predicates. Pure
#     restriction-to-declared-domain: exact finite-domain semantics.
# B2: session-aware Tier-1. Step-01 Tier-1 sees per-call pins only; session pins live
#     in Z3. Verdicts are session-independent and sound, but Tier-1 SAT model
#     completion can contradict active session pins. Repair: track the session pin
#     stack per handle; Tier-1 combines (call wins on conflict only if... NO: any
#     same-var conflict between session and call pins is an immediate UNSAT), and
#     model completion prefers session values, then call pins, then domain-lo.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
import z3
from PC_TYPED_DAG import BOOL
from S01_DAG_COMPILER import width_domain


def _bvars(d, extra):
    """(decls-needed, domain-predicates) for a binder's bound names."""
    info = []
    for v in extra:
        nid = d.vars.get(v)
        if nid is None:
            info.append((v, True, None))
        else:
            info.append((v, d.nodes[nid][1] == BOOL, nid))
    return info


def compile_root_scoped(d, root):
    """Scoped-bounds variant of compile_root (same contract + in-scope domains)."""
    import time
    from S01_DAG_COMPILER import compile_root as _orig
    t0 = time.time()
    decls = {}
    widths = []

    def decl(name, is_bool):
        if name not in decls:
            decls[name] = z3.Bool(name) if is_bool else z3.Int(name)
        return decls[name]

    exprs = {}
    n_exists = n_forall = 0
    for m in d.topo([root]):
        k, t, a, e = d.nodes[m]
        if k == 'const':
            exprs[m] = z3.BoolVal(bool(e)) if t == BOOL else z3.IntVal(e[0])
        elif k == 'var':
            nm = e[1]
            isb = (t == BOOL)
            exprs[m] = decl(nm, isb)
            if not isb:
                lo, hi = width_domain(d, m)
                widths.append({'name': nm, 'width': e[2], 'signed': bool(e[3]) if len(e) > 3 else False, 'lo': lo, 'hi': hi})
        elif k == 'not':
            exprs[m] = z3.Not(exprs[a[0]])
        elif k == 'and':
            exprs[m] = z3.And(exprs[a[0]], exprs[a[1]])
        elif k == 'or':
            exprs[m] = z3.Or(exprs[a[0]], exprs[a[1]])
        elif k == 'xor':
            exprs[m] = z3.Xor(exprs[a[0]], exprs[a[1]])
        elif k == 'ite':
            exprs[m] = z3.If(exprs[a[0]], exprs[a[1]], exprs[a[2]])
        elif k == 'eq':
            exprs[m] = exprs[a[0]] == exprs[a[1]]
        elif k == 'lt':
            exprs[m] = exprs[a[0]] < exprs[a[1]]
        elif k in ('add', 'sub'):
            exprs[m] = exprs[a[0]] + exprs[a[1]] if k == 'add' else exprs[a[0]] - exprs[a[1]]
        elif k == 'le':
            exprs[m] = exprs[a[0]] <= exprs[a[1]]
        elif k in ('exists', 'forall'):
            blist, dpreds = [], []
            for (v, isb, nid) in _bvars(d, e):
                z = decl(v, isb)
                blist.append(z)
                if not isb and nid is not None:
                    lo, hi = width_domain(d, nid)
                    dpreds.append(z3.And(lo <= z, z <= hi))
            if k == 'exists':
                exprs[m] = z3.Exists(blist, z3.And(*(dpreds + [exprs[a[0]]])))
                n_exists += 1
            else:
                exprs[m] = z3.ForAll(blist, z3.Implies(z3.And(*dpreds) if dpreds else z3.BoolVal(True), exprs[a[0]]))
                n_forall += 1
        else:
            raise AssertionError(('unsupported node kind', k, m))
    depth = {}
    for m in d.topo([root]):
        k, t, a, e = d.nodes[m]
        if k in ('exists', 'forall'):
            depth[m] = depth.get(a[0], 0) + 1
        elif a:
            depth[m] = max([depth.get(x, 0) for x in a] or [0])
        else:
            depth[m] = 0
    bounds = []
    seen_b = set()
    for wrec in widths:
        v = wrec['name']
        if v in seen_b:
            continue
        seen_b.add(v)
        z = decls[v]
        bounds.append(z3.And(wrec['lo'] <= z, z <= wrec['hi']))
    stats = {'dag_nodes': len(d.topo([root])), 'decls': len(decls),
             'int_bounds': len(bounds), 'exists': n_exists, 'forall': n_forall,
             'qdepth': max(depth.values()) if depth else 0,
             'translate_s': round(time.time() - t0, 2), 'scoped_bounds': True}
    return {'vars': decls, 'bounds': bounds, 'body': exprs[root], 'width_audit': widths, 'stats': stats}


def install_scoped_compile(ps):
    """Point a ProductionSolver instance at the scoped compiler (instance attribute;
    Step-01 module untouched)."""
    import types
    from S01_SCOPED_BINDERS import normalize, bound_names, free_names
    import z3 as _z3

    def compile_scoped(self, root, tag='root'):
        from PC_TYPED_DAG import BOOL as _B
        if self.d.typ(root) != _B:
            raise AssertionError(('compile requires a Bool root', root))
        nroot, ninfo = normalize(self.d, root)
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

    ps.compile = types.MethodType(compile_scoped, ps)
    # session-aware Tier-1: combine session pins (stack) with call pins
    _orig_tier1 = ps.tier1

    def tier1_session(self, handle, env):
        sess = {}
        for frame in handle.get('_session_stack', []):
            for kk, vv in frame.items():
                if kk in sess and sess[kk] != vv:
                    return {'status': 'UNSAT', 'reason': 'session-contradiction', 'model': None, 'cpu_s': 0.0}
                sess[kk] = vv
        for kk, vv in env.items():
            if kk in sess and sess[kk] != vv:
                return {'status': 'UNSAT', 'reason': 'session-call-contradiction', 'model': None, 'cpu_s': 0.0}
        combined = dict(sess)
        combined.update(env)
        r = _orig_tier1(handle, combined)
        if r is not None and r['status'] == 'SAT' and isinstance(r.get('model'), dict):
            # completion prefers session values (already in combined); nothing more needed
            pass
        return r

    ps.tier1 = types.MethodType(tier1_session, ps)
    return ps
