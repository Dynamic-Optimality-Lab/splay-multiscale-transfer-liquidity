"""Independent pointer-source guard law, primitive recurrence and reachability audit."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def ck(ok,msg):
    if not ok:raise AssertionError(msg)
def main():
    cp=HERE/'guarded_B_cycle_certificate.json';cert=json.loads(cp.read_text(encoding='utf-8'))
    spec=importlib.util.spec_from_file_location('pointer_source',ROOT/'python/liquidity/legacy_embedding.py')
    p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
    def ptr(t):
        if t is None:return None
        z=p.mknode(t[0],ptr(t[1]),ptr(t[2]))
        for side in ('l','r'):
            if z[side] is not None:z[side]['p']=z
        return z
    def raw(t):return None if t is None else [t['k'],raw(t['l']),raw(t['r'])]
    def mirror(t):return None if t is None else [14-t[0],mirror(t[2]),mirror(t[1])]
    def vine(n):
        t=None
        for k in range(n,0,-1):t=[k,None,t]
        return t
    def inorder(t):return [] if t is None else inorder(t[1])+[t[0]]+inorder(t[2])
    def depth(t,x):
        d=0
        while t is not None:
            if t[0]==x:return d
            t=t[1] if x<t[0] else t[2];d+=1
        raise AssertionError('present source key')
    calls=trees=0
    def validate(t,keys):
        nonlocal trees
        ck(inorder(t)==keys,'strict BST and exact source key set');trees+=1
    def access(t,x,occ,keys):
        nonlocal calls
        validate(t,keys);d=depth(t,x);out,events=p.splay_trace(ptr(t),x);after=raw(out);validate(after,keys)
        ev=[[e['case'],e['lo'],e['hi'],e['orient']] for e in events]
        q=sum(e[0]!='ZIG' for e in ev);z=sum(e[0]=='ZIG' for e in ev)
        ck((q,z,len(ev))==(d//2,d%2,(d+1)//2),'source grouped doubles/zigs')
        calls+=1
        return after,dict(occurrence=occ,key=x,source_B=t,destination_B=after,d_B=d,q=q,z=z,B_events=ev)
    def mirror_events(events):
        cm={'LL':'RR','RR':'LL','LR':'RL','RL':'LR','ZIG':'ZIG'};om={'L':'R','R':'L','-':'-'}
        return [[cm[e[0]],14-e[2],14-e[1],om[e[3]]] for e in events]
    def mirror_row(r):return dict(r,key=14-r['key'],source_B=mirror(r['source_B']),destination_B=mirror(r['destination_B']),B_events=mirror_events(r['B_events']))
    keys=list(range(1,14));localkeys=list(range(1,13));mlocalkeys=list(range(2,14))
    targets=[1,9,5,3,11,7,2,10,6,4,12,8];word=[y for x in targets for y in (x,13)]
    initial=[13,vine(12),None];mi=mirror(initial);validate(initial,keys);validate(mi,keys)
    ck(cert['key_size']==13 and cert['initial_diagonal_B']==initial and cert['guard']==13 and
      cert['local_targets']==targets and cert['generator']==word and cert['lap_cap']==64,'literal gated construction')
    b,mb=initial,mi;rows=[];mrows=[];checks=[];boundaries=[dict(lap=0,B=b)];seen={json.dumps(b):0};start=end=None
    cases={};local_calls=0
    for lap in range(1,65):
        for x in targets:
            ck(b[0]==13 and mb[0]==1 and b[2] is None and mb[1] is None,'guard restored with untouched outside fringe')
            local=b[1];mlocal=mb[2];d=depth(local,x);away=bool(d%2 and x<local[0])
            full,lr=access(local,x,0,localkeys);mfull,mlr=access(mlocal,14-x,0,mlocalkeys);local_calls+=2
            ck(mlr==mirror_row(lr),'independent reflected local splay')
            expected=full;mexpected=mfull
            if away:
                ck(lr['B_events'][-1][0]=='ZIG' and lr['B_events'][-1][3]=='L' and full[2][0]==local[0],
                  'source final local left zig is the omitted one')
                u=full[2];expected=[u[0],[full[0],full[1],u[1]],u[2]]
                ck(mlr['B_events'][-1][0]=='ZIG' and mlr['B_events'][-1][3]=='R' and mfull[1][0]==mlocal[0],
                  'reflected omitted final right zig')
                mu=mfull[1];mexpected=[mu[0],mu[1],[mfull[0],mu[2],mfull[2]]]
            ck(mexpected==mirror(expected),'local law respects source reflection')
            occ=len(rows);b,r1=access(b,x,occ,keys);mb,mr1=access(mb,14-x,occ,keys)
            b,r2=access(b,13,occ+1,keys);mb,mr2=access(mb,1,occ+1,keys)
            ck(mr1==mirror_row(r1) and mr2==mirror_row(r2),'global source reflection, all intervals and orientations')
            ck(r1==cert['full_orbit_replay'][occ] and r2==cert['full_orbit_replay'][occ+1],'every tuple/pointer global row')
            ck(b==[13,expected,None] and mb==[1,None,mexpected],'exact returned shape law in both orientations')
            ck((r1['q'],r2['q'])==((d+1)//2,int(away)),'exact guard query/return double identity')
            check=dict(query_occurrence=occ,return_occurrence=occ+1,key=x,local_source=local,local_full_splay=full,
              local_events=lr['B_events'],local_depth=d,local_root=local[0],away_odd_case=away,
              expected_returned_local=expected,actual_returned_local=b[1],query_q=r1['q'],return_q=r2['q'])
            checks.append(check);rows.extend([r1,r2]);mrows.extend([mr1,mr2])
            label='zero' if d==0 else ('even' if d%2==0 else ('odd_away' if away else 'odd_toward'))
            cases[label]=cases.get(label,0)+1
        boundaries.append(dict(lap=lap,B=b));state=json.dumps(b)
        if state in seen:start=24*seen[state];end=len(rows);break
        seen[state]=lap
    ck(start==24 and end==48 and boundaries==cert['boundary_records'],'first exact whole-word recurrence')
    ck(checks==cert['guard_law_checkpoints'],'all declared guard identities from independent local/global sources')
    cyc=rows[start:end];mcyc=mrows[start:end]
    ck(cyc[-1]['destination_B']==cyc[0]['source_B'] and mcyc[-1]['destination_B']==mcyc[0]['source_B'],'true B closure in both orientations')
    # Decompose independently using a linear scan of the distinct-state stack.
    vertices=[cyc[0]['source_B']];origins=[start];edges=[];components=[]
    for r in cyc:
        ck(r['source_B']==vertices[-1],'source path remains valid after loop cancellation')
        dest=r['destination_B']
        if dest not in vertices:
            edges.append(r);vertices.append(dest);origins.append(r['occurrence']+1)
        else:
            j=vertices.index(dest);ee=edges[j:]+[r]
            ck(len({json.dumps(v['source_B']) for v in ee})==len(ee),'emitted cycle is simple, not a repeated period')
            components.append(dict(component_index=len(components),start_original_occurrence=origins[j],source_B=ee[0]['source_B'],
              word=[v['key'] for v in ee],edge_original_occurrences=[v['occurrence'] for v in ee],length=len(ee),
              Q_B=sum(v['q'] for v in ee),Z_B=sum(v['z'] for v in ee),G_B=sum(max(v['q']-2,0) for v in ee),simple=True))
            vertices=vertices[:j+1];origins=origins[:j+1];edges=edges[:j]
    ck(len(vertices)==1 and not edges and components==cert['simple_cycle_components'],'canonical full decomposition')
    ids=[i for c in components for i in c['edge_original_occurrences']]
    ck(sorted(ids)==list(range(start,end)) and len(ids)==len(set(ids)),'every original source edge assigned exactly once')
    whole=dict(source_start=start,source_end=end,transient_laps=1,period_laps=1,length=24,
      Q_B=sum(r['q'] for r in cyc),Z_B=sum(r['z'] for r in cyc),G_B=sum(max(r['q']-2,0) for r in cyc))
    ck(whole==cert['recurrent_walk'] and (whole['Q_B'],whole['Z_B'],whole['G_B'])==(38,10,9),'exact recurrent costs and G')
    ck(sum(c['G_B'] for c in components)==whole['G_B'] and len(components)==1,'no padding or concatenation creates success')
    selected=cert['selected_cycle'];component=next(c for c in components if c['G_B']>=5)
    ck(selected['component']==component and component['length']==24 and component['G_B']==9,'first simple threshold witness')
    ck(selected['reachability_prefix']==rows[:24],'source-exact reachability from the stated diagonal')
    expected=[dict(r,occurrence=i,original_occurrence=r['occurrence']) for i,r in enumerate(cyc)]
    ck(selected['full_cycle_replay']==expected,'complete primitive cycle provenance')
    t=initial
    for r in selected['reachability_prefix']:
        ck(t==r['source_B'],'prefix source sharing');t=r['destination_B']
    ck(t==component['source_B'],'prefix reaches exact recurrent input')
    before=t
    for r in selected['full_cycle_replay']:
        ck(t==r['source_B'],'selected cycle valid as its own repeated word');t=r['destination_B']
    ck(t==before,'selected extracted word exactly returns')
    ck(cert['outcome']=='B_HEADROOM_CERTIFIED' and cert['G_threshold']==5 and cert['primitive_cycle_required'] and
      cert['finite_fits']==cert['size_sweeps']==cert['adaptive_generator_changes']==cert['A_resets_executed']==cert['FI_UD_cut_trials']==0 and
      cert['matching_terminal_line']=='FROZEN' and cert['universal_CD']=='OPEN','scope and no unproved A reset claim')
    with (HERE/'reflected_cycle_certificate.json').open('x',encoding='utf-8') as f:
        json.dump(dict(initial_diagonal_B=mi,reachability_prefix=mrows[:24],cycle_replay=[dict(r,occurrence=i) for i,r in enumerate(mcyc)],
          word=[14-x for x in word],G_B=9,Q_B=38,Z_B=10,simple=True,source_exact=True),f,indent=2);f.write('\n')
    result=dict(status='PASS',date='2026-10-31',B_headroom_target='ACHIEVED',fixed_key_size=13,selected_cycle_length=24,
      selected_Q_B=38,selected_Z_B=10,selected_G_B=9,threshold=5,planned_two_one_StepEv_reset_capacity=4,
      G_minus_planned_capacity=5,simple_cycle=True,internal_repeated_B_states=0,period_multiplication_used=False,
      diagonal_reachability_prefix_length=24,whole_orbit_global_rows_per_orientation=len(rows),
      local_guard_pairs_per_orientation=len(checks),guard_law_case_counts=cases,
      global_pointer_source_accesses=calls-local_calls,local_pointer_source_accesses=local_calls,total_pointer_source_accesses=calls,
      strict_BST_tree_occurrences_validated=trees,canonical_components=len(components),edge_multiplicity_exact=True,
      new_finite_key_sizes=0,finite_fits=0,adaptive_generator_changes=0,A_resets_executed=0,FI_UD_cut_trials=0,
      actual_E_or_C_D_certified=False,strict_FI_only_closed_walk_coverage='NOT ESTABLISHED',universal_CD='OPEN',
      matching_terminal_line='FROZEN',producer_imported=False,old_recognizers_executed=False,
      certificate_sha256=hashlib.sha256(cp.read_bytes()).hexdigest())
    with (HERE/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False);f.write('\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
