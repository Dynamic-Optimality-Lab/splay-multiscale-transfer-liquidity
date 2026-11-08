"""Audit the proposed first-return event-cap<=2 route on stored sources.

This is a mechanism falsification/control, not universal proof by examples.
All original source rotations, closures and costs are already accepted.
"""
import collections,hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    mp=F/'marked_demotion_relation.json';rp=F/'independent_MFR35_theorem.json';md=json.loads(mp.read_text());ret=json.loads(rp.read_text());reports=[]
    for mc in md['controls']:
        name=mc['source'];rc=next(c for c in ret['controls'] if c['source']==name)
        path=B/'SOURCE_JOINT_REPAIR_03/actual_monotone_return_source.json' if name=='AF' else F/'cluster_collateral_closed_source.json'
        rows=json.loads(path.read_text())['period_rows'];by={r['t']:i for i,r in enumerate(rows)};n=len(rows)
        groups=collections.defaultdict(list);mapped={};types={}
        for d in mc['source_demands']:groups[tuple(d['loss_rotations'][0])].append(d)
        for u,ds in groups.items():
            ds.sort(key=lambda a:(by[a['demand'][0]]-by[u[0]])%n);d=tuple(ds[-1]['demand']);mapped[d]=u;types[d]='DIRECT'
        for d in rc['return_map']:
            key=tuple(d['demand']);assert key not in mapped;mapped[key]=tuple(d['bit']);types[key]='RETURN'
        assert len(mapped)==mc['Q'];load=collections.defaultdict(list)
        for d,u in mapped.items():load[u[:2]].append({'demand':d,'bit':u,'type':types[d]})
        bad=[]
        for e,claims in load.items():
            if len(claims)<=2:continue
            ev=next(z for z in rows[by[e[0]]]['A_events'] if z['j']==e[1]);bad.append({'source_event':e,'claims':claims,
              'pattern':ev['pattern'],'pivots':[z['pivot'] for z in ev['rotations']],
              'physical_units':[(e[0],e[1],0),(e[0],e[1],1)],'deficiency':len(claims)-2})
        reports.append({'source':name,'Q':mc['Q'],'event_load_peak':max(map(len,load.values())),
          'overloaded_events':bad,'full_assignment':[{'demand':d,'unit':u,'type':types[d]} for d,u in sorted(mapped.items())],
          'source_operations_or_owners_changed':False})
    fail=any(c['overloaded_events'] for c in reports)
    out={'status':'MFR_FIRST_RETURN_EVENT_CAP2_REFUTED' if fail else 'STORED_SOURCE_CONTROLS_PASS_MFR_EVENT_CAP2',
      'candidate':'every original maximal-core source, MD first direct loss plus first fringe-return; choose at most two claims per actual event',
      'controls':reports,'source_queries':0,'source_engine_calls':0,'JR35':'OPEN','passing_controls_not_universal':True,
      'refutation_scope':'only this frozen first-return event-supplier rule, not all return choices and not Coarse-Double',
      'input_sha256':{str(p):sha(p) for p in (mp,rp,F/'analyze_MFR35_full_assignment.py')}}
    with (F/'MFR35_full_assignment_analysis.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({'status':out['status'],'controls':[{'source':c['source'],'Q':c['Q'],'event_load_peak':c['event_load_peak'],'overloaded_events':len(c['overloaded_events'])} for c in reports]}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof289_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
