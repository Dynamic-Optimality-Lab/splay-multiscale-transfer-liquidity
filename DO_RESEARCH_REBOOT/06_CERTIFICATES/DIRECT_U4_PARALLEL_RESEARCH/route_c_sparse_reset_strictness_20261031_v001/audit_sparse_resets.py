"""Exact finite one-reset classification at the fixed thirteen-key size."""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
OLD=HERE.parent/'route_c_strict_cycle_audit_20261031_v001'
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
    def mirror(t,n):return L if t==L else s.node(n+1-t[1],mirror(t[3],n),mirror(t[2],n))
    def depth(t,x):
        found,d=s.lookup(t,x);assert found;return d
    def step(a,b,mode,x,occ):
        da=depth(a,x);ap,ae=s.trace(a,x)
        if mode=='K':db=depth(b,x);bp,be=s.trace(b,x)
        else:db,bp,be=None,b,[]
        q=sum(e[0]!='ZIG' for e in be);z=sum(e[0]=='ZIG' for e in be)
        assert len(ae)==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0)
        return ap,bp,dict(occurrence=occ,mode=mode,key=x,source_A=raw(a),source_B=raw(b),destination_A=raw(ap),
          destination_B=raw(bp),d_A=da,d_B=db,a=len(ae),q=q,z=z,A_events=ae,B_events=be,delta=q-2*len(ae))
    def blocks(rows):
        n=len(rows);leaders=[i for i,r in enumerate(rows) if r['a']>0];bs=[]
        for u,i in enumerate(leaders):
            end=leaders[(u+1)%len(leaders)];ids=[i];j=(i+1)%n
            while j!=end:ids.append(j);j=(j+1)%n
            key=rows[i]['key'];a=rows[i]['a'];q=sum(rows[t]['q'] for t in ids)
            assert all(rows[t]['a']==0 and rows[t]['key']==key for t in ids[1:])
            kk=[t for t in ids if rows[t]['mode']=='K'];active=[t for t in kk if rows[t]['d_B']>0];assert len(active)<=1
            bs.append(dict(leader=i,key=key,indices=ids,a=a,q=q,delta=q-2*a,has_KEEP=bool(kk),
              first_KEEP=kk[0] if kk else None,B_active_access=active[0] if active else None))
        return bs
    def collar(rows,bs,i):
        t=rows[bs[i]['B_active_access']]['source_B']
        return {t[0]}|{ch[0] for ch in t[1:] if ch is not None}
    def coarse_bound(rows,bs,i,j,y):
        at=bs[i]['B_active_access'];pre,post=rows[at]['source_B'],rows[at]['destination_B']
        d,h=depth(tup(pre),y),depth(tup(post),y);assert d>=0 and h>=0
        off=(j-i)%len(bs);assert off>0
        active=[bs[(i+z)%len(bs)]['B_active_access'] for z in range(1,off)
          if bs[(i+z)%len(bs)]['B_active_access'] is not None]
        hh=[dict(after_access=at,depth=h)];previous=h
        for at2 in active:
            dd=depth(tup(rows[at2]['destination_B']),y);assert dd<=previous+2
            hh.append(dict(after_access=at2,depth=dd));previous=dd
        c=h//2+len(active) if bs[j]['has_KEEP'] else 0
        assert bs[j]['q']<=c
        return dict(anchor=i,anchor_occurrence=bs[i]['leader'],pre_depth=d,h=h,k=len(active),ceiling=c,
          intervening_B_occurrences=active,depth_history=hh)

    def path(t,x):
        keys=[];directions=[]
        while t is not None:
            keys.append(t[0])
            if t[0]==x:return keys,directions
            side='L' if x<t[0] else 'R';directions.append(side);t=t[1] if side=='L' else t[2]
        raise AssertionError('present source key')
    def envelope(t,x,y):
        px,dirs=path(t,x);py,_=path(t,y);d=len(dirs);h=len(py)-1
        common=0
        while common<min(len(px),len(py)) and px[common]==py[common]:common+=1
        lca=common-1;ops=[]
        for number in range(d//2):
            top=d-2*(number+1)
            ops.append(dict(case=''.join(dirs[top:top+2]),site_depth=top,grandparent=px[top],parent=px[top+1]))
        if d%2:ops.append(dict(case='ZIG',site_depth=0,grandparent=px[0],parent=None))
        role='root_noop' if d==0 else ('accessed' if x==y else None)
        entry=None;mu=r=m=0;candidate=h
        if role=='accessed':candidate=0
        if role is None:
            entry=next(z for z,op in enumerate(ops) if op['site_depth']<=lca);op=ops[entry]
            if op['case']=='ZIG':role='zig_root' if y==op['grandparent'] else 'zig_fringe';mu=1
            elif y==op['parent']:role='parent';mu=0
            else:role='grandparent' if y==op['grandparent'] else 'fringe';mu=2
            outer=[op for op in ops[entry+1:] if op['case']!='ZIG'];r=len(outer)
            matching='LL' if y<x else 'RR';m=sum(op['case']==matching for op in outer)
            candidate=h+mu-r-m
        U=min(h+2,max(0,candidate))
        return dict(source_depth=h,access_depth=d,lca_depth=lca,operations=ops,entry_operation=entry,
          entry_role=role,first_gain_allowance=mu,outer_doubles=r,matching_outer_doubles=m,
          target_side='equal' if y==x else ('left' if y<x else 'right'),upper_depth=U)
    def bound(rows,bs,i,j,y,refined=True):
        result=coarse_bound(rows,bs,i,j,y)
        if not refined:return result
        active=result['intervening_B_occurrences'];profile=None;first=None;firstactual=None
        c=result['ceiling']
        if active:
            first=active[0];fr=rows[first]
            assert fr['source_B']==rows[bs[i]['B_active_access']]['destination_B']
            profile=envelope(fr['source_B'],fr['key'],y)
            assert [op['case'] for op in profile['operations']]==[e[0] for e in fr['B_events']]
            firstactual=depth(tup(fr['destination_B']),y);assert firstactual<=profile['upper_depth']
            c=profile['upper_depth']//2+len(active)-1 if bs[j]['has_KEEP'] else 0
        assert bs[j]['q']<=c<=result['ceiling']
        result.update(coarse_ceiling=result['ceiling'],ceiling=c,first_intervention=first,
          first_frame_profile=profile,actual_first_post_depth_for_verification=firstactual)
        return result
    def scan(rows,bs,cut,refined=True):
        history=[];paid={};pools=[];assignments=[]
        units={i:[[b['leader'],e,bit] for e in range(b['a']) for bit in (0,1)] for i,b in enumerate(bs)}
        demands={i:[[t,e] for t in b['indices'] for e,event in enumerate(rows[t]['B_events']) if event[0]!='ZIG'] for i,b in enumerate(bs)}
        for turn in range(len(bs)):
            j=(cut+turn)%len(bs);b=bs[j];capacity=2*b['a']
            if b['delta']>0:
                for d,c in zip(demands[j][:capacity],units[j]):assignments.append(dict(demand=d,credit=c,kind='positive_local'))
                history.append(j);paid[j]=0;continue
            facts=[bound(rows,bs,i,j,b['key'],refined) for i in history]
            ceiling=min(f['ceiling'] for f in facts) if facts else None
            reserve=min(capacity,ceiling) if facts else capacity
            assert b['q']<=reserve
            for d,c in zip(demands[j],units[j][:reserve]):assignments.append(dict(demand=d,credit=c,kind='payer_local'))
            cursor=reserve;loans=[]
            for i in history:
                owed=bs[i]['delta']-paid[i]
                if not owed:continue
                amount=min(owed,capacity-cursor)
                if not amount:break
                start=paid[i];selected=units[j][cursor:cursor+amount]
                for d,c in zip(demands[i][2*bs[i]['a']+start:2*bs[i]['a']+start+amount],selected):
                    assignments.append(dict(demand=d,credit=c,kind='split_payer_transfer'))
                loans.append(dict(anchor=i,anchor_occurrence=bs[i]['leader'],demand_start=start,demand_end=start+amount,
                  credit_start=cursor,credit_end=cursor+amount,credits=selected))
                cursor+=amount;paid[i]+=amount
            pools.append(dict(block=j,payer_occurrence=b['leader'],key=b['key'],capacity=capacity,source_history=list(history),
              facts=facts,ceiling=ceiling,reservation=reserve,own_q=b['q'],loans=loans,
              retired_unused=capacity-b['q']-(cursor-reserve),balances_after=[[i,bs[i]['delta']-paid[i]] for i in history]))
        unpaid=[[bs[i]['leader'],bs[i]['delta']-paid[i]] for i in history if paid[i]<bs[i]['delta']]
        allD={tuple(d) for ds in demands.values() for d in ds};allC={tuple(c) for cs in units.values() for c in cs}
        usedD=[tuple(v['demand']) for v in assignments];usedC=[tuple(v['credit']) for v in assignments]
        assert len(usedD)==len(set(usedD))==len(usedC)==len(set(usedC)) and set(usedD)<=allD and set(usedC)<=allC
        assert len(allD)-len(assignments)==sum(v for _,v in unpaid)
        if not unpaid:assert set(usedD)==allD
        return dict(cut=cut,accepted=not unpaid,pools=pools,unpaid=unpaid,unpaid_excess=sum(v for _,v in unpaid),
          credit_assignments=assignments,unused_credit_count=len(allC)-len(assignments))


    def compact(t):
        return dict(cut=t['cut'],accepted=t['accepted'],unpaid=t['unpaid'],unpaid_excess=t['unpaid_excess'],
          transfers=[[p['payer_occurrence'],v['anchor_occurrence'],v['demand_start'],v['demand_end'],v['credit_start'],v['credit_end']]
            for p in t['pools'] for v in p['loans']])

    skeleton=[13,11,12,9,10,7,8,5,6,3,4,1,2]
    initial=s.vine(13);setup_word=[['D',13],['D',12]];a0=b0=initial;setup=[]
    for k,(mode,x) in enumerate(setup_word):a0,b0,r0=step(a0,b0,mode,x,-k-1);setup.append(r0)
    def digest_pair(a,b):
        return hashlib.sha256(json.dumps([a,b],separators=(',',':')).encode('utf-8')).hexdigest()
    def compact_row(r0):
        d={k:v for k,v in r0.items() if k not in ('source_A','source_B','destination_A','destination_B')}
        d['source_pair_sha256']=digest_pair(r0['source_A'],r0['source_B'])
        d['destination_pair_sha256']=digest_pair(r0['destination_A'],r0['destination_B'])
        return d
    def orbit(gap,target):
        word=[]
        for pos,key in enumerate(skeleton):
            word.append(['K',key])
            if pos==gap:word.append(['D',target])
        a,b=a0,b0;seen={(a,b):0};rows=[]
        boundaries=[dict(lap=0,A=raw(a),B=raw(b))];start=end=None
        for lap in range(1,65):
            for mode,x in word:
                a,b,r0=step(a,b,mode,x,len(rows));rows.append(r0)
                if mode=='D':
                    assert r0['a']>=1 and r0['destination_A'][0]==target
                    assert r0['destination_B'][0]==skeleton[gap] and r0['destination_A'][0]!=r0['destination_B'][0]
                    if gap==2 and target==13:assert r0['a']==1
            boundaries.append(dict(lap=lap,A=raw(a),B=raw(b)))
            if (a,b) in seen:start=14*seen[(a,b)];end=len(rows);break
            seen[(a,b)]=lap
        meta=None;test=None;full=None
        if start is None:outcome='OPEN_LAP_CAP'
        else:
            cycle=[dict(r0,occurrence=k) for k,r0 in enumerate(rows[start:end])]
            assert cycle[-1]['destination_A']==cycle[0]['source_A'] and cycle[-1]['destination_B']==cycle[0]['source_B']
            bs=blocks(cycle);E=sum(max(v['delta'],0) for v in bs);CD=sum(2*v['a'] for v in bs if not v['has_KEEP'])
            diagonal=[r0['occurrence'] for r0 in cycle if r0['source_A']==r0['source_B']]
            meta=dict(transient_laps=start//14,period_laps=(end-start)//14,cycle_length=len(cycle),E=E,C_D=CD,
              A=sum(r0['a'] for r0 in cycle),Q_B=sum(r0['q'] for r0 in cycle),Z_B=sum(r0['z'] for r0 in cycle),
              diagonal_source_occurrences=diagonal,reset_costs=[r0['a'] for r0 in cycle if r0['mode']=='D'],actual_pair_closure=True)
            if diagonal:outcome='DIAGONAL_IN_CYCLE'
            elif E<=CD:outcome='DELETE_DOMINATED'
            else:
                coarse=[scan(cycle,bs,cut,False) for cut in range(len(bs))]
                fresh=[scan(cycle,bs,cut,True) for cut in range(len(bs))]
                oldgood=[v for v in coarse if v['accepted']];good=[v for v in fresh if v['accepted']]
                assert {v['cut'] for v in oldgood}<={v['cut'] for v in good}
                test=dict(old_UD_trials=[compact(v) for v in coarse],FI_trials=[compact(v) for v in fresh],
                  old_UD_accepted_cuts=[v['cut'] for v in oldgood],FI_accepted_cuts=[v['cut'] for v in good],
                  selected_FI_ledger=good[0] if good else None,
                  FI_alternative_assignment_checks=sum(len(v['credit_assignments']) for v in good),
                  UD_alternative_assignment_checks=sum(len(v['credit_assignments']) for v in oldgood))
                outcome='UD_ACCEPTS' if oldgood else ('STRICT_FOUND' if good else 'FI_REJECTS')
                if outcome=='STRICT_FOUND':full=dict(full_orbit_replay=rows,full_cycle_replay=cycle,
                  full_reachability_replay=setup+rows[:start],cycle_blocks=bs)
        case=dict(gap=gap,target=target,word=word,lap_cap=64,boundaries=boundaries,
          orbit_replay=[compact_row(r0) for r0 in rows],cycle=meta,comparison=test,outcome=outcome)
        return case,full
    cases=[];strict=None;shared_B={};counts={}
    for gap in range(2,13):
        for target in range(1,14):
            if target in (skeleton[gap],skeleton[(gap+1)%13]):continue
            case,full=orbit(gap,target);cases.append(case)
            for boundary in case['boundaries']:
                lap=boundary['lap']
                if lap in shared_B:assert shared_B[lap]==boundary['B']
                else:shared_B[lap]=boundary['B']
            counts[case['outcome']]=counts.get(case['outcome'],0)+1
            if len(cases)%16==0 or case['comparison'] is not None:
                print(json.dumps(dict(processed=len(cases),gap=gap,target=target,outcome=case['outcome'],counts=counts)),flush=True)
            if full is not None:
                strict=dict(case_index=len(cases)-1,**full);break
        if strict is not None:break
    cert=dict(schema='fixed-thirteen-key-single-reset-classification-v1',date='2026-10-31',skeleton=skeleton,
      initial_diagonal=raw(initial),setup_prefix=setup_word,setup_replay=setup,orbit_initial_A=raw(a0),orbit_initial_B=raw(b0),
      declared_parameter_count=121,cases=cases,shared_B_boundary_states=shared_B,outcome_counts=counts,strict_witness=strict,
      strict_new_closed_walk_coverage=bool(strict),parameter_order='gap 2..12, target 1..13, exclude adjacent KEEP targets',
      stopped_at_first_strict_witness=bool(strict),all_declared_cases_examined=len(cases)==121,
      all_examined_orbits_closed=all(v['outcome']!='OPEN_LAP_CAP' for v in cases),
      finite_fits=0,size_sweeps=0,adaptive_generator_changes=0,lap_cap=64,matching_terminal_line='FROZEN',universal_CD='OPEN',
      old_UD_FI_rules_changed=False,actual_payer_q_used_as_reservation_oracle=False)
    save('sparse_reset_certificate.json',cert)
    print(json.dumps(dict(preserved_files=len(pins),stage_files=len(stage),processed=len(cases),outcomes=counts,
      strict_new_closed_walk_coverage=bool(strict),strict_case=strict and {k:cases[strict['case_index']][k] for k in ('gap','target','cycle')}),indent=2))

if __name__=='__main__':main()
