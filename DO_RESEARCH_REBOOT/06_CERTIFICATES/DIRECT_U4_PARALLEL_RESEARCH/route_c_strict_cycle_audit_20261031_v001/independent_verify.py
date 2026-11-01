"""Independent pointer proof of synchronization and DELETE-budget unit certification."""
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
    cp=HERE/'fixed_generator_certificate.json';cert=json.loads(cp.read_text(encoding='utf-8'))
    old=json.loads((HERE.parent/'route_c_first_intervention_ceiling_20261031_v001/first_intervention_certificate.json').read_text(encoding='utf-8'))
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

    def ud_pass(rows,bs,cut):
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
            facts=[coarse_fact(rows,bs,i,j) for i in history]
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
    valid_trees=0;orbit_rows=0;setup_rows=0;orbit_summary=[]
    canonical=[['K',x] for x in [13,11,12,9,10,7,8,5,6,3,4,1,2]]
    ck(len(cert['witnesses'])==2,'one fixed word and reflection only')
    for wi,w in enumerate(cert['witnesses']):
        n=w['n'];ck(n==13 and w['lap_cap']==64,'fixed original size and predeclared cap')
        initial=vine(13) if wi==0 else mirror(vine(13),13)
        expected_word=canonical if wi==0 else [[m,14-x] for m,x in canonical]
        expected_setup=[['D',13],['D',12]] if wi==0 else [['D',1],['D',2]]
        ck(w['initial_diagonal']==initial and w['generator']==expected_word and w['setup_prefix']==expected_setup,'literal gated source construction')
        rows=w['orbit_replay'];ck(len(rows)==10 and w['requests_executed']==10,'stopped at tenth request, no new word tried')
        trees=[initial,w['orbit_initial_A'],w['orbit_initial_B']]
        for r in w['setup_replay']+rows:trees.extend(r[k] for k in ('source_A','source_B','destination_A','destination_B'))
        for t in trees:ck(inorder(t)==list(range(1,14)),'exact source BST and fixed keys');valid_trees+=1
        a,b=replay(initial,initial,w['setup_prefix'],w['setup_replay']);ck((a,b)==(w['orbit_initial_A'],w['orbit_initial_B']),'reachable non-diagonal seed')
        ck(a!=b,'seed not already synchronized')
        pairs=[(a,b)];sync=None
        for i,r in enumerate(rows):
            ck(r['occurrence']==i,'actual orbit request identity')
            a,b=replay(a,b,[w['generator'][i]],[r]);ck((a,b) not in pairs,'no transient repeated paired state')
            pairs.append((a,b))
            if a==b:
                ck(sync is None,'stops at first equality');sync=i
        ck(sync==9==w['sync_occurrence'] and a==b and (a,b)==(w['final_A'],w['final_B']),'first exact paired synchronization at K3/reflected K11')
        ck(w['stop_reason']=='diagonal_synchronization' and w['extracted_cycle'] is None and not w['strict_closed_walk_found'],'failure honestly recorded, synchronization not called closure')
        ck(w['completed_whole_laps']==0 and w['repeat_records']==[] and w['boundary_records']==[
          dict(completed_laps=0,request_count=0,A=w['orbit_initial_A'],B=w['orbit_initial_B'])],'no unexecuted boundary/lap budget claimed')
        orbit_rows+=len(rows);setup_rows+=len(w['setup_replay'])
        orbit_summary.append(dict(name=w['name'],sync_occurrence=9,sync_key=rows[-1]['key'],requests=10,
          transient_A=sum(r['a'] for r in rows),transient_Q_B=sum(r['q'] for r in rows),
          transient_positive_occurrences=[r['occurrence'] for r in rows if r['delta']>0],new_closed_candidate=False))
    normal,reflected=cert['witnesses']
    for a,b in zip(normal['orbit_replay'],reflected['orbit_replay']):
        ck(all(b[k]==mirror(a[k],13) for k in ('source_A','source_B','destination_A','destination_B')),'mirrored full source states')
    baseline_rows=baseline_prefix=cuts=successes=alternatives=selected=0;delete_maps=[]
    ck(len(cert['delete_budget_controls'])==len(old['witnesses'])==12,'fixed prior control corpus')
    for w,saved in zip(old['witnesses'],cert['delete_budget_controls']):
        n=w['n'];rows=w['full_replay'];initial=w['initial_diagonal']
        trees=[initial,w['cycle_initial_A'],w['cycle_initial_B']]
        for r in w['prefix_replay']+rows:trees.extend(r[k] for k in ('source_A','source_B','destination_A','destination_B'))
        for t in trees:ck(inorder(t)==list(range(1,n+1)),'baseline raw BST provenance');valid_trees+=1
        a,b=replay(initial,initial,w['prefix'],w['prefix_replay']);ck((a,b)==(w['cycle_initial_A'],w['cycle_initial_B']),'baseline reachability')
        aa,bb=replay(a,b,w['word'],rows);ck((aa,bb)==(a,b),'baseline actual paired closure')
        bs=blocks(rows);ck(bs==w['blocks'],'baseline exact source blocks')
        E=sum(max(b0['delta'],0) for b0 in bs);CD=sum(2*b0['a'] for b0 in bs if not b0['has_KEEP'])
        good=[];chosen=None
        for cut in range(len(bs)):
            t=ud_pass(rows,bs,cut);ck(compact(t)==w['old_UD_trials'][cut],'all old UD cut transfers/residuals unchanged')
            if t['accepted']:
                good.append(cut);alternatives+=len(t['credit_assignments'])
                if chosen is None:chosen=t
            cuts+=1
        ck(saved==dict(name=w['name'],E=E,C_D=CD,delete_dominated=E<=CD,old_UD_accepted_cuts=good,source_word_changed=False),'source-derived barrier values')
        ck(E<=CD and good,'all listed prior cycles belong to the deletion-budget sufficient class')
        dmap=delete_only_map(rows,bs);ck(dmap['cut'] in good,'explicit minimum cut is also old-UD accepted')
        ck(len(dmap['credit_assignments'])==w['Q_B'] and dmap['unused_credit_count']==w['weight'],'DELETE-only accounting and all own KEEP work')
        delete_maps.append(dict(name=w['name'],**dmap));successes+=len(good);selected+=len(chosen['credit_assignments'])
        baseline_rows+=len(rows);baseline_prefix+=len(w['prefix_replay'])
    ck(not cert['strict_new_closed_walk_coverage'] and cert['strictness_success_criterion_unchanged'],'strictness target not redefined after failure')
    ck(cert['finite_fits']==cert['size_sweeps']==cert['adaptive_word_searches']==0 and cert['fixed_generator_attempts']==1 and
      not cert['allocation_optimizer_used'] and cert['matching_terminal_line']=='FROZEN','scope and freeze')
    with (HERE/'delete_budget_certificates.json').open('x',encoding='utf-8') as f:json.dump(delete_maps,f,indent=2,ensure_ascii=False);f.write('\n')
    result=dict(status='PASS',date='2026-10-31',strict_new_closed_walk_coverage='NOT ESTABLISHED',
      fixed_generator='REFUTED—EXACT as a strictness witness: synchronization after ten KEEPs',
      new_orbit_source_rows=orbit_rows,new_setup_rows=setup_rows,baseline_cycle_source_rows=baseline_rows,
      baseline_prefix_rows=baseline_prefix,pointer_source_accesses=calls,strict_BST_tree_occurrences_validated=valid_trees,
      baseline_UD_cuts_verified=cuts,baseline_UD_successes=successes,baseline_UD_alternative_assignment_checks=alternatives,
      baseline_UD_selected_assignments=selected,DELETE_only_assignment_checks=sum(len(v['credit_assignments']) for v in delete_maps),
      DELETE_only_cut_direction='minimum cumulative sum; CW00A corrects original draft',
      new_closed_candidates_extracted=0,new_UD_FI_cycle_cut_trials=0,new_closed_cycle_assignments=0,
      no_credit_reuse=True,no_prefix_or_second_lap_credit=True,old_FI_cut_statuses_preserved_by_pins_not_reexecuted=True,
      original_source_words_preserved=12,fixed_generator_attempts=1,adaptive_word_searches=0,size_sweeps=0,finite_fits=0,
      producer_imported=False,old_recognizers_executed=False,matching_terminal_line='FROZEN',universal_CD='OPEN',
      source_generator_orbits=orbit_summary,certificate_sha256=hashlib.sha256(cp.read_bytes()).hexdigest())
    with (HERE/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False);f.write('\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
