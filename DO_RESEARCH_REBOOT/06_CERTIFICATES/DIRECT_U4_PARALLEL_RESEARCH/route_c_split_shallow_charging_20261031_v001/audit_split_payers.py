"""Fixed split-payer construction; tuple source, no search or fitted parameters."""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
OLD=HERE.parent/'route_c_cross_run_shallow_charging_20261031_v001'
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
    def bound(rows,bs,i,j,y):
        at=bs[i]['B_active_access'];pre,post=rows[at]['source_B'],rows[at]['destination_B']
        d,h=depth(tup(pre),y),depth(tup(post),y);assert d<=1 and 1<=h<=3
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
    def xr_scan(rows,bs,cut):
        pending=[];common=None;E=0;closings=[]
        for t in range(len(bs)):
            j=(cut+t)%len(bs);b=bs[j]
            if b['delta']>0:
                pending.append(j);E+=b['delta'];cc=collar(rows,bs,j);common=cc if common is None else common&cc
            elif pending and b['key'] in common:
                c=min(bound(rows,bs,i,j,b['key'])['ceiling'] for i in pending)
                if E+c<=2*b['a']:
                    closings.append(dict(anchors=list(pending),payer=j,excess=E,ceiling=c))
                    pending=[];common=None;E=0
        return dict(cut=cut,accepted=not pending,closings=closings,
          unpaid_anchor_occurrences=[bs[i]['leader'] for i in pending],unpaid_excess=E)
    def scan(rows,bs,cut):
        history=[];paid={};pools=[];assignments=[]
        units={i:[[b['leader'],e,bit] for e in range(b['a']) for bit in (0,1)] for i,b in enumerate(bs)}
        demands={i:[[t,e] for t in b['indices'] for e,event in enumerate(rows[t]['B_events']) if event[0]!='ZIG'] for i,b in enumerate(bs)}
        for turn in range(len(bs)):
            j=(cut+turn)%len(bs);b=bs[j];capacity=2*b['a']
            if b['delta']>0:
                for d,c in zip(demands[j][:capacity],units[j]):assignments.append(dict(demand=d,credit=c,kind='positive_local'))
                history.append(j);paid[j]=0;continue
            facts=[bound(rows,bs,i,j,b['key']) for i in history if b['key'] in collar(rows,bs,i)]
            ceiling=min(f['ceiling'] for f in facts) if facts else None
            reserve=min(capacity,ceiling) if facts else capacity
            assert b['q']<=reserve
            for d,c in zip(demands[j],units[j][:reserve]):assignments.append(dict(demand=d,credit=c,kind='payer_local'))
            cursor=reserve;loans=[]
            for i in history:
                owed=bs[i]['delta']-paid[i]
                if not owed or b['key'] not in collar(rows,bs,i):continue
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
    def witness(name,initial,n,prefix,word,strict,prior=None):
        a=b=initial;pr=[]
        for k,(mode,x) in enumerate(prefix):a,b,r=step(a,b,mode,x,-k-1);pr.append(r)
        ia,ib=a,b;rows=[]
        for k,(mode,x) in enumerate(word):a,b,r=step(a,b,mode,x,k);rows.append(r)
        assert (a,b)==(ia,ib)
        bs=blocks(rows);trials=[scan(rows,bs,c) for c in range(len(bs))];good=[t for t in trials if t['accepted']];assert good
        xr=[xr_scan(rows,bs,c) for c in range(len(bs))];oldgood=[t['cut'] for t in xr if t['accepted']]
        assert set(oldgood)<={t['cut'] for t in good}
        chosen=good[0]
        if strict:
            assert not oldgood and chosen['cut']==0
            assert [(r['a'],r['q'],r['delta']) for r in rows[:6]]==[(1,6,4),(3,0,-6),(1,3,1),(1,0,-2),(1,0,-2),(1,0,-2)]
            paying=[p for p in chosen['pools'] if p['loans']]
            assert [(p['payer_occurrence'],[(v['anchor_occurrence'],v['demand_end']-v['demand_start']) for v in p['loans']]) for p in paying]==[(3,[(0,2)]),(4,[(0,2)]),(5,[(2,1)])]
            assert rows[16]['destination_A']==rows[16]['destination_B']
        else:
            normalized=json.loads(json.dumps(rows));assert normalized==prior['full_replay']
            assert oldgood==prior['accepted_cuts']
        A,Q,Z=sum(r['a'] for r in rows),sum(r['q'] for r in rows),sum(r['z'] for r in rows)
        compact=[dict(cut=t['cut'],accepted=t['accepted'],unpaid=t['unpaid'],unpaid_excess=t['unpaid_excess'],
          transfers=[[p['payer_occurrence'],v['anchor_occurrence'],v['demand_start'],v['demand_end'],v['credit_start'],v['credit_end']]
            for p in t['pools'] for v in p['loans']]) for t in trials]
        return dict(name=name,strict_split=strict,n=n,initial_diagonal=raw(initial),prefix=prefix,prefix_replay=pr,word=word,
          cycle_initial_A=raw(ia),cycle_initial_B=raw(ib),full_replay=rows,blocks=bs,chosen_cut=chosen['cut'],
          selected_ledger=chosen,cut_trials=compact,accepted_cuts=[t['cut'] for t in good],old_XR_trials=xr,old_XR_accepted_cuts=oldgood,
          alternative_assignment_checks=sum(len(t['credit_assignments']) for t in good),A=A,Q_B=Q,Z_B=Z,weight=2*A-Q,
          KEEP_support=sorted({r['key'] for r in rows if r['mode']=='K'}),actual_pair_closure=True)
    n=13;prefix=[['D',13],['D',12]]
    word=([['K',13],['D',11],['K',12],['K',2],['D',1],['D',2]]+[['K',k] for k in range(3,14)]+
      [['K',k] for k in range(1,14)]+[['K',k] for k in range(12,0,-1)]+[['D',13],['D',12]])
    assert len(word)==44
    new=witness('cross_run_essential_split',s.vine(n),n,prefix,word,True)
    reflection=witness('cross_run_essential_split_reflection',mirror(s.vine(n),n),n,
      [[m,n+1-x] for m,x in prefix],[[m,n+1-x] for m,x in word],True)
    old=json.loads((OLD/'cross_run_shallow_certificate.json').read_text(encoding='utf-8'))
    controls=[witness('preserved_'+w['name'],tup(w['initial_diagonal']),w['n'],w['prefix'],w['word'],False,w) for w in old['witnesses']]
    cert=dict(schema='one-period-retained-fact-split-shallow-v1',date='2026-10-31',witnesses=[new,reflection]+controls,
      finite_fits=0,size_sweeps=0,word_searches=0,source_graph_searches=0,allocation_optimizer_used=False,
      matching_terminal_line='FROZEN',universal_CD='OPEN',all_cut_trials_are_alternative_one_period_passes=True)
    save('split_shallow_certificate.json',cert)
    print(json.dumps(dict(preserved_files=len(pins),stage_files=len(stage),witnesses=[dict(name=w['name'],length=len(w['word']),
      A=w['A'],Q_B=w['Q_B'],Z_B=w['Z_B'],weight=w['weight'],accepted_cuts=len(w['accepted_cuts']),old_XR_cuts=len(w['old_XR_accepted_cuts'])) for w in cert['witnesses']]),indent=2))

if __name__=='__main__':main()
