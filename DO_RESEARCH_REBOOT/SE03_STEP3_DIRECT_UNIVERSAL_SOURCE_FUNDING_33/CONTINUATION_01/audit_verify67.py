"""Independent exact sparse conversion and original-edge retention audit."""
import hashlib,json,pickle,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def node(t):return isinstance(t,tuple)
def skeleton(t,scale=1):return None if not node(t) else (t[0]/scale,skeleton(t[1],scale),skeleton(t[2],scale))
def reconstruct(trees,p=2.5):
    roots={t[0] for t in trees}
    if len(roots)==1:
        k=next(iter(roots))
        if k<p:
            assert all(t[1]==trees[0][1] for t in trees)
            return k,trees[0][1],reconstruct([t[2] for t in trees],p)
        assert all(t[2]==trees[0][2] for t in trees)
        return k,reconstruct([t[1] for t in trees],p),trees[0][2]
    def restrict(t,lower):
        if t is None:return None
        k,L,R=t
        if (k<p)==lower:return k,restrict(L,lower),restrict(R,lower)
        return restrict(L if lower else R,lower)
    L,R=restrict(trees[0],True),restrict(trees[0],False)
    assert L is not None and R is not None
    assert all(restrict(t,True)==L and restrict(t,False)==R for t in trees)
    return p,L,R
def main():
    with (B/'full_geometry_compressed_work_08.pkl').open('rb') as f:w=pickle.load(f)
    with (B/'full_geometry_sparse_work_00.pkl').open('rb') as f:s=pickle.load(f)
    Z=json.loads((B/'native10_source_actions.json').read_text());N=len(Z['trees']);assert s['N']==N==16796
    def strip(v):return tuple(map(strip,v)) if isinstance(v,list) else v
    T=[skeleton(strip(t)) for t in Z['trees']];bypi={};geometry=0
    for a,pi in w['projections'].items():
        if len(pi)>1:
            assert reconstruct([T[v] for v in pi])==skeleton(w['A'][a],2)
            assert pi not in bypi;bypi[pi]=a;geometry+=1
    codes=[bypi[pi]*N+b for b,pi in w['features']];assert len(set(codes))==len(codes)
    assert s['A']==w['A'] and s['A_index']==w['A_index'] and s['cursor']==w['cursor'] and s['source_couplings']==w['source_couplings'] and s['actions']==w['actions'] and s['actions2']==w['actions2'] and s['projections']==w['projections']
    assert s['lower']=={c:v for c,v in zip(codes,w['lower']) if v>0}
    assert s['pred']=={c:j for c,j in zip(codes,w['pred']) if c in s['lower']}
    assert len(s['updates'])==len(w['updates'])
    for old,new in zip(w['updates'],s['updates']):
        assert all(new[k]==v for k,v in old.items())
        assert new['source_code']==(None if old['source_feature'] is None else codes[old['source_feature']]) and new['target_code']==codes[old['target_feature']]
    assert all(u is None or w['lower'][j]<=u for j,u in enumerate(w['upper'])) and not w['pending'] and w['counter'] is None
    groups={k:[] for k in range(1,11)}
    for b,t in enumerate(Z['trees']):groups[t[0]].append(b)
    rank={b:i for bb in groups.values() for i,b in enumerate(bb)};ap,bp,xp=w['cursor'];expected=[]
    for c in s['lower']:
        a,b=divmod(c,N)
        if a>ap or a==ap and rank[b]>=bp:expected.append(c)
    assert expected==s['pending']
    # Retention, not a repeated source-semantic or sign audit: every historical
    # mutable edge is present in the declared re-generation grammar.
    actionsets={a:set(opts)|{(x,at,1,None) for x,at in w['actions'].get(a,[])} for a,opts in w['actions2'].items()}
    edges=0
    for (u,v),e in w['edges'].items():
        a,b=divmod(codes[u],N);at,bt=divmod(codes[v],N)
        assert e['source_A']==w['A'][a] and e['actual_A_target']==w['A'][at]
        action=(e['target_actual_key'],at,e['H'],e['DELETE_helper'])
        assert action in actionsets.get(a,{(x,t,1,None) for x,t in w['actions'].get(a,[])})
        assert (b,bt)==(e['source_B_core_index'],e['B_target_core_index']) and e['price']==2*e['H']-e['Q']
        edges+=1
        if edges%32768==0 and time.process_time()-START>CAP-2:raise TimeoutError('CONVERSION_RETENTION_AUDIT_CAP')
    assert edges==2135234 and len(s['lower'])==21887 and len(s['updates'])==24320
    assert time.process_time()-START<CAP-1
    files=('SPARSE_SOURCE_REGENERATION.md','full_geometry_sparse_work_00.pkl','full_geometry_sparse_conversion.json','audit_verify67.py')
    out('sparse_source_conversion_independent_audit.json',{'status':'PASS_EXACT_SPARSE_SOURCE_PREFIX_CONVERSION','profiles_including_implicit_zeros_verified':len(codes),'retained_positive_labels':len(s['lower']),'old_edges_retained_by_complete_regeneration_grammar':edges,'causal_records_preserved':len(s['updates']),'branched_geometry_reconstruction_instances':geometry,'cursor_preserved':s['cursor'],'pending_unprocessed_positive_source_rows':len(s['pending']),'fixed_endpoint_bounds':'satisfied now; regenerated on future source-label rises','future_propagation_requirement':'ALL H1 actions plus H2/helper actions, including H1 actions omitted from the old phase2-only seed enumeration','source_queries':0,'source_engine_calls':0,'complete_source_funding_certificate':False,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in files}})
    print(json.dumps({'status':'PASS_EXACT_SPARSE_CONVERSION','old_profiles':len(codes),'positive_labels':len(s['lower']),'retained_edges':edges,'source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify67_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
