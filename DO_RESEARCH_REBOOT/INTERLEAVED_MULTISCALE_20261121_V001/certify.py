"""Compact exact Hall cuts and proof-scope records from complete witnesses."""
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    verified=json.loads((HERE/'INDEPENDENT_VERIFICATION.json').read_text());assert verified['passed']
    cuts=[]
    for file in sorted(HERE.glob('*_complete_witness.json')):
        w=json.loads(file.read_text());s=w['source'];n=s['n']
        for st in s['stages']:
            i=st['depth'];r=st['r'];physical=lambda k:n+1-(1<<i)*k if s['reflected'] else (1<<i)*k
            assert w['rows'][st['maximum_op']-1]['target']==physical(r)
            assert w['rows'][st['critical_op']-1]['target']==physical(r-1)
            assert w['rows'][st['maximum_op']-1]['q_B']==(r-1)//2
        for dem in w['all_B_double_records']:
            if 'Gamma_clock' in dem:
                assert dem['Gamma_lap']==dem['Gamma_clock']//w['period_clock']
                assert dem['kappa_lap']==dem['kappa_clock']//w['period_clock']
        for p in w['result']['probe_certificates']:
            if p['copy']<2:continue
            assert len(p['selected_seed_runs'])==s['h'] and len(p['all_real_A_resource_units'])==1
            origin=n+1 if s['reflected'] else 0
            delta=[]
            for ticket in p['selected_seed_runs']:
                z=abs(p['target']-origin);v=(z&-z).bit_length()-1
                gap=ticket['depth']-v;delta.append(gap)
            assert delta==list(range(s['h']))
            cuts.append({'witness':file.name,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),
                         'source_h':s['h'],'source_n':n,'window_radius':s['radius'],
                         'literal_birth_demands':[z['birth'] for z in p['selected_seed_runs']],
                         'labels':[z['label'] for z in p['selected_seed_runs']],
                         'alignment_deficits':delta,'common_first_hit':p['op'],
                         'allowed_KEEP_gaps':p['allowed_original_KEEP_window'],
                         'all_real_A_units':p['all_real_A_resource_units'],
                         'Hall_demand':s['h'],'Hall_capacity_at_load_C':'C',
                         'parametric_deficit':'h-C; positive for h>C',
                         'forced_genuine_U_records':p['forced_internal_U_doubles']})
    (HERE/'HALL_CERTIFICATES.json').write_text(json.dumps({'cuts':cuts,'exact_scope':'Deficient first-hit-window resource graph; not a deficient graph with all original A work as available resources.'},indent=2),encoding='utf-8')
    theorem={
      'proof_url':'https://app.notion.com/p/41f6251839be81a1ab00fe1038effc58',
      'principal_result':'REFUTED—EXACT: unrestricted cross-scale pooling of all selected seed birth runs into uniformly bounded original-KEEP-radius first-hit A windows.',
      'parametric_quantifiers':'For every finite load C and fixed integer radius ell>=0, choose integer h>C and pad ell+1 identity KEEPs on each side of the common first hit. The complete original W_(h,ell,Y) contains h distinct eligible seed birth runs but exactly one real A cost unit in their union of permitted windows.',
      'same_source_scales':'One W has n=12*2^h-3 throughout. Its stages use d_i=i,r_i=12*2^(h-i)-3,p_i=1,q_i=3*2^(h-i)-2. No switch of sources, carriers or ambient support is made between stages.',
      'arbitrary_interleaving_lemma':'After the p=1 critical prefix, all odd base vertices below r-2 are protected leaves. F={2,4,...,r-3,r-2,r-1,r} is an actual rooted free hull. Arbitrary original KEEP traffic on F preserves those full subtrees; the final full decreasing F scan yields the exact full T_((r-3)/2,d+1).',
      'selected_stack':'a=2^(h+1)+1, x=a+1; L_i=[a,a+2^(i+1)-2], size2^(i+1)-1. Original maximum bit0 step(r_i-g_i)/2, g_i=2^(h+1-i)+1, creates L_i. All chosen runs survive until common KEEP x.',
      'actual_consumer_obstruction':'In copy2, B probe LL whole frames L3,L5,...,L_(2*floor((h-1)/2)+1) are neutral, interior and absent from A over their full original Pi windows. Hence at least floor((h-1)/2) genuine original U_int consumers meet unbounded scale/alignment deficits at that one A gap.',
      'derived_positive_theorem':{'status':'PROVED—RESTRICTED DOMAIN, source-uniform at the precise eligibility below.',
        'quantity':'R_(o,k) is the literal original U_int subset whose whole-frame carrier-rank label is I_(d,j)^o=[o+j*2^(d+1)+1,o+(j+1)*2^(d+1)-1], d>=1, and d-v2(abs(x-o))<=k at its producing KEEP rank x. Origin o is fixed once per source and k is fixed; x=o has no canonical containing interval.',
        'bound':'R_(o,k)(W)<=(k+1)K_B(W)<=(k+1)A(W). In particular R_(o,2)<=3A.',
        'real_A_load':'At most k+1, on bit0 of the first nonzero original A StepEv in each producer KEEP gap.',
        'domain':'All admissible exactly paired-closed original sources with their original static ancestor-closed B carrier S and original literal U_int predicate. Carrier ranks are only measurements; no physical path/node/event is removed. A private ancestors and helpers remain unrestricted.',
        'proof':'A canonical interval of depth d containing x has d>=v2(abs(x-o)). Eligibility leaves only k+1 possible depths. Whole-frame carrier labels strictly increase along the original B splay, so at most one demand at each eligible depth is produced at a KEEP. Distinct original KEEP gaps give disjoint real A representatives.',
        'birth_corollary':'All actual B canonical-label birth runs with first-hit deficit<=k likewise have A load<=k+1 across all sizes, because at a first hit the live labels are nested and at most one exists per eligible depth.',
        'not_a_one_size_sum':'Bound the simultaneous load at each actual A representative over every scale, then sum original KEEP gaps once.',
        'nonvacuity':'The new h>=3 sources contain an actual U whole frame L3 of deficit2. Uniform E inflation shifts both its canonical depth and target valuation by the same amount, producing arbitrarily large covered frames with the same constant3.'},
      'literal_complement':'Original U_int whose frame is noncanonical for the single chosen origin, or whose alignment deficit exceeds k. In the new stack forced original U frames have deficits2,4,...; this complement is unbounded within one complete source family.',
      'not_refuted':['Existence of an arbitrary nonlocal globally bounded A charge','Scalar total seed count O(A) with a different redistribution','A demand allocator that can discard congested seed tickets and use other tickets','The old fixed-size and one-depth bounds','The old I/J lifecycle theorem','Universal Coarse Double or Dynamic Optimality as conjectures'],
      'not_proved':['Global O(A) bound for the entire arbitrary-restoration/multiple-scale residual','A strict enlargement of the frozen actual UF paid partition','An actual UF hard escape or counterexample to the original cost inequality'],
      'accounting_composition':'Assign old paid original IDs first, then restrict the new R_(o,k) map to the literal remainder. Add at most k+1 to its old A-load coefficient. No owner-vacancy or virtual-A credit claim.',
      'next_missing_implication':'Control unbounded alignment-deficit and noncanonical consumer groups with remote original A restoration work, proving global sharing; or reallocate pooled seed tickets with an independently proved density/packing bound. A fixed first-hit window cannot provide the necessary capacity.',
      'before':'One chosen size admits a first-hit injection. All-depth overlap and arbitrary restored ancestry had no audited budget.',
      'after':'A complete same-carrier arbitrary-interleaving construction gives unbounded cross-scale first-hit congestion. Bounded alignment deficit, rather than bounded size, has a proved global A budget. The full complement remains open.',
      'net_advancement':'Exact rejection of one natural all-depth charging extension, plus a scoped all-scale bound for an explicitly recognized original U class. This does not close universal conservation.',
      'graph_edge':'arbitrary interleaved whole-carrier coarsening -> live cross-scale ancestry stack -> common first hit. The bounded-deficit part maps to original A with load k+1; the unbounded-deficit part cannot use bounded first-hit windows.'}
    (HERE/'THEOREM_CERTIFICATE.json').write_text(json.dumps(theorem,indent=2),encoding='utf-8')
    print(json.dumps({'exact_Hall_cuts':len(cuts),'all_h_obstruction':'symbolic proof required and stated','bounded_alignment_K_at_k2':3}))


if __name__=='__main__':main()
