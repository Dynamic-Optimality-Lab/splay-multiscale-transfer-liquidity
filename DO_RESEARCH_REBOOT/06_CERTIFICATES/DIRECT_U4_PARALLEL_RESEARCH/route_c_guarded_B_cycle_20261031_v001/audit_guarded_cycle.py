"""One guarded source recurrence and canonical simple-cycle extraction; no fit."""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
OLD=HERE.parent/'route_c_two_reset_budget_20261031_v001'
STAGE=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:json.dump(value,f,indent=2,ensure_ascii=False);f.write('\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def main():
    inherited=json.loads((OLD/'entry_source_pins.json').read_text(encoding='utf-8'))
    pins=dict(inherited['files'])
    for rel,h in pins.items():assert sha(ROOT/rel)==h,rel
    for p in HERE.parent.rglob('*'):
        if p.is_file() and HERE not in p.parents:pins[p.relative_to(ROOT).as_posix()]=sha(p)
    stage={p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    status=git('status','--porcelain=v1','--untracked-files=no');assert not status and len(stage)==125
    save('entry_source_pins.json',dict(date='2026-10-31',head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),
      tracked_status=status,files=pins,stage_files=stage,inherited_pins=len(inherited['files'])))
    spec=importlib.util.spec_from_file_location('tuple_source',ROOT/'python/independent/splay.py')
    s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s);L=s.LEAF
    def raw(t):return None if t==L else [t[1],raw(t[2]),raw(t[3])]
    def tup(t):return L if t is None else s.node(t[0],tup(t[1]),tup(t[2]))
    def row(t,x,occ):
        found,d=s.lookup(t,x);assert found
        after,events=s.trace(t,x);q=sum(e[0]!='ZIG' for e in events);z=sum(e[0]=='ZIG' for e in events)
        assert (q,z,len(events))==(d//2,d%2,(d+1)//2)
        return after,dict(occurrence=occ,key=x,source_B=raw(t),destination_B=raw(after),d_B=d,q=q,z=z,B_events=events)
    targets=[1,9,5,3,11,7,2,10,6,4,12,8];word=[v for x in targets for v in (x,13)]
    initial=s.node(13,s.vine(12),L);b=initial;seen={b:0};rows=[];checks=[];boundaries=[dict(lap=0,B=raw(b))];start=end=None
    for lap in range(1,65):
        for x in targets:
            assert b[1]==13 and b[3]==L
            local=b[2];found,d=s.lookup(local,x);assert found
            full,local_events=s.trace(local,x);away=d%2==1 and x<local[1]
            expected=full
            if away:
                assert local_events[-1][0]=='ZIG' and local_events[-1][3]=='L' and full[3][1]==local[1]
                root=full[3];expected=s.node(root[1],s.node(full[1],full[2],root[2]),root[3])
            before_occ=len(rows);b,r1=row(b,x,len(rows));rows.append(r1)
            b,r2=row(b,13,len(rows));rows.append(r2)
            assert b==s.node(13,expected,L)
            assert (r1['q'],r2['q'])==((d+1)//2,int(away))
            checks.append(dict(query_occurrence=before_occ,return_occurrence=before_occ+1,key=x,
              local_source=raw(local),local_full_splay=raw(full),local_events=local_events,local_depth=d,
              local_root=local[1],away_odd_case=away,expected_returned_local=raw(expected),
              actual_returned_local=raw(b[2]),query_q=r1['q'],return_q=r2['q']))
        boundaries.append(dict(lap=lap,B=raw(b)))
        if b in seen:start=24*seen[b];end=len(rows);break
        seen[b]=lap
    components=[];selected=None;whole=None
    if start is not None:
        cyc=rows[start:end];vertices=[tup(cyc[0]['source_B'])];origins=[start];edges=[];where={vertices[0]:0}
        whole=dict(source_start=start,source_end=end,transient_laps=start//24,period_laps=(end-start)//24,
          length=len(cyc),Q_B=sum(r['q'] for r in cyc),Z_B=sum(r['z'] for r in cyc),
          G_B=sum(max(r['q']-2,0) for r in cyc))
        for r in cyc:
            assert tup(r['source_B'])==vertices[-1]
            dest=tup(r['destination_B'])
            if dest not in where:
                edges.append(r);vertices.append(dest);origins.append(r['occurrence']+1);where[dest]=len(vertices)-1
            else:
                j=where[dest];ee=edges[j:]+[r]
                assert ee[0]['source_B']==ee[-1]['destination_B']
                assert len({tup(v['source_B']) for v in ee})==len(ee)
                comp=dict(component_index=len(components),start_original_occurrence=origins[j],
                  source_B=ee[0]['source_B'],word=[v['key'] for v in ee],
                  edge_original_occurrences=[v['occurrence'] for v in ee],length=len(ee),
                  Q_B=sum(v['q'] for v in ee),Z_B=sum(v['z'] for v in ee),G_B=sum(max(v['q']-2,0) for v in ee),simple=True)
                components.append(comp)
                if selected is None and comp['G_B']>=5:
                    selected=dict(component=comp,reachability_prefix=rows[:origins[j]],
                      full_cycle_replay=[dict(v,occurrence=k,original_occurrence=v['occurrence']) for k,v in enumerate(ee)])
                edges=edges[:j];vertices=vertices[:j+1];origins=origins[:j+1];where={v:k for k,v in enumerate(vertices)}
        assert len(vertices)==1 and not edges
        ids=[v for c in components for v in c['edge_original_occurrences']]
        assert sorted(ids)==list(range(start,end)) and len(ids)==len(set(ids))
        assert sum(c['G_B'] for c in components)==whole['G_B'] and sum(c['Q_B'] for c in components)==whole['Q_B']
        if selected is not None:
            t=initial
            for r in selected['reachability_prefix']:
                assert raw(t)==r['source_B'];t,ev=s.trace(t,r['key']);assert raw(t)==r['destination_B']
            target=t
            for r in selected['full_cycle_replay']:
                assert raw(t)==r['source_B'];t,ev=s.trace(t,r['key']);assert raw(t)==r['destination_B']
            assert t==target
    outcome='B_HEADROOM_CERTIFIED' if selected is not None else ('OPEN_LAP_CAP' if start is None else 'NO_SIMPLE_COMPONENT_REACHES_FIVE')
    cert=dict(schema='maximum-guard-source-cycle-v1',date='2026-10-31',key_size=13,initial_diagonal_B=raw(initial),
      guard=13,local_targets=targets,generator=word,lap_cap=64,full_orbit_replay=rows,guard_law_checkpoints=checks,
      boundary_records=boundaries,recurrent_walk=whole,simple_cycle_components=components,selected_cycle=selected,
      outcome=outcome,G_threshold=5,primitive_cycle_required=True,finite_fits=0,size_sweeps=0,
      adaptive_generator_changes=0,A_resets_executed=0,FI_UD_cut_trials=0,
      matching_terminal_line='FROZEN',universal_CD='OPEN',strict_FI_only_closed_walk_coverage='NOT ESTABLISHED')
    save('guarded_B_cycle_certificate.json',cert)
    print(json.dumps(dict(preserved_files=len(pins),stage_files=len(stage),outcome=outcome,recurrent_walk=whole,
      components=[{k:v for k,v in c.items() if k not in ('source_B','edge_original_occurrences')} for c in components],
      selected=selected and selected['component']),indent=2))
if __name__=='__main__':main()
