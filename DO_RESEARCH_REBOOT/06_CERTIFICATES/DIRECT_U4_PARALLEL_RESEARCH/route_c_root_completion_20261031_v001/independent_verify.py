"""Independent completion evaluation, local P duals and source replay."""
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
def ev(es):return [[e['case'],e['lo'],e['hi'],e['orient']] for e in es]

def main():
    cp=OUT/'root_completion_certificate.json';c=json.loads(cp.read_text(encoding='utf-8'));gs=c['matching_graphs'];covered=0
    ck(len(gs)==12,'twelve frozen local P graphs')
    for g in gs:
        ka,aa=proper(g['A']);kb,bb=proper(g['B']);r=g['A'][0];common=sorted(set(aa)&set(bb));cs=set(common)
        ck(ka==kb and len(ka) in (6,7) and r==g['root_A'],'same source keys and root')
        left=[I for I in aa if I not in cs];right=[J for J in bb if J not in cs and not (J[0]<=r<=J[1])]
        ck(g['all_A_intervals']==[list(I) for I in aa] and g['all_B_intervals']==[list(J) for J in bb],'all interval vertices regenerated')
        ck(g['forced_exact_pairs']==[list(I) for I in common] and all(not (I[0]<=r<=I[1]) for I in common),'all exact pairs eligible')
        ck(g['left_residual']==[list(I) for I in left] and g['eligible_right_residual']==[list(J) for J in right],'all residual vertices')
        ck(g['ineligible_B_intervals']==[list(J) for J in bb if J[0]<=r<=J[1]],'all root exclusions')
        adj=[[j for j,J in enumerate(right) if I[0]==J[0] or I[1]==J[1]] for I in left]
        ck(adj==g['adjacency'],'all endpoint edges/nonedges')
        m=g['matching'];cl=g['cover_left'];cr=g['cover_right']
        ck(len({i for i,j in m})==len({j for i,j in m})==len(m),'matching disjointness')
        ck(all(type(i) is type(j) is int and 0<=i<len(left) and j in adj[i] for i,j in m),'genuine matching edges')
        ck(len(set(cl))==len(cl) and len(set(cr))==len(cr),'cover distinctness')
        ck(all(type(i) is int and 0<=i<len(left) for i in cl) and all(type(j) is int and 0<=j<len(right) for j in cr),'cover bounds')
        ck(all(i in cl or j in cr for i,row in enumerate(adj) for j in row),'all residual edges covered')
        ck(len(m)==len(cl)+len(cr)==g['mu_root'],'rank certified by dual equality')
        ck(g['F']==len(aa)-len(common) and g['P']==g['F']-len(m),'P values recomputed')
        if len(ka)==7:ck(not any(adj) and g['mu_root']==0,'new n7 graphs have empty residual edge set')
        covered+=sum(map(len,adj))
    completions=0;rows=0;keep_identities=0
    def completion(a,b):
        nonlocal completions
        r=a[0];bt,es=P.splay_trace(ptr(b),r);bt=raw(bt);ka,ai=proper(a);kb,bi=proper(bt)
        ck(ka==kb,'completion preserves common keys')
        common=sorted(set(ai)&set(bi));f=len(ai)-len(common);q=sum(e['case']!='ZIG' for e in es);z=sum(e['case']=='ZIG' for e in es);d=depth(b,r)
        ck(bt[0]==r and q==d//2 and z==d%2,'completion source cost/root')
        completions+=1
        return {'root_A':r,'completed_B':bt,'completion_depth':d,'completion_q':q,'completion_z':z,'completion_events':ev(es),
          'common_terminal_intervals':[list(I) for I in common],'F_terminal':f,'Phi':f+q}
    def verify(r):
        nonlocal rows,keep_identities
        a,b=r['source_A'],r['source_B'];mode=r['mode'];x=r['key'];da=depth(a,x);db=depth(b,x) if mode=='K' else None
        aa,ea=P.splay_trace(ptr(a),x)
        if mode=='K':bb,eb=P.splay_trace(ptr(b),x)
        else:bb,eb=ptr(b),[]
        aa,bb=raw(aa),raw(bb);ac=len(ea);q=sum(e['case']!='ZIG' for e in eb);z=sum(e['case']=='ZIG' for e in eb)
        ck((aa,bb)==(r['destination_A'],r['destination_B']),'actual physical endpoints')
        ck((da,db,ac,q,z)==(r['dA'],r['dB'],r['a'],r['q'],r['z']),'actual source costs')
        ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'actual depth/event units')
        ck(ev(ea)==r['events_A'] and ev(eb)==r['events_B'],'actual oriented events')
        v0,vm,v1=completion(a,b),completion(aa,b),completion(aa,bb)
        ck((v0,vm,v1)==(r['source_completion'],r['after_A_completion'],r['destination_completion']),'all completion traces and explicit potential values regenerated')
        delta=v1['Phi']-v0['Phi'];budget=2*ac-q
        ck((delta,budget,delta<=budget)==(r['delta_Phi'],r['budget'],r['whole_law_holds']),'whole source law verdict')
        if mode=='K':
            ck(v1['Phi']-vm['Phi']==-q and vm['completed_B']==bb and v1['completed_B']==bb and v1['completion_q']==0,'exact full B identity')
            keep_identities+=1
        if 'source_P' in r:
            for sa,sb,k in [(a,b,'source_P'),(aa,bb,'destination_P')]:
                v=r[k];g=gs[v['graph_id']];ck(g['A']==sa and g['B']==sb and v['P']==g['P'],'raw P attached to correct actual pair')
            ck((v0['Phi']-r['source_P']['P'],v1['Phi']-r['destination_P']['P'])==(r['R_source'],r['R_destination']),'joint correction values')
        rows+=1
    ck(len(c['controls'])==len(c['reflections'])==3,'three frozen controls and reflections')
    expected=[(4,4,3,-1),(5,3,1,1),(5,8,0,2)]
    for r,m,e in zip(c['controls'],c['reflections'],expected):
        verify(r);verify(m)
        ck((r['source_completion']['Phi'],r['destination_completion']['Phi'],r['R_source'],r['R_destination'])==e,'registered exact values')
        n=len(inspect(r['source_A'])[0])
        ck(m['source_A']==mirror(r['source_A'],n) and m['source_B']==mirror(r['source_B'],n),'source reflection')
        ck(m['destination_A']==mirror(r['destination_A'],n) and m['destination_B']==mirror(r['destination_B'],n),'destination reflection')
        ck((m['source_completion']['Phi'],m['destination_completion']['Phi'],m['a'],m['q'],m['z'])==(r['source_completion']['Phi'],r['destination_completion']['Phi'],r['a'],r['q'],r['z']),'reflection values/costs')
    bad=c['controls'][2]
    ck((bad['a'],bad['q'],bad['z'],bad['delta_Phi'],bad['budget'])==(1,0,0,3,2),'one-zig actual DELETE failure')
    s=bad['source_completion'];d=bad['destination_completion']
    ck(s['F_terminal']==d['F_terminal']==5 and (s['completion_q'],d['completion_q'])==(0,3),'terminal scalar f7 cancels while completion charge rises3')
    w=c['closed_witness'];a=w['initial_A'];b=w['initial_B'];ia,ib=a,b;At=Qt=Zt=ds=0
    ck(a==b and len(w['word'])==len(w['full_replay'])==21,'complete diagonal word')
    for (mode,x),r in zip(w['word'],w['full_replay']):
        ck((a,b,mode,x)==(r['source_A'],r['source_B'],r['mode'],r['key']),'physical source-state sharing')
        verify(r);a,b=r['destination_A'],r['destination_B'];At+=r['a'];Qt+=r['q'];Zt+=r['z'];ds+=r['delta_Phi']
    ck(a==ia and b==ib and ds==0 and (At,Qt,Zt)==(27,0,12)==(w['A'],w['Q_B'],w['Z_B']),'actual pair closure, costs and explicit Phi telescope')
    r=w['full_replay'][w['failed_edge_index']]
    ck((r['source_A'],r['source_B'],r['destination_A'],r['destination_B'])==(bad['source_A'],bad['source_B'],bad['destination_A'],bad['destination_B']),'registered odd-family edge is reachable')
    result={'status':'PASS','date':'2026-10-31','matching_cover_equalities':len(gs),'residual_edges_covered':covered,
      'source_controls':3,'reflections':3,'complete_source_rows':rows,'completion_evaluations_with_multiplicity':completions,
      'finite_full_B_identities_checked':keep_identities,'universal_B_proof':'CP01_EXPLICIT_CORRECTION_AND_UNIVERSAL_B_LAW.md',
      'equal_root_reserve_control_R_source':3,'previous_DELETE_and_starved_helper_controls_pass':True,
      'new_DELETE_counterexample':{'n':7,'a':1,'actual_q':0,'source_completion_q':0,'destination_completion_q':3,'F_terminal_before':5,'F_terminal_after':5,'Phi_source':5,'Phi_destination':8,'budget':2},
      'terminal_F_only_scalar_class_refuted':True,'class_scope':'arbitrary finite f_n of completed-pair F only, with the fixed +Q term',
      'actual_pair_closure':True,'explicit_Phi_telescope':0,'closed_totals':{'A':At,'Q_B':Qt,'Z_B':Zt},'CD_counterexample':False,
      'all_odd_family_proof':'CP02_ALL_ODD_DELETE_AND_TERMINAL_CLASS_OBSTRUCTION.md','finite_checks_not_an_all_size_fit':True,
      'connector_purpose':'one fixed analytic n7 witness reachability; no potential labels evaluated during its BFS',
      'finite_potential_fits':0,'new_pair_graphs':0,'new_metric_graphs':0,'matching_solver_calls':0,
      'certificate_sha256':hashlib.sha256(cp.read_bytes()).hexdigest()}
    with (OUT/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
