"""Inspect only stored original rotations, no new source replay."""
import collections,hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    rp=F/'independent_RLC35_and_B_only_control.json';r=json.loads(rp.read_text());reports=[]
    for control in r['RLC_controls']:
        p=B/'SOURCE_JOINT_REPAIR_03/actual_monotone_return_source.json' if control['source']=='AF' else F/'cluster_collateral_closed_source.json'
        rows=json.loads(p.read_text())['period_rows'];by={z['t']:z for z in rows};load=collections.defaultdict(list)
        for a in control['raw_assignment']:load[tuple(a['bit'][:2])].append(a)
        bad=[]
        for (t,j),claims in load.items():
            if len(claims)<=2:continue
            row=by[t];event=next(e for e in row['A_events'] if e['j']==j)
            bad.append({'event':[t,j],'source_kind':row.get('kind',row.get('op')),'source_target':row['key'],
              'genuine_F':row['genuine_F'],'event_pattern':event['pattern'],
              'actual_rotation_pivots':[z['pivot'] for z in event['rotations']],
              'actual_before':event['rotations'][0]['before'],'actual_after':event['rotations'][-1]['after'],
              'claims':claims,'excess':len(claims)-2})
        reports.append({'source':control['source'],'event_load_peak':max(map(len,load.values())),
          'overloaded_events':bad,'total_event_excess':sum(a['excess'] for a in bad),
          'raw_collision_units':len(control['collisions']),'total_claims':control['demands']})
    out={'status':'EXACT_STORED_SOURCE_RLC_EVENT_OVERLOADS','controls':reports,'source_queries':0,'source_engine_calls':0,'JR35':'OPEN',
      'input_sha256':{str(rp):sha(rp)}}
    with (F/'RLC35_event_overloads.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({'status':out['status'],'controls':[{k:v for k,v in a.items() if k!='overloaded_events'} for a in reports]}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof288_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
