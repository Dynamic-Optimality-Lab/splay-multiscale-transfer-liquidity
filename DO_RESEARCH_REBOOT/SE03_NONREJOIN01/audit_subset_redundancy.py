"""Universal guard-subsumption certificates; no source states or masks tested."""
import collections,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
start=time.process_time();cap=float(sys.argv[1]);error=None
def out(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
try:
    d=json.loads((ROOT/'DO_RESEARCH_REBOOT/M3_XFER21/M3_CERTIFICATE.json').read_text())
    cs=[]
    for section,arr in [('Step4',d['parent_Step4_certificate']['clauses']),('completion',d['completion_clauses'])]:
        for i,q in enumerate(arr):
            if q['kind']!='score_cube':continue
            cs.append({'id':[section,i],'core':q['core'],'level':q['level'],
                'marks':frozenset(q.get('marks',[])),'nonmarks':frozenset(q.get('nonmarks',[])),
                'eq':frozenset(tuple(x) for x in q.get('score_equalities',[]))})
    groups=collections.defaultdict(list)
    for q in cs:groups[q['core']].append(q)
    certificates=[];unresolved=[]
    for q in cs:
        if len(q['marks'])<5 and not q['nonmarks']:continue
        found=None
        for v in groups[q['core']]:
            if v['id']==q['id'] or v['level']<q['level']:continue
            if len(v['marks'])>4 or v['nonmarks']:continue
            if v['marks']<=q['marks'] and v['eq']<=q['eq']:
                found=v;break
        if found:certificates.append({'antecedent':q['id'],'consequent':found['id'],
            'reason':'same core and outer P/N; higher-or-equal level; subset positive marks and ScoreAt equalities; no negative guard'})
        else:unresolved.append(q['id'])
        assert time.process_time()-start<cap
    out('subset_guard_implications.json',{'status':'EXACT_SYNTACTIC_IMPLICATIONS_ONLY',
        'certificates':certificates,'not_proved_by_this_rule':unresolved,
        'D0_included':False,'anchor_disjunctions_included':False,
        'source_witness_selection_proved':False,'all_clause_redundancy_proved':False,
        'no_implication_counterexample_claimed_for_unresolved':True,
        'semantic_evaluations':0,'new_masks_tested':0,'new_finite_tests':0})
    print(json.dumps({'proved_guard_implications':len(certificates),'not_proved_by_this_rule':len(unresolved),
        'universal_witness_padding':'OPEN'}))
except BaseException as ex:
    error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_subset_redundancy_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
