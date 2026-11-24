"""Extract exact candidate coefficients and check closed-form ledger identities.

The parameterized mathematical proofs are in the linked Notion manuscript;
these checks preserve finite physical evidence and the symbolic block table.
"""
import json
import math
from collections import Counter,defaultdict
from pathlib import Path
import sys

sys.dont_write_bytecode=True
from verify_witnesses import labels, rotate, vine

HERE=Path(__file__).resolve().parent


def motifs(tree):
    edges=set();paths=set();forks=set();stack=[tree]
    while stack:
        v=stack.pop()
        if v is None:continue
        key,left,right=v
        if left is not None and right is not None:forks.add((key,left[0],right[0]))
        for side,child in [('L',left),('R',right)]:
            if child is None:continue
            edges.add((key,child[0],side))
            for second,grandchild in [('L',child[1]),('R',child[2])]:
                if grandchild is not None:paths.add((key,child[0],grandchild[0],side,second))
            stack.append(child)
    return edges,paths,forks,labels(tree)


def four_features(trees):
    a,b=motifs(trees['A']),motifs(trees['B'])
    return [len(y-x) for x,y in zip(a,b)]


def selected_feature_changes(w):
    n=w['source']['N'];p=w['source']['p'];trees={'A':vine(n),'B':vine(n)}
    selected={n-1+(1<<p),2*n+2};before={};after={}
    for e in w['real_rotations']:
        actor,op,_,_=e['id']
        if actor=='B' and op in selected and op not in before:before[op]=four_features(trees)
        trees[actor]=rotate(trees[actor],e['demoted'],e['direction'])
        if actor=='B' and op in selected:after[op]=four_features(trees)
    return {op:[y-x for x,y in zip(before[op],after[op])] for op in selected}


def mersenne_index(n):
    return (n+1).bit_length()-1 if n>=3 and n&(n+1)==0 else None


def main():
    if (HERE/'FINAL_MANIFEST.json').exists():
        raise RuntimeError('Sealed run: output generation requires a new versioned directory.')
    summaries=[json.loads(p.read_text()) for p in HERE.glob('H_p*_summary.json')]
    phase_checks=[]
    for d in summaries:
        if d['p']!=3:continue
        q=d['q'];ell=d['N'].bit_length()-2;eps=int((q+1)&q==0)
        assert d['totals']=={'a':64*(q+1),'q_B':28*q+25,'z_B':28*q+27,'u':10*q+5,
                              'd':48*q+53,'k':32*q+37,'A_rotations':64*(q+1),'B_rotations':84*q+77}
        predicted={'prep:A':-ell,'descent:A':-eps,'descent:B':ell-7*q-4+eps,
                   'forward:A':-ell,'forward:B':7*q+4+ell,'reverse:A':-ell,'reverse:B':ell}
        assert {k:v['M'] for k,v in d['phase_potential_changes'].items()}==predicted
        phase_checks.append({'q':q,'N':d['N'],'ell':ell,'epsilon':eps,'all_closed_forms_match':True})
    witnesses=[]
    for path in sorted(HERE.glob('*_complete_witness.json')):
        w=json.loads(path.read_text());n=w['source']['N'];coefs=defaultdict(Counter);births15=deaths15=0;losses=defaultdict(Counter)
        for e in w['real_rotations']:
            if e['id'][0]!='B':continue
            t=e['id'][1];x=e['target'];old=e['removed'];new=e['created']
            assert old[0]<=x<=old[1] and not new[0]<=x<=new[1]
            for lab,sign in [(old,1),(new,-1)]:
                h=mersenne_index(lab[1]-lab[0]+1)
                common=(lab[0]==1 and lab[1]<x) or (lab[1]==n and lab[0]>x) or lab==[1,n]
                if h is not None and not common:coefs[t][h]+=sign
            r=old[1]-old[0]+1;losses[t][r]+=1
            births15+=new[1]-new[0]+1==15;deaths15+=r==15
        assert all(all(c<=1 for c in v.values()) for v in losses.values())
        assert births15==deaths15
        own15=sum(d['U_int'] and 15 in d['created_sizes'] for d in w['all_B_double_records'])
        assert own15<=births15<=2*n+len({n+1-(1<<j) for j in range(w['source']['p']+1)})-1
        p=w['source']['p'];q=w['source']['q'];last=n-1+(1<<p)
        if p>=3:assert {h:v for h,v in coefs[last].items() if v}=={p+1:-q}
        if q==5:
            first3=2*n+2
            assert {h:v for h,v in coefs[first3].items() if v}=={h:1 for h in range(2,p+2)}
        feature_changes=selected_feature_changes(w)
        if p>=3:assert feature_changes[last]==[0,0,0,-2]
        if q==5 and p>=3:assert feature_changes[2*n+2]==[0,-1,-1,-(2+int(p%2==0))]
        witnesses.append({'witness':path.name,'p':p,'q':q,'own_size15_U_demands':own15,'actual_size15_births':births15,
                          'actual_size15_deaths':deaths15,'last_critical_sparse_weight_coefficients':dict(coefs[last]),
                          'first_forward_KEEP3_sparse_weight_coefficients':dict(coefs[2*n+2]),
                          'old_four_feature_deltas':feature_changes})
    result={'p3_all_parameter_formula_checks':phase_checks,'original_witness_layer_checks':witnesses,
            'universal_claims_require_symbolic_proof':True}
    (HERE/'EXACT_LAYER_COEFFICIENTS.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    theorem={
      'primary_quantity':'Phi_M(A,B;S)=-sum_{J in J_S(B)\\J_S(A)} 1[|J|=2^h-1 for some h>=2]',
      'A_rotation_bound':{'upper':1,'lower':-1,'domain':'Any complete same-key BST pair and fixed S, with original SET duplicate suppression. All orientations and private nodes included.'},
      'H3q_burst':{'N':'16(q+1)+1','operation':'N+7','u':'q','d':2,'k':1,'Delta_B_Phi_M':'-q','Delta_B_Phi_15':'-q'},
      'H3q_first_maximum_obstruction':{'operation':'N','a_current':0,'u':0,'d':2,'k':1,
        'Delta_B_Phi_M':'floor(log2 N)-1','parameter_choice':'q=2^(h-4)-1, h>=5 => N=2^h+1 and Delta=h-1',
        'conclusion':'No finite absolute beta,gamma can bound u+Delta_B Phi_M by beta*d+gamma*k on all original B phases.'},
      'positive_demand_restoration_obstruction':{'source':'Complete H_(p,5), p>=1','N':'12*2^p+1','operation':'2N+2, first forward KEEP3',
        'a_current':1,'incoming_A_KEEP_gap_cost':1,'u':'ceil(p/2)','d':'2+1[p even]','k':1,
        'Delta_B_Phi_M':'p','conclusion':'Positive-demand phases alone also violate every such fixed-coefficient law, even with an additional fixed multiple of the incoming A KEEP-gap cost.'},
      'post_derivation_scope_extension':{'quantity':'Phi_w=-sum_{h>=2} w_h * #{J in J_S(B)\\J_S(A): |J|=2^h-1}',
        'weights':'Arbitrary fixed signed finite real values w_h, independent of source/support/ambient size. Only finitely many occur in each finite state.',
        'critical_necessity':'For each p>=3, the last critical H_(p,q) phase has u=q, d=2,k=1,Delta=-q*w_(p+1). Letting q grow forces w_h>=1 for all h>=4.',
        'restoration_contradiction':'The first forward KEEP3 in H_(p,5) has Delta=sum_(h=2)^(p+1) w_h. Then u+Delta >=ceil(p/2)+(p-2)+w2+w3 -> infinity, while d<=3,k=1 and incoming A gap=1.',
        'claim':'The complete B-phase certificate is impossible throughout this entire reweighted layer family. This is a corollary of the same exact source transitions, not a changed success criterion.'},
      'strictly_larger_obstruction_class':{'quantity':'Phi_(lambda,w)=lambda_E*f_E+lambda_P*f_P+lambda_F*f_F+lambda_S*Psi+Phi_w',
        'coefficients':'All fixed signed finite real lambda_i and fixed signed finite real scale weights w_h, independent of source and ambient population.',
        'critical_old_feature_delta':'(0,0,0,-2) for all p>=3 at the last critical H_(p,q) phase',
        'restoration_old_feature_delta':'(0,-1,-1,-d), d=2+1[p even], at first forward KEEP3 of H_(p,5), p>=3',
        'proof':'Critical q variation still forces w_h>=1 for h>=4. Restoration contributes sum(w_h)-lambda_P-lambda_F-d*lambda_S, whose unbounded growth cannot be canceled by fixed old coefficients. Even a fixed multiple of incoming KEEP-gap A work is1 at that restoration access.',
        'scope_limit':'Does not exclude arbitrary cardinality weights outside the Mersenne support, source-dependent weight assignments, other A/B geometry, or globally overlapping-window laws with a separately proved budget.'},
      'fixed_layer_positive_theorem':{'quantity':'B_r(W) = all actual B SET births with proper nonempty S-label cardinality exactly r',
        'bound':'B_r<=K_B<=A, for every r>=1, uniformly in r and source',
        'reason':'Every B SET death contains the accessed key, so at most one distinct size-r label dies per B access; new labels exclude that key and cannot die in that access. Cyclic birth/death totals agree.',
        'scoped_demand_class':'Original U_int doubles whose own two bits include an actual size-r SET birth; choose the earliest such bit. The class has size<=A.',
        'literal_complement':'Original U_int demands with no such own-double size-r birth.',
        'novelty_limit':'An exact-layer potential realization/sharpening of the prior bounded-cardinality birth mechanism. No strict enlargement of the frozen UF paid class has been established.'},
      'status':'Required A-locality and linear H3q burst response proved symbolically; the selected global B law has new exact parametric source obstructions. Universal CD and Dynamic Optimality remain open.'}
    (HERE/'THEOREM_CERTIFICATE.json').write_text(json.dumps(theorem,indent=2),encoding='utf-8')
    print(json.dumps({'H3q_formula_checks':len(phase_checks),'complete_witness_layer_checks':len(witnesses),'theorem_certificate':'written'}))


if __name__=='__main__':main()
