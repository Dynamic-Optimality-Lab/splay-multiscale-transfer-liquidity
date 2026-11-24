"""Independent exact original-event checks of the two failed credit invariants."""
import sys
import json
from pathlib import Path
sys.dont_write_bytecode=True
from verify import V,read,priorities,nodes
HERE=Path(__file__).resolve().parent


def rotate(t,promoted,demoted):
    frames=[];cur=t
    while cur.k!=demoted:
        if demoted<cur.k:frames.append((cur.k,'L',cur.r));cur=cur.l
        else:frames.append((cur.k,'R',cur.l));cur=cur.r
        assert cur is not None
    if promoted<demoted:assert cur.l.k==promoted;cur=V.V.right(cur)
    else:assert cur.r.k==promoted;cur=V.V.left(cur)
    for key,side,sibling in reversed(frames):cur=V.V.node(key,cur,sibling) if side=='L' else V.V.node(key,sibling,cur)
    return cur


def forest(t,bank,owner,cross):
    return {(v.k,c.k,side) for v in nodes(t) if bank[owner[v.k]]==0
            for side,c in enumerate((v.l,v.r)) if c is not None and bank[owner[c.k]]==0
            and (not cross or owner[v.k]!=owner[c.k])}


def check(name,cross):
    result=read(name);assert result['status']=='REFUTED_EXACT_ORIGINAL_PHYSICAL_INVARIANT'
    counter=result['counterexample'];z=read(counter['complete_trace']);saved=read(counter['complete_policy'])
    tape,stats=V.physical(z);events=priorities(z,tape);stock=saved['initial_greatest_fixed_point'].copy()
    trees={a:V.immutable(z['source']['initial_'+a]) for a in ('A','B')}
    owner={k:i for i,block in enumerate(z['blocks']) for k in block};steps={tuple(s['id']):s for s in z['steps']}
    assert forest(trees['A'],stock,owner,cross)==forest(trees['B'],stock,owner,cross)
    for index,((e,order),row) in enumerate(zip(events,saved['rows'])):
        assert e['id']==row['id'] and row['priority']==order
        if e['id'][0] in ('A','B'):
            for b in steps[tuple(e['id'])]['bits']:trees[e['id'][0]]=rotate(trees[e['id'][0]],b['promoted'],b['demoted'])
        mass=sum(stock[b] for b in order)
        if e['a'] or e['k']:after=[5]*len(order);paid=0
        else:paid=min(mass,e['q']);after=[min(5,max(0,mass-paid-5*j)) for j in range(len(order))]
        for b,value in zip(order,after):stock[b]=value
        assert after==row['after'] and paid==row['paid']
        A=forest(trees['A'],stock,owner,cross);B=forest(trees['B'],stock,owner,cross)
        if index<counter['event_index']:assert A==B
        else:
            assert index==counter['event_index'] and e['id']==counter['original_event'] and A!=B
            assert stock==counter['stock']
            assert all(V.raw(trees[a])==counter['snapshots'][a] for a in trees)
            edge=tuple(counter['physical_directed_edge']);present=A if counter['edge_present_only_in']=='A' else B;absent=B if counter['edge_present_only_in']=='A' else A
            assert edge in present and edge not in absent
            assert stock[owner[edge[0]]]==stock[owner[edge[1]]]==0
            assert not cross or owner[edge[0]]!=owner[edge[1]]
            assert e['q']==paid==1 and row['unpaid']==0
            return {'candidate':result['candidate'],'original_event':e['id'],'physical_edge':list(edge),
                'owner_banks':[owner[edge[0]],owner[edge[1]]],'owner_stocks':[0,0],
                'event_fully_paid':True,'full_original_source_verified':True,'all_prior_boundaries_satisfied':True,
                'all_closed_balances_scope':'A zero coordinate at the greatest clipped cyclic balance is zero at every smaller closed balance; the physical edge discrepancy is independent of balances.',
                'new_UF_escape_claim':False,'original_operations':stats['operations']}
    raise AssertionError('Missing counterevent.')


def main():
    cases=[check('ZERO_EDGE_INVARIANT_RESULT.json',False),check('CROSS_BLOCK_ZERO_EDGE_RESULT.json',True)]
    result={'passed':True,'cases':cases,'selected_H5_bank_refuted':False,'universal_CD':'OPEN',
        'scope':'Two stated physical state-invariant candidates refuted on the same complete original source. This is not a failed funded guard or an aggregate-cost counterexample.'}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        p=HERE/'ZERO_EDGE_INDEPENDENT_VERIFICATION.json'
        if p.exists():assert json.loads(p.read_text())==result
        else:p.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'passed':True,'counterevents':[r['original_event'] for r in cases],'bank_funding_refuted':False,'universal_CD':'OPEN'}))


if __name__=='__main__':main()
