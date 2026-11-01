"""Independent pointer classification and exact old-UD certificates for sparse resets."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def ck(ok,message):
    if not ok:raise AssertionError(message)

def main():
    cp=HERE/'sparse_reset_certificate.json';cert=json.loads(cp.read_text(encoding='utf-8'))
    spec=importlib.util.spec_from_file_location('pointer_source',ROOT/'python/liquidity/legacy_embedding.py')
    p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
    def ptr(t):
        if t is None:return None
        z=p.mknode(t[0],ptr(t[1]),ptr(t[2]))
        for side in ('l','r'):
            if z[side] is not None:z[side]['p']=z
        return z
    def raw(t):return None if t is None else [t['k'],raw(t['l']),raw(t['r'])]
    def mirror(t,n):return None if t is None else [n+1-t[0],mirror(t[2],n),mirror(t[1],n)]
    def vine(n):
        t=None
        for k in range(n,0,-1):t=[k,None,t]
        return t
    def inorder(t):
        if t is None:return []
        ck(isinstance(t,list) and len(t)==3 and type(t[0]) is int,'raw BST format')
        return inorder(t[1])+[t[0]]+inorder(t[2])
    def depth(t,x):
        d=0
        while t is not None:
            if t[0]==x:return d
            t=t[1] if x<t[0] else t[2];d+=1
        raise AssertionError('request must be present')
    def events(es):return [[e['case'],e['lo'],e['hi'],e['orient']] for e in es]
    calls=0
    def access(t,x):
        nonlocal calls
        d=depth(t,x);out,es=p.splay_trace(ptr(t),x);q=sum(e['case']!='ZIG' for e in es);z=sum(e['case']=='ZIG' for e in es)
        ck(q==d//2 and z==d%2 and len(es)==(d+1)//2,'source event count')
        calls+=1
        return raw(out),events(es),d,q,z
    def replay(a,b,word,rows):
        ck(len(word)==len(rows),'entire literal source word')
        for (mode,x),r in zip(word,rows):
            ck((a,b,mode,x)==(r['source_A'],r['source_B'],r['mode'],r['key']),'successive physical pair')
            aa,ae,da,_,_=access(a,x)
            if mode=='K':bb,be,db,q,z=access(b,x)
            else:bb,be,db,q,z=b,[],None,0,0
            ck((aa,bb,ae,be,da,db,len(ae),q,z,q-2*len(ae))==
              (r['destination_A'],r['destination_B'],r['A_events'],r['B_events'],r['d_A'],r['d_B'],r['a'],r['q'],r['z'],r['delta']),
              'pointer endpoints, identities, orientations and costs')
            a,b=aa,bb
        return a,b
    def blocks(rows):
        leaders=[i for i,r in enumerate(rows) if r['a']];out=[];N=len(rows)
        for at,i in enumerate(leaders):
            end=leaders[(at+1)%len(leaders)];ids=[i];j=(i+1)%N
            while j!=end:ids.append(j);j=(j+1)%N
            ck(all(rows[t]['a']==0 and rows[t]['key']==rows[i]['key'] for t in ids[1:]),'maximal source A-root block')
            keeps=[t for t in ids if rows[t]['mode']=='K'];changed=[t for t in keeps if rows[t]['d_B']>0]
            ck(len(changed)<=1,'unique genuine B change in block')
            q=sum(rows[t]['q'] for t in ids);a=rows[i]['a']
            out.append(dict(leader=i,key=rows[i]['key'],indices=ids,a=a,q=q,delta=q-2*a,has_KEEP=bool(keeps),
              first_KEEP=keeps[0] if keeps else None,B_active_access=changed[0] if changed else None))
        return out
    def shallow(rows,bs,i):
        t=rows[bs[i]['B_active_access']]['source_B'];return {t[0]}|{c[0] for c in t[1:] if c is not None}
    def coarse_fact(rows,bs,i,j):
        y=bs[j]['key'];at=bs[i]['B_active_access'];r=rows[at]
        before=depth(r['source_B'],y);h=depth(r['destination_B'],y)
        ck(before>=0 and h>=0,'actual arbitrary-key post-anchor depth, including zero')
        off=(j-i)%len(bs);ck(off>0,'source anchor is earlier in selected one-period pass')
        changed=[];hh=[dict(after_access=at,depth=h)];previous=h
        for advance in range(1,off):
            b=bs[(i+advance)%len(bs)];ai=b['B_active_access']
            if ai is None:continue
            dd=depth(rows[ai]['destination_B'],y);ck(dd<=previous+2,'whole-splay displacement including zero-double zig')
            changed.append(ai);hh.append(dict(after_access=ai,depth=dd));previous=dd
        ceiling=h//2+len(changed) if bs[j]['has_KEEP'] else 0
        if bs[j]['has_KEEP']:
            actual=depth(rows[bs[j]['first_KEEP']]['source_B'],y)
            ck(actual<=h+2*len(changed) and bs[j]['q']==actual//2,'delayed bound on physical payer work')
        ck(bs[j]['q']<=ceiling,'own work covered by each fact separately')
        return dict(anchor=i,anchor_occurrence=bs[i]['leader'],pre_depth=before,h=h,k=len(changed),ceiling=ceiling,
          intervening_B_occurrences=changed,depth_history=hh)

    def search_path(t,key):
        out=[]
        while t is not None:
            out.append(t[0])
            if key==t[0]:return out
            t=t[1] if key<t[0] else t[2]
        raise AssertionError('present source path')
    def subtree(t,key):
        while t is not None:
            if t[0]==key:return t
            t=t[1] if key<t[0] else t[2]
        raise AssertionError('operation site ancestor present')
    def envelope(t,x,y,source_events):
        px,py=search_path(t,x),search_path(t,y);d=len(px)-1;h=len(py)-1
        same=0
        for ax,ay in zip(px,py):
            if ax!=ay:break
            same+=1
        ops=[]
        ck(len(source_events)==(d+1)//2,'complete pointer-source operation list')
        for index,event in enumerate(source_events):
            zig=event[0]=='ZIG';top=0 if zig else d-2*(index+1)
            ck(zig==(index==len(source_events)-1 and d%2==1),'only final zig')
            ops.append(dict(case=event[0],site_depth=top,grandparent=px[top],parent=None if zig else px[top+1]))
        if d==0:role='root_noop';entry=None;mu=outer=matched=0;cap=h
        elif x==y:role='accessed';entry=None;mu=outer=matched=0;cap=0
        else:
            # Choose entry by subtree membership, independently of the producer's LCA test.
            entry=next(index for index,op in enumerate(ops) if y in inorder(subtree(t,op['grandparent'])))
            op=ops[entry]
            if op['case']=='ZIG':role='zig_root' if y==op['grandparent'] else 'zig_fringe';mu=1
            elif y==op['parent']:role='parent';mu=0
            else:role='grandparent' if y==op['grandparent'] else 'fringe';mu=2
            following=[op['case'] for op in ops[entry+1:] if op['case']!='ZIG']
            outer=len(following);matched=sum(case==('LL' if y<x else 'RR') for case in following)
            cap=h+mu-outer-matched
        return dict(source_depth=h,access_depth=d,lca_depth=same-1,operations=ops,entry_operation=entry,
          entry_role=role,first_gain_allowance=mu,outer_doubles=outer,matching_outer_doubles=matched,
          target_side='equal' if y==x else ('left' if y<x else 'right'),upper_depth=min(h+2,max(0,cap)))
    def fact(rows,bs,i,j,refined=True):
        f=coarse_fact(rows,bs,i,j)
        if not refined:return f
        first=None;profile=None;actual_first=None;c=f['ceiling'];changes=f['intervening_B_occurrences']
        if changes:
            first=changes[0];r=rows[first];y=bs[j]['key']
            ck(r['source_B']==rows[bs[i]['B_active_access']]['destination_B'],'no hidden B change before first intervention')
            profile=envelope(r['source_B'],r['key'],y,r['B_events'])
            actual_first=depth(r['destination_B'],y);ck(actual_first<=profile['upper_depth'],'universal frame upper bound at actual first source event')
            c=profile['upper_depth']//2+len(changes)-1 if bs[j]['has_KEEP'] else 0
        ck(bs[j]['q']<=c<=f['ceiling'],'refined own-work ceiling sound and pointwise no larger')
        f.update(coarse_ceiling=f['ceiling'],ceiling=c,first_intervention=first,first_frame_profile=profile,
          actual_first_post_depth_for_verification=actual_first)
        return f
    def independent_pass(rows,bs,cut,refined=True):
        demands={i:[[t,e] for t in b['indices'] for e,ev in enumerate(rows[t]['B_events']) if ev[0]!='ZIG'] for i,b in enumerate(bs)}
        credits={i:[[b['leader'],e,bit] for e in range(b['a']) for bit in (0,1)] for i,b in enumerate(bs)}
        allD={tuple(d) for ds in demands.values() for d in ds};allC={tuple(c) for cs in credits.values() for c in cs}
        claims=[];usedD=set();usedC=set();history=[];cursor={};pools=[]
        def claim(d,c,kind):
            td,tc=tuple(d),tuple(c)
            ck(td in allD and tc in allC and td not in usedD and tc not in usedC,'unique actual cycle demand and unit; no prefix/lap budget')
            usedD.add(td);usedC.add(tc);claims.append(dict(demand=d,credit=c,kind=kind))
        for j in [(cut+v)%len(bs) for v in range(len(bs))]:
            b=bs[j];cap=len(credits[j])
            if b['delta']>0:
                for d,c in zip(demands[j][:cap],credits[j]):claim(d,c,'positive_local')
                history.append(j);cursor[j]=0;continue
            facts=[fact(rows,bs,i,j,refined) for i in history]
            ceiling=min(f['ceiling'] for f in facts) if facts else None
            reserve=min(cap,ceiling) if facts else cap;ck(b['q']<=reserve,'own-work prefix is reserved once')
            for z,d in enumerate(demands[j]):claim(d,credits[j][z],'payer_local')
            left=cap-reserve;outgoing=reserve;loans=[]
            eligible=[i for i in history if cursor[i]<bs[i]['delta']]
            for i in eligible:
                if not left:break
                amount=min(left,bs[i]['delta']-cursor[i]);start=cursor[i]
                selected=credits[j][outgoing:outgoing+amount]
                for offset,c in enumerate(selected):claim(demands[i][2*bs[i]['a']+start+offset],c,'split_payer_transfer')
                loans.append(dict(anchor=i,anchor_occurrence=bs[i]['leader'],demand_start=start,demand_end=start+amount,
                  credit_start=outgoing,credit_end=outgoing+amount,credits=selected))
                cursor[i]+=amount;outgoing+=amount;left-=amount
            ck(len(credits[j])-len([c for c in usedC if c[0]==b['leader']])==cap-b['q']-(outgoing-reserve),'retired physical pool exactly once')
            pools.append(dict(block=j,payer_occurrence=b['leader'],key=b['key'],capacity=cap,source_history=history[:],facts=facts,
              ceiling=ceiling,reservation=reserve,own_q=b['q'],loans=loans,retired_unused=cap-b['q']-(outgoing-reserve),
              balances_after=[[i,bs[i]['delta']-cursor[i]] for i in history]))
        unpaid=[[bs[i]['leader'],bs[i]['delta']-cursor[i]] for i in history if cursor[i]<bs[i]['delta']]
        ck(len(allD)-len(usedD)==sum(v for _,v in unpaid),'residual conservation at end of exactly one period')
        if not unpaid:ck(usedD==allD,'every B double paid')
        return dict(cut=cut,accepted=not unpaid,pools=pools,unpaid=unpaid,unpaid_excess=sum(v for _,v in unpaid),
          credit_assignments=claims,unused_credit_count=len(allC)-len(usedC))


    def compact(t):
        return dict(cut=t['cut'],accepted=t['accepted'],unpaid=t['unpaid'],unpaid_excess=t['unpaid_excess'],
          transfers=[[p['payer_occurrence'],v['anchor_occurrence'],v['demand_start'],v['demand_end'],v['credit_start'],v['credit_end']]
            for p in t['pools'] for v in p['loans']])
    def delete_only_map(rows,bs):
        values=[b['delta'] if b['delta']>0 else (-2*b['a'] if not b['has_KEEP'] else 0) for b in bs]
        cumulative=[0]
        for v in values:cumulative.append(cumulative[-1]+v)
        total=cumulative[-1];ck(total<=0,'delete-only sufficient budget')
        cut=min(range(len(cumulative)),key=lambda j:cumulative[j])%len(bs)
        order=[(cut+j)%len(bs) for j in range(len(bs))];rotated=[values[j] for j in order]
        ck(all(sum(rotated[j:])<=0 for j in range(len(rotated))),'correct MINIMUM cut makes every suffix nonpositive')
        credits={i:[[b['leader'],e,bit] for e in range(b['a']) for bit in (0,1)] for i,b in enumerate(bs)}
        demands={i:[[t,e] for t in b['indices'] for e,ev in enumerate(rows[t]['B_events']) if ev[0]!='ZIG'] for i,b in enumerate(bs)}
        allD={tuple(d) for ds in demands.values() for d in ds};allC={tuple(c) for cs in credits.values() for c in cs}
        claims=[];usedD=set();usedC=set();pending=[];paid={};pool_visits=[]
        def claim(d,c,kind):
            dd,cc=tuple(d),tuple(c)
            ck(dd in allD and cc in allC and dd not in usedD and cc not in usedC,'one actual unit and demand; no reuse')
            usedD.add(dd);usedC.add(cc);claims.append(dict(demand=d,credit=c,kind=kind))
        debt=0;queue_history=[]
        for j in order:
            b=bs[j];capacity=2*b['a']
            if b['delta']>0:
                for d,c in zip(demands[j][:capacity],credits[j]):claim(d,c,'positive_local')
                pending.append(j);paid[j]=0;debt+=b['delta']
            elif b['has_KEEP']:
                for d,c in zip(demands[j],credits[j]):claim(d,c,'KEEP_local_only')
            else:
                ck(b['q']==0,'pure DELETE block has no own B work')
                offset=0
                for i in pending:
                    left=bs[i]['delta']-paid[i];amount=min(left,capacity-offset)
                    if not amount:continue
                    for z in range(amount):claim(demands[i][2*bs[i]['a']+paid[i]+z],credits[j][offset+z],'DELETE_only_transfer')
                    paid[i]+=amount;offset+=amount;debt-=amount
                    if offset==capacity:break
                pool_visits.append(dict(block=j,used=offset,retired=capacity-offset))
            queue_history.append(debt)
        ck(debt==0 and usedD==allD,'closed-walk deletion budget supplies every residual')
        ck(len(pool_visits)==len({v['block'] for v in pool_visits}),'each DELETE pool visited once')
        return dict(cut=cut,E=sum(max(b['delta'],0) for b in bs),C_D=sum(2*b['a'] for b in bs if not b['has_KEEP']),
          cumulative_sums=cumulative,rotated_values=rotated,queue_history=queue_history,credit_assignments=claims,pool_visits=pool_visits,
          unused_credit_count=len(allC)-len(usedC),no_reuse=True)

    def digest_pair(a,b):return hashlib.sha256(json.dumps([a,b],separators=(',',':')).encode('utf-8')).hexdigest()
    def compact_row(r):
        v={k:x for k,x in r.items() if k not in ('source_A','source_B','destination_A','destination_B')}
        v.update(source_pair_sha256=digest_pair(r['source_A'],r['source_B']),
          destination_pair_sha256=digest_pair(r['destination_A'],r['destination_B']))
        return v
    def advance(a,b,mode,x,occ):
        aa,ae,da,_,_=access(a,x)
        if mode=='K':bb,be,db,q,z=access(b,x)
        else:bb,be,db,q,z=b,[],None,0,0
        r=dict(occurrence=occ,mode=mode,key=x,source_A=a,source_B=b,destination_A=aa,destination_B=bb,
          d_A=da,d_B=db,a=len(ae),q=q,z=z,A_events=ae,B_events=be,delta=q-2*len(ae))
        return aa,bb,r
    def mirrored_events(es):
        case_map={'LL':'RR','RR':'LL','LR':'RL','RL':'LR','ZIG':'ZIG'}
        orient_map={'L':'R','R':'L','-':'-'}
        return [[case_map[e[0]],14-e[2],14-e[1],orient_map[e[3]]] for e in es]
    def mirrored_row(r):
        out=dict(r,key=14-r['key'],A_events=mirrored_events(r['A_events']),B_events=mirrored_events(r['B_events']))
        for k in ('source_A','source_B','destination_A','destination_B'):out[k]=mirror(r[k],13)
        return out
    valid_trees=0
    def validate_row(r):
        nonlocal valid_trees
        for k in ('source_A','source_B','destination_A','destination_B'):
            ck(inorder(r[k])==list(range(1,14)),'strict raw BST and complete fixed key set');valid_trees+=1
    skeleton=[13,11,12,9,10,7,8,5,6,3,4,1,2]
    expected_parameters=[(g,t) for g in range(2,13) for t in range(1,14) if t not in (skeleton[g],skeleton[(g+1)%13])]
    ck(len(expected_parameters)==121 and cert['declared_parameter_count']==121 and cert['skeleton']==skeleton,'entire gated finite parameter class')
    ck([(v['gap'],v['target']) for v in cert['cases']]==expected_parameters and cert['all_declared_cases_examined'],'no parameter replacement or omitted case')
    initial=vine(13);mirror_initial=mirror(initial,13);valid_trees+=2
    ck(cert['initial_diagonal']==initial and cert['setup_prefix']==[['D',13],['D',12]],'fixed seed and reachability prefix')
    a0=b0=initial;ma0=mb0=mirror_initial
    for i,(mode,x) in enumerate(cert['setup_prefix']):
        a0,b0,r=advance(a0,b0,mode,x,-i-1);ma0,mb0,mr=advance(ma0,mb0,mode,14-x,-i-1)
        ck(r==cert['setup_replay'][i] and mr==mirrored_row(r),'both exact setup orientations')
        validate_row(r);validate_row(mr)
    ck((a0,b0)==(cert['orbit_initial_A'],cert['orbit_initial_B']),'source setup endpoints')
    outcomes={};period_counts={};funding_counts={};shared_B={};maps=[];orbit_rows=0;cycle_rows=0;max_laps=0
    non_diag=0;non_diag_positive=0;UD_units=DELETE_units=0;all_primitive=True
    for ci,case in enumerate(cert['cases']):
        g,t=case['gap'],case['target'];word=[]
        for pos,key in enumerate(skeleton):
            word.append(['K',key])
            if pos==g:word.append(['D',t])
        ck(case['word']==word and case['lap_cap']==64,'literal single-reset generator and cap')
        a,b=a0,b0;ma,mb=ma0,mb0;rows=[];mrows=[]
        seen={json.dumps([a,b],separators=(',',':')):0};start=end=None;boundary_records=[dict(lap=0,A=a,B=b)]
        ck(len(case['orbit_replay'])%14==0,'complete whole-word boundary observation')
        total_laps=len(case['orbit_replay'])//14;ck(1<=total_laps<=64,'predeclared bound')
        for lap in range(1,total_laps+1):
            for mode,x in word:
                occ=len(rows);a,b,r=advance(a,b,mode,x,occ);ma,mb,mr=advance(ma,mb,mode,14-x,occ)
                ck(compact_row(r)==case['orbit_replay'][occ] and mr==mirrored_row(r),'source digests, all costs/events and exact reflected states')
                validate_row(r);validate_row(mr);rows.append(r);mrows.append(mr)
                if mode=='D':
                    ck(r['a']>=1 and a[0]==t and b[0]==skeleton[g] and a[0]!=b[0],'pure positive-cost reset separates roots')
                    if (g,t)==(2,13):ck(r['a']==1,'exact cheap-reset identity')
            boundary_records.append(dict(lap=lap,A=a,B=b))
            if lap in shared_B:ck(shared_B[lap]==b,'B source orbit independent of reset placement')
            else:shared_B[lap]=b
            state=json.dumps([a,b],separators=(',',':'))
            if state in seen:
                ck(lap==total_laps,'first repeated boundary, not a later selected loop')
                start=14*seen[state];end=len(rows);break
            seen[state]=lap
        ck(start is not None and case['cycle'] is not None,'all 121 reached exact recurrence, none capped')
        ck(boundary_records==case['boundaries'],'all stored exact boundary pairs')
        cyc=[dict(r,occurrence=i) for i,r in enumerate(rows[start:end])]
        mcyc=[dict(r,occurrence=i) for i,r in enumerate(mrows[start:end])]
        ck((cyc[-1]['destination_A'],cyc[-1]['destination_B'])==(cyc[0]['source_A'],cyc[0]['source_B']),'actual normal paired closure')
        ck((mcyc[-1]['destination_A'],mcyc[-1]['destination_B'])==(mcyc[0]['source_A'],mcyc[0]['source_B']),'actual reflected paired closure')
        unique={json.dumps([r['source_A'],r['source_B']],separators=(',',':')) for r in cyc}
        ck(len(unique)==len(cyc),'primitive source cycle; no internal pair repeat')
        bs=blocks(cyc);mbs=blocks(mcyc)
        E=sum(max(v['delta'],0) for v in bs);CD=sum(2*v['a'] for v in bs if not v['has_KEEP'])
        diag=[r['occurrence'] for r in cyc if r['source_A']==r['source_B']]
        meta=dict(transient_laps=start//14,period_laps=(end-start)//14,cycle_length=len(cyc),E=E,C_D=CD,
          A=sum(r['a'] for r in cyc),Q_B=sum(r['q'] for r in cyc),Z_B=sum(r['z'] for r in cyc),
          diagonal_source_occurrences=diag,reset_costs=[r['a'] for r in cyc if r['mode']=='D'],actual_pair_closure=True)
        ck(meta==case['cycle'],'source-derived recurrence, non-diagonality, costs and budget')
        ck(len(meta['reset_costs'])==meta['period_laps'] and CD==2*sum(meta['reset_costs']),'one pure DELETE pool per period')
        outcome='DIAGONAL_IN_CYCLE' if diag else ('DELETE_DOMINATED' if E<=CD else 'SURVIVOR')
        ck(E<=CD and outcome==case['outcome'] and case['comparison'] is None,'all cases independently fail the mandatory excess filter')
        # One concrete accepting old-UD cut is sufficient to disprove rejection at every cut.
        dmap=delete_only_map(cyc,bs);mdmap=delete_only_map(mcyc,mbs)
        ud=independent_pass(cyc,bs,dmap['cut'],False);mud=independent_pass(mcyc,mbs,mdmap['cut'],False)
        ck(ud['accepted'] and mud['accepted'] and dmap['cut']==mdmap['cut'],'old UD acceptance in each orientation')
        ck(ud['credit_assignments']==mud['credit_assignments'] and dmap['credit_assignments']==mdmap['credit_assignments'],
          'same distinct event-unit map under reflection, separate resource budgets')
        ck(len(ud['credit_assignments'])==len(dmap['credit_assignments'])==meta['Q_B'],'every B double funded once in either alternative proof')
        UD_units+=2*len(ud['credit_assignments']);DELETE_units+=2*len(dmap['credit_assignments'])
        maps.append(dict(case_index=ci,gap=g,target=t,E=E,C_D=CD,cycle_length=len(cyc),old_UD_accepted_cut=dmap['cut'],
          normal_UD_ledger=ud,normal_DELETE_only_map=dmap,reflected_maps_independently_checked=True,
          mirrored_assignments_equal_normal=True,alternative_budgets_not_combined=True))
        outcomes[outcome]=outcomes.get(outcome,0)+1
        key=(meta['transient_laps'],meta['period_laps']);period_counts[str(key)]=period_counts.get(str(key),0)+1
        key=(E,CD,not diag);funding_counts[str(key)]=funding_counts.get(str(key),0)+1
        if not diag:non_diag+=1;non_diag_positive+=E>0
        orbit_rows+=2*len(rows);cycle_rows+=2*len(cyc);max_laps=max(max_laps,total_laps)
    ck({str(k):v for k,v in shared_B.items()}==cert['shared_B_boundary_states'],'complete shared B recurrence')
    ck(outcomes==cert['outcome_counts']=={'DIAGONAL_IN_CYCLE':90,'DELETE_DOMINATED':31},'complete finite outcome classification')
    ck(cert['all_examined_orbits_closed'] and not cert['strict_new_closed_walk_coverage'] and cert['strict_witness'] is None and
      not cert['stopped_at_first_strict_witness'],'no strictness promotion or capped case hidden')
    ck(cert['finite_fits']==cert['size_sweeps']==cert['adaptive_generator_changes']==0 and
      not cert['old_UD_FI_rules_changed'] and not cert['actual_payer_q_used_as_reservation_oracle'] and
      cert['matching_terminal_line']=='FROZEN','fixed scope and frozen architecture')
    with (HERE/'old_UD_acceptance_certificates.json').open('x',encoding='utf-8') as f:json.dump(maps,f,indent=2,ensure_ascii=False);f.write('\n')
    result=dict(status='PASS',date='2026-10-31',fixed_key_size=13,fixed_reset_parameter_cases=121,source_orientations_per_case=2,
      complete_exact_orbit_classification=True,cap_limited_cases=0,max_laps_to_first_repeat=max_laps,
      primitive_period_laps_observed=[1,2],new_normal_and_reflected_orbit_rows=orbit_rows,
      normal_and_reflected_recurrent_cycle_rows=cycle_rows,setup_source_rows=4,pointer_source_accesses=calls,
      strict_BST_tree_occurrences_validated=valid_trees,non_diagonal_cycles=non_diag,
      non_diagonal_cycles_with_positive_excess=non_diag_positive,cycles_with_diagonal_state=90,
      cases_satisfying_E_greater_C_D=0,all_cases_old_UD_covered=True,explicit_old_UD_cut_certificates=242,
      old_UD_unit_assignment_checks=UD_units,DELETE_only_unit_assignment_checks=DELETE_units,
      new_survivor_all_cut_comparisons=0,new_FI_only_closed_walks=0,strict_new_closed_walk_coverage='NOT ESTABLISHED',
      no_credit_reuse=True,alternative_maps_and_orientations_have_separate_budgets=True,no_prefix_or_second_lap_credit=True,
      producer_imported=False,old_recognizers_executed=False,finite_fits=0,size_sweeps=0,adaptive_generator_changes=0,
      matching_terminal_line='FROZEN',universal_CD='OPEN',
      period_classification=period_counts,funding_classification=funding_counts,
      certificate_sha256=hashlib.sha256(cp.read_bytes()).hexdigest())
    with (HERE/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False);f.write('\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
