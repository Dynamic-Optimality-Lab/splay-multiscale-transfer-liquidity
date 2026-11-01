"""Verify the unchanged antichain root-zig counterexample independently."""
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
    ck(ks==sorted(set(ks)),'valid ordered keys')
    return ks,ai|bi|{(ks[0],ks[-1])}
def proper(t):
    ks,ss=inspect(t)
    if ks:ss.remove((ks[0],ks[-1]))
    ck(len(ss)==max(0,len(ks)-1),'proper set multiplicity')
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
def mirror(t):return None if t is None else [8-t[0],mirror(t[2]),mirror(t[1])]
def disjoint(I,J):return I[1]<J[0] or J[1]<I[0]
def ev(es):return [[e['case'],e['lo'],e['hi'],e['orient']] for e in es]

def main():
    cp=OUT/'root_bound_countercertificate.json';c=json.loads(cp.read_text(encoding='utf-8'));tg=c['terminal_graphs'];pg=c['raw_P_graphs']
    duals=ants=subsets=0
    def dual(adj,nr,d,allowed):
        nonlocal duals
        ck(d['allowed_right']==sorted(allowed),'permitted right subset');allowed=set(allowed)
        mat=d['matching'];cl=d['cover_left'];cr=d['cover_right']
        ck(len({i for i,j in mat})==len({j for i,j in mat})==len(mat),'disjoint matching endpoints')
        ck(all(type(i) is type(j) is int and 0<=i<len(adj) and j in allowed and j in adj[i] for i,j in mat),'all genuine permitted edges')
        ck(len(set(cl))==len(cl) and len(set(cr))==len(cr),'cover distinctness')
        ck(all(type(i) is int and 0<=i<len(adj) for i in cl) and all(type(j) is int and 0<=j<nr and j in allowed for j in cr),'cover bounds')
        ck(all(i in cl or j in cr for i,row in enumerate(adj) for j in row if j in allowed),'every allowed edge covered')
        ck(len(mat)==len(cl)+len(cr)==d['rank'],'exact rank by matching/cover equality');duals+=1
    for g in tg:
        ka,aa=proper(g['A']);kb,bb=proper(g['C']);co=sorted(set(aa)&set(bb));cs=set(co)
        ck(ka==kb==list(range(1,8)) and g['A'][0]==g['C'][0],'same seven keys and completed root')
        l=[I for I in aa if I not in cs];r=[J for J in bb if J not in cs]
        ck(g['all_A_intervals']==[list(I) for I in aa] and g['all_C_intervals']==[list(J) for J in bb],'all terminal intervals')
        ck(g['forced_exact_pairs']==[list(I) for I in co] and g['left_residual']==[list(I) for I in l] and g['right_residual']==[list(J) for J in r],'forced pairs and residual vertices')
        adj=[[j for j,J in enumerate(r) if I[0]==J[0] or I[1]==J[1]] for I in l];ck(adj==g['adjacency'],'all terminal endpoint edges')
        maximal=set()
        for mask in range(1<<len(r)):
            subsets+=1;s=tuple(j for j in range(len(r)) if (mask>>j)&1)
            if any(not disjoint(r[i],r[j]) for i in s for j in s if i<j):continue
            if all(any(not disjoint(r[i],r[j]) for i in s) for j in range(len(r)) if j not in s):maximal.add(s)
        listed=[tuple(d['allowed_right']) for d in g['maximal_antichain_duals']]
        ck(len(listed)==len(set(listed)) and set(listed)==maximal,'complete maximal antichain classification for this fixed pair')
        for d in g['maximal_antichain_duals']:dual(adj,len(r),d,d['allowed_right']);ants+=1
        dual(adj,len(r),g['unrestricted_dual'],range(len(r)))
        alpha=max(d['rank'] for d in g['maximal_antichain_duals']);bi=g['maximizing_antichain_index'];f=len(aa)-len(co)
        ck(0<=bi<len(listed) and g['maximal_antichain_duals'][bi]['rank']==alpha==g['alpha'],'global alpha upper and attaining matching')
        ck((g['F'],g['K'],g['Ehat'])==(f,f-alpha,f-g['unrestricted_dual']['rank']),'unchanged terminal objective')
    for g in pg:
        ka,aa=proper(g['A']);kb,bb=proper(g['B']);r=g['A'][0];co=sorted(set(aa)&set(bb));cs=set(co)
        ck(ka==kb==list(range(1,8)),'raw P keys')
        l=[I for I in aa if I not in cs];rr=[J for J in bb if J not in cs and not (J[0]<=r<=J[1])]
        ck(g['forced_exact_pairs']==[list(I) for I in co] and g['left_residual']==[list(I) for I in l] and g['eligible_right_residual']==[list(J) for J in rr],'raw P vertices')
        adj=[[j for j,J in enumerate(rr) if I[0]==J[0] or I[1]==J[1]] for I in l];ck(adj==g['adjacency'],'raw P edges')
        dual(adj,len(rr),g['dual'],range(len(rr)));f=len(aa)-len(co)
        ck((g['F'],g['P'])==(f,f-g['dual']['rank']),'raw P rank and value')
    rows=completions=0
    def completion(a,b,v):
        nonlocal completions
        r=a[0];bt,es=P.splay_trace(ptr(b),r);bt=raw(bt);d=depth(b,r);q=sum(e['case']!='ZIG' for e in es);z=sum(e['case']=='ZIG' for e in es)
        g=tg[v['terminal_graph']];ck(g['A']==a and g['C']==bt,'terminal certificate at correct completed pair')
        expected={'root_A':r,'completed_B':bt,'completion_depth':d,'completion_q':q,'completion_z':z,'completion_events':ev(es),
          'terminal_graph':v['terminal_graph'],'F_terminal':g['F'],'alpha_terminal':g['alpha'],'K_terminal':g['K'],'Phi':g['K']+q}
        ck(v==expected and q==d//2 and z==d%2 and bt[0]==r,'completion formula, source events and costs');completions+=1
    def verify(row):
        nonlocal rows
        a,b=row['source_A'],row['source_B'];x=row['key'];mode=row['mode'];da=depth(a,x);db=depth(b,x) if mode=='K' else None
        aa,ea=P.splay_trace(ptr(a),x)
        if mode=='K':bb,eb=P.splay_trace(ptr(b),x)
        else:bb,eb=ptr(b),[]
        aa,bb=raw(aa),raw(bb);ac=len(ea);q=sum(e['case']!='ZIG' for e in eb);z=sum(e['case']=='ZIG' for e in eb)
        ck((aa,bb)==(row['destination_A'],row['destination_B']),'actual source endpoints')
        ck((da,db,ac,q,z)==(row['dA'],row['dB'],row['a'],row['q'],row['z']),'actual source costs')
        ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'depth/event units')
        ck(ev(ea)==row['events_A'] and ev(eb)==row['events_B'],'all oriented actual events')
        v0,vm,v1=row['source_completion'],row['after_A_completion'],row['destination_completion']
        completion(a,b,v0);completion(aa,b,vm);completion(aa,bb,v1)
        delta=v1['Phi']-v0['Phi'];budget=2*ac-q
        ck((delta,budget,delta<=budget)==(row['delta_Phi'],row['budget'],row['whole_law_holds']),'full source verdict')
        if mode=='K':ck(v1['Phi']-vm['Phi']==-q,'valid B identity remains exact')
        if 'source_P' in row:
            for sa,sb,k in [(a,b,'source_P'),(aa,bb,'destination_P')]:
                v=row[k];g=pg[v['raw_P_graph']];ck(g['A']==sa and g['B']==sb and g['P']==v['P'],'raw P attached correctly')
            ck((v0['Phi']-row['source_P']['P'],v1['Phi']-row['destination_P']['P'])==(row['R_source'],row['R_destination']),'same explicit correction values')
        rows+=1
    ck(len(c['controls'])==2 and c['candidate_modified'] is False,'one fixed counterexample plus reflection, unchanged candidate')
    bad,ref=c['controls'];verify(bad);verify(ref)
    ck(bad['source_A']==[1,None,[7,[3,[2,None,None],[5,[4,None,None],[6,None,None]]],None]],'explicit parity-comb input A')
    ck((bad['mode'],bad['key'],bad['dA'],bad['a'],bad['q'],bad['z'],bad['delta_Phi'],bad['budget'])==('D',7,1,1,0,0,3,2),'in-domain root-zig violation')
    ck(bad['source_B']==bad['destination_B'] and len(bad['events_A'])==1 and bad['events_A'][0][0]=='ZIG','B frozen and one actual A zig')
    s,d=bad['source_completion'],bad['destination_completion']
    ck((s['F_terminal'],d['F_terminal'],s['alpha_terminal'],d['alpha_terminal'],s['K_terminal'],d['K_terminal'])==(5,5,1,1,4,4),'equal terminal K proven by complete optimality certificates')
    ck((s['completion_q'],d['completion_q'],s['Phi'],d['Phi'])==(0,3,4,7),'completion charge drives the violation')
    ck((bad['source_P']['P'],bad['destination_P']['P'],bad['R_source'],bad['R_destination'])==(3,6,1,1),'retained correction does not drop')
    ck(ref['source_A']==mirror(bad['source_A']) and ref['source_B']==mirror(bad['source_B']) and ref['destination_A']==mirror(bad['destination_A']) and ref['destination_B']==mirror(bad['destination_B']),'exact reflection')
    ck((ref['delta_Phi'],ref['budget'],ref['dA'])==(3,2,1),'other zig orientation fails')
    w=c['closed_witness'];a=w['initial_A'];b=w['initial_B'];ia,ib=a,b;At=Qt=Zt=ds=0;failed=[]
    ck(a==b and len(w['word'])==len(w['full_replay'])==20,'complete diagonal source word')
    for i,((mode,x),r) in enumerate(zip(w['word'],w['full_replay'])):
        ck((a,b,mode,x)==(r['source_A'],r['source_B'],r['mode'],r['key']),'physical source sharing')
        verify(r);a,b=r['destination_A'],r['destination_B'];At+=r['a'];Qt+=r['q'];Zt+=r['z'];ds+=r['delta_Phi']
        if not r['whole_law_holds']:failed.append(i)
    ck(a==ia and b==ib and ds==0 and (At,Qt,Zt)==(27,0,12)==(w['A'],w['Q_B'],w['Z_B']),'actual paired closure, costs and Phi telescope')
    ck(failed==w['other_failed_indices']==[6] and w['failed_edge_index']==6,'registered zig is the only recorded failing edge')
    r=w['full_replay'][6];ck((r['source_A'],r['source_B'],r['destination_A'],r['destination_B'])==(bad['source_A'],bad['source_B'],bad['destination_A'],bad['destination_B']),'counteredge reached from diagonal')
    result={'status':'PASS','date':'2026-10-31','terminal_graphs':len(tg),'all_maximal_antichains_verified':ants,
      'antichain_subset_checks':subsets,'raw_P_graphs':len(pg),'matching_cover_equalities':duals,
      'source_controls':2,'complete_source_rows':rows,'completion_evaluations_with_multiplicity':completions,
      'universal_root_zig_double_bound':'REFUTED—EXACT','root_zig_counterexample':{'n':7,'dA':1,'a':1,'actual_q':0,'K_before':4,'K_after':4,'Phi_before':4,'Phi_after':7,'increment':3,'bound':2},
      'both_zig_orientations_verified':True,'root_double_cases_separately_classified':False,
      'candidate_definition_unchanged':True,'actual_pair_closure':True,'closed_totals':{'A':At,'Q_B':Qt,'Z_B':Zt},
      'failed_replay_indices':failed,'explicit_Phi_telescope':0,'CD_counterexample':False,
      'all_odd_n_proof':'RB01_ALL_ODD_ROOT_ZIG_REFUTATION.md','all_size_proof_is_analytic_not_fit':True,
      'finite_potential_fits':0,'new_pair_graphs':0,'new_metric_graphs':0,
      'certificate_sha256':hashlib.sha256(cp.read_bytes()).hexdigest()}
    with (OUT/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
