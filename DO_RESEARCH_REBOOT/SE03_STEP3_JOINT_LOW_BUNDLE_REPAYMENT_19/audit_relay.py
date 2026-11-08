"""Producer profiles for the source-derived immediate old-root restriction.
No new splays/graphs/independent implementation checks.
"""
import importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;OLD=P/'SE03_STEP3_RR7_CREATOR_MARKED_FRONTIERS_18'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
def main():
    spec=importlib.util.spec_from_file_location('C19_reused_watch',OLD/'audit_marked.py')
    W=importlib.util.module_from_spec(spec);spec.loader.exec_module(W)
    reports=[]
    for label,source in (('A80','rr7_source_candidate.json'),('B82','overfull_source_result.json')):
        rows=read(OLD/source)['rows'];M={t['target'] for t in rows if t['genuine_F']}
        v=W.L.build(rows,M);births=W.births(rows,M);by={t['occurrence']:t for t in rows};profiles=[]
        for i,m in enumerate(v['macros']):
            if m['H']!=1:continue
            t=next(by[t] for t in m['occurrences'] if by[t]['a'])
            oldA=t['before'][0][0];oldB=by[m['occurrences'][0]]['before'][1][0]
            assert oldA==oldB and oldA in M and t['target']==m['target']
            born=[q for q in births if q['source_occurrence']==t['occurrence'] and q['qualified']]
            roots=[q for q in born if q['edge'][1]==oldA]
            assert len(roots)==1 and len(born)<=2
            nxt=v['macros'][(i+1)%len(v['macros'])]
            if nxt['target']==oldA:assert nxt['Q']==1
            profiles.append({'producer_macro':i,'H':1,'Q':m['Q'],'old_root':oldA,
              'producer_target':m['target'],'event_case':t['A_events'][0]['case'],
              'old_root_birth':roots[0]['edge'],'other_qualified_births':[q['edge'] for q in born if q not in roots],
              'next_macro':nxt['macro'],'next_target':nxt['target'],'next_Q':nxt['Q'],
              'restriction':'next H1/Q2 anonymous or marked-zig frontier cannot target old root; marked-parent outer-edge frontier is a separate exception'})
        reports.append({'source':label,'H1_producers':profiles})
    out('immediate_relay_profiles.json',{'status':'SOURCE_RESTRICTION_DERIVATION_AUDIT_PENDING',
      'reports':reports,'universal_replication_or_ancestry_capacity_claim':False,'source_engine_calls':0})
    print(json.dumps({'status':'IMMEDIATE_OLD_ROOT_RESTRICTION_PRODUCER_PASS',
      'counts':[(z['source'],len(z['H1_producers'])) for z in reports]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_relay_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
      'source_engine_calls':0,'new_finite_tests':0,'old_semantic_rows_replayed':0})
