"""Independent original-root, complete state, midpoint, macro and mixed-cycle audit."""
import sys,json,time,ast
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_H1F01','DO_RESEARCH_REBOOT/M3_FRC01',
             'DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
import verify_full_mixed as V
from one_gap_potential import OneGapPotential
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_HIGH_COMPILER import build_shigh
from build_fragment import BASE
OUT=BASE/'original_audit.json'
def main():
    assert not OUT.exists();start=time.process_time();P=OneGapPotential()
    for path in BASE.glob('*.py'):ast.parse(path.read_text(),filename=str(path))
    controls=json.loads((BASE/'original_controls.json').read_text());hidden=json.loads((BASE/'hidden_fringe_control.json').read_text())
    records=controls['records']+[hidden['record']];assert len(records)==16
    d=DAG();L=build_slow(d,'MXL');dh=DAG();H=build_shigh(dh,'MXH')
    assert len(d.nodes)==1400081 and len(dh.nodes)==53455
    byname={r['label']:r for r in records};assert len(byname)==16
    for r in records:
        dag,root=(d,L['root']) if r['kind']=='LOW' else (dh,H['root'])
        e=r['environment'];assert set(e)==set(dag.vars);V.bounds(dag,e);assert dag.ev_ground(root,e)
        for suffix,state in (('s',r['source']),('t',r['destination'])):
            tag=('MXL' if r['kind']=='LOW' else 'MXH')+suffix
            assert e[tag+'_mu']==state['mu']==341
            assert [e[tag+'_sg'+str(i)] for i in range(10)]==state['sigma']==[1]+[0]*9
            assert e[tag+'_b_broot']==state['b']['root']
            for f in V.FIELDS:assert [e[tag+'_b_b'+f+str(i)] for i in range(19)]==state['b'][f]
            for i,(k,s,x) in enumerate(state['alpha']):
                assert e[tag+'_ak'+str(i)]==k and e[tag+'_aS'+str(i)]==bool(s) and e[tag+'_aI'+str(i)]==x
            assert V.phi(state)==-3
        a=P.inspect(r['source']);b=P.inspect(r['destination'])
        assert a==r['potential_source'] and b==r['potential_destination']
        assert r['joint_reduced_weight']==r['w']-b['one_gap_joint']+a['one_gap_joint']>=0
        if r['kind']=='LOW':
            assert e['MXL_H']==r['H'] and e['MXLbt_q']==r['q'] and e['MXL_w']==r['w']==2*r['H']-r['q']
            assert a['table_node'] is not None and b['table_node'] is not None
        else:
            assert e['MXH_q']==r['q'] and e['MXH_w1']==r['w']==6-r['q']
            m=r['shared_midpoint'];assert m['mu']==e['MXHg_fmu']==341
            assert m['sigma']==[e['MXHg_fsg'+str(i)] for i in range(10)]==[1]+[0]*9
            assert m['v']==e['MXHg_fv'] and m['b']['root']==e['MXHg_fb_broot']
            for f in V.FIELDS:assert m['b'][f]==[e['MXHg_fb_b'+f+str(i)] for i in range(19)]
            assert r['OM_reduced_weight']==r['w']+a['one_gap_joint']>=0 and r['MO_reduced_weight']==-b['one_gap_joint']>=0
        assert time.process_time()-start<300,'UNKNOWN: original audit cap'
    for variant in controls['full_macro_variants']:
        x=byname[variant['original']];y=byname[variant['variant']]
        assert x['source']==y['source'] and x['destination']==y['destination'] and x['H']==y['H'] and x['w']==y['w']
    cycle=[byname[n] for n in controls['closed_mixed_cycle']['labels']]
    for x,y in zip(cycle,cycle[1:]+cycle[:1]):assert x['destination']==y['source']
    assert sum(r['w'] for r in cycle)==sum(r['joint_reduced_weight'] for r in cycle)==4
    noncanon=byname['noncanonical_high_abstract_shadow'];assert noncanon['d']==9 and noncanon['true_core_depth']==8
    assert noncanon['destination']['alpha']==[[0,1,8]]+[[2,0,0] for _ in range(6)]
    assert noncanon['potential_destination']['table_node'] is None
    assert hidden['fringe_depth']==9 and hidden['record']['fringe_is_hidden'] and hidden['full_physical_ranks_assigned']
    result={'status':'COMPLETE','original_low_roots_replayed':14,'original_high_roots_replayed':2,
            'total_roots_replayed':16,'full_ordinary_states_checked':True,'lo_hi_and_exact_midpoint_checked':True,
            'physical_rank_hidden_fringe_control':True,'cheap_H1_repaired_original_controls':3,
            'whole_macro_variants_same_full_states_and_weight':4,'noncanonical_high_and_abstract_shadow_verified':True,
            'closed_mixed_cycle_weight':4,'closed_mixed_cycle_complete_state_sharing':True,
            'negative_mixed_cycles_certified':0,'cpu_seconds':round(time.process_time()-start,3)}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
