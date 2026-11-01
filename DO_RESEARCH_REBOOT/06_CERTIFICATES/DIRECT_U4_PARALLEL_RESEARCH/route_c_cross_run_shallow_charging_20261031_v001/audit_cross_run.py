"""Cut-certified one-pool batches spanning distinct positive runs; no source search."""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PARENT=HERE.parent
STAGE=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,v):
    with (HERE/name).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2,ensure_ascii=False);f.write('\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()

def main():
    olddir=PARENT/'route_c_shared_shallow_charging_20261031_v001'
    oldpins=json.loads((olddir/'entry_source_pins.json').read_text(encoding='utf-8'))
    pins=dict(oldpins['files'])
    for rel,value in pins.items():assert sha(ROOT/rel)==value,rel
    for p in PARENT.rglob('*'):
        if p.is_file() and HERE not in p.parents:pins[p.relative_to(ROOT).as_posix()]=sha(p)
    stage={p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert len(stage)==125
    status=git('status','--porcelain=v1','--untracked-files=no');assert not status
    save('entry_source_pins.json',dict(date='2026-10-31',head=git('rev-parse','HEAD'),
      branch=git('branch','--show-current'),tracked_status=status,files=pins,
      stage_files=stage,inherited_pins=len(oldpins['files'])))
    spec=importlib.util.spec_from_file_location('tuple_source',ROOT/'python/independent/splay.py')
    s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s);L=s.LEAF
    def raw(t):return None if t==L else [t[1],raw(t[2]),raw(t[3])]
    def tup(t):return L if t is None else s.node(t[0],tup(t[1]),tup(t[2]))
    def mirror(t,n):return L if t==L else s.node(n+1-t[1],mirror(t[3],n),mirror(t[2],n))
    def depth(t,x):return s.lookup(t,x)[1]
    def step(a,b,mode,x,occ):
        ap,ae=s.trace(a,x);da=depth(a,x)
        if mode=='K':bp,be=s.trace(b,x);db=depth(b,x)
        else:bp,be,db=b,[],None
        q=sum(e[0]!='ZIG' for e in be);z=sum(e[0]=='ZIG' for e in be)
        assert len(ae)==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0)
        return ap,bp,dict(occurrence=occ,mode=mode,key=x,source_A=raw(a),source_B=raw(b),
          destination_A=raw(ap),destination_B=raw(bp),d_A=da,d_B=db,a=len(ae),q=q,z=z,
          A_events=ae,B_events=be,delta=q-2*len(ae))
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
    def runs(bs):
        if not bs or not any(b['delta']>0 for b in bs):return []
        if all(b['delta']>0 for b in bs):return None
        rr=[];m=len(bs)
        for i,b in enumerate(bs):
            if b['delta']<=0 or bs[(i-1)%m]['delta']>0:continue
            ids=[];j=i
            while bs[j]['delta']>0:ids.append(j);j=(j+1)%m
            rr.append(ids)
        return rr
    def collar(rows,bs,i):
        pre=tup(rows[bs[i]['B_active_access']]['source_B'])
        return {pre[1]}|{child[1] for child in pre[2:] if child!=L}
    def bound(rows,bs,i,j,y,history=False):
        at=bs[i]['B_active_access'];pre=tup(rows[at]['source_B']);post=tup(rows[at]['destination_B'])
        d,h=depth(pre,y),depth(post,y);assert d<=1 and 1<=h<=3
        m=len(bs);offset=(j-i)%m;assert offset>0
        active=[bs[(i+z)%m]['B_active_access'] for z in range(1,offset) if bs[(i+z)%m]['B_active_access'] is not None]
        k=len(active);c=h//2+k if bs[j]['has_KEEP'] else 0
        r=dict(anchor=i,anchor_occurrence=rows[bs[i]['leader']]['occurrence'],pre_depth=d,h=h,k=k,ceiling=c)
        if history:
            hh=[dict(after_access=rows[at]['occurrence'],depth=h)];previous=h
            for ai in active:
                dd=depth(tup(rows[ai]['destination_B']),y);assert dd<=previous+2
                hh.append(dict(after_access=rows[ai]['occurrence'],depth=dd));previous=dd
            r.update(intervening_B_occurrences=[rows[a]['occurrence'] for a in active],depth_history=hh)
        return r
    def scan(rows,bs,cut):
        m=len(bs);pending=[];common=None;E=0;packets=[];tests=[]
        if not m:
            assert sum(r['q'] for r in rows)==0
            return dict(cut=0,accepted=True,packets=[],unpaid_anchor_occurrences=[],unpaid_excess=0)
        rr=runs(bs);runmap={i:k for k,ids in enumerate(rr or []) for i in ids}
        for turn in range(m):
            j=(cut+turn)%m;b=bs[j]
            if b['delta']>0:
                pending.append(j);E+=b['delta'];cc=collar(rows,bs,j)
                common=cc if common is None else common&cc
                continue
            if not pending:continue
            y=b['key'];bb=[bound(rows,bs,i,j,y) for i in pending] if y in common else []
            c=min(v['ceiling'] for v in bb) if bb else None
            ok=bool(bb) and E+c<=2*b['a']
            tests.append(dict(block=j,key=y,pending_anchor_occurrences=[rows[bs[i]['leader']]['occurrence'] for i in pending],
              pending_excess=E,common_keys=sorted(common),anchor_bounds=bb,ceiling=c,
              A_capacity=2*b['a'],admissible=ok))
            if not ok:continue
            extent=(j-pending[0])%m;ids=[(pending[0]+z)%m for z in range(extent+1)]
            interior=[z for z in ids if z not in pending and z!=j]
            assert [z for z in ids if bs[z]['delta']>0]==pending
            assert all(bs[z]['delta']<=0 for z in interior)
            assert b['q']<=c and b['delta']<=-E<0
            packet=dict(anchors=list(pending),anchor_occurrences=[rows[bs[i]['leader']]['occurrence'] for i in pending],
              payer=j,payer_occurrence=rows[b['leader']]['occurrence'],key=y,common_keys=sorted(common),excess=E,
              anchor_bounds=[bound(rows,bs,i,j,y,True) for i in pending],ceiling=c,
              threshold_lhs=E+c,threshold_rhs=2*b['a'],payer_q=b['q'],payer_a=b['a'],
              indices=ids,interior=interior,packet_delta=sum(bs[z]['delta'] for z in ids),
              distinct_positive_runs=len({runmap[z] for z in pending}),closing_tests=tests)
            assert packet['packet_delta']<=0
            packets.append(packet);pending=[];common=None;E=0;tests=[]
        accepted=not pending
        used=[z for p in packets for z in p['indices']];assert len(used)==len(set(used))
        if accepted:assert all(b['delta']<=0 for i,b in enumerate(bs) if i not in used)
        return dict(cut=cut,accepted=accepted,packets=packets,
          unpaid_anchor_occurrences=[rows[bs[i]['leader']]['occurrence'] for i in pending],unpaid_excess=E)
    def assign(rows,bs,packets):
        credits={i:[[rows[b['leader']]['occurrence'],z,slot] for z in range(b['a']) for slot in (0,1)] for i,b in enumerate(bs)}
        demands={i:[[rows[t]['occurrence'],z] for t in b['indices'] for z,e in enumerate(rows[t]['B_events']) if e[0]!='ZIG'] for i,b in enumerate(bs)}
        allocation=[];slices=[];handled=set()
        for p in packets:
            j=p['payer'];handled.add(j);cursor=0
            for i in p['anchors']:
                handled.add(i);local=2*bs[i]['a'];excess=bs[i]['delta']
                for d,c in zip(demands[i][:local],credits[i]):allocation.append(dict(demand=d,credit=c,kind='anchor_local'))
                selected=credits[j][cursor:cursor+excess]
                for d,c in zip(demands[i][local:],selected):allocation.append(dict(demand=d,credit=c,kind='cross_run_payer_transfer'))
                slices.append(dict(anchor_occurrence=rows[bs[i]['leader']]['occurrence'],payer_occurrence=rows[bs[j]['leader']]['occurrence'],
                                   start=cursor,end=cursor+excess,credits=selected));cursor+=excess
            assert cursor==p['excess']
            for d,c in zip(demands[j],credits[j][cursor:]):allocation.append(dict(demand=d,credit=c,kind='payer_local'))
        for i,b in enumerate(bs):
            if i in handled:continue
            assert b['delta']<=0
            for d,c in zip(demands[i],credits[i]):allocation.append(dict(demand=d,credit=c,kind='other_local'))
        assert len(allocation)==sum(r['q'] for r in rows)
        assert len({tuple(v['demand']) for v in allocation})==len({tuple(v['credit']) for v in allocation})==len(allocation)
        return allocation,slices
    def old_SP(rows,bs):
        rr=runs(bs)
        if rr is None:return False
        m=len(bs)
        for run in rr:
            common=set.intersection(*(collar(rows,bs,i) for i in run));E=sum(bs[i]['delta'] for i in run);found=False
            for off in range(1,m):
                j=(run[-1]+off)%m;b=bs[j]
                if b['delta']>0:break
                if b['key'] in common:
                    c=min(bound(rows,bs,i,j,b['key'])['ceiling'] for i in run)
                    if E+c<=2*b['a']:found=True;break
            if not found:return False
        return True
    def witness(name,initial,n,prefix,word,cross):
        a=b=initial;pr=[]
        for i,(mode,x) in enumerate(prefix):a,b,r=step(a,b,mode,x,-i-1);pr.append(r)
        ia,ib=a,b;rows=[]
        for i,(mode,x) in enumerate(word):a,b,r=step(a,b,mode,x,i);rows.append(r)
        assert (a,b)==(ia,ib)
        bs=blocks(rows);trials=[scan(rows,bs,cut) for cut in range(len(bs))]
        good=[t for t in trials if t['accepted']];assert good
        chosen=good[0];allocation,slices=assign(rows,bs,chosen['packets'])
        compact=[];alternative_assignment_count=0
        for t in trials:
            if t['accepted']:
                aa,_=assign(rows,bs,t['packets']);alternative_assignment_count+=len(aa)
            compact.append(dict(cut=t['cut'],accepted=t['accepted'],
              packet_occurrences=[[p['anchor_occurrences'],p['payer_occurrence']] for p in t['packets']],
              unpaid_anchor_occurrences=t['unpaid_anchor_occurrences'],unpaid_excess=t['unpaid_excess']))
        accepted_SP=old_SP(rows,bs);assert accepted_SP is (not cross)
        if cross:
            assert runs(bs)==[[0],[2]]
            assert [(r['a'],r['q'],r['delta']) for r in rows[:5]]==[(2,6,2),(2,0,-4),(1,3,1),(1,2,0),(2,0,-4)]
            p=chosen['packets'][0]
            assert p['anchors']==[0,2] and p['payer']==4 and p['distinct_positive_runs']==2
            assert p['excess']==3 and p['ceiling']==1 and p['threshold_lhs']==p['threshold_rhs']==4
            assert [(b['h'],b['k'],b['ceiling']) for b in p['anchor_bounds']]==[(1,2,2),(1,1,1)]
            assert rows[12]['destination_A']==rows[12]['destination_B']
        A,Q,Z=sum(r['a'] for r in rows),sum(r['q'] for r in rows),sum(r['z'] for r in rows)
        return dict(name=name,strict_cross_run=cross,n=n,initial_diagonal=raw(initial),prefix=prefix,prefix_replay=pr,
          cycle_initial_A=raw(ia),cycle_initial_B=raw(ib),word=word,full_replay=rows,blocks=bs,positive_runs=runs(bs),
          chosen_cut=chosen['cut'],packets=chosen['packets'],credit_assignments=allocation,payer_slices=slices,
          cut_trials=compact,accepted_cuts=[t['cut'] for t in good],rejected_cut_count=len(trials)-len(good),
          alternative_assignment_checks=alternative_assignment_count,satisfies_old_SP=accepted_SP,
          A=A,Q_B=Q,Z_B=Z,weight=2*A-Q,unused_credit_count=2*A-Q,actual_pair_closure=True,
          KEEP_support=sorted({r['key'] for r in rows if r['mode']=='K'}))
    n=13;initial=s.vine(n);prefix=[['D',9]]
    word=([['K',13],['D',11],['K',12],['K',11],['K',2]]+[['K',k] for k in range(3,14)]+
          [['K',k] for k in range(1,14)]+[['K',k] for k in range(12,0,-1)]+[['D',9]])
    assert len(word)==42
    new=witness('two_distinct_runs_one_batch_payer',initial,n,prefix,word,True)
    ref=witness('two_distinct_runs_one_batch_payer_reflection',mirror(initial,n),n,
      [[m,n+1-x] for m,x in prefix],[[m,n+1-x] for m,x in word],True)
    oldcert=json.loads((olddir/'shared_shallow_certificate.json').read_text(encoding='utf-8'));preserved=[]
    for old in oldcert['witnesses']:
        current=witness('preserved_'+old['name'],tup(old['initial_diagonal']),old['n'],old['prefix'],old['word'],False)
        assert all(json.loads(json.dumps(r))==prior for r,prior in zip(current['full_replay'],old['full_replay']))
        preserved.append(current)
    for w,old in ((new,oldcert['witnesses'][0]),(ref,oldcert['witnesses'][1])):
        assert w['full_replay'][3]['destination_A']==old['full_replay'][2]['destination_A']
        assert w['full_replay'][3]['destination_B']==old['full_replay'][2]['destination_B']
        for r,prior in zip(w['full_replay'][4:],old['full_replay'][3:]):
            assert json.loads(json.dumps({k:v for k,v in r.items() if k!='occurrence'}))=={k:v for k,v in prior.items() if k!='occurrence'}
    cert=dict(schema='cyclic-cut-greedy-cross-run-batching-v1',date='2026-10-31',witnesses=[new,ref]+preserved,
      finite_fits=0,size_sweeps=0,word_searches=0,source_graph_searches=0,allocation_optimizer_used=False,
      matching_terminal_line='FROZEN',universal_CD='OPEN',all_cut_trials_are_alternative_one_period_passes=True)
    save('cross_run_shallow_certificate.json',cert)
    print(json.dumps(dict(preserved_files=len(pins),stage_files=len(stage),
      witnesses=[dict(name=w['name'],length=len(w['word']),A=w['A'],Q_B=w['Q_B'],Z_B=w['Z_B'],weight=w['weight'],
        old_SP=w['satisfies_old_SP'],chosen_cut=w['chosen_cut'],accepted_cuts=len(w['accepted_cuts']),
        rejected_cuts=w['rejected_cut_count'],packets=[[p['anchor_occurrences'],p['payer_occurrence']] for p in w['packets']]) for w in cert['witnesses']]),indent=2))

if __name__=='__main__':main()
