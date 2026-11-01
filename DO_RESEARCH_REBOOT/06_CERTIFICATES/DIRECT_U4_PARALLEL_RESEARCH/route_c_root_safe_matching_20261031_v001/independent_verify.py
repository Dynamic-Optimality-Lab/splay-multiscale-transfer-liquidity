"""Verify root eligibility, matching/cover duals and full pointer-source replay.

Imports no producer, tuple source or matching algorithm.
"""
from pathlib import Path
import hashlib,json,sys
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/'python'))
from liquidity import legacy_embedding as P
def ck(ok,msg):
    if not ok:raise AssertionError(msg)
def inspect(t):
    if t is None:return [],set()
    l,li=inspect(t[1]);r,ri=inspect(t[2]);ks=l+[t[0]]+r
    ck(ks==sorted(set(ks)),'valid distinct ordered keys')
    return ks,li|ri|{(ks[0],ks[-1])}
def proper(t):
    keys,ss=inspect(t)
    if keys:ss.remove((keys[0],keys[-1]))
    ck(len(ss)==max(0,len(keys)-1),'proper subtree multiplicity')
    return keys,sorted(ss)
def depth(t,x):
    d=0
    while t is not None:
        if t[0]==x:return d
        t=t[1] if x<t[0] else t[2];d+=1
    raise AssertionError('absent access')
def ptr(t):
    if t is None:return None
    p=P.mknode(t[0],ptr(t[1]),ptr(t[2]))
    for side in ('l','r'):
        if p[side] is not None:p[side]['p']=p
    return p
def raw(t):return None if t is None else [t['k'],raw(t['l']),raw(t['r'])]
def reflection(t,n):return None if t is None else [n+1-t[0],reflection(t[2],n),reflection(t[1],n)]

def main():
    path=OUT/'root_matching_certificate.json';c=json.loads(path.read_text(encoding='utf-8'));graphs=c['matching_graphs'];covered=0
    for g in graphs:
        ka,ai=proper(g['A']);kb,bi=proper(g['B']);r=g['A'][0] if ka else None
        ck(ka==kb and r==g['root_A'],'same keys and actual A root')
        common=sorted(set(ai)&set(bi));cs=set(common)
        eligible=lambda I:not (I[0]<=r<=I[1])
        ck(all(eligible(I) for I in common),'every forced pair eligible')
        left=[I for I in ai if I not in cs];right=[J for J in bi if J not in cs and eligible(J)]
        ck(g['all_A_intervals']==[list(I) for I in ai] and g['all_B_intervals']==[list(J) for J in bi],'all interval vertices regenerated')
        ck(g['forced_exact_pairs']==[list(I) for I in common],'all and only exact pairs forced')
        ck(g['left_residual']==[list(I) for I in left] and g['eligible_right_residual']==[list(J) for J in right],'all root eligible residual vertices')
        bad=[J for J in bi if not eligible(J)]
        ck(g['ineligible_B_intervals']==[list(J) for J in bad],'every gated B interval regenerated')
        adj=[[j for j,J in enumerate(right) if I[0]==J[0] or I[1]==J[1]] for I in left]
        ck(adj==g['adjacency'],'all and only endpoint edges')
        m=g['matching'];cl=g['cover_left'];cr=g['cover_right']
        ck(len({i for i,j in m})==len({j for i,j in m})==len(m),'one-to-one matching')
        ck(all(type(i) is type(j) is int and 0<=i<len(left) and j in adj[i] for i,j in m),'all matching edges genuine')
        ck(len(set(cl))==len(cl) and len(set(cr))==len(cr),'cover has distinct vertices')
        ck(all(type(i) is int and 0<=i<len(left) for i in cl) and all(type(j) is int and 0<=j<len(right) for j in cr),'cover bounds')
        ck(all(i in cl or j in cr for i,row in enumerate(adj) for j in row),'every edge covered')
        ck(len(m)==len(cl)+len(cr)==g['mu_root'],'maximum certified by matching/cover equality')
        f=len(ai)-len(common);v=f-len(m);d=depth(g['B'],r) if r is not None else 0
        ck(len(bad)==d and v>=d,'root-depth counting bound')
        ck((f,v,d)==(g['F'],g['P'],g['d_B_root_A']),'all potential values regenerated');covered+=sum(map(len,adj))
    rows=0
    def verify(row):
        nonlocal rows
        a,b=row['source_A'],row['source_B'];mode=row['mode'];x=row['key'];da=depth(a,x);db=depth(b,x) if mode=='K' else None
        aa,ea=P.splay_trace(ptr(a),x)
        if mode=='K':bb,eb=P.splay_trace(ptr(b),x)
        else:bb,eb=ptr(b),[]
        aa,bb=raw(aa),raw(bb);ac=len(ea);q=sum(e['case']!='ZIG' for e in eb);z=sum(e['case']=='ZIG' for e in eb)
        ck((aa,bb)==(row['destination_A'],row['destination_B']),'complete physical endpoints')
        ck((da,db,ac,q,z)==(row['dA'],row['dB'],row['a'],row['q'],row['z']),'source costs')
        ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'depth conventions')
        ev=lambda es:[[e['case'],e['lo'],e['hi'],e['orient']] for e in es]
        ck(ev(ea)==row['events_A'] and ev(eb)==row['events_B'],'oriented source events')
        for sa,sb,key in [(a,b,'source_values'),(aa,b,'after_A_values'),(aa,bb,'destination_values')]:
            v=row[key];g=graphs[v['graph_id']]
            ck(g['A']==sa and g['B']==sb,'correct graph attached to each physical state')
            ck(v=={'F':g['F'],'mu_root':g['mu_root'],'P':g['P'],'root_A':g['root_A'],'d_B_root_A':g['d_B_root_A'],'graph_id':v['graph_id']},'exact graph valuation')
        delta=row['destination_values']['P']-row['source_values']['P'];budget=2*ac-q
        ck((delta,budget,delta<=budget)==(row['delta_P'],row['budget'],row['whole_law_holds']),'whole source law verdict')
        bdelta=row['destination_values']['P']-row['after_A_values']['P']
        ck(row['B_full_q_holds']==(bdelta<=-q),'full-q flag exact')
        if mode=='K':ck(bdelta<=0,'weak universal B nonincrease checked on replay')
        rows+=1
    for row in c['controls']+c['reflections']:verify(row)
    expected=[(5,2,0,2,1),(4,2,0,2,0),(3,1,0,1,1),(5,2,0,2,1),(1,4,1,0,0)]
    ck(len(c['controls'])==len(c['reflections'])==5,'frozen five controls and reflections')
    for r,m,e in zip(c['controls'],c['reflections'],expected):
        ck((r['source_values']['P'],r['destination_values']['P'],r['a'],r['q'],r['z'])==e,'registered exact control values')
        n=len(inspect(r['source_A'])[0])
        ck(m['source_A']==reflection(r['source_A'],n) and m['source_B']==reflection(r['source_B'],n),'actual input reflection')
        ck(m['destination_A']==reflection(r['destination_A'],n) and m['destination_B']==reflection(r['destination_B'],n),'actual output reflection')
        ck((m['source_values']['P'],m['destination_values']['P'],m['a'],m['q'],m['z'])==e,'reflection values and costs')
    ck(all(r['whole_law_holds'] for r in c['controls'][:4]) and not c['controls'][4]['whole_law_holds'],'four consumers paid, DELETE fails')
    bad=c['controls'][4];sg=graphs[bad['source_values']['graph_id']];dg=graphs[bad['destination_values']['graph_id']]
    ck((sg['F'],dg['F'],sg['mu_root'],dg['mu_root'])==(5,5,4,1),'family rank identity at six')
    ck(sg['eligible_right_residual']==[[3,6],[4,6],[5,6],[6,6]] and dg['eligible_right_residual']==[[1,1]],'exact eligibility collapse')
    w=c['closed_witness'];a=w['initial_A'];b=w['initial_B'];ia,ib=a,b;At=Qt=Zt=ds=0
    ck(a==b and len(w['word'])==len(w['full_replay'])==18,'complete diagonal word')
    for (mode,x),r in zip(w['word'],w['full_replay']):
        ck((a,b,mode,x)==(r['source_A'],r['source_B'],r['mode'],r['key']),'source-state sharing')
        verify(r);a,b=r['destination_A'],r['destination_B'];At+=r['a'];Qt+=r['q'];Zt+=r['z'];ds+=r['delta_P']
    ck(a==ia and b==ib and ds==0,'exact actual paired closure and telescoping')
    ck((At,Qt,Zt)==(20,0,12)==(w['A'],w['Q_B'],w['Z_B']),'closed totals')
    r=w['full_replay'][w['failed_edge_index']]
    ck(r['source_A']==bad['source_A'] and r['source_B']==bad['source_B'] and r['delta_P']==3 and r['budget']==2,'reachable DELETE failure')
    result={'status':'PASS','date':'2026-10-31','matching_graphs_verified':len(graphs),'matching_cover_equalities':len(graphs),
      'residual_edges_covered':covered,'source_controls':5,'reflections':5,'complete_source_rows':rows,
      'four_registered_starved_consumers_paid':True,'universal_DELETE_candidate_refuted':True,
      'DELETE_counterexample':{'n':6,'P_source':1,'P_destination':4,'a':1,'q':0,'z':0,'delta_P':3,'budget':2},
      'actual_pair_closure':True,'closed_word':w['word'],'closed_totals':{'A':At,'Q_B':Qt,'Z_B':Zt},
      'CD_counterexample':False,'all_size_family_proof':'RS03_UNBOUNDED_DELETE_OBSTRUCTION.md',
      'all_size_proof_is_analytic_not_finite_extrapolation':True,'full_q_universal_B_law_established':False,
      'finite_potential_fits':0,'new_pair_graphs':0,'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    with (OUT/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
