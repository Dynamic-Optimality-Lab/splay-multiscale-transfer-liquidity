"""Static pointwise structural bound on OLD, already complete debt tables.
No new source relation, source tree path, splay or root query is generated.
The finite grammar's original uniform lifting theorem is inherited, not
reproved or replaced by finite population samples. A passing arithmetic
bound applies to that grammar ONLY; it is not the missing return bridge.
"""
import json,time,collections,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;OLD=P/'SE03_STEP2_UNARY_A_LIFT_14'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def marked_degrees(t,M):
    deg={m:0 for m in M}
    def visit(n,parent):
        if isinstance(n,str):return
        if n[0] in M:
            if parent is not None:deg[parent]+=1
            parent=n[0]
        visit(n[1],parent);visit(n[2],parent)
    visit(t,None);return deg
def main():
    grammar=read(OLD/'branch_grammar2.json');A=grammar['states'];roots=collections.Counter(t[0]//1000 for t in A)
    table=read(OLD/'branch_core11_mask0.json');offset=0;maxgap=-99;witness=None;counts=collections.Counter();bad=[]
    for bi,t in enumerate(table['BF_trees']):
        deg=marked_degrees(t,set(table['marks']));E=sum(max(v-2,0) for v in deg.values())
        n=roots[table['marks'].index(t[0])+1];dd=table['debt'][offset:offset+n]
        gap=max(dd)-E;counts[(E,max(dd))]+=1
        if gap>maxgap:maxgap=gap;witness={'BF_index':bi,'BF_tree':t,'E6':E,'maximum_D6':max(dd),'debt_offset':offset,'root_class_size':n}
        if gap>1:bad.append({'BF_index':bi,'E6':E,'max_D6':max(dd),'debt_offset':offset})
        offset+=n
    assert offset==len(table['debt'])
    out('inherited_D6_excess_bound.json',{'status':'COMPLETE_STATIC_TABLE_ANALYSIS','new_source_queries':0,
        'pointwise_candidate':'D6<=E6+1','candidate_holds_on_entire_inherited_grammar':not bad,
        'maximum_D6_minus_E6':maxgap,'maximizing_saved_state_block':witness,
        'violating_BF_blocks':bad,'E6_D6max_counts':[{'E6':e,'max_D6':d,'BF_blocks':n} for (e,d),n in sorted(counts.items())],
        'states_analyzed':offset,'BF_states':len(table['BF_trees']),
        'role':'pointwise property of the old COMPLETE grammar; NO new source realizability or seven-key terminal source theorem inferred',
        'input_sha256':{str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (OLD/'branch_grammar2.json',OLD/'branch_core11_mask0.json')}})
    print(json.dumps({'status':'STATIC_D6_BOUND_ANALYSIS','candidate_holds':not bad,'max_D6_minus_E6':maxgap,'violating_BF_blocks':len(bad),'source_queries':0}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_algebra_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
