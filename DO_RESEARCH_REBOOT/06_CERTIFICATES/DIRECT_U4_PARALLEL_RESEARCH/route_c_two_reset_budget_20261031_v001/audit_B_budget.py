"""Exact B-only gate for the fixed two-reset architecture; no A search or fit."""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
OLD=HERE.parent/'route_c_sparse_reset_strictness_20261031_v001'
STAGE=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:json.dump(value,f,indent=2,ensure_ascii=False);f.write('\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def main():
    oldpins=json.loads((OLD/'entry_source_pins.json').read_text(encoding='utf-8'))
    pins=dict(oldpins['files'])
    for rel,h in pins.items():assert sha(ROOT/rel)==h,rel
    for p in HERE.parent.rglob('*'):
        if p.is_file() and HERE not in p.parents:pins[p.relative_to(ROOT).as_posix()]=sha(p)
    stage={p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    status=git('status','--porcelain=v1','--untracked-files=no');assert not status and len(stage)==125
    save('entry_source_pins.json',dict(date='2026-10-31',head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),
      tracked_status=status,files=pins,stage_files=stage,inherited_pins=len(oldpins['files'])))
    spec=importlib.util.spec_from_file_location('tuple_source',ROOT/'python/independent/splay.py')
    s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s);L=s.LEAF
    def raw(t):return None if t==L else [t[1],raw(t[2]),raw(t[3])]
    keys=[1,9,5,13,3,11,7,2,10,6,4,12,8]
    b=s.vine(13);rows=[];boundaries=[dict(lap=0,B=raw(b))];seen={b:0};start=end=None
    for lap in range(1,65):
        for key in keys:
            found,d=s.lookup(b,key);assert found
            bp,events=s.trace(b,key);q=sum(e[0]!='ZIG' for e in events);z=sum(e[0]=='ZIG' for e in events)
            assert (q,z,len(events))==(d//2,d%2,(d+1)//2)
            rows.append(dict(occurrence=len(rows),key=key,source_B=raw(b),destination_B=raw(bp),d_B=d,q=q,z=z,B_events=events))
            b=bp
        boundaries.append(dict(lap=lap,B=raw(b)))
        if b in seen:start=13*seen[b];end=len(rows);break
        seen[b]=lap
    cycle=rows[start:end] if start is not None else None
    period=(end-start)//13 if cycle is not None else None
    G=sum(max(r['q']-2,0) for r in cycle) if cycle is not None else None
    passed=cycle is not None and G>4*period
    cert=dict(schema='two-reset-fixed-B-budget-v1',date='2026-10-31',key_size=13,initial_B=raw(s.vine(13)),
      KEEP_skeleton=keys,lap_cap=64,full_replay=rows,boundary_records=boundaries,
      first_repeated_boundary=start is not None,transient_laps=start//13 if start is not None else None,
      primitive_period_laps=period,cycle_source_start=start,cycle_source_end=end,cycle_G_B=G,
      two_effective_reset_capacity=4*period if period is not None else None,B_budget_passed=passed,
      q_vector=[r['q'] for r in cycle] if cycle is not None else None,
      outcome='BUDGET_PASSES' if passed else ('BUDGET_BLOCKED' if cycle is not None else 'OPEN_B_LAP_CAP'),
      A_policy_cases_executed=0,fixed_A_policy_count_if_passed=78,finite_fits=0,size_sweeps=0,
      adaptive_skeleton_changes=0,matching_terminal_line='FROZEN',universal_CD='OPEN')
    save('B_budget_certificate.json',cert)
    print(json.dumps(dict(preserved_files=len(pins),stage_files=len(stage),outcome=cert['outcome'],
      transient_laps=cert['transient_laps'],period_laps=period,G_B=G,reset_capacity=cert['two_effective_reset_capacity'],
      q_vector=cert['q_vector']),indent=2))
if __name__=='__main__':main()
