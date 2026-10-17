# S03_RELATION_SCOPE_COMPILER.py — exact relational projection (Gates B/G06-G09).
# project_edge(d, root, keep_prefixes): binds EVERYTHING outside the declared
# sort interface in a top-level EXISTS (membership-preserving: membership in
# EXISTS-hidden(F) iff witness exists, which is the edge definition). Empty hidden
# set returns the root unchanged (no vacuous binder). Free-var audit verifies
# FreeVars(result) ⊆ interface mechanically. Normalization (Step-01/02, additive)
# later gives each binder unique ownership (privatization), so independently
# projected edges never share witnesses unless explicitly correlated.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
from PC_TYPED_DAG import DAG, BOOL
from S01_SCOPED_BINDERS import bound_names


def interface_vars(d, root, keep_prefixes):
    keep = set()
    for v in d.vars_in(root):
        for p in keep_prefixes:
            if v.startswith(p):
                keep.add(v)
                break
    return keep


def project_edge(d, root, keep_prefixes):
    """Returns (projected_root, audit). Audit proves the free-var condition."""
    assert d.typ(root) == BOOL, root
    keep = interface_vars(d, root, keep_prefixes)
    # Names already bound inside are closed already; bind only the rest (avoids
    # vacuous re-binding that would merely force privatization copies).
    hidden = sorted(set(d.vars_in(root)) - keep - set(bound_names(d, root)))
    if not hidden:
        proot = root
    else:
        proot = d.EXISTS(tuple(hidden), root)
    # mechanical audit (recomputed, not trusted from construction): every free
    # (non-bound) variable of the projection must lie in the declared interface.
    free = set(d.vars_in(proot)) - set(bound_names(d, proot))
    outside = sorted(free - keep)
    assert not outside, ('free witness escapes projection', outside)
    return proot, {'interface': sorted(keep), 'bound': hidden, 'free': sorted(free)}
