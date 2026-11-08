"""Bounded exact original KEEP/DELETE path falsification, not a proof by search.

Full A/B Catalan ranks are lossless. Accepted non-target-leaf identities
reuse native11 primitives. Every new Hamiltonian primitive is charged.
Only an actual positive-weight CLOSED full-pair cycle is a counterexample.
"""
import hashlib,importlib.util,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
sys.path.insert(0,str(F));import ranked_source_bst as R
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();PHASE=sys.argv[3];BATCH=int(sys.argv[4]);V=None
class StopQueries(Exception):pass
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    global V
    with (F/'probe11_source_actions.pkl').open('rb') as f:old=pickle.load(f)
    sp=importlib.util.spec_from_file_location('beam13_fresh_source',B/'audit_core39.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    fresh={};records={};frontier=[];depth=0;processed=0;candidate=None
    if BATCH>1:
        with (F/f'full_source13_beam_{BATCH-1:02d}.pkl').open('rb') as f:z=pickle.load(f)
        fresh=z['fresh'];records=z['records'];frontier=z['frontier'];depth=z['depth'];processed=z['processed'];del z
    def kernel(t,n,x):
        key=(t,n,x)
        if key in fresh:return fresh[key]
        if V.CALLS>=max(0,QCAP-30):raise StopQueries
        out,h,q,_=V.splay(t,x,False);fresh[key]=(out,h,q);return fresh[key]
    lift=R.Lift(old,kernel)
    if BATCH==1:
        with (F/'ranked13_LOW_search_01.pkl').open('rb') as f:z=pickle.load(f)
        D=z['D'];word=json.loads((F/'native13_hard_B_word.json').read_text())
        for row in word['rows']:
            b=row['B_source'];g=R.unrank(13,1,b)[0];lo,hi=R.OFF[13][g-1:g+1]
            top=int(D[lo:hi].max());special=[lo+i for i in range(hi-lo) if int(D[lo+i])==top][:3]
            for a in [b]+special:
                records.setdefault((a,b),(0,None,None,None,None,None));frontier.append((a,b))
        frontier=list(dict.fromkeys(frontier));del z,D
    status='CHECKPOINT';newfront={};i=0;substitutions=0
    def check_cycle(key):
        seen={};chain=[];u=key
        while u is not None and len(chain)<3000:
            if u in seen:
                cyc=chain[seen[u]:];gain=sum(records[v][5]-2*records[v][4] for v in cyc)
                if gain>0:
                    # Parents point backwards. Reverse to literal source order.
                    edges=[]
                    for v in reversed(cyc):
                        score,prev,kind,x,h,q=records[v]
                        edges.append({'source':prev,'destination':v,'kind':kind,'target':x,'H':h,'Q':q})
                    assert edges[0]['source']==edges[-1]['destination']
                    assert all(edges[k]['destination']==edges[(k+1)%len(edges)]['source'] for k in range(len(edges)))
                    return {'gain_Q_minus_2A':gain,'A':sum(e['H'] for e in edges),'Q':sum(e['Q'] for e in edges),
                      'genuine_support':sorted({e['target'] for e in edges if e['kind']=='KEEP' and R.unrank(13,1,e['source'][1])[0]!=e['target']}),
                      'edges':edges,'verification':'PRODUCER_CANDIDATE; independent original replay and source closure required'}
                return None
            seen[u]=len(chain);chain.append(u);u=records[u][1]
        return None
    try:
        while frontier and time.process_time()-START<CAP-4:
            newfront={};i=0
            while i<len(frontier) and time.process_time()-START<CAP-4:
                key=frontier[i];a,b=key;score=records[key][0]
                ta=R.unrank(13,1,a);tb=R.unrank(13,1,b);ar=ta[0];br=tb[0]
                actions=[]
                if ar!=br:actions.append(('KEEP',ar,ta,0))
                for x in R.near(ta):
                    out,h,_=lift.action(ta,13,x);assert h==1
                    actions.extend((('KEEP',x,out,1),('DELETE',x,out,1)))
                for kind,x,out,h in actions:
                    aa=R.rank_tree(out,1,13)
                    if kind=='KEEP' and x!=br:
                        bt,_,q=lift.action(tb,13,x);bb=R.rank_tree(bt,1,13)
                    else:bb=b;q=0
                    dest=(aa,bb);value=score+q-2*h
                    if value>records.get(dest,(-10**9,))[0]:
                        records[dest]=(value,key,kind,x,h,q);newfront[dest]=value
                        if value>6 and processed%127==0:
                            candidate=check_cycle(dest)
                            if candidate:status='POSITIVE_CLOSED_SOURCE_CYCLE_CANDIDATE';break
                processed+=1;i+=1
                live=646646+len(lift.index)+3*len(records)+3*len(newfront)+2*len(frontier)+len(fresh)+100000
                if candidate:break
                if len(records)>=150000 or live>=1900000:status='RECORD_GUARD_CHECKPOINT';break
            if candidate or status!='CHECKPOINT':break
            if i<len(frontier):
                # The unprocessed old suffix and generated successors remain
                # exact frontiers; none is silently treated as explored.
                frontier=list(dict.fromkeys(frontier[i:]+sorted(newfront,key=lambda k:(newfront[k],k),reverse=True)[:3000]));newfront={};break
            frontier=sorted(newfront,key=lambda k:(newfront[k],k),reverse=True)[:3000];depth+=1;newfront={}
    except StopQueries:
        status='QUERY_RESERVE_CHECKPOINT';frontier=list(dict.fromkeys(frontier[i:]+sorted(newfront,key=lambda k:(newfront[k],k),reverse=True)[:3000]));newfront={}
    if newfront:frontier=list(dict.fromkeys(frontier[i:]+sorted(newfront,key=lambda k:(newfront[k],k),reverse=True)[:3000]))
    z={'status':status,'records':records,'frontier':frontier,'fresh':fresh,'depth':depth,'processed':processed,
      'candidate':candidate,'max_path_gain':max(v[0] for v in records.values()),'source_queries':V.CALLS,'source_engine_calls':V.CALLS,
      'source_leaf_substitutions_this_batch':lift.substitutions,'JR35':'OPEN',
      'limits':'beam3000; records150000; stopping guards are not mathematical negative verdicts',
      'input_sha256':{str(p):sha(p) for p in (F/'ranked_source_bst.py',F/'probe11_source_actions.pkl',F/'independent_probe11_source_actions.json',B/'OFF_PATH_LEAF_SOURCE_LIFT.md',F/'search_full_source13_beam.py')}}
    with (F/f'full_source13_beam_{BATCH:02d}.pkl').open('xb') as f:pickle.dump(z,f,protocol=5)
    report={k:v for k,v in z.items() if k not in ('records','frontier','fresh')};report.update({'records':len(records),'frontier':len(frontier),'fresh_primitive_bindings':len(fresh)})
    with (F/f'full_source13_beam_{BATCH:02d}.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        n=0 if V is None else V.CALLS
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':n,'source_engine_calls':n},f)
