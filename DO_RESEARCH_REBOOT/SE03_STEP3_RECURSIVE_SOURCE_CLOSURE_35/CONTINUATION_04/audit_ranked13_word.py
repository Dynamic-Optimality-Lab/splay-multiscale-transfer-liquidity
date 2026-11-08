"""Independent Catalan decoding and LAST-leaf H1 source substitution.

H>=2 uses the complete independent endpoint envelope. Saves partial
coverage before the remaining cumulative audit allowance is consumed.
"""
import functools,hashlib,importlib.util,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();PHASE=sys.argv[3];BATCH=int(sys.argv[4]);V=None
C=[1]
for n in range(1,14):C.append(sum(C[i]*C[n-1-i] for i in range(n)))
OFF={n:[sum(C[j]*C[n-1-j] for j in range(i)) for i in range(n+1)] for n in range(1,14)}
@functools.lru_cache(maxsize=16000)
def decode(n,lo,i):
    if not n:assert i==0;return None
    assert 0<=i<C[n]
    k=next(k for k in range(n) if i<OFF[n][k+1]);a,b=divmod(i-OFF[n][k],C[n-1-k])
    return (lo+k,decode(k,lo,a),decode(n-1-k,lo+k+1,b))
@functools.lru_cache(maxsize=16000)
def encode(t,lo,n):
    if not n:assert t is None;return 0
    k,l,r=t;i=k-lo;assert 0<=i<n
    return OFF[n][i]+encode(l,lo,i)*C[n-i-1]+encode(r,k+1,n-i-1)
def last_leaf(t,x):
    if t is None:return None
    if not t[1] and not t[2]:return t[0] if t[0]!=x else None
    return last_leaf(t[2],x) or last_leaf(t[1],x)
@functools.lru_cache(maxsize=16000)
def drop(t,y):
    if t is None:return None
    if t[0]==y:assert not t[1] and not t[2];return None
    return (t[0]-(t[0]>y),drop(t[1],y),drop(t[2],y))
@functools.lru_cache(maxsize=16000)
def raise_tree(t,y):
    if t is None:return None
    return (t[0]+(t[0]>=y),raise_tree(t[1],y),raise_tree(t[2],y))
def insert(t,y):
    if t is None:return (y,None,None)
    return (t[0],insert(t[1],y),t[2]) if y<t[0] else (t[0],t[1],insert(t[2],y))
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    global V
    cp=F/'ranked13_LOW_search_01.pkl';wp=F/'native13_hard_B_word.json'
    with cp.open('rb') as f:res=pickle.load(f)
    D=res['D'];del res
    with (F/'probe11_source_actions.pkl').open('rb') as f:old=pickle.load(f)
    oi={t:i for i,t in enumerate(old['trees'])};word=json.loads(wp.read_text())
    assert len(D)==C[13]==742900 and int(D.min())==0 and int(D.max())==2
    qmap={};nxt={}
    for row in word['rows']:
        g=decode(13,1,row['B_source'])[0];qmap[g]=row['Q'];nxt[g]=row['KEEP']
    assert len(qmap)==13 and sum(qmap.values())==29 and max(qmap.values())==3
    if BATCH==1:
        sp=importlib.util.spec_from_file_location('N13_independent_B',B/'audit_verify79.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
        V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
        b=V.Mutable(decode(13,1,word['rows'][0]['B_source']))
        for row in word['rows']:
            assert tup(b.snapshot())==decode(13,1,row['B_source'])
            _,q,_=b.splay(row['KEEP'],False)
            assert q==row['Q'] and tup(b.snapshot())==decode(13,1,row['B_target'])
        assert tup(b.snapshot())==decode(13,1,word['rows'][0]['B_source'])
        s=checked=all_endpoint_states=0;prior_B_checks=13
    else:
        p=json.loads((F/f'independent_ranked13_word_{BATCH-1:02d}.json').read_text())
        assert p['status']=='PARTIAL_INDEPENDENT_SOURCE_COVERAGE';s=p['next_source'];checked=p['H1_literal_checks'];all_endpoint_states=p['H1_all_endpoint_safe_states'];prior_B_checks=p['B_source_checks_total']
    mins={g:int(D[OFF[13][g-1]:OFF[13][g]].min()) for g in range(1,14)}
    maxs={g:int(D[OFF[13][g-1]:OFF[13][g]].max()) for g in range(1,14)}
    high=min(4-qmap[g]+mins[nxt[g]]-maxs[g] for g in qmap);assert high>=0
    @functools.lru_cache(maxsize=18000)
    def act(t,n,x):
        if n==11:
            i=oi[t];assert int(old['H'][i,x-1])==1
            return old['trees'][int(old['destination'][i,x-1])]
        y=last_leaf(t,x);assert y is not None
        return insert(raise_tree(act(drop(t,y),n-1,x-(x>y)),y),y)
    while s<C[13] and time.process_time()-START<CAP-2:
        g=next(g for g in range(1,14) if s<OFF[13][g]);x=nxt[g]
        rhs=int(D[s])+qmap[g]-2
        if rhs<=mins[x]:all_endpoint_states+=1;s+=1;continue
        t=decode(13,1,s);u=t;depth=None
        for d in range(3):
            if u[0]==x:depth=d;break
            u=u[1] if x<u[0] else u[2]
            if u is None:break
        if depth is not None:
            assert depth in (1,2);out=act(t,13,x);j=encode(out,1,13)
            assert int(D[j])>=rhs;checked+=1
        s+=1
    r={'status':'PASS_COMPLETE_RANKED13_FIXED_WORD_SOURCE_SIGNS' if s==C[13] else 'PARTIAL_INDEPENDENT_SOURCE_COVERAGE',
      'next_source':s,'total_full_A_states':C[13],'H1_literal_checks':checked,'H1_all_endpoint_safe_states':all_endpoint_states,
      'H_ge_2_minimum_margin':high,'D_range':[0,2],'c':'min(H,2)','conservative_Bank25_bound':6,
      'B_source_checks_total':prior_B_checks,'source_queries':0 if V is None else V.CALLS,'source_engine_calls':0 if V is None else V.CALLS,
      'source_binding':'independent Catalan decoder/encoder and LAST non-target leaf twice to accepted native11 table',
      'scope':'one exact thirteen-key full-B cycle; arbitrary A words on these anchors and rigid off-path hangers',
      'JR35':'OPEN','reservation':'DEFERRED','independent_is_same_agent_distinct_implementation':True,
      'input_sha256':{str(p):sha(p) for p in (cp,wp,F/'probe11_source_actions.pkl',F/'independent_probe11_source_actions.json',B/'OFF_PATH_LEAF_SOURCE_LIFT.md',F/'audit_ranked13_word.py')}}
    with (F/f'independent_ranked13_word_{BATCH:02d}.json').open('x',encoding='utf8') as f:json.dump(r,f,indent=2)
    print(json.dumps({k:v for k,v in r.items() if k!='input_sha256'}),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        calls=0 if V is None else V.CALLS
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':calls,'source_engine_calls':calls},f)
