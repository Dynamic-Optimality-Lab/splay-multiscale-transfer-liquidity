"""Literal full-tree LOW constraints for ONE fixed original B cycle.

Dense coefficients are indexed by the injective Catalan full-tree rank.
Chunks are streamed; no finite quotient and no new source-kernel calls.
"""
import hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
sys.path.insert(0,str(F));import ranked_source_bst as R
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3];BATCH=int(sys.argv[4])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    bp=max(F.glob('ranked13_LOW_build_*.pkl'));wp=F/'native13_hard_B_word.json'
    with bp.open('rb') as f:model=pickle.load(f)
    assert model['status']=='COMPLETE_RANKED13_FIXED_WORD_LOW' and not model['partial_rows']
    chunks=model['root_chunks'];word=json.loads(wp.read_text());N=R.C[13]
    nxt={int(g):x for g,x in word['next_key_by_root'].items()}
    phase_roots=[R.unrank(13,1,r['B_source'])[0] for r in word['rows']]
    qmap={g:r['Q'] for g,r in zip(phase_roots,word['rows'])}
    assert len(qmap)==13 and sum(qmap.values())==29
    if BATCH==1:
        D=np.zeros(N,dtype=np.int32);parent=np.full(N,-1,dtype=np.int32)
        pending=list(phase_roots);processed=updates=0
    else:
        with (F/f'ranked13_LOW_search_{BATCH-1:02d}.pkl').open('rb') as f:z=pickle.load(f)
        assert z['status']=='CHECKPOINT';D=z['D'];parent=z['parent'];pending=z['pending'];processed=z['processed'];updates=z['updates']
        del z
    stopped=False;live_peak=2*N
    while pending and time.process_time()-START<CAP-4:
        g=pending[0];x=nxt[g];changed=False
        for chunk in chunks[g]:
            cp=F/chunk['file'];assert sha(cp)==chunk['sha256']
            with cp.open('rb') as f:rows=pickle.load(f)
            assert len(rows)==chunk['rows']
            for k in range(0,len(rows),15000):
                a=np.asarray(rows[k:k+15000],dtype=np.int32)
                # A single source has distinct (destination,H) rows. Sorting
                # by destination and descending score gives one best witness.
                scores=D[a[:,0]]+qmap[g]-2*a[:,2]
                order=np.lexsort((-scores,a[:,1]));dest=a[order,1]
                take=np.r_[True,dest[1:]!=dest[:-1]];ix=order[take]
                targets=a[ix,1];values=scores[ix];better=values>D[targets]
                targets=targets[better];ii=ix[better];values=values[better]
                if len(targets):
                    D[targets]=values;parent[targets]=a[ii,0];updates+=len(targets);changed=True
                live=2*N+len(rows)+20*len(a)+R.unrank.cache_info().currsize+1000
                live_peak=max(live_peak,live);assert live<2000000
            del rows
        pending.pop(0);processed+=1
        if changed and x not in pending:pending.append(x)
        if int(D.max())>32:
            stopped=True;break
    mins={g:int(D[R.OFF[13][g-1]:R.OFF[13][g]].min()) for g in range(1,14)}
    maxs={g:int(D[R.OFF[13][g-1]:R.OFF[13][g]].max()) for g in range(1,14)}
    h2=min(4-qmap[g]+mins[nxt[g]]-maxs[g] for g in qmap)
    h3=min(6-qmap[g]+mins[nxt[g]]-maxs[g] for g in qmap)
    status='LARGE_WIDTH_NEEDS_LITERAL_CYCLE_RECONSTRUCTION' if stopped else ('CHECKPOINT' if pending else 'COMPLETE_FIXED_WORD_LOW_SIGNS')
    result={'status':status,'D':D,'parent':parent,'pending':pending,'processed':processed,'updates':updates,
      'source_queries':0,'source_engine_calls':0,'JR35':'OPEN','N_full_A_states':N,
      'max_D':int(D.max()),'H_ge_2_envelope':h2,'H_ge_3_envelope':h3,'live_record_upper_bound':live_peak,
      'input_sha256':{str(p):sha(p) for p in (bp,wp,F/'ranked_source_bst.py',F/'search_ranked13_LOW.py')}}
    with (F/f'ranked13_LOW_search_{BATCH:02d}.pkl').open('xb') as f:pickle.dump(result,f,protocol=5)
    report={k:v for k,v in result.items() if k not in ('D','parent')}
    with (F/f'ranked13_LOW_search_{BATCH:02d}.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
