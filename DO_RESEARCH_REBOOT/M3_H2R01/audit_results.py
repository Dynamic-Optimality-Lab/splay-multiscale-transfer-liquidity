"""Independent certificate completeness, full-root replay and signed-obstruction audit."""
import sys,json,time,hashlib
from pathlib import Path
from functools import lru_cache
from collections import Counter
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_H2R01','DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
import splay as S
import verify_full_mixed as F
from terminal_potential import CappedPotential
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
BASE=Path('DO_RESEARCH_REBOOT/M3_H2R01');OUT=BASE/'audit_results.json'
@lru_cache(None)
def trees(a,b):
    if a==b:return (S.LEAF,)
    return tuple(S.node(k,l,r) for k in range(a,b) for l in trees(a,k) for r in trees(k+1,b))
def read(name):return json.loads((BASE/name).read_text())
def main():
    assert not OUT.exists();start=time.process_time();P=CappedPotential()
    assert len(set(P.trees))==4862 and set(P.trees)==set(trees(0,9))
    kernel=read('fringe_kernel_certificate.json');rows=kernel['rows']
    assert len(rows)==43758
    assert {(r['entry_core'],r['target']) for r in rows}==set((i,x) for i in range(4862) for x in range(9))
    retained=[r for r in rows if r['gap0_childless_at_exit']]
    assert len(retained)==16842
    zeros=[r for r in retained if r['w']==0]
    fails=[r for r in retained if r['residual']<0]
    assert len(zeros)==1024 and all(r['residual']>=0 for r in zeros)
    assert fails==kernel['failures'] and len(fails)==3
    assert [(r['entry_core'],r['target'],r['exit_core']) for r in fails]==[(952,2,1917),(1710,2,1937),(2538,3,2141)]
    assert all(r['w']==1 and r['psi_source']==2 and r['psi_destination']==0 and r['residual']==-1 for r in fails)
    assert all(r['psi_destination']>=1 for r in zeros)
    primitive=read('ten_node_rotation_certificate.json')
    assert primitive['cases']==570 and len(primitive['rows'])==570
    assert all(r['all_115_fields_reflexive'] and r['pins_sha256']==hashlib.sha256(json.dumps(r['pins'],sort_keys=True).encode()).hexdigest() for r in primitive['rows'])
    terminal=read('terminal_floor_certificate.json')
    assert terminal['old_joint_ordinary_values_checked']==251480 and terminal['terminal_rows']==4224
    assert terminal['total_checks']==420904 and terminal['joint_below_negative_psi']
    assert all(r['psi_destination']>=r['terminal_q']-2 for r in terminal['rows'])
    d=DAG();L=build_slow(d,'MXL');assert len(d.nodes)==1400081
    controls=read('original_h2_controls.json')['records']+read('original_fringe_controls.json')['records']
    assert len(controls)==13;labels=set();negative_residuals=[]
    for r in controls:
        assert r['label'] not in labels;labels.add(r['label']);e=r['environment']
        assert set(e)==set(d.vars);F.bounds(d,e);assert d.ev_ground(L['root'],e)
        assert e['MXL_H']==r['H']==2 and e['MXLbt_q']==r['q'] and e['MXL_w']==r['w']==4-r['q']
        for tag,state in (('MXLs',r['source']),('MXLt',r['destination'])):
            assert e[tag+'_mu']==state['mu']
            assert [e[tag+'_sg'+str(i)] for i in range(10)]==state['sigma']
            assert e[tag+'_b_broot']==state['b']['root']
            for f in F.FIELDS:assert [e[tag+'_b_b'+f+str(i)] for i in range(19)]==state['b'][f]
            for i,(k,s,x) in enumerate(state['alpha']):
                assert e[tag+'_ak'+str(i)]==k and e[tag+'_aS'+str(i)]==bool(s) and e[tag+'_aI'+str(i)]==x
        ps=P.inspect(r['source']);pt=P.inspect(r['destination'])
        assert r['potential_source']==ps and r['potential_destination']==pt
        residual=r['w']-pt['capped_joint']+ps['capped_joint'];assert r['reduced_weight']==residual
        assert r['source']['mu']==r['destination']['mu'] and r['source']['sigma']==r['destination']['sigma']
        assert r['source']['mu'].bit_count()==5 and F.phi(r['source'])==F.phi(r['destination'])==-3
        if residual<0:negative_residuals.append(r['label'])
        assert time.process_time()-start<300,'UNKNOWN: audit cap'
    assert len(negative_residuals)==3
    returns=read('exception_returns.json');bridges=read('zero_bridge_search.json')
    assert not returns['negative_B_cycle_candidates'] and bridges['negative_B_candidates']==0
    result={'status':'COMPLETE','complete_ordered_core_trees':4862,'kernel_queries':43758,
            'retained_kernel_rows':len(retained),'weight_zero_rows_passed':len(zeros),
            'weight_one_rows_passed':sum(r['w']==1 and r['residual']>=0 for r in retained),
            'weight_one_obstructions':3,'primitive_symbolic_cases':570,
            'primitive_symbolic_scalar_identities':570*115,'full_original_low_roots_replayed':13,
            'full_saved_ordinary_state_fields_checked':True,'masks':sorted({r['source']['mu'] for r in controls}),
            'negative_residual_labels':negative_residuals,'certified_negative_mixed_cycles':0,
            'h0_rule':'no active true-path B rotation at h=0; do not replace the inherited anomalous high h=0 correction',
            'claim':'principal sigma=0 H2 law proved; all chi8 H2 zero helpers covered; capped +1 fringe extension refuted on three kernels',
            'cpu_seconds':round(time.process_time()-start,3)}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result),flush=True)
if __name__=='__main__':main()
