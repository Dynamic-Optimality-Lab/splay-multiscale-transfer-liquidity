"""Verify every maximal antichain and dual; no producer or matching solver."""
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
    ck(len(ss)==max(0,len(ks)-1),'proper interval multiplicity')
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
def mirror(t,n):return None if t is None else [n+1-t[0],mirror(t[2],n),mirror(t[1],n)]
def disjoint(I,J):return I[1]<J[0] or J[1]<I[0]
def ev(es):return [[e['case'],e['lo'],e['hi'],e['orient']] for e in es]

def main():
    cp=OUT/'antichain_terminal_certificate.json';c=json.loads(cp.read_text(encoding='utf-8'));tg=c['terminal_graphs'];pg=c['raw_P_graphs']
    dual_count=anti_count=subset_checks=0
    def verify_dual(adj,nright,d,allowed):
        nonlocal dual_count
        ck(d['allowed_right']==sorted(allowed),'all and only permitted right vertices')
        m=d['matching'];cl=d['cover_left'];cr=d['cover_right'];allowed=set(allowed)
        ck(len({i for i,j in m})==len({j for i,j in m})==len(m),'disjoint matching endpoints')
        ck(all(type(i) is type(j) is int and 0<=i<len(adj) and j in allowed and j in adj[i] for i,j in m),'genuine permitted matching edges')
        ck(len(set(cl))==len(cl) and len(set(cr))==len(cr),'cover distinctness')
        ck(all(type(i) is int and 0<=i<len(adj) for i in cl) and all(type(j) is int and j in allowed and 0<=j<nright for j in cr),'cover bounds')
        ck(all(i in cl or j in cr for i,row in enumerate(adj) for j in row if j in allowed),'cover every permitted edge')
        ck(len(m)==len(cl)+len(cr)==d['rank'],'exact optimum by dual equality');dual_count+=1
    for g in tg:
        ka,aa=proper(g['A']);kc,cc=proper(g['C']);common=sorted(set(aa)&set(cc));cs=set(common)
        ck(ka==kc and len(ka) in (6,7) and g['A'][0]==g['C'][0],'same keys and completed roots')
        l=[I for I in aa if I not in cs];r=[J for J in cc if J not in cs]
        ck(g['all_A_intervals']==[list(I) for I in aa] and g['all_C_intervals']==[list(J) for J in cc],'every terminal interval regenerated')
        ck(g['forced_exact_pairs']==[list(I) for I in common] and g['left_residual']==[list(I) for I in l] and g['right_residual']==[list(J) for J in r],'forced exact pairs and residual-only restriction')
        adj=[[j for j,J in enumerate(r) if I[0]==J[0] or I[1]==J[1]] for I in l]
        ck(adj==g['adjacency'] and len(r)<=6,'every terminal endpoint edge')
        maximal=set()
        for mask in range(1<<len(r)):
            subset_checks+=1;s=tuple(j for j in range(len(r)) if (mask>>j)&1)
            if any(not disjoint(r[i],r[j]) for i in s for j in s if i<j):continue
            if all(any(not disjoint(r[i],r[j]) for i in s) for j in range(len(r)) if j not in s):maximal.add(s)
        listed=[tuple(d['allowed_right']) for d in g['maximal_antichain_duals']]
        ck(len(set(listed))==len(listed) and set(listed)==maximal,'ALL maximal residual B antichains, no missing cases')
        for d in g['maximal_antichain_duals']:
            verify_dual(adj,len(r),d,d['allowed_right']);anti_count+=1
        verify_dual(adj,len(r),g['unrestricted_dual'],range(len(r)))
        alpha=max(d['rank'] for d in g['maximal_antichain_duals']);best=g['maximizing_antichain_index']
        ck(0<=best<len(listed) and g['maximal_antichain_duals'][best]['rank']==alpha==g['alpha'],'global antichain optimum attained and bounded')
        f=len(aa)-len(common);mu=g['unrestricted_dual']['rank']
        ck((g['F'],g['K'],g['Ehat'])==(f,f-alpha,f-mu) and 0<=alpha<=mu,'terminal objective and Ehat<=K<=F')
    for g in pg:
        ka,aa=proper(g['A']);kb,bb=proper(g['B']);r=g['A'][0];common=sorted(set(aa)&set(bb));cs=set(common)
        ck(ka==kb,'raw P same keys')
        l=[I for I in aa if I not in cs];rr=[J for J in bb if J not in cs and not (J[0]<=r<=J[1])]
        ck(g['forced_exact_pairs']==[list(I) for I in common] and g['left_residual']==[list(I) for I in l] and g['eligible_right_residual']==[list(J) for J in rr],'raw P exact pairs and eligibility')
        adj=[[j for j,J in enumerate(rr) if I[0]==J[0] or I[1]==J[1]] for I in l]
        ck(adj==g['adjacency'],'all raw P endpoint edges')
        verify_dual(adj,len(rr),g['dual'],range(len(rr)));f=len(aa)-len(common)
        ck((g['F'],g['P'])==(f,f-g['dual']['rank']),'raw P values independently computed')
    rows=completions=keeps=0
    def completion(a,b,v):
        nonlocal completions
        r=a[0];ct,es=P.splay_trace(ptr(b),r);ct=raw(ct);d=depth(b,r);q=sum(e['case']!='ZIG' for e in es);z=sum(e['case']=='ZIG' for e in es)
        g=tg[v['terminal_graph']];ck(g['A']==a and g['C']==ct,'terminal optimum attached to actual completed pair')
        ck(q==d//2 and z==d%2 and ct[0]==r,'completion roots and costs')
        expected={'root_A':r,'completed_B':ct,'completion_depth':d,'completion_q':q,'completion_z':z,'completion_events':ev(es),
          'terminal_graph':v['terminal_graph'],'F_terminal':g['F'],'alpha_terminal':g['alpha'],'K_terminal':g['K'],'Phi':g['K']+q}
        ck(v==expected,'all explicit completion potential values regenerated');completions+=1
    def verify(row):
        nonlocal rows,keeps
        a,b=row['source_A'],row['source_B'];mode=row['mode'];x=row['key'];da=depth(a,x);db=depth(b,x) if mode=='K' else None
        aa,ea=P.splay_trace(ptr(a),x)
        if mode=='K':bb,eb=P.splay_trace(ptr(b),x)
        else:bb,eb=ptr(b),[]
        aa,bb=raw(aa),raw(bb);ac=len(ea);q=sum(e['case']!='ZIG' for e in eb);z=sum(e['case']=='ZIG' for e in eb)
        ck((aa,bb)==(row['destination_A'],row['destination_B']),'full actual endpoints')
        ck((da,db,ac,q,z)==(row['dA'],row['dB'],row['a'],row['q'],row['z']),'actual source costs')
        ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'actual depth convention')
        ck(ev(ea)==row['events_A'] and ev(eb)==row['events_B'],'all actual oriented events')
        v0,vm,v1=row['source_completion'],row['after_A_completion'],row['destination_completion']
        completion(a,b,v0);completion(aa,b,vm);completion(aa,bb,v1)
        delta=v1['Phi']-v0['Phi'];budget=2*ac-q
        ck((delta,budget,delta<=budget)==(row['delta_Phi'],row['budget'],row['whole_law_holds']),'full source inequality verdict')
        if mode=='K':ck(v1['Phi']-vm['Phi']==-q,'full B identity');keeps+=1
        if 'source_P' in row:
            for sa,sb,k in [(a,b,'source_P'),(aa,bb,'destination_P')]:
                v=row[k];g=pg[v['raw_P_graph']];ck(g['A']==sa and g['B']==sb and g['P']==v['P'],'raw P attached correctly')
            ck((v0['Phi']-row['source_P']['P'],v1['Phi']-row['destination_P']['P'])==(row['R_source'],row['R_destination']),'joint R values')
        rows+=1
    ck(len(c['controls'])==len(c['reflections'])==6,'all frozen controls tested, no expanded corpus')
    expected=[(3,4),(4,2),(5,6),(3,2),(3,2),(3,5)]
    for r,m,e in zip(c['controls'],c['reflections'],expected):
        verify(r);verify(m);n=len(inspect(r['source_A'])[0])
        ck((r['source_completion']['Phi'],r['destination_completion']['Phi'])==e and r['whole_law_holds'],'fixed controls all pass')
        ck(m['source_A']==mirror(r['source_A'],n) and m['source_B']==mirror(r['source_B'],n),'input reflection')
        ck(m['destination_A']==mirror(r['destination_A'],n) and m['destination_B']==mirror(r['destination_B'],n),'output reflection')
        ck((m['source_completion']['Phi'],m['destination_completion']['Phi'],m['a'],m['q'],m['z'])==(r['source_completion']['Phi'],r['destination_completion']['Phi'],r['a'],r['q'],r['z']),'reflection values and costs')
    ck(c['first_failure'] is None and c['first_failure_reflection'] is None and c['disposition']=='OPEN','no candidate refutation or universal promotion')
    w=c['closed_witness'];a=w['initial_A'];b=w['initial_B'];ia,ib=a,b;At=Qt=Zt=ds=0
    ck(a==b and len(w['word'])==len(w['full_replay'])==21,'frozen CP closed word')
    for (mode,x),row in zip(w['word'],w['full_replay']):
        ck((a,b,mode,x)==(row['source_A'],row['source_B'],row['mode'],row['key']),'physical source sharing')
        verify(row);ck(row['whole_law_holds'],'frozen replay edges pass')
        a,b=row['destination_A'],row['destination_B'];At+=row['a'];Qt+=row['q'];Zt+=row['z'];ds+=row['delta_Phi']
    ck(a==ia and b==ib and ds==0 and (At,Qt,Zt)==(27,0,12)==(w['A'],w['Q_B'],w['Z_B']),'actual closure, costs and explicit telescope')
    ck(c['global_DELETE_not_inferred_from_survival'] is True,'finite survival explicitly not a universal proof')
    result={'status':'PASS','date':'2026-10-31','terminal_graphs':len(tg),'all_maximal_antichains_verified':anti_count,
      'antichain_subset_completeness_checks':subset_checks,'raw_P_graphs':len(pg),'total_matching_cover_equalities':dual_count,
      'source_controls':6,'reflections':6,'complete_source_rows':rows,'completion_evaluations_with_multiplicity':completions,
      'finite_B_identities_checked':keeps,'all_frozen_controls_and_replay_pass':True,'candidate_disposition':'OPEN',
      'universal_DELETE_proved':False,'no_counterexample_in_frozen_audit':True,'no_finite_survival_promotion':True,
      'actual_pair_closure':True,'closed_totals':{'A':At,'Q_B':Qt,'Z_B':Zt},'explicit_Phi_telescope':0,
      'finite_potential_fits':0,'new_BFS_calls':0,'new_pair_graphs':0,'new_metric_graphs':0,'coefficient_searches':0,
      'certificate_sha256':hashlib.sha256(cp.read_bytes()).hexdigest()}
    with (OUT/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
