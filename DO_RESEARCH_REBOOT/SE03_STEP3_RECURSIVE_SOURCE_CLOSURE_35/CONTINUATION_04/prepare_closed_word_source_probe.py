"""Actual B recurrent trajectories, for exact full-A negative-cycle search."""
import hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def balanced(lo,hi):
    if lo>hi:return None
    m=(lo+hi)//2;return (m,balanced(lo,m-1),balanced(m+1,hi))
def main():
    with (F/'probe11_source_actions.pkl').open('rb') as f:z=pickle.load(f)
    au=json.loads((F/'independent_probe11_source_actions.json').read_text());assert au['input_sha256'][str(F/'probe11_source_actions.pkl')]==sha(F/'probe11_source_actions.pkl')
    words=[[1,11,2,10,3,9,4,8,5,7,6],[1,6,2,7,3,8,4,9,5,10,11],
      [6,1,11,3,9,5,7,2,10,4,8],[1,11,3,9,5,7,2,10,4,8,6],
      [6,3,1,2,4,5,9,7,8,10,11],[1,11,3,9,5,7,10],
      [y for x in [1,11,3,9,5,7,2,10,4,8] for y in (x,6)],
      [y for x in [3,5,7,9,10,11] for y in (x,1)]]
    index={t:i for i,t in enumerate(z['trees'])};start=index[balanced(1,11)];models=[];skipped=[]
    for w in words:
        seen={};cur=start;boundaries=[];copies=[]
        for k in range(128):
            if cur in seen:break
            seen[cur]=k;boundaries.append(cur);rows=[]
            for x in w:
                nxt=int(z['destination'][cur,x-1]);rows.append((cur,x,int(z['Q'][cur,x-1]),nxt));cur=nxt
            copies.append(rows)
        else:skipped.append({'W':w,'reason':'NO_PERIOD_WITHIN_CONSTRUCTION_CAP'});continue
        pre=seen[cur];cycle=sum(copies[pre:],[])
        assert cycle[-1][3]==cycle[0][0]
        if len(cycle)>31:skipped.append({'W':w,'reason':'SOURCE_STATE_CAP_AT_THIS_PHASE_COUNT','period_length':len(cycle)});continue
        assert all(z['roots'][s]!=x for s,x,q,t in cycle)
        models.append({'W':w,'B_initial_common':start,'reaching_KEEP_word':w*pre,'phase_rows':cycle,
          'genuine_support':sorted(set(w)),'phase_count':len(cycle),'actual_B_period_Q':sum(q for s,x,q,t in cycle),
          'warming_word_copies':pre,'period_word_copies':len(copies)-pre})
    out={'models':models,'skipped':skipped,'source_table_sha256':sha(F/'probe11_source_actions.pkl'),
      'source_queries':0,'source_engine_calls':0,'purpose':'actual full-source negative cycles; no passing promotion'}
    with (F/'closed_word_source_probe_models.pkl').open('xb') as f:pickle.dump(out,f,protocol=5)
    report={'models':[{k:v for k,v in m.items() if k!='phase_rows'} for m in models],'skipped':skipped,
      'source_queries':0,'JR35':'OPEN'}
    with (F/'closed_word_source_probe_models.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof228_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
