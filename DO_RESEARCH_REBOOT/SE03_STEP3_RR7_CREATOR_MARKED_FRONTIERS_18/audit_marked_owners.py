"""New actual owner variants for the marked-parent class and source-local
macro-tail replacements. Producer only; no independent allowance consumed.
"""
import json,time
import audit_rr7_owners as V
import audit_marked as W
B=V.B
def main():
    c=json.loads((B/'rr7_source_candidate.json').read_text());old=json.loads((B/'rr7_owner_certificates.json').read_text())
    tried=[];found=[]
    for z in (5,7,3,9,11,13):
        r=V.one(c,z,True);M={t['target'] for t in r['rows'] if t['genuine_F']};v=V.L.build(r['rows'],M)
        f6=V.unpack(r['f6']);lock={d:f6[d] for d in v['D']&set(f6)};ex=V.X.exchange(v['D'],v['U'],lock,v['h0'])
        Rnat=v['D']-set(v['h0']);deep={tuple(d) for q in v['deep'] for d in q['natural_excess']}
        profile=W.analyze('new_marked_erasure_'+str(z),r['rows']);claims={tuple(q['frontier']):q for q in profile['claims']}
        qual=[]
        for path in r['partial_owner_paths']:
            if path['frontier'] is None:continue
            root=tuple(path['root']);d=tuple(path['frontier']);alpha=root if root in Rnat else ex['blocked'][root]['owner']
            q=claims.get(d)
            if alpha in deep and q and q['kind'].startswith('MARKED_PARENT'):
                qual.append({'root':root,'deep_anchor':alpha,'first_frontier':d,'path':path,'watched_claim':q})
        r['qualifying_marked_first_frontiers']=qual;r['watched_profile']=profile;tried.append(r)
        print(json.dumps({'erased':z,'u':r['u'],'core6':r['six_key_core'],'marked_deep_frontiers':len(qual)}),flush=True)
        if qual:found.append(r);break
    repairs=[]
    for r in old['reports']+found:
        rows=r['rows'];M={t['target'] for t in rows if t['genuine_F']};v=V.L.build(rows,M)
        profile=W.analyze('local_macro_tail_'+str(r['erased'])+'_'+str(r['mirrored']),rows)
        assert not profile['outside_H1_zero_class'];groups={}
        for q in profile['claims']:
            creator_t=q['creator']['source_occurrence']
            m=next(m for m in v['macros'] if creator_t in m['occurrences'])
            groups.setdefault(m['macro'],{'macro':m,'claims':[]})['claims'].append(q)
        by={t['occurrence']:t for t in rows};full=dict(v['h']);source_pairs=[]
        for group in groups.values():
            m=group['macro'];us=[(t,j,b) for t in m['occurrences'] for j in range(1,by[t]['a']+1) for b in (0,1)]
            tail=[u for u in us if u not in set(v['h'].values())]
            qs=sorted(group['claims'],key=lambda q:q['frontier']);assert len(tail)>=len(qs)
            selected=tail[-len(qs):]
            for q,u in zip(qs,selected):
                d=tuple(q['frontier']);full[d]=u
                source_pairs.append({'frontier':d,'old_watched_creator':q['creator']['unit'],
                    'replacement':u,'creator_macro':m['macro'],'macro_H_Q':[m['H'],m['Q']],
                    'macro_beta_z':[len(m['branch']),m['z']]})
        assert set(full)==v['D'] and len(set(full.values()))==len(full)
        prior=V.unpack(r['prior']);f6=V.unpack(r['f6']);ai={u:d for d,u in prior.items()};fi={u:d for d,u in f6.items()}
        extra={d:u for d,u in full.items() if d not in v['h']}
        result=W.A.extend(v['D'],v['U'],prior,v['h'],lambda d,image:(extra[d],{'kind':'EXACT_CREATOR_MACRO_TAIL','demand':d}) if d in extra else None)
        assert not result['blocked'] and set(result['allocation'])==v['D']
        for q in source_pairs:q['old_effective_owner']=ai.get(tuple(q['replacement']));q['archived_f6_owner']=fi.get(tuple(q['replacement']))
        repairs.append({'erased':r['erased'],'mirrored':r['mirrored'],'actual_interval':r['actual_interval'],
            'source_pairs':source_pairs,'comparison':V.pack(full),'allocation':V.pack(result['allocation']),
            'all_original_a_values_fixed':True,'paths':result['paths'],
            'scope':'this exact source has sufficient measured creator-macro tails; not a universal low-creator capacity theorem'})
    W.out('marked_owner_certificates.json',{'status':'PRODUCER_AUDIT_PENDING','reports':tried,
        'qualified_marked_parent_source_found':bool(found),'source_engine_calls':V.calls})
    W.out('creator_macro_tail_repairs.json',{'status':'PRODUCER_EXACT_FULL_SOURCE_REPAIRS_AUDIT_PENDING','repairs':repairs})
    print(json.dumps({'status':'MARKED_OWNER_AND_LOCAL_TAIL_PRODUCER_PASS',
        'qualified_marked':[{'erased':r['erased'],'core6':r['six_key_core'],'qualifiers':r['qualifying_marked_first_frontiers']} for r in found],
        'source_pairs':[r['source_pairs'] for r in repairs],'new_source_engine_calls':V.calls}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:W.out('audit_marked_owners_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':V.calls,'backend_source_rows_supplied':V.backend_rows,'new_finite_tests':0,'old_semantic_rows_replayed':0})
