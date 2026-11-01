"""Independent inherited-dual, joint-correction and full source readback."""
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
    ck(ks==sorted(set(ks)),'ordered distinct keys')
    return ks,ai|bi|{(ks[0],ks[-1])}
def proper(t):
    ks,ss=inspect(t)
    if ks:ss.remove((ks[0],ks[-1]))
    ck(len(ss)==max(0,len(ks)-1),'proper subtree multiplicity')
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
    raise AssertionError('absent key')
def mirror(t):return None if t is None else [7-t[0],mirror(t[2]),mirror(t[1])]

def main():
    cp=OUT/'joint_alignment_certificate.json';c=json.loads(cp.read_text(encoding='utf-8'));gs=c['matching_graphs'];covered=0
    ck(len(gs)==22,'frozen inherited graph count')
    origins={}
    for g in gs:
        op=g['origin_certificate']
        if op not in origins:origins[op]=json.loads((ROOT/op).read_text(encoding='utf-8'))['matching_graphs']
        old=origins[op][g['origin_graph_index']]
        ck(all(g[k]==v for k,v in old.items()),'every dual inherited unchanged from pinned source')
        ka,aa=proper(g['A']);kb,bb=proper(g['B']);r=g['A'][0];common=sorted(set(aa)&set(bb));cs=set(common)
        ck(ka==kb==list(range(1,7)) and r==g['root_A'],'same six keys and actual root')
        left=[I for I in aa if I not in cs];right=[J for J in bb if J not in cs and not (J[0]<=r<=J[1])]
        ck(g['all_A_intervals']==[list(I) for I in aa] and g['all_B_intervals']==[list(J) for J in bb],'all interval vertices regenerated')
        ck(g['forced_exact_pairs']==[list(I) for I in common] and all(not (I[0]<=r<=I[1]) for I in common),'all forced pairs eligible')
        ck(g['left_residual']==[list(I) for I in left] and g['eligible_right_residual']==[list(J) for J in right],'all residual vertices')
        ck(g['ineligible_B_intervals']==[list(J) for J in bb if J[0]<=r<=J[1]],'all root exclusions')
        adj=[[j for j,J in enumerate(right) if I[0]==J[0] or I[1]==J[1]] for I in left]
        ck(adj==g['adjacency'],'every edge and nonedge')
        mat=g['matching'];cl=g['cover_left'];cr=g['cover_right']
        ck(len({i for i,j in mat})==len({j for i,j in mat})==len(mat),'disjoint matching endpoints')
        ck(all(type(i) is type(j) is int and 0<=i<len(left) and j in adj[i] for i,j in mat),'valid matching edges')
        ck(len(set(cl))==len(cl) and len(set(cr))==len(cr),'cover distinctness')
        ck(all(type(i) is int and 0<=i<len(left) for i in cl) and all(type(j) is int and 0<=j<len(right) for j in cr),'cover bounds')
        ck(all(i in cl or j in cr for i,row in enumerate(adj) for j in row),'all residual edges covered')
        ck(len(mat)==len(cl)+len(cr)==g['mu_root'],'maximum by dual equality')
        ck(g['F']==len(aa)-len(common) and g['P']==g['F']-len(mat),'P and F independently computed');covered+=sum(map(len,adj))
    rows=0
    def verify(r):
        nonlocal rows
        a,b=r['source_A'],r['source_B'];mode=r['mode'];x=r['key'];da=depth(a,x);db=depth(b,x) if mode=='K' else None
        aa,ea=P.splay_trace(ptr(a),x)
        if mode=='K':bb,eb=P.splay_trace(ptr(b),x)
        else:bb,eb=ptr(b),[]
        aa,bb=raw(aa),raw(bb);ac=len(ea);q=sum(e['case']!='ZIG' for e in eb);z=sum(e['case']=='ZIG' for e in eb)
        ck((aa,bb)==(r['destination_A'],r['destination_B']),'complete physical endpoints')
        ck((da,db,ac,q,z)==(r['dA'],r['dB'],r['a'],r['q'],r['z']),'source costs')
        ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'depth conventions')
        ev=lambda es:[[e['case'],e['lo'],e['hi'],e['orient']] for e in es]
        ck(ev(ea)==r['events_A'] and ev(eb)==r['events_B'] and r['budget']==2*ac-q,'all orientations and budget')
        if 'source_values' in r:
            for sa,sb,key in [(a,b,'source_values'),(aa,bb,'destination_values')]:
                v=r[key];g=gs[v['graph_id']];same=sa[0]==sb[0];corr=0 if same else g['mu_root'];h=g['P']+corr
                ck(g['A']==sa and g['B']==sb,'value graph attached to correct pair')
                ck(v=={'P':g['P'],'F':g['F'],'mu_root':g['mu_root'],'same_roots':same,'R':corr,'H':h,'graph_id':v['graph_id']},'joint correction recomputed')
                ck(h==(g['P'] if same else g['F']) and corr>=0,'same fixed root rule on all states')
            delta=r['destination_values']['H']-r['source_values']['H']
            ck(delta==r['delta_H'] and r['whole_law_holds']==(delta<=r['budget']),'full source law verdict')
        rows+=1
    ck(len(c['controls'])==len(c['reflections'])==7,'seven frozen controls and reflections')
    expected=[(5,2),(4,2),(5,2),(5,5),(5,1),(5,2),(1,5)]
    for r,m,e in zip(c['controls'],c['reflections'],expected):
        verify(r);verify(m)
        ck((r['source_values']['H'],r['destination_values']['H'])==e,'registered control values')
        ck(m['source_A']==mirror(r['source_A']) and m['source_B']==mirror(r['source_B']),'input reflection')
        ck(m['destination_A']==mirror(r['destination_A']) and m['destination_B']==mirror(r['destination_B']),'output reflection')
        ck((m['source_values']['H'],m['destination_values']['H'],m['a'],m['q'],m['z'])==(r['source_values']['H'],r['destination_values']['H'],r['a'],r['q'],r['z']),'reflection values and costs')
    ck(all(r['whole_law_holds'] for r in c['controls'][:6]) and not c['controls'][6]['whole_law_holds'],'six prior controls repaired, new DELETE refuted')
    bad=c['controls'][6];v0=bad['source_values'];v1=bad['destination_values']
    ck(bad['source_A']!=bad['source_B'] and bad['source_A'][0]==bad['source_B'][0]==1,'equal-root source is not diagonal')
    ck(v0['same_roots'] and not v1['same_roots'] and (v0['P'],v1['P'],v0['R'],v1['R'])==(1,5,0,0),'new alignment-breaking family')
    ck((bad['a'],bad['q'],bad['z'],bad['delta_H'],bad['budget'])==(1,0,0,4,2),'single-zig full DELETE failure')
    necessary_delta=bad['budget']-(v1['P']-v0['P'])
    ck(necessary_delta==-2 and necessary_delta==4-6,'general correction family bound at n6')
    # Nonnegative R with zero at this equal-root input has Delta R>=0,
    # contradicting the required Delta R<=-2. No candidate evaluation needed.
    ck(0>necessary_delta,'normalization class contradiction')
    w=c['closed_witness'];a=w['initial_A'];b=w['initial_B'];ia,ib=a,b;At=Qt=Zt=0
    ck(a==b and len(w['word'])==len(w['full_replay'])==19,'complete diagonal word')
    for (mode,x),r in zip(w['word'],w['full_replay']):
        ck((a,b,mode,x)==(r['source_A'],r['source_B'],r['mode'],r['key']),'physical source sharing')
        ck('source_values' not in r,'no other replay H labels')
        verify(r);a,b=r['destination_A'],r['destination_B'];At+=r['a'];Qt+=r['q'];Zt+=r['z']
    ck(a==ia and b==ib and (At,Qt,Zt)==(20,0,12)==(w['A'],w['Q_B'],w['Z_B']),'actual pair closure and totals')
    r=w['full_replay'][w['failed_edge_index']]
    ck((r['source_A'],r['source_B'],r['destination_A'],r['destination_B'])==(bad['source_A'],bad['source_B'],bad['destination_A'],bad['destination_B']),'failed DELETE physically reachable')
    result={'status':'PASS','date':'2026-10-31','inherited_matching_cover_equalities':len(gs),'residual_edges_covered':covered,
      'source_controls':7,'reflections':7,'complete_source_rows':rows,'six_prior_controls_pass':True,
      'new_DELETE_counterexample':{'n':6,'a':1,'q':0,'z':0,'P_source':1,'P_destination':5,'R_source':0,'R_destination':0,'H_delta':4,'budget':2},
      'source_equal_roots_but_different_trees':True,'general_R_required_delta_upper_at_n6':necessary_delta,
      'nonnegative_equal_root_zero_class_refuted':True,'class_scope':'nonnegative R zero on all equal-root pairs; does not exclude R(A,A)=0 alone or signed R',
      'actual_pair_closure':True,'closed_totals':{'A':At,'Q_B':Qt,'Z_B':Zt},'CD_counterexample':False,
      'full_universal_B_law_for_H_established':False,'analytic_all_size_family':'JA02_EQUAL_ROOT_DELETE_AND_CLASS_OBSTRUCTION.md',
      'finite_potential_fits':0,'matching_solver_calls':0,'new_BFS_calls':0,'new_pair_graphs':0,'new_metric_graphs':0,
      'certificate_sha256':hashlib.sha256(cp.read_bytes()).hexdigest()}
    with (OUT/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
