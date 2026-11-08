"""Choose literal difficult B words, not CD counterexamples or universal bounds."""
import hashlib,json,pickle,random,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=F/'eight_core_B_source_01.pkl'
    with p.open('rb') as f:z=pickle.load(f)
    assert z['status']=='PRODUCER_B8_SS_TABLE_COMPLETE';rows=z['rows'];N=len(z['trees']);rng=random.Random(353108);found={};passes=0
    def take(v,parent):
        seen={};chain=[]
        while v in parent and len(chain)<400:
            if v in seen:
                ids=chain[seen[v]:][::-1];rr=[rows[j] for j in ids]
                assert all(rr[i][1]==rr[(i+1)%len(rr)][0] for i in range(len(rr)))
                keys=[r[2] for r in rr];support=set(keys);Q=sum(r[3] for r in rr)
                if len(support)<7 or Q<=2*len(rr):return
                rotations=[tuple(keys[j:]+keys[:j]) for j in range(len(keys))];canonical=min(rotations)
                if canonical not in found:found[canonical]={'word':keys,'edges':rr,'Q':Q,'M':len(rr),'ratio':Q/len(rr),'genuine_support':sorted(support),'initial_B':z['trees'][rr[0][0]]}
                return
            seen[v]=len(chain);j=parent[v];chain.append(j);v=rows[j][0]
    for trial in range(24):
        D=[0]*N;parent={};order=list(range(len(rows)));rng.shuffle(order)
        # Different thresholds favour different genuinely closed high-Q words.
        penalty=[2,2.5,2.75,3][trial%4]
        for k in range(12):
            changed=False
            for j in order:
                s,t,x,q=rows[j];value=D[s]+q-penalty
                if value>D[t]:
                    D[t]=value;parent[t]=j;changed=True
                    if value>8 and (j+k)%97==0:take(t,parent)
            passes+=1
            if not changed or len(found)>=40 or time.process_time()-START>CAP-4:break
        if len(found)>=40 or time.process_time()-START>CAP-4:break
    controls=sorted(found.values(),key=lambda r:(-r['ratio'],r['M'],r['word']))
    out={'status':'LITERAL_DIFFICULT_B_CYCLE_INVENTORY','cycles':controls,'cycles_found':len(controls),'passes':passes,
      'source_queries':0,'source_engine_calls':0,'JR35':'OPEN','none_is_a_CD_counterexample_without_actual_A':True,
      'input_sha256':{str(p):sha(p),str(F/'select_eight_core_B_cycles.py'):sha(F/'select_eight_core_B_cycles.py')}}
    with (F/'eight_core_B_cycles.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({'cycles':len(controls),'best':[{'word':r['word'],'Q':r['Q'],'M':r['M'],'ratio':r['ratio']} for r in controls[:5]]}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof294_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
