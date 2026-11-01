"""Independent local P duals, one-zig witnesses and full source replay.

No producer, tuple source, matching solver, graph search or metric enumeration.
The global extrema are established analytically in PE02, not by finite testing.
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
    a,ai=inspect(t[1]);b,bi=inspect(t[2]);ks=a+[t[0]]+b
    ck(ks==sorted(set(ks)),'valid ordered distinct keys')
    return ks,ai|bi|{(ks[0],ks[-1])}
def proper(t):
    ks,ss=inspect(t)
    if ks:ss.remove((ks[0],ks[-1]))
    ck(len(ss)==max(0,len(ks)-1),'exact proper subtree multiplicity')
    return ks,sorted(ss)
def ptr(t):
    if t is None:return None
    p=P.mknode(t[0],ptr(t[1]),ptr(t[2]))
    for side in ('l','r'):
        if p[side] is not None:p[side]['p']=p
    return p
def raw(t):return None if t is None else [t['k'],raw(t['l']),raw(t['r'])]
def depth(t,x):
    d=0
    while t is not None:
        if t[0]==x:return d
        t=t[1] if x<t[0] else t[2];d+=1
    raise AssertionError('absent access')
def mirror(t,n):return None if t is None else [n+1-t[0],mirror(t[2],n),mirror(t[1],n)]

def main():
    cp=OUT/'p_envelope_certificate.json';c=json.loads(cp.read_text(encoding='utf-8'));graphs=c['matching_graphs'];covered=0
    ck(len(graphs)==8 and c['n']==6,'frozen eight graphs at n6')
    for g in graphs:
        ka,aa=proper(g['A']);kb,bb=proper(g['B']);r=g['A'][0]
        ck(ka==kb==list(range(1,7)) and r==g['root_A'],'same ranked keys and actual root')
        common=sorted(set(aa)&set(bb));cs=set(common)
        left=[I for I in aa if I not in cs];right=[J for J in bb if J not in cs and not (J[0]<=r<=J[1])]
        ck(g['all_A_intervals']==[list(I) for I in aa] and g['all_B_intervals']==[list(J) for J in bb],'all proper intervals regenerated')
        ck(g['forced_exact_pairs']==[list(I) for I in common] and all(not (I[0]<=r<=I[1]) for I in common),'exact pairs all eligible')
        ck(g['left_residual']==[list(I) for I in left] and g['eligible_right_residual']==[list(J) for J in right],'all eligible residual vertices')
        ck(g['ineligible_B_intervals']==[list(J) for J in bb if J[0]<=r<=J[1]],'all excluded B intervals')
        adj=[[j for j,J in enumerate(right) if I[0]==J[0] or I[1]==J[1]] for I in left]
        ck(g['adjacency']==adj,'every edge and nonedge')
        m=g['matching'];cl=g['cover_left'];cr=g['cover_right']
        ck(len({i for i,j in m})==len({j for i,j in m})==len(m),'disjoint matching endpoints')
        ck(all(type(i) is type(j) is int and 0<=i<len(left) and j in adj[i] for i,j in m),'genuine matching edges')
        ck(len(set(cl))==len(cl) and len(set(cr))==len(cr),'cover distinctness')
        ck(all(type(i) is int and 0<=i<len(left) for i in cl) and all(type(j) is int and 0<=j<len(right) for j in cr),'cover bounds')
        ck(all(i in cl or j in cr for i,row in enumerate(adj) for j in row),'cover every residual edge')
        ck(len(m)==len(cl)+len(cr)==g['mu_root'],'exact maximum by matching-cover duality')
        ck(g['F']==len(aa)-len(common) and g['P']==g['F']-len(m),'P independently computed');covered+=sum(map(len,adj))
    ck([g['P'] for g in graphs]==[1,4,1,5]*2,'four local P values and reflections')
    for g,h in zip(graphs[:4],graphs[4:]):
        ck(h['A']==mirror(g['A'],6) and h['B']==mirror(g['B'],6),'physical graph reflection')
    rows=0
    def verify(r):
        nonlocal rows
        a,b=r['source_A'],r['source_B'];mode=r['mode'];x=r['key'];da=depth(a,x);db=depth(b,x) if mode=='K' else None
        aa,ea=P.splay_trace(ptr(a),x)
        if mode=='K':bb,eb=P.splay_trace(ptr(b),x)
        else:bb,eb=ptr(b),[]
        aa,bb=raw(aa),raw(bb);ac=len(ea);q=sum(e['case']!='ZIG' for e in eb);z=sum(e['case']=='ZIG' for e in eb)
        ck((aa,bb)==(r['destination_A'],r['destination_B']),'full source endpoints')
        ck((da,db,ac,q,z)==(r['dA'],r['dB'],r['a'],r['q'],r['z']),'actual source costs')
        ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'depth/event units')
        ev=lambda es:[[e['case'],e['lo'],e['hi'],e['orient']] for e in es]
        ck(ev(ea)==r['events_A'] and ev(eb)==r['events_B'] and r['budget']==2*ac-q,'all orientations and budget')
        if 'J_source' in r:
            sg,dg=graphs[r['source_graph']],graphs[r['destination_graph']]
            ck((sg['A'],sg['B'],dg['A'],dg['B'])==(a,b,aa,bb),'local P certificate bound to correct control')
            # PE02 proves global upper maxima 4 and 5 for these two B trees;
            # the distance-one attaining auxiliary tree is checked below.
            js=max(sg['P'],4-1)
            jd=dg['P'] if mode=='D' else max(dg['P'],5-1)
            ck((js,jd)==(r['J_source'],r['J_destination'])==(3,4),'envelope arithmetic under analytic global extrema')
            ck((js-sg['P'],jd-dg['P'])==(r['R_source'],r['R_destination']),'explicit correction values')
            ck(r['delta_J']==jd-js and r['whole_law_holds']==(jd-js<=r['budget']),'whole corrected law verdict')
        rows+=1
    ck(len(c['controls'])==4,'frozen four source controls')
    for r in c['controls']:verify(r)
    d,dm,k,km=c['controls']
    ck((d['a'],d['q'],d['z'],d['whole_law_holds'])==(1,0,0,True),'DELETE repaired')
    ck((k['a'],k['q'],k['z'],k['whole_law_holds'])==(0,0,1,False),'B zero-double law refuted')
    for r,m in [(d,dm),(k,km)]:
        ck(m['source_A']==mirror(r['source_A'],6) and m['source_B']==mirror(r['source_B'],6),'source controls reflected')
        ck(m['destination_A']==mirror(r['destination_A'],6) and m['destination_B']==mirror(r['destination_B'],6),'destination controls reflected')
    metric=c['one_rotation_distance']
    ck(metric['source_A']==graphs[0]['A'] and metric['auxiliary_Tstar']==graphs[1]['A'],'metric attached to correct trees')
    ck(d['source_A']!=d['destination_A'] and d['dA']==1 and len(d['events_A'])==1 and d['events_A'][0][0]=='ZIG' and metric['rho']==1,'distance one, upper by actual zig and lower by distinctness')
    # Same-size algebraic contradiction, not a coefficient sweep.
    mb=graphs[1]['P'];mc=graphs[3]['P'];selfp=graphs[0]['P'];min_source_for_DELETE=mb-d['budget']
    ck(mb==4 and mc==mb+1 and selfp==graphs[2]['P']==1 and min_source_for_DELETE>selfp,'max-branch conditions for symbolic proof')
    upper=mb-min_source_for_DELETE;lower=mc-selfp
    ck((upper,lower)==(2,4) and upper<lower,'incompatible coefficient bounds')
    ck(c['coefficient_formulas']['same_n6_DELETE_necessary_upper']==upper and c['coefficient_formulas']['same_n6_KEEP_necessary_lower']==lower,'coefficient certificate exact')
    w=c['closed_witness'];a=w['initial_A'];b=w['initial_B'];ia,ib=a,b;At=Qt=Zt=0
    ck(a==b and len(w['word'])==len(w['full_replay'])==18,'complete diagonal word')
    for (mode,x),r in zip(w['word'],w['full_replay']):
        ck((a,b,mode,x)==(r['source_A'],r['source_B'],r['mode'],r['key']),'shared physical source states')
        ck('J_source' not in r,'no other replay J labels claimed')
        verify(r);a,b=r['destination_A'],r['destination_B'];At+=r['a'];Qt+=r['q'];Zt+=r['z']
    ck(a==ia and b==ib and (At,Qt,Zt)==(18,0,12)==(w['A'],w['Q_B'],w['Z_B']),'physical pair closure and totals')
    bad=w['full_replay'][w['failed_edge_index']]
    ck((bad['source_A'],bad['source_B'],bad['destination_A'],bad['destination_B'])==(k['source_A'],k['source_B'],k['destination_A'],k['destination_B']),'bad corrected KEEP is reachable')
    result={'status':'PASS','date':'2026-10-31','local_matching_cover_equalities':len(graphs),'residual_edges_covered':covered,
      'local_P_values':[g['P'] for g in graphs],'one_zig_distance_witness_verified':True,'correction_source_DELETE_destination_KEEP_destination':[2,0,3],
      'corrected_DELETE_control':{'a':1,'J_source':3,'J_destination':4,'budget':2},
      'corrected_B_counterexample':{'a':0,'q':0,'z':1,'J_source':3,'J_destination':4,'budget':0},
      'coefficient_necessary_bounds_same_n6':{'lambda_upper_from_DELETE':upper,'lambda_lower_from_KEEP':lower,'contradiction':True},
      'coefficient_scope':'all nonnegative lambda, including choices separately per n; algebraic argument PE02',
      'analytic_global_maxima_proof':'PE02_EXACT_EXTREMA_AND_B_OBSTRUCTION.md','global_auxiliary_trees_enumerated':0,
      'global_extrema_are_written_proof_not_finite_exhaustion':True,'source_controls':4,'complete_source_rows':rows,
      'actual_pair_closure':True,'closed_totals':{'A':At,'Q_B':Qt,'Z_B':Zt},'CD_counterexample':False,
      'other_replay_J_labels_claimed':False,'finite_potential_fits':0,'new_pair_graphs':0,'new_metric_graphs':0,'new_BFS_calls':0,
      'certificate_sha256':hashlib.sha256(cp.read_bytes()).hexdigest()}
    with (OUT/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
