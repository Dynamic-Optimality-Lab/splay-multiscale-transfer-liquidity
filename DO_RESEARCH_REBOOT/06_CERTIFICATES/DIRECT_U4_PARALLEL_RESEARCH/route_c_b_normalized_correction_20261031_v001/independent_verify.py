"""Independent local duals, analytic-bound arithmetic and pointer-source replay."""
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
    ck(ks==sorted(set(ks)),'ordered distinct source keys')
    return ks,ai|bi|{(ks[0],ks[-1])}
def proper(t):
    ks,ss=inspect(t)
    if ks:ss.remove((ks[0],ks[-1]))
    ck(len(ss)==max(0,len(ks)-1),'proper subtree multiplicity')
    return ks,sorted(ss)
def node(t,x):
    while t is not None:
        if t[0]==x:return t
        t=t[1] if x<t[0] else t[2]
    raise AssertionError('absent key')
def depth(t,x):
    d=0
    while t is not None:
        if t[0]==x:return d
        t=t[1] if x<t[0] else t[2];d+=1
    raise AssertionError('absent key')
def ptr(t):
    if t is None:return None
    p=P.mknode(t[0],ptr(t[1]),ptr(t[2]))
    for side in ('l','r'):
        if p[side] is not None:p[side]['p']=p
    return p
def raw(t):return None if t is None else [t['k'],raw(t['l']),raw(t['r'])]
def mirror(t):return None if t is None else [7-t[0],mirror(t[2]),mirror(t[1])]

def main():
    cp=OUT/'b_normalization_certificate.json';c=json.loads(cp.read_text(encoding='utf-8'));gs=c['matching_graphs'];covered=0
    ck(len(gs)==14,'frozen fourteen local graphs')
    for g in gs:
        ka,aa=proper(g['A']);kb,bb=proper(g['B']);r=g['A'][0];common=sorted(set(aa)&set(bb));cs=set(common)
        ck(ka==kb==list(range(1,7)) and r==g['root_A'],'same ranked keys and actual root')
        left=[I for I in aa if I not in cs];right=[J for J in bb if J not in cs and not (J[0]<=r<=J[1])]
        ck(g['all_A_intervals']==[list(I) for I in aa] and g['all_B_intervals']==[list(J) for J in bb],'all interval sets regenerated')
        ck(g['forced_exact_pairs']==[list(I) for I in common] and all(not (I[0]<=r<=I[1]) for I in common),'all exact pairs eligible')
        ck(g['left_residual']==[list(I) for I in left] and g['eligible_right_residual']==[list(J) for J in right],'all eligible residual vertices')
        ck(g['ineligible_B_intervals']==[list(J) for J in bb if J[0]<=r<=J[1]],'all gated B vertices')
        adj=[[j for j,J in enumerate(right) if I[0]==J[0] or I[1]==J[1]] for I in left]
        ck(adj==g['adjacency'],'every edge and nonedge')
        mat=g['matching'];cl=g['cover_left'];cr=g['cover_right']
        ck(len({i for i,j in mat})==len({j for i,j in mat})==len(mat),'disjoint matching endpoints')
        ck(all(type(i) is type(j) is int and 0<=i<len(left) and j in adj[i] for i,j in mat),'valid matching edges')
        ck(len(set(cl))==len(cl) and len(set(cr))==len(cr),'cover distinctness')
        ck(all(type(i) is int and 0<=i<len(left) for i in cl) and all(type(j) is int and 0<=j<len(right) for j in cr),'cover bounds')
        ck(all(i in cl or j in cr for i,row in enumerate(adj) for j in row),'all residual edges covered')
        ck(len(mat)==len(cl)+len(cr)==g['mu_root'],'maximum by matching-cover equality')
        ck(g['F']==len(aa)-len(common) and g['P']==g['F']-len(mat),'P values recomputed');covered+=sum(map(len,adj))
    ck([g['P'] for g in gs[:8]]==[1,4,1,5]*2 and [g['P'] for g in gs[8:]]==[4,2,5]*2,'all fourteen fixed P values')
    for i,j in [(0,4),(1,5),(2,6),(3,7),(8,11),(9,12),(10,13)]:
        ck(gs[j]['A']==mirror(gs[i]['A']) and gs[j]['B']==mirror(gs[i]['B']),'physical graph reflections')
    # Source maximum attained by root3 at depth5; range P<=5 is analytic.
    for si,di,wi in [(8,9,10),(11,12,13)]:
        src,dst,wit=gs[si],gs[di],gs[wi]
        ck(src['B']==wit['B'] and depth(wit['B'],wit['root_A'])==5 and wit['P']==5,'depth-five attaining auxiliary tree')
        ck(not wit['eligible_right_residual'] and not wit['forced_exact_pairs'],'witness has no eligible matching credit')
        ck(all(I[0]<=wit['root_A']<=I[1] for I in proper(wit['B'])[1]),'all proper source B intervals contain the witness root')
        ck(node(dst['B'],1)[1:]==[None,None] and node(dst['B'],6)[1:]==[None,None],'both destination extreme keys are leaves')
        ck(src['P']==4 and dst['P']==2,'self terms used in envelope bounds')
    rows=0
    def verify(r):
        nonlocal rows
        a,b=r['source_A'],r['source_B'];mode=r['mode'];x=r['key'];da=depth(a,x);db=depth(b,x) if mode=='K' else None
        aa,ea=P.splay_trace(ptr(a),x)
        if mode=='K':bb,eb=P.splay_trace(ptr(b),x)
        else:bb,eb=ptr(b),[]
        aa,bb=raw(aa),raw(bb);ac=len(ea);q=sum(e['case']!='ZIG' for e in eb);z=sum(e['case']=='ZIG' for e in eb)
        ck((aa,bb)==(r['destination_A'],r['destination_B']),'full physical endpoints')
        ck((da,db,ac,q,z)==(r['dA'],r['dB'],r['a'],r['q'],r['z']),'source costs')
        ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'depth/event convention')
        ev=lambda es:[[e['case'],e['lo'],e['hi'],e['orient']] for e in es]
        ck(ev(ea)==r['events_A'] and ev(eb)==r['events_B'] and r['budget']==2*ac-q,'oriented events and budget')
        if 'valuation_kind' in r:
            sg,dg=gs[r['source_graph']],gs[r['destination_graph']]
            ck((sg['A'],sg['B'],dg['A'],dg['B'])==(a,b,aa,bb),'graphs bound to correct source control')
            if r['valuation_kind']=='EXACT_INHERITED_PE':
                ms=4;md=4 if mode=='D' else 5;js=3;jd=4;ps=js-ms;pd=jd-md
                ck((js,jd,ms,md,ps,pd)==(r['J_source'],r['J_destination'],r['M_source'],r['M_destination'],r['Phi_source'],r['Phi_destination']),'normalized old PE arithmetic')
                ck((ps-sg['P'],pd-dg['P'])==(r['R_source'],r['R_destination']),'new correction values')
                ck(r['delta_Phi']==pd-ps and r['whole_law_holds']==(pd-ps<=r['budget']),'old safeguards repaired')
            else:
                ck(r['valuation_kind']=='CERTIFIED_BOUNDS','only registered value kinds')
                ms=5;js=max(sg['P'],ms-1);ps=js-ms;jlo=dg['P'];mhi=4;plo=jlo-mhi;required=ps+r['budget']
                ck((js,ms,ps,ps-sg['P'])==(r['J_source'],r['M_source'],r['Phi_source'],r['R_source']),'exact source from self term and nonself metric positivity')
                ck((jlo,mhi,plo,required,plo-ps)==(r['J_destination_lower'],r['M_destination_upper'],r['Phi_destination_lower'],r['required_Phi_destination_upper'],r['delta_Phi_lower']),'destination bounds and separation')
                ck((ac,q,z)==(0,2,0) and plo>required and r['law_refuted_by_bound'],'full-q law strictly refuted')
                ck(all(k not in r for k in ['J_destination','M_destination','Phi_destination']),'no uncomputed exact destination values invented')
        rows+=1
    ck(len(c['controls'])==6,'six frozen source controls')
    for r in c['controls']:verify(r)
    # Same-n c-normalization contradiction: old B zig forces c>=1;
    # with that sign, helper lower difference is -2+c, requiring c<=0.
    o=c['coefficient_obstruction'];ck(o=={'old_zero_double_edge_J_delta':1,'old_zero_double_edge_M_delta':1,'necessary_c6_lower':1,'helper_J_delta_lower':-2,'helper_M_delta_upper':-1,'helper_q':2,'necessary_c6_upper_under_c6_nonnegative':0},'exact coefficient inequalities')
    ck(c['controls'][2]['mode']=='K' and c['controls'][2]['a']==c['controls'][2]['q']==0 and c['controls'][2]['J_destination']-c['controls'][2]['J_source']==1 and c['controls'][2]['M_destination']-c['controls'][2]['M_source']==1,'old source forces c>=1')
    w=c['closed_witness'];a=w['initial_A'];b=w['initial_B'];ia,ib=a,b;At=Qt=Zt=0
    ck(a==b and len(w['word'])==len(w['full_replay'])==12,'complete diagonal word')
    for (mode,x),r in zip(w['word'],w['full_replay']):
        ck((a,b,mode,x)==(r['source_A'],r['source_B'],r['mode'],r['key']),'source-state sharing')
        ck('valuation_kind' not in r,'no other replay potential labels')
        verify(r);a,b=r['destination_A'],r['destination_B'];At+=r['a'];Qt+=r['q'];Zt+=r['z']
    ck(a==ia and b==ib and (At,Qt,Zt)==(16,4,2)==(w['A'],w['Q_B'],w['Z_B']),'actual pair closure and totals')
    bad=w['full_replay'][w['failed_edge_index']];ctrl=c['controls'][4]
    ck((bad['source_A'],bad['source_B'],bad['destination_A'],bad['destination_B'])==(ctrl['source_A'],ctrl['source_B'],ctrl['destination_A'],ctrl['destination_B']),'failed bound applies to reachable whole KEEP')
    result={'status':'PASS','date':'2026-10-31','matching_cover_equalities':len(gs),'residual_edges_covered':covered,
      'source_controls':6,'complete_source_rows':rows,'source_M_attaining_depth5_witness_verified':True,
      'destination_extreme_leaf_hypothesis_verified':True,'all_auxiliary_destination_upper_bound':'written extremal-leaf proof in BN02, not finite enumeration',
      'new_counterexample':{'a':0,'q':2,'z':0,'Phi_source':-1,'Phi_destination_lower':-2,'required_destination_upper':-3,'strict_separation':True},
      'old_DELETE_and_zero_double_KEEP_repaired':True,'coefficient_necessary_bounds_same_n6':{'c6_lower':1,'c6_upper':0,'contradiction':True},
      'exact_helper_destination_J_M_Phi_claimed':False,'other_replay_Phi_labels_claimed':False,
      'actual_pair_closure':True,'closed_totals':{'A':At,'Q_B':Qt,'Z_B':Zt},'CD_counterexample':False,
      'finite_potential_fits':0,'new_pair_graphs':0,'new_metric_graphs':0,'new_BFS_calls':0,'auxiliary_trees_enumerated':0,
      'certificate_sha256':hashlib.sha256(cp.read_bytes()).hexdigest()}
    with (OUT/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
