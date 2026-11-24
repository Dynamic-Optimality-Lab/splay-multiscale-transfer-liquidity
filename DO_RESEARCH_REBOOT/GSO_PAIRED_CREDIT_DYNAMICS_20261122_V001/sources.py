"""Original cost-preserving rigid gap expansion; no old source is modified."""
import sys
import importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('credit_dynamics_old_transport',
    HERE.parent/'GSO_CONSERVATIVE_TRANSPORT_20261122_V001/transport.py')
T=importlib.util.module_from_spec(spec);sys.modules[spec.name]=T;spec.loader.exec_module(T)


def inflate(source,gaps):
    m=len(source['initial_A']['children']);assert len(gaps)==m+1 and all(type(v)==int and v>=0 for v in gaps)
    oldkeys=list(range(1,m+1));mapping={};gapkeys={};cursor=1
    for gap in range(m+1):
        gapkeys[gap]=list(range(cursor,cursor+gaps[gap]));cursor+=gaps[gap]
        if gap<m:mapping[gap+1]=cursor;cursor+=1
    def full(tree):
        nodes={}
        for gap,keys in gapkeys.items():
            for j,key in enumerate(keys):nodes[str(key)]=[None,keys[j+1] if j+1<len(keys) else None]
        for old in oldkeys:
            l,r=tree['children'][str(old)]
            nodes[str(mapping[old])]=[mapping[l] if l is not None else (gapkeys[old-1][0] if gapkeys[old-1] else None),
                mapping[r] if r is not None else (gapkeys[old][0] if gapkeys[old] else None)]
        assert len(nodes)==cursor-1
        return {'root':mapping[tree['root']],'children':nodes}
    out={'name':'cardinality_alias__'+source['name'],'initial_A':full(source['initial_A']),
        'initial_B':full(source['initial_B']),'diagonal':full(source['diagonal']),
        'prefix':[[mode,mapping[x]] for mode,x in source.get('prefix',[])],
        'operations':[[mode,mapping[x]] for mode,x in source['operations']],
        'expected_A':source['expected_A'],'expected_Q':28*source['q']+25,
        'embedding':{'old_keys':oldkeys,'mapping':mapping,'gap_sizes':gaps,
                     'physical_support':cursor-1,'rigid_hangers':'Right vines, never accessed or used as pivots.'},
        'original_q_parameter':source['q']}
    return out
