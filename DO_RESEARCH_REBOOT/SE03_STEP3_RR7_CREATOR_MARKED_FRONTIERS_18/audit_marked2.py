"""Continue after the documented extra-hole failure. No failed result
is promoted; all additional original demands are explicitly covered.
"""
import json,time
import audit_marked as V
B=V.B;P=V.P
def main():
    profiles=[]
    for name in ('leaf_source_certificates2.json','zero_run_source_certificates.json'):
        for i,f in enumerate(V.read(P/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15'/name)['reports']):
            profiles.append(V.analyze(name+':'+str(i),f['rows']))
    data=V.read(B/'rr7_owner_certificates.json');repairs=[]
    for report in data['reports']:
        rows=report['rows'];M={t['target'] for t in rows if t['genuine_F']};v=V.L.build(rows,M)
        profiles.append(V.analyze('new_RR7_'+str(report['erased']),rows))
        if not report['qualifying_RR7_collisions']:continue
        prior=V.unpack(report['prior']);f6=V.unpack(report['f6']);fi={u:d for d,u in f6.items()};ai={u:d for d,u in prior.items()}
        full=dict(v['h']);mates=[]
        for c in report['qualifying_RR7_collisions']:
            d=tuple(c['first_undefined_frontier']);u=tuple(c['creator_unit']);mate=(u[0],u[1],1-u[2])
            assert mate not in set(full.values());full[d]=mate
            mates.append({'frontier':d,'old_kappa':u,'mate':mate,'old_effective_owner':ai.get(mate),
                'archived_auxiliary_owner':fi.get(mate),'old_comparison_owner_of_kappa':c['existing_comparison_preimage']})
        by={t['occurrence']:t for t in rows};end=report['base']+5
        supplier=next(m for m in v['macros'] if m['occurrences'][-1]==end)
        assert supplier['Q']==1
        units=[(t,j,b) for t in supplier['occurrences'] for j in range(1,by[t]['a']+1) for b in (0,1)]
        protected=[u for u in units[2:] if u not in set(full.values())]
        extra=sorted(v['D']-set(full));assert len(protected)>=len(extra)
        extra_pairs=list(zip(extra,protected));full.update(extra_pairs)
        assert set(full)==v['D'] and len(set(full.values()))==len(full)
        additions={d:u for d,u in full.items() if d not in v['h']}
        result=V.A.extend(v['D'],v['U'],prior,v['h'],lambda d,image:(additions[d],{'kind':'EXACT_SOURCE_MATE_PLUS_Q1_TAIL_COVER','demand':d}) if d in additions else None)
        assert not result['blocked'] and set(result['allocation'])==v['D']
        repairs.append({'erased':report['erased'],'mirrored':report['mirrored'],'actual_interval':report['actual_interval'],
            'mate_cases':mates,'additional_original_holes':extra,'additional_source_pairs':extra_pairs,
            'Q1_supplier':supplier,'comparison':V.pack(full),'allocation':V.pack(result['allocation']),
            'old_a':report['prior'],'all_old_a_values_fixed':True,'paths':result['paths'],
            'count_A':sum(t['a'] for t in rows),'count_QF':sum(t['qF'] for t in rows),'count_QE':sum(t['qE'] for t in rows),
            'scope':'complete exact source repair; not a universal mate or supplier theorem'})
    V.out('marked_watched_edge_profiles.json',{'status':'PRODUCER_DERIVATIONS_AUDIT_PENDING','profiles':profiles,
        'universal_usable_escape_proved':False,'source_engine_calls':0})
    V.out('rr7_counter_repairs.json',{'status':'PRODUCER_EXACT_SOURCE_REPAIR_AUDIT_PENDING','repairs':repairs,
        'supersedes_failed_assertion':'marked phase assumed one hole; current source explicitly includes all additional holes'})
    print(json.dumps({'status':'MARKED_WATCH_AND_FULL_SOURCE_REPAIR_PRODUCER_PASS',
        'profiles':[{'label':x['label'],'types':[c['kind'] for c in x['claims']],
            'collisions':sum(not c['protected'] for c in x['claims']),'outside_zero_class':x['outside_H1_zero_class']} for x in profiles],
        'repairs':[{'erased':x['erased'],'mate':x['mate_cases'],'additional_holes':x['additional_original_holes'],
            'A_QF_QE':[x['count_A'],x['count_QF'],x['count_QE']]} for x in repairs]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:V.out('audit_marked2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':0,'new_finite_tests':0,'old_semantic_rows_replayed':0})
