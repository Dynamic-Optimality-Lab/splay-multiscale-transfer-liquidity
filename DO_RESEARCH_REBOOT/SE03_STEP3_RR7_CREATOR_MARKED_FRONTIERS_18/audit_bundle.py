"""Exact nonlocal repayment of the new overfull LOW prototype.
This proves one source case; it does not assume a universal ancestry bound.
"""
import json,time
import audit_marked as W
B=W.B
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
def main():
    s=W.read(B/'overfull_source_result.json');rows=s['rows'];M={t['target'] for t in rows if t['genuine_F']};v=W.L.build(rows,M)
    prof=W.analyze('bundled_LOW_source',rows);groups={};by={t['occurrence']:t for t in rows}
    for q in prof['claims']:
        m=next(m for m in v['macros'] if q['creator']['source_occurrence'] in m['occurrences'])
        groups.setdefault(m['macro'],{'macro':m,'claims':[]})['claims'].append(q)
    assert set(groups)=={0,1,5}
    assert groups[1]['macro']['H']==1
    direct={tuple(q['frontier']) for q in groups[0]['claims']}
    producer_front=tuple(groups[0]['claims'][0]['frontier'])
    assert producer_front[0]==groups[1]['macro']['occurrences'][-1]
    bundled=sorted(direct|{tuple(q['frontier']) for q in groups[1]['claims']})
    full=dict(v['h']);pairs=[]
    for group,claims in ((groups[0],bundled),(groups[5],[tuple(q['frontier']) for q in groups[5]['claims']])):
        m=group['macro'];us=[(t,j,b) for t in m['occurrences'] for j in range(1,by[t]['a']+1) for b in (0,1)]
        tail=[u for u in us if u not in set(v['h'].values())]
        assert len(tail)>=len(claims)
        pp=list(zip(claims,tail[-len(claims):]));full.update(pp);pairs+=pp
    assert set(full)==v['D'] and len(set(full.values()))==len(full) and set(full.values())<=v['U']
    T=len(s['word']);base=len(s['reaching_prefix'])+T;tau=lambda z:(z[0]+base,*z[1:])
    actual={tau(d):tau(u) for d,u in full.items()}
    assert all(base<z[0]<=base+T for z in set(actual)|set(actual.values()))
    out('overfull_nonlocal_bundle_repayment.json',{'status':'EXACT_SOURCE_DERIVATION_AUDIT_PENDING',
        'source':'overfull_source_result.json','word_length':T,'selected_prefix_word_copies':1,
        'actual_interval':[base+1,base+T],'relative_source_pairs':pairs,
        'actual_source_pairs':[(tau(d),tau(u)) for d,u in pairs],
        'relative_comparison':W.pack(full),'actual_comparison':W.pack(actual),
        'A':sum(t['a'] for t in rows),'QF':sum(t['qF'] for t in rows),
        'bundled_frontiers':bundled,'bundle_source_macro':groups[0]['macro'],
        'original_auxiliary_owner_map':'not constructed for this extra source; owner composition remains parametric in a supplied certified map',
        'universal_bundle_capacity_claim':False})
    print(json.dumps({'status':'EXACT_BUNDLED_SOURCE_REPAYMENT_PASS','relative_pairs':pairs,
        'actual_interval':[base+1,base+T],'A_QF':[sum(t['a'] for t in rows),sum(t['qF'] for t in rows)]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_bundle_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':0,'new_finite_tests':0,'old_semantic_rows_replayed':0})
