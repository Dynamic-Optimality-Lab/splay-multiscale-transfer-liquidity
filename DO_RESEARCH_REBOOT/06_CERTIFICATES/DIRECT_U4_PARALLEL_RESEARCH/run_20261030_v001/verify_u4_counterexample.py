"""Exact physical Pair Access counterexample to original U4-M, not to Coarse-Double.

Run from repository root with python -B. Creates one new JSON beside this script.
Pointer replay, independent frame replay, original instrumentation, original matching,
and one-period cyclic neighborhoods are all checked separately.
"""
from pathlib import Path
import sys, json, hashlib, copy, itertools
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
sys.path[:0] = [str(ROOT/'python'), str(ROOT/'scripts')]
from liquidity import legacy_embedding as P
from independent import splay as S
import wp6_overflow as O

def require(condition, detail):
    if not condition:
        raise AssertionError(detail)

def enc(t):
    return None if t is None else [t['k'],enc(t['l']),enc(t['r'])]

def dec(t):
    return S.LEAF if t is None else S.node(t[0],dec(t[1]),dec(t[2]))

def serial(t):
    return None if t == S.LEAF else [t[1],serial(t[2]),serial(t[3])]

def vine(n):
    t = None
    for k in range(n,0,-1):
        t = [k,None,t]
    return t

def word(n):
    return [('D',n-1),('D',n),('K',n)]+[(m,x) for x in range(n-1,0,-1) for m in ('D','K')]

def replay_both(t0,w):
    pa,pb=O.to_ptr(t0),O.to_ptr(t0)
    ta,tb=dec(t0),dec(t0)
    rows=[]
    for i,(m,x) in enumerate(w):
        beforeA,beforeB=enc(pa),enc(pb)
        da=P._depth_to(pa,x)[0];db=P._depth_to(pb,x)[0] if m=='K' else None
        require(S.lookup(ta,x)==(True,da),('A depth',i))
        pa,ea=P.splay_trace(pa,x);ta,et=S.trace(ta,x)
        require([(e['case'],e['lo'],e['hi'],e['orient']) for e in ea]==et,('A events',i))
        eb=[]
        if m=='K':
            require(S.lookup(tb,x)==(True,db),('B depth',i))
            pb,eb=P.splay_trace(pb,x);tb,eu=S.trace(tb,x)
            require([(e['case'],e['lo'],e['hi'],e['orient']) for e in eb]==eu,('B events',i))
        require(enc(pa)==serial(ta) and enc(pb)==serial(tb),('full states',i))
        a=len(ea);q=sum(e['case']!='ZIG' for e in eb);z=sum(e['case']=='ZIG' for e in eb)
        require(a==(da+1)//2 and (m!='K' or (q==db//2 and z==db%2)),('cost formulas',i))
        rows.append({'access':i,'mode':m,'key':x,'source_A':beforeA,'source_B':beforeB,
                     'destination_A':enc(pa),'destination_B':enc(pb),'dA':da,'dB':db,
                     'a':a,'q':q,'z':z,'A_events':ea,'B_events':eb})
    require(enc(pa)==t0 and enc(pb)==t0,'paired closure')
    return rows

def credits(rows):
    return [[i,j,c] for i,r in enumerate(rows) for j in range(r['a']) for c in (0,1)]

def cyclic_graph(t0,w,laps=3):
    m=len(w);rep=O.replay(t0,t0,w*laps)
    require(rep['endA']==t0 and rep['endB']==t0,'instrumented closure')
    lower=(laps-1)*m
    demands=copy.deepcopy([d for d in O.creators(rep) if lower<=d['acc']<lower+m])
    rows=copy.deepcopy(rep['accesses'][lower:lower+m])
    for r in rows:
        r['idx']%=m
        if r['setup'] is not None:r['setup']%=m
    for d in demands:
        require(d['creator'] is not None and not d['genesis'],'cyclic creator exists')
        d['acc']%=m;d['creator']%=m
        require(rows[d['creator']]['m']=='K','creator must be KEEP')
        require(rows[d['creator']]['a']==0,'all creator pools empty')
    charge=O.charge({'accesses':rows},copy.deepcopy(demands))
    allcredits=credits(rows)
    pools={i:{j for j,c in enumerate(allcredits) if c[0]==i} for i in range(m)}
    adj=[]
    for d in demands:
        t=d['acc'];s=rows[t]['setup'];c=d['creator']
        neigh=pools[t]|pools[c]|(pools[s] if s is not None else set())
        adj.append(sorted(neigh))
        d['setup']=s;d['eligible_credit_ids']=sorted(neigh)
        d['eligible_units']=[allcredits[j] for j in sorted(neigh)]
    size,mtL,mtR=O.kuhn_match(len(demands),len(allcredits),adj)
    require(size==charge['matched'],'independent neighborhood vs charge')
    xset=[j for j,d in enumerate(demands) if d['acc']==2]
    neighborhood=sorted(set().union(*(set(adj[j]) for j in xset)))
    require(len(xset)==3 and len(neighborhood)==2,'three demands two neighbors')
    for k in (1,2):
        for sub in itertools.combinations(xset,k):
            require(len(set().union(*(set(adj[j]) for j in sub)))>=k,'minimal Hall subset')
    require(size==5 and len(demands)==6 and len(allcredits)==22,'full matching counts')
    return {'demands':demands,'credit_units':allcredits,'adjacency':adj,'matched':size,
            'original_charge':charge,'matching_left_to_credit':mtL,
            'minimal_Hall_X':xset,'complete_Hall_neighborhood_ids':neighborhood,
            'complete_Hall_neighborhood_units':[allcredits[j] for j in neighborhood],
            'deficiency':len(xset)-len(neighborhood),'period_accesses':m,'context_laps':laps,
            'credits_counted_once':True}

def main():
    target=OUT/'u4_counterexample_certificate.json'
    require(not target.exists(),'append-only output already exists')
    t0=vine(7);w=word(7);rows=replay_both(t0,w)
    graphs=[cyclic_graph(t0,w,laps) for laps in (2,3,4)]
    for g in graphs[1:]:
        for key in ('demands','credit_units','adjacency','matched','minimal_Hall_X','complete_Hall_neighborhood_units'):
            require(g[key]==graphs[0][key],('periodic stability',key))
    A=sum(r['a'] for r in rows);Q=sum(r['q'] for r in rows);Z=sum(r['z'] for r in rows)
    require((A,Q,Z)==(11,6,4),'aggregate costs')
    family=[]
    for n in range(2,65):
        for mirrored in (False,True):
            base=vine(n);ww=word(n)
            if mirrored:
                def mirror(t):
                    return None if t is None else [n+1-t[0],mirror(t[2]),mirror(t[1])]
                base=mirror(base);ww=[(m,n+1-x) for m,x in ww]
            rr=replay_both(base,ww)
            require(all(r['a']==0 for r in rr if r['mode']=='K'),'family starved KEEPs')
            require(rr[1]['a']==1 and rr[2]['q']==(n-1)//2,'family setup and demand')
            family.append({'n':n,'mirrored':mirrored,'A':sum(r['a'] for r in rr),
                           'Q':sum(r['q'] for r in rr),'distinguished_q':rr[2]['q'],
                           'distinguished_eligible_credits':2,'full_accesses':len(ww),'paired_closure':True})
    doubled=replay_both(t0,w*2)
    require(sum(r['a'] for r in doubled)==22 and sum(r['q'] for r in doubled)==12,'nonprimitive accounting')
    source_paths=['python/liquidity/legacy_embedding.py','python/independent/splay.py','scripts/wp6_overflow.py']
    result={'status':'EXACT_COUNTEREXAMPLE_FOUND','target_refuted':'original U4-M local/creator/consumer-setup matching',
            'CD_U_refuted':False,'repository_head':'fea2a25b05e97f726b6e1891cebb12c4cfca821a',
            'source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in source_paths},
            'initial_A':t0,'initial_B':t0,'initial_state_diagonal':True,'reachability_prefix':[],
            'word':w,'full_state_replay':rows,'A':A,'Q_B':Q,'Z_B':Z,'B':Q+Z,'Q_minus_2A':Q-2*A,
            'R':sum(max(r['q']-2*r['a'],0) for r in rows),
            'S':sum(max(2*r['a']-r['q'],0) for r in rows),
            'closure_A':rows[-1]['destination_A']==t0,'closure_B':rows[-1]['destination_B']==t0,
            'cyclic_graph':graphs[1],'periodic_context_stability_laps':[2,3,4],
            'all_KEEP_A_costs_zero':True,'nonstarved_KEEP_competitor_exists':False,
            'family_controls':family,'family_control_count':len(family),
            'nonprimitive_two_periods':{'A':22,'Q_B':12,'paired_closure':True},
            'scope':'One exact seven-key original-source witness; finite family checks support a separate all-n construction proof. No Coarse-Double counterexample or fixed-support Stage11G claim.'}
    with target.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:result[k] for k in ('status','target_refuted','A','Q_B','Z_B','Q_minus_2A','family_control_count')},indent=2))
    print(json.dumps({'Hall_X':graphs[1]['minimal_Hall_X'],'neighborhood':graphs[1]['complete_Hall_neighborhood_units'],'matched':5,'demand':6},indent=2))

if __name__=='__main__':main()
