"""Independent pointer replay, earliest-payer and actual-unit certificate verification."""
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
    cp=HERE/'delayed_shallow_certificate.json';cert=json.loads(cp.read_text(encoding='utf-8'))
    spec=importlib.util.spec_from_file_location('pointer_source',ROOT/'python/liquidity/legacy_embedding.py')
    p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
    def ptr(t):
        if t is None:return None
        r=p.mknode(t[0],ptr(t[1]),ptr(t[2]))
        for side in ('l','r'):
            if r[side] is not None:r[side]['p']=r
        return r
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
        ck(q==d//2 and z==d%2 and len(es)==(d+1)//2,'exact source event units')
        calls+=1
        return raw(tt),es,d,q,z
    def replay(a,b,word,rows):
        ck(len(word)==len(rows),'full source trace')
        for (mode,x),r in zip(word,rows):
            ck((a,b,mode,x)==(r['source_A'],r['source_B'],r['mode'],r['key']),'physical source sharing')
            aa,ae,da,_,_=access(a,x)
            if mode=='K':bb,be,db,q,z=access(b,x)
            else:bb,be,db,q,z=b,[],None,0,0
            ck((aa,bb)==(r['destination_A'],r['destination_B']),'physical endpoints')
            ck((da,db,len(ae),q,z,evs(ae),evs(be),q-2*len(ae))==
               (r['d_A'],r['d_B'],r['a'],r['q'],r['z'],r['A_events'],r['B_events'],r['delta']),
               'every actual event and signed count')
            a,b=aa,bb
        return a,b
    def blocks(rows):
        n=len(rows);leaders=[i for i,r in enumerate(rows) if r['a']>0];bs=[]
        for u,i in enumerate(leaders):
            end=leaders[(u+1)%len(leaders)];ids=[i];j=(i+1)%n
            while j!=end:ids.append(j);j=(j+1)%n
            x=rows[i]['key'];a=rows[i]['a'];q=sum(rows[j]['q'] for j in ids)
            ck(all(rows[j]['a']==0 and rows[j]['key']==x for j in ids[1:]),'maximal A-root block')
            kk=[j for j in ids if rows[j]['mode']=='K'];active=[j for j in kk if rows[j]['d_B']>0]
            ck(len(active)<=1,'unique B activity per block')
            bs.append(dict(leader=i,key=x,indices=ids,a=a,q=q,delta=q-2*a,has_KEEP=bool(kk),
                           first_KEEP=kk[0] if kk else None,B_active_access=active[0] if active else None))
        return bs
    def verify_pair(rows,bs,i,j):
        m=len(bs);offset=(j-i)%m;anchor,payer=bs[i],bs[j]
        ck(0<offset<m and anchor['delta']>0,'distinct forward payer and positive anchor')
        interior=[(i+z)%m for z in range(1,offset)]
        ck(all(bs[t]['delta']<=0 for t in interior),'no intervening positive')
        at=anchor['B_active_access'];ck(at is not None,'anchor has genuine B work')
        pre,post=rows[at]['source_B'],rows[at]['destination_B'];scanned=[];k=0
        for off in range(1,offset+1):
            v=(i+off)%m;b=bs[v];y=b['key'];d=depth(pre,y)
            ck(b['delta']<=0,'canonical scan cannot cross a positive')
            h=depth(post,y) if d<=1 else None
            if h is not None:ck(1<=h<=3,'old root or child transport bound')
            c=(h//2+k if b['has_KEEP'] else 0) if h is not None else None
            ok=h is not None and anchor['delta']+c<=2*b['a']
            scanned.append(dict(block=v,offset=off,key=y,pre_anchor_depth=d,h=h,k=k,ceiling=c,
                                A_capacity=2*b['a'],admissible=ok))
            ck(ok==(off==offset),'chosen payer is first admissible one')
            if off<offset:k+=int(b['B_active_access'] is not None)
        y=payer['key'];h=depth(post,y);c=h//2+k if payer['has_KEEP'] else 0
        intervening=[bs[t]['B_active_access'] for t in interior if bs[t]['B_active_access'] is not None]
        ck(k==len(intervening),'tax counts every genuine B change, not q')
        history=[dict(after_access=rows[at]['occurrence'],depth=h)];prev=h
        for access_index in intervening:
            r=rows[access_index];ck(r['mode']=='K' and r['d_B']>0,'genuine B intervention')
            d=depth(r['destination_B'],y);ck(d<=prev+2,'per-splay source displacement')
            history.append(dict(after_access=r['occurrence'],depth=d));prev=d
        if payer['has_KEEP']:
            first=payer['first_KEEP'];d=depth(rows[first]['source_B'],y)
            ck(d<=h+2*k and payer['q']<=d//2<=c,'derived delayed B bound')
        else:ck(payer['q']==0 and c==0,'KEEP-less payer has no B demand')
        ck(anchor['delta']+c<=2*payer['a'] and payer['delta']<=-anchor['delta']<0,'private payer threshold and negative surplus')
        ids=[(i+z)%m for z in range(offset+1)]
        arc_delta=sum(bs[t]['delta'] for t in ids);ck(arc_delta<=0,'complete interval paid')
        return dict(anchor=i,payer=j,offset=offset,indices=ids,interior=interior,key=y,
          pre_anchor_depth=depth(pre,y),h=h,k=k,ceiling=c,intervening_B_accesses=intervening,
          depth_history=history,endpoint_q=payer['q'],endpoint_a=payer['a'],
          threshold_lhs=anchor['delta']+c,threshold_rhs=2*payer['a'],arc_delta=arc_delta,
          anchor_occurrence=rows[anchor['leader']]['occurrence'],payer_occurrence=rows[payer['leader']]['occurrence'],
          scanned_candidates=scanned)
    def check_arcs(rows,bs,physical_pairs):
        leader_map={rows[b['leader']]['occurrence']:i for i,b in enumerate(bs)}
        arcs=[verify_pair(rows,bs,leader_map[i],leader_map[j]) for i,j in physical_pairs]
        positives={i for i,b in enumerate(bs) if b['delta']>0}
        ck({a['anchor'] for a in arcs}==positives and len(arcs)==len(positives),'every positive assigned exactly once')
        used=[v for a in arcs for v in a['indices']]
        ck(len(used)==len(set(used)),'no overlapping charging intervals')
        ck(all(b['delta']<=0 for i,b in enumerate(bs) if i not in used),'remaining blocks local')
        return arcs
    def check_credits(rows,bs,arcs,allocation):
        by_occ={r['occurrence']:r for r in rows}
        belongs={rows[t]['occurrence']:i for i,b in enumerate(bs) for t in b['indices']}
        expected_d={(o,j) for o,r in by_occ.items() for j,e in enumerate(r['B_events']) if e[0]!='ZIG'}
        expected_c={(o,j,slot) for o,r in by_occ.items() for j in range(len(r['A_events'])) for slot in (0,1)}
        allowed={(a['anchor'],a['payer']) for a in arcs};ds=[];cs=[]
        for r in allocation:
            d,cr=tuple(r['demand']),tuple(r['credit'])
            ck(d in expected_d and cr in expected_c,'genuine source demand and credit')
            bd,bc=belongs[d[0]],belongs[cr[0]]
            ck(bd==bc or (bd,bc) in allowed,'no lending from intermediates or other payers')
            ds.append(d);cs.append(cr)
        ck(set(ds)==expected_d and len(set(ds))==len(ds),'every B double paid once')
        ck(len(set(cs))==len(cs),'no A unit reused')
        return len(expected_c)-len(cs)
    oldpath=HERE.parent/'route_c_shallow_successor_charging_20261031_v001/shallow_successor_certificate.json'
    old=json.loads(oldpath.read_text(encoding='utf-8'))
    full_count=prefix_count=cut_count=allocation_count=0;summary=[]
    for wi,w in enumerate(cert['witnesses']):
        rows=w['full_replay'];initial=w['initial_diagonal'];delayed=wi<2
        ck(w['strict_delayed']==delayed and len(rows)==(23 if delayed else 22),'predeclared scope')
        a,b=replay(initial,initial,w['prefix'],w['prefix_replay'])
        ck((a,b)==(w['cycle_initial_A'],w['cycle_initial_B']),'actual diagonal reachability')
        aa,bb=replay(a,b,w['word'],rows)
        ck((aa,bb)==(a,b) and w['actual_pair_closure'],'exact paired closure')
        ck([r['occurrence'] for r in rows]==list(range(len(rows))),'one occurrence budget per cycle')
        bs=blocks(rows);ck(bs==w['blocks'],'all block metadata')
        physical_pairs=[(a['anchor_occurrence'],a['payer_occurrence']) for a in w['arcs']]
        arcs=check_arcs(rows,bs,physical_pairs);ck(arcs==w['arcs'],'full source certificate for first-payer scan')
        ck(len(arcs)==1 and arcs[0]['anchor']==0,'sole positive anchor')
        unused=check_credits(rows,bs,arcs,w['credit_assignments'])
        A,Q,Z=sum(r['a'] for r in rows),sum(r['q'] for r in rows),sum(r['z'] for r in rows)
        expected=(30,12,16,48) if delayed else (31,11,16,51)
        ck((A,Q,Z,2*A-Q)==expected==(w['A'],w['Q_B'],w['Z_B'],w['weight']),'complete exact totals')
        ck(unused==w['unused_credit_count']==2*A-Q,'unit-credit accounting')
        immediate_sc=True
        for i,b in enumerate(bs):
            if b['delta']<=0:continue
            next_block=bs[(i+1)%len(bs)];pre=rows[b['B_active_access']]['source_B']
            immediate_sc &= depth(pre,next_block['key'])<=1 and b['delta']<=2*next_block['a']-1
        ck(immediate_sc==w['satisfies_old_SC']==(not delayed),'strict extension and old acceptance')
        ck(len(w['all_cuts'])==len(rows),'all seams recorded')
        for cut,r in enumerate(w['all_cuts']):
            rr=rows[cut:]+rows[:cut];bc=blocks(rr)
            ac=check_arcs(rr,bc,physical_pairs)
            ck(check_credits(rr,bc,ac,w['credit_assignments'])==unused,'same physical resources work at every cut')
            ck(r==dict(cut=cut,accepted=True,anchor_payer_occurrences=sorted([list(v) for v in physical_pairs]),charged_demands=Q),'cut-invariant first payers')
            cut_count+=1
        if delayed:
            arc=arcs[0]
            ck((arc['offset'],arc['h'],arc['k'],arc['ceiling'],arc['threshold_lhs'],arc['threshold_rhs'])==(2,1,1,1,2,2),'genuine delayed payer binds source threshold')
            ck([(r['a'],r['q'],r['delta']) for r in rows[:3]]==[(1,3,1),(2,1,-3),(1,0,-2)],'positive, intervention and payer')
            ck(arc['arc_delta']==-4 and rows[1]['d_B']>0,'genuine intervening B work')
            ck(rows[6]['destination_A']==rows[6]['destination_B'],'synchronization by KEEP6 or reflection')
            pre=rows[0]['source_B'];root=pre[0]
            ck(depth(pre,rows[1]['key'])==2 and all(bs[j]['key']!=root for j in (1,2,3)),'old SC and short former-root conditions fail')
            ck(w['novelty']['positive_blocks']==[0] and w['novelty']['KEEP_support']==list(range(1,8)) and
               w['novelty']['first_former_root_return_offset']==8,'named older packet/support exclusions')
        else:
            prior=old['witnesses'][wi-2]
            ck(w['prefix']==prior['prefix'] and w['word']==prior['word'],'old word unchanged')
            ck(all({k:v for k,v in r.items() if k!='occurrence'}==o for r,o in zip(rows,prior['full_replay'])),'old source rows unchanged')
        full_count+=len(rows);prefix_count+=len(w['prefix_replay']);allocation_count+=len(w['credit_assignments'])
        summary.append(dict(name=w['name'],A=A,Q_B=Q,Z_B=Z,weight=2*A-Q,old_SC=immediate_sc))
    for wi in (0,2):
        original,ref=cert['witnesses'][wi:wi+2]
        ck(ref['initial_diagonal']==mirror(original['initial_diagonal'],7) and
           ref['word']==[[m,8-x] for m,x in original['word']],'reflected word')
        for r,s in zip(original['full_replay'],ref['full_replay']):
            ck(all(s[k]==mirror(r[k],7) for k in ('source_A','source_B','destination_A','destination_B')),'reflected complete states')
    ck(len(cert['depth_tax_controls'])==6,'three literal tax controls plus reflections')
    zero_double_changes=0
    for r in cert['depth_tax_controls']:
        tt,es,d,q,z=access(r['tree'],r['target']);before,after=depth(r['tree'],r['tracked']),depth(tt,r['tracked'])
        ck((tt,evs(es),d,q,z)==(r['tree_after'],r['events'],r['target_depth'],r['q'],r['z']),'literal tax-control trace')
        ck((before,after,int(d>0),d>0)==(r['tracked_depth_before'],r['tracked_depth_after'],r['tax'],r['genuine_B_change']),'tax uses activity')
        ck(after-before<=2*r['tax'],'source displacement bound')
        if d==1:
            ck(q==0 and r['tax']==1 and after-before==1,'zero-double zig still incurs delay tax')
            zero_double_changes+=1
    ck(zero_double_changes==2,'both orientations of zero-double change')
    v1=(HERE/'audit_delayed_shallow.py').read_text(encoding='utf-8')
    expected=v1.replace("save('entry_source_pins.json',dict(","save('entry_source_pins_v002.json',dict(").replace(
      "assert {k:v for k,v in row.items() if k!='occurrence'}==prior",
      "assert json.loads(json.dumps({k:v for k,v in row.items() if k!='occurrence'}))==prior")
    ck((HERE/'audit_delayed_shallow_v002.py').read_text(encoding='utf-8')==expected,'v002 changes only output pin name and tuple/JSON comparison')
    ck(cert['finite_fits']==cert['word_searches']==cert['larger_finite_sizes']==cert['source_graph_searches']==0 and
       cert['matching_terminal_line']=='FROZEN','scope and freeze')
    result=dict(status='PASS',date='2026-10-31',complete_cycle_source_rows=full_count,
      complete_reachability_prefix_rows=prefix_count,pointer_source_accesses=calls,
      exact_credit_assignments=allocation_count,cyclic_cuts_verified=cut_count,
      depth_tax_controls=6,zero_double_zig_changes_verified=zero_double_changes,
      no_credit_reuse=True,canonical_first_payers_verified=True,disjoint_intervals_verified=True,
      source_reachability_and_pair_closure=True,strict_extension_of_SC=True,preserved_SC_witnesses=2,
      witnesses=summary,producer_imported=False,allocation_optimizer_used=False,old_recognizers_executed=False,
      serialization_only_v002_correction_verified=True,initial_failed_artifacts_preserved=True,
      all_size_theorem='analytic proof in DS01; no finite extrapolation',
      restricted_class='PROVED—RESTRICTED DOMAIN',universal_CD='OPEN',
      matching_terminal_line='FROZEN',finite_fits=0,larger_finite_sizes=0,
      certificate_sha256=hashlib.sha256(cp.read_bytes()).hexdigest())
    with (HERE/'independent_audit.json').open('x',encoding='utf-8') as f:
        json.dump(result,f,indent=2,ensure_ascii=False);f.write('\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
