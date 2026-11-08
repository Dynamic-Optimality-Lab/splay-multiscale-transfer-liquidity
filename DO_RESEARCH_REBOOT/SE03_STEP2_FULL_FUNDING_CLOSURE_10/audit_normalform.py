"""Independent new residual-anchor assertion and exact local-rule failures.
The retained legacy source replayer uses both immutable implementations.
"""
import importlib.util,itertools,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_FINAL_PLUS_ONE_07'
spec=importlib.util.spec_from_file_location('legacy_source10',OLD/'audit_controls2.py')
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
from physical_exchange import exchange
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def maps(D,U):
    for k in range(len(D)+1):
        for ds in itertools.combinations(D,k):
            for us in itertools.permutations(U,k):yield dict(zip(ds,us))
def main():
    D={0,1,2};U={0,1,2,3};ms=list(maps(tuple(sorted(D)),tuple(sorted(U))));checked=0
    for l in ms:
        for h in ms:
            a=exchange(D,U,l,h);R=D-set(h)
            anchor={p:p for p in (D-set(l))&R}
            anchor.update({p:v['owner'] for p,v in a['blocked'].items()})
            assert set(anchor)==a['uncovered'] and set(anchor.values())<=R
            assert len(set(anchor.values()))==len(anchor)
            free=U-set(a['allocation'].values())
            assert U-(set(l.values())|set(h.values()))<=free
            checked+=1
    original=json.loads((B/'donor_rule_audit.json').read_text());replayed=[]
    for ex in original['counterexamples']:
        f=json.loads((B.parent.parent/ex['source']).read_text());name=ex['family']
        if 'word' not in f:f['word']=f['source_word']
        for reflected in (False,True):replayed.append(d.replay(name,f,reflected))
        # Recompute the critical scalar obstruction directly from actual rows;
        # do NOT call the producer's packet-classification/repair code.
        for slot in ('deficit_packet','preceding_packet'):
            v=ex[slot];rr=[f['rows'][i-1] for i in v['occurrences']]
            assert sum(r['a'] for r in rr)==v['H'] and sum(r['qF'] for r in rr)==v['Q']
        a,b=ex['deficit_packet'],ex['preceding_packet']
        assert a['Q']-2*a['H']>max(0,2*b['H']-b['Q'])
    out('normalform_audit.json',{'status':'PASS_UNIFORM_COMPONENTS_LOCAL_REPAIR_REFUTED_MAIN_OPEN',
        'residual_anchor_small_map_pairs':checked,'counterexamples_dual_replayed':len(replayed),
        'source_reports':replayed,'source_engine_calls':d.calls,'old_semantic_rows_replayed':d.replayed,
        'new_finite_tests':0,'residual_anchor_theorem':'universal algebraic proof, map cases are additional regression assertions',
        'local_repair':'REFUTED_EXACT','global_source_supply':'OPEN','Step2':'OPEN'})
    print(json.dumps({'status':'PASS_PARTIAL_ONLY','anchor_checks':checked,'replays':len(replayed),
        'source_engine_calls':d.calls,'source_rows':d.replayed}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_normalform_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':d.calls,'old_semantic_rows_replayed':d.replayed,'new_finite_tests':0})
