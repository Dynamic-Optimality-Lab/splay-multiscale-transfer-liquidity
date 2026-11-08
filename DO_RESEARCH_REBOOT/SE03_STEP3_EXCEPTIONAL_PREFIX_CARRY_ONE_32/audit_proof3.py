"""Static terminal-root bound on the inherited complete six-key debt array.
No new source query or operation; marked-tree degree arithmetic only.
"""
import json,time,collections
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;OLD=P/'SE03_STEP2_UNARY_A_LIFT_14'
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    g=json.loads((OLD/'branch_grammar2.json').read_text());c=json.loads((OLD/'branch_core11_mask0.json').read_text());M=set(c['marks'])
    roots=collections.Counter(t[0]//1000 for t in g['states']);o=0;maxdiff=-99;bad=[];checked=0;witness=None
    for b,t in enumerate(c['BF_trees']):
        n=roots[c['marks'].index(t[0])+1];dd=c['debt'][o:o+n]
        if t[0]==7:
            deg={x:0 for x in M}
            def visit(v,p):
                if isinstance(v,str):return
                if v[0] in M:
                    if p is not None:deg[p]+=1
                    p=v[0]
                visit(v[1],p);visit(v[2],p)
            visit(t,None);E=sum(max(d-2,0) for d in deg.values());Efull=E+int(deg[7]>=2);diff=max(dd)-Efull;checked+=n
            if diff>maxdiff:maxdiff=diff;witness={'BF_index':b,'BF_tree':t,'E6':E,'root_degree':deg[7],'E7_with_inactive9_child':Efull,'max_D6':max(dd),'debt_offset':o}
            if diff>1:bad.append({'BF_index':b,'difference':diff})
        o+=n
    assert o==len(c['debt'])
    out('old_chart_terminal_root_bound.json',{'status':'COMPLETE_STATIC_TERMINAL_ROOT_ANALYSIS','new_source_queries':0,
        'candidate':'D6(root7)<=E7(with extra inactive9 child)+1','candidate_holds':not bad,'maximum_difference':maxdiff,
        'states_checked':checked,'violating_BF_blocks':bad,'maximum_witness':witness,
        'scope':'necessary old six-key syntax; not a new source realization or automatic q5 packet-boundary license'})
    print(json.dumps({'status':'ROOT_BOUND_ANALYSIS','holds':not bad,'maximum_difference':maxdiff,'bad_blocks':len(bad),'queries':0}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_proof3_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
