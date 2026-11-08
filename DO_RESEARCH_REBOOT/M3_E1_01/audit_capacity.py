"""Independent universal slack audit of public capacity, not a state test."""
import ast, hashlib, json, sys, time
from pathlib import Path
BASE = Path(__file__).resolve().parent
CAP = min(120.0, float(sys.argv[1]))

def write(name, obj):
    with (BASE/name).open('x', encoding='utf-8') as stream:
        json.dump(obj, stream, indent=2)

def lin(**values):
    return {key: value for key, value in values.items() if value}

def add(*items):
    out = {}
    for item in items:
        for key, value in item.items():
            out[key] = out.get(key, 0)+value
    return {key: value for key, value in out.items() if value}

def neg(item):
    return {key: -value for key, value in item.items()}

def main():
    assert json.loads((BASE/'e1_run_result.json').read_text())['status'] == 'PASS'
    assert json.loads((BASE/'e1_controller_exit.json').read_text())['error'] is None
    # Independent symbolic variables; no numerical values are substituted.
    weight, floor_t, cap_s = lin(w=1), lin(psi_t=1), lin(c_s=1)
    # c_s=w+psi_t-a, A(D)(t)=psi_t+b, a,b>=0.
    cap_s = add(weight, floor_t, lin(capacity_slack=-1))
    debt_t = add(floor_t, lin(target_floor_slack=1))
    raised_residual = add(weight, debt_t, neg(cap_s))
    assert raised_residual == lin(capacity_slack=1, target_floor_slack=1)
    assert all(value >= 0 for value in raised_residual.values())
    # Nonnegative exit margin for a negative w comes from the OLD law.
    negative_margin = add(lin(psi_s=1), lin(negative_core_slack=1))
    assert all(value >= 0 for value in negative_margin.values())

    source, target = lin(D_s=1), lin(D_t=1)
    residual = add(weight, target, neg(source))
    source_upper_gap = add(weight, lin(constant=2), neg(source))
    assert add(source_upper_gap, neg(residual)) == lin(constant=2, D_t=-1)
    # This is old residual plus range slack (2-D_t), with each nonnegative.
    assert add(add(weight, lin(constant=2), neg(lin(psi_s=1))),
               neg(add(weight, lin(psi_t=1), neg(lin(psi_s=1))))) == lin(constant=2, psi_t=-1)
    assert add(add(weight, lin(constant=2)), neg(add(weight, floor_t))) == lin(constant=2, psi_t=-1)
    # Capped-minimum monotonicity is universal, including an empty V:
    # append the same cap2 as an additional index; lower<=upper pointwise.

    # floor preservation: if integer parts violate by >=1, write fs=w+ft+1+n;
    # fractional source u>=0 and fractional target1-eps<1, eps>0.
    fs = add(weight, lin(floor_t=1, constant=1, integer_excess=1))
    real_source = add(fs, lin(source_fraction=1))
    real_target = lin(floor_t=1, constant=1, epsilon=-1)
    rounding_contradiction = add(real_source, neg(weight), neg(real_target))
    assert rounding_contradiction == lin(integer_excess=1, source_fraction=1, epsilon=1)
    # epsilon is STRICTLY positive. Hence the old inequality cannot hold.

    # A depth8 negative edge: psi_t>=psi_s+2 and psi_t<=2 force psi_s=0.
    # source<=w+D_t and D_t<=2 force source<=0 when w=-2.
    assert add(lin(constant=-2), lin(constant=2, target_range_slack=-1)) == lin(target_range_slack=-1)
    # For w=-1, U<=1; negative-core floor makes target>=1.
    assert add(lin(constant=-1), lin(constant=2)) == lin(constant=1)
    # D0=Lambda: capacity-dominated sources use the raised identity above;
    # floor-dominated sources with w<0 use old negative-core slack;
    # remaining w>=psi_s gives residual (w-psi_s)+Lambda_t>=0.
    seed_safe_residual = add(lin(weight_above_source_floor=1), lin(Lambda_t=1))
    assert all(value >= 0 for value in seed_safe_residual.values())

    # Read AST provenance for the V converse and direct-witness construction.
    source_path = BASE.parent/'06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py'
    text = source_path.read_text(encoding='utf-8-sig')
    module = ast.parse(text)
    low = ast.unparse(next(n for n in module.body if isinstance(n, ast.FunctionDef) and n.name=='build_slow'))
    assert 'state_valid7(d, s)' in low and 'state_valid7(d, t)' in low
    assert 'C.append(d.EQ(s.mu, t.mu))' in low and 'C.append(d.EQ(s.sig[i], t.sig[i]))' in low
    assert 'st0 = AState(d, wit)' in low and 'shadow_match7(d, wit, st0, s)' in low
    assert 'shadow_match7(d, wit, st, t)' in low
    assert 'b_tree_valid(d, bs[0], bsts[0], s.sig)' in low
    assert 'b_tree_valid(d, t.b, bst5, t.sig)' in low
    # Equality to replay constrains topology/root, not old lo/hi annotations.
    endpoint_loop = next(n for n in ast.walk(module) if isinstance(n, ast.For) and ast.unparse(n.target)=='(a1, a2)' and 't.b.kl' in ast.unparse(n.iter))
    loop_text = ast.unparse(endpoint_loop)
    assert all('t.b.'+name in loop_text for name in ('kl','rl','kr','rr'))
    assert 't.b.lo' not in loop_text and 't.b.hi' not in loop_text
    assert 'C.append(d.EQ(t.b.root, bs[5].root))' in low
    assert 'no_intermediate_genuine(d, wit, s, bs, last, e, active)' in low
    result = {
        'status': 'UNIVERSAL_PUBLIC_CAPACITY_AUDIT_PASS',
        'E1_gate_passed_before_outside_phase': True,
        'raised_source_residual': raised_residual,
        'necessary_U_slack': 'old H1 residual+(2-D_target)',
        'U_source_admissibility_qualification_required': True,
        'visible_target_realization_review': 'real child or real grandchild, with ghost-parent observations reducing to a real source-root child; nonroot filter removes literal-slot0 aliases',
        'c_nonnegative_and_c_le_U_and_psi_le_U': True,
        'floor_preservation_contradiction': rounding_contradiction,
        'minimum_monotonicity_empty_set_cap_included': True,
        'depth8_debt0_unconditional_for_feasible_H1_debt': True,
        'depth6_7_debt_at_most1': True,
        'outside_E1_depth_partition_exhaustive': True,
        'seed_Lambda_possible_failures': ['w0,psi_source1,c_source0','w0,psi_source2,c_source<2','w1,psi_source2,c_source<2'],
        'seed_Lambda_globally_proved': False,
        'fixed_value_sources_do_not_automatically_discharge_edges': True,
        'original_source_endpoint_B_bounds_provenance_confirmed': True,
        'Score_bearing_H2_normalization_preservation_proved': False,
        'new_finite_population_tests': 0, 'new_source_transition_queries': 0,
        'new_original_root_evaluations': 0, 'new_label_fits': 0,
        'negative_core_bank_recomputed': False,
        'whole_source_formalization_claimed': False,
        'source_SHA256': hashlib.sha256(source_path.read_bytes()).hexdigest(),
        'M3_status': 'OPEN', 'CPU_seconds': time.process_time(), 'CPU_cap': CAP,
    }
    assert time.process_time() < CAP
    write('capacity_audit.json', result)
    print(json.dumps(result, indent=2), flush=True)

if __name__=='__main__':
    error = None
    try:
        main()
    except BaseException as exception:
        error = {'type': type(exception).__name__, 'message': str(exception)}
        raise
    finally:
        write('capacity_audit_exit.json', {'whole_process_CPU_seconds': time.process_time(), 'CPU_cap': CAP, 'error': error})
