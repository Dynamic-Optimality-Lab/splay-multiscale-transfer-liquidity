"""Distinct cross-reset verification and static mixed-template interfaces.
Only26 new A-only source operations; completed source periods are reused.
"""
import importlib.util,json,sys,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;QCAP=int(sys.argv[2]);CAP=float(sys.argv[1]);START=time.process_time()
sp=importlib.util.spec_from_file_location('C30_reset_mutable',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py')
I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
def tick():
    if I.queries>=QCAP or time.process_time()-START>=CAP-1:raise TimeoutError('cross reset inherited cap')
    I.queries+=1
I.tick=tick
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    p=json.loads((B/'mixed_reset_bridge_receipt.json').read_text());n=json.loads((B/'forward_recovery_and_period_receipt.json').read_text());old=json.loads((P/'SE03_STEP3_MARKED_COMB_SIGNED_REPAYMENT_29/comb_source_fixtures.json').read_text());caps=[]
    for q in p['reports']:
        tree=I.Tree(q['initial'][0]);cost=0
        for z in q['rows']:
            assert tree.shape()==I.fr(z['before_A']);path,ev=tree.access(z['target']);assert path==z['A_path'] and ev==z['A_events'] and tree.shape()==I.fr(z['after_A']);cost+=len(ev)
        assert cost==q['reset_A_cost'] and tree.shape()==I.fr(q['after_A'])
    assert p['reports'][0]['after_A']==p['reports'][1]['after_A']
    # Each first reset begins at root3 and accesses13: first event exists.
    # All comparer endpoints in that reset are therefore stable bits j1.
    for q in old['reports']:
        h=I.mp(q['full_independent_H']);lo=q['actual_interval'][0]
        prefix_units=[u for u in h.values() if lo<=u[0]<lo+13]
        assert set(prefix_units)<={(lo,1,0),(lo,1,1)} and I.buffer_peak(h)==3
        assert q['period'][:13]==[['D',x] for x in range(13,0,-1)]
        caps.append(q['signed_period_rho'])
    hu=I.mp(n['full_H_aligned']);lo=n['aligned_source_interval'][0]
    assert {u for u in hu.values() if lo<=u[0]<lo+13}<={(lo,1,0),(lo,1,1)} and I.buffer_peak(hu)==3
    state=I.fr(p['W_boundary'][1]);_,ch=I.marked(state,I.M);L=sum(not v for v in ch.values());br=sum(len(v)>=2 for v in ch.values());E=L-br-1
    assert L-1==E+2==3
    assert p['W_boundary'][1:]==p['U_boundary'][1:]
    assert I.queries==26
    out('independent_mixed_reset_audit.json',{'status':'PASS_DISTINCT_CROSS_RESET_AND_MIXED_TEMPLATE_INTERFACE','source_queries':I.queries,
        'reset_cost_W':p['reset_cost_W'],'reset_cost_U':p['reset_cost_U'],'common_signed_boundary':3,
        'W0_W1_signed_periods':caps,'U_signed_period':60,'raw_H_local_peak':3,'raw_H_all_m_all_cut_bound':6,
        'normalized_profile_condition':9,'physical_extension_bound':24,'independent_raw_working_bound':17,
        'scope':'written reset-synchronization and source-block induction for arbitrary cyclic words in W0/W1/U; normalized old-owner eligibility/profile hypotheses NOT discharged universally',
        'trust':'distinct implementation operated by SAME research agent; not external review or formal proof assistant',
        'input_sha256':{x:hashlib.sha256((B/x).read_bytes()).hexdigest() for x in ('mixed_reset_bridge_receipt.json','forward_recovery_and_period_receipt.json')}})
    print(json.dumps({'status':'MIXED_RESET_INDEPENDENT_PASS','queries':I.queries,'W_signed':caps,'common_potential_boundary':3}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent3_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':I.queries,'source_queries':I.queries})
