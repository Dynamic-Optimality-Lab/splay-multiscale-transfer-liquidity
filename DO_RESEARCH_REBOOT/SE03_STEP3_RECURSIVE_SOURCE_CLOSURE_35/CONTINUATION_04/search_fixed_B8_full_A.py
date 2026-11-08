"""Actual full-A search over one literal closed B word; no abstract source quotient."""
import functools,hashlib,importlib.util,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
sys.path.insert(0,str(F));import ranked_source_bst15 as R
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);PHASE=sys.argv[3];BATCH=int(sys.argv[4]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
@functools.lru_cache(None)
def small(lo,hi):
    if lo>hi:return (None,)
    return tuple((k,l,r) for k in range(lo,hi+1,2) for l in small(lo,k-2) for r in small(k+2,hi))
def insert(t,x):
    if t is None:return (x,None,None)
    return (t[0],insert(t[1],x),t[2]) if x<t[0] else (t[0],t[1],insert(t[2],x))
def main():
    global V
    source=F/'eight_core_B_cycles.json';cy=json.loads(source.read_text())['cycles'][0];M=cy['M'];word=cy['word'];bedges=cy['edges']
    with (F/'eight_core_B_source_01.pkl').open('rb') as f:basis=pickle.load(f)
    bt=[basis['trees'][e[0]] for e in bedges]
    with (F/'probe11_source_actions.pkl').open('rb') as f:old=pickle.load(f)
    sp=importlib.util.spec_from_file_location('B8_fixed_actual_A_kernel',B/'audit_core39.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    fresh=dict(basis['fresh']);records={};frontier=[];depth=processed=0;tight=None;candidate=None
    if BATCH>1:
        with (F/f'fixed_B8_full_A_{BATCH-1:02d}.pkl').open('rb') as f:z=pickle.load(f)
        assert z['word']==word;fresh=z['fresh'];records=z['records'];frontier=z['frontier'];depth=z['depth'];processed=z['processed'];tight=z['tight']
    else:
        with (F/'full_source15_beam_11.pkl').open('rb') as f:fresh.update(pickle.load(f)['fresh'])
        for phase,b in enumerate(bt):
            g=b[0]
            shapes=[b]+[(g,l,r) for l in small(1,g-2) for r in small(g+2,15)]
            for a in shapes:
                for x in range(2,16,2):
                    # Full native B seed already contains evens; only add missing
                    # leaves to the odd-only source seeds.
                    if a is not b:a=insert(a,x)
                key=(R.rank_tree(a,1,15),phase);records[key]=(0,None,None,None,None,None);frontier.append(key)
    def kernel(t,n,x):
        key=(t,n,x)
        if key not in fresh:
            assert V.CALLS<QCAP
            out,h,q,_=V.splay(t,x,False);fresh[key]=(out,h,q)
        return fresh[key]
    lift=R.Lift(old,kernel)
    def take_cycle(start,dest,edge):
        chain=[edge];u=start;seen=set()
        while u is not None and u not in seen and len(chain)<1800:
            if u==dest:
                edges=list(reversed(chain));gain=sum(e['Q']-2*e['H'] for e in edges)
                if gain<0 or not any(e['kind']=='KEEP' for e in edges):return None
                assert all(edges[i]['destination']==edges[(i+1)%len(edges)]['source'] for i in range(len(edges)))
                return {'gain_Q_minus_2A':gain,'A':sum(e['H'] for e in edges),'Q':sum(e['Q'] for e in edges),'edges':edges,
                  'genuine_support':sorted({e['target'] for e in edges if e['kind']=='KEEP'}),
                  'verification':'PRODUCER_ONLY: actual full states, distinct source replay and reachability/period proof required'}
            seen.add(u);r=records[u]
            if r[1] is None:return None
            chain.append({'source':r[1],'destination':u,'kind':r[2],'target':r[3],'H':r[4],'Q':r[5]});u=r[1]
        return None
    def prune(keys):
        keep=set(keys);todo=list(keep)
        while todo:
            u=todo.pop();p=records[u][1]
            if p is not None and p not in keep:keep.add(p);todo.append(p)
        return {k:records[k] for k in keep}
    status='CHECKPOINT';i=0;newfront={}
    while frontier and time.process_time()-START<CAP-4:
        if len(records)>60000:records=prune(frontier)
        i=0;newfront={}
        while i<len(frontier) and time.process_time()-START<CAP-4:
            key=frontier[i];a,phase=key;tree=R.unrank(15,1,a);score=records[key][0];x=word[phase]
            out,h,_=lift.action(tree,15,x)
            actions=[('KEEP',x,out,h,bedges[phase][3],(phase+1)%M)]
            for y in range(1,16):
                if y==tree[0]:continue
                out,h,_=lift.action(tree,15,y);actions.append(('DELETE',y,out,h,0,phase))
            for kind,x,out,h,q,pnext in actions:
                dest=(R.rank_tree(out,1,15),pnext);value=score+q-2*h;oldvalue=records.get(dest,(-10**9,))[0]
                if value>=oldvalue and dest in records:
                    hit=take_cycle(key,dest,{'source':key,'destination':dest,'kind':kind,'target':x,'H':h,'Q':q})
                    if hit and hit['gain_Q_minus_2A']>0:candidate=hit;status='POSITIVE_CLOSED_SOURCE_CYCLE_CANDIDATE';break
                    if hit and tight is None:tight=hit
                if value>oldvalue:records[dest]=(value,key,kind,x,h,q);newfront[dest]=value
            processed+=1;i+=1
            if candidate:break
            if len(records)>150000:
                records=prune(frontier[i:]+list(newfront))
                if len(records)>140000:status='RECORD_GUARD_CHECKPOINT';break
            assert 646646+2*len(lift.index)+3*len(records)+len(fresh)+3*len(frontier)+22000<2000000
        pick=sorted(newfront,key=lambda k:(newfront[k],k),reverse=True)[:5000]
        if candidate or status!='CHECKPOINT' or i<len(frontier):frontier=list(dict.fromkeys(frontier[i:]+pick));break
        frontier=pick;depth+=1
    z={'status':status,'word':word,'B_edges':bedges,'records':records,'frontier':frontier,'fresh':fresh,'depth':depth,'processed':processed,'candidate':candidate,'tight':tight,
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'cached_leaf_substitutions':lift.substitutions,'JR35':'OPEN','search_is_incomplete':True,
      'input_sha256':{str(p):sha(p) for p in (source,F/'eight_core_B_source_01.pkl',F/'probe11_source_actions.pkl',F/'search_fixed_B8_full_A.py',B/'OFF_PATH_LEAF_SOURCE_LIFT.md')}}
    with (F/f'fixed_B8_full_A_{BATCH:02d}.pkl').open('xb') as f:pickle.dump(z,f,protocol=5)
    report={k:v for k,v in z.items() if k not in ('records','frontier','fresh','tight','candidate')};report.update({'records':len(records),'frontier':len(frontier),'candidate':candidate,'tight':tight})
    with (F/f'fixed_B8_full_A_{BATCH:02d}.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps({'status':status,'depth':depth,'processed':processed,'positive_candidate':bool(candidate),'tight_cycle':bool(tight),'source_queries':V.CALLS}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        calls=0 if V is None else V.CALLS
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':calls,'source_engine_calls':calls},f)
