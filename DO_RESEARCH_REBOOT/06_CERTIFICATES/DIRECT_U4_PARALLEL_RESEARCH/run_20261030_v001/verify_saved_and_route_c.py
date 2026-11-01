"""Independent saved-witness check: tuple engine, cyclic setups, exhaustive Hall subsets.

No original genealogy or matching implementation is used here. Every possible
creator is a KEEP; all KEEP credits are zero, so creator identity cannot affect
the neighborhood. This verifies the counterexample even if ancestry is refined.
"""
from pathlib import Path
import sys,json,itertools,hashlib
from functools import lru_cache
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/'python'))
from independent import splay as S

def ck(x,msg):
    if not x:raise AssertionError(msg)

def dec(t):return S.LEAF if t is None else S.node(t[0],dec(t[1]),dec(t[2]))
def enc(t):return None if t==S.LEAF else [t[1],enc(t[2]),enc(t[3])]

def main():
    output=OUT/'independent_witness_and_route_c.json'
    ck(not output.exists(),'append-only output')
    path=OUT/'u4_counterexample_certificate.json';c=json.loads(path.read_text())
    w=c['word'];rows=c['full_state_replay'];m=len(w)
    a=dec(c['initial_A']);b=dec(c['initial_B']);A=Q=Z=0
    for i,((mode,x),r) in enumerate(zip(w,rows)):
        ck((enc(a),enc(b))==(r['source_A'],r['source_B']),('source',i))
        da=S.lookup(a,x)[1];a,ae=S.trace(a,x)
        db=S.lookup(b,x)[1] if mode=='K' else None
        if mode=='K':b,be=S.trace(b,x)
        else:be=[]
        av=len(ae);qv=sum(e[0]!='ZIG' for e in be);zv=sum(e[0]=='ZIG' for e in be)
        ck((da,db,av,qv,zv)==(r['dA'],r['dB'],r['a'],r['q'],r['z']),('cost',i))
        ck((enc(a),enc(b))==(r['destination_A'],r['destination_B']),('destination',i))
        ck(mode!='K' or av==0,'every KEEP starved')
        A+=av;Q+=qv;Z+=zv
    ck(enc(a)==c['initial_A'] and enc(b)==c['initial_B'],'exact closure')
    g=c['cyclic_graph'];units=g['credit_units'];adj=[]
    for d in g['demands']:
        t=d['acc'];x=w[t][1]
        previous=[(t-j)%m for j in range(1,m+1) if w[(t-j)%m][1]==x and rows[(t-j)%m]['a']>0]
        ck(previous,'setup exists');setup=previous[0]
        ck(w[setup][0]=='D','DELETE setup')
        # Local and every possible creator pool are empty: no provenance choice can add credit.
        neighborhood=[j for j,u in enumerate(units) if u[0]==setup]
        ck(neighborhood==d['eligible_credit_ids'],'complete independent neighborhood')
        adj.append(neighborhood)
    deficits=[]
    for mask in range(1<<len(adj)):
        subset=[j for j in range(len(adj)) if mask>>j&1]
        neigh=set().union(*(set(adj[j]) for j in subset)) if subset else set()
        deficits.append((len(subset)-len(neigh),subset,sorted(neigh)))
    maximum=max(x[0] for x in deficits)
    hallX=[j for j,d in enumerate(g['demands']) if d['acc']==2]
    ck(maximum==1 and len(hallX)==3,'Hall deficiency')
    for defect,subset,neigh in deficits:
        if set(subset)<set(hallX):ck(defect<=0,'inclusion minimality')
    @lru_cache(None)
    def maximum_matching(j,used):
        if j==len(adj):return 0
        return max([maximum_matching(j+1,used)]+[1+maximum_matching(j+1,used|(1<<v)) for v in adj[j] if not used>>v&1])
    ck(maximum_matching(0,0)==5,'independent exhaustive matching')
    # A closed physical source witness disproving direct B-only transition potentials.
    t0=S.vine(3);a=b=t0;small=[]
    for mode,x in [('D',3),('K',3),('D',1),('K',1)]:
        before=enc(b);da=S.lookup(a,x)[1];a,ae=S.trace(a,x)
        db=S.lookup(b,x)[1] if mode=='K' else None
        if mode=='K':b,be=S.trace(b,x)
        else:be=[]
        small.append({'mode':mode,'key':x,'dA':da,'dB':db,'a':len(ae),
                      'q':sum(e[0]!='ZIG' for e in be),'B_source':before,'B_destination':enc(b)})
    ck(a==b==t0,'three-key closure')
    ck(sum(r['q'] for r in small if r['mode']=='K')==2 and all(r['a']==0 for r in small if r['mode']=='K'),'B-only contradiction')
    result={'status':'PASS','source_certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'source_replay_accesses':m,'Hall_subsets_exhausted':len(deficits),
            'maximum_Hall_deficiency':maximum,'matching_size_independent_exhaustive':5,
            'costs':{'A':A,'Q_B':Q,'Z_B':Z,'Q_minus_2A':Q-2*A},
            'creator_identity_not_assumed':'all B mutation creators are KEEPs; every KEEP has zero A credit',
            'original_neighborhood_preserved':True,'B_only_potential_counterexample':small,
            'bounded_range_necessary_condition':'For n-family K_n, Psi(source)-Psi(destination)>=floor((n-1)/2); hence no range bound independent of n covers all raw accesses.',
            'does_not_refute_macro_potential':True,'general_Route_C':'OPEN',
            'new_universal_CD_proof':False}
    with output.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='B_only_potential_counterexample'},indent=2))

if __name__=='__main__':main()
