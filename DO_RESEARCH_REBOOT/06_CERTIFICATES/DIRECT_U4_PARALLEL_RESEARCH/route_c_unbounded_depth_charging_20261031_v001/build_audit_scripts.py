"""Write standalone versioned auditors exclusively; never execute/alter old auditors."""
from pathlib import Path

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'route_c_split_shallow_charging_20261031_v001'

def replace_once(source,old,new):
    assert source.count(old)==1,old
    return source.replace(old,new,1)

def save(name,text):
    with (HERE/name).open('x',encoding='utf-8') as f:f.write(text)

source=(OLD/'audit_split_payers.py').read_text(encoding='utf-8')
source=source.replace('route_c_cross_run_shallow_charging_20261031_v001','route_c_split_shallow_charging_20261031_v001')
source=replace_once(source,'assert d<=1 and 1<=h<=3','assert d>=0 and h>=0')
start=source.index('    def xr_scan(');end=source.index('    def scan(',start)
source=source[:start]+source[end:]
source=replace_once(source,'def scan(rows,bs,cut):','def scan(rows,bs,cut,shallow=False):')
source=replace_once(source,"facts=[bound(rows,bs,i,j,b['key']) for i in history if b['key'] in collar(rows,bs,i)]",
  "facts=[bound(rows,bs,i,j,b['key']) for i in history if not shallow or b['key'] in collar(rows,bs,i)]")
source=replace_once(source,"if not owed or b['key'] not in collar(rows,bs,i):continue",
  "if not owed or (shallow and b['key'] not in collar(rows,bs,i)):continue")
source=source[:source.index('    def witness(')]+'''
    def compact(t):
        return dict(cut=t['cut'],accepted=t['accepted'],unpaid=t['unpaid'],unpaid_excess=t['unpaid_excess'],
          transfers=[[p['payer_occurrence'],v['anchor_occurrence'],v['demand_start'],v['demand_end'],v['credit_start'],v['credit_end']]
            for p in t['pools'] for v in p['loans']])
    def witness(name,initial,n,prefix,word,strict,prior=None):
        a=b=initial;pr=[]
        for k,(mode,x) in enumerate(prefix):a,b,r=step(a,b,mode,x,-k-1);pr.append(r)
        ia,ib=a,b;rows=[]
        for k,(mode,x) in enumerate(word):a,b,r=step(a,b,mode,x,k);rows.append(r)
        assert (a,b)==(ia,ib)
        bs=blocks(rows);trials=[scan(rows,bs,c) for c in range(len(bs))];good=[t for t in trials if t['accepted']];assert good
        oldtrials=[scan(rows,bs,c,True) for c in range(len(bs))];oldgood=[t['cut'] for t in oldtrials if t['accepted']]
        assert set(oldgood)<={t['cut'] for t in good}
        chosen=good[0]
        if strict:
            assert not oldgood and chosen['cut']==0
            assert [(r['a'],r['q'],r['delta']) for r in rows[:6]]==[(1,6,4),(3,3,-3),(1,1,-1),(1,1,-1),(3,0,-6),(1,0,-2)]
            assert [i for i,b in enumerate(bs) if b['delta']>0]==[0]
            paying=[p for p in chosen['pools'] if p['loans']]
            assert [(p['payer_occurrence'],[(v['anchor_occurrence'],v['demand_end']-v['demand_start']) for v in p['loans']]) for p in paying]==[(1,[(0,3)]),(4,[(0,1)])]
            deep=paying[0]
            assert deep['facts'][0]['pre_depth']==10 and deep['facts'][0]['h']==7 and deep['facts'][0]['k']==0
            assert (deep['own_q'],deep['ceiling'],deep['capacity'],deep['reservation'])==(3,3,6,3)
            assert rows[16]['destination_A']==rows[16]['destination_B']
        else:
            assert json.loads(json.dumps(rows))==prior['full_replay']
            assert oldgood==prior['accepted_cuts']
            assert [compact(t) for t in oldtrials]==prior['cut_trials']
        A,Q,Z=sum(r['a'] for r in rows),sum(r['q'] for r in rows),sum(r['z'] for r in rows)
        return dict(name=name,strict_beyond_shallow=strict,n=n,initial_diagonal=raw(initial),prefix=prefix,prefix_replay=pr,word=word,
          cycle_initial_A=raw(ia),cycle_initial_B=raw(ib),full_replay=rows,blocks=bs,chosen_cut=chosen['cut'],selected_ledger=chosen,
          cut_trials=[compact(t) for t in trials],accepted_cuts=[t['cut'] for t in good],
          old_SL_trials=[compact(t) for t in oldtrials],old_SL_accepted_cuts=oldgood,
          alternative_assignment_checks=sum(len(t['credit_assignments']) for t in good),
          old_SL_alternative_assignment_checks=sum(len(t['credit_assignments']) for t in oldtrials if t['accepted']),
          A=A,Q_B=Q,Z_B=Z,weight=2*A-Q,KEEP_support=sorted({r['key'] for r in rows if r['mode']=='K'}),actual_pair_closure=True)
    n=13;prefix=[['D',13],['D',12]]
    word=([['K',13],['K',11],['K',12],['K',2],['D',3],['D',2]]+[['K',k] for k in range(3,14)]+
      [['K',k] for k in range(1,14)]+[['K',k] for k in range(12,0,-1)]+[['D',13],['D',12]])
    assert len(word)==44
    new=witness('deep_KEEP_split_payer',s.vine(n),n,prefix,word,True)
    reflection=witness('deep_KEEP_split_payer_reflection',mirror(s.vine(n),n),n,
      [[m,n+1-x] for m,x in prefix],[[m,n+1-x] for m,x in word],True)
    old=json.loads((OLD/'split_shallow_certificate.json').read_text(encoding='utf-8'))
    controls=[witness('preserved_'+w['name'],tup(w['initial_diagonal']),w['n'],w['prefix'],w['word'],False,w) for w in old['witnesses']]
    cert=dict(schema='one-period-arbitrary-key-post-depth-v1',date='2026-10-31',witnesses=[new,reflection]+controls,
      finite_fits=0,size_sweeps=0,word_searches=0,source_graph_searches=0,allocation_optimizer_used=False,
      matching_terminal_line='FROZEN',universal_CD='OPEN',all_cut_trials_are_alternative_one_period_passes=True,
      actual_payer_q_used_as_reservation_oracle=False)
    save('arbitrary_key_certificate.json',cert)
    print(json.dumps(dict(preserved_files=len(pins),stage_files=len(stage),witnesses=[dict(name=w['name'],length=len(w['word']),
      A=w['A'],Q_B=w['Q_B'],Z_B=w['Z_B'],weight=w['weight'],accepted_cuts=len(w['accepted_cuts']),old_SL_cuts=len(w['old_SL_accepted_cuts'])) for w in cert['witnesses']]),indent=2))

if __name__=='__main__':main()
'''
source=source.replace('"""Fixed split-payer construction; tuple source, no search or fitted parameters."""',
  '"""Arbitrary-key split payers from actual post-depths; no search or fit."""')
save('audit_arbitrary_keys.py',source)
