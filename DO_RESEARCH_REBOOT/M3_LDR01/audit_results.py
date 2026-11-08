"""Read-only complete-domain integer certificate and original-control provenance audit."""
import ast,hashlib,itertools,json,os,sys
from pathlib import Path
from collections import Counter
from functools import lru_cache
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'python/independent'),str(ROOT/'DO_RESEARCH_REBOOT/M3_PHI01')]
import splay as S
import verify_full_mixed as V

def read(n):return json.loads((HERE/n).read_text(encoding='utf-8'))
def native(p):return Path(chr(92)*2+'?'+chr(92)+str(p.absolute())) if os.name=='nt' else p
def sha(p):return hashlib.sha256(native(p).read_bytes()).hexdigest()
@lru_cache(None)
def trees(lo,hi):
    if lo==hi:return (S.LEAF,)
    return tuple(S.node(r,l,t) for r in range(lo,hi) for l in trees(lo,r) for t in trees(r+1,hi))
def structure(m):return (m['root'],*(tuple(m[f]) for f in ('kl','rl','kr','rr')))
def erase(t):
    if t==S.LEAF:return t
    if t[1] not in range(9):assert t[2]==t[3]==S.LEAF;return S.LEAF
    return S.node(t[1],erase(t[2]),erase(t[3]))
def env_state(e,pre):
    return {'mu':e[pre+'_mu'],'sigma':[e[f'{pre}_sg{i}'] for i in range(10)],
            'alpha':[[e[f'{pre}_ak{i}'],e[f'{pre}_aS{i}'],e[f'{pre}_aI{i}']] for i in range(7)],
            'b':{'root':e[pre+'_b_broot'],
                 **{f:[e[f'{pre}_b_b{f}{i}'] for i in range(19)] for f in ('kl','rl','kr','rr','lo','hi')}}}

def main():
    scripts=list(HERE.glob('*.py'))
    for p in scripts:ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
    c=read('negative_run_census.json');ts=trees(0,9);ids={t:i for i,t in enumerate(ts)}
    assert c['status']=='COMPLETE' and c['core_topologies']==len(ts)==len(c['nodes'])==4862
    assert c['access_queries']==43758 and c['negative_edges']==len(c['edges'])==4224
    for i,n in enumerate(c['nodes']):
        assert n['id']==i and V.from_serial(n['tree'])==ts[i]
        assert isinstance(n['psi'],int) and 0<=n['psi']<=2
    ps=[n['psi'] for n in c['nodes']];expected=[];dep=Counter()
    for i,t in enumerate(ts):
        for x in range(9):
            h=S.lookup(t,x)[1]
            if h>=6:
                expected.append({'source':i,'destination':ids[S.trace(t,x)[0]],
                                 'target':x,'depth':h,'deficit':h//2-2});dep[str(h)]+=1
    assert expected==c['edges'] and dict(dep)==c['depth_counts']=={'6':2816,'7':1152,'8':256}
    assert Counter(ps)=={0:4223,1:556,2:83}
    assert c['potential_histogram']=={'0':4223,'1':556,'2':83}
    topo=c['topological_order'];assert sorted(topo)==list(range(4862))
    rank={v:i for i,v in enumerate(topo)};incoming=[[] for _ in ts];out=[[] for _ in ts]
    residuals=Counter()
    for e in expected:
        s=e['source'];t=e['destination'];d=e['deficit']
        assert rank[s]<rank[t] and ps[t]-ps[s]>=d
        incoming[t].append((s,d));out[s].append((t,d));residuals[ps[t]-ps[s]-d]+=1
    for i in topo:assert ps[i]==max([0]+[ps[s]+d for s,d in incoming[i]])
    length=[0]*4862
    for i in topo:
        for j,d in out[i]:length[j]=max(length[j],length[i]+1)
    assert c['acyclic'] and c['max_run_deficit']==max(ps)==2
    assert c['max_run_length']==max(length)==2
    replay=read('census_replay.json')
    assert replay['status']=='COMPLETE' and replay['cases']==len(replay['rows'])==4224 and replay['all_match']
    assert replay['cpu_seconds']<120
    for e,r in zip(expected,replay['rows']):
        assert {k:r[k] for k in e}==e and r['production_replay_matches']
        target=V.bmodel(ts[e['destination']],True)
        assert r['output_structure_sha256']==hashlib.sha256(json.dumps(structure(target)).encode()).hexdigest()
    rot=read('core_rotation_certificate.json');pins=[]
    for x,p in itertools.permutations(range(9),2):
        for g in [19]+[i for i in range(9) if i not in (x,p)]:
            if g!=19 and ((x<g)!=(p<g)):continue
            pins.append({'x':x,'p':p,'g':g,'sx':x>p,'sp':g!=19 and p>g,'pr':g==19})
    assert rot['status']=='COMPLETE' and rot['cases']==len(pins)==len(rot['rows'])==408
    assert rot['fields_per_case']==115 and rot['production_DAG_nodes']==638 and rot['source_fields_unfixed']
    for p,r in zip(pins,rot['rows']):
        assert r['pins']==p and r['all_115_fields_reflexive']
        assert r['pins_sha256']==hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()
    search=read('helper_search.json')
    assert search['status']=='COMPLETE' and search['cap_reason'] is None
    assert search['seeds_registered']==search['seeds_completed']==8 and search['max_low_edges']==6
    assert search['extensions']==94995 and search['state_occurrences']==search['return_tests']==32987
    assert search['closed_candidates']==search['hard_closed_candidates']==0 and search['best_candidates']=={}
    assert search['A_core_trees']==4862 and search['A_shadow_classes']==634 and search['A_shadow_transition_options']==5946
    assert len(search['progress'])==48 and search['cpu_seconds']<120
    controls=read('full_run_controls.json');zero=read('zero_reset_control.json')
    assert controls['status']==zero['status']=='COMPLETE'
    assert controls['queries']==len(controls['records'])==8 and zero['queries']==1
    assert controls['low_DAG_nodes']==zero['low_DAG_nodes']==1400081<4000000
    assert controls['cpu_seconds']+zero['cpu_seconds']<300
    records=controls['records']+[zero['record']];byname={r['label']:r for r in records}
    for r in records:
        e=r['environment'];assert r['root'] is True and r['kind']=='LOW'
        assert env_state(e,'MXLs')==r['source'] and env_state(e,'MXLt')==r['destination']
        assert r['source']['mu']==r['destination']['mu']==341
        assert r['source']['sigma']==r['destination']['sigma']
        assert r['phi_source']==r['phi_destination']==-3
        a=V.from_serial(r['A_source']);b=V.from_serial(r['B_source']);x=r['word'][0][1]
        assert r['word']==[['K',x]]
        assert V.serial(S.trace(a,x)[0])==r['A_destination']
        assert V.serial(S.trace(b,x)[0])==r['B_destination']
        da=S.lookup(a,x)[1];db=S.lookup(b,x)[1]
        assert r['H']==(da+1)//2==e['MXL_H']
        assert r['q']==db//2==e['MXLbt_q']
        assert r['w']==2*r['H']-r['q']==e['MXL_w']
        spsi=ps[ids[erase(b)]];tpsi=ps[ids[erase(S.trace(b,x)[0])]]
        assert spsi==r['psi_source'] and tpsi==r['psi_destination']
        assert r['Xi_change']==spsi-tpsi and r['Xi_edge_residual']==r['w']-(spsi-tpsi)
        if r['w']<0:assert tpsi-spsi>=-r['w']
    for run in controls['runs']:
        edges=[byname[n] for n in run['labels']]
        for l,r in zip(edges,edges[1:]):assert l['destination']==r['source']
        assert run['full_shared_states'] and run['closed'] is False
        assert run['weights']==[e['w'] for e in edges]
        assert run['total_weight']==sum(run['weights'])
        assert run['D_L']==sum(max(0,-w) for w in run['weights'])
        assert run['P_L']==sum(max(0,w) for w in run['weights'])
    runs={r['label']:r for r in controls['runs']}
    assert runs['sharp_minus2']['weights']==runs['sharp_minus2_gap0']['weights']==[-2]
    assert byname['sharp_minus2_gap0_0']['source']['sigma'][0]==1
    assert runs['two_minus1']['weights']==[-1,-1]
    assert runs['helper_reset']['weights']==[-2,1,0,-1] and runs['helper_reset']['D_L']==3
    assert byname['helper_reset_1']['Xi_edge_residual']==-1
    assert zero['record']['w']==0 and zero['record']['Xi_edge_residual']==-2
    assert controls['negative_mixed_cycle_certified'] is False
    hashes=0
    if (HERE/'manifest.json').exists():
        m=read('manifest.json')
        for sec in ('files','frozen_dependencies','baseline_preservation'):
            for row in m[sec]:assert sha(ROOT/row['path'])==row['sha256'],row['path'];hashes+=1
    print(json.dumps({'status':'PASS','core_topologies':4862,'negative_rows':4224,
                      'potential_range':[0,2],'edge_residual_histogram':dict(residuals),
                      'production_replay_rows':4224,'symbolic_rotation_cases':408,
                      'original_low_controls':9,'python_files_parsed':len(scripts),
                      'manifest_hashes_checked':hashes,
                      'scope':'read-only complete-domain integer/provenance/state audit; completed generators evaluated original roots'}))
if __name__=='__main__':main()
