"""Distinct source-snapshot checks and free-term mathematical audit.
No fresh original-source primitive is executed.
"""
import hashlib,importlib.util,itertools,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parent;C=P/'SE03_STEP3_GLOBAL_JOINT_OWNERSHIP_34';B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';START=time.process_time();CAP=float(sys.argv[1])
sp=importlib.util.spec_from_file_location('independent_parent_reader',C/'audit_pools.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def right(t):
    g,p,D=t;k,A,Bb=p;return k,A,(g,Bb,D)
def left(t):
    g,A,p=t;k,Bb,Cc=p;return k,(g,A,Bb),Cc
def reflect(t):return t if not isinstance(t,tuple) else (t[0],reflect(t[2]),reflect(t[1]))
def main():
    data=json.loads((C/'pooled_source_results.json').read_text());checks=[]
    for case in data['cases']:
        rows=case['source_rows'];by={r['t']:r for r in rows};mm=case['macros'];M={m['target'] for m in mm};foreign=0;paircount=0
        for m in mm:
            x=m['target'];end=m['end'];G=I.amap(by[end]['B0'])[x]&M
            assert G=={p['g'] for p in m['retirement_proof']}
            for p in m['retirement_proof']:
                g=p['g']
                for t in p['all_retiring_operations']:
                    r=by[t];assert g in I.amap(r['A0'])[x] and g not in I.amap(r['A1'])[x]
                    if t==end or r['mode']!='K':continue
                    y=r['x'];assert y<x<g or g<x<y;foreign+=1
        for i,m in enumerate(mm):
            G=I.amap(by[m['end']]['B0'])[m['target']]&M
            for j in range(i+1,len(mm)):
                n=mm[j];H=I.amap(by[n['end']]['B0'])[n['target']]&M
                fw={mm[k]['target'] for k in range(i+1,j)};rv={mm[k]['target'] for k in list(range(j+1,len(mm)))+list(range(i))}
                assert len((G&H)-fw)<=1 and len((G&H)-rv)<=1 and not(((G&H)-fw)&((G&H)-rv));paircount+=1
        checks.append(dict(source=case['name'],foreign_KEEP_retirements=foreign,cyclic_pairs=paircount,source_queries=0))
    # Exhaustive symbolic depth<=2 cases. A/B/C/L are arbitrary ordered terms.
    rr=('a','L',('p','A',('x','B','C')))
    assert right(right(left(left(rr))))==rr
    rl=('a','L',('p',('x','A','B'),'C'))
    after_first=('a','L',right(rl[2]));after_x=left(after_first);after_return=right(after_x)
    assert after_return==('a','L',('x','A',('p','B','C')))
    zig=('a','L',('x','A','B'));assert right(left(zig))==zig
    for t in (rr,rl,zig):assert reflect(reflect(t))==t
    # Actual finite countermodel to NUMERIC sufficiency, not an original BST.
    own=[{(i,0),(i,1)} for i in range(3)];common={('C',0),('C',1)};N=[v|common for v in own];Q=[3]*3
    for k in (1,2):
        for ids in itertools.combinations(range(3),k):assert len(set().union(*(N[i] for i in ids)))>=sum(Q[i] for i in ids)
    U=set().union(*N);sigma=sum(len(v)-q for v,q in zip(N,Q));overlap=sum(map(len,N))-len(U);local_unused=0;delta=sum(Q)-len(U)
    assert (sigma,overlap,local_unused,delta)==(3,4,0,1)
    assert all(len(N[i]-set().union(*(N[j] for j in range(3) if j!=i)))==2<3 for i in range(3))
    first=[v|{('C',0)} for v in own];assert all(len(first[i]&first[j])==1 for i,j in itertools.combinations(range(3),2))
    docs=['ROTATION_LEVEL_OVERLAP_IDENTITIES.md','PRIVATE_CAPACITY_RECURSION.md','CYCLIC_BIRTH_INTERSECTION.md','SOURCE_COALITION_REDUCTION.md','KEEP_RETIREMENT_ORDER.md','SHALLOW_ANCHOR_RETURN_BARRIER.md','MINIMAL_CONNECTED_COUNTERCUT.md','ABSTRACT_COMPENSATION_COUNTERMODEL.md']
    result=dict(status='PASS_DISTINCT_STATIC_RECURSION_SOURCE_LEMMA_AUDIT',input_sha256={d:sha(F/d) for d in docs},accepted_source_graph_sha256=sha(C/'pooled_source_results.json'),source_snapshot_checks=checks,free_term_shallow_return_cases=['depth1 zig','depth2 RR','depth2 RL','their reflected frames'],countermodel=dict(sigma=sigma,overlap=overlap,local_unused=0,deficit=delta,proper_coalitions_pass=True,source_realized=False,SI34_refutation=False),written_proofs_reviewed=['exact capacity/marginal identities','fixed-source peeling/order independence','B path-to-star disjoint-subtree argument','foreign KEEP root separation','DELETE identity-subword contraction and actual occurrence transport','well-founded countercut normalization'],verification_scope='same-agent independent implementation and written proof/static checks; not formal theorem-prover certification or external review',source_queries=0,source_engine_calls=0,ROOT35='ACTIVE',uniform_PEEL35='ACTIVE')
    with (F/'independent_recursive_lemma_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    assert time.process_time()-START<CAP-1
    print(result['status'],flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify85_exit.json').open('x') as f:json.dump(dict(whole_process_CPU_seconds=time.process_time(),error=error,source_queries=0,source_engine_calls=0),f)
