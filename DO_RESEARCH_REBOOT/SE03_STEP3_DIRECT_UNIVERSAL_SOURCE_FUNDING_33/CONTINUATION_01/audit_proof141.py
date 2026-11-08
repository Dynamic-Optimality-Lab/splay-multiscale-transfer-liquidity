"""Any state-defined selector of an old contraction debt: exact-domain probe.
Monotone domain closure is sound for refutation. A passing prefix is not proof.
"""
import collections,json,pickle,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])

def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)

def main():
    Z=json.loads((B/'native10_source_actions.json').read_text());N=len(Z['trees']);mir=Z['mirror'];O=pickle.loads((B/'native10_B_modal_factored_debt.pkl').read_bytes())
    def D(a,b):return O['base'][b]+O['residual'].get(min(a*N+b,mir[a]*N+mir[b]),0)
    with (B/'full_geometry_compressed_work_08.pkl').open('rb') as f:w=pickle.load(f)
    domains=[];lo=[];pred=[];updates=[];bad=None;initial_complete=True
    def ceil_domain(j,value):return next((d for d in domains[j] if d>=value),None)
    def old_chain(v):
        chain=[];j=w['pred'][v]
        while j is not None:
            r=w['updates'][j];chain.append(r);j=r['parent']
        chain.reverse();return chain
    def feature(v):return {'id':v,'B':w['features'][v][0],'Pi':w['features'][v][1],'allowed_debts':domains[v]}
    def witness(v,requested,last_edge=None,source=None):
        records=[];j=pred[source] if source is not None else pred[v];start=source if source is not None else v
        while j is not None:
            r=updates[j];records.append(r);start=r['source'];j=r['parent']
        records.reverse()
        return {'target':feature(v),'required_raw_bound':requested,'original_source_upper':w['upper'][v],
                'original_source_upper_edge':w['upper_edge'][v],
                'initial_source':feature(start),'initial_continuous_bound':w['lower'][start],
                'initial_continuous_derivation':old_chain(start),'initial_domain_floor':next((x for x in domains[start] if x>=w['lower'][start]),None),
                'rounded_edge_derivation':[{**r,'source_profile':feature(r['source']),'target_profile':feature(r['target'])} for r in records],
                'last_edge':last_edge,'last_source_profile':feature(source) if source is not None else None}
    for j,(b,pi) in enumerate(w['features']):
        vals=tuple(sorted({D(a,b) for a in pi}));domains.append(vals);pred.append(None)
        value=ceil_domain(j,w['lower'][j]);lo.append(value)
        if value is None or w['upper'][j] is not None and value>w['upper'][j]:bad=witness(j,w['lower'][j] if value is None else value);break
        if time.process_time()-START>CAP-6:initial_complete=False;break
    steps=0;q=collections.deque(range(len(lo))) if initial_complete and bad is None else collections.deque();queued=set(q)
    while q and bad is None and time.process_time()-START<CAP-5:
        u=q.popleft();queued.remove(u)
        for v,e in w['outgoing'].get(u,{}).items():
            requested=lo[u]-e['price'];steps+=1
            if requested<=lo[v]:continue
            value=ceil_domain(v,requested)
            if value is None or w['upper'][v] is not None and value>w['upper'][v]:bad=witness(v,requested,e,u);break
            updates.append({'source':u,'target':v,'edge':e,'source_lower':lo[u],'raw_bound':requested,'rounded_bound':value,'parent':pred[u]});lo[v]=value;pred[v]=len(updates)-1
            if len(w['updates'])+len(updates)>=3900000:raise MemoryError('CUMULATIVE_CAUSAL_DAG_RESERVE')
            if v not in queued:queued.add(v);q.append(v)
    result={'status':'ANY_B_GEOMETRY_CONTRACTION_DEBT_SELECTOR_RAW_REFUTATION' if bad else 'EXACT_CONTRACTION_DEBT_DOMAIN_DISCOVERY_OPEN','counter':bad,'input_model':'full_geometry_compressed_work_08.pkl','input_mutable_profiles':len(w['features']),'profile_domains_built':len(domains),'initial_domains_complete':initial_complete,'constraint_relaxations':steps,'new_domain_updates':len(updates),'pending':len(q),'all_domains_saturated':initial_complete and not q and bad is None,'qualification':'No counter refutes arbitrary real-valued F; a counter refutes J(B,Pi) constrained to equal one of the old contraction debts. Full-A implications require the separate reconstruction lemma. Not a concatenated source path unless independently established.','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'}
    out('full_geometry_exact_debt_domain_candidate.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('counter','qualification')}))

if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof141_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
