"""Cost-preserving common-gap inflation and anonymous-port pump adversary.

Universal provenance is the complete arbitrary-gap rotation identity and the
H3q spine argument in the Notion proof. Finite observations do not prove it.
"""
import sys
from collections import Counter
from fractions import Fraction
sys.dont_write_bytecode=True
import trace as X
import trace_teacher as T


def inflate(source,width=5):
    assert width==5
    n=len(source['initial_A']['children']);assert sorted(map(int,source['initial_A']['children']))==list(range(1,n+1))
    old=source.copy();old['expected_Q']=source.get('expected_Q',X.K.OLD.replay(source)['Q_B'])
    out=X.C.embed(old,n=width*n,active=tuple(width*k for k in range(1,n+1)))
    out['name']='uniform_gap5__'+source['name'];out['parent_source_name']=source['name'];out['padding_width']=5
    out['original_q_parameter']=source.get('q');out['original_p_parameter']=source.get('p')
    return out


def relax_candidate():
    old=X.K.load(X.HERE/'run_001/JOINT_PORT_POTENTIAL.json');rows=X.K.load(X.HERE/'run_001/POTENTIAL_ROWS.json.gz')
    fixed=old.copy();fixed.update({'status':'FINITE_EXACT','c':'2','d':'2','c_plus_d':'4','recovery':'Preserve all rounded potential coefficients; increase only c,d to2 and verify every row exactly. The failed original recovery is preserved.'})
    p={s:Fraction(v) for s,v in fixed['values'].items()}
    slack=[Fraction(r['q'])+sum(v*p[s] for s,v in r['delta'].items())-2*r['a']-2*r['k'] for r in rows]
    fixed['max_exact_slack']=str(max(slack));fixed['worst_original_id']=rows[max(range(len(rows)),key=lambda i:slack[i])]['id']
    T.verify_potential(rows,fixed);X.write('run_001/FINITE_RELAXED_CANDIDATE.json',fixed)
    return fixed


def check_step_swaps(z):
    n=z['source']['embedding']['physical_keys'][-1]//5;q=z['source']['original_q_parameter'];op=n+7;x=n-7
    r=z['operations'][op-1];assert r['a']==1 and r['q']==q+1 and r['k']==1 and r['local_only_unchanged']
    chosen=z['steps'][r['steps'][0]:r['steps'][1]];rr=[s for s in chosen if s['actor']=='B' and s['type']=='RR'];assert len(rr)==q
    swaps=[]
    for s in rr:
        before=Counter(s['signature_before'].values());after=Counter(s['signature_after'].values());assert before==after
        for b in s['bits']:
            assert b['internal_block'] is None and b['middle'] is not None
            # The physical H comb pivots and transported middle roots all
            # have nonempty original-skeleton left children. This is the
            # symbolic finite type responsible for the histogram swap.
        swaps.append(s['id'])
    assert all(all(not v for v in mask) for s in chosen for mask in s['retained_bit_masks'].values())
    assert sum(abs(v) for v in r['delta'].values())<=20
    return {'source':z['source']['name'],'op':op,'physical_target':5*x,'a':r['a'],'q':r['q'],'k':r['k'],'RR_steps_with_exact_anonymous_histogram_cancellation':swaps,'all_original_rotations_cross_blocks':True,'whole_delta_l1':sum(abs(v) for v in r['delta'].values()),'whole_delta':r['delta'],'claim_scope':'Finite verification; arbitrary-q proof is the explicit uniform-gap / RR-swap argument.'}


def run():
    cert=relax_candidate() if not (X.HERE/'run_001/FINITE_RELAXED_CANDIDATE.json').exists() else X.K.load(X.HERE/'run_001/FINITE_RELAXED_CANDIDATE.json')
    out=[]
    for i,q in ((16,1),(17,5)):
        name=f'run_001/trace_{i:02d}.json.gz';source=X.K.PARAM.H(3,q)
        z=X.K.load(X.HERE/name) if (X.HERE/name).exists() else X.compile_source(inflate(source))
        if not (X.HERE/name).exists():X.write(name,z)
        bn=f'run_001/bank_{i:02d}.json.gz'
        if not (X.HERE/bn).exists():X.write(bn,T.bank(z,c=4,d=0,capacity=4))
        pump=check_step_swaps(z)
        p={s:Fraction(v) for s,v in cert['values'].items()};r=z['operations'][len(source['initial_A']['children'])+6]
        # Complete formula: all unseen anonymous states receive value zero.
        value=Fraction(r['q'])+sum(v*p.get(s,0) for s,v in r['delta'].items())-2*r['a']-2*r['k']
        pump['finite_candidate_zero_extension_slack']=str(value)
        out.append(pump);print({'index':i,'source':z['source']['name'],'A':z['A'],'Q_B':z['Q_B'],'pump_delta_l1':pump['whole_delta_l1'],'candidate_slack':str(value)},flush=True)
    X.write('run_001/PADDING_PUMP_CERTIFICATE.json',{'cases':out,'universal_claim':'For every fixed shared finite-valued function f of the declared anonymous block observer, the H3q RR part has exactly zero change after uniform gap padding. The whole critical change has absolute value <=10*range(f), while a=k=1,q=q+1. No finite c,d can prove acceptance in this grammar.','root_status':'OPEN','excluded':'Fixed anonymous-port block-state sums (and uniformly bounded global corrections), not named-port geometry, unbounded state functions or history-aware banks.'})


if __name__=='__main__':run()
