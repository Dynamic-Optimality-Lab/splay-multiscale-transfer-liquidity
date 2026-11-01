"""B normalization of J: frozen local duals and inherited source witnesses."""
from pathlib import Path
import hashlib,json,subprocess,sys
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/'python'))
from independent import splay as S
from liquidity import legacy_embedding as P
def ck(ok,msg):
    if not ok:raise AssertionError(msg)
def save(n,v):
    with (OUT/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dec(t):return S.LEAF if t is None else S.node(t[0],dec(t[1]),dec(t[2]))
def raw(t):return None if t==S.LEAF else [t[1],raw(t[2]),raw(t[3])]
def ptr(t):
    if t==S.LEAF:return None
    p=P.mknode(t[1],ptr(t[2]),ptr(t[3]))
    for k in ('l','r'):
        if p[k] is not None:p[k]['p']=p
    return p
def rp(t):return None if t is None else [t['k'],rp(t['l']),rp(t['r'])]
def vine(lo,hi):
    t=S.LEAF
    for k in range(hi,lo-1,-1):t=S.node(k,S.LEAF,t)
    return t
def clades(t):
    if t==S.LEAF:return set()
    ks=S.inorder(t)
    return {(ks[0],ks[-1])}|clades(t[2])|clades(t[3])
def proper(t):
    ks=S.inorder(t);ss=clades(t)
    if ks:ss.remove((ks[0],ks[-1]))
    return sorted(ss)
def mir(t,n):return S.LEAF if t==S.LEAF else S.node(n+1-t[1],mir(t[3],n),mir(t[2],n))
def mi(I,n=6):return (n+1-I[1],n+1-I[0])

def graph(label,a,b,pairs,cover_left,cover_right):
    aa=proper(a);bb=proper(b);r=a[1];common=sorted(set(aa)&set(bb));cs=set(common)
    left=[I for I in aa if I not in cs];right=[J for J in bb if J not in cs and not (J[0]<=r<=J[1])]
    adj=[[j for j,J in enumerate(right) if I[0]==J[0] or I[1]==J[1]] for I in left]
    mat=sorted([[left.index(I),right.index(J)] for I,J in pairs]);cl=sorted(left.index(I) for I in cover_left);cr=sorted(right.index(J) for J in cover_right)
    ck(len({i for i,j in mat})==len({j for i,j in mat})==len(mat),'disjoint matching')
    ck(all(j in adj[i] for i,j in mat),'all matching edges')
    ck(len(mat)==len(cl)+len(cr) and all(i in cl or j in cr for i,row in enumerate(adj) for j in row),'matching-cover equality')
    f=len(aa)-len(common)
    return {'label':label,'A':raw(a),'B':raw(b),'root_A':r,'all_A_intervals':[list(I) for I in aa],'all_B_intervals':[list(J) for J in bb],
      'forced_exact_pairs':[list(I) for I in common],'left_residual':[list(I) for I in left],'eligible_right_residual':[list(J) for J in right],
      'ineligible_B_intervals':[list(J) for J in bb if J[0]<=r<=J[1]],'adjacency':adj,'matching':mat,'cover_left':cl,'cover_right':cr,
      'mu_root':len(mat),'F':f,'P':f-len(mat)}

def edge(label,a,b,mode,x):
    aa,ea=S.trace(a,x)
    if mode=='K':bb,eb=S.trace(b,x)
    else:bb,eb=b,[]
    pa,pea=P.splay_trace(ptr(a),x)
    if mode=='K':pb,peb=P.splay_trace(ptr(b),x)
    else:pb,peb=ptr(b),[]
    ev=lambda es:[[e['case'],e['lo'],e['hi'],e['orient']] for e in es]
    ck(raw(aa)==rp(pa) and raw(bb)==rp(pb),'source engines endpoints agree')
    ck([list(e) for e in ea]==ev(pea) and [list(e) for e in eb]==ev(peb),'all oriented events agree')
    da=S.lookup(a,x)[1];db=S.lookup(b,x)[1] if mode=='K' else None;ac=len(ea);q=sum(e[0]!='ZIG' for e in eb);z=sum(e[0]=='ZIG' for e in eb)
    ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'source units')
    return aa,bb,{'label':label,'source_A':raw(a),'source_B':raw(b),'mode':mode,'key':x,'destination_A':raw(aa),'destination_B':raw(bb),
      'dA':da,'dB':db,'a':ac,'q':q,'z':z,'events_A':ev(pea),'events_B':ev(peb),'budget':2*ac-q}

def main():
    ck((OUT/'BN00_FOUR_RULE_GATE.md').is_file(),'written gate precedes audit')
    prior=OUT.parent/'route_c_p_envelope_correction_20261031_v001'
    pe=json.loads((prior/'p_envelope_certificate.json').read_text(encoding='utf-8'))
    entry=json.loads((prior/'entry_source_pins.json').read_text(encoding='utf-8'));paths=set(entry['files'])
    paths.update(prior.relative_to(ROOT).as_posix()+'/'+p for p in ['PE00_FOUR_RULE_GATE.md','PE01_EXPLICIT_CORRECTION_AND_DELETE.md','PE02_EXACT_EXTREMA_AND_B_OBSTRUCTION.md','PE03_SOURCE_REPLAY_AND_VERIFICATION.md','PE04_STRATEGY_REVIEW.md','PE05_FINAL_REPORT.md','p_envelope_certificate.json','independent_audit.json','final_integrity.json'])
    rap=OUT.parent/'route_c_analytic_20261030_v001/six_key_closed_controls.json'
    fxp=OUT.parent/'route_c_fixed_exact_pairs_20261031_v001/fixed_exact_pair_certificate.json'
    paths.update([rap.relative_to(ROOT).as_posix(),fxp.relative_to(ROOT).as_posix()])
    pins={p:sha(ROOT/p) for p in sorted(paths)}
    ck(all(pins[p]==h for p,h in entry['files'].items()),'all inherited pins unchanged')
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    ck(not git('status','--porcelain=v1','--untracked-files=no'),'tracked entry clean')
    save('entry_source_pins.json',{'date':'2026-10-31','head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),
      'files':pins,'stage11g_all_files':entry['stage11g_all_files'],'gate_sha256':sha(OUT/'BN00_FOUR_RULE_GATE.md')})
    graphs=pe['matching_graphs'].copy();ck(len(graphs)==8,'inherit eight local PE graphs')
    controls=[]
    for r in pe['controls']:
        _,_,row=edge('normalized_'+r['label'],dec(r['source_A']),dec(r['source_B']),r['mode'],r['key'])
        ms=4;md=4 if r['mode']=='D' else 5;ps=r['J_source']-ms;pd=r['J_destination']-md
        row.update({'valuation_kind':'EXACT_INHERITED_PE','source_graph':r['source_graph'],'destination_graph':r['destination_graph'],
          'J_source':r['J_source'],'J_destination':r['J_destination'],'M_source':ms,'M_destination':md,
          'Phi_source':ps,'Phi_destination':pd,'R_source':ps-graphs[r['source_graph']]['P'],'R_destination':pd-graphs[r['destination_graph']]['P'],
          'delta_Phi':pd-ps,'whole_law_holds':pd-ps<=row['budget']})
        ck(row['whole_law_holds'],'normalization repairs previous safeguards');controls.append(row)
    fx=json.loads(fxp.read_text(encoding='utf-8'))
    old=next(r for r in fx['controls'] if r['label']=='helper_L_m0')
    astar=dec(old['destination_A']);b=dec(old['source_B']);c=dec(old['destination_B'])
    aux=S.node(3,vine(1,2),vine(4,6))
    specs=[('starved_helper_source',astar,b,[((3,6),(3,3))],[],[(3,3)]),
      ('starved_helper_destination',astar,c,[((3,5),(3,3))],[(3,5)],[]),
      ('M_source_attaining_root3',aux,b,[],[],[])]
    graphs += [graph(*s) for s in specs]
    graphs += [graph('reflection_'+label,mir(a,6),mir(bb,6),[(mi(I),mi(J)) for I,J in pairs],[mi(I) for I in cl],[mi(J) for J in cr]) for label,a,bb,pairs,cl,cr in specs]
    ck([g['P'] for g in graphs[8:]]==[4,2,5]*2,'new local P and maximizing witness')
    for label,a0,b0,sg,dg in [('starved_L_KEEP2',astar,b,8,9),('reflection_starved_L_KEEP2',mir(astar,6),mir(b,6),11,12)]:
        x=2 if sg==8 else 5
        _,_,row=edge(label,a0,b0,'K',x)
        ck((row['destination_A'],row['destination_B'])==(graphs[dg]['A'],graphs[dg]['B']),'new source endpoints match bound graphs')
        row.update({'valuation_kind':'CERTIFIED_BOUNDS','source_graph':sg,'destination_graph':dg,
          'J_source':4,'M_source':5,'Phi_source':-1,'R_source':-5,
          'J_destination_lower':2,'M_destination_upper':4,'Phi_destination_lower':-2,
          'required_Phi_destination_upper':-3,'delta_Phi_lower':-1,'law_refuted_by_bound':True})
        ck((row['a'],row['q'],row['z'],row['budget'])==(0,2,0,-2),'actual starved full-q requirement');controls.append(row)
    ra=json.loads(rap.read_text(encoding='utf-8'))['controls'][0]
    idx=ra['zero_helper_index'];word=ra['word'][:idx]+[['D',2],['K',2]]+ra['word'][idx+1:]
    aa=dec(ra['initial_A']);bb=dec(ra['initial_B']);ia,ib=aa,bb;replay=[]
    for i,(mode,x) in enumerate(word):aa,bb,row=edge('closed_'+str(i),aa,bb,mode,x);replay.append(row)
    ck(aa==ia and bb==ib,'actual diagonal pair closure')
    bad=replay[idx+1];ck(bad['source_A']==raw(astar) and bad['source_B']==raw(b),'starved counteredge physically reached')
    At=sum(r['a'] for r in replay);Qt=sum(r['q'] for r in replay);Zt=sum(r['z'] for r in replay)
    ck((At,Qt,Zt)==(16,4,2),'inserting DELETE splits the old helper without changing totals')
    save('b_normalization_certificate.json',{'date':'2026-10-31','n':6,'matching_graphs':graphs,'controls':controls,
      'source_M_maximizer_graph':10,'reflected_source_M_maximizer_graph':13,
      'coefficient_obstruction':{'old_zero_double_edge_J_delta':1,'old_zero_double_edge_M_delta':1,'necessary_c6_lower':1,
        'helper_J_delta_lower':-2,'helper_M_delta_upper':-1,'helper_q':2,'necessary_c6_upper_under_c6_nonnegative':0},
      'closed_witness':{'initial_A':raw(ia),'initial_B':raw(ib),'word':word,'failed_edge_index':idx+1,'full_replay':replay,'A':At,'Q_B':Qt,'Z_B':Zt},
      'no_exact_destination_J_M_or_Phi_claimed_for_helper':True,'no_other_replay_Phi_labels_claimed':True,
      'finite_potential_fits':0,'new_pair_graphs':0,'new_metric_graphs':0,'new_BFS_calls':0,'auxiliary_trees_enumerated':0})
    print(json.dumps({'matching_duals':len(graphs),'new_helper_P_values':[g['P'] for g in graphs[8:]],
      'old_controls':[{k:r[k] for k in ['label','Phi_source','Phi_destination','R_source','R_destination','whole_law_holds']} for r in controls[:4]],
      'new_failure':{k:controls[4][k] for k in ['a','q','z','Phi_source','Phi_destination_lower','required_Phi_destination_upper']},
      'closed_word':word,'totals':[At,Qt,Zt],'source_pins':len(pins)},indent=2))

if __name__=='__main__':main()
