"""Independent entire H1 grammar with LAST-leaf substitution and HIGH H>=2."""
import functools,hashlib,importlib.util,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def leaves(t):
    if t[1] is None and t[2] is None:return [t[0]]
    return ([] if t[1] is None else leaves(t[1]))+([] if t[2] is None else leaves(t[2]))
def lower(t,y):
    if t is None:return None
    if t[0]==y:assert not t[1] and not t[2];return None
    return (t[0]-(t[0]>y),lower(t[1],y),lower(t[2],y))
@functools.lru_cache(maxsize=30000)
def raise_tree(t,y):
    if t is None:return None
    return (t[0]+(t[0]>=y),raise_tree(t[1],y),raise_tree(t[2],y))
def insert(t,y):
    if t is None:return (y,None,None)
    if y<t[0]:return (t[0],insert(t[1],y),t[2])
    return (t[0],t[1],insert(t[2],y))
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def main():
    global V
    bp=F/'native12_tree_basis.pkl';cp=F/'native12_HARD_word_LOW_result.pkl';wp=F/'native12_hard_B_word.json'
    with bp.open('rb') as f:basis=pickle.load(f)
    with cp.open('rb') as f:result=pickle.load(f)
    with (F/'probe11_source_actions.pkl').open('rb') as f:old=pickle.load(f)
    word=json.loads(wp.read_text());T=basis['trees'];D=result['D'];index={t:i for i,t in enumerate(T)};oi={t:i for i,t in enumerate(old['trees'])}
    assert len(index)==len(T)==208012 and len(D)==len(T) and int(D.min())==0 and int(D.max())==1
    C=[1]
    for n in range(1,13):C.append(sum(C[i]*C[n-1-i] for i in range(n)))
    assert C[12]==len(T) and basis['root_counts']==[C[i]*C[11-i] for i in range(12)]
    def ordered(u,lo,hi):
        if u is None:return 0
        k,l,r=u;assert lo<=k<=hi
        return 1+ordered(l,lo,k-1)+ordered(r,k+1,hi)
    for t in T:assert ordered(t,1,12)==12
    sp=importlib.util.spec_from_file_location('N12_hard_B_distinct',B/'audit_verify79.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    b=V.Mutable(T[word['rows'][0]['B_source']]);qmap={};nextkey={};n_B=0
    for r in word['rows']:
        assert tup(b.snapshot())==T[r['B_source']];g=b.snapshot()[0]
        _,q,_=b.splay(r['KEEP'],False);assert q==r['Q'] and tup(b.snapshot())==T[r['B_target']]
        qmap[g]=q;nextkey[g]=r['KEEP'];n_B+=1
    assert tup(b.snapshot())==T[word['rows'][0]['B_source']] and n_B==12 and sum(qmap.values())==26 and max(qmap.values())<=3
    count=0
    for s,t in enumerate(T):
        g=t[0];x=nextkey[g];u=t;depth=None
        for d in range(3):
            if u[0]==x:depth=d;break
            u=u[1] if x<u[0] else u[2]
            if u is None:break
        if depth is None:continue
        assert depth in (1,2)
        y=next(y for y in reversed(leaves(t)) if y!=x);a=oi[lower(t,y)];xx=x-(x>y)
        assert int(old['H'][a,xx-1])==1
        end=insert(raise_tree(old['trees'][int(old['destination'][a,xx-1])],y),y);target=index[end]
        assert 2-qmap[g]+int(D[target])-int(D[s])>=0;count+=1
        assert time.process_time()-START<CAP-1
    off=basis['root_offsets'];mins={g:int(D[off[g-1]:off[g]].min()) for g in range(1,13)}
    maxs={g:int(D[off[g-1]:off[g]].max()) for g in range(1,13)}
    high=min(4-qmap[g]+mins[nextkey[g]]-maxs[g] for g in range(1,13));assert high>=0
    r={'status':'PASS_COMPLETE_NATIVE12_HARD_WORD_SOURCE_SIGNS','full_A_states':len(T),'H1_source_rows':count,
      'H_ge_2_minimum_margin':high,'D_range':[0,1],'c':'min(H,2)','conservative_Bank25_working_bound':5,
      'new_B_source_kernel_checks':V.CALLS,'A_source_bindings':'independent LAST non-target leaf into accepted complete native11, not producer FIRST leaf',
      'enumeration_completeness':'all C12 distinct valid ordered twelve-key BSTs; every depth1/2 target recognized',
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'scope':'one exact twelve-genuine-key B cycle, arbitrary original A helpers on the twelve anchors and rigid off-path hangers',
      'all_twelve_key_words_or_arbitrary_support':False,'JR35':'OPEN','reservation':'DEFERRED',
      'input_sha256':{str(p):sha(p) for p in (bp,cp,wp,F/'probe11_source_actions.pkl',F/'independent_probe11_source_actions.json',B/'OFF_PATH_LEAF_SOURCE_LIFT.md')}}
    with (F/'independent_native12_hard_word.json').open('x',encoding='utf8') as f:json.dump(r,f,indent=2)
    print(json.dumps({k:v for k,v in r.items() if k!='input_sha256'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        n=0 if V is None else V.CALLS
        with (B/'audit_verify145_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':n,'source_engine_calls':n},f)
