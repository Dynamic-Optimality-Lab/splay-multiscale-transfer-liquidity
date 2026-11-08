"""Can ANY geometry-aware selector within the old contraction-debt range work?"""
import json,pickle,time,sys,hashlib,collections
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    Z=json.loads((B/'native10_source_actions.json').read_text());N=len(Z['trees']);mir=Z['mirror'];O=pickle.loads((B/'native10_B_modal_factored_debt.pkl').read_bytes());D=lambda a,b:O['base'][b]+O['residual'].get(min(a*N+b,mir[a]*N+mir[b]),0)
    with (B/'full_geometry_compressed_work_01.pkl').open('rb') as f:w=pickle.load(f)
    low=w['lower'];upper=w['upper'];upper_kind=['source']*len(low);lo=[];hi=[]
    for j,(b,pi) in enumerate(w['features']):
        vals=[D(a,b) for a in pi];mn,mx=min(vals),max(vals);lo.append(mn);hi.append(mx)
        if mn>low[j]:low[j]=mn;w['pred'][j]=None;w['depth'][j]=0
        if upper[j] is None or mx<upper[j]:upper[j]=mx;upper_kind[j]='selector_interval'
    def extract(v):
        chain=[];j=w['pred'][v];source=v;base=low[v]
        while j is not None:
            r=w['updates'][j];chain.append(r['edge']);source=r['source_feature'];base=r['source_lower'];j=r['parent']
        chain.reverse();return chain,source,base
    def counter(v):
        cc,ss,ll=extract(v);kind=upper_kind[v];endmax=upper[v]
        if kind=='source':e=w['upper_edge'][v];assert e is not None;cc.append(e);endmax=e['target_frozen_value']
        assert sum(e['price'] for e in cc)+endmax-ll<0
        return {'type':'ANY_OLD_CONTRACTION_DEBT_RANGE_SELECTOR','start_feature':ss,'start_lower':ll,'target_feature':v,'required':low[v],'upper':upper[v],'upper_kind':kind,'final_endpoint_bound':endmax,'causal_edges':cc}
    bad=None;q=collections.deque(range(len(low)));queued=set(q);steps=0
    for v in range(len(low)):
        if low[v]>upper[v]:bad=counter(v);break
    while q and bad is None and time.process_time()-START<CAP-6:
        u=q.popleft();queued.remove(u)
        for v,e in w['outgoing'].get(u,{}).items():
            value=low[u]-e['price'];steps+=1
            if value<=low[v]:continue
            w['updates'].append({'edge':e,'source_feature':u,'target_feature':v,'source_lower':low[u],'new_lower':value,'parent':w['pred'][u]});low[v]=value;w['pred'][v]=len(w['updates'])-1
            if value>upper[v]:bad=counter(v);break
            if v not in queued:q.append(v);queued.add(v)
    if bad:
        for e in bad['causal_edges']:
            for side,key,bkey in [('source','source_contraction_indices','source_B_core_index'),('target','target_contraction_indices','B_target_core_index')]:e[side+'_full_projection_debts']=[D(a,e[bkey]) for a in e[key]]
        bad['start_profile']=w['features'][bad['start_feature']] if bad['start_feature'] is not None else None;bad['target_profile']=w['features'][bad['target_feature']]
    out('full_geometry_selector_range_candidate.json',{'status':'ANY_FULL_GEOMETRY_CONTRACTION_RANGE_SELECTOR_REFUTATION_CANDIDATE' if bad else 'FULL_GEOMETRY_SELECTOR_RANGE_DISCOVERY_OPEN','counter':bad,'mutable_features':len(low),'constraint_relaxations':steps,'pending':len(q),'scope':'ANY nonnegative state rule, even retaining full actual A geometry, whose value lies between min/max D10 of all anchor contractions; source edges only relate matching full contraction profiles; fixed one-private gap2 inventory','qualification':'if different physical A states with identical full Pi occur between edges, the extracted chain refutes only F(B,Pi) interval selectors, not arbitrary full-A geometry; independent check must distinguish','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'});print(json.dumps({'status':'SELECTOR_RANGE_PROBE','counter':None if bad is None else {k:v for k,v in bad.items() if k not in ('causal_edges','start_profile','target_profile')},'edges':0 if bad is None else len(bad['causal_edges']),'steps':steps}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof123_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
