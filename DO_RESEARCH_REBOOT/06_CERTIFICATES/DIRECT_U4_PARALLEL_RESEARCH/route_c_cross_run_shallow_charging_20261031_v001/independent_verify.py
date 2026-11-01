"""Independent pointer replay and cut-by-cut one-period batch/credit certification."""
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
    cp=HERE/'cross_run_shallow_certificate.json';cert=json.loads(cp.read_text(encoding='utf-8'))
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
        ck(isinstance(t,list) and len(t)==3 and type(t[0]) is int,'raw tree format')
        return inorder(t[1])+[t[0]]+inorder(t[2])
    def depth(t,x):
        d=0
        while t is not None:
            if t[0]==x:return d
            t=t[1] if x<t[0] else t[2];d+=1
        raise AssertionError('absent request')
    def evs(es):return [[e['case'],e['lo'],e['hi'],e['orient']] for e in es]
    calls=0
    def access(t,x):
        nonlocal calls
        d=depth(t,x);out,es=p.splay_trace(ptr(t),x)
        q=sum(e['case']!='ZIG' for e in es);z=sum(e['case']=='ZIG' for e in es)
        ck(q==d//2 and z==d%2 and len(es)==(d+1)//2,'source grouped units')
        calls+=1
        return raw(out),es,d,q,z
    def replay(a,b,word,rows):
        ck(len(word)==len(rows),'complete source word')
        for (mode,x),r in zip(word,rows):
            ck((a,b,mode,x)==(r['source_A'],r['source_B'],r['mode'],r['key']),'physical source-state sharing')
            aa,ae,da,_,_=access(a,x)
            if mode=='K':bb,be,db,q,z=access(b,x)
            else:bb,be,db,q,z=b,[],None,0,0
            ck((aa,bb)==(r['destination_A'],r['destination_B']),'source endpoints')
            ck((da,db,len(ae),q,z,evs(ae),evs(be),q-2*len(ae))==
               (r['d_A'],r['d_B'],r['a'],r['q'],r['z'],r['A_events'],r['B_events'],r['delta']),'all source event identities and costs')
            a,b=aa,bb
        return a,b
    def blocks(rows):
        n=len(rows);leaders=[i for i,r in enumerate(rows) if r['a']>0];bs=[]
        for u,i in enumerate(leaders):
            end=leaders[(u+1)%len(leaders)];ids=[i];j=(i+1)%n
            while j!=end:ids.append(j);j=(j+1)%n
            key=rows[i]['key'];a=rows[i]['a'];q=sum(rows[t]['q'] for t in ids)
            ck(all(rows[t]['a']==0 and rows[t]['key']==key for t in ids[1:]),'A-root block')
            kk=[t for t in ids if rows[t]['mode']=='K'];active=[t for t in kk if rows[t]['d_B']>0]
            ck(len(active)<=1,'one nontrivial B splay per block')
            bs.append(dict(leader=i,key=key,indices=ids,a=a,q=q,delta=q-2*a,has_KEEP=bool(kk),
              first_KEEP=kk[0] if kk else None,B_active_access=active[0] if active else None))
        return bs
    def runs(bs):
        if not any(b['delta']>0 for b in bs):return []
        if all(b['delta']>0 for b in bs):return None
        rr=[];m=len(bs)
        for i,b in enumerate(bs):
            if b['delta']<=0 or bs[(i-1)%m]['delta']>0:continue
            ids=[];j=i
            while bs[j]['delta']>0:ids.append(j);j=(j+1)%m
            rr.append(ids)
        return rr
    def collar(rows,bs,i):
        pre=rows[bs[i]['B_active_access']]['source_B']
        return {pre[0]}|{ch[0] for ch in pre[1:] if ch is not None}
    def bound(rows,bs,i,j,y,history=False):
        at=bs[i]['B_active_access'];pre,post=rows[at]['source_B'],rows[at]['destination_B']
        d,h=depth(pre,y),depth(post,y);ck(d<=1 and 1<=h<=3,'source shallow eligibility and post height')
        m=len(bs);off=(j-i)%m;ck(off>0,'one-period forward source bound')
        active=[bs[(i+z)%m]['B_active_access'] for z in range(1,off) if bs[(i+z)%m]['B_active_access'] is not None]
        k=len(active);c=h//2+k if bs[j]['has_KEEP'] else 0
        result=dict(anchor=i,anchor_occurrence=rows[bs[i]['leader']]['occurrence'],pre_depth=d,h=h,k=k,ceiling=c)
        if history:
            hh=[dict(after_access=rows[at]['occurrence'],depth=h)];previous=h
            for ai in active:
                ck(rows[ai]['mode']=='K' and rows[ai]['d_B']>0,'tax is genuine B activity, not positive q')
                dd=depth(rows[ai]['destination_B'],y);ck(dd<=previous+2,'source displacement')
                hh.append(dict(after_access=rows[ai]['occurrence'],depth=dd));previous=dd
            result.update(intervening_B_occurrences=[rows[a]['occurrence'] for a in active],depth_history=hh)
        return result
    def independent_pass(rows,bs,cut):
        m=len(bs);anchors=[];E=0;common=None;packets=[];tests=[]
        run_map={i:k for k,rr in enumerate(runs(bs) or []) for i in rr}
        order=[(cut+t)%m for t in range(m)]
        ck(len(order)==len(set(order))==m,'one pass, no second-lap block')
        for j in order:
            b=bs[j]
            if b['delta']>0:
                anchors.append(j);E+=b['delta'];cc=collar(rows,bs,j)
                common=cc if common is None else common&cc
                continue
            if not anchors:continue
            y=b['key'];bb=[bound(rows,bs,i,j,y) for i in anchors] if y in common else []
            c=min(r['ceiling'] for r in bb) if bb else None
            ok=bool(bb) and E+c<=2*b['a']
            tests.append(dict(block=j,key=y,pending_anchor_occurrences=[rows[bs[i]['leader']]['occurrence'] for i in anchors],
              pending_excess=E,common_keys=sorted(common),anchor_bounds=bb,ceiling=c,A_capacity=2*b['a'],admissible=ok))
            if not ok:continue
            ck(b['delta']<=0,'payer cannot be a pending positive')
            extent=(j-anchors[0])%m;ids=[(anchors[0]+t)%m for t in range(extent+1)]
            ck([z for z in ids if bs[z]['delta']>0]==anchors,'every encountered positive retained')
            interior=[z for z in ids if z not in anchors and z!=j]
            ck(all(bs[z]['delta']<=0 for z in interior),'interveners pay locally')
            bb=[bound(rows,bs,i,j,y,True) for i in anchors]
            if b['has_KEEP']:
                d=depth(rows[b['first_KEEP']]['source_B'],y)
                ck(b['q']==rows[b['first_KEEP']]['q'],'payer own B count once')
                for r in bb:ck(d<=r['h']+2*r['k'] and b['q']<=r['ceiling'],'all bounds concern the same actual payer')
            else:ck(b['q']==c==0,'KEEP-less payer')
            ck(c==min(r['ceiling'] for r in bb) and E+c<=2*b['a'] and b['delta']<=-E<0,'one shared pool threshold')
            packet=dict(anchors=list(anchors),anchor_occurrences=[rows[bs[i]['leader']]['occurrence'] for i in anchors],
              payer=j,payer_occurrence=rows[b['leader']]['occurrence'],key=y,common_keys=sorted(common),excess=E,
              anchor_bounds=bb,ceiling=c,threshold_lhs=E+c,threshold_rhs=2*b['a'],payer_q=b['q'],payer_a=b['a'],
              indices=ids,interior=interior,packet_delta=sum(bs[z]['delta'] for z in ids),
              distinct_positive_runs=len({run_map[z] for z in anchors}),closing_tests=tests)
            ck(packet['packet_delta']<=0,'packet total')
            packets.append(packet);anchors=[];E=0;common=None;tests=[]
        used=[z for packet in packets for z in packet['indices']]
        ck(len(used)==len(set(used)),'sequential batches do not overlap')
        accepted=not anchors
        if accepted:ck(all(b['delta']<=0 for i,b in enumerate(bs) if i not in used),'accepted pass covers all positives')
        else:ck(E==sum(bs[i]['delta'] for i in anchors)>0,'rejected pass retains unpaid positive debt')
        return dict(cut=cut,accepted=accepted,packets=packets,
          unpaid_anchor_occurrences=[rows[bs[i]['leader']]['occurrence'] for i in anchors],unpaid_excess=E)
    def construct_credit_map(rows,bs,packets):
        pool={i:[(rows[b['leader']]['occurrence'],z,s) for z in range(b['a']) for s in (0,1)] for i,b in enumerate(bs)}
        demand={i:[(rows[t]['occurrence'],z) for t in b['indices'] for z,e in enumerate(rows[t]['B_events']) if e[0]!='ZIG'] for i,b in enumerate(bs)}
        claims={};spent=set();handled=set();slices=[]
        def claim(ds,cs):
            ck(len(ds)==len(cs),'all proposed units fit')
            for d,c in zip(ds,cs):
                ck(d not in claims and c not in spent,'no duplicate demand or credit')
                claims[d]=c;spent.add(c)
        for p in packets:
            j=p['payer'];handled.add(j);cursor=0
            for i in p['anchors']:
                handled.add(i);local=2*bs[i]['a'];extra=bs[i]['delta']
                claim(demand[i][:local],pool[i]);selected=pool[j][cursor:cursor+extra]
                claim(demand[i][local:],selected)
                slices.append(dict(anchor_occurrence=rows[bs[i]['leader']]['occurrence'],payer_occurrence=rows[bs[j]['leader']]['occurrence'],
                  start=cursor,end=cursor+extra,credits=[list(c) for c in selected]));cursor+=extra
            ck(cursor==p['excess'] and cursor+bs[j]['q']<=len(pool[j]),'total payer capacity counted once')
            claim(demand[j],pool[j][cursor:cursor+len(demand[j])])
        for i,b in enumerate(bs):
            if i in handled:continue
            ck(b['delta']<=0,'only nonpositive blocks left local')
            claim(demand[i],pool[i][:len(demand[i])])
        all_d={d for dd in demand.values() for d in dd};all_c={c for cc in pool.values() for c in cc}
        ck(set(claims)==all_d and set(claims.values())<=all_c,'complete actual one-period resource map')
        return claims,slices,len(all_c)-len(spent)
    def old_SP(rows,bs):
        rr=runs(bs)
        if rr is None:return False
        m=len(bs)
        for run in rr:
            cc=set.intersection(*(collar(rows,bs,i) for i in run));E=sum(bs[i]['delta'] for i in run);found=False
            for off in range(1,m):
                j=(run[-1]+off)%m;b=bs[j]
                if b['delta']>0:break
                if b['key'] in cc:
                    c=min(bound(rows,bs,i,j,b['key'])['ceiling'] for i in run)
                    if E+c<=2*b['a']:found=True;break
            if not found:return False
        return True
    old=json.loads((HERE.parent/'route_c_shared_shallow_charging_20261031_v001/shared_shallow_certificate.json').read_text(encoding='utf-8'))
    total_rows=prefix_rows=trial_count=accepted_count=rejected_count=selected_units=alternative_checks=valid_trees=0;summary=[]
    for wi,w in enumerate(cert['witnesses']):
        cross=wi<2;rows=w['full_replay'];n=w['n'];initial=w['initial_diagonal']
        expected_initial=vine(n) if wi%2==0 else mirror(vine(n),n)
        ck(initial==expected_initial,'exact diagonal vine')
        trees=[initial,w['cycle_initial_A'],w['cycle_initial_B']]
        for r in w['prefix_replay']+rows:trees.extend(r[k] for k in ('source_A','source_B','destination_A','destination_B'))
        for tree in trees:ck(inorder(tree)==list(range(1,n+1)),'strict BST order and exact key set');valid_trees+=1
        ck(w['strict_cross_run']==cross and len(rows)==(42 if cross else len(old['witnesses'][wi-2]['word'])),'predeclared corpus')
        a,b=replay(initial,initial,w['prefix'],w['prefix_replay']);ck((a,b)==(w['cycle_initial_A'],w['cycle_initial_B']),'diagonal reachability')
        aa,bb=replay(a,b,w['word'],rows);ck((aa,bb)==(a,b) and w['actual_pair_closure'],'actual paired closure')
        ck([r['occurrence'] for r in rows]==list(range(len(rows))),'single cycle occurrence budget')
        bs=blocks(rows);ck(bs==w['blocks'] and runs(bs)==w['positive_runs'],'source blocks and distinct runs')
        ck(len(w['cut_trials'])==len(bs),'every block-cut trial, not only successful ones')
        successes=[];chosen=None;alt=0
        for cut,saved in enumerate(w['cut_trials']):
            result=independent_pass(rows,bs,cut)
            compact=dict(cut=cut,accepted=result['accepted'],packet_occurrences=[[p['anchor_occurrences'],p['payer_occurrence']] for p in result['packets']],
              unpaid_anchor_occurrences=result['unpaid_anchor_occurrences'],unpaid_excess=result['unpaid_excess'])
            ck(saved==compact,'complete cut trial and honest rejection accounting')
            if result['accepted']:
                claims,_,_=construct_credit_map(rows,bs,result['packets']);alt+=len(claims);accepted_count+=1;successes.append(cut)
                if chosen is None:chosen=result
            else:rejected_count+=1
            trial_count+=1
        ck(successes==w['accepted_cuts'] and chosen is not None and chosen['cut']==w['chosen_cut'],'first successful one-period pass')
        ck(chosen['packets']==w['packets'] and alt==w['alternative_assignment_checks'],'selected full source certificate and independent alternative checks')
        claims,slices,unused=construct_credit_map(rows,bs,chosen['packets'])
        stored={tuple(r['demand']):tuple(r['credit']) for r in w['credit_assignments']}
        ck(len(stored)==len(w['credit_assignments']) and stored==claims and slices==w['payer_slices'],'all actual shared slices and units')
        A,Q,Z=sum(r['a'] for r in rows),sum(r['q'] for r in rows),sum(r['z'] for r in rows)
        expected=(62,35,28,89) if cross else (old['witnesses'][wi-2]['A'],old['witnesses'][wi-2]['Q_B'],old['witnesses'][wi-2]['Z_B'],old['witnesses'][wi-2]['weight'])
        ck((A,Q,Z,2*A-Q)==expected==(w['A'],w['Q_B'],w['Z_B'],w['weight']),'source totals')
        ck(unused==w['unused_credit_count']==2*A-Q,'unused budget identity')
        sp=old_SP(rows,bs);ck(sp==w['satisfies_old_SP']==(not cross),'strict extension and old SP preservation')
        if cross:
            ck(runs(bs)==[[0],[2]] and [(r['a'],r['q'],r['delta']) for r in rows[:5]]==[(2,6,2),(2,0,-4),(1,3,1),(1,2,0),(2,0,-4)],'distinct positive runs separated by DELETE')
            packet=chosen['packets'][0]
            ck(packet['anchors']==[0,2] and packet['payer']==4 and packet['distinct_positive_runs']==2,'one payer across both runs')
            ck((packet['excess'],packet['ceiling'],packet['threshold_lhs'],packet['threshold_rhs'],packet['packet_delta'])==(3,1,4,4,-5),'source minimum and one pool')
            ck([(b['h'],b['k'],b['ceiling']) for b in packet['anchor_bounds']]==[(1,2,2),(1,1,1)],'DELETE bridge adds no B tax')
            ck([(s['start'],s['end']) for s in slices]==[(0,2),(2,3)],'disjoint cross-run slices')
            ck(not any(c[0]==1 for c in claims.values()),'no DELETE bridge credits lent')
            ck(sum(c[0]==3 for c in claims.values())==2 and all(d[0]==3 for d,c in claims.items() if c[0]==3),'saturated KEEP bridge lends nothing')
            ck(len(successes)==38 and len(bs)-len(successes)==4,'four rejected cuts remain unpaid, not falsely promoted')
            ck(rows[12]['destination_A']==rows[12]['destination_B'],'synchronization by KEEP10')
            prior=old['witnesses'][wi]
            ck((rows[3]['destination_A'],rows[3]['destination_B'])==(prior['full_replay'][2]['destination_A'],prior['full_replay'][2]['destination_B']),'exact rejoin with old SP pair')
            for r,o in zip(rows[4:],prior['full_replay'][3:]):
                ck({k:v for k,v in r.items() if k!='occurrence'}=={k:v for k,v in o.items() if k!='occurrence'},'old closing suffix unchanged')
            ck(w['KEEP_support']==list(range(1,14)),'genuine unbounded-family core support')
        else:
            prior=old['witnesses'][wi-2]
            ck(w['prefix']==prior['prefix'] and w['word']==prior['word'] and rows==prior['full_replay'],'all six old source words unchanged')
        total_rows+=len(rows);prefix_rows+=len(w['prefix_replay']);selected_units+=len(claims);alternative_checks+=alt
        summary.append(dict(name=w['name'],A=A,Q_B=Q,Z_B=Z,weight=2*A-Q,old_SP=sp,accepted_cuts=len(successes),rejected_cuts=len(bs)-len(successes)))
    for i in (0,2,4,6):
        w,r=cert['witnesses'][i:i+2];n=w['n']
        ck(r['initial_diagonal']==mirror(w['initial_diagonal'],n) and r['word']==[[m,n+1-x] for m,x in w['word']],'reflected word')
        for a,b in zip(w['full_replay'],r['full_replay']):
            ck(all(b[k]==mirror(a[k],n) for k in ('source_A','source_B','destination_A','destination_B')),'reflected full states')
    literal=([['K',13],['D',11],['K',12],['K',11],['K',2]]+[['K',k] for k in range(3,14)]+
      [['K',k] for k in range(1,14)]+[['K',k] for k in range(12,0,-1)]+[['D',9]])
    ck(cert['witnesses'][0]['word']==literal and cert['witnesses'][0]['prefix']==[['D',9]],'literal gate binding')
    ck(len(cert['witnesses'])==8 and cert['finite_fits']==cert['size_sweeps']==cert['word_searches']==cert['source_graph_searches']==0 and
       not cert['allocation_optimizer_used'] and cert['matching_terminal_line']=='FROZEN','scope and freeze')
    result=dict(status='PASS',date='2026-10-31',complete_cycle_source_rows=total_rows,complete_diagonal_prefix_rows=prefix_rows,
      pointer_source_accesses=calls,strict_BST_tree_occurrences_validated=valid_trees,block_cut_trials_verified=trial_count,
      accepted_trial_covers=accepted_count,rejected_trials_with_unpaid_debt=rejected_count,
      selected_cover_credit_assignments=selected_units,alternative_cover_assignment_checks=alternative_checks,
      alternative_covers_are_not_combined=True,no_credit_reuse=True,no_second_lap_or_prefix_credit=True,
      every_pending_positive_retained=True,first_qualifying_closure_verified=True,
      strict_extension_of_SP=True,old_SP_DS_SC_controls_preserved=6,new_distinct_positive_runs=2,
      source_reachability_and_pair_closure=True,witnesses=summary,producer_imported=False,
      allocation_optimizer_used=False,old_recognizers_executed=False,
      all_size_result='analytic theorem XR01 and family XR02; no finite extrapolation',
      restricted_class='PROVED—RESTRICTED DOMAIN',universal_CD='OPEN',matching_terminal_line='FROZEN',
      finite_fits=0,size_sweeps=0,certificate_sha256=hashlib.sha256(cp.read_bytes()).hexdigest())
    with (HERE/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False);f.write('\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
