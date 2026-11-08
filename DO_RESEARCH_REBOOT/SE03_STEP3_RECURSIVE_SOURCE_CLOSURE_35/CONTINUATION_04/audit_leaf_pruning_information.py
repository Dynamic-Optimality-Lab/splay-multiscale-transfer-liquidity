"""Independent source realization and old-coefficient audit of LP35.
Every new mutable source access is cumulatively charged. Edges are
separately embeddable; the quotient cycle is NOT an original source walk.
"""
import hashlib,importlib.util,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';C14=P/'SE03_STEP2_UNARY_A_LIFT_14'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def node(t):return isinstance(t,tuple)
def bare(t):return (t[0],bare(t[1]),bare(t[2])) if node(t) or isinstance(t,list) else None
def keys(t):return [] if not node(t) else keys(t[1])+[t[0]]+keys(t[2])
def main():
    global V
    sp=importlib.util.spec_from_file_location('LP35_distinct_mutable',B/'audit_verify79.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    old=json.loads((C14/'branch_core11_mask0.json').read_text());ga=json.loads((C14/'branch_grammar2.json').read_text())
    a6=[tup(t) for t in ga['states']];b6=[bare(tup(t)) for t in old['BF_trees']];aid={t:i for i,t in enumerate(a6)};bid={t:i for i,t in enumerate(b6)}
    ar={g:[i for i,t in enumerate(a6) if t[0]==1000*g] for g in range(1,7)};offset=[0]
    for t in b6:offset.append(offset[-1]+len(ar[(t[0]+1)//2]))
    assert offset[-1]==len(old['debt'])
    M=set(range(1000,8000,1000))
    def project_A(t,omitted):
        retained=sorted(M-{omitted});ranks={k:1000*(i+1) for i,k in enumerate(retained)}
        def go(u):
            if u is None:return None
            l,r=go(u[1]),go(u[2])
            if u[0] in ranks:return (ranks[u[0]],l,r)
            if l is None:return r
            if r is None:return l
            return (1000*sum(k<u[0] for k in retained)+500,l,r)
        return go(t)
    def profile(at,bt):
        entries=[]
        def visit(u,parent=None):
            if u is None:return
            if u[0] in M and u[1] is None and u[2] is None and parent is not None:
                entries.append((u[0],parent[0]))
            visit(u[1],u);visit(u[2],u)
        visit(bt);out=[]
        for e,p in sorted(entries):
            def remove(u):
                if u is None:return None
                if u[0]==p:
                    if u[1] and u[1][0]==e:return u[2]
                    assert u[2] and u[2][0]==e;return u[1]
                return (u[0],remove(u[1]),remove(u[2]))
            bb=remove(bt);rank={k:i+1 for i,k in enumerate(keys(bb))}
            def ren(u):return None if u is None else (rank[u[0]],ren(u[1]),ren(u[2]))
            bt6=ren(bb);ap=project_A(at,e);j=bid[bt6];i=aid[ap];root=(bt6[0]+1)//2
            assert i in ar[root];v=old['debt'][offset[j]+ar[root].index(i)];out.append((e,v))
        code=0
        for _,v in out:code=4*code+v
        return out,code
    def fill(t,allkeys):
        present=set(keys(t))
        def vine(v):return None if not v else (v[0],None,vine(v[1:]))
        def go(u,lo,hi):
            if not node(u):return vine([k for k in allkeys if lo<k<hi and k not in present])
            return (u[0],go(u[1],lo,u[0]),go(u[2],u[0],hi))
        return go(t,0,8000)
    def Bscale(t):return None if not node(t) else (1000*((t[0]+1)//2)+(500 if t[0]%2==0 else 0),Bscale(t[1]),Bscale(t[2]))
    a=json.loads((F/'branch_H1_r7.json').read_text());a2=json.loads((F/'branch_H2_r7.json').read_text())
    b=json.loads((F/'maximal_B_grammar.json').read_text());m=json.loads((F/'active_a10_model.json').read_text())
    with (F/'real_leaf_profile_packets.pkl').open('rb') as f:pm=pickle.load(f)
    cert=json.loads((F/'real_leaf_profile_search_01.json').read_text());ee=list(reversed(cert['cycle_edges']));assert cert['cycle_weight']<0
    assert all(e['t']==ee[(i+1)%len(ee)]['s'] for i,e in enumerate(ee))
    controls=[];total=0;packet_pairs=0
    for i,e in enumerate(ee):
        packet=pm['packets'][e['packet_id']];group=tuple(e['source_group']);s,t,w=pm['groups'][group][e['source_row']]
        assert (s,t)==(e['A_source'],e['A_target'])
        if w[0]=='single':_,h,rid=w;extra=[]
        else:_,h,rid,hh,y,mid=w;extra=[1000*(y+1)];packet_pairs+=1
        source=(a if h==1 else a2)['witnesses'][rid];at=tup(source['source']);accesses=source.get('accesses',[1000*(group[3]+1)])+extra
        assert len(packet['B_edges'])==(2 if extra else 1)
        bstart=Bscale(bare(tup(b['trees'][packet['source']])));K=sorted(set(keys(at))|set(keys(bstart)))
        actualA,actualB=fill(at,K),fill(bstart,K);assert set(keys(actualA))==set(keys(actualB))==set(K)
        AA,BB=V.Mutable(actualA),V.Mutable(actualB);beforeP,cs=profile(actualA,bstart)
        assert packet['source']*4096+cs==e['s']
        rows=[];H=Q=0;keepindex=0
        # The last access of the first LOW witness ends its natural macro.
        firstlen=len(accesses)-len(extra)
        for j,k in enumerate(accesses):
            keep=j==firstlen-1 or j>=firstlen;ab=AA.snapshot();bb=BB.snapshot();hh,qa,events=AA.splay(k,True);q=0
            if keep:
                assert bb[0]!=k;_,q,_=BB.splay(k,False)
                edge=m['B_edges'][packet['B_edges'][keepindex]];keepindex+=1
                assert q==edge['q']
            H+=hh;Q+=q
            rows.append({'local_t':j+1,'kind':'K' if keep else 'D','key':k,'a':hh,'qF':q,'A_before':ab,'BF_before':bb,
              'A_after':AA.snapshot(),'BF_after':BB.snapshot(),'A_events':events})
        targetcore=Bscale(bare(tup(b['trees'][packet['target']])));afterP,ct=profile(tup(AA.snapshot()),targetcore)
        assert packet['target']*4096+ct==e['t'] and H==e['H'] and Q==packet['Q'] and 2*H-Q==e['w']
        total+=e['w'];controls.append({'id':i,'source_profile':e['s'],'target_profile':e['t'],'weight':e['w'],'H':H,'Q':Q,
          'source_leaf_D6':beforeP,'target_leaf_D6':afterP,'initial_A':actualA,'initial_BF':actualB,'physical_keys':K,
          'actual_rows':rows,'separate_closed_embedding':'UNIFORM_A_REALIZATION_OVER_CLOSED_B + pinned all-seven B SCC',
          'is_full_period_replay':False})
        assert time.process_time()-START<CAP-2
    assert total==cert['cycle_weight']==-2 and packet_pairs>0
    out={'status':'PASS_SOURCE_EXACT_INFORMATION_CLASS_REFUTATION','source_edges':len(ee),'actual_q6_q1_pairs':packet_pairs,
      'cycle_weight':total,'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'controls':controls,
      'same_ambient_key_set_per_edge':True,'each_edge_separately_closed_embeddable':True,
      'one_concatenated_source_cycle':False,'JR35':'OPEN','Coarse_Double_refuted':False,
      'input_sha256':{str(p):sha(p) for p in [F/'real_leaf_profile_search_01.json',F/'real_leaf_profile_packets.pkl',
        C14/'branch_core11_mask0.json',C14/'branch_grammar2.json',C14/'branch_all_independent_audit.json',
        B/'UNIFORM_A_REALIZATION_OVER_CLOSED_B.md',F/'independent_branch_H1_audit.json',B/'audit_verify79.py']}}
    with (F/'independent_leaf_profile_refutation.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k not in ('controls','input_sha256')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify112_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,
          'source_queries':0 if V is None else V.CALLS,'source_engine_calls':0 if V is None else V.CALLS},f)
