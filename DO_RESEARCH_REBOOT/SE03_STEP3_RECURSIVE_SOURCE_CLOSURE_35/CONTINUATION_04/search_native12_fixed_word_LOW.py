"""Literal larger-support countercycle search on complete H1/H2 rows."""
import hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    bp=F/'native12_tree_basis.pkl';mp=F/'native12_LOW_build_01.pkl';wp=F/'native12_fixed_B_word.json'
    word=json.loads(wp.read_text())
    with bp.open('rb') as f:basis=pickle.load(f)
    with mp.open('rb') as f:m=pickle.load(f)
    assert m['status']=='COMPLETE_LITERAL_NATIVE12_FIXED_WORD_LOW'
    assert m['basis_sha256']==sha(bp) and m['B_word_sha256']==sha(wp)
    N=basis['source_state_count'];offset=basis['root_offsets'];roots=np.repeat(np.arange(1,13,dtype=np.int8),basis['root_counts'])
    models={}
    for br in word['rows']:
        g=basis['trees'][br['B_source']][0];x=br['KEEP'];r=m['groups'][g]
        assert np.all((offset[g-1]<=r[:,0])&(r[:,0]<offset[g])) and np.all((offset[x-1]<=r[:,1])&(r[:,1]<offset[x]))
        r=r[np.argsort(r[:,1],kind='stable')];begin=np.r_[0,np.flatnonzero(r[1:,1]!=r[:-1,1])+1];targets=r[begin,1]
        models[g]=(r,begin,targets,x,br['Q']);m['groups'][g]=r
    D=np.zeros(N,dtype=np.int32);parent=np.full(N,-1,dtype=np.int32);ph=np.zeros(N,dtype=np.int8);py=ph.copy()
    updates=sweeps=0;cycle=None;done=False
    def find(a):
        seen={};trail=[]
        while a>=0 and a not in seen:
            seen[a]=len(trail);trail.append(a);a=int(parent[a])
        if a<0:return None
        back=trail[seen[a]:];edges=[];cost=0
        for t in back:
            s=int(parent[t]);g=int(roots[s]);x=models[g][3];q=models[g][4];h=int(ph[t]);y=int(py[t])
            assert int(roots[t])==x
            w=2*h-q;cost+=w
            edges.append({'A_source':s,'A_target':t,'source_root':g,'KEEP':x,'H':h,'Q':q,
              'A_word':([['D',y]] if y else [])+[['K',x]],'weight':w})
        return {'edges':list(reversed(edges)),'weight':cost} if cost<0 else None
    while time.process_time()-START<CAP-3 and sweeps<10000:
        changed=0
        for br in word['rows']:
            g=basis['trees'][br['B_source']][0];r,begin,targets,x,q=models[g];R=len(r)
            score=D[r[:,0]].astype(np.int64)+q-2*r[:,2]
            packed=(score+100000)*R+np.arange(R,dtype=np.int64)
            chosen=np.maximum.reduceat(packed,begin);value=(chosen//R-100000).astype(np.int32);rows=(chosen%R).astype(np.int32)
            bad=value>D[targets];tt=targets[bad];which=rows[bad]
            if len(tt):
                D[tt]=value[bad];parent[tt]=r[which,0];ph[tt]=r[which,2];py[tt]=r[which,3];changed+=len(tt)
                cycle=find(int(tt[int(np.argmax(value[bad]))]))
                if cycle:break
        updates+=changed;sweeps+=1
        if cycle:break
        if not changed:done=True;break
    maximum=int(D.max());qmax=max(r['Q'] for r in word['rows'])
    out={'status':'ORIGINAL_NATIVE12_LOW_NEGATIVE_CYCLE_CANDIDATE' if cycle else ('COMPLETE_FIXED_WORD_LOW_NO_NEGATIVE_CYCLE' if done else 'CHECKPOINT'),
      'D':D,'parent_A_source':parent,'parent_H':ph,'parent_helper':py,'sweeps':sweeps,'coefficient_updates':updates,'max_D':maximum,
      'cycle':cycle,'HIGH_H3_coarse_minimum_margin':6-qmax-maximum,
      'physical_anchor_count':12,'actual_B_period':word['word'],'source_A_states':N,'source_LOW_rows':sum(len(r) for r in m['groups'].values()),
      'source_queries':0,'source_engine_calls':0,'JR35':'OPEN','positive_result_is_bounded_only':True,
      'independent_status':'PENDING','input_sha256':{str(p):sha(p) for p in (bp,mp,wp)}}
    with (F/'native12_fixed_word_LOW_result.pkl').open('xb') as f:pickle.dump(out,f,protocol=5)
    report={k:v for k,v in out.items() if k not in ('D','parent_A_source','parent_H','parent_helper')}
    with (F/'native12_fixed_word_LOW_result.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
