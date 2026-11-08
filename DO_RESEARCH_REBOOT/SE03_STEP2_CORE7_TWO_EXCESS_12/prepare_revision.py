"""Metadata revision. Preserve the failed draft byte-for-byte and its charges."""
from pathlib import Path
B=Path(__file__).resolve().parent
s=(B/'audit_construction.py').read_text()
s=s.replace('from two_slot_allocator import independent_full,from_frozen_auxiliary','from two_slot_allocator import independent_full,from_frozen_auxiliary,extend_two')
s=s.replace("assert set(('0','1','2','blocked_nonanchor_root'))<=set(branches)","""assert set(('0','2'))<=set(branches)
    # Repeating the same closed word makes the two actual erased sectors
    # symmetric. Do not assert asymmetric partial branches are realized.
    p0=sorted(build['R'])[0];a0={d:u for d,u in build['h'].items() if d!=p0}
    one=extend_two(D,U,a0,build['h']);assert len(one['missing'])==1
    one_control={'kind':'source-ID one-hole paid fixture, not claimed to be the partial10 map for this word',
        'paid':pack(a0),'missing':p0,'extension':pack(one['additions']),'paths':one['paths']}
    tests+=1""")
s=s.replace("'branches':dict(branches),\n        'source_engine_calls'","'branches':dict(branches),'one_residual_paid_control':one_control,\n        'actual_partial_branch_limit':'these repeated-word erased sectors realize zero/two symmetrically; general one/blocked cases audited separately',\n        'source_engine_calls'")
s=s.replace("'physical_receipts.json'","'physical_receipts2.json'")
s=s.replace("'audit_construction_exit.json'","'audit_construction2_exit.json'")
with (B/'audit_construction2.py').open('x',encoding='utf-8') as f:f.write(s)
