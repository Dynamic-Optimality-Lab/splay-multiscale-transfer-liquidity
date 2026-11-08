"""Find exact THREE-event source paths behind failed free-endpoint envelopes.
All primitives were independently certified. No new engine query, synthetic
endpoint edge, or source counterexample claim follows without a real cycle.
"""
import hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1];sys.path.insert(0,str(F));B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
from probe11_decision_dag import DAG
CAP=float(sys.argv[1]);START=time.process_time();NATIVE_BATCH=7
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    with (F/'global_probe11_LOW_model.pkl').open('rb') as f:m=pickle.load(f)
    with (F/'probe11_source_actions.pkl').open('rb') as f:primitive=pickle.load(f)
    cname=f'global_probe11_DAG_{NATIVE_BATCH:02d}.pkl'
    with (F/cname).open('rb') as f:z=pickle.load(f)
    n=m['A_count'];dag=DAG(z['nodes'],z['nextid']);AD=primitive['destination'];H=primitive['H'];classes=m['classes'];local=m['local'];roots=m['roots']
    # Producer-side exact ranges; final certificates require their own audit.
    mm={}
    def bounds(i,n,width):
        if i<0:return (-i-1,-i-1)
        key=(i,n,width)
        if key in mm:return mm[key]
        l,r=dag.nodes[i];half=width//2
        a=bounds(l,min(n,half),half)
        if n<=half:answer=a
        else:
            b=bounds(r,n-half,half);answer=(min(a[0],b[0]),max(a[1],b[1]))
        mm[key]=answer;return answer
    ranges={}
    for g,p in set((int(g),p) for g,p in zip(roots,z['columns'])):
        k=len(classes[g-1]);ranges[g,p]=bounds(p,k,1<<(k-1).bit_length())
    mn=np.array([ranges[int(g),p][0] for g,p in zip(roots,z['columns'])],dtype=np.int16);mx=np.array([ranges[int(g),p][1] for g,p in zip(roots,z['columns'])],dtype=np.int16)
    margin=6-m['B_Q'].astype(np.int16)+mn[m['B_destination']]-mx[:,None];genuine=roots[:,None]!=(np.arange(11)+1)[None,:]
    bad=np.argwhere(genuine&(margin<0));work={}
    for b,x0 in bad.tolist():work.setdefault((int(roots[b]),z['columns'][b]),[]).append((b,x0+1))
    rows=[];proofs=[];compositions=0
    for (g,profile),bedges in work.items():
        initial=dag.vector(profile,len(classes[g-1]));values=np.full((4,n),-1000000,dtype=np.int32)
        active=initial>0;values[0,classes[g-1][active]]=initial[active]
        parent=np.full((4,n),-1,dtype=np.int32);prevh=np.zeros((4,n),dtype=np.int8);lastkey=prevh.copy()
        # H0 source values cannot violate: 6-Q>=1 and all target debt>=0.
        for total in (1,2,3):
            for k in range(1,total+1):
                hprev=total-k;finite=values[hprev]>-500000
                for y0 in range(11):
                    ss=np.flatnonzero(finite&(H[:,y0]==k));compositions+=len(ss)
                    if not len(ss):continue
                    tt=AD[ss,y0];cand=(values[hprev,ss].astype(np.int64)-2*k+10000)*n+ss
                    best=np.full(n,-10**15,dtype=np.int64);np.maximum.at(best,tt,cand);vv=best//n-10000
                    changed=np.flatnonzero(vv>values[total])
                    values[total,changed]=vv[changed];parent[total,changed]=(best[changed]%n).astype(np.int32);prevh[total,changed]=hprev;lastkey[total,changed]=y0+1
        for b,x in bedges:
            bt=int(AD[b,x-1]);q=int(primitive['Q'][b,x-1]);cl=classes[x-1];target=dag.vector(z['columns'][bt],len(cl));offer=values[3,cl]+q;viol=np.flatnonzero(offer>target)
            proofs.append({'B_source':b,'KEEP':x,'B_target':bt,'Q':q,'failed_free_envelope':int(margin[b,x-1]),
              'actual_H3_violations':len(viol),'maximum_actual_violation':int((offer-target).max()),
              'actual_H3_margin':int((target-offer).min())})
            ordered=sorted(viol.tolist(),key=lambda t:(-int(offer[t]-target[t]),t))[:8]
            for a in ordered:
                end=int(cl[a]);cur=end;h=3;word=[]
                while h:
                    y=int(lastkey[h,cur]);s=int(parent[h,cur]);hp=int(prevh[h,cur]);assert s>=0 and y>0
                    assert int(AD[s,y-1])==cur and int(H[s,y-1])==h-hp
                    word.append(y);cur=s;h=hp
                start=cur;word.reverse();assert word[-1]==x and int(roots[start])==g
                state=start;cost=0
                for y in word:cost+=int(H[state,y-1]);state=int(AD[state,y-1])
                assert state==end and cost==3
                code=1
                for y in word:code=12*code+y
                ds=int(initial[int(local[start])]);dt=int(target[a]);assert ds+q-6>dt
                rows.append({'B_source':b,'B_target':bt,'A_source':start,'A_target':end,'g':g,'KEEP':x,'H':3,'Q':q,
                  'A_word':[{'kind':'D' if i<len(word)-1 else 'K','key':y} for i,y in enumerate(word)],
                  'word_code_base12':code,'D_source':ds,'D_target':dt,'signed_margin':6-q+dt-ds})
        assert time.process_time()-START<CAP-2
    out={'status':'ACTUAL_H3_OMISSIONS_FOUND' if rows else 'ALL_H3_SIGNED_LAWS_FOR_THIS_CANDIDATE',
      'candidate':cname,'free_endpoint_failures':len(bad),'distinct_source_profiles_resolved':len(work),'exact_source_cases':proofs,
      'source_constraints_to_add':rows,'cached_primitive_compositions':compositions,'source_queries':0,'source_engine_calls':0,
      'not_a_negative_original_source_cycle':True,'JR35':'OPEN','LOW_quiescence':False,
      'input_sha256':{p:sha(F/p) for p in (cname,'global_probe11_LOW_model.pkl','probe11_source_actions.pkl','independent_probe11_source_actions.json')}}
    with (F/'probe11_H3_source_resolution_07.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k not in ('source_constraints_to_add','exact_source_cases','input_sha256')}),flush=True)
    print(json.dumps({'literal_new_constraints':len(rows)}),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof242_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
