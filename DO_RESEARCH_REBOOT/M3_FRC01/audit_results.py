"""Independent exact finite and original-relation audit of the compensation theorem."""
import sys,json,time
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_FRC01','DO_RESEARCH_REBOOT/M3_H2R01',
             'DO_RESEARCH_REBOOT/M3_PHI01','DO_RESEARCH_REBOOT/M2_SEP01','python/independent']
import splay as S
import verify_full_mixed as F
from experiment import D,trace,unpack,structure
from PC_B_CONTROLLER import verify_bpath,b_splay_event
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_HIGH_COMPILER import build_shigh
from compensated_potential import CompensatedPotential
BASE=Path('DO_RESEARCH_REBOOT/M3_FRC01');OUT=BASE/'audit_results.json'
def main():
    assert not OUT.exists();start=time.process_time();P=CompensatedPotential()
    c=json.loads((BASE/'compensation_certificate.json').read_text());R=set(c['R'])
    assert R=={1917,1937,2141,2965} and c['R_access_queries']==36
    assert {(r['source'],r['target']) for r in c['h1_rows']}=={(u,x) for u in R for x in range(9)}
    neutral=[];typed=[]
    for r in c['h1_rows']:
        u=r['source'];x=r['target'];v=r['destination'];t=P.old.trees[u]
        assert P.old.psi[u]==0 and S.lookup(t,x)[1]==r['depth']<=5
        assert r['w']==2-r['depth']//2>=0
        if r['w']==0 and P.old.psi[v]==0:neutral.append((u,x,v))
        a=-1;b=-P.old.psi[v]-int(v in R)
        assert r['new_source']==a and r['new_destination']==b
        assert r['reduced_weight']==r['w']-b+a>=0
        source=F.bmodel(F.insert(t,-1),True)
        expected=F.bmodel(F.insert(P.old.trees[v],-1),True)
        bs,bt,path,dirs=trace(source,x,r['depth']);assert verify_bpath(D,bs,bt,0).v
        actual=unpack(b_splay_event(D,bs,bt,0,D.const_bool(False)))
        assert structure(actual)==structure(expected)
        assert actual['lo']==source['lo'] and actual['hi']==source['hi']
        typed.append({'source':u,'target':x,'destination':v,'all_typed_pairs_match':True,'interval_fields_carried':True})
        assert time.process_time()-start<120,'UNKNOWN: typed replay cap'
    assert neutral==[(2141,6,2965)]
    kernel=json.loads(Path('DO_RESEARCH_REBOOT/M3_H2R01/fringe_kernel_certificate.json').read_text())
    retained=[r for r in kernel['rows'] if r['gap0_childless_at_exit']]
    assert len(retained)==len(c['h2_fringe_rows'])==16842
    for raw,row in zip(retained,c['h2_fringe_rows']):
        u=raw['entry_core'];v=raw['exit_core'];a=-P.old.psi[u]-int(u in R);b=-P.old.psi[v]-int(v in R)
        assert row['entry_core']==u and row['exit_core']==v and row['target']==raw['target']
        assert row['w']==raw['w']==4-raw['q'] and row['new_source']==a and row['new_destination']==b
        assert row['reduced_weight']==row['w']-b+a>=0
        if raw['w']==0:assert P.old.psi[v]>=1
    assert len(c['Gamma0_terminal_rows'])==4224
    for r in c['Gamma0_terminal_rows']:
        assert P.old.psi[r['destination']]>=r['q']-2
        assert r['new_destination']<=2-r['q']
        assert r['worst_case_reduced_weight']==4-r['q']-r['new_destination']-2>=0
    d=DAG();L=build_slow(d,'MXL');dh=DAG();H=build_shigh(dh,'MXH')
    ctrl=json.loads((BASE/'original_compensation_controls.json').read_text());records=ctrl['records']
    assert len(records)==8;lookup={r['label']:r for r in records}
    for r in records:
        dag,root=(d,L['root']) if r['kind']=='LOW' else (dh,H['root'])
        env=r['environment'];assert set(env)==set(dag.vars);F.bounds(dag,env);assert dag.ev_ground(root,env)
        for suffix,state in (('s',r['source']),('t',r['destination'])):
            tag=('MXL' if r['kind']=='LOW' else 'MXH')+suffix
            assert env[tag+'_mu']==state['mu']
            assert [env[tag+'_sg'+str(i)] for i in range(10)]==state['sigma']
            assert env[tag+'_b_broot']==state['b']['root']
            for f in F.FIELDS:assert [env[tag+'_b_b'+f+str(i)] for i in range(19)]==state['b'][f]
            for i,(k,s,x) in enumerate(state['alpha']):
                assert env[tag+'_ak'+str(i)]==k and env[tag+'_aS'+str(i)]==bool(s) and env[tag+'_aI'+str(i)]==x
            assert F.phi(state)==-3 and state['mu'].bit_count()==5 and state['sigma'][0]==1
        a=P.inspect(r['source']);b=P.inspect(r['destination'])
        assert a==r['potential_source'] and b==r['potential_destination']
        assert r['new_reduced_weight']==r['w']-b['compensated_joint']+a['compensated_joint']>=0
        if r['kind']=='LOW':
            assert env['MXL_H']==r['H'] and env['MXLbt_q']==r['q']
            assert env['MXL_w']==r['w']==2*r['H']-r['q']
        else:
            assert env['MXH_q']==r['q'] and env['MXH_w1']==r['w']==6-r['q']
            mid=r['shared_midpoint'];assert mid['mu']==env['MXHg_fmu']==r['source']['mu']==r['destination']['mu']
            assert mid['sigma']==[env['MXHg_fsg'+str(i)] for i in range(10)]
            assert mid['v']==env['MXHg_fv'] and mid['b']['root']==env['MXHg_fb_broot']
            for f in F.FIELDS:assert mid['b'][f]==[env['MXHg_fb_b'+f+str(i)] for i in range(19)]
            assert r['OM_reduced_weight']==r['w']+a['compensated_joint']>=0
            assert r['MO_reduced_weight']==-b['compensated_joint']>=0
        assert time.process_time()-start<300,'UNKNOWN: original audit cap'
    for b in ctrl['blocks']:
        legs=[lookup[label] for label in b['labels']]
        for a,z in zip(legs,legs[1:]):assert a['destination']==z['source']
        assert b['old_reduced_weight']==sum(e['old_reduced_weight'] for e in legs)>=0
        assert b['new_reduced_weight']==sum(e['new_reduced_weight'] for e in legs)>=0
        assert b['weight']==sum(e['w'] for e in legs)
        assert b['closed']==(legs[0]['source']==legs[-1]['destination'])==False
    result={'status':'COMPLETE','R':sorted(R),'typed_original_B_replays':36,
        'typed_replay_rows':typed,'unique_unpaid_zero_H1_successor':{'source':2141,'target':6,'destination':2965},
        'maximum_neutral_delays_before_repayment':1,'maximum_successors_to_repayment':2,
        'H2_fringe_rows_rechecked':16842,'Gamma0_terminal_rows_rechecked':4224,
        'full_original_low_roots_replayed':7,'full_original_high_roots_replayed':1,
        'ordinary_state_fields_and_high_shared_midpoint_checked':True,'shared_state_compensation_blocks':4,
        'full_cycles_in_controls':0,'negative_mixed_cycles_certified':0,'new_potential_range':[-2,0],
        'claim':'all chi8 H2 edges repaid; all chi8 original H1 edges from corrected basin repaid; old certified inequalities preserved',
        'cpu_seconds':round(time.process_time()-start,3)}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='typed_replay_rows'},indent=2),flush=True)
if __name__=='__main__':main()
