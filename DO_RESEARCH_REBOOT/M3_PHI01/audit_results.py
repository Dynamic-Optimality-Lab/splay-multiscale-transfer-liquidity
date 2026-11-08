"""Read-only deterministic provenance, state-sharing and certificate audit."""
import ast,hashlib,itertools,json,os
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent

def native(p):return Path(chr(92)*2+'?'+chr(92)+str(p.absolute())) if os.name=='nt' else p
def sha(p):return hashlib.sha256(native(p).read_bytes()).hexdigest()
def read(n):return json.loads((HERE/n).read_text(encoding='utf-8'))
def rank(i):return 2*i+1 if i<9 else 2*(i-9)
def phi(s):return -3*int(s['b']['kr'][8]==0 and s['b']['rr'][8]==19)
def env_state(e,pre):
    return {'mu':e[pre+'_mu'],'sigma':[e[f'{pre}_sg{i}'] for i in range(10)],
            'alpha':[[e[f'{pre}_ak{i}'],e[f'{pre}_aS{i}'],e[f'{pre}_aI{i}']] for i in range(7)],
            'b':{'root':e[pre+'_b_broot'],
                 **{f:[e[f'{pre}_b_b{f}{i}'] for i in range(19)] for f in ('kl','rl','kr','rr','lo','hi')}}}

def main():
    scripts=list(HERE.glob('*.py'))
    for p in scripts:ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
    c=read('primitive_certificate.json');expected=[];roles=Counter()
    for x,p in itertools.permutations(range(18),2):
        for g in [19]+[i for i in range(18) if i not in (x,p)]:
            if g!=19 and ((rank(x)<rank(g))!=(rank(p)<rank(g))):continue
            pins={'x':x,'p':p,'g':g,'sx':rank(x)>rank(p),
                  'sp':g!=19 and rank(p)>rank(g),'pr':g==19}
            expected.append(pins)
    assert c['status']=='COMPLETE' and c['cases']==len(expected)==len(c['rows'])==3570
    assert c['production_DAG_nodes']==638 and c['cpu_seconds']<120
    for pins,row in zip(expected,c['rows']):
        assert row['pins']==pins and row['kr_reflexive'] and row['rr_reflexive']
        assert row['pins_sha256']==hashlib.sha256(json.dumps(pins,sort_keys=True).encode()).hexdigest()
        role='X' if pins['x']==8 else 'P' if pins['p']==8 else 'GP' if pins['g']==8 else 'OFF'
        assert row['role_of_8']==role;roles[role]+=1
    assert dict(roles)==c['roles']=={'OFF':2992,'X':153,'P':153,'GP':272}
    s=read('mixed_search.json')
    assert s['status']=='COMPLETE' and s['core_B_trees']==4862 and s['examined_B_sources']==3584
    assert s['low_extensions']==359720<500000 and s['closed_return_candidates']==17051
    assert s['low_prefix_counts']=={'legal_low_prefix_1':14336,'legal_low_prefix_2':54024,'legal_low_prefix_3':201496}
    assert s['minima']=={'1':6,'2':9,'3':4} and s['negative_cycle_candidates']==[]
    assert s['cpu_seconds']<120
    controls=read('full_mixed_controls.json')
    assert controls['status']=='COMPLETE' and controls['cpu_seconds']<300
    assert controls['low_DAG_nodes']==1400081<4000000 and controls['high_DAG_nodes']==53455<4000000
    assert controls['queries']==len(controls['records'])==22
    records={r['label']:r for r in controls['records']}
    assert len(records)==22
    assert sum(r['kind']=='LOW' for r in records.values())==controls['low_queries']==16
    assert sum(r['kind']=='HIGH' for r in records.values())==controls['high_queries']==6
    for r in records.values():
        assert r['root'] is True
        pre='MXL' if r['kind']=='LOW' else 'MXH';e=r['environment']
        assert env_state(e,pre+'s')==r['source'] and env_state(e,pre+'t')==r['destination']
        assert phi(r['source'])==r['phi_source'] and phi(r['destination'])==r['phi_destination']
        assert r['source']['mu']==r['destination']['mu']==341
        assert r['source']['sigma']==r['destination']['sigma']
        if r['kind']=='LOW':
            assert e['MXL_H']==r['H'] and e['MXLbt_q']==r['q'] and e['MXL_w']==r['w']
            assert r['w']==2*r['H']-r['q'] and r['phi_source']==r['phi_destination']
            for q,m in enumerate(r['B_event_boundaries']):
                for i in range(19):
                    assert e[f'MXLsb{q}_bpar{i}']==m['bpar'][i]
                    assert e[f'MXLsb{q}_bdep{i}']==m['bdep'][i]
            if r['phi_source']==-3:
                assert all(m['kr'][8]==0 and m['rr'][8]==19 for m in r['B_event_boundaries'])
        else:
            assert r['q']==r['d']//2 and r['w']==6-r['q']
            assert e['MXH_q']==r['q'] and e['MXH_w1']==r['w']
            mid=r['shared_midpoint']
            assert mid['mu']==e['MXHg_fmu'] and mid['v']==e['MXHg_fv']
            assert mid['sigma']==[e[f'MXHg_fsg{i}'] for i in range(10)]
            assert mid['b']==r['destination']['b'] and mid['b']['root']==e['MXHg_fb_broot']
            for f in ('kl','rl','kr','rr','lo','hi'):
                assert mid['b'][f]==[e[f'MXHg_fb_b{f}{i}'] for i in range(19)]
            assert r['w']>=r['phi_destination']-r['phi_source']
    assert len(controls['cycles'])==6
    for c in controls['cycles']:
        legs=[records[label] for label in c['labels']]
        for l,r in zip(legs,legs[1:]+legs[:1]):assert l['destination']==r['source']
        assert c['full_state_closure'] and c['total_weight']==sum(r['w'] for r in legs)>=0
        assert c['low_weight']==sum(r['w'] for r in legs if r['kind']=='LOW')
        assert c['high_weight']==sum(r['w'] for r in legs if r['kind']=='HIGH')>=0
        assert all((phi(r['source'])==-3)==c['chi8'] for r in legs)
    for p in (0,1):
        r=records[f'negative_low_phi_obstruction_p{p}']
        assert r['H']==1 and r['q']==4 and r['w']==-2 and r['phi_source']==r['phi_destination']==-3*p
    r=records['fringe_internal_gap_macro'];mid=r['B_event_boundaries'][1]
    assert mid['root']==9 and mid['kr'][9]==0 and r['H']==2 and r['q']==1 and r['w']==3
    assert r['source']['sigma'][0]==1 and r['destination']['sigma'][0]==1
    r=records['present_outer_gap9_phi_zero']
    assert r['source']['sigma'][9]==1 and phi(r['source'])==phi(r['destination'])==0
    hashes=0
    if (HERE/'manifest.json').exists():
        m=read('manifest.json')
        for section in ('files','frozen_dependencies','baseline_preservation'):
            for row in m[section]:
                assert sha(ROOT/row['path'])==row['sha256'],row['path'];hashes+=1
    print(json.dumps({'status':'PASS','primitive_rows':3570,'complete_controls':22,
                      'closed_mixed_cycles':6,'python_files_parsed':len(scripts),
                      'manifest_hashes_checked':hashes,'scope':'read-only provenance/state/weight audit; completed generators certify original roots'}))
if __name__=='__main__':main()
