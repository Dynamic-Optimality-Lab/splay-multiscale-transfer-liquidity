"""Unrestricted physical metric-energy attack; complete original witnesses.

The added DELETE caps change only A. They return A exactly to the old H3q
states, so every old B operation and the complete paired restoration remain.
Auxiliary flattening rotations certify distance; they are not original credit.
"""
import sys
import json
import gzip
import importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('joint_metric_readonly_transport',
    HERE.parent/'GSO_CONSERVATIVE_TRANSPORT_20261122_V001/transport.py')
T=importlib.util.module_from_spec(spec);sys.modules[spec.name]=T;spec.loader.exec_module(T)


def write(name,value):
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    path=HERE/name;assert not path.exists();path.parent.mkdir(parents=True,exist_ok=True)
    with (gzip.open(path,'wt',encoding='utf-8') if path.suffix=='.gz' else path.open('w',encoding='utf-8')) as f:json.dump(value,f,indent=None if path.suffix=='.gz' else 2)


def anchored_source(q):
    s=T.B.K.PARAM.H(3,q);N=len(s['initial_A']['children']);x=N-7;i=N+7
    up=lambda lo:[['D',k] for k in range(lo,N+1)]
    down=lambda hi:[['D',k] for k in range(N-1,hi-1,-1)]
    s['name']='metric_anchor_H3q_'+str(q)
    s['operations']=s['operations'][:i-1]+up(x+2)+down(x+1)+[['K',x]]+up(x+1)+down(x)+s['operations'][i:]
    s['expected_A']=4*(N-1)+26;s['expected_Q']=28*q+25
    return s,{'parameter_q':q,'N':N,'target':x,'before_boundary':N+12,'after_boundary':N+26,
              'critical_operation':N+19,'fragment_A':14,'fragment_Q_B':q+1,
              'distance_both_ends':N-3}


def left_spine(t):
    out=[];k=t.root
    while k is not None:out.append(k);k=t.ch[k][0]
    return out


def flatten(t):
    """Rotate each off-left-spine vertex onto the spine exactly once."""
    N=len(t.keys);initial=len(left_spine(t));moves=[];k=t.root
    while k is not None:
        right=t.ch[k][1]
        if right is None:k=t.ch[k][0];continue
        before=len(left_spine(t));p=t.parent[right];t.rotate(right)
        assert len(left_spine(t))==before+1;moves.append([right,p]);k=right
    assert len(moves)==N-initial and len(left_spine(t))==N
    return moves


def main():
    rows=[]
    for q in (1,17,129):
        s,meta=anchored_source(q);z=T.F.compile_source(s)
        keys=sorted(map(int,s['initial_A']['children']))
        trees={a:T.B.K.OLD.Tree(s['initial_'+a],keys) for a in ('A','B')}
        snapshots={};distance_witnesses=[]
        for j,(mode,x) in enumerate(s['operations'],1):
            T.B.K.OLD.plain(trees['A'],x)
            if mode=='K':T.B.K.OLD.plain(trees['B'],x)
            if j in (meta['before_boundary'],meta['after_boundary']):
                label='before' if j==meta['before_boundary'] else 'after'
                assert len(left_spine(trees['A']))==meta['N']
                assert left_spine(trees['B'])==[meta['N']-3 if label=='before' else meta['N']-7,2,1]
                snap=trees['B'].state();copy=T.B.K.OLD.Tree(snap,keys)
                moves=flatten(copy);assert len(moves)==meta['distance_both_ends']
                snapshots[label]={'A':trees['A'].state(),'B':snap}
                distance_witnesses.append({'boundary':label,'rotations':moves,
                    'kind':'Auxiliary geodesic certificate only, not source A work.'})
        section=z['operations'][meta['before_boundary']:meta['after_boundary']]
        assert sum(o['a'] for o in section)==14 and sum(o['q'] for o in section)==q+1
        assert z['A']==meta['N']*4+22 and z['Q_B']==28*q+25
        name='metric/anchor_'+str(q)
        write(name+'_trace.json.gz',z)
        write(name+'_certificate.json.gz',{'meta':meta,'snapshots':snapshots,'flattenings':distance_witnesses,
              'full_A':z['A'],'full_Q_B':z['Q_B'],'physical_counterexample_to_CD':False})
        rows.append({**meta,'trace':name+'_trace.json.gz','certificate':name+'_certificate.json.gz',
                     'full_A':z['A'],'full_Q_B':z['Q_B'],'operations':len(z['operations']),
                     'real_rotations':z['real_rotations']})
        print(json.dumps(rows[-1]),flush=True)
    theorem={'status':'PROVED_PARAMETRIC_ORIGINAL_SOURCE_METRIC_GRAMMAR_OBSTRUCTION',
        'grammar':'Phi_N(A,B)=f_N(D_rot(A,B)), arbitrary real-valued f_N; no linearity, monotonicity or Lipschitz assumption.',
        'attempted_law':'q_t+Phi_N(after)-Phi_N(before)<=C*a_t on every original operation of every admissible exactly paired-closed source.',
        'distance_identity':'D_rot(T,left_vine_N)=N-left_spine_length(T). Each rotation changes spine length by at most1; flattening realizes exactly this many.',
        'original_family':'Complete H3q with four counted A-only adjacent caps of6,6,7,7 zigs around its last critical KEEP. Empty prefix, full old restoration preserved. N=16(q+1)+1.',
        'flat_fragment':'A=left_vine_N at both ends. B left spines are [N-3,2,1] and [N-7,2,1], hence D=N-3 at both ends. Actual fragment A=14,Q_B=q+1.',
        'universal_contradiction':'Telescoping the proposed law on the original14-operation fragment gives q+1<=14C for every positive integer q. Choose q+1>14C. This excludes every finite real C and every family f_N.',
        'proof_dependencies':['Original H3q full critical comb recurrence, j=2 and j=3 with T0=1 and r0=2.','Actual adjacent two-vine A zig identity; all DELETE caps leave B fixed.','General left-spine distance theorem, arbitrary hanging subtrees retained.'],
        'complete_witnesses':rows,'not_refuted':['Universal CD','Arbitrary shape-dependent potentials','Persistent globally shared overflow accounts with a proved physical invariant'],
        'unrestricted_original_cost_obligations_deleted':0,'universal_CD':'OPEN'}
    write('UNRESTRICTED_METRIC_OBSTRUCTION.json',theorem)


if __name__=='__main__':main()
