"""One restricted charging theorem, a fixed closed witness and exact credit certificate."""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PARENT = HERE.parent
STAGE = ROOT / 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,indent=2,ensure_ascii=False);f.write('\n')

def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()

def main():
    inherited = json.loads((PARENT/'route_c_full_form_obstruction_audit_20261031_v001/entry_source_pins.json').read_text(encoding='utf-8'))
    pins = dict(inherited['files'])
    for rel,value in pins.items():
        assert sha(ROOT/rel) == value,rel
    for p in PARENT.rglob('*'):
        if p.is_file() and HERE not in p.parents:
            pins[p.relative_to(ROOT).as_posix()] = sha(p)
    definitions = [
      '26AJ_direct_coarse_double_repayment.md','26AK_delayed_coarse_double_repayment.md',
      '26AL_generalized_signed_repayment.md','26AM_two_splay_signed_repayment.md',
      '26AN_double_positive_packet_repayment.md','26AO_order_expanded_double_positive_repayment.md',
      '26AP_variable_length_bulk_repayment.md','26AQ_shallow_bridge_cross_run_repayment.md',
      '26AR_essential_split_sink_allocation.md','26AS_source_derived_shared_credit_allocation.md',
      'DIRECT_NFKS_RT2_three_keep_key_coarse_double.md','DIRECT_CD_K4_four_keep_key_coarse_double.md',
      'DIRECT_CDK5_LOW_five_key_submaximal_core.md']
    for name in definitions:
        rel = 'DO_RESEARCH_REBOOT/02_PROVED/'+name
        pins[rel] = sha(ROOT/rel)
    stage = {p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert len(stage) == 125
    status=git('status','--porcelain=v1','--untracked-files=no');assert not status
    save('entry_source_pins.json',dict(date='2026-10-31',head=git('rev-parse','HEAD'),
         branch=git('branch','--show-current'),tracked_status=status,files=pins,
         stage_files=stage,inherited_pins=len(inherited['files']),
         banked_definition_files=definitions))
    spec=importlib.util.spec_from_file_location('tuple_source',ROOT/'python/independent/splay.py')
    s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
    L=s.LEAF
    def raw(t):
        return None if t==L else [t[1],raw(t[2]),raw(t[3])]
    def tup(t):
        return L if t is None else s.node(t[0],tup(t[1]),tup(t[2]))
    def mirror(t,n):
        return L if t==L else s.node(n+1-t[1],mirror(t[3],n),mirror(t[2],n))
    def step(a,b,mode,x):
        ap,ae=s.trace(a,x);da=s.lookup(a,x)[1]
        if mode=='K':
            bp,be=s.trace(b,x);db=s.lookup(b,x)[1]
        else:
            bp,be,db=b,[],None
        q=sum(e[0]!='ZIG' for e in be);z=sum(e[0]=='ZIG' for e in be)
        assert len(ae)==(da+1)//2 and q==(db//2 if db is not None else 0)
        assert z==(db%2 if db is not None else 0)
        row=dict(mode=mode,key=x,source_A=raw(a),source_B=raw(b),destination_A=raw(ap),
                 destination_B=raw(bp),d_A=da,d_B=db,a=len(ae),q=q,z=z,
                 A_events=ae,B_events=be,delta=q-2*len(ae))
        return ap,bp,row
    def block_data(rows):
        n=len(rows);leaders=[i for i,r in enumerate(rows) if r['a']>0]
        if not leaders:
            assert sum(r['q'] for r in rows)==0
            return []
        blocks=[]
        for k,i in enumerate(leaders):
            j=leaders[(k+1)%len(leaders)];ids=[i];p=(i+1)%n
            while p!=j:
                ids.append(p);p=(p+1)%n
            x=rows[i]['key'];ac=rows[i]['a']
            assert all(rows[t]['key']==x and rows[t]['a']==0 for t in ids[1:])
            active=[t for t in ids if rows[t]['mode']=='K' and rows[t]['d_B']>0]
            assert len(active)<=1
            q=sum(rows[t]['q'] for t in ids)
            blocks.append(dict(leader=i,key=x,indices=ids,a=ac,q=q,delta=q-2*ac,
                               B_active_access=active[0] if active else None))
        return blocks
    def recognize(rows):
        bs=block_data(rows);pairs=[]
        for i,block in enumerate(bs):
            if block['delta']<=0:
                continue
            j=(i+1)%len(bs);other=bs[j];at=block['B_active_access']
            assert at is not None
            before=tup(rows[at]['source_B']);after=tup(rows[at]['destination_B'])
            d=s.lookup(before,other['key'])[1];dp=s.lookup(after,other['key'])[1]
            ok=d<=1 and block['delta']<=2*other['a']-1
            if not ok:
                return False,bs,pairs
            assert dp<=3 and other['q']<=1 and other['delta']<=1-2*other['a']<0
            pairs.append(dict(positive=i,successor=j,successor_key=other['key'],
                              pre_positive_B_depth=d,post_positive_B_depth=dp,
                              former_B_root=before[1],capacity_bound=2*other['a']-1,
                              pair_delta=block['delta']+other['delta']))
        used=[z for pair in pairs for z in (pair['positive'],pair['successor'])]
        assert len(used)==len(set(used))
        return True,bs,pairs
    def assign(rows,bs,pairs):
        credits={i:[[b['leader'],ev,slot] for ev in range(b['a']) for slot in (0,1)]
                 for i,b in enumerate(bs)}
        demands={i:[[at,ev] for at in b['indices'] for ev,e in enumerate(rows[at]['B_events']) if e[0]!='ZIG']
                 for i,b in enumerate(bs)}
        assignments=[];paid=set()
        for pair in pairs:
            i,j=pair['positive'],pair['successor'];paid.update((i,j))
            local=2*bs[i]['a'];excess=bs[i]['delta']
            for d,cr in zip(demands[i][:local],credits[i]):
                assignments.append(dict(demand=d,credit=cr,kind='positive_local',block=i))
            for d,cr in zip(demands[i][local:],credits[j][:excess]):
                assignments.append(dict(demand=d,credit=cr,kind='successor_transfer',block=i))
            for d,cr in zip(demands[j],credits[j][excess:]):
                assignments.append(dict(demand=d,credit=cr,kind='successor_local',block=j))
        for i,b in enumerate(bs):
            if i in paid:
                continue
            assert b['delta']<=0
            for d,cr in zip(demands[i],credits[i]):
                assignments.append(dict(demand=d,credit=cr,kind='singleton_local',block=i))
        all_demands=[d for ds in demands.values() for d in ds]
        assert len(assignments)==len(all_demands)==sum(r['q'] for r in rows)
        assert len({tuple(v['demand']) for v in assignments})==len(assignments)
        assert len({tuple(v['credit']) for v in assignments})==len(assignments)
        return assignments
    def witness(name,initial,prefix,word):
        a=b=initial;pr=[]
        for mode,x in prefix:
            a,b,row=step(a,b,mode,x);pr.append(row)
        ia,ib=a,b;rows=[]
        for mode,x in word:
            a,b,row=step(a,b,mode,x);rows.append(row)
        assert (a,b)==(ia,ib)
        ok,bs,pairs=recognize(rows);assert ok
        assert len(pairs)==1 and pairs[0]['positive']==0
        assert rows[0]['a']==1 and rows[0]['q']==3 and rows[0]['delta']==1
        assert rows[1]['destination_A']==rows[1]['destination_B']
        assignments=assign(rows,bs,pairs)
        cuts=[]
        for cut in range(len(rows)):
            rr=rows[cut:]+rows[:cut];accepted,bb,pp=recognize(rr)
            assert accepted
            aa=assign(rr,bb,pp)
            cuts.append(dict(cut=cut,accepted=accepted,positive_blocks=len(pp),charged_demands=len(aa)))
        pair=pairs[0];r=pair['former_B_root']
        successor_keys=[bs[j%len(bs)]['key'] for j in (1,2,3)]
        first_return=next(j for j in range(1,len(bs)) if bs[j]['key']==r)
        novel=dict(KEEP_support=sorted({r['key'] for r in rows if r['mode']=='K'}),
                   positive_blocks=[i for i,b in enumerate(bs) if b['delta']>0],
                   positive_run_lengths=[1],former_root=r,next_three_keys=successor_keys,
                   first_former_root_return_offset=first_return,
                   AJ_exclusion='immediate successor is not former root',
                   AK_AL_exclusion='second successor is not former root',
                   AM_exclusion='third successor is not former root',
                   AN_AO_exclusion='only one positive; every packet requires two distinct positives',
                   AP_exclusion='unit run length 1; next key is not former root',
                   AQ_AR_AS_exclusion='insufficient positive runs for bridge/split/shared components; direct AP also fails',
                   support_le_5_classes_exclusion='seven genuine KEEP keys')
        assert all(k!=r for k in successor_keys) and first_return>3
        A=sum(v['a'] for v in rows);Q=sum(v['q'] for v in rows);Z=sum(v['z'] for v in rows)
        assert Q<=2*A and len(assignments)==Q
        return dict(name=name,n=7,initial_diagonal=raw(initial),prefix=prefix,prefix_replay=pr,
                    cycle_initial_A=raw(ia),cycle_initial_B=raw(ib),word=word,full_replay=rows,
                    A=A,Q_B=Q,Z_B=Z,weight=2*A-Q,actual_pair_closure=True,
                    blocks=bs,charging_pairs=pairs,credit_assignments=assignments,
                    unused_credit_count=2*A-Q,all_cuts=cuts,novelty=novel,
                    synchronized_after_cycle_access=1)
    initial=s.vine(7);prefix=[['D',7],['D',6]]
    word=([['K',7],['K',2]]+[['K',k] for k in range(3,8)]+
          [['K',k] for k in range(1,8)]+[['K',k] for k in range(6,0,-1)]+[['D',7],['D',6]])
    assert len(word)==22
    original=witness('old_child_successor',initial,prefix,word)
    reflected=witness('old_child_successor_reflection',mirror(initial,7),
                      [[m,8-x] for m,x in prefix],[[m,8-x] for m,x in word])
    sharp=[]
    for mirrored in (False,True):
        t=s.vine(4);x=4;y=2
        if mirrored:
            t=mirror(t,4);x=1;y=3
        tt,ev=s.trace(t,x);d=s.lookup(t,y)[1];dd=s.lookup(tt,y)[1]
        assert (d,dd)==(1,3)
        sharp.append(dict(tree=raw(t),target=x,tracked=y,tree_after=raw(tt),events=ev,
                          depth_before=d,depth_after=dd,return_q=dd//2))
    cert=dict(schema='shallow-successor-restricted-charging-v1',date='2026-10-31',
              witnesses=[original,reflected],sharp_transport_controls=sharp,
              fixed_witness_searches=0,finite_fits=0,larger_finite_sizes=0,
              matching_terminal_line='FROZEN',universal_CD='OPEN',
              restricted_class='all positive blocks have pre-B-depth<=1 successor and delta<=2a_successor-1')
    save('shallow_successor_certificate.json',cert)
    print(json.dumps(dict(preserved_files=len(pins),stage_files=len(stage),
         controls=[dict(name=w['name'],prefix=len(w['prefix']),cycle=len(w['word']),blocks=len(w['blocks']),
                       A=w['A'],Q_B=w['Q_B'],Z_B=w['Z_B'],weight=w['weight'],
                       assignments=len(w['credit_assignments']),pair=w['charging_pairs'][0],
                       next_three_keys=w['novelty']['next_three_keys']) for w in cert['witnesses']]),indent=2))

if __name__=='__main__':
    main()
