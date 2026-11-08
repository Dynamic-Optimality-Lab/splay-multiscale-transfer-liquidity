"""One new FIX source query, plus independent saved-proof/domain arithmetic.
No whole-period replay, no giant factorial construction, no original graph
compiler or old witness re-audit. All source queries charged cumulatively.
"""
import importlib.util,json,sys,time,math,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;QCAP=int(sys.argv[2]);CAP=float(sys.argv[1]);START=time.process_time()
sp=importlib.util.spec_from_file_location('FR31_FIX_mutable',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py')
I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
def tick():
    if I.queries>=QCAP or time.process_time()-START>=CAP-1:raise TimeoutError('FR31 inherited cap')
    I.queries+=1
I.tick=tick
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    f=json.loads((B/'FIX_9_activation_control.json').read_text());tree=I.Tree(f['before_A']);pa,ev=tree.access(9)
    assert pa==f['A_path']=='LRRL' and len(ev)==f['A_cost']==2 and ev==f['A_events'] and tree.shape()==I.fr(f['after_A'])
    c=json.loads((B/'prefix_first_return_countercertificate_v2.json').read_text());W=c['closed_block_W'];qs=[z['q'] for z in c['inverse_receipts']]
    assert len(W)==101 and set(k for mode,k in W if mode=='K')==I.M
    assert c['support_loop']==[['K',1],['K',3]]
    assert [z['qF'] for z in c['support_loop_B_receipt']]==[1,1]
    assert c['support_loop_B_receipt'][0]['before'][1]==c['original_diagonal_tree']==c['support_loop_B_receipt'][-1]['after'][1]
    # Independent length/cost recurrences; no source evaluation is hidden.
    L=[0];Q=[0]
    for k in range(1,4):L.append(1+2*L[-1]);Q.append(1+Q[-1]+2*L[-2])
    assert L==[0,1,3,7] and Q==[0,1,4,11]
    assert sum(L[q] for q in qs)==40 and sum(Q[q] for q in qs)==54 and sum(qs)==26
    assert c['full_W_Q']==82 and c['full_W_genuine_KEEPs']==58 and 2*58-82==34
    C=math.comb(26,13)//14;assert c['symbolic_closed_history']['C']==C==742900
    assert c['symbolic_closed_history']['first_counter_helper_absolute']==85+101*C+39
    assert c['symbolic_closed_history']['first_counter_return_absolute']==85+101*C+44
    al=c['ledger'];assert sum(z['sigma_E'] for z in al[1:7])==-1 and sum(z['sigma_E'] for z in al[1:])==0
    assert c['first_return_actual_A']==6 and c['first_return_full_Q']==12 and c['first_return_original_price']==0
    assert al[1]['E_before']==1 and al[6]['E_after']==0 and al[7]['E_after']==1
    own=I.mp(c['local_native_h0']);H=I.mp(c['local_full_comparison']);assert all(H[d]==u for d,u in own.items()) and len(H)==len(set(H.values()))==12
    assert H[(125,3)]==(126,1,1) and H[(127,3)]==(128,1,1)
    assert c['full_raw_comparison_license']['raw_working_bound']==4+16==20
    assert I.queries==1
    out('final_independent_proof_audit.json',{'status':'PASS_DISTINCT_FIX_CONTROL_AND_SEVEN_KEEP_COMPLETION_ARITHMETIC','source_queries_this_phase':1,
        'new_FIX_activation_A_cost':2,'PREFIX_activation_A_cost':1,'PREFIX_first_return_sigma':-1,'FIX_universal_status':'OPEN; this cost control is not all FIX paths',
        'W_length':101,'full_W_Q':82,'genuine_KEEPs':58,'CD_margin_at_least':34,'support_loop_domain_gap_closed':True,
        'source_completion':'root-first SS inverse plus ordered reset; erased closure by finite13-BST functional orbit and explicit C! period',
        'complete_word_or_giant_period_replayed':False,'scope_of_execution':'prior mutable30-call prefix, tuple8-call revised suffix, and this one FIX A access; all exact source-closure claims beyond these use the written proof schemas',
        'trust':'same research agent with distinct implementations; not external peer review or formal proof-assistant verification',
        'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('prefix_first_return_countercertificate_v2.json','CLOSED_COUNTEREXAMPLE_PROOF.md','FIX_9_activation_control.json')}})
    print(json.dumps({'status':'FR31_FINAL_PROOF_AUDIT_PASS','new_queries':1,'PREFIX_sigma':-1,'FIX_activation_cost':2,'seven_KEEP_completion':True}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent3_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':I.queries,'source_queries':I.queries})
