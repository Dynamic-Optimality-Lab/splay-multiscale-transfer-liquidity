"""Symbolic one-credit spine renewal; no full-bank hypothesis is needed."""
import sys
import z3
sys.dont_write_bytecode = True
import transport as T


def main():
    H, t, w, g, left, p, previous = z3.Reals('H t w g left p previous')
    remaining = t+w+g+left+p+previous-1
    clamp = lambda v: z3.If(v<=0, 0, z3.If(v>=H, H, v))
    base = [H>=1, t>=0, t<=H, w>=1, w<=H, g>=1, g<=H,
            left>=0, left<=H, p>=0, p<=H, previous>=0, previous<=H]
    target = clamp(remaining)
    persistent = clamp(remaining-H)
    claims = {
        'funded_unit_guard': remaining>=1,
        'target_accumulates_one': target>=z3.If(t+1>=H, H, t+1),
        'full_target_remains_full': z3.Implies(t==H, target==H),
        'persistent_spine_keeps_one_after_warmup': z3.Implies(t==H, persistent>=1),
        'input_left_and_other_carry_may_be_zero': z3.Implies(z3.And(left==0,p==0,previous==0,t==H),persistent>=1)
    }
    checked=[]
    for name, claim in claims.items():
        solver=z3.Solver(); solver.add(*base,z3.Not(claim)); assert solver.check()==z3.unsat
        checked.append(name)
    T.write('SPINE_RENEWAL_CERTIFICATE.json', {
        'status': 'PROVED_RESTRICTED_PHYSICAL_STREAM', 'queries': checked,
        'quantifiers': 'Every real H>=1, arbitrary initial target balance in[0,H], arbitrary other nonnegative carry/retiring inputs, two fresh distinct old spine banks each>=1.',
        'rule': 'Target first, second-middle persistent root second; other roles afterward.',
        'initialization': 'No target credit is assumed. Each funded step raises it by at least one until cap H; ceil(H) steps suffice.',
        'renewal': 'Once the target bank is full, every finalized persistent-spine bank receives at least one credit. The target stays full. The same lower spine profile can therefore be iterated at arbitrarily many certified coarsening scales.',
        'physical_binding': 'Exact LL/RR six-role windows from the original full H comb recurrence; owners must be distinct, fresh banks must enter with>=1, and nonreset interleavings must not invalidate those inputs.',
        'arbitrary_source_gap': 'Derive and maintain the fresh-spine entry lower bound under every legal original predecessor, including cross rotations, overlapping footprints, and restoration. This is not proved or assumed.',
        'global_budget_and_seam': 'The already proved9H A budget and monotone greatest-cyclic-balance construction apply to the selected physical-role policy.',
        'unrestricted_root_cost_obligations_deleted': 0, 'universal_CD': 'OPEN'})
    print({'proved_symbolic_queries':len(checked),'full_bank_assumption_removed':True,'universal_CD':'OPEN'})


if __name__ == '__main__':
    main()
