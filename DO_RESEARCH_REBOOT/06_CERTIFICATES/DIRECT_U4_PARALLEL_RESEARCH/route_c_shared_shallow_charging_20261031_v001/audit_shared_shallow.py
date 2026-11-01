"""One common payer per maximal positive run, fixed source words and explicit slices."""
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
    olddir=PARENT/'route_c_delayed_shallow_charging_20261031_v001'
    oldpins=json.loads((olddir/'entry_source_pins_v002.json').read_text(encoding='utf-8'))
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
    s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
    L=s.LEAF
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
            x=rows[i]['key'];a=rows[i]['a'];q=sum(rows[j]['q'] for j in ids)
            assert all(rows[j]['a']==0 and rows[j]['key']==x for j in ids[1:])
            kk=[j for j in ids if rows[j]['mode']=='K'];active=[j for j in kk if rows[j]['d_B']>0]
            assert len(active)<=1
            bs.append(dict(leader=i,key=x,indices=ids,a=a,q=q,delta=q-2*a,has_KEEP=bool(kk),
              first_KEEP=kk[0] if kk else None,B_active_access=active[0] if active else None))
        return bs
    def runs(bs):
        if not bs or not any(b['delta']>0 for b in bs):return []
        if all(b['delta']>0 for b in bs):return None
        m=len(bs);out=[]
        for i,b in enumerate(bs):
            if b['delta']<=0 or bs[(i-1)%m]['delta']>0:continue
            ids=[];j=i
            while bs[j]['delta']>0:ids.append(j);j=(j+1)%m
            out.append(ids)
        return out
    def bound(rows,bs,i,j,y,history=False):
        m=len(bs);at=bs[i]['B_active_access'];pre=tup(rows[at]['source_B']);post=tup(rows[at]['destination_B'])
        d=depth(pre,y);h=depth(post,y);assert d<=1 and 1<=h<=3
        offset=(j-i)%m;assert offset>0
        between=[(i+z)%m for z in range(1,offset)]
        active=[bs[z]['B_active_access'] for z in between if bs[z]['B_active_access'] is not None]
        k=len(active);c=h//2+k if bs[j]['has_KEEP'] else 0
        out=dict(anchor=i,anchor_occurrence=rows[bs[i]['leader']]['occurrence'],
                 pre_depth=d,h=h,k=k,ceiling=c)
        if history:
            hist=[dict(after_access=rows[at]['occurrence'],depth=h)];previous=h
            for ai in active:
                dd=depth(tup(rows[ai]['destination_B']),y);assert dd<=previous+2
                hist.append(dict(after_access=rows[ai]['occurrence'],depth=dd));previous=dd
            out.update(intervening_B_occurrences=[rows[a]['occurrence'] for a in active],depth_history=hist)
        return out
    def recognize(rows):
        bs=blocks(rows);rr=runs(bs)
        if rr is None:return False,bs,[],[]
        if not bs:assert sum(r['q'] for r in rows)==0
        m=len(bs);packets=[]
        for run in rr:
            E=sum(bs[i]['delta'] for i in run);common=None
            for i in run:
                pre=tup(rows[bs[i]['B_active_access']]['source_B'])
                collar={pre[1]}|{child[1] for child in pre[2:] if child!=L}
                common=collar if common is None else common&collar
            common=sorted(common);last=run[-1];scanned=[];chosen=None
            for off in range(1,m):
                j=(last+off)%m;b=bs[j]
                if b['delta']>0:break
                y=b['key'];bounds=[bound(rows,bs,i,j,y) for i in run] if y in common else []
                ceiling=min(v['ceiling'] for v in bounds) if bounds else None
                ok=bool(bounds) and E+ceiling<=2*b['a']
                scanned.append(dict(payer=j,offset_after_run=off,key=y,common_key=y in common,
                   anchor_bounds=bounds,ceiling=ceiling,run_excess=E,A_capacity=2*b['a'],admissible=ok))
                if not ok:continue
                assert b['q']<=ceiling and b['delta']<=-E<0
                extent=(j-run[0])%m;ids=[(run[0]+z)%m for z in range(extent+1)]
                interior=[(last+z)%m for z in range(1,off)]
                assert all(bs[z]['delta']<=0 for z in interior)
                chosen=dict(run=run,anchor_occurrences=[rows[bs[i]['leader']]['occurrence'] for i in run],
                  payer=j,payer_occurrence=rows[b['leader']]['occurrence'],key=y,common_keys=common,
                  run_excess=E,anchor_bounds=[bound(rows,bs,i,j,y,True) for i in run],
                  ceiling=ceiling,threshold_lhs=E+ceiling,threshold_rhs=2*b['a'],
                  payer_q=b['q'],payer_a=b['a'],indices=ids,interior=interior,
                  packet_delta=sum(bs[z]['delta'] for z in ids),scanned_candidates=scanned)
                assert chosen['packet_delta']<=0
                break
            if chosen is None:return False,bs,rr,packets
            packets.append(chosen)
        used=[i for packet in packets for i in packet['indices']]
        assert len(used)==len(set(used))
        assert all(b['delta']<=0 for i,b in enumerate(bs) if i not in used)
        return True,bs,rr,packets
    def assign(rows,bs,packets):
        credits={i:[[rows[b['leader']]['occurrence'],z,slot] for z in range(b['a']) for slot in (0,1)] for i,b in enumerate(bs)}
        demands={i:[[rows[t]['occurrence'],z] for t in b['indices'] for z,e in enumerate(rows[t]['B_events']) if e[0]!='ZIG'] for i,b in enumerate(bs)}
        out=[];handled=set();slices=[]
        for packet in packets:
            j=packet['payer'];handled.add(j);cursor=0
            for i in packet['run']:
                handled.add(i);local=2*bs[i]['a'];excess=bs[i]['delta']
                for d,c in zip(demands[i][:local],credits[i]):out.append(dict(demand=d,credit=c,kind='anchor_local'))
                selected=credits[j][cursor:cursor+excess]
                for d,c in zip(demands[i][local:],selected):out.append(dict(demand=d,credit=c,kind='shared_payer_transfer'))
                slices.append(dict(anchor_occurrence=rows[bs[i]['leader']]['occurrence'],
                  payer_occurrence=rows[bs[j]['leader']]['occurrence'],start=cursor,end=cursor+excess,credits=selected))
                cursor+=excess
            assert cursor==packet['run_excess']
            for d,c in zip(demands[j],credits[j][cursor:]):out.append(dict(demand=d,credit=c,kind='payer_local'))
        for i,b in enumerate(bs):
            if i in handled:continue
            assert b['delta']<=0
            for d,c in zip(demands[i],credits[i]):out.append(dict(demand=d,credit=c,kind='other_local'))
        assert len(out)==sum(r['q'] for r in rows)
        assert len({tuple(v['demand']) for v in out})==len({tuple(v['credit']) for v in out})==len(out)
        return out,slices
    def old_DS(rows,bs):
        m=len(bs)
        for i,b in enumerate(bs):
            if b['delta']<=0:continue
            pre=tup(rows[b['B_active_access']]['source_B'])
            collar={pre[1]}|{ch[1] for ch in pre[2:] if ch!=L};found=False
            for off in range(1,m):
                j=(i+off)%m;other=bs[j]
                if other['delta']>0:break
                if other['key'] in collar:
                    c=bound(rows,bs,i,j,other['key'])['ceiling']
                    if b['delta']+c<=2*other['a']:found=True;break
            if not found:return False
        return True
    def witness(name,initial,n,prefix,word,shared):
        a=b=initial;pr=[]
        for i,(mode,x) in enumerate(prefix):a,b,r=step(a,b,mode,x,-i-1);pr.append(r)
        ia,ib=a,b;rows=[]
        for i,(mode,x) in enumerate(word):a,b,r=step(a,b,mode,x,i);rows.append(r)
        assert (a,b)==(ia,ib)
        ok,bs,rr,packets=recognize(rows);assert ok
        allocation,slices=assign(rows,bs,packets);accepted_DS=old_DS(rows,bs)
        assert accepted_DS is (not shared)
        if shared:
            assert rr==[[0,1]] and len(packets)==1
            p=packets[0]
            assert [(r['a'],r['q'],r['delta']) for r in rows[:4]]==[(2,6,2),(1,3,1),(1,2,0),(2,0,-4)]
            assert p['common_keys']==[rows[3]['key']] and p['run_excess']==3 and p['ceiling']==1
            assert [(v['h'],v['k'],v['ceiling']) for v in p['anchor_bounds']]==[(1,2,2),(1,1,1)]
            assert p['threshold_lhs']==p['threshold_rhs']==4 and p['payer']==3
            assert rows[11]['destination_A']==rows[11]['destination_B']
        physical=sorted((tuple(p['anchor_occurrences']),p['payer_occurrence']) for p in packets);cuts=[]
        for cut in range(len(rows)):
            rotated=rows[cut:]+rows[:cut];accepted,bb,_,pp=recognize(rotated);assert accepted
            ids=sorted((tuple(p['anchor_occurrences']),p['payer_occurrence']) for p in pp);assert ids==physical
            alloc,sl=assign(rotated,bb,pp)
            assert {(tuple(v['demand']),tuple(v['credit'])) for v in alloc}=={(tuple(v['demand']),tuple(v['credit'])) for v in allocation}
            cuts.append(dict(cut=cut,accepted=True,packet_occurrences=[[list(a),j] for a,j in ids],charged_demands=len(alloc)))
        A,Q,Z=sum(r['a'] for r in rows),sum(r['q'] for r in rows),sum(r['z'] for r in rows)
        return dict(name=name,strict_shared=shared,n=n,initial_diagonal=raw(initial),prefix=prefix,prefix_replay=pr,
          cycle_initial_A=raw(ia),cycle_initial_B=raw(ib),word=word,full_replay=rows,blocks=bs,positive_runs=rr,
          packets=packets,credit_assignments=allocation,payer_slices=slices,all_cuts=cuts,
          satisfies_old_DS=accepted_DS,A=A,Q_B=Q,Z_B=Z,weight=2*A-Q,unused_credit_count=2*A-Q,
          actual_pair_closure=True,KEEP_support=sorted({r['key'] for r in rows if r['mode']=='K'}))
    n=13;initial=s.vine(n);prefix=[['D',9]]
    word=([['K',13],['K',12],['K',11],['K',2]]+[['K',k] for k in range(3,14)]+
          [['K',k] for k in range(1,14)]+[['K',k] for k in range(12,0,-1)]+[['D',9]])
    assert len(word)==41
    new=witness('two_anchors_one_delayed_pool',initial,n,prefix,word,True)
    ref=witness('two_anchors_one_delayed_pool_reflection',mirror(initial,n),n,
          [[m,n+1-x] for m,x in prefix],[[m,n+1-x] for m,x in word],True)
    oldcert=json.loads((olddir/'delayed_shallow_certificate.json').read_text(encoding='utf-8'))
    oldw=[]
    for old in oldcert['witnesses']:
        current=witness('preserved_'+old['name'],tup(old['initial_diagonal']),old['n'],old['prefix'],old['word'],False)
        assert all(json.loads(json.dumps(r))==prior for r,prior in zip(current['full_replay'],old['full_replay']))
        oldw.append(current)
    cert=dict(schema='one-shared-shallow-payer-per-positive-run-v1',date='2026-10-31',
      witnesses=[new,ref]+oldw,finite_fits=0,size_sweeps=0,source_graph_searches=0,word_searches=0,
      source_witness_n13_analytically_predetermined=True,allocation_optimizer_used=False,
      matching_terminal_line='FROZEN',universal_CD='OPEN')
    save('shared_shallow_certificate.json',cert)
    print(json.dumps(dict(preserved_files=len(pins),stage_files=len(stage),
      witnesses=[dict(name=w['name'],n=w['n'],length=len(w['word']),A=w['A'],Q_B=w['Q_B'],Z_B=w['Z_B'],
         weight=w['weight'],old_DS=w['satisfies_old_DS'],run_excesses=[p['run_excess'] for p in w['packets']],
         ceilings=[p['ceiling'] for p in w['packets']],thresholds=[[p['threshold_lhs'],p['threshold_rhs']] for p in w['packets']]) for w in cert['witnesses']]),indent=2))

if __name__=='__main__':main()
