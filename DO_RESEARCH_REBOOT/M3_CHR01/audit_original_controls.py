"""Read-only state-sharing and joint-potential audit of full original-root controls."""
import json,ast
from fragment_graph import BASE
from verify_original_controls import Potential

def env_state(e,pre):
    return {'mu':e[pre+'_mu'],'sigma':[e[f'{pre}_sg{i}'] for i in range(10)],
            'alpha':[[e[f'{pre}_ak{i}'],e[f'{pre}_aS{i}'],e[f'{pre}_aI{i}']] for i in range(7)],
            'b':{'root':e[pre+'_b_broot'],
                 **{f:[e[f'{pre}_b_b{f}{i}'] for i in range(19)] for f in ('kl','rl','kr','rr','lo','hi')}}}
def main():
    c=json.loads((BASE/'original_controls.json').read_text());assert c['status']=='COMPLETE'
    assert c['controls']==len(c['records'])==8 and c['original_root_evaluations']==9
    assert c['low_DAG_nodes']==1400081 and c['high_DAG_nodes']==53455 and c['cpu_seconds']<300
    P=Potential();byname={r['label']:r for r in c['records']}
    for r in c['records']:
        assert r['root'] is True;pre='MXL' if r['kind']=='LOW' else 'MXH';e=r['environment']
        assert env_state(e,pre+'s')==r['source'] and env_state(e,pre+'t')==r['destination']
        assert r['source']['mu']==r['destination']['mu']==341
        assert r['source']['sigma']==r['destination']['sigma']==[0]*10
        s=P(r['source']);t=P(r['destination'])
        assert s==r['joint_potential_source'] and t==r['joint_potential_destination']
        assert r['extended_reduced_weight']==r['w']-(t-s)>=0
        if r['kind']=='LOW':
            assert r['w']==2*r['H']-r['q']==e['MXL_w']
            assert r['H']==e['MXL_H'] and r['q']==e['MXLbt_q']
        else:
            assert r['q']==r['d']//2 and r['w']==6-r['q']
            assert r['d']==e['MXHbt_bd0'] and r['q']==e['MXH_q'] and r['w']==e['MXH_w1']
            assert r['midpoint_potential']==0 and r['OM_reduced_weight']==r['w']+s>=0
            assert r['MO_reduced_weight']==-t>=0
            assert r['extended_reduced_weight']==r['OM_reduced_weight']+r['MO_reduced_weight']
            m=r['shared_midpoint'];assert m['b']==r['destination']['b']
            assert m['mu']==e['MXHg_fmu']==341 and m['sigma']==[e[f'MXHg_fsg{i}'] for i in range(10)]
            assert m['v']==e['MXHg_fv'] and m['b']['root']==e['MXHg_fb_broot']
            for f in ('kl','rl','kr','rr','lo','hi'):assert m['b'][f]==[e[f'MXHg_fb_b{f}{i}'] for i in range(19)]
    z=byname['zero_reset_debt_retained'];p=byname['plus1_reset_debt_retained']
    assert z['w']==0 and (z['joint_potential_source'],z['joint_potential_destination'])==(-2,-2)
    assert p['w']==1 and (p['joint_potential_source'],p['joint_potential_destination'])==(-2,-1)
    assert byname['expensive_H2_DELETE_KEEP']['H']==2 and byname['expensive_H2_DELETE_KEEP']['w']==3
    n=byname['noncanonical_high_to_abstract_shadow']
    assert n['d']==9 and n['w']==2 and n['noncanonical_declared_depth'] and n['abstract_only_destination_shadow']
    assert n['joint_potential_destination']==0
    cyc=c['mixed_closed_cycle'];legs=[byname[label] for label in cyc['labels']]
    for l,r in zip(legs,legs[1:]+legs[:1]):assert l['destination']==r['source']
    assert cyc['full_state_closure'] and cyc['high_midpoint_shared']
    assert cyc['weight']==sum(r['w'] for r in legs)==4
    assert sum(r['joint_potential_destination']-r['joint_potential_source'] for r in legs)==0
    files=list(BASE.glob('*.py'))
    for f in files:ast.parse(f.read_text(encoding='utf-8'),filename=str(f))
    print(json.dumps({'status':'PASS','controls':8,'original_root_evaluations':9,
                      'full_state_mixed_cycle_weight':4,'cheap_reset_endpoints':{'zero':[-2,-2],'plus1':[-2,-1]},
                      'python_files_parsed':len(files),
                      'scope':'read-only provenance/state audit; completed generator evaluated original low/high roots'}))
if __name__=='__main__':main()
