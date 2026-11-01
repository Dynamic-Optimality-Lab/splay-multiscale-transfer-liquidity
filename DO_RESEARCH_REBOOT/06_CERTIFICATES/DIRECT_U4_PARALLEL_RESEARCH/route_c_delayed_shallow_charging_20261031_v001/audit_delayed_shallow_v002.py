"""Canonical delayed private-payer charging on four fixed source walks; no search."""
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
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,indent=2,ensure_ascii=False);f.write('\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()

def main():
    olddir=PARENT/'route_c_shallow_successor_charging_20261031_v001'
    oldpins=json.loads((olddir/'entry_source_pins.json').read_text(encoding='utf-8'))
    pins=dict(oldpins['files'])
    for rel,value in pins.items():assert sha(ROOT/rel)==value,rel
    for p in PARENT.rglob('*'):
        if p.is_file() and HERE not in p.parents:pins[p.relative_to(ROOT).as_posix()]=sha(p)
    stage={p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert len(stage)==125
    status=git('status','--porcelain=v1','--untracked-files=no');assert not status
    save('entry_source_pins_v002.json',dict(date='2026-10-31',head=git('rev-parse','HEAD'),
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
            kk=[j for j in ids if rows[j]['mode']=='K']
            active=[j for j in kk if rows[j]['d_B']>0];assert len(active)<=1
            bs.append(dict(leader=i,key=x,indices=ids,a=a,q=q,delta=q-2*a,has_KEEP=bool(kk),
                           first_KEEP=kk[0] if kk else None,B_active_access=active[0] if active else None))
        return bs
    def recognize(rows):
        bs=blocks(rows);m=len(bs);arcs=[]
        if not bs:
            assert sum(r['q'] for r in rows)==0
            return True,bs,arcs
        for i,b in enumerate(bs):
            if b['delta']<=0:continue
            at=b['B_active_access'];assert at is not None
            pre=tup(rows[at]['source_B']);post=tup(rows[at]['destination_B'])
            collar=[pre[1]]+[child[1] for child in pre[2:] if child!=L]
            heights={y:depth(post,y) for y in collar}
            assert all(1<=h<=3 for h in heights.values())
            k=0;scanned=[];chosen=None
            for offset in range(1,m):
                j=(i+offset)%m;other=bs[j]
                if other['delta']>0:break
                y=other['key'];h=heights.get(y)
                ceiling=(h//2+k if other['has_KEEP'] else 0) if h is not None else None
                admissible=h is not None and b['delta']+ceiling<=2*other['a']
                scanned.append(dict(block=j,offset=offset,key=y,pre_anchor_depth=depth(pre,y),
                     h=h,k=k,ceiling=ceiling,A_capacity=2*other['a'],admissible=admissible))
                if admissible:
                    interior=[(i+z)%m for z in range(1,offset)]
                    intermediate=[bs[t]['B_active_access'] for t in interior if bs[t]['B_active_access'] is not None]
                    assert len(intermediate)==k and other['q']<=ceiling
                    assert other['delta']<=-b['delta']<0
                    hist=[dict(after_access=rows[at]['occurrence'],depth=h)]
                    previous=h
                    for access_index in intermediate:
                        d=depth(tup(rows[access_index]['destination_B']),y)
                        assert d<=previous+2
                        hist.append(dict(after_access=rows[access_index]['occurrence'],depth=d));previous=d
                    chosen=dict(anchor=i,payer=j,offset=offset,indices=[(i+z)%m for z in range(offset+1)],
                        interior=interior,key=y,pre_anchor_depth=depth(pre,y),h=h,k=k,ceiling=ceiling,
                        intervening_B_accesses=intermediate,depth_history=hist,
                        endpoint_q=other['q'],endpoint_a=other['a'],threshold_lhs=b['delta']+ceiling,
                        threshold_rhs=2*other['a'],arc_delta=sum(bs[t]['delta'] for t in [(i+z)%m for z in range(offset+1)]),
                        anchor_occurrence=rows[b['leader']]['occurrence'],payer_occurrence=rows[other['leader']]['occurrence'],
                        scanned_candidates=scanned)
                    assert chosen['arc_delta']<=0
                    break
                k+=int(other['B_active_access'] is not None)
            if chosen is None:return False,bs,arcs
            arcs.append(chosen)
        used=[v for arc in arcs for v in arc['indices']]
        assert len(used)==len(set(used))
        assert all(b['delta']<=0 for i,b in enumerate(bs) if i not in used)
        return True,bs,arcs
    def assign(rows,bs,arcs):
        credits={i:[[rows[b['leader']]['occurrence'],j,slot] for j in range(b['a']) for slot in (0,1)] for i,b in enumerate(bs)}
        demands={i:[[rows[t]['occurrence'],j] for t in b['indices'] for j,e in enumerate(rows[t]['B_events']) if e[0]!='ZIG'] for i,b in enumerate(bs)}
        out=[];paid=set()
        for arc in arcs:
            i,j=arc['anchor'],arc['payer'];paid.update((i,j));local=2*bs[i]['a'];excess=bs[i]['delta']
            for d,cr in zip(demands[i][:local],credits[i]):out.append(dict(demand=d,credit=cr,kind='anchor_local'))
            for d,cr in zip(demands[i][local:],credits[j][:excess]):out.append(dict(demand=d,credit=cr,kind='delayed_transfer'))
            for d,cr in zip(demands[j],credits[j][excess:]):out.append(dict(demand=d,credit=cr,kind='payer_local'))
        for i,b in enumerate(bs):
            if i in paid:continue
            assert b['delta']<=0
            for d,cr in zip(demands[i],credits[i]):out.append(dict(demand=d,credit=cr,kind='other_local'))
        assert len(out)==sum(r['q'] for r in rows)
        assert len({tuple(a['demand']) for a in out})==len({tuple(a['credit']) for a in out})==len(out)
        return out
    def old_sc(rows,bs):
        for i,b in enumerate(bs):
            if b['delta']<=0:continue
            other=bs[(i+1)%len(bs)];at=b['B_active_access']
            if depth(tup(rows[at]['source_B']),other['key'])>1 or b['delta']>2*other['a']-1:return False
        return True
    def witness(name,initial,prefix,word,delayed):
        a=b=initial;pr=[]
        for i,(mode,x) in enumerate(prefix):a,b,r=step(a,b,mode,x,-i-1);pr.append(r)
        ia,ib=a,b;rows=[]
        for i,(mode,x) in enumerate(word):a,b,r=step(a,b,mode,x,i);rows.append(r)
        assert (a,b)==(ia,ib)
        ok,bs,arcs=recognize(rows);assert ok and len(arcs)==1 and arcs[0]['anchor']==0
        allocation=assign(rows,bs,arcs);accepted_sc=old_sc(rows,bs)
        assert accepted_sc is (not delayed)
        if delayed:
            assert (arcs[0]['offset'],arcs[0]['k'],arcs[0]['h'],arcs[0]['ceiling'])==(2,1,1,1)
            assert (rows[0]['a'],rows[0]['q'],rows[0]['delta'])==(1,3,1)
            assert (rows[1]['a'],rows[1]['q'],rows[1]['delta'])==(2,1,-3)
            assert (rows[2]['a'],rows[2]['q'],rows[2]['delta'])==(1,0,-2)
            assert rows[6]['destination_A']==rows[6]['destination_B']
        base_pairs=sorted((z['anchor_occurrence'],z['payer_occurrence']) for z in arcs);cuts=[]
        for cut in range(len(rows)):
            rr=rows[cut:]+rows[:cut];accepted,bb,aa=recognize(rr);assert accepted
            pairs=sorted((z['anchor_occurrence'],z['payer_occurrence']) for z in aa)
            assert pairs==base_pairs
            alloc=assign(rr,bb,aa)
            assert {(tuple(v['demand']),tuple(v['credit'])) for v in alloc}=={(tuple(v['demand']),tuple(v['credit'])) for v in allocation}
            cuts.append(dict(cut=cut,accepted=True,anchor_payer_occurrences=pairs,charged_demands=len(alloc)))
        root=rows[bs[0]['B_active_access']]['source_B'][0]
        first_return=next(i for i in range(1,len(bs)) if bs[i]['key']==root)
        A,Q,Z=sum(r['a'] for r in rows),sum(r['q'] for r in rows),sum(r['z'] for r in rows)
        return dict(name=name,strict_delayed=delayed,n=7,initial_diagonal=raw(initial),prefix=prefix,
            prefix_replay=pr,cycle_initial_A=raw(ia),cycle_initial_B=raw(ib),word=word,full_replay=rows,
            blocks=bs,arcs=arcs,credit_assignments=allocation,all_cuts=cuts,satisfies_old_SC=accepted_sc,
            A=A,Q_B=Q,Z_B=Z,weight=2*A-Q,unused_credit_count=2*A-Q,actual_pair_closure=True,
            novelty=dict(positive_blocks=[i for i,b in enumerate(bs) if b['delta']>0],
                KEEP_support=sorted({r['key'] for r in rows if r['mode']=='K'}),former_root=root,
                next_three_keys=[bs[i]['key'] for i in (1,2,3)],first_former_root_return_offset=first_return))
    initial=s.vine(7);prefix=[['D',7],['D',6]]
    newword=([['K',7],['K',3],['K',2]]+[['K',k] for k in range(3,8)]+
             [['K',k] for k in range(1,8)]+[['K',k] for k in range(6,0,-1)]+[['D',7],['D',6]])
    assert len(newword)==23
    new=witness('genuine_B_delayed_child_payer',initial,prefix,newword,True)
    newref=witness('genuine_B_delayed_child_payer_reflection',mirror(initial,7),
          [[m,8-x] for m,x in prefix],[[m,8-x] for m,x in newword],True)
    oldcert=json.loads((olddir/'shallow_successor_certificate.json').read_text(encoding='utf-8'))
    preserved=[]
    for old in oldcert['witnesses']:
        current=witness('preserved_'+old['name'],tup(old['initial_diagonal']),old['prefix'],old['word'],False)
        for row,prior in zip(current['full_replay'],old['full_replay']):
            assert json.loads(json.dumps({k:v for k,v in row.items() if k!='occurrence'}))==prior
        preserved.append(current)
    local=[]
    for reflected in (False,True):
        for target in (1,2,3):
            t=s.vine(3);x=target;y=1
            if reflected:t=mirror(t,3);x=4-target;y=3
            tt,ev=s.trace(t,x);d=depth(t,x);q=sum(e[0]!='ZIG' for e in ev)
            before,after=depth(t,y),depth(tt,y)
            assert after-before<=2*int(d>0)
            local.append(dict(tree=raw(t),target=x,tracked=y,tree_after=raw(tt),events=ev,
                  target_depth=d,q=q,z=d%2,genuine_B_change=d>0,tax=int(d>0),
                  tracked_depth_before=before,tracked_depth_after=after))
    cert=dict(schema='delayed-private-shallow-charging-v1',date='2026-10-31',
       witnesses=[new,newref]+preserved,depth_tax_controls=local,
       canonical_scan='first qualifying payer before next positive; local interveners, private endpoint',
       finite_fits=0,word_searches=0,larger_finite_sizes=0,source_graph_searches=0,
       matching_terminal_line='FROZEN',universal_CD='OPEN')
    save('delayed_shallow_certificate.json',cert)
    print(json.dumps(dict(preserved_files=len(pins),stage_files=len(stage),
      witnesses=[dict(name=w['name'],length=len(w['word']),A=w['A'],Q_B=w['Q_B'],Z_B=w['Z_B'],
          weight=w['weight'],old_SC=w['satisfies_old_SC'],payer_offset=w['arcs'][0]['offset'],
          k=w['arcs'][0]['k'],h=w['arcs'][0]['h'],ceiling=w['arcs'][0]['ceiling'],
          threshold=[w['arcs'][0]['threshold_lhs'],w['arcs'][0]['threshold_rhs']]) for w in cert['witnesses']]),indent=2))

if __name__=='__main__':main()
