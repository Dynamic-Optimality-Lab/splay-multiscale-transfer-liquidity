"""Test convex-hull compatibility of the FULL-spectrum state rule.
This alters only a sufficient extension condition, never the old certificate.
"""
import json,pickle,time,sys,collections
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    with (B/'B_full_spectrum_work_01.pkl').open('rb') as f:w=pickle.load(f)
    labels=[];upper=[];base=[];pred=[];updates=[]
    for b,counts in w['features']:
        vals=[d for d,c in enumerate(counts) if c];base.append(min(vals));labels.append(min(vals));upper.append(max(vals));pred.append(None)
    q=collections.deque(range(len(labels)));pending=set(q);bad=None;chain=[]
    while q:
        u=q.popleft();pending.remove(u)
        for v,e in w['outgoing'].get(u,{}).items():
            value=labels[u]-e['price']
            if value<=labels[v]:continue
            updates.append({'edge':e,'source_label':labels[u],'target_label':value,'parent':pred[u]});pred[v]=len(updates)-1;labels[v]=value
            if value>upper[v]:bad={'feature':v,'B':w['features'][v][0],'spectrum_counts':w['features'][v][1],'required':value,'upper':upper[v]};break
            if v not in pending:q.append(v);pending.add(v)
        if bad or time.process_time()-START>CAP-2:break
    start_lower=None
    if bad:
        j=pred[bad['feature']]
        while j is not None:chain.append(updates[j]['edge']);start_lower=updates[j]['source_label'];j=updates[j]['parent']
        chain.reverse();assert sum(e['price'] for e in chain)+bad['upper']-start_lower<0
    result={'status':'FULL_B_FULL_SPECTRUM_ALL_CONVEX_SELECTOR_RULES_REFUTED_CANDIDATE' if bad else 'CONVEX_SELECTOR_SOURCE_PREFIX_FEASIBLE' if not q else 'CONVEX_SELECTOR_SOURCE_PREFIX_CHECK_OPEN','contradiction':bad,'causal_edges':chain,'start_required_lower':start_lower,'variables':len(labels),'source_edge_constraints':len(w['edges']),'maximum_label':max(labels),'new_extra_assumption':'min(spectrum)<=F(B,spectrum)<=max(spectrum); no source rule is weakened','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'};out('B_full_spectrum_convex_selector_result.json',result)
    if not bad and not q:
        w['labels']=labels;w['upper']=upper;w['base']=base;w['pred']=pred;w['updates']=[];w['depth']=[0]*len(labels);w['bounds_mode']='convex_selector';w['pending']=[]
        # Do not reuse old predecessor indices with an empty update archive.
        w['pred']=[None]*len(labels)
        with (B/'B_full_spectrum_selector_seed.pkl').open('xb') as f:pickle.dump(w,f,protocol=5)
    print(json.dumps({k:v for k,v in result.items() if k!='causal_edges'}));print(json.dumps([{'BF':[e['source_B_core_index'],e['B_target_core_index']],'multisets':[e['source_value_multiset'],e['target_value_multiset']],'price':e['price']} for e in chain]))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof98_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
