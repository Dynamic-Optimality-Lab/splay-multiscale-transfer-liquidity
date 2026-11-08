"""Independent STATIC arithmetic/indexing checks, no source execution.
Recompute the NEW root-bound and weakened q5 law from the old certified
arrays; use the alternative leaf/branch identity for E. Exact current
manuscript hashes are pinned, but mathematical induction is not claimed
formally verified by these arithmetic tests.
"""
import json,time,collections,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;OLD=P/'SE03_STEP2_UNARY_A_LIFT_14'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    g=read(OLD/'branch_grammar2.json');c=read(OLD/'branch_core11_mask0.json');M=c['marks'];A=g['states'];T=c['BF_trees']
    rootA={r:[i for i,t in enumerate(A) if t[0]==1000*r] for r in range(1,7)}
    values={};o=0
    for b,t in enumerate(T):
        for a in rootA[M.index(t[0])+1]:values[(b,a)]=c['debt'][o];o+=1
    assert o==len(c['debt']);root_bad=0;maxdiff=-100;states=0
    for b,t in enumerate(T):
        if t[0]!=7:continue
        children={m:[] for m in M}
        def visit(n,parent):
            if isinstance(n,str):return
            if n[0] in children:
                if parent is not None:children[parent].append(n[0])
                parent=n[0]
            visit(n[1],parent);visit(n[2],parent)
        visit(t,None)
        L=sum(not v for v in children.values());branches=sum(len(v)>=2 for v in children.values())
        E7=L-branches-1+int(len(children[7])>=2)
        for a in rootA[4]:
            diff=values[(b,a)]-E7;maxdiff=max(maxdiff,diff);root_bad+=int(diff>1);states+=1
    assert root_bad==0 and maxdiff==1
    q5_margins={};violations={}
    for h in (1,2):
        rel=collections.defaultdict(list)
        for a,x,z in g['H'+str(h)]:rel[(A[a][0]//1000,x)].append((a,z))
        smallest=99;bad=0
        for s,t,key,q in c['BF_relation']:
            if q!=5:continue
            for a,z in rel[(M.index(T[s][0])+1,M.index(key)+1)]:
                margin=2*h-q+values[(t,z)]-values[(s,a)];smallest=min(smallest,margin);bad+=int(margin < -1)
        assert smallest==-1 and bad==0;q5_margins[h]=smallest;violations[h]=bad
    b=read(B/'six_key_boundary_analysis.json');bad2=[z for z in b['all_terminal_bridge_violations'] if z['return_H_lower_bound']<=2 and z['margin']+2*(2-z['return_H_lower_bound'])<0]
    assert len(bad2)==2 and {z['A_index'] for z in bad2}=={381} and {z['BF_index'] for z in bad2}=={1060,1063}
    u=read(B/'upper_seven_form_arithmetic.json');p=u['path_lower_potential'];E=u['E']
    for s,t,key,q,sig in u['source_derived_edges']:assert sig==2-q+E[t]-E[s] and sig+p[s]>=p[t]
    assert all(p[s]+v>=0 for s,v in u['first_lower_sigma_min'].items())
    w=read(B/'transient_W105_certificate.json');old=read(P/'SE03_STEP3_FIRST_RETURN_7_REPAYMENT_31/prefix_first_return_countercertificate_v2.json')
    assert w['closed_block_W105']==old['closed_block_W'][:42]+[['K',13],['K',9],['K',11],['K',9]]+old['closed_block_W'][42:]
    assert w['closed_block_Q']==82+6 and w['closed_block_genuine_KEEPs']==58+4 and w['terminal_signed_balance']==-1+sum(w['inserted_sigma'])==1
    assert w['terminal_debt']==0 and not w['is_principal_FR32_counterexample']
    names=['PRE_ACTIVATION_CARRY_THEOREM.md','UPPER_ONLY_BARRIER.md','TRANSIENT_CARRY_TWO_CONTROL.md','SIX_KEY_PASSIVE_LEAF_BRIDGE.md']
    out('static_independent_audit.json',{'status':'PASS_NEW_STATIC_BOUND_ARRAY_GRAPH_AND_WORD_ARITHMETIC','new_source_queries':0,
        'no9_root_bound_states':states,'root_bound_max_difference':maxdiff,'q5_singleton_min_LOW_margin':q5_margins,
        'actual_H2_terminal_static_exceptions':bad2,'upper_graph_edges_checked':12,'W105_terminal_debt':0,
        'source_inductions_formally_checked':False,'seven_form_source_replay':False,'whole_closure_replay':False,
        'external_audit':False,'trust':'same research agent, separate static implementation; old source relation/grammar reused unchanged',
        'input_manuscript_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in names}})
    print(json.dumps({'status':'INDEPENDENT_STATIC_AUDIT_PASS','queries':0,'no9_root_bound_states':states,'H2_bad_sectors':2,'principal_CARRY1':'OPEN'}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
