"""Complete literal LOW rows for one twelve-key B cycle, streamed by root."""
import functools,hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3];BATCH=int(sys.argv[4])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    bp=F/'native12_tree_basis.pkl';wp=F/'native12_fixed_B_word.json';word=json.loads(wp.read_text())
    assert word['basis_sha256']==sha(bp)
    with bp.open('rb') as f:basis=pickle.load(f)
    T=basis['trees'];offset=basis['root_offsets'];N=len(T);index={t:i for i,t in enumerate(T)}
    with (F/'probe11_source_actions.pkl').open('rb') as f:old=pickle.load(f)
    oldindex={t:i for i,t in enumerate(old['trees'])};nextkey={int(k):v for k,v in word['next_key_by_root'].items()}
    @functools.lru_cache(maxsize=40000)
    def remove(t,y):
        if t is None:return None
        if t[0]==y:assert t[1] is None and t[2] is None;return None
        return (t[0]-(t[0]>y),remove(t[1],y),remove(t[2],y))
    @functools.lru_cache(maxsize=40000)
    def raise_tree(t,y):
        if t is None:return None
        return (t[0]+(t[0]>=y),raise_tree(t[1],y),raise_tree(t[2],y))
    def insert(t,y):
        if t is None:return (y,None,None)
        return (t[0],insert(t[1],y),t[2]) if y<t[0] else (t[0],t[1],insert(t[2],y))
    def leaf(t,x):
        if t[1] is None and t[2] is None:return t[0] if t[0]!=x else None
        return (leaf(t[1],x) if t[1] else None) or (leaf(t[2],x) if t[2] else None)
    calls=0
    @functools.lru_cache(maxsize=30000)
    def lift(s,x):
        nonlocal calls
        t=T[s];y=leaf(t,x);assert y is not None
        a=oldindex[remove(t,y)];xx=x-(x>y)
        result=insert(raise_tree(old['trees'][int(old['destination'][a,xx-1])],y),y);calls+=1
        return index[result],int(old['H'][a,xx-1])
    def depth_at_most(t,x,limit):
        for d in range(limit+1):
            if t[0]==x:return d
            t=t[1] if x<t[0] else t[2]
            if t is None:return None
        return None
    def near(t):
        out=[]
        for c in t[1:]:
            if c:
                out.append(c[0])
                out.extend(d[0] for d in c[1:] if d)
        return out
    if BATCH==1:z={'g':1,'next_s':0,'groups':{},'partial':{},'source_substitutions':0,'source_queries':0}
    else:
        with (F/f'native12_LOW_build_{BATCH-1:02d}.pkl').open('rb') as f:z=pickle.load(f)
        assert z['status']=='CHECKPOINT'
    g=z['g'];s=z['next_s'];groups=z['groups'];rows=z['partial'];initial_sub=z['source_substitutions'];del z
    while g<=12 and time.process_time()-START<CAP-4:
        x=nextkey[g];s=max(s,offset[g-1]);stop=offset[g]
        while s<stop and time.process_time()-START<CAP-4:
            d=depth_at_most(T[s],x,4)
            if d is not None and d>0:
                t,h=lift(s,x);assert h==(d+1)//2;rows.setdefault((s,t,h),0)
            for y in near(T[s]):
                mid,h=lift(s,y);assert h==1
                d=depth_at_most(T[mid],x,2)
                if d is not None and d>0:
                    t,h=lift(mid,x);assert h==1;rows.setdefault((s,t,2),y)
            s+=1
        if s==stop:
            groups[g]=np.array([(a,b,h,y) for (a,b,h),y in sorted(rows.items())],dtype=np.int32).reshape(-1,4)
            rows={};g+=1;s=offset[g-1] if g<=12 else N
            lift.cache_clear();remove.cache_clear();raise_tree.cache_clear()
        live=647000+2*N+sum(len(a) for a in groups.values())+len(rows)+len(oldindex)+remove.cache_info().currsize+raise_tree.cache_info().currsize+lift.cache_info().currsize
        assert live<2000000
    out={'status':'COMPLETE_LITERAL_NATIVE12_FIXED_WORD_LOW' if g>12 else 'CHECKPOINT','g':g,'next_s':s,
      'groups':groups,'partial':rows,'source_substitutions':initial_sub+calls,'source_queries':0,'source_engine_calls':0,
      'basis_sha256':sha(bp),'B_word_sha256':sha(wp),'actual_H1_H2_helpers_preserved':True,'JR35':'OPEN'}
    with (F/f'native12_LOW_build_{BATCH:02d}.pkl').open('xb') as f:pickle.dump(out,f,protocol=5)
    report={k:v for k,v in out.items() if k not in ('groups','partial')}
    report.update({'completed_roots':sorted(groups),'completed_rows':sum(len(a) for a in groups.values()),'partial_rows':len(rows),
      'live_record_upper_bound':647000+2*N+sum(len(a) for a in groups.values())+len(rows)+len(oldindex)+remove.cache_info().currsize+raise_tree.cache_info().currsize+lift.cache_info().currsize})
    with (F/f'native12_LOW_build_{BATCH:02d}.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
