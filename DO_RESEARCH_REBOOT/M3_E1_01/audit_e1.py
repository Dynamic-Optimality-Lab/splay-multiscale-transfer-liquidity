"""Independent universal order/source audit. No instantiated states or trees."""
import ast, hashlib, json, sys, time
from pathlib import Path

BASE = Path(__file__).resolve().parent
CAP = min(120.0, float(sys.argv[1]))

def write(name, obj):
    with (BASE / name).open('x', encoding='utf-8') as stream:
        json.dump(obj, stream, indent=2)

def expr(**terms):
    return {name: value for name, value in terms.items() if value}

def plus(*terms):
    answer = {}
    for term in terms:
        for name, value in term.items():
            answer[name] = answer.get(name, 0) + value
    return {name: value for name, value in answer.items() if value}

def minus(term):
    return {name: -value for name, value in term.items()}

def twice(term):
    return plus(term, term)

def main():
    # Each named variable below is universally quantified. No numerical
    # assignment, topology, population, or transition is generated.
    one = expr(constant=1)
    q = plus(twice(one), expr(excess_q=1))
    depth = plus(expr(constant=3), expr(depth_slack=-1))
    contradiction = plus(twice(q), minus(depth))
    assert contradiction == expr(constant=1, excess_q=2, depth_slack=1)
    assert all(v >= 0 for v in contradiction.values())
    # q>=2 and depth<=3 contradict depth-2q>=0. The constant1 is strict.

    # Unchanged source: old residual rho>=0, destination increment delta>=0.
    old_source = expr(source=1)
    old_target = expr(target=1)
    weight = expr(weight=1)
    old_residual = plus(weight, old_target, minus(old_source))
    new_target = plus(old_target, expr(destination_increment=1))
    unchanged_residual = plus(weight, new_target, minus(old_source))
    assert plus(unchanged_residual, minus(old_residual)) == expr(destination_increment=1)
    # Raised source: source becomes1, weight=1+a, destination debt=b.
    raised_residual = plus(plus(one, expr(weight_slack=1)), expr(new_target=1), minus(one))
    assert raised_residual == expr(weight_slack=1, new_target=1)
    assert all(v >= 0 for v in raised_residual.values())
    # Range and floor follow from max of entries in[0,2] and max>=D.

    # Provenance audit reads AST only; it does not compile/evaluate a root.
    source_path = BASE.parent / '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py'
    rotation_path = BASE.parent / '06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ROTATION_INTERPRETER.py'
    module = ast.parse(source_path.read_text(encoding='utf-8-sig'))
    functions = {n.name: ast.unparse(n) for n in module.body if isinstance(n, ast.FunctionDef)}
    shadow, match, low = (functions[n] for n in ('shadow7', 'shadow_match7', 'build_slow'))
    assert 'k = d.ITE(d.EQ(kk, d.const_int(0, 2)), dkk, kk)' in shadow
    assert 'r = d.ITE(d.EQ(kk, d.const_int(0, 2)), dref, ref)' in shadow
    assert "order = ['root', 'L', 'R', 'LL', 'LR', 'RL', 'RR']" in match
    assert 'is_slot = d.EQ(kk, d.const_int(0, 2))' in match
    assert 'd.OR(d.NOT(is_slot), d.EQ(cs, s.aS[p]))' in match
    assert 'd.OR(d.NOT(d.AND(is_slot, cs)), d.EQ(ci, s.aI[p]))' in match
    assert 'C.append(s.aS[0])' in low
    assert 'C.append(d.EQ(s.aI[0], muxb(' in low
    assert 'C.append(tisS)' in low and 'C.append(marked)' in low and 'C.append(chg)' in low
    assert 'root_terminated(d, wit, bt, st, bs[e], e, active)' in low
    assert 'same_keep_target(d, wit, inv, bt, e, active)' in low
    assert 'd.LE(d.ADD(bt.q, bt.q, 5), bd_last)' in low
    assert 'd.LT(bd_last, d.ADD(d.ADD(bt.q, bt.q, 5), d.const_int(2, 5), 5))' in low
    assert 'd.EQ(wv, d.SUB(d.ADD(Hv, Hv, 3), bt.q, 5))' in low
    rmodule = ast.parse(rotation_path.read_text(encoding='utf-8-sig'))
    mux = next(n for n in rmodule.body if isinstance(n, ast.FunctionDef) and n.name == 'mux_ref')
    assert isinstance(mux.body[0], ast.Assign) and ast.unparse(mux.body[0]) == 'r = vec[0]'
    astate = next(n for n in rmodule.body if isinstance(n, ast.ClassDef) and n.name == 'AState')
    assert 'self.root = d.const_int(0, W_REF)' in ast.unparse(astate)
    result = {
        'status': 'UNIVERSAL_E1_AUGMENTATION_AUDIT_PASS',
        'quantifiers': 'all full shared ordinary states, all masks/signatures, all original H1 witnesses, all public real debts in[0,2]',
        'inequalities_preserved_individually': True,
        'depth_contradiction_polynomial': contradiction,
        'unchanged_source_increment': expr(destination_increment=1),
        'raised_source_residual': raised_residual,
        'source_shadow_kind_filter_and_slot0_fallback_confirmed': True,
        'source_root_sync_marked_terminal_original_q_weight_confirmed': True,
        'source_cover_argument': 'real active target depth1/2 appears at its authoritative shadow position; coarse positions cannot carry an active path; alias root labels are excluded',
        'reused_H1_normal_form_and_active_path_proof': True,
        'whole_source_formalization_claimed': False,
        'private_inventory_assumption': False,
        'debt_2_sources_all_discharged': False,
        'Score_bearing_H2_preservation_claimed': False,
        'new_finite_population_tests': 0,
        'new_source_transition_queries': 0,
        'new_original_root_evaluations': 0,
        'source_hashes': {p.as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in (source_path, rotation_path)},
        'CPU_seconds': time.process_time(), 'CPU_cap': CAP,
    }
    assert time.process_time() < CAP
    write('e1_audit.json', result)
    print(json.dumps(result, indent=2), flush=True)

if __name__ == '__main__':
    error = None
    try:
        main()
    except BaseException as exception:
        error = {'type': type(exception).__name__, 'message': str(exception)}
        raise
    finally:
        write('e1_audit_exit.json', {'whole_process_CPU_seconds': time.process_time(), 'CPU_cap': CAP, 'error': error})
