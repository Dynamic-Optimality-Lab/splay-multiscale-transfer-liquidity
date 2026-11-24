"""Independent geometric checks of the actual refutation certificates."""
import json,time
from pathlib import Path
from collections import Counter
from sharp01_validate import tuple_state,ref
BASE=Path(__file__).resolve().parent

def features(a,b,carrier):
    def data(t):
        aa={};depth={};edges=set();labels=set()
        def visit(t,anc):
            if t==ref.LEAF:return set()
            _,x,l,r=t;aa[x]=set(anc);depth[x]=len(anc)
            for side,c in enumerate((l,r)):
                if c!=ref.LEAF:edges.add((x,c[1],side))
            st=visit(l,anc+[x])|visit(r,anc+[x])|({x} if x in carrier else set())
            if st:labels.add(frozenset(st))
            return st
        visit(t,[]);return aa,depth,edges,labels
    aa,da,ea,la=data(a);ab,db,eb,lb=data(b)
    return dict(edges=len(eb-ea),ancestry=sum(len(ab[x]-aa[x]) for x in aa),SET=len(lb-la),
                depth_sum=sum(max(db[x]-da[x],0) for x in aa),depth_max=max([0]+[db[x]-da[x] for x in aa]))

def main():
    start=time.process_time();idx=json.loads((BASE/'SHARP01_GAP_LEDGER.json').read_text())['ledgers']
    rr=json.loads((BASE/'SHARP01_RESULTS.json').read_text());cache={}
    def ledger(name):
        if name not in cache:cache[name]=json.loads((BASE/next(i['path'] for i in idx if i['name']==name)).read_text())
        return cache[name]
    certificates=[]
    choices={'edges':('H_2_1',2),'ancestry':('W_5_1',41),'SET':('W_5_1',25),'depth_sum':('W_5_1',25),'depth_max':('W_5_1',25)}
    for f,(name,gi) in choices.items():
        l=ledger(name);g=l['gaps'][gi-1];carrier=set(l['summary']['carrier'])
        before=features(*(tuple_state(l['states'][s]) for s in g['start']),carrier)
        after=features(*(tuple_state(l['states'][s]) for s in g['end']),carrier)
        assert before==g['Phi_start'] and after==g['Phi_end']
        delta=before[f]-after[f];assert g['d']>0 and delta<=0
        certificates.append({'template':f,'source':name,'gap_index':gi,'d':g['d'],'Phi_start':before[f],'Phi_end':after[f],
                             'delta':delta,'conclusion':'no nonnegative scalar multiple satisfies every original gap inequality'})
    # Independently replay representative cuts, comparing complete states,
    # cases and costs to the saved original phase at every operation.
    cuts=[]
    selected=['H_6_1','W_5','W_star','G_4_1_L31_r1_z1','lifted_H_4_1_r2','I^3Z','warm_marked_5_1_r3','C15_owner_r7_mirrorFalse','C15_zero_r7_mirrorFalse']
    for name in selected:
        l=ledger(name);ops=l['operations'];cut=len(ops)//3
        if name=='H_6_1':cut=100  # lies inside the initial DELETE run
        st=ops[cut-1]['post'];a,b=(tuple_state(l['states'][s]) for s in st);initial=(a,b);A=Q=0
        for row in ops[cut:]+ops[:cut]:
            x=row['target'];A+=(ref.lookup(a,x)[1]+1)//2;a,ae=ref.trace(a,x)
            if row['tag']=='K':Q+=ref.lookup(b,x)[1]//2;b,be=ref.trace(b,x)
            assert (a,b)==tuple(tuple_state(l['states'][s]) for s in row['post'])
        assert (a,b)==initial and A==l['summary']['A'] and Q==l['summary']['Q']
        cuts.append({'source':name,'cut_after_original_operation':cut,'pass':True})
    # Inspect the exact minimum single-demand deficiency of the first-event rule.
    uu=json.loads((BASE/'SHARP01_PHYSICAL_INCIDENCE.json').read_text())
    s=next(s for s in uu['sources'] if s['source']=='C15_owner_r7_mirrorFalse')
    rule=s['rules']['unit_first_A_recreation'];neighbors=rule['edges']['13']
    assert len(neighbors)==3 and ledger(s['source'])['gaps'][12]['u']==4
    assert all(s['units'][str(j)]['gap_index']==15 for j in neighbors)
    # Reconstruct every primitive ancestry change of this Hall witness with
    # immutable subtrees, then recompute first-return eligibility independently.
    ll=ledger(s['source']);at=tuple_state(ll['source']['initial_A']);bt=tuple_state(ll['source']['initial_B'])
    def pairs(t):
        ans=set()
        def walk(t,above):
            if t==ref.LEAF:return
            _,x,l,r=t;ans.update((v,x) for v in above);walk(l,above+[x]);walk(r,above+[x])
        walk(t,[]);return ans
    def rotate(t,p,side):
        _,x,l,r=t
        if x!=p:
            return ref.node(x,rotate(l,p,side),r) if p<x else ref.node(x,l,rotate(r,p,side))
        child=(l,r)[side];assert child!=ref.LEAF
        _,v,cl,cr=child
        return ref.node(v,cl,ref.node(x,cr,r)) if side==0 else ref.node(v,ref.node(x,l,cl),cr)
    gains={};primitive_count=0
    for ep,e in enumerate(ll['events']):
        old=at if e['id'][0]=='A' else bt;new=rotate(old,e['pivot'],e['side'])
        minus=pairs(old)-pairs(new);plus=pairs(new)-pairs(old)
        assert minus=={(e['ancestry_removed'][0],x) for x in e['ancestry_removed'][1]}
        assert plus=={(e['ancestry_added'][0],x) for x in e['ancestry_added'][1]}
        if e['id'][0]=='A':at=new;gains[ep]=(e['id'],plus)
        else:bt=new
        primitive_count+=1
    assert at==tuple_state(ll['source']['initial_A']) and bt==tuple_state(ll['source']['initial_B'])
    g=ll['gaps'][12];x=g['target'];end=ll['operations'][g['KEEP_operation_id']-1]['event_range'][1]
    first_ids=set()
    for y in g['B_only_ancestors']:
        matches=[ep for ep,(eid,ps) in gains.items() if (y,x) in ps]
        if matches:first_ids.add(tuple(gains[next((ep for ep in matches if ep>=end),matches[0])][0]))
    recomputed=[int(j) for j,unit in s['units'].items() if tuple(unit['rotation_witness']) in first_ids]
    assert set(recomputed)==set(neighbors)
    cert={'status':'PASS','potential_refutations':certificates,'representative_cyclic_replays':cuts,
          'first_restoration_unit_Hall_certificate':{'source':s['source'],'demand_gap':13,'demand':4,'eligible_unit_ids':[s['units'][str(j)]['id'] for j in neighbors],'capacity':3,'deficiency':1},
          'Hall_witness_primitive_ancestry_checks':primitive_count,
          'cpu_seconds':time.process_time()-start,'level':'same agent; separate immutable geometric reconstruction, not formal/external certification'}
    (BASE/'SHARP01_COUNTERCERTIFICATES.json').write_text(json.dumps(cert,indent=2));print(json.dumps(cert))

if __name__=='__main__':main()
