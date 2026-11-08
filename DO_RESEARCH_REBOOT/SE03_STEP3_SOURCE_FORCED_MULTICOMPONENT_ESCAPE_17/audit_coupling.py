"""Producer analysis of the physical coupling and existing source cut.
No separate implementation audit or splay replay is performed.
"""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def read(n):return json.loads((B/n).read_text(encoding='utf-8'))
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
def unpack(v):return {tuple(x['demand']):tuple(x['unit']) for x in v}
def main():
    w=read('two_component_preparation_repair.json');old=w['old_source']
    a=unpack(old['old_a']);h=unpack(old['leaf_h']);fE=unpack(old['f6'])
    ia={u:d for d,u in a.items()};ih={u:d for d,u in h.items()};ie={u:d for d,u in fE.items()}
    D={(t['occurrence'],k) for t in old['rows'] for k in range(1,t['qF']+1)}
    comp=[];all_C=set();all_U=set()
    for p in w['old_blocked_components']:
        C={tuple(s['demand']) for s in p['steps']}|{tuple(p['frontier'])}
        P={tuple(p['root'])};HC={h[d] for d in C if d in h};paid={a[d] for d in C-P}
        assert HC==paid and len(HC)==len(C)-1
        assert not C&all_C and not HC&all_U
        all_C|=C;all_U|=HC
        comp.append({'root':p['root'],'frontier':p['frontier'],'demands':sorted(C),
            'internal_comparison_units':sorted(HC),'fixed_paid_units':sorted(paid),
            'deficiency_for_this_comparison_only':1,'source_complete_saturated':False})
    unit_records=[]
    for p in w['preparation_repairs']:
        u=tuple(p['terminal']);t=next(t for t in old['rows'] if t['occurrence']==u[0])
        assert u not in ia and u not in ih and 1<=u[1]<=t['a']
        aux_owner=ie.get(u)
        assert aux_owner is None or aux_owner not in D
        unit_records.append({'root':p['root'],'unit':u,'mode':t['mode'],'access_target':t['target'],
            'A_path':t['A_path'],'A_events_at_occurrence':t['A_events'],
            'selected_StepEv':t['A_events'][u[1]-1],
            'old_effective_full_owner':ia.get(u),'old_leaf_comparison_preimage':ih.get(u),
            'archived_auxiliary_owner':aux_owner,
            'auxiliary_status':'UNUSED_BY_f6' if aux_owner is None else 'E_ONLY_EFFECTIVE_CLAIM_RETIRED_IN_FULL_LEDGER'})
    assert {tuple(x['unit']) for x in unit_records}=={(35,2,0),(35,2,1)}
    out('component_cut_and_owner_inventory.json',{'status':'PRODUCER_PROOF_DERIVATION_AUDIT_PENDING',
        'components':comp,'union_demands':sorted(all_C),'union_internal_units':sorted(all_U),
        'initial_comparison_boundary_holes':sorted(tuple(x['frontier']) for x in comp),
        'two_bit_source_escape_inventory':unit_records,
        'old_single_bit_candidate':old['allowed_deep_only_tail'],
        'physical_coupling':'candidate restriction assigns the same singleton tail pool to two otherwise disjoint blocked comparison components',
        'not_full_source_cut':'the preparation-tail edges leave it, so it is not saturated under all demonstrated source rules'})
    print(json.dumps({'status':'COUPLING_PRODUCER_PASS','cut_size':len(all_C),'internal_units':len(all_U),
        'actual_donors':unit_records}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_coupling_exit.json',{'whole_process_CPU_seconds':time.process_time(),
        'error':error,'source_engine_calls':0,'new_finite_tests':0,'old_semantic_rows_replayed':0})
