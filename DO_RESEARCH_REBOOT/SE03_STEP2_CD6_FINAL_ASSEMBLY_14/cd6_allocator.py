"""One all-domain six-key allocator, exact actual occurrence IDs.
Certified backends are imported unchanged; no table/semantics is rebuilt.
"""
import functools,json,sys
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent
OLD=P/'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13';NEW=P/'SE03_STEP2_UNARY_A_LIFT_14'
sys.path[:0]=[str(OLD),str(NEW)]
from source_funding import own_map,core7,with_owners
from debt_funding import build as core8,labels_core,freeze
from branch_funding import build as high
@functools.lru_cache(None)
def cert8():return json.loads((OLD/'bf8_comparison.json').read_text())
def allocate(rows,*,auxiliary_demands=None,fE=None,frozen_prior=None):
    if not rows:raise ValueError('six genuine keys require a nonempty history')
    actual=[r['occurrence'] for r in rows];T=len(rows)
    if actual!=list(range(actual[0],actual[0]+T)):raise ValueError('one contiguous actual source period required')
    if rows[-1]['after'][:2]!=rows[0]['before'][:2]:raise ValueError('exact A/full-B paired closure required')
    ids={t:i+1 for i,t in enumerate(actual)}
    local=[dict(r,occurrence=i+1) for i,r in enumerate(rows)]
    M={r['target'] for r in rows if r['genuine_F']};S=labels_core(freeze(rows[0]['before'][1]),M);k=len(S)
    if len(M)!=6 or k not in range(6,12):raise ValueError('outside certified six-key source partition')
    if k==6:
        v=own_map(local);assert set(v['h0'])==v['D'];v.update(h=dict(v['h0']),working_units=4)
    elif k==7:v=core7(local);v['working_units']=4
    elif k==8:v=core8(local,cert8());v['working_units']=v['max_working_units']
    else:v=high(local)
    def into(d):
        if d[0] not in ids:raise ValueError('owner/donor occurrence outside the actual period')
        return (ids[d[0]],)+tuple(d[1:])
    def back(d):return (actual[d[0]-1],)+tuple(d[1:])
    def restore(m):return {back(d):back(u) for d,u in m.items()}
    f=v['h'];owner=None
    if (auxiliary_demands is None)!=(fE is None):raise ValueError('supply BOTH actual auxiliary domain and certified fixed map')
    if fE is not None:
        E={into(d) for d in auxiliary_demands};fixed={into(d):into(u) for d,u in fE.items()}
        owner=with_owners(v,E,fixed)
        prior=restore(owner['prior']['allocation'])
        if frozen_prior is not None and prior!=frozen_prior:raise ValueError('supplied old partial map differs from certified original h0/l exchange')
        f=owner['extension']['allocation']
        owner={'common':{back(d) for d in owner['common']},'prior':prior,
            'additions':restore(owner['extension']['additions']),
            'all_old_values_fixed':True,
            'licensed_paths':[{'root':back(z['root']),'steps':[(back(d),back(u)) for d,u in z['steps']],
                'terminal_unit':back(z['terminal_unit'])} for z in owner['licensed']['paths']]}
    elif frozen_prior is not None:raise ValueError('old partial map needs its original common-owner data')
    D={back(d) for d in v['D']};U={back(u) for u in v['U']};answer=restore(f);h=restore(v['h']);h0=restore(v['h0'])
    assert set(answer)==D and len(set(answer.values()))==len(D) and set(answer.values())<=U
    assert all(h[d]==u for d,u in h0.items())
    assert len(D)==sum(r['qF'] for r in rows) and len(U)==2*sum(r['a'] for r in rows)
    return {'core':k,'marks':M,'fixed_full_core':S,'D':D,'U':U,'h0':h0,'h':h,'f':answer,'owners':owner,
        'working_bound':11,'actual_period':(actual[0],actual[-1]),'local_to_actual':actual,
        'backend_receipts':'unchanged backend construction; local occurrence i means actual local_to_actual[i-1]'}
def realize_aligned_period(mapping,T,copy_start,cut):
    """Transport relative word positions into (copy_start+cut,...,+cut+T].
    Caller certifies cut legality; this bijection does not authorize a cut.
    """
    if not 0<=cut<T:raise ValueError('cut index outside one period')
    def tau(t):
        if not 1<=t<=T:raise ValueError('borrowed source occurrence outside one period')
        return copy_start+t+(T if t<=cut else 0)
    return {(tau(d[0]),)+tuple(d[1:]):(tau(u[0]),)+tuple(u[1:]) for d,u in mapping.items()}
