"""Constructively erase closed original DELETE loops without touching old inputs."""
import sys
import json
import gzip
import importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('credit_gap_normalization_immutable',
    HERE.parent/'GSO_CONSERVATIVE_TRANSPORT_20261122_V001/verify.py')
V=importlib.util.module_from_spec(spec);sys.modules[spec.name]=V;spec.loader.exec_module(V)


def fingerprint(tree):
    rows=[];stack=[tree]
    while stack:
        t=stack.pop();rows.append((t.k,t.l.k if t.l else None,t.r.k if t.r else None))
        stack.extend(v for v in (t.l,t.r) if v is not None)
    return (tree.k,tuple(sorted(rows)))


def delete_gap(initial,operations):
    assert all(mode=='D' for mode,_ in operations),'A KEEP may change B; only DELETE loops are licensed.'
    t=initial;states=[t];keys=[fingerprint(t)];index={keys[0]:0};kept=[];removed=[];original_cost=0
    for position,(_,target) in enumerate(operations,1):
        t,depth=V.V.rebuild(t,target,lambda *args:None,lambda *args:None);original_cost+=(depth+1)//2
        key=fingerprint(t)
        if key in index:
            at=index[key];removed.append([row['original_position'] for row in kept[at:]]+[position])
            kept=kept[:at];states=states[:at+1];keys=keys[:at+1];index={k:i for i,k in enumerate(keys)}
            t=states[-1]
        else:
            kept.append({'original_position':position,'target':target});states.append(t);keys.append(key);index[key]=len(keys)-1
    final=fingerprint(t);reduced=initial;cost=0
    for row in kept:
        reduced,depth=V.V.rebuild(reduced,row['target'],lambda *args:None,lambda *args:None);cost+=(depth+1)//2
    assert fingerprint(reduced)==final and len(keys)==len(set(keys)) and cost<=original_cost
    removed_ids=[p for loop in removed for p in loop];all_ids=[row['original_position'] for row in kept]+removed_ids
    assert sorted(all_ids)==list(range(1,len(operations)+1))
    return {'kept':kept,'erased_loops':removed,'original_A_cost':original_cost,'reduced_A_cost':cost,
        'complete_A_state_preserved':True,'kept_A_states_distinct':True,
        'scope':'A single literal DELETE-only gap. Whole-source cyclic normalization uses a KEEP cut and unchanged physical boundary states.'}


def main():
    old=HERE.parent/'GLOBAL_ACCOUNTING_SYNTHESIS_20261121_V001/F2_s2.json.gz'
    with gzip.open(old,'rt',encoding='utf-8') as f:source=json.load(f)['source']
    # Read-only historical control: no fifth new complete source is generated.
    gap=source['operations'][:2];result=delete_gap(V.immutable(source['initial_A']),gap)
    assert result['erased_loops']==[[1,2]] and result['kept']==[]
    assert result['original_A_cost']==2 and result['reduced_A_cost']==0
    output={'historical_complete_source':'GLOBAL_ACCOUNTING_SYNTHESIS_20261121_V001/F2_s2.json.gz',
        'original_literal_gap':gap,'normalization':result,'new_complete_source_materialized':False,
        'root_scope_restriction':'None: explicit loop erasure preserves Q_B and does not increase A. This is a lossless normalization, not an assumption excluding difficult sources.',
        'global_bound':'OPEN'}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        p=HERE/'NORMALIZATION_CONTROL.json'
        if p.exists():assert json.loads(p.read_text())==output
        else:p.write_text(json.dumps(output,indent=2),encoding='utf-8')
    print(json.dumps({'erased_original_DELETE_operations':2,'A_before':2,'A_after':0,'root_scope_restricted':False}))


if __name__=='__main__':main()
