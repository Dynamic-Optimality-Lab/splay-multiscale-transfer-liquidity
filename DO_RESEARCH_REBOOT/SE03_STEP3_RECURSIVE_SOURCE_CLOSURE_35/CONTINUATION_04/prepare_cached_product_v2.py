"""Prepare only pinned, previously checked source transitions; no splay engine."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;P=C.parent
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();M=set(range(1,14,2))
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def freeze(t):
    if isinstance(t,str):
        assert t.startswith('F') and t[1:].isdigit()
        return None # explicit legal empty specialization of certified inert F-gap terms
    return None if t is None else (t[0],freeze(t[1]),freeze(t[2]))
def mirror(t):return None if t is None else (14-t[0],mirror(t[2]),mirror(t[1]))
def keys(t):return [] if t is None else keys(t[1])+[t[0]]+keys(t[2])
def core(t):
    if t is None:return set()
    l,r=core(t[1]),core(t[2]);return l|r|{t[0]} if t[0] in M or l or r else set()
def main():
    prior=read(C/'CONTINUATION_03/campaign_manifest.json')
    for n,h in prior['artifacts'].items():assert sha(C/'CONTINUATION_03'/n)==h
    nativepath=B/'native10_source_actions.json';a=read(nativepath);nativeaudit=read(B/'native10_source_independent_audit.json')
    assert sha(nativepath)==nativeaudit['input_sha256']=='36438e382a4fe50eca206a15bbb54cc8510effee1311addbf755486b839e8f95'
    srcs=[
      (B/'SOURCE_JOINT_REPAIR_03/actual_monotone_return_source.json','period_rows',B/'SOURCE_JOINT_REPAIR_03/independent_source_audit.json','input_sha256'),
      (P/'SE03_STEP3_NONEXTREMAL_SHALLOW_HELPER_REPAYMENT_30/nonextremal_source_countercertificate.json','rows',P/'SE03_STEP3_NONEXTREMAL_SHALLOW_HELPER_REPAYMENT_30/independent_audit.json','input_sha256'),
      (P/'SE03_STEP3_GUARDED_E4_PHYSICAL_ESCAPE_28/shortened_source_control.json','rows',P/'SE03_STEP3_GUARDED_E4_PHYSICAL_ESCAPE_28/independent_audit.json','input_sha256'),
      (P/'SE03_STEP3_GUARDED_E4_PHYSICAL_ESCAPE_28/catchment_forcing_countercertificate.json','rows',P/'SE03_STEP3_GUARDED_E4_PHYSICAL_ESCAPE_28/family_independent_audit.json','sha256')]
    sources=[];trees=[];index={};edges=[];lookup={}
    def node(t):
        if t not in index:index[t]=len(trees);trees.append(t)
        return index[t]
    for path,field,receipt,hashfield in srcs:
        checked=read(receipt)[hashfield];matches=[h for n,h in checked.items() if Path(n.replace('\\','/')).name==path.name]
        assert matches==[sha(path)]
        source=read(path);sources.append({'path':str(path),'sha256':sha(path),'rows_field':field,'audit':str(receipt),'audit_sha256':sha(receipt)})
        for i,r in enumerate(source[field]):
            if not r['genuine_F']:continue
            x=r.get('key',r.get('target'));assert x in M
            s=freeze(r['BF_before'] if 'BF_before' in r else r['before'][1])
            t=freeze(r['BF_after'] if 'BF_after' in r else r['after'][1]);q=r['qF']
            assert keys(s)==keys(t)==list(range(1,14)) and s[0]!=x and t[0]==x
            if len(core(s))!=13 or len(core(t))!=13:continue
            for reflected in (False,True):
                ss,tt,xx=(mirror(s),mirror(t),14-x) if reflected else (s,t,x)
                si,ti=node(ss),node(tt);key=(si,xx)
                if key in lookup:assert lookup[key]==(ti,q);continue
                lookup[key]=(ti,q);edges.append({'source':si,'target':ti,'key':xx,'q':q,
                  'origin_source':len(sources)-1,'origin_row':i,'reflected':reflected})
    adj=[[] for _ in trees]
    for i,e in enumerate(edges):adj[e['source']].append(i)
    # Tarjan SCC on the small cached B graph, not on BST source queries.
    number={};low={};stack=[];on=set();components=[]
    def visit(v):
        number[v]=low[v]=len(number);stack.append(v);on.add(v)
        for ei in adj[v]:
            w=edges[ei]['target']
            if w not in number:visit(w);low[v]=min(low[v],low[w])
            elif w in on:low[v]=min(low[v],number[w])
        if low[v]==number[v]:
            comp=[]
            while True:
                w=stack.pop();on.remove(w);comp.append(w)
                if w==v:break
            components.append(comp)
    for v in range(len(trees)):
        if v not in number:visit(v)
    eligible=[]
    for comp in components:
        st=set(comp);labs={e['key'] for e in edges if e['source'] in st and e['target'] in st}
        if labs==M:eligible.append(sorted(comp))
    aset=[]
    native_marks={1,3,5,7,8,9,10};extras=[2,4,6]
    def internal(t):
        if t is None:return set()
        return ({t[0]} if t[1] is not None or t[2] is not None else set())|internal(t[1])|internal(t[2])
    internals=[internal(t) for t in a['trees']]
    for k in range(4):
        allowed=native_marks|set(extras[:k]);inactive=set(extras[k:])
        ids=[i for i,v in enumerate(internals) if not v.intersection(inactive)]
        assert len(ids)==[429,1430,4862,16796][k]
        aset.append({'extra_active':k,'allowed_native_keys':sorted(allowed),'A_tree_ids':ids})
    graph={'status':'PINNED_ORIGINAL_CACHE_PRODUCT_PREPARED','B_trees':trees,'B_edges':edges,
      'all_genuine_marks':sorted(M),'eligible_B_SCCs':eligible,'A_submodels':aset,
      'native_to_physical':[1,2,3,4,5,6,7,9,11,13],'always_rigid_omitted_physical':[8,10,12],
      'sources':sources,'native_actions':str(nativepath),'native_actions_sha256':sha(nativepath),
      'native_actions_audit_sha256':sha(B/'native10_source_independent_audit.json'),
      'source_queries':0,'source_engine_calls':0,'certified_F_gap_specialization':'all empty, new lifted source instance; historical sources unchanged',
      'new_product_compositions_are_not_original_engine_calls':True,'JR35':'OPEN'}
    out('cached_product_inputs.json',graph)
    out('cached_product_inventory.json',{'status':graph['status'],'B_vertices':len(trees),'B_edges':len(edges),
      'eligible_B_SCC_sizes':list(map(len,eligible)),'A_submodel_counts':[len(v['A_tree_ids']) for v in aset],
      'max_full_native10_product_states':len(trees)*16796,'source_queries':0,'source_engine_calls':0,'JR35':'OPEN'})
    print(json.dumps(read(F/'cached_product_inventory.json')),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof181_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
