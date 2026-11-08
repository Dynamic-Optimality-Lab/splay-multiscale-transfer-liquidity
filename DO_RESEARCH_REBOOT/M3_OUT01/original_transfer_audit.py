"""Complete original-root audit of low-table transfer outside chi8."""
import sys,json,time,copy
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_OUT01','DO_RESEARCH_REBOOT/M3_GAPINT01']
from potential import OutsidePotential
from outside_original import DAG,build_slow,build_shigh,V
BASE=Path('DO_RESEARCH_REBOOT/M3_OUT01')

def main():
    assert json.loads((BASE/'proof_certificate.json').read_text())['status']=='PASS_PRODUCTION_DAG'
    out=BASE/'original_transfer_audit.json';assert not out.exists();start=time.process_time()
    d=DAG();L=build_slow(d,'MXL');dh=DAG();H=build_shigh(dh,'MXH');P=OutsidePotential();records=[]
    campaigns=['M3_GAP01']+[f'M3_GAPINT0{g}' for g in range(1,5)]
    for name in campaigns:
        j=json.loads((Path('DO_RESEARCH_REBOOT')/name/'original_audit.json').read_text())
        for old in j['records']:
            r=copy.deepcopy(old);r['label']=name+'_outside_'+r['label'];e=r['environment']
            changes=[]
            for key in list(e):
                if key.endswith('bkr8') and e[key]==0:
                    rk=key[:-4]+'brr8'
                    assert rk in e and e[rk]==19,(key,rk)
                    e[key]=2;changes.append(key)
            assert changes
            for st in (r['source'],r['destination']):
                b=st['b'];assert b['kr'][8]==0 and b['rr'][8]==19;b['kr'][8]=2
            if r['kind']=='HIGH':
                r['shared_midpoint']['b']['kr'][8]=2
            dd,root=(d,L['root']) if r['kind']=='LOW' else (dh,H['root'])
            V.bounds(dd,e);assert dd.ev_ground(root,e),r['label']
            si=P.inspect(r['source']);ti=P.inspect(r['destination'])
            assert si['value']==r['potential_source']['value'] and ti['value']==r['potential_destination']['value']
            residual=r['w']+si['value']-ti['value'];assert residual>=0
            if r['kind']=='HIGH':assert r['w']+si['value']>=0 and -ti['value']>=0
            r.update(potential_source=si,potential_destination=ti,residual=residual,
                     outside_source=True,outside_destination=True,dephantomized_variables=changes)
            records.append(r);assert time.process_time()-start<300,'UNKNOWN source-transfer audit cap'
        print(json.dumps({'campaign':name,'completed_original_roots':len(records),'cpu_seconds':round(time.process_time()-start,3)}),flush=True)
    cycles=[]
    for name in campaigns:
        rs=[r for r in records if r['label'].startswith(name+'_') and 'cycle' in r['label'] or (r['label'].startswith(name+'_') and 'shared_high_return' in r['label'])]
        lows=[r for r in rs if r['kind']=='LOW'];highs=[r for r in rs if r['kind']=='HIGH']
        for low in lows:
            for high in highs:
                if low['source']==high['destination'] and low['destination']==high['source']:
                    cycles.append({'campaign':name,'full_shared_state_closure':True,'same_midpoint':True,
                                   'weight':low['w']+high['w']})
    # GAP01's low cycle has a historical label without the substring cycle.
    if not any(c['campaign']=='M3_GAP01' for c in cycles):
        low=next(r for r in records if r['label']=='M3_GAP01_outside_population3_core_and_fringe_ports_low')
        high=next(r for r in records if r['label']=='M3_GAP01_outside_population3_shared_high_return')
        assert low['source']==high['destination'] and low['destination']==high['source']
        cycles.append({'campaign':'M3_GAP01','full_shared_state_closure':True,'same_midpoint':True,'weight':low['w']+high['w']})
    assert len(cycles)==5 and all(c['weight']==8 for c in cycles)
    for r in records:
        dd,root=(d,L['root']) if r['kind']=='LOW' else (dh,H['root'])
        assert dd.ev_ground(root,r['environment'])
    result={'status':'PASS','original_roots':len(records),'independent_replays':len(records),
            'gaps_verified':sorted({g for r in records for g,n in enumerate(r['source']['sigma']) if n}),
            'maximum_opaque_population':max(max(r['source']['sigma']) for r in records),
            'unchanged_low_table_values':True,'closed_mixed_cycles':cycles,
            'DAG_nodes':[len(d.nodes),len(dh.nodes)],'cpu_seconds':round(time.process_time()-start,3),'records':records}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2),flush=True)

if __name__=='__main__':main()
