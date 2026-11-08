"""Preserve v1; correct the inherited physical-tree field name and checkpoint results.

Use the EXISTING frozen DAG.simplify for repeated mask substitutions;
all private witness fields are pinned, only the two shared mu vars remain.
V1 already executed all126 complete roots before the later schema error.
"""
from pathlib import Path
p=Path('DO_RESEARCH_REBOOT/M3_MSK01/original_audit.py');q=p.with_name('original_audit_v2.py');assert not q.exists();s=p.read_text()
s=s.replace("original_audit.json","original_audit_v2.json").replace("seed['A_source']","seed['A_source_physical']")
marker='    for marks in itertools.combinations(range(9),5):'
assert marker in s
block='''    reductions={};muvars={d.nodes[L['s'].mu][3][1],d.nodes[L['t'].mu][3][1]}
    for x,r in seeds.items():
        rr=d.simplify(L['root'],{k:v for k,v in r['environment'].items() if k not in muvars})
        assert set(d.vars_in(rr))<=muvars
        reductions[x]={'root':rr,'remaining_vars':sorted(d.vars_in(rr)),
          'reachable_nodes':[[n,d.nodes[n]] for n in d.topo([rr])]}
        assert len(d.nodes)<4000000
'''
s=s.replace(marker,block+marker)
old="V.put(d,e,L['s'].mu,mu);V.put(d,e,L['t'].mu,mu);V.bounds(d,e);assert d.ev_ground(L['root'],e)"
assert s.count(old)==1
s=s.replace(old,"V.put(d,e,L['s'].mu,mu);V.put(d,e,L['t'].mu,mu);V.bounds(d,e);assert d.ev_ground(reductions[x]['root'],e)")
s=s.replace("    assert len(runs)==126","    assert len(runs)==126\n    with (BASE/'mask_roots_v2.json').open('x',encoding='utf-8') as f:json.dump({'status':'PASS','runs':runs,'base_environments':seeds,'exact_original_partial_evaluation':reductions},f,indent=2)")
s=s.replace("'base_environments':seeds,","'base_environments':seeds,'exact_original_partial_evaluation':reductions,")
with q.open('x',encoding='utf-8') as f:f.write(s)
print(str(q))
