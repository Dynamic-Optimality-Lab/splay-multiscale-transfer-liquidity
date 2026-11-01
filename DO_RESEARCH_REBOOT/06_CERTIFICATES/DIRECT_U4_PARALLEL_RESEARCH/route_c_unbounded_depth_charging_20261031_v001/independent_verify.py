"""Pointer-source arbitrary-depth audit; no producer or old recognizer imports."""
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
    cp=HERE/'arbitrary_key_certificate.json';cert=json.loads(cp.read_text(encoding='utf-8'))
    old=json.loads((HERE.parent/'route_c_split_shallow_charging_20261031_v001/split_shallow_certificate.json').read_text(encoding='utf-8'))
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
    def fact(rows,bs,i,j):
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
    def independent_pass(rows,bs,cut,shallow_only=False):
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
            facts=[fact(rows,bs,i,j) for i in history if not shallow_only or b['key'] in shallow(rows,bs,i)]
            ceiling=min(f['ceiling'] for f in facts) if facts else None
            reserve=min(cap,ceiling) if facts else cap;ck(b['q']<=reserve,'own-work prefix is reserved once')
            for z,d in enumerate(demands[j]):claim(d,credits[j][z],'payer_local')
            left=cap-reserve;outgoing=reserve;loans=[]
            eligible=[i for i in history if cursor[i]<bs[i]['delta'] and (not shallow_only or b['key'] in shallow(rows,bs,i))]
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
    totals=dict(rows=0,prefix=0,trees=0,cuts=0,accepted=0,rejected=0,selected=0,alternatives=0,old_successes=0,old_alternatives=0)
    summary=[];zero_height=False;binding_deep=False;discarded_real_spare=False;changed_recipient_allocation=False
    literal=([['K',13],['K',11],['K',12],['K',2],['D',3],['D',2]]+[['K',k] for k in range(3,14)]+
      [['K',k] for k in range(1,14)]+[['K',k] for k in range(12,0,-1)]+[['D',13],['D',12]])
    for wi,w in enumerate(cert['witnesses']):
        strict=wi<2;n=w['n'];rows=w['full_replay'];initial=w['initial_diagonal']
        ck(initial==(vine(n) if wi%2==0 else mirror(vine(n),n)),'fixed exact diagonal source')
        trees=[initial,w['cycle_initial_A'],w['cycle_initial_B']]
        for r in w['prefix_replay']+rows:trees.extend(r[k] for k in ('source_A','source_B','destination_A','destination_B'))
        for t in trees:ck(inorder(t)==list(range(1,n+1)),'strict BST and complete fixed key set');totals['trees']+=1
        ck(w['strict_beyond_shallow']==strict and [r['occurrence'] for r in rows]==list(range(len(rows))),'single-period occurrence budget')
        ck([r['occurrence'] for r in w['prefix_replay']]==[-i-1 for i in range(len(w['prefix']))],'prefix provenance')
        a,b=replay(initial,initial,w['prefix'],w['prefix_replay']);ck((a,b)==(w['cycle_initial_A'],w['cycle_initial_B']),'diagonal reachability')
        aa,bb=replay(a,b,w['word'],rows);ck((aa,bb)==(a,b) and w['actual_pair_closure'],'actual paired closure')
        bs=blocks(rows);ck(bs==w['blocks'],'independent maximal A-root blocks')
        ck(len(w['cut_trials'])==len(w['old_SL_trials'])==len(bs),'all old/new cuts including failures')
        good=[];oldgood=[];chosen=None;alternatives=0;oldalt=0
        for cut in range(len(bs)):
            t=independent_pass(rows,bs,cut);sl=independent_pass(rows,bs,cut,True)
            ck(compact(t)==w['cut_trials'][cut] and compact(sl)==w['old_SL_trials'][cut],'all cut outcomes, transfers and unpaid tails')
            if t['accepted']:
                good.append(cut);alternatives+=len(t['credit_assignments']);totals['accepted']+=1
                if chosen is None:chosen=t
            else:totals['rejected']+=1
            if sl['accepted']:
                oldgood.append(cut);oldalt+=len(sl['credit_assignments']);ck(t['accepted'],'each previously successful shallow cut preserved')
            totals['cuts']+=1
        ck(good==w['accepted_cuts'] and oldgood==w['old_SL_accepted_cuts'] and chosen==w['selected_ledger'],'full selected ledger and membership lists')
        ck(chosen is not None and chosen['cut']==w['chosen_cut'] and alternatives==w['alternative_assignment_checks'] and
          oldalt==w['old_SL_alternative_assignment_checks'],'selected first success and separate alternative budgets')
        A,Q,Z=sum(r['a'] for r in rows),sum(r['q'] for r in rows),sum(r['z'] for r in rows)
        ck((A,Q,Z,2*A-Q)==(w['A'],w['Q_B'],w['Z_B'],w['weight']) and chosen['unused_credit_count']==2*A-Q,'source totals and unused unit conservation')
        ck(w['KEEP_support']==sorted({r['key'] for r in rows if r['mode']=='K'}),'genuine support')
        for pool in chosen['pools']:
            ck(len(pool['facts'])==len(pool['source_history']),'every historical positive fact kept, paid or unpaid, at every key')
            zero_height|=any(f['h']==0 for f in pool['facts'])
        if strict:
            expected_word=literal if wi==0 else [[m,14-x] for m,x in literal]
            expected_prefix=[['D',13],['D',12]] if wi==0 else [['D',1],['D',2]]
            ck(w['word']==expected_word and w['prefix']==expected_prefix and len(rows)==44,'pre-execution literal binding')
            ck([(r['a'],r['q'],r['delta']) for r in rows[:6]]==[(1,6,4),(3,3,-3),(1,1,-1),(1,1,-1),(3,0,-6),(1,0,-2)],'first six costs predetermined')
            ck([i for i,b in enumerate(bs) if b['delta']>0]==[0],'no unnoticed positive supplying old extra facts')
            ck(not oldgood and good==[0]+list(range(5,44)),'all-cut old rejection and four honest new failures')
            paying=[pool for pool in chosen['pools'] if pool['loans']]
            ck([(pool['payer_occurrence'],[(v['anchor_occurrence'],v['demand_start'],v['demand_end']) for v in pool['loans']]) for pool in paying]==
              [(1,[(0,0,3)]),(4,[(0,3,4)])],'one anchor split between distinct deep-key pools')
            deep=paying[0];f=deep['facts'][0]
            ck((f['pre_depth'],f['h'],f['k'],deep['own_q'],deep['capacity'],deep['reservation'])==(10,7,0,3,6,3),'deep KEEP has binding nonzero own-work reservation')
            ck(paying[0]['key'] not in shallow(rows,bs,0) and paying[1]['key'] not in shallow(rows,bs,0),'both actual lenders outside old root/child eligibility')
            ck(deep['loans'][0]['credit_start']==3 and deep['loans'][0]['credit_end']==6,'own prefix and deep loan suffix disjoint')
            p12=next(pool for pool in chosen['pools'] if pool['payer_occurrence']==2)
            p2=next(pool for pool in chosen['pools'] if pool['payer_occurrence']==3)
            ck((p12['ceiling'],p12['reservation'],p12['own_q'])==(4,2,1) and
              (p2['ceiling'],p2['reservation'],p2['own_q'])==(2,2,1),'conservative bounds discard actual spare; no exact-surplus oracle')
            binding_deep=True;discarded_real_spare=True
            ck(rows[16]['destination_A']==rows[16]['destination_B'],'synchronization by KEEP13')
            ck((A,Q,Z,2*A-Q)==(68,35,30,101),'exact new totals')
        else:
            prior=old['witnesses'][wi-2]
            ck(rows==prior['full_replay'] and w['prefix_replay']==prior['prefix_replay'] and w['word']==prior['word'] and w['prefix']==prior['prefix'],
              'all ten prior source words and prefixes unchanged')
            ck(w['old_SL_trials']==prior['cut_trials'] and oldgood==prior['accepted_cuts'] and
              oldalt==prior['alternative_assignment_checks'],'old per-cut transfer certificates unchanged')
            ck((A,Q,Z,2*A-Q)==(prior['A'],prior['Q_B'],prior['Z_B'],prior['weight']),'old totals unchanged')
            changed_recipient_allocation|=chosen['credit_assignments']!=prior['selected_ledger']['credit_assignments']
        totals['rows']+=len(rows);totals['prefix']+=len(w['prefix_replay']);totals['selected']+=len(chosen['credit_assignments'])
        totals['alternatives']+=alternatives;totals['old_successes']+=len(oldgood);totals['old_alternatives']+=oldalt
        summary.append(dict(name=w['name'],A=A,Q_B=Q,Z_B=Z,weight=2*A-Q,accepted_cuts=len(good),old_SL_accepted_cuts=len(oldgood)))
    for i in range(0,len(cert['witnesses']),2):
        w,r=cert['witnesses'][i:i+2];n=w['n']
        ck(r['initial_diagonal']==mirror(w['initial_diagonal'],n) and r['word']==[[m,n+1-x] for m,x in w['word']],'reflected literal')
        for a,b in zip(w['full_replay'],r['full_replay']):
            ck(all(b[k]==mirror(a[k],n) for k in ('source_A','source_B','destination_A','destination_B')),'both orientations at every physical endpoint')
    ck(len(cert['witnesses'])==12 and cert['finite_fits']==cert['size_sweeps']==cert['word_searches']==cert['source_graph_searches']==0 and
      not cert['allocation_optimizer_used'] and not cert['actual_payer_q_used_as_reservation_oracle'] and cert['matching_terminal_line']=='FROZEN','scope and freeze')
    ck(binding_deep and discarded_real_spare and zero_height and changed_recipient_allocation,'load-bearing deep/zero-height/conservative/changed-allocation coverage')
    result=dict(status='PASS',date='2026-10-31',complete_cycle_source_rows=totals['rows'],complete_diagonal_prefix_rows=totals['prefix'],
      pointer_source_accesses=calls,strict_BST_tree_occurrences_validated=totals['trees'],block_cut_trials_verified=totals['cuts'],
      accepted_trial_ledgers=totals['accepted'],rejected_trials_with_unpaid_debt=totals['rejected'],
      selected_ledger_credit_assignments=totals['selected'],alternative_ledger_assignment_checks=totals['alternatives'],
      old_SL_alternative_assignment_checks=totals['old_alternatives'],prior_successful_SL_cuts_preserved=totals['old_successes'],
      old_source_controls_preserved=10,no_credit_reuse=True,all_source_facts_retained_after_payment=True,
      one_reservation_and_retirement_per_pool=True,no_second_lap_or_prefix_credit=True,alternative_ledgers_are_not_combined=True,
      strict_extension_of_SL=True,deep_KEEP_with_nonzero_own_B_work_verified=True,zero_post_height_verified=True,
      total_debt_containment_does_not_assume_identical_recipient_allocations=True,source_reachability_and_pair_closure=True,
      producer_imported=False,old_recognizers_executed=False,actual_payer_q_used_as_reservation_oracle=False,
      allocation_optimizer_used=False,finite_fits=0,size_sweeps=0,restricted_class='PROVED—RESTRICTED DOMAIN',universal_CD='OPEN',
      matching_terminal_line='FROZEN',all_size_result='UD01 source/ledger theorem and UD02 analytic fringe/scan family; not finite extrapolation',
      witnesses=summary,certificate_sha256=hashlib.sha256(cp.read_bytes()).hexdigest())
    with (HERE/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False);f.write('\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
