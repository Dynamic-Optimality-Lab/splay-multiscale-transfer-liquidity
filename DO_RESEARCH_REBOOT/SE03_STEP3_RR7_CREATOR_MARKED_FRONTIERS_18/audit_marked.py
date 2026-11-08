"""Producer watched-edge source construction and explicit counter repair.
Old per-operation source data reused; no new engine/audit calls.
"""
import importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent
def mod(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=mod('creator18marked',P/'SE03_STEP3_SOURCE_FORCED_MULTICOMPONENT_ESCAPE_17/audit_lineage.py')
L=mod('channels18marked',P/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/leaf_channels.py')
A=mod('augment18marked',P/'SE03_STEP3_NONLOCAL_OWNERSHIP_TRANSFER_16/adaptive_transfer.py')
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
def unpack(v):return {tuple(x['demand']):tuple(x['unit']) for x in v}
def pack(v):return [{'demand':d,'unit':u} for d,u in sorted(v.items())]
def outer(parent,x,parents):
    q=parents[parent]
    while q is not None:
        if x<parent and q<parent:return False
        if x>parent and q>parent:return False
        q=parents[q]
    return True
def births(rows,M):
    allnew=[]
    for i,t in enumerate(rows):
        bef=C.parents(t['before'][0]);aft=C.parents(t['after'][0]);v=t['target'];groups={}
        for x in sorted(M):
            par=aft[x]
            if x==v or par is None or par==bef[x]:continue
            qualifies=par not in M or outer(par,x,aft)
            operand=x if par==v else par
            jj=[j for j,e in enumerate(t['A_events'],1) if operand in (e.get('G'),e.get('P'))]
            assert len(jj)==1
            item={'row_index':i,'edge':(par,x),'creator_event':jj[0],
                'source_occurrence':t['occurrence'],'qualified':qualifies,'unit':None,
                'parent_marked':par in M,'frame':t['A_events'][jj[0]-1]}
            allnew.append(item)
            if qualifies:groups.setdefault(jj[0],[]).append(item)
        for j,items in groups.items():
            assert len(items)<=2,(t['occurrence'],j,[z['edge'] for z in items])
            for bit,item in enumerate(sorted(items,key=lambda z:z['edge'])):item['unit']=(t['occurrence'],j,bit)
    return allnew
def analyze(label,rows):
    M={t['target'] for t in rows if t['genuine_F']};v=L.build(rows,M);cc=births(rows,M)
    by={t['occurrence']:i for i,t in enumerate(rows)};hi={u:d for d,u in v['h'].items()};claims=[];uncovered=[];used=set()
    for raw in sorted(v['R']):
        d=tuple(raw);m=next(m for m in v['macros'] if d in [tuple(z) for z in m['branch_unpaid']])
        if (m['H'],m['Q'],len(m['branch']),m['z'])!=(1,2,2,1):uncovered.append(d);continue
        positives=[by[t] for t in m['occurrences'] if rows[by[t]]['a']]
        assert len(positives)==1;k=positives[0];t=rows[k];par=C.parents(t['before'][0]);x=m['target']
        if par[x] not in M:edge=(par[x],x);kind='ANONYMOUS_PARENT_DOUBLE'
        elif len(t['A_path'])==1:edge=(par[x],x);kind='MARKED_PARENT_ZIG'
        else:edge=(t['before'][0][0],par[x]);kind='MARKED_PARENT_DOUBLE_OUTER_EDGE'
        after=C.parents(t['after'][0]);assert par[edge[1]]==edge[0] and after[edge[1]]!=edge[0]
        earlier=[z for z in cc if tuple(z['edge'])==edge and z['row_index']<k]
        c=max(earlier,key=lambda z:z['row_index']) if earlier else max((z for z in cc if tuple(z['edge'])==edge),key=lambda z:z['row_index'])
        assert c['qualified'],('inner edge supposedly reached root',label,d,c)
        unit=tuple(c['unit']);assert unit not in used;used.add(unit)
        claims.append({'frontier':d,'kind':kind,'watched_edge':edge,'creator':c,
            'comparison_preimage':hi.get(unit),'protected':unit not in hi})
    return {'label':label,'claims':claims,'outside_H1_zero_class':uncovered,
        'raw_candidates_distinct':True,'all_comparison_protected':all(c['protected'] for c in claims)}
def main():
    profiles=[]
    for name in ('leaf_source_certificates2.json','zero_run_source_certificates.json'):
        for i,f in enumerate(read(P/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15'/name)['reports']):
            profiles.append(analyze(name+':'+str(i),f['rows']))
    data=read(B/'rr7_owner_certificates.json');repairs=[]
    for report in data['reports']:
        rows=report['rows'];M={t['target'] for t in rows if t['genuine_F']};v=L.build(rows,M)
        profiles.append(analyze('new_RR7_'+str(report['erased']),rows))
        if not report['qualifying_RR7_collisions']:continue
        prior=unpack(report['prior']);f6=unpack(report['f6']);fi={u:d for d,u in f6.items()};ai={u:d for d,u in prior.items()}
        full=dict(v['h']);mates=[]
        for c in report['qualifying_RR7_collisions']:
            d=tuple(c['first_undefined_frontier']);u=tuple(c['creator_unit']);mate=(u[0],u[1],1-u[2])
            assert mate not in set(full.values());full[d]=mate
            mates.append({'frontier':d,'old_kappa':u,'mate':mate,'old_effective_owner':ai.get(mate),
                'archived_auxiliary_owner':fi.get(mate),'old_comparison_owner_of_kappa':c['existing_comparison_preimage']})
        # This constructed source has one branch hole; do not assume that generally.
        assert set(full)==v['D'] and len(set(full.values()))==len(full)
        additions={d:u for d,u in full.items() if d not in v['h']}
        result=A.extend(v['D'],v['U'],prior,v['h'],lambda d,image:(additions[d],{'kind':'EXACT_COUNTER_MATE_CASE','demand':d}) if d in additions else None)
        assert not result['blocked'] and set(result['allocation'])==v['D']
        repairs.append({'erased':report['erased'],'mirrored':report['mirrored'],'actual_interval':report['actual_interval'],
            'mate_cases':mates,'comparison':pack(full),'allocation':pack(result['allocation']),
            'old_a':report['prior'],'all_old_a_values_fixed':True,'paths':result['paths'],
            'count_A':sum(t['a'] for t in rows),'count_QF':sum(t['qF'] for t in rows),'count_QE':sum(t['qE'] for t in rows),
            'scope':'complete exact source repair, not a universal mate theorem'})
    out('marked_watched_edge_profiles.json',{'status':'PRODUCER_DERIVATIONS_AUDIT_PENDING','profiles':profiles,
        'universal_usable_escape_proved':False,'source_engine_calls':0})
    out('rr7_counter_repairs.json',{'status':'PRODUCER_EXACT_SOURCE_REPAIR_AUDIT_PENDING','repairs':repairs})
    print(json.dumps({'status':'MARKED_WATCH_AND_MATE_PRODUCER_PASS','source_engine_calls':0,
        'profiles':[{'label':x['label'],'types':[c['kind'] for c in x['claims']],
            'collisions':sum(not c['protected'] for c in x['claims'])} for x in profiles],
        'mate_repairs':[{'erased':x['erased'],'pairs':x['mate_cases'],'A_QF_QE':[x['count_A'],x['count_QF'],x['count_QE']]} for x in repairs]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_marked_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':0,'new_finite_tests':0,'old_semantic_rows_replayed':0})
