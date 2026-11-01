"""Validate distinct physical source units; no FI/UD recognizer claim."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
path = HERE / 'full_source_replays.json'
data = json.loads(path.read_text(encoding='utf-8'))
rows = data['diagonal_return']['replay']
kept = [r for r in rows if r['mode'] == 'KEEP']
mapping = []
for i, row in enumerate(kept):
    demand_events = [j for j, ev in enumerate(row['B_events']) if ev[0] != 'ZIG']
    assert len(demand_events) == row['q']
    own_units = [[0, row['occurrence'], ev, bit] for ev in range(row['a']) for bit in [0, 1]]
    for j, ev in enumerate(demand_events):
        if j < len(own_units):
            unit = own_units[j]
            kind = 'own actual source occurrence'
        else:
            helper = kept[(i+1) % len(kept)]
            capacity_index = helper['q']+j-len(own_units)
            assert capacity_index < 2*helper['a']
            unit = [0, helper['occurrence'], capacity_index//2, capacity_index % 2]
            kind = 'distinct next KEEP spare unit'
        mapping.append(dict(demand=[0, row['occurrence'], ev], unit=unit, kind=kind))
assert len(mapping) == 176
assert len({tuple(r['unit']) for r in mapping}) == len(mapping)
assert len({tuple(r['demand']) for r in mapping}) == len(mapping)
assert all(rows[r['unit'][1]]['mode'] == 'KEEP' for r in mapping)
assert sum(r['kind'] == 'distinct next KEEP spare unit' for r in mapping) == 12
out = dict(status='PASS', source_replays_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
    checked_mapping=mapping, physical_cycles_represented=1, cycle_id=0,
    B_double_demands=176, distinct_A_units_used=176, reused_units=0,
    DELETE_units_used=0, reachability_prefix_units_used=0, helper_demand_assignments=12,
    reflection_uses_same_occurrence_event_ids=True,
    claim='source-cost injection using own units and distinct next-KEEP spare units',
    FI_UD_protocol_classification='NOT CLAIMED', new_original_CD_walk_class_settled=False)
with (HERE / 'event_unit_injection_certificate.json').open('x', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(json.dumps({k: out[k] for k in ['status', 'B_double_demands', 'distinct_A_units_used',
    'reused_units', 'DELETE_units_used', 'reachability_prefix_units_used', 'helper_demand_assignments']}, indent=2))
