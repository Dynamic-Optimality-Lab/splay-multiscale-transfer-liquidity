"""Stream complete full-state LOW edges; never materialize a C13 catalogue."""
import hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';sys.path.insert(0,str(F))
import ranked_source_bst as R
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3];BATCH=int(sys.argv[4])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    wp=F/'native13_hard_B_word.json';word=json.loads(wp.read_text())
    with (F/'probe11_source_actions.pkl').open('rb') as f:old=pickle.load(f)
    lift=R.Lift(old);N=R.C[13];nextkey={int(g):x for g,x in word['next_key_by_root'].items()}
    if BATCH==1:z={'g':1,'next_s':0,'partial_rows':[],'root_chunks':{},'source_substitutions':0,'completed_rows':0,'chunks_written':0}
    else:
        with (F/f'ranked13_LOW_build_{BATCH-1:02d}.pkl').open('rb') as f:z=pickle.load(f)
        assert z['status']=='CHECKPOINT'
    g=z['g'];s=z['next_s'];rows=z['partial_rows'];chunks=z['root_chunks'];completed=z['completed_rows'];seq=z['chunks_written'];prior=z['source_substitutions']
    del z
    def flush(g):
        nonlocal rows,completed,seq
        if not rows:return
        seq+=1;name=f'ranked13_LOW_g{g:02d}_chunk{seq:03d}.pkl'
        with (F/name).open('xb') as f:pickle.dump(rows,f,protocol=5)
        chunks.setdefault(g,[]).append({'file':name,'rows':len(rows),'sha256':sha(F/name)})
        completed+=len(rows);rows=[]
    while g<=13 and time.process_time()-START<CAP-4:
        x=nextkey[g];s=max(s,R.OFF[13][g-1]);stop=R.OFF[13][g]
        while s<stop and time.process_time()-START<CAP-4:
            t=R.unrank(13,1,s);local={}
            d=R.depth_at_most(t,x,4)
            if d is not None and d>0:
                out,h,q=lift.action(t,13,x);assert h==(d+1)//2
                local[R.rank_tree(out,1,13),h]=0
            for y in R.near(t):
                mid,h,_=lift.action(t,13,y);assert h==1
                d=R.depth_at_most(mid,x,2)
                if d is not None and d>0:
                    out,h,_=lift.action(mid,13,x);assert h==1
                    local.setdefault((R.rank_tree(out,1,13),2),y)
            rows.extend((s,t,h,y) for (t,h),y in sorted(local.items()));s+=1
            if len(rows)>=160000:flush(g)
        if s==stop:
            flush(g);chunks.setdefault(g,[]);g+=1;s=R.OFF[13][g-1] if g<=13 else N;lift.clear()
        caches=lift.action.cache_info().currsize+R.unrank.cache_info().currsize+R.rank_tree.cache_info().currsize+R.remove_leaf.cache_info().currsize+R.raise_tree.cache_info().currsize
        assert N+646646+len(lift.index)+len(rows)+caches<2000000
        assert completed+len(rows)<=5000000
    out={'status':'COMPLETE_RANKED13_FIXED_WORD_LOW' if g>13 else 'CHECKPOINT','g':g,'next_s':s,'partial_rows':rows,
      'root_chunks':chunks,'source_substitutions':prior+lift.substitutions,'completed_rows':completed,
      'chunks_written':seq,'source_queries':0,'source_engine_calls':0,'N_full_A_states':N,'JR35':'OPEN',
      'input_sha256':{str(p):sha(p) for p in (wp,F/'ranked_source_bst.py',F/'probe11_source_actions.pkl',F/'independent_probe11_source_actions.json')}}
    with (F/f'ranked13_LOW_build_{BATCH:02d}.pkl').open('xb') as f:pickle.dump(out,f,protocol=5)
    report={k:v for k,v in out.items() if k not in ('partial_rows','root_chunks')}
    report.update({'partial_rows':len(rows),'completed_roots':[a for a in chunks if a<g],
      'live_record_upper_bound':N+646646+len(lift.index)+len(rows)+lift.action.cache_info().currsize+R.unrank.cache_info().currsize+R.rank_tree.cache_info().currsize+R.remove_leaf.cache_info().currsize+R.raise_tree.cache_info().currsize})
    with (F/f'ranked13_LOW_build_{BATCH:02d}.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
