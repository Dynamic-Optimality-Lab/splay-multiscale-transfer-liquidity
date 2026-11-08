"""Static W105 descriptor and seven-form arithmetic, no source query.
Source normal-form derivations are in the manuscript, not executed here.
"""
import json,time,math,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;OLD=P/'SE03_STEP3_FIRST_RETURN_7_REPAYMENT_31'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    c=read(OLD/'prefix_first_return_countercertificate_v2.json');w=c['closed_block_W'];assert w[41]==['K',9]
    L=[['K',x] for x in (13,9,11,9)];W=w[:42]+L+w[42:]
    assert len(W)==105 and {x for m,x in W if m=='K'}=={1,3,5,7,9,11,13}
    assert [W[i-1] for i in (39,41,42,43,47,48,49)]==[['K',11],['K',11],['K',9],['K',13],['K',5],['K',7],['K',11]]
    assert sum((2,1,2,1))==6 and sum((-1,2,-1,2))==2
    C=math.comb(26,13)//14
    v={'status':'EXACT_TRANSIENT_TWO_CONTROL_WITH_SYMBOLIC_CLOSURE','source_queries_this_phase':0,
       'base_C31_counter_sha256':hashlib.sha256((OLD/'prefix_first_return_countercertificate_v2.json').read_bytes()).hexdigest(),
       'closed_block_W105':W,'insertion_after_W101_position':42,'inserted_KEEP_word':L,
       'inserted_H':[1,1,1,1],'inserted_Q':[2,1,2,1],'inserted_E_boundaries':[1,0,1,0,1],
       'inserted_sigma':[-1,2,-1,2],'closed_block_Q':88,'closed_block_genuine_KEEPs':62,'CD_margin_lower_bound':36,
       'short_prefix_helper':124,'short_prefix_first_upper':126,'short_prefix_intermediate_two':128,
       'short_prefix_FIRST_return7':133,'terminal_signed_balance':1,'terminal_debt':0,'maximum_displayed_intermediate_debt':2,
       'closed_source_descriptor':{'C':C,'reaching_word':['C31_N85',{'repeat':'closed_block_W105','times':C}],
           'period':{'repeat':'closed_block_W105','times':{'factorial':C}},
           'initial_A':'C31_A0','initial_BF':'C31_T','initial_BE':{'iterate':'F105','times':C,'seed':'C31_E0'},
           'F105':'ordinary execution of W105 retaining all original KEEPs except target11',
           'first_helper_absolute':85+105*C+39,'first_transient_two_absolute':85+105*C+43,'first_return7_absolute':85+105*C+48},
       'W105_and_period_replayed':False,'source_completion':'A/B identity insertion plus inherited W101 inverse/reset; erased finite orbit written proof',
       'is_principal_FR32_counterexample':False,'external_audit':False}
    out('transient_W105_certificate.json',v)
    E=dict(zip('ABCDEFG',(1,0,0,0,1,2,1)));p=dict(zip('ABCDEFG',(0,0,1,-1,1,3,3)))
    edges=[('A','B',11,1,0),('A','D',13,2,-1),('B','A',9,1,2),('B','C',13,1,1),('C','B',11,1,1),('C','F',9,2,2),
           ('D','E',9,1,2),('E','D',13,1,0),('E','B',11,2,-1),('F','G',13,1,0),('G','F',9,1,2),('G','B',11,2,-1)]
    for a,b,x,q,sig in edges:assert sig==2-q+E[b]-E[a] and sig>=p[b]-p[a]
    lower=[0,2,3,3,0,0,2];assert all(p[s]+v>=0 for s,v in zip('ABCDEFG',lower))
    out('upper_seven_form_arithmetic.json',{'status':'PASS_ALL_SYMBOLIC_EDGE_AND_LOWER_EXIT_ARITHMETIC','source_queries':0,
        'E':E,'path_lower_potential':p,'source_derived_edges':edges,'first_lower_sigma_min':dict(zip('ABCDEFG',lower)),
        'source_normal_forms':'UPPER_ONLY_BARRIER.md; derived symbolically, not newly replayed',
        'arbitrary_upper_length_proof':'telescope sigma>=Delta p; add proved lower-exit bound; never assert a bounded return length',
        'principal_terminal_CARRY1_proved':False})
    print(json.dumps({'status':'W105_AND_SEVEN_FORM_ARITHMETIC_PASS','source_queries':0,'W105_terminal_debt':0,'transient_debt':2}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_proof4_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
