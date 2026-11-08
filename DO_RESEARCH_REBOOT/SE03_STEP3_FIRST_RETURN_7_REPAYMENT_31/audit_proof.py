"""Completion/domain and integer proof audit, using saved source facts only.
No tree operation/compiler/root query; no replay or expansion of the period.
"""
import json,math,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    c=json.loads((B/'prefix_first_return_countercertificate.json').read_text());old=json.loads((P/'SE03_STEP3_NONEXTREMAL_SHALLOW_HELPER_REPAYMENT_30/nonextremal_source_countercertificate.json').read_text())
    T=c['original_diagonal_tree'];loop=[z for z in old['rows'] if z['occurrence'] in (145,146)]
    assert [z['target'] for z in loop]==[1,3] and loop[0]['before'][1]==T==loop[-1]['after'][1]
    assert [z['BF_path'] for z in loop]==['LL','RR'] and [z['qF'] for z in loop]==[1,1]
    support=[['K',1],['K',3]];W=c['P_word']+c['inverse_word']+support+c['last_A_reset']
    assert len(c['P_word'])==45 and len(c['inverse_word'])==40 and len(W)==101
    keeps={x for mode,x in W if mode=='K'};assert keeps=={1,3,5,7,9,11,13}
    q=[z['q'] for z in c['inverse_receipts']];assert len(q)==16 and sum(q)==26 and max(q)==3 and q.count(3)==2
    source_inverse=[]
    for k in range(4):
        L=2**k-1;Tq=2**(k+1)-k-2
        assert (L,Tq)==((0,0),(1,1),(3,4),(7,11))[k]
        if k:assert L==1+2*(2**(k-1)-1) and Tq==1+(2**k-(k-1)-2)+2*(2**(k-1)-1)
        assert k+Tq==2*L
        source_inverse.append({'q':k,'length':L,'B_doubles':Tq})
    Lsum=sum(2**k-1 for k in q);Qinv=sum(2**(k+1)-k-2 for k in q);Qfull=sum(q)+Qinv+2;ngenuine=len(q)+Lsum+2
    assert (Lsum,Qinv,Qfull,ngenuine)==(40,54,82,58)
    assert 2*ngenuine-Qfull==34
    C=math.comb(26,13)//14;assert C==742900
    # Entry and exact negative/recovery ledger values remain literal.
    al=c['ledger'];assert [z['sigma_E'] for z in al]==[0,-1,0,0,0,0,0,1]
    assert c['R_return']==0<c['D_entry']==1
    offset=85+101*C
    # Keep the earlier incomplete six-support completion as historical;
    # this v2 is the authoritative seven-genuine-key source certificate.
    v=dict(c);v.update(status='AUTHORITATIVE_FR31_PREFIX_COUNTER_V2_SEVEN_GENUINE_KEEP_CLOSED_CONSTRUCTION',
        supersedes='v1 completion word missed genuine KEEP1; new literal KEEP1,KEEP3 support loop closes B and restores the declared source domain. Local replay/negative ledger unchanged.',
        support_loop=support,support_loop_B_receipt=loop,closed_block_W=W,W_length=101,full_W_Q=82,
        full_W_genuine_KEEPs=58,CD_safe_margin_lower_bound=34,
        symbolic_closed_history={'C':C,'M_expression':{'op':'factorial','argument':C},'reaching_word':{'concat':['known_reaching_prefix_N',{'repeat':'closed_block_W','times':C}]},
            'source_period':{'repeat':'closed_block_W','times':{'op':'factorial','argument':C}},
            'initial_A':'known_synchronized_A0','initial_BF':'original_diagonal_tree','initial_BE':{'iterate':'F_E','times':C,'seed':'known_erased_seed_E0'},
            'F_E':'ordinary bottom-up execution of W retaining exactly original KEEPs with target!=11',
            'first_counter_helper_absolute':offset+39,'first_counter_upper_absolute':offset+41,'first_counter_return_absolute':offset+44,
            'closed_period_length_expression':{'multiply':[101,{'op':'factorial','argument':C}]},
            'finite_orbit_lemma':'all13-key BSTs number C; after C iterations any deterministic total F is periodic with p<=C; p divides C!',
            'full_period_replayed':False,'actual_distinct_word_copies':True},
        source_inverse_schema=source_inverse,
        full_raw_comparison_license={'prefix_signed_packet':'seven macros helper through next11; original sigma total0',
            'inverse_packet_budget_rule':'c=1 for Q1/2; for Q3 use c=2 iff actual H>=2, else c=1; every original natural owner included',
            'inverse_packet_sigma_lower_bound':'q_original-DeltaE(original forward)>=0',
            'largest_selected_packet_units':16,'intrinsic_E_width_bound':4,'raw_working_bound':20,
            'full_independent_H':'native h0; each of two original Q3 deficits paid by its following Q1 spare; any inverse central Q3 deficit paid by preceding Q1 spare in that inverse word',
            'aligned_H_profile_bound':3,'all_copy_all_legal_cut_H_profile_bound':6,
            'normalized_extension':'actual a, original retirement/eligibility/transport and B_a<=9 => B_extended<=24; NOT asserted for all supplied maps'},
        whole_W_A_cost='not numerically replayed; actual original A cost >=58 by genuine-macro root synchronization',
        source_queries_this_phase=0)
    out('prefix_first_return_countercertificate_v2.json',v)
    out('completion_arithmetic_audit.json',{'status':'PASS_SAVED_FACTS_AND_CLOSED_SOURCE_SCHEMA_ARITHMETIC','new_source_queries':0,
        'W_length':101,'genuine_KEEP_support':sorted(keeps),'support_loop_B_receipt_reused':True,'Q_W':Qfull,'genuine_KEEPs_W':ngenuine,
        'lower_bound_2A_minus_Q':34,'C':C,'period_expression':'W^(C!)','root_first_inverse':source_inverse,
        'first_return_sigma':-1,'full_horizon_source_replayed':False,
        'scope':'arithmetic/source-word certificate and universal closure manuscript; not execution or external certification of the enormous period',
        'counter_schema_sha256':hashlib.sha256((B/'CLOSED_COUNTEREXAMPLE_PROOF.md').read_bytes()).hexdigest()})
    print(json.dumps({'status':'SEVEN_KEEP_COMPLETION_V2_PASS','W_length':101,'Q_W':82,'genuine_KEEPs':58,'CD_margin_at_least':34,'source_queries':0}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_proof_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
