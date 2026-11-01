"""Pointer-source verification of common bounds, pool slices and all cyclic seams."""
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
    cp=HERE/'shared_shallow_certificate.json';cert=json.loads(cp.read_text(encoding='utf-8'))
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
        d=depth(t,x);tt,es=p.splay_trace(ptr(t),x)
        q=sum(e['case']!='ZIG' for e in es);z=sum(e['case']=='ZIG' for e in es)
        ck(q==d//2 and z==d%2 and len(es)==(d+1)//2,'source event units')
        calls+=1
        return raw(tt),es,d,q,z
    def replay(a,b,word,rows):
        ck(len(word)==len(rows),'complete source trace')
        for (mode,x),r in zip(word,rows):
            ck((a,b,mode,x)==(r['source_A'],r['source_B'],r['mode'],r['key']),'physical source sharing')
            aa,ae,da,_,_=access(a,x)
            if mode=='K':bb,be,db,q,z=access(b,x)
            else:bb,be,db,q,z=b,[],None,0,0
            ck((aa,bb)==(r['destination_A'],r['destination_B']),'full source endpoints')
            ck((da,db,len(ae),q,z,evs(ae),evs(be),q-2*len(ae))==
               (r['d_A'],r['d_B'],r['a'],r['q'],r['z'],r['A_events'],r['B_events'],r['delta']),
               'actual grouped costs and patterns')
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
            ck(len(active)<=1,'at most one nontrivial B splay per block')
            bs.append(dict(leader=i,key=key,indices=ids,a=a,q=q,delta=q-2*a,has_KEEP=bool(kk),
              first_KEEP=kk[0] if kk else None,B_active_access=active[0] if active else None))
        return bs
    def positive_runs(bs):
        if not any(b['delta']>0 for b in bs):return []
        ck(not all(b['delta']>0 for b in bs),'all-positive cycle cannot have a distinct payer')
        m=len(bs);rr=[]
        for i,b in enumerate(bs):
            if b['delta']<=0 or bs[(i-1)%m]['delta']>0:continue
            ids=[];j=i
            while bs[j]['delta']>0:ids.append(j);j=(j+1)%m
            rr.append(ids)
        ck(len({i for r in rr for i in r})==sum(b['delta']>0 for b in bs),'every positive appears in one maximal run')
        return rr
    def anchor_bound(rows,bs,i,j,y,with_history=False):
        at=bs[i]['B_active_access'];ck(at is not None,'positive anchor has B work')
        pre,post=rows[at]['source_B'],rows[at]['destination_B'];d=depth(pre,y);h=depth(post,y)
        ck(d<=1 and 1<=h<=3,'common pre-shallow key and source post height')
        m=len(bs);off=(j-i)%m;ck(0<off<m,'distinct payer in one period')
        between=[(i+z)%m for z in range(1,off)]
        active=[bs[t]['B_active_access'] for t in between if bs[t]['B_active_access'] is not None]
        k=len(active);c=h//2+k if bs[j]['has_KEEP'] else 0
        r=dict(anchor=i,anchor_occurrence=rows[bs[i]['leader']]['occurrence'],pre_depth=d,h=h,k=k,ceiling=c)
        if with_history:
            history=[dict(after_access=rows[at]['occurrence'],depth=h)];previous=h
            for ai in active:
                row=rows[ai];ck(row['mode']=='K' and row['d_B']>0,'tax counts a genuine B-changing KEEP')
                dd=depth(row['destination_B'],y);ck(dd<=previous+2,'one-splay displacement')
                history.append(dict(after_access=row['occurrence'],depth=dd));previous=dd
            r.update(intervening_B_occurrences=[rows[a]['occurrence'] for a in active],depth_history=history)
        return r
    def verify_packet(rows,bs,run,j):
        m=len(bs);E=sum(bs[i]['delta'] for i in run);common=None
        for i in run:
            pre=rows[bs[i]['B_active_access']]['source_B']
            collar={pre[0]}|{ch[0] for ch in pre[1:] if ch is not None}
            common=collar if common is None else common&collar
        common=sorted(common);off=(j-run[-1])%m;ck(0<off<m,'forward shared payer')
        scanned=[]
        for z in range(1,off+1):
            at=(run[-1]+z)%m;b=bs[at];y=b['key']
            ck(b['delta']<=0,'no intervening positive run')
            bb=[anchor_bound(rows,bs,i,at,y) for i in run] if y in common else []
            c=min(r['ceiling'] for r in bb) if bb else None
            ok=bool(bb) and E+c<=2*b['a']
            ck(ok==(z==off),'first admissible shared payer, not an arbitrary later choice')
            scanned.append(dict(payer=at,offset_after_run=z,key=y,common_key=y in common,
              anchor_bounds=bb,ceiling=c,run_excess=E,A_capacity=2*b['a'],admissible=ok))
        b=bs[j];y=b['key'];bounds=[anchor_bound(rows,bs,i,j,y,True) for i in run]
        c=min(r['ceiling'] for r in bounds)
        if b['has_KEEP']:
            first=b['first_KEEP'];dd=depth(rows[first]['source_B'],y)
            ck(b['q']==rows[first]['q'],'payer demand is counted once')
            for r in bounds:ck(dd<=r['h']+2*r['k'] and b['q']<=r['ceiling'],'each source bound limits the same payer work')
        else:ck(b['q']==c==0,'KEEP-less payer')
        ck(b['q']<=c and E+c<=2*b['a'] and b['delta']<=-E<0,'common minimum and one-pool threshold')
        extent=(j-run[0])%m;ids=[(run[0]+z)%m for z in range(extent+1)]
        interior=[(run[-1]+z)%m for z in range(1,off)]
        ck(len(ids)==len(set(ids)) and all(bs[t]['delta']<=0 for t in interior),'one period and locally paid intermediates')
        packet_delta=sum(bs[t]['delta'] for t in ids);ck(packet_delta<=0,'packet total')
        return dict(run=run,anchor_occurrences=[rows[bs[i]['leader']]['occurrence'] for i in run],
          payer=j,payer_occurrence=rows[b['leader']]['occurrence'],key=y,common_keys=common,run_excess=E,
          anchor_bounds=bounds,ceiling=c,threshold_lhs=E+c,threshold_rhs=2*b['a'],payer_q=b['q'],payer_a=b['a'],
          indices=ids,interior=interior,packet_delta=packet_delta,scanned_candidates=scanned)
    def verify_packets(rows,bs,physical):
        rr=positive_runs(bs);leader_map={rows[b['leader']]['occurrence']:i for i,b in enumerate(bs)}
        packets=[];covered=[]
        for anchors,payer in physical:
            run=[leader_map[v] for v in anchors];j=leader_map[payer]
            ck(run in rr,'packet anchors are exactly a maximal positive run')
            packets.append(verify_packet(rows,bs,run,j));covered.append(tuple(run))
        ck(len(covered)==len(set(covered))==len(rr) and set(covered)=={tuple(r) for r in rr},'all runs covered once')
        used=[i for packet in packets for i in packet['indices']]
        ck(len(used)==len(set(used)),'no shared pool or intermediate block across packets')
        ck(all(b['delta']<=0 for i,b in enumerate(bs) if i not in used),'unassigned blocks pay locally')
        return packets
    def verify_credits(rows,bs,packets,allocation,slices=None):
        by_occ={r['occurrence']:r for r in rows};belongs={rows[t]['occurrence']:i for i,b in enumerate(bs) for t in b['indices']}
        expected_d={(o,z) for o,r in by_occ.items() for z,e in enumerate(r['B_events']) if e[0]!='ZIG'}
        expected_c={(o,z,slot) for o,r in by_occ.items() for z in range(len(r['A_events'])) for slot in (0,1)}
        allowed={(i,p['payer']) for p in packets for i in p['run']};ds=[];cs=[]
        for r in allocation:
            d,cr=tuple(r['demand']),tuple(r['credit']);ck(d in expected_d and cr in expected_c,'actual cycle event identity; no prefix credit')
            bd,bc=belongs[d[0]],belongs[cr[0]]
            ck(bd==bc or (bd,bc) in allowed,'only the shared payer lends to its own run')
            ds.append(d);cs.append(cr)
        ck(set(ds)==expected_d and len(set(ds))==len(ds),'every B double paid exactly once')
        ck(len(set(cs))==len(cs),'no actual credit reused')
        expected_slices=[]
        for packet in packets:
            j=packet['payer'];po=rows[bs[j]['leader']]['occurrence']
            pool=[[po,z,slot] for z in range(bs[j]['a']) for slot in (0,1)];cursor=0
            for i in packet['run']:
                ao=rows[bs[i]['leader']]['occurrence'];excess=bs[i]['delta'];selected=pool[cursor:cursor+excess]
                expected_slices.append(dict(anchor_occurrence=ao,payer_occurrence=po,start=cursor,end=cursor+excess,credits=selected))
                got=[r for r in allocation if belongs[r['demand'][0]]==i and belongs[r['credit'][0]]==j]
                ck([r['credit'] for r in got]==selected and len(got)==excess,'distinct contiguous slice for each anchor')
                cursor+=excess
            ck(cursor==packet['run_excess'] and cursor+bs[j]['q']<=len(pool),'payer own work plus total excess fits once')
            own=[r for r in allocation if belongs[r['demand'][0]]==j]
            ck([r['credit'] for r in own]==pool[cursor:cursor+bs[j]['q']],'payer own work follows all shared slices')
        if slices is not None:ck(expected_slices==slices,'exact stored reservation slices')
        return len(expected_c)-len(cs)
    def private_DS(rows,bs):
        m=len(bs)
        for i,b in enumerate(bs):
            if b['delta']<=0:continue
            pre=rows[b['B_active_access']]['source_B'];collar={pre[0]}|{ch[0] for ch in pre[1:] if ch is not None};found=False
            for off in range(1,m):
                j=(i+off)%m;other=bs[j]
                if other['delta']>0:break
                if other['key'] in collar and b['delta']+anchor_bound(rows,bs,i,j,other['key'])['ceiling']<=2*other['a']:
                    found=True;break
            if not found:return False
        return True
    old=json.loads((HERE.parent/'route_c_delayed_shallow_charging_20261031_v001/delayed_shallow_certificate.json').read_text(encoding='utf-8'))
    total_rows=total_prefix=total_cuts=total_assignments=0;summary=[]
    for wi,w in enumerate(cert['witnesses']):
        shared=wi<2;rows=w['full_replay'];initial=w['initial_diagonal']
        ck(w['strict_shared']==shared and len(rows)==(41 if shared else (23 if wi<4 else 22)),'fixed corpus only')
        a,b=replay(initial,initial,w['prefix'],w['prefix_replay'])
        ck((a,b)==(w['cycle_initial_A'],w['cycle_initial_B']),'diagonal reachability prefix')
        aa,bb=replay(a,b,w['word'],rows);ck((aa,bb)==(a,b) and w['actual_pair_closure'],'actual paired closure')
        ck([r['occurrence'] for r in rows]==list(range(len(rows))),'one physical budget per period')
        bs=blocks(rows);rr=positive_runs(bs);ck(bs==w['blocks'] and rr==w['positive_runs'],'source blocks and maximal runs')
        physical=[(tuple(p['anchor_occurrences']),p['payer_occurrence']) for p in w['packets']]
        packets=verify_packets(rows,bs,physical);ck(packets==w['packets'],'all shared-source profiles and first-payer metadata')
        unused=verify_credits(rows,bs,packets,w['credit_assignments'],w['payer_slices'])
        A,Q,Z=sum(r['a'] for r in rows),sum(r['q'] for r in rows),sum(r['z'] for r in rows)
        expected=(60,35,28,85) if shared else ((30,12,16,48) if wi<4 else (31,11,16,51))
        ck((A,Q,Z,2*A-Q)==expected==(w['A'],w['Q_B'],w['Z_B'],w['weight']),'source totals')
        ck(unused==w['unused_credit_count']==2*A-Q,'complete exact resource identity')
        ds=private_DS(rows,bs);ck(ds==w['satisfies_old_DS']==(not shared),'strict shared coverage and private preservation')
        ck(len(w['all_cuts'])==len(rows),'all cuts represented')
        for cut,r in enumerate(w['all_cuts']):
            rotated=rows[cut:]+rows[:cut];bc=blocks(rotated);pp=verify_packets(rotated,bc,physical)
            ck(verify_credits(rotated,bc,pp,w['credit_assignments'])==unused,'same physical units work across every seam')
            ids=sorted((tuple(p['anchor_occurrences']),p['payer_occurrence']) for p in pp)
            ck(r==dict(cut=cut,accepted=True,packet_occurrences=[[list(z),j] for z,j in ids],charged_demands=Q),'cut-invariant shared payer')
            total_cuts+=1
        if shared:
            ck(rr==[[0,1]] and [(r['a'],r['q'],r['delta']) for r in rows[:4]]==[(2,6,2),(1,3,1),(1,2,0),(2,0,-4)],'two real anchors, saturated intervener and sole payer')
            packet=packets[0]
            ck(packet['payer']==3 and packet['run_excess']==3 and packet['ceiling']==1 and packet['threshold_lhs']==packet['threshold_rhs']==4,'one shared threshold')
            ck([(v['h'],v['k'],v['ceiling']) for v in packet['anchor_bounds']]==[(1,2,2),(1,1,1)],'same payer is bounded by minimum, not sum')
            ck([(v['start'],v['end']) for v in w['payer_slices']]==[(0,2),(2,3)],'two disjoint shared slices')
            intervener_credits=[v for v in w['credit_assignments'] if v['credit'][0]==2]
            ck(len(intervener_credits)==2 and all(v['demand'][0]==2 for v in intervener_credits),'intervener has no lent or duplicated capacity')
            ck(packet['packet_delta']==-1 and rows[11]['destination_A']==rows[11]['destination_B'],'paid packet and synchronization by KEEP10')
            ck(w['KEEP_support']==list(range(1,14)),'thirteen genuine KEEP targets')
            for i in (0,1):
                root=rows[i]['source_B'][0]
                ck(bs[(i+1)%len(bs)]['key']!=root,'old AJ immediate former-root predicate fails')
                if i==0:ck(bs[1]['delta']>0,'old AL/AM intermediate nonpositive predicate fails')
                else:ck(all(bs[i+j]['key']!=root for j in (1,2,3)),'old delayed former-root predicates fail')
            ck(bs[0]['delta']==2,'old unit-positive packet classes cannot cover first anchor')
        else:
            prior=old['witnesses'][wi-2]
            ck(w['prefix']==prior['prefix'] and w['word']==prior['word'] and rows==prior['full_replay'],'all inherited source rows unchanged')
        total_rows+=len(rows);total_prefix+=len(w['prefix_replay']);total_assignments+=len(w['credit_assignments'])
        summary.append(dict(name=w['name'],A=A,Q_B=Q,Z_B=Z,weight=2*A-Q,old_DS=ds))
    for i in (0,2,4):
        w,r=cert['witnesses'][i:i+2];n=w['n']
        ck(r['initial_diagonal']==mirror(w['initial_diagonal'],n) and r['word']==[[m,n+1-x] for m,x in w['word']],'reflected word')
        for a,b in zip(w['full_replay'],r['full_replay']):
            ck(all(b[k]==mirror(a[k],n) for k in ('source_A','source_B','destination_A','destination_B')),'reflected full states')
    ck(len(cert['witnesses'])==6 and cert['finite_fits']==cert['size_sweeps']==cert['source_graph_searches']==cert['word_searches']==0 and
       not cert['allocation_optimizer_used'] and cert['source_witness_n13_analytically_predetermined'] and cert['matching_terminal_line']=='FROZEN','scope and freeze')
    result=dict(status='PASS',date='2026-10-31',complete_cycle_source_rows=total_rows,
      complete_diagonal_prefix_rows=total_prefix,pointer_source_accesses=calls,
      cyclic_cuts_verified=total_cuts,exact_credit_assignments=total_assignments,
      no_credit_reuse=True,shared_pool_counted_once=True,distinct_anchor_slices_verified=True,
      intermediate_capacity_not_borrowed=True,canonical_first_payers_verified=True,
      source_reachability_and_pair_closure=True,strict_extension_of_DS=True,
      old_private_witnesses_preserved=4,new_run_deficits=[2,1],new_shared_ceiling=1,
      new_pool_capacity=4,new_anchor_slices=[[0,2],[2,3]],witnesses=summary,
      producer_imported=False,allocation_optimizer_used=False,old_recognizers_executed=False,
      all_size_result='analytic theorem SP01 and family SP02; not finite extrapolation',
      restricted_class='PROVED—RESTRICTED DOMAIN',universal_CD='OPEN',
      matching_terminal_line='FROZEN',finite_fits=0,size_sweeps=0,
      certificate_sha256=hashlib.sha256(cp.read_bytes()).hexdigest())
    with (HERE/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False);f.write('\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
