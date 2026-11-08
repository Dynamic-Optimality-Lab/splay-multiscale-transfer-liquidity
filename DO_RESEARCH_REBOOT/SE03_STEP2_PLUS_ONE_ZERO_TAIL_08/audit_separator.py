"""Inspect and prove a candidate stronger NEG2 target source separator."""
import collections,json,time
from pathlib import Path
from audit_seeds import c,s
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
def main():
    data=json.loads((B/'zero_closure.json').read_text());shapes=collections.Counter();B4={};other=[]
    for i,r in enumerate(data['records']):
        b=freeze(r['BF']);L=c.leaves(b);degree=sum(v==b[0] for v in s.parentmap(b).values())
        shapes[L,degree]+=1
        if L==4:
            B4[b]=s.parentmap(b)
            if degree in (1,4):other.append(i)
    report={'status':'ROOT_DEGREE_SEPARATES_NEG2' if not other else 'A_DEPENDENT_NEG2_SEPARATION_REQUIRED',
        'state_shapes':[{'leaves':k[0],'marked_root_degree':k[1],'frames':v} for k,v in sorted(shapes.items())],
        'four_leaf_distinct_BF_contexts':len(B4),'four_leaf_NEG2_root_degree_candidates':other,
        'candidate_invariant':'cold NEG2 target has L4 and root marked degree1 or4',
        'source_engine_calls':0,'new_finite_tests':0}
    out('separator.json',report);print(json.dumps(report),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_separator_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'new_finite_tests':0})
