"""Falsify a full physical credit invariant on complete original witnesses."""
import sys
import json
import gzip
from pathlib import Path
sys.dont_write_bytecode=True
from sources import T
HERE=Path(__file__).resolve().parent


def read(name):
    p=HERE/name
    with (gzip.open(p,'rt',encoding='utf-8') if p.suffix=='.gz' else p.open(encoding='utf-8')) as f:return json.load(f)


def zero_edges(t,stock,owner,cross_only=False):
    return {(k,child,side) for k in t.keys if stock[owner[k]]==0
            for side,child in enumerate(t.ch[k]) if child is not None and stock[owner[child]]==0
            and (not cross_only or owner[k]!=owner[child])}


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    cross_only='--cross-block' in sys.argv
    checked=0;counter=None
    for case in read('COMPLETE_SOURCE_AUDIT.json')['cases']:
        z=read(case['trace']);policy=read(case['local_bank']);keys=sorted(map(int,z['source']['initial_A']['children']))
        trees={a:T.B.K.OLD.Tree(z['source']['initial_'+a],keys) for a in ('A','B')}
        stock=policy['initial_greatest_fixed_point'].copy();owner={key:i for i,block in enumerate(z['blocks']) for key in block}
        steps={tuple(s['id']):s for s in z['steps']}
        assert zero_edges(trees['A'],stock,owner,cross_only)==zero_edges(trees['B'],stock,owner,cross_only)
        for row in policy['rows']:
            identifier=row['id']
            if identifier[0] in ('A','B'):
                step=steps[tuple(identifier)]
                for bit in step['bits']:trees[identifier[0]].rotate(bit['promoted'])
            for bank,value in zip(row['priority'],row['after']):stock[bank]=value
            checked+=1
            A=zero_edges(trees['A'],stock,owner,cross_only);B=zero_edges(trees['B'],stock,owner,cross_only)
            if A!=B:
                actor='A' if A-B else 'B';edge=min((A-B) if A-B else (B-A))
                counter={'complete_trace':case['trace'],'complete_policy':case['local_bank'],'q':case['q'],
                    'original_event':identifier,'event_index':row['event'],'edge_present_only_in':actor,
                    'physical_directed_edge':list(edge),'edge_owner_banks':[owner[edge[0]],owner[edge[1]]],
                    'owner_stocks':[stock[owner[edge[0]]],stock[owner[edge[1]]]],
                    'counter_event_paid':row['paid'],'counter_event_unpaid':row['unpaid'],
                    'initial_forest_relation':True,'all_previous_checked_boundaries_satisfied':True,
                    'snapshots':{a:trees[a].state() for a in trees},'stock':stock}
                break
        if counter:break
    result={'status':'REFUTED_EXACT_ORIGINAL_PHYSICAL_INVARIANT' if counter else 'NO_HIT_IN_BOUNDED_ORIGINAL_AUDIT',
        'candidate':'CROSS_BLOCK_ZERO_EDGE_CANDIDATE.json' if cross_only else 'ZERO_EDGE_INVARIANT_CANDIDATE.json','checked_boundaries':checked,'counterexample':counter,
        'bank_funding_refuted':False,'universal_CD':'OPEN'}
    p=HERE/('CROSS_BLOCK_ZERO_EDGE_RESULT.json' if cross_only else 'ZERO_EDGE_INVARIANT_RESULT.json');assert not p.exists();p.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'status':result['status'],'checked_boundaries':checked,
        'event':None if counter is None else counter['original_event'],
        'edge':None if counter is None else counter['physical_directed_edge'],'universal_CD':'OPEN'}))


if __name__=='__main__':main()
