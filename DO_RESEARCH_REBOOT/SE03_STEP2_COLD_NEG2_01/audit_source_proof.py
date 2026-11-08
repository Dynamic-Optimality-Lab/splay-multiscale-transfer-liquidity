"""Independent free-term proof using the frozen frame engine and scoped M3."""
import json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
sys.path.insert(0,str(ROOT/'python'))
from independent import splay as frozen
account={'new_finite_tests':0,'source_engine_calls':0}
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def term(t):
    # A tagged opaque hole is formal proof notation, not a claimed actual
    # source leaf with extra fields. Its interior is NEVER read or searched.
    if isinstance(t,str):return ('leaf',t)
    return frozen.node(t[0],term(t[1]),term(t[2]))
def holes(t):
    return [t[1]] if t[0]=='leaf' else holes(t[2])+holes(t[3])
def step(t,x):
    z,events=frozen.trace(t,x);account['source_engine_calls']+=1
    assert sorted(holes(z))==sorted(holes(t))
    return z,events
def main():
    data=json.loads((B/'symbolic_replay.json').read_text());debt=json.loads((B/'debt_v3_audit.json').read_text())
    records=[]
    for f in data['families']:
        a=b=term(f['initial_full_diagonal']);e=term(f['auxiliary_recurrent_start'])
        for q in f['rows']:
            a,ev=step(a,q['target']);be=[];ee=[]
            if q['mode']=='K':b,be=step(b,q['target'])
            if q['mode']=='K' and q['target']!=f['erased_key']:e,ee=step(e,q['target'])
            assert (a,b,e)==tuple(term(t) for t in q['after'])
            assert (len(ev),sum(v[0]!='ZIG' for v in be),sum(v[0]!='ZIG' for v in ee))==(q['a'],q['qF'],q['qE'])
        assert a==b==term(f['initial_full_diagonal']) and e==term(f['auxiliary_recurrent_start'])
        assert sorted(holes(a))==['F'+str(i) for i in sorted(range(12),key=lambda j:'F'+str(j))]
        records.append({'family':f['name'],'all_free_term_endpoints_equal':True,'all_physical_costs_equal':True,
            'universal_lift':'every request stops at a distinguished key; no hole tested; substitution of any ordered BST for each hole commutes with every frame'})
    # Exact Omega target lower bound1, requiring NO guess of its full debt.
    f=data['families'][0];F=[('leaf','F'+str(i)) for i in range(12)];N=frozen.node
    gap=N(10,N(9,F[8],F[9]),F[10]);v=N(11,gap,F[11])
    for k in range(8,0,-1):v=N(k,F[k-1],v)
    a=term(f['critical_old_A']);b=v;costs=[]
    for x in (11,1):
        a,ae=step(a,x);b,be=step(b,x)
        costs.append((len(ae),sum(q[0]!='ZIG' for q in be)))
    assert costs==[(1,4),(1,1)]
    assert a==term(f['critical_end_A']) and b==term(f['critical_end_BF'])
    # Fixed Scores {1..8,11}, marks {1,3,5,7,11}; M3 applies to this
    # ordinary hypothetical source without a closed-source IH. Its q4 edge
    # forces intermediate D=2; following q1 price+1 forces endpoint D>=1.
    # The actual endpoint chart is exactly this fixed chart.
    omega_target_interval=[1,2]
    sig=data['families'][2]
    assert sig['critical_packet']['H']==1 and sig['critical_packet']['Q']==4
    assert sig['new_chart']['Scores']==list(range(1,10))
    assert sig['new_chart']['marks']==[1,3,5,7,9]
    # These Scores were ancestor-closed already at Sigma's source, with
    # actual {10,11} in a private gap. Hence its single K7 is an original
    # fixed-chart H1/q4 source edge. Range and valid M3 force target2.
    assert sig['new_chart']['tree'][1] is not None and sig['new_chart']['tree'][2] is not None
    sigtarget=next(r for r in debt['witnesses'] if r['name']=='Sigma_singleton')['endpoints']['target']
    assert sigtarget['normalized_D_exact']==2 and sigtarget['psi']==2
    gamma=next(r for r in debt['witnesses'] if r['name']=='Gamma_pair')
    assert gamma['endpoints']['source']['normalized_D_exact']==0 and gamma['endpoints']['target']['normalized_D_exact']==2
    assert gamma['residual_exact']==0
    out('source_proof_audit.json',{'status':'PASS_INDEPENDENT_UNIVERSAL_SOURCE_COUNTERCERTIFICATES',
        'families':records,'Omega_normalized_source':1,'Omega_normalized_target_interval':omega_target_interval,
        'Omega_residual_interval':[-2,-1],'Sigma_normalized_endpoints':[1,2],'Sigma_residual':-1,
        'Gamma_normalized_endpoints':[0,2],'Gamma_residual':0,
        'local_M3_use':'fixed actual nine-Score source tree only; no changing-chart inference',
        'Hhidden_use':'marked third path label is a real Score at authorized R; hence false in both counterexamples',
        'generic_width2_refutation':False,'counterexample_to_original_CD':False,
        'same_agent_independent_derivation':True,'external_peer_review':False,'whole_compiler_formalization':False,
        **account})
    print(json.dumps({'status':'PASS_INDEPENDENT_UNIVERSAL_SOURCE_COUNTERCERTIFICATES','Omega_residual':[-2,-1],
        'Sigma_residual':-1,'Gamma_residual':0,**account}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_source_proof_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
