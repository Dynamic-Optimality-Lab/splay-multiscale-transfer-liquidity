"""Exact n7 test of arbitrary nonlinear complete joint-depth summary potentials.

No source writes, no fitting, no solver dependency. A positive summary cycle
refutes the architecture, not physical Coarse-Double. Outputs are exclusive.
"""
from pathlib import Path
from functools import lru_cache
from collections import deque,Counter
from array import array
import sys,json,time,hashlib,subprocess,ast
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path[:0]=[str(ROOT/'python')]
from independent import splay as S
from liquidity import legacy_embedding as P
N=7
START=time.process_time()

def ck(x,msg):
    if not x:raise AssertionError(msg)

def save(name,obj):
    with (OUT/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args]).decode('utf-8').strip()

@lru_cache(None)
def trees(lo,hi):
    if lo==hi:return (S.LEAF,)
    return tuple(S.node(x,l,r) for x in range(lo,hi) for l in trees(lo,x) for r in trees(x+1,hi))

def serial(t):return None if t==S.LEAF else [t[1],serial(t[2]),serial(t[3])]
def decode(t):return S.LEAF if t is None else S.node(t[0],decode(t[1]),decode(t[2]))
def ptr(t):
    if t==S.LEAF:return None
    q=P.mknode(t[1],ptr(t[2]),ptr(t[3]))
    if q['l'] is not None:q['l']['p']=q
    if q['r'] is not None:q['r']['p']=q
    return q
def tuple_ptr(t):return S.LEAF if t is None else S.node(t['k'],tuple_ptr(t['l']),tuple_ptr(t['r']))

def depthvec(t,n=N):return tuple(S.lookup(t,x)[1] for x in range(1,n+1))
def feature(a,b,n=N):
    da=depthvec(a,n);db=depthvec(b,n)
    return (n,a[1],b[1],tuple(sorted(n*u+v for u,v in zip(da,db))))
def feature_json(a,b,n=N):
    f=feature(a,b,n)
    return {'n':n,'root_A':a[1],'root_B':b[1],
            'joint_depth_histogram':[[k//n,k%n,v] for k,v in sorted(Counter(f[3]).items())]}

def source_snapshot():
    names=git('ls-files').splitlines()
    selected={x for x in names if Path(x).suffix in ('.py','.md','.lean')}
    old=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001'
    for name in ('u4_counterexample_certificate.json','five_keep_nine_core_counterexample.json','U4_09_UNIFORM_POTENTIAL_ALTERNATIVE.md'):
        selected.add((old/name).relative_to(ROOT).as_posix())
    files={name:sha(ROOT/name) for name in sorted(selected) if (ROOT/name).is_file()}
    entry={'date':'2026-10-30','timezone':'Asia/Karachi','head':git('rev-parse','HEAD'),
           'branch':git('branch','--show-current'),'tracked_status':git('status','--porcelain=v1','--untracked-files=no'),
           'files':files,'coverage':'All tracked Python/Markdown/Lean and the inherited physical counterexample inputs. Active untracked Stage11G work is not claimed frozen.'}
    ck(entry['tracked_status']=='','tracked tree changed before entry')
    save('entry_source_pins.json',entry)
    return entry

def end_integrity(entry):
    bad=[name for name,digest in entry['files'].items() if not (ROOT/name).exists() or sha(ROOT/name)!=digest]
    result={'source_files_compared':len(entry['files']),'source_bytes_changed':bad,
            'head_unchanged':git('rev-parse','HEAD')==entry['head'],
            'branch_unchanged':git('branch','--show-current')==entry['branch'],
            'tracked_tree_clean':git('status','--porcelain=v1','--untracked-files=no')=='',
            'outputs_confined_to_new_run':True,'Stage11G_modified':False}
    result['status']='PASS' if not bad and result['head_unchanged'] and result['branch_unchanged'] and result['tracked_tree_clean'] else 'FAIL'
    save('integrity.json',result)
    return result

def check_old_inputs():
    old=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001'
    results=[]
    for name in ('u4_counterexample_certificate.json','five_keep_nine_core_counterexample.json'):
        c=json.loads((old/name).read_text(encoding='utf-8'));a=decode(c['initial_A']);b=decode(c['initial_B'])
        n=len(S.inorder(a));a0=a;b0=b;seen=set();A=Q=0
        for i,((mode,x),r) in enumerate(zip(c['word'],c['full_state_replay'])):
            seen.add(feature(a,b,n));ap,ae=S.trace(a,x)
            if mode=='K':bp,be=S.trace(b,x)
            else:bp=b;be=[]
            q=sum(e[0]!='ZIG' for e in be);ck((len(ae),q)==(r['a'],r['q']),('inherited costs',name,i))
            ck(serial(ap)==r['destination_A'] and serial(bp)==r['destination_B'],('inherited state',name,i))
            A+=len(ae);Q+=q;a=ap;b=bp
        ck(a==a0 and b==b0 and A==c['A'] and Q==c['Q_B'],('inherited closure',name))
        results.append({'input':name,'n':n,'accesses':len(c['word']),'A':A,'Q_B':Q,
                        'paired_closure':True,'exact_summary_states':len(seen),'uses_latest_setup_ID':False})
    save('overwritten_setup_input_regression.json',results)

def physical_tables():
    ts=trees(1,N+1);ids={t:i for i,t in enumerate(ts)};count=len(ts)
    tr=[];dep=[]
    for i,t in enumerate(ts):
        tt=[];dd=[]
        for x in range(1,N+1):
            q=ptr(t);depth=P._depth_to(q,x)[0];pout,pe=P.splay_trace(q,x)
            tout,te=S.trace(t,x)
            ck(tuple_ptr(pout)==tout,('engine destination',i,x))
            ck([(v['case'],v['lo'],v['hi'],v['orient']) for v in pe]==te,('engine trace',i,x))
            ck(depth==S.lookup(t,x)[1] and len(te)==(depth+1)//2,('depth/StepEv',i,x))
            tt.append(ids[tout]);dd.append(depth)
        tr.append(tt);dep.append(dd)
    ck(count==429,'Catalan n7')
    return ts,tr,dep

def successors(u,m,tr):
    a,b=divmod(u,m)
    for k in range(N):
        an=tr[a][k]
        yield an*m+b,2*k
        yield an*m+tr[b][k],2*k+1

def recurrent_domain(m,tr,anchor):
    nv=m*m;ne=nv*2*N
    parents=array('i',[-1])*nv;parent_op=array('b',[-1])*nv;parents[anchor]=anchor
    queue=deque([anchor])
    while queue:
        u=queue.popleft()
        for v,op in successors(u,m,tr):
            if parents[v]<0:parents[v]=u;parent_op[v]=op;queue.append(v)
    # Reverse CSR, retaining the actual forward source and operation.
    counts=array('I',[0])*nv
    for u in range(nv):
        for v,op in successors(u,m,tr):counts[v]+=1
    offsets=array('I',[0])
    for value in counts:offsets.append(offsets[-1]+value)
    ck(offsets[-1]==ne and ne<5000000,'source edge ceiling')
    cursor=array('I',offsets[:-1]);sources=array('I',[0])*ne;ops=array('b',[0])*ne
    for u in range(nv):
        for v,op in successors(u,m,tr):
            j=cursor[v];sources[j]=u;ops[j]=op;cursor[v]+=1
    back=array('i',[-1])*nv;back_op=array('b',[-1])*nv;back[anchor]=anchor;queue=deque([anchor])
    while queue:
        v=queue.popleft()
        for j in range(offsets[v],offsets[v+1]):
            u=sources[j]
            if back[u]<0:back[u]=v;back_op[u]=ops[j];queue.append(u)
    valid=bytearray(int(parents[u]>=0 and back[u]>=0) for u in range(nv))
    return valid,parents,parent_op,back,back_op

def build_quotient(ts,tr,dep,valid):
    m=len(ts);classes={};features=[];qids=array('I',[0])*(m*m)
    for u in range(m*m):
        a,b=divmod(u,m)
        # Sorted depth-pair codes are a lossless multiset representation at fixed n.
        key=bytes([ts[a][1],ts[b][1]]+sorted(N*x+y for x,y in zip(dep[a],dep[b])))
        if key not in classes:classes[key]=len(features);features.append(key)
        qids[u]=classes[key]
    adj=[{} for _ in features];concrete=0
    for u in range(m*m):
        if not valid[u]:continue
        a,b=divmod(u,m);row=adj[qids[u]]
        for v,op in successors(u,m,tr):
            if not valid[v]:continue
            k=op//2;costA=(dep[a][k]+1)//2
            reward=(dep[b][k]//2 if op%2 else 0)-2*costA
            target=qids[v];old=row.get(target)
            if old is None or reward>old[0]:row[target]=(reward,u,op)
            concrete+=1
        if u%4096==0:ck(time.process_time()-START<120,'UNKNOWN source/quotient construction CPU cap')
    edges=[(u,v,w,p,op) for u,row in enumerate(adj) for v,(w,p,op) in sorted(row.items())]
    ck(len(features)<2000000 and len(edges)<5000000,'quotient ceilings')
    return features,qids,edges,concrete

def predecessor_positive_cycle(pred):
    done=bytearray(len(pred))
    for initial in range(len(pred)):
        if done[initial] or pred[initial] is None:continue
        chain=[];position={};v=initial
        while not done[v] and pred[v] is not None and v not in position:
            position[v]=len(chain);chain.append(v);v=pred[v][0]
        if v in position:
            cycle=list(reversed([pred[z] for z in chain[position[v]:]]))
            if sum(e[2] for e in cycle)>0:
                ck(all(cycle[j][1]==cycle[(j+1)%len(cycle)][0] for j in range(len(cycle))),'cycle order')
                return cycle
        for z in chain:done[z]=1
    return None

def solve(qn,edges):
    phase=time.process_time();labels=[0]*qn;pred=[None]*qn;passes=0;scans=0
    for it in range(qn):
        changed=0
        for j,e in enumerate(edges):
            u,v,w,physical,op=e
            if labels[v]<labels[u]+w:
                labels[v]=labels[u]+w;pred[v]=e;changed+=1
            scans+=1
            if j%16384==0:ck(time.process_time()-phase<120,'UNKNOWN exact quotient solver CPU cap')
        passes+=1
        cycle=predecessor_positive_cycle(pred)
        if cycle:return {'status':'POSITIVE_SUMMARY_CYCLE','passes':passes,'scans':scans,'cycle':cycle}
        if not changed:
            ck(all(labels[v]>=labels[u]+w for u,v,w,_,_ in edges),'complete finite label inequalities')
            return {'status':'FINITE_POTENTIAL_ONLY','passes':passes,'scans':scans,'labels':[-x for x in labels]}
    raise AssertionError('UNKNOWN: no extracted positive cycle after complete Bellman-Ford passes')

def replay_path(ts,tr,m,start,steps):
    u=start;w=[]
    for op in steps:
        k=op//2;a,b=divmod(u,m)
        u=tr[a][k]*m+(tr[b][k] if op%2 else b);w.append(['K' if op%2 else 'D',k+1])
    return u,w

def serialize_result(solution,ts,tr,dep,features,qids,parents,parent_op,back,back_op,anchor):
    m=len(ts)
    if solution['status']=='FINITE_POTENTIAL_ONLY':
        save('finite_summary_potential.json',{'n':N,'labels':solution['labels'],'encoded_class_features':[list(f) for f in features],
            'feature_encoding':'rootA,rootB, sorted n*dA+dB; full paired-depth multiset, n fixed at7','all_size_claim':False})
        return {'finite_potential_range':[min(solution['labels']),max(solution['labels'])]}
    records=[]
    for j,(u,v,w,p,op) in enumerate(solution['cycle']):
        ai,bi=divmod(p,m);k=op//2;x=k+1;mode='K' if op%2 else 'D'
        ap=tr[ai][k];bp=tr[bi][k] if op%2 else bi;after=ap*m+bp
        forward=[];cur=p
        while cur!=anchor:forward.append(parent_op[cur]);cur=parents[cur]
        forward.reverse();end,prefix=replay_path(ts,tr,m,anchor,forward);ck(end==p,'diagonal reachability prefix')
        ret=[];cur=after
        while cur!=anchor:ret.append(back_op[cur]);cur=back[cur]
        end,return_word=replay_path(ts,tr,m,after,ret);ck(end==anchor,'return to diagonal anchor')
        source={'A':serial(ts[ai]),'B':serial(ts[bi])};destination={'A':serial(ts[ap]),'B':serial(ts[bp])}
        records.append({'source_summary_id':u,'destination_summary_id':v,'mode':mode,'key':x,
            'source':source,'destination':destination,'a':(dep[ai][k]+1)//2,
            'q':dep[bi][k]//2 if mode=='K' else 0,'dA':dep[ai][k],'dB':dep[bi][k] if mode=='K' else None,
            'reward':w,'source_summary':feature_json(ts[ai],ts[bi]),'destination_summary':feature_json(ts[ap],ts[bp]),
            'diagonal_prefix':prefix,'diagonal_return':return_word})
    stitches=[]
    for j,e in enumerate(records):
        nxt=records[(j+1)%len(records)]
        ck(e['destination_summary']==nxt['source_summary'],'full summary equality')
        stitches.append({'after_edge':j,'before_edge':(j+1)%len(records),
            'full_physical_pair_equal':e['destination']==nxt['source'],
            'A_equal':e['destination']['A']==nxt['source']['A'],'B_equal':e['destination']['B']==nxt['source']['B']})
    result={'status':'EXACT_SUMMARY_ARCHITECTURE_COUNTERCERTIFICATE','n':N,'summary_cycle_reward':sum(e['reward'] for e in records),
            'edges':records,'stitches':stitches,'diagonal_anchor':{'A':serial(ts[anchor//m]),'B':serial(ts[anchor%m])},
            'all_selected_edges_reachable_and_recurrent':True,'physical_CoarseDouble_counterexample':False,
            'claim_refuted':'Any arbitrary real-valued F(n,rootA,rootB,complete joint-depth histogram) satisfying every original transition inequality',
            'scope':'Universal architecture refuted by finite source-exact premises. Summary cycle is not presumed physically liftable.'}
    save('nonlinear_joint_depth_countercertificate.json',result)
    return {'summary_cycle_edges':len(records),'summary_cycle_reward':result['summary_cycle_reward'],
            'incompatible_physical_stitches':sum(not s['full_physical_pair_equal'] for s in stitches)}

def main():
    ck(not (OUT/'entry_source_pins.json').exists(),'append-only run already started')
    entry=source_snapshot();check_old_inputs();ts,tr,dep=physical_tables();m=len(ts)
    anchor=ts.index(S.vine(N))*(m+1)
    valid,parents,parent_op,back,back_op=recurrent_domain(m,tr,anchor)
    features,qids,edges,concrete=build_quotient(ts,tr,dep,valid)
    construction=time.process_time()-START
    print(json.dumps({'phase':'source_complete','physical_pairs':m*m,'recurrent_pairs':sum(valid),
          'summary_states':len(features),'source_edges_retained':concrete,'summary_edges':len(edges),'CPU_seconds':round(construction,3)}),flush=True)
    solution=solve(len(features),edges)
    details=serialize_result(solution,ts,tr,dep,features,qids,parents,parent_op,back,back_op,anchor)
    ck(time.process_time()-START<300,'UNKNOWN total experiment CPU cap')
    result={'status':solution['status'],'n':N,'physical_shapes':m,'physical_transitions_dual_engine_checked':m*N,
            'physical_pairs':m*m,'diagonal_anchor_recurrent_pairs':sum(valid),'summary_states':len(features),
            'concrete_edges_retained':concrete,'summary_edges':len(edges),'passes':solution['passes'],'integer_edge_scans':solution['scans'],
            'construction_CPU_seconds':round(construction,3),'total_CPU_seconds':round(time.process_time()-START,3),
            'all_size_invariant_proved':False,'Stage11G_changed':False,**details}
    save('result.json',result);end_integrity(entry)
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':
    try:main()
    except Exception as error:
        if not (OUT/'failure.json').exists():save('failure.json',{'status':'FAILED_OR_UNKNOWN','type':type(error).__name__,'error':str(error),'CPU_seconds':time.process_time()-START})
        raise
