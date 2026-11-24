"""Independent original replay and geodesic certificates; no producer import."""
import sys
import json
import gzip
import importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('joint_metric_independent_original',
    HERE.parent/'GSO_CONSERVATIVE_TRANSPORT_20261122_V001/verify.py')
V=importlib.util.module_from_spec(spec);sys.modules[spec.name]=V;spec.loader.exec_module(V)


def read(path):
    with (gzip.open(path,'rt',encoding='utf-8') if path.suffix=='.gz' else path.open(encoding='utf-8')) as f:return json.load(f)


def spine(t):
    result=[]
    while t is not None:result.append(t.k);t=t.l
    return result


def plain(t,x):return V.V.rebuild(t,x,lambda *args:None,lambda *args:None)[0]


def flatten_rotation(t,promoted,demoted):
    frames=[];cur=t
    while cur.k!=demoted:
        if demoted<cur.k:frames.append((cur.k,'L',cur.r));cur=cur.l
        else:frames.append((cur.k,'R',cur.l));cur=cur.r
        assert cur is not None
    assert cur.r is not None and cur.r.k==promoted
    cur=V.V.left(cur)
    for key,side,sibling in reversed(frames):
        cur=V.V.node(key,cur,sibling) if side=='L' else V.V.node(key,sibling,cur)
    return cur


def main():
    theorem=read(HERE/'UNRESTRICTED_METRIC_OBSTRUCTION.json');rows=[]
    for row in theorem['complete_witnesses']:
        z=read(HERE/row['trace']);cert=read(HERE/row['certificate']);meta=cert['meta'];N=meta['N'];q=meta['parameter_q']
        _,stats=V.physical(z)
        assert N==16*(q+1)+1 and z['A']==4*(N-1)+26 and z['Q_B']==28*q+25
        A=V.immutable(z['source']['initial_A']);B=V.immutable(z['source']['initial_B'])
        boundaries={}
        for j,(mode,x) in enumerate(z['source']['operations'],1):
            A=plain(A,x)
            if mode=='K':B=plain(B,x)
            if j in (meta['before_boundary'],meta['after_boundary']):
                name='before' if j==meta['before_boundary'] else 'after'
                assert V.raw(A)==cert['snapshots'][name]['A']
                assert V.raw(B)==cert['snapshots'][name]['B']
                assert spine(A)==list(range(N,0,-1))
                assert spine(B)==[N-3 if name=='before' else N-7,2,1]
                boundaries[name]=B
        assert set(boundaries)=={'before','after'}
        for witness in cert['flattenings']:
            t=boundaries[witness['boundary']];moves=witness['rotations']
            assert len(moves)==N-3
            for promoted,demoted in moves:
                length=len(spine(t));t=flatten_rotation(t,promoted,demoted)
                assert len(spine(t))==length+1
            assert spine(t)==list(range(N,0,-1))
        ops=z['operations'][meta['before_boundary']:meta['after_boundary']]
        assert len(ops)==14 and sum(o['a'] for o in ops)==14 and sum(o['q'] for o in ops)==q+1
        assert sum(o['mode']=='K' for o in ops)==1
        rows.append({'q':q,'keys':N,'fragment_A':14,'fragment_Q_B':q+1,'equal_endpoint_distance':N-3,**stats})
    result={'passed':True,'complete_original_sources':len(rows),'operations':sum(r['operations'] for r in rows),
            'real_rotations':sum(r['real_rotations'] for r in rows),'cases':rows,
            'geodesic_upper_paths_checked':2*len(rows),'distance_lower_bound':'Universal one-rotation left-spine bound, also checked in MetricKernel.lean.',
            'all_parameter_proof':'Uses exact old H3q recurrence plus counted A-only cap identities; finite witnesses are not extrapolated.',
            'scope':'Arbitrary rotation-distance-only whole-operation potentials, unrestricted original source domain.',
            'original_counterexample_to_Universal_CD':False,'universal_CD':'OPEN'}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        path=HERE/'INDEPENDENT_METRIC_VERIFICATION.json'
        if path.exists():assert read(path)==result
        else:path.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('passed','complete_original_sources','operations','real_rotations','universal_CD')}))


if __name__=='__main__':main()
