"""Verify full event pools/matchings and the exact failed selector cut.

Reuses accepted original before/after rotations. No semantic re-execution.
"""
import collections,hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def contains(t,y,x):
    while t[0]!=x:
        if t[0]==y:return True
        t=t[1] if x<t[0] else t[2]
    return False
def main():
    ap=F/'MFR35_all_return_options.json';fp=F/'MFR35_full_assignment_analysis.json';mp=F/'marked_demotion_relation.json'
    a=json.loads(ap.read_text());first=json.loads(fp.read_text());md=json.loads(mp.read_text());reports=[];pins=[ap,fp,mp,F/'MFR35_CANDIDATE_STATUS.md',F/'audit_MFR35_all_return_control.py']
    for c in a['controls']:
        p=B/'SOURCE_JOINT_REPAIR_03/actual_monotone_return_source.json' if c['source']=='AF' else F/'cluster_collateral_closed_source.json'
        rows=json.loads(p.read_text())['period_rows'];by={r['t']:i for i,r in enumerate(rows)};N=len(rows);pins.append(p)
        graph={tuple(x['demand']):{tuple(u) for u in x['units']} for x in c['pools']}
        mc=next(z for z in md['controls'] if z['source']==c['source']);groups=collections.defaultdict(list)
        for d in mc['source_demands']:groups[tuple(d['loss_rotations'][0])].append(d)
        direct={};fresh={}
        for u,ds in groups.items():
            ds.sort(key=lambda d:(by[d['demand'][0]]-by[u[0]])%N);d=tuple(ds[-1]['demand'])
            want={(u[0],u[1],b) for b in (0,1)};assert graph[d]==want;direct[d]=u;fresh[d]=u
        for z in c['return_options']:
            d=tuple(z['demand']);contact=z['contact'];reset=z['reset'];key=z['z'];G=z['old_proxy'];expected=set();rr=[];fresh_candidates=[]
            last=contact
            segment=[rows[(by[contact]+i)%N] for i in range(1,(by[reset]-by[contact])%N+1)]
            for row in segment:
                if row['genuine_F'] and row['key']==key:last=row['t']
            assert last==z['last_genuine_contact_key_before_reset']
            for row in segment:
                for e in row['A_events']:
                    for rot in e['rotations']:
                        if contains(rot['before'],key,G) and not contains(rot['after'],key,G):
                            assert rot['pivot']==key;u=(row['t'],e['j'],rot['bit']);rr.append(u)
                            expected|={(row['t'],e['j'],0),(row['t'],e['j'],1)}
                            if (by[row['t']]-by[contact])%N>(by[last]-by[contact])%N:fresh_candidates.append(u)
            assert rr==[tuple(u) for u in z['all_return_rotation_bits']] and graph[d]==expected
            assert tuple(z['fresh_tenure_first_bit'])==fresh_candidates[0];fresh[d]=fresh_candidates[0]
        seen=set();demands=set()
        for pair in c['matching']:
            d,u=tuple(pair['demand']),tuple(pair['unit']);assert d not in demands and u not in seen and u in graph[d]
            demands.add(d);seen.add(u)
        assert demands==set(graph) and len(demands)==c['Q']
        freshload=collections.Counter(u[:2] for u in fresh.values());assert max(freshload.values())==c['fresh_tenure_event_load_peak']
        failed=next(z for z in first['controls'] if z['source']==c['source']);cutchecks=[]
        for cut in failed['overloaded_events']:
            e=tuple(cut['source_event']);units={e+(0,),e+(1,)};ds=set()
            for claim in cut['claims']:
                d,u=tuple(claim['demand']),tuple(claim['bit']);assert d not in ds and u in units;ds.add(d)
                if claim['type']=='DIRECT':assert direct[d]==u
                else:
                    rr=next(z for z in c['return_options'] if tuple(z['demand'])==d)
                    assert tuple(rr['all_return_rotation_bits'][0])==u
            assert len(ds)>len(units) and len(ds)-len(units)==cut['deficiency']
            cutchecks.append({'event':e,'demands':sorted(ds),'units':sorted(units),'deficiency':len(ds)-len(units)})
        reports.append({'source':c['source'],'complete_eligibility_pools_verified':True,'injective_full_control_size':len(demands),
          'first_selector_negative_cuts':cutchecks,'fresh_selector_event_peak':max(freshload.values())})
    out={'status':'PASS_SOURCE_EXACT_MFR_SELECTOR_REFUTATION_AND_COMPLETE_OPTION_CONTROLS',
      'controls':reports,'first_return_selector':'REFUTED','all_return_universal_source_supply':'OPEN',
      'JR35':'OPEN','reservation':'DEFERRED','source_queries':0,'source_engine_calls':0,
      'independent_is_same_agent_distinct_implementation':True,'input_sha256':{str(p):sha(p) for p in pins}}
    with (F/'independent_MFR35_all_return_control.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k!='input_sha256'}),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify153_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
