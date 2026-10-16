# S01_DAG_COMPILER.py — structural DAG->Z3 compiler (cache: node id -> Z3 expr).
# Semantics: Bool->z3.Bool; Int->z3.Int (unbounded math ints: EXACT, no wraparound by
# construction). Width/signedness metadata becomes explicit finite-domain bounds
# conjoined at the top (equivalent to the historical Solver's width domains).
# Quantifiers compile to native z3.Exists/z3.Forall over normalized (unique) binders.
# Iterative topo traversal (no recursion on graph depth). No silent fallbacks: unknown
# node kinds raise.
import sys, time
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
import z3
from PC_TYPED_DAG import BOOL, INT


def width_domain(d, nid):
    """(lo, hi) finite domain for a var node, mirroring Solver.domain exactly."""
    k, t, a, e = d.nodes[nid]
    assert k == 'var', nid
    if t == BOOL:
        return (0, 1)
    name, w = e[1], e[2]
    signed = e[3] if len(e) > 3 else False
    if signed:
        return (-(1 << (w - 1)), (1 << (w - 1)) - 1)
    return (0, (1 << w) - 1)


def compile_root(d, root, seed_tag='s01'):
    """Returns dict(vars, bounds, body, decls, width_audit, stats).
    decls: name -> z3 const (one per name; normalized binders are globally unique).
    bounds: [lo<=v, v<=hi] for every INT var in cone (Bool needs none)."""
    t0 = time.time()
    decls = {}
    widths = []
    exprs = {}
    n_exists = n_forall = 0
    max_qdepth = [0]

    def decl(name, is_bool):
        if name not in decls:
            decls[name] = z3.Bool(name) if is_bool else z3.Int(name)
        return decls[name]

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
        elif k == 'le':
            exprs[m] = exprs[a[0]] <= exprs[a[1]]
        elif k in ('add', 'sub'):
            exprs[m] = exprs[a[0]] + exprs[a[1]] if k == 'add' else exprs[a[0]] - exprs[a[1]]
        elif k in ('exists', 'forall'):
            blist = []
            for v in e:
                nid = d.vars.get(v)
                if nid is None:
                    # undeclared bound name: must be vacuous (no occurrence possible
                    # without a var node); Bool default is sound (nonempty domain,
                    # formula independent of var => quantifier is identity).
                    assert v not in d.vars_in(a[0]), ('bound name occurs but undeclared', v)
                    blist.append(decl(v, True))
                else:
                    blist.append(decl(v, d.nodes[nid][1] == BOOL))
            bound = blist
            if k == 'exists':
                exprs[m] = z3.Exists(bound, exprs[a[0]])
                n_exists += 1
            else:
                exprs[m] = z3.ForAll(bound, exprs[a[0]])
                n_forall += 1
        else:
            raise AssertionError(('unsupported node kind', k, m))
    # quantifier nesting depth (iterative over cone)
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
             'translate_s': round(time.time() - t0, 2)}
    return {'vars': decls, 'bounds': bounds, 'body': exprs[root], 'width_audit': widths, 'stats': stats}
