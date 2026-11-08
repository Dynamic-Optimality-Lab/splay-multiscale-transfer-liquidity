"""Independent replay of saved complete roots and adversarial inventory checks."""
import sys,json,time,copy,hashlib
from pathlib import Path
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_ACL01')
from original_controls import V,DAG,build_slow,build_shigh,CompleteOneGapPotential,BASE
def main():
    out=BASE/'audit.json';assert not out.exists();start=time.process_time();P=CompleteOneGapPotential()
    d=DAG();L=build_slow(d,'MXL');dh=DAG();H=build_shigh(dh,'MXH')
    result=json.loads((BASE/'original_controls.json').read_text());count=0;floor=0;faults=[]
    for r in result['records']:
        dd,root=(d,L['root']) if r['kind']=='LOW' else (dh,H['root'])
        assert dd.ev_ground(root,r['environment']);count+=1
        ps=P(r['source']);pt=P(r['destination']);assert ps==r['potential_source']['value'] and pt==r['potential_destination']['value']
        assert r['w']+ps-pt==r['reduced_weight']>=0
        if r['kind']=='LOW':
            assert r['destination']['b']['root'] in (0,2,4,6,8)
            assert r['potential_destination']['rule']=='canonical_completion'
            assert pt<=-r['potential_destination']['psi'];floor+=1
        assert time.process_time()-start<300
    for name in ('multi_S_port_RL_to_LR','empty_port_negative_False'):
        r=next(x for x in result['records'] if x['label']==name);e=dict(r['environment']);inv=r['port_inventory'][0];i,b=inv['slot'],inv['side']
        if inv['hidden_S']:key=f'MXLv_hs{i}_{b}_{inv["hidden_S"][0]}';e[key]=False
        else:key=f'MXLv_z0_{i}_{b}';e[key]=1
        assert not d.ev_ground(L['root'],e);faults.append({'label':name,'mutated':key,'root':False})
    # The HIGH relation permits alpha patterns which cannot be low witnesses.
    r=next(x for x in result['records'] if x['kind']=='HIGH');e=dict(r['environment']);s=copy.deepcopy(r['destination'])
    s['alpha']=[[0,1,s['b']['root']]]+[[2,0,0] for _ in range(6)]
    for i,(k,ss,x) in enumerate(s['alpha']):e[f'MXHt_ak{i}']=k;e[f'MXHt_aS{i}']=bool(ss);e[f'MXHt_aI{i}']=x
    assert dh.ev_ground(H['root'],e) and P.inspect(s)['rule']=='invalid_low_shape_zero'
    faults.append({'label':'high_to_invalid_low_alpha','original_high_root':True,'potential':P(s)})
    baseline=json.loads((BASE/'entry_baseline.json').read_text());preserved=0
    for row in baseline:
        p=Path(row['path']);p=p if p.is_absolute() else Path.cwd()/p
        assert hashlib.sha256(Path('\\\\?\\'+str(p.resolve())).read_bytes()).hexdigest()==row['sha256'],row['path'];preserved+=1
    res={'status':'PASS','original_roots_independently_replayed':count,'genuine_destination_floors':floor,
      'adversarial_inventory_rejections':faults[:2],'high_only_alpha_control':faults[2],
      'entry_files_preserved':preserved,'first_finite_harness_failure':'v1 attempted to normalize private anonymous-root patterns; these have no registered joint states. v2/v3 retain all ordinary state checks and explicitly exclude those private patterns.',
      'cpu_seconds':round(time.process_time()-start,3)}
    assert res['cpu_seconds']<300
    with out.open('x',encoding='utf-8') as f:json.dump(res,f,indent=2)
    print(json.dumps(res),flush=True)
if __name__=='__main__':main()
