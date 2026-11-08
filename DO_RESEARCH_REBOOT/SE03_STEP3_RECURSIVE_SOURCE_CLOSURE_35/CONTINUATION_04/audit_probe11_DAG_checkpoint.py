"""Independent exact representation/monotonicity check, not signed sealing."""
import hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();BATCH=int(sys.argv[3]);PHASE=sys.argv[4]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    with (F/'global_probe11_LOW_model.pkl').open('rb') as f:m=pickle.load(f)
    with (F/'global_probe11_DAG_entry.pkl').open('rb') as f:old=pickle.load(f)
    name=f'global_probe11_DAG_{BATCH:02d}.pkl'
    with (F/name).open('rb') as f:now=pickle.load(f)
    on,nn=old['nodes'],now['nodes'];omax={};nmax={}
    def vmax(i,table):return -i-1 if i<0 else table[i]
    for nodes,out in ((on,omax),(nn,nmax)):
        assert len(set(nodes.values()))==len(nodes)
        for i in sorted(nodes):
            l,r=nodes[i];assert l<i and r<i and not(l==r and l<0)
            assert (l<0 or l in nodes) and (r<0 or r in nodes)
            out[i]=max(vmax(l,out),vmax(r,out))
    for i in set(on)&set(nn):assert on[i]==nn[i]
    memo={};comparisons=0
    def dominates(a,b):
        nonlocal comparisons
        if a==-1 or a==b:return True
        if b<0 and -b-1>=vmax(a,omax):return True
        if a<0 and b<0:return -b-1>=-a-1
        key=(a,b)
        if key in memo:return memo[key]
        al,ar=(a,a) if a<0 else on[a];bl,br=(b,b) if b<0 else nn[b]
        answer=dominates(al,bl) and dominates(ar,br);memo[key]=answer;comparisons+=1
        assert len(memo)<1500000
        return answer
    assert len(now['columns'])==len(old['columns'])==m['B_count']
    for a,b in zip(old['columns'],now['columns']):assert dominates(a,b)
    def suffix_max(node,start,width):
        if start>=width:return -1
        if start<=0 or node<0:return vmax(node,nmax)
        l,r=nn[node];half=width//2
        return max(suffix_max(l,start,half),vmax(r,nmax)) if start<half else suffix_max(r,start-half,half)
    unique=set((int(g),r) for g,r in zip(m['roots'],now['columns']));mx=0
    for g,r in unique:
        n=len(m['classes'][g-1]);size=1<<(n-1).bit_length();mx=max(mx,vmax(r,nmax))
        if n<size:assert suffix_max(r,n,size)==0
    assert mx==now['max_D'] and not now['cycle']
    out={'status':'PASS_EXACT_DAG_REPRESENTATION_AND_MONOTONICITY','checkpoint':name,'DAG_nodes':len(nn),'distinct_root_functions':len(unique),
      'literal_B_states':len(now['columns']),'memoized_structural_comparisons':comparisons,'current_max_D':mx,
      'all_padding_zero':True,'dominates_independently_audited_entry':True,'pending_B_columns':len(now['pending']),
      'signed_certificate_claimed':False,'new_funding_proof_claimed':False,'JR35':'OPEN','source_queries':0,'source_engine_calls':0,
      'input_sha256':{p:sha(F/p) for p in (name,'global_probe11_DAG_entry.pkl','independent_probe11_DAG_conversion.json','DECISION_DAG_REPRESENTATION.md')}}
    with (F/f'independent_probe11_DAG_checkpoint_{BATCH:02d}.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps(out),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
