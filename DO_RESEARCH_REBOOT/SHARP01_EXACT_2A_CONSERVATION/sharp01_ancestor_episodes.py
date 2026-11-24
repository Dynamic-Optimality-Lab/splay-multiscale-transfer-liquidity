"""Exact origins of B-only ancestry at every positive-u gap; saved data only."""
from pathlib import Path
from collections import defaultdict,Counter
import json,time
from sharp01_oracle import Tree
BASE=Path(__file__).resolve().parent;start=time.process_time();out=[];kinds=Counter()
idx=json.loads((BASE/'SHARP01_GAP_LEDGER.json').read_text())['ledgers']
for item in idx:
    l=json.loads((BASE/item['path']).read_text());wanted=defaultdict(set)
    for g in l['gaps']:
        if g['u']:
            for y in g['B_only_ancestors']:wanted[y].add(g['target'])
    stream=defaultdict(list)
    for ep,e in enumerate(l['events']):
        for field,truth in (('ancestry_removed',False),('ancestry_added',True)):
            y,xx=e[field]
            if y in wanted:
                for x in wanted[y].intersection(xx):stream[y,x].append((ep,e['id'],truth,e['SET_sign'],e['middle']))
    ta=Tree(l['source']['initial_A']);tb=Tree(l['source']['initial_B']);episodes={}
    for pair,changes in stream.items():
        y,x=pair;a=y in ta.path(x)[:-1];b=y in tb.path(x)[:-1];initial=(a,b);trans=[]
        for ep,eid,truth,sign,middle in changes:
            old=b and not a
            if eid[0]=='A':assert a!=truth;a=truth
            else:assert b!=truth;b=truth
            new=b and not a
            if old!=new:trans.append({'event_position':ep,'id':eid,'became_B_only':new,'origin_kind':('A_loss' if eid[0]=='A' else 'B_gain') if new else ('A_gain' if eid[0]=='A' else 'B_loss'),'SET_sign':sign,'middle_subtree_root':middle})
        assert (a,b)==initial
        episodes[pair]=trans
    records=[]
    for g in l['gaps']:
        if not g['u']:continue
        boundary=l['operations'][g['previous_KEEP_operation_id']-1]['event_range'][1]
        for y in g['B_only_ancestors']:
            ts=episodes[y,g['target']];born=[t for t in ts if t['became_B_only']];dead=[t for t in ts if not t['became_B_only']]
            assert born and dead
            origin=next((t for t in reversed(born) if t['event_position']<boundary),born[-1])
            end=next((t for t in dead if t['event_position']>=boundary),dead[0])
            kinds[origin['origin_kind']]+=1
            records.append({'gap_index':g['gap_index'],'target':g['target'],'B_only_ancestor':y,'actual_discrepancy_origin':origin,'first_end_after_gap_start':end})
    out.append({'source':item['name'],'gap_start_B_only_episodes':records})
    assert time.process_time()-start<20
result={'sources':out,'origin_reference_counts':dict(kinds),'counting_note':'A physical origin may be referenced by several gaps/ancestors; counts are not distinct paid events','cpu_seconds':time.process_time()-start}
(BASE/'SHARP01_ANCESTOR_EPISODES.json').write_text(json.dumps(result,separators=(',',':')))
print(json.dumps({k:v for k,v in result.items() if k!='sources'}))
