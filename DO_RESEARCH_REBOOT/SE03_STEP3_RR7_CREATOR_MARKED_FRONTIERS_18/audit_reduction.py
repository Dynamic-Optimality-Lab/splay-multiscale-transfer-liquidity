"""Producer projection of NEW repaired maps and measured creator-group
reduction. No old source replay or independent verification.
"""
import json,time
import audit_marked as W
B=W.B;P=W.P
def read(n):return json.loads((B/n).read_text(encoding='utf-8'))
def main():
    aligned=read('fully_aligned_countercertificates.json')['cases'];repairs=read('creator_macro_tail_repairs.json')['repairs'];outputs=[]
    for c in aligned:
        r=next(r for r in repairs if r['erased']==c['erased'] and r['mirrored']==c['mirrored'])
        shift=c['coordinate_shift'];tau=lambda z:(z[0]+shift,*z[1:])
        f={tau(z['demand']):tau(z['unit']) for z in r['allocation']}
        h={tau(z['demand']):tau(z['unit']) for z in r['comparison']}
        prior=W.unpack(c['maps']['prior']);locks=W.unpack(c['maps']['locked_common'])
        rows=c['rows'];D={(t['occurrence'],j) for t in rows for j in range(1,t['qF']+1)}
        U={(t['occurrence'],j,b) for t in rows for j in range(1,t['a']+1) for b in (0,1)}
        assert set(f)==set(h)==D and len(set(f.values()))==len(f) and len(set(h.values()))==len(h)
        assert set(f.values())|set(h.values())<=U
        assert all(f[d]==u for d,u in prior.items()) and all(f[d]==u for d,u in locks.items())
        outputs.append({'erased':c['erased'],'mirrored':c['mirrored'],'actual_interval':c['actual_interval'],
            'actual_allocation':W.pack(f),'independent_source_comparison':W.pack(h),'old_a':W.pack(prior),
            'all_old_a_and_common_values_fixed':True,
            'source_pairs':[dict(z,frontier=tau(z['frontier']),old_watched_creator=tau(z['old_watched_creator']),replacement=tau(z['replacement'])) for z in r['source_pairs']],
            'full_recent_closes':c['initial_full_recent']==c['final_full_recent'],
            'erased_recent_closes':c['initial_erased_recent']==c['final_erased_recent']})
    sources=[]
    # Old source data are used only for new group/capacity quantities.
    for name in ('leaf_source_certificates2.json','zero_run_source_certificates.json'):
        for i,s in enumerate(W.read(P/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15'/name)['reports']):sources.append((name+':'+str(i),s['rows']))
    for c in aligned:sources.append(('aligned_'+str(c['erased'])+'_'+str(c['mirrored']),c['rows']))
    ov=read('overfull_source_result.json')
    if ov['status'].startswith('ACTUAL_CLOSED'):sources.append(('overfull_LOW_source',ov['rows']))
    profiles=[]
    for label,rows in sources:
        M={t['target'] for t in rows if t['genuine_F']};v=W.L.build(rows,M);profile=W.analyze(label,rows)
        groups={};by={t['occurrence']:t for t in rows};extended=dict(v['h'])
        for q in profile['claims']:
            m=next(m for m in v['macros'] if q['creator']['source_occurrence'] in m['occurrences'])
            groups.setdefault(m['macro'],{'macro':m,'claims':[]})['claims'].append(q)
        caps=[]
        for g in groups.values():
            m=g['macro'];qs=sorted(g['claims'],key=lambda z:z['frontier']);count=len(qs)
            children={tuple(q['watched_edge'])[1] for q in qs}
            assert len(children)==count and count<=min(len(M)-1,2*m['H'])
            us=[(t,j,b) for t in m['occurrences'] for j in range(1,by[t]['a']+1) for b in (0,1)]
            tail=[u for u in us if u not in set(v['h'].values())]
            msize=min(2*m['H'],len(m['branch'])+m['z']);assert len(tail)==2*m['H']-msize
            num=min(count,len(tail));pairs=list(zip([tuple(z['frontier']) for z in qs[:num]],tail[-num:] if num else []))
            extended.update(pairs)
            caps.append({'creator_macro':m['macro'],'H':m['H'],'m':msize,'g':count,'tail':len(tail),
                'new_source_pairs':pairs,'remaining_group_deficit':count-num})
        assert len(set(extended.values()))==len(extended)
        profiles.append({'source':label,'r':len(M),'creator_groups':caps,
            'remaining_comparison_holes':sorted(v['D']-set(extended)),
            'other_frontiers_not_claimed_by_H1_zero_rule':profile['outside_H1_zero_class']})
    W.out('fully_aligned_source_repairs.json',{'status':'PRODUCER_AUDIT_PENDING','cases':outputs})
    W.out('creator_group_reduction_profiles.json',{'status':'PRODUCER_ILLUSTRATIONS_OF_SYMBOLIC_REDUCTION_AUDIT_PENDING','profiles':profiles,
        'universal_full_source_escape_proved':False})
    print(json.dumps({'status':'ALIGNED_REPAIR_AND_GROUP_REDUCTION_PRODUCER_PASS','aligned_cases':len(outputs),
        'overfull_profile':next((x for x in profiles if x['source']=='overfull_LOW_source'),None)}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:W.out('audit_reduction_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':0,'new_finite_tests':0,'old_semantic_rows_replayed':0})
