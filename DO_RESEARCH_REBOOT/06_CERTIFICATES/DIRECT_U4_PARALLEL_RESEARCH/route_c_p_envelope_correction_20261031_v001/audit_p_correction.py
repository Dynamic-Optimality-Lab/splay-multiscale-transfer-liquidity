"""Frozen correction audit: eight hand-dual graphs, no matching/metric search."""
from pathlib import Path
import hashlib,json,subprocess,sys
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/'python'))
from independent import splay as S
from liquidity import legacy_embedding as P
def ck(ok,msg):
    if not ok:raise AssertionError(msg)
def save(name,v):
    with (OUT/name).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def raw(t):return None if t==S.LEAF else [t[1],raw(t[2]),raw(t[3])]
def ptr(t):
    if t==S.LEAF:return None
    p=P.mknode(t[1],ptr(t[2]),ptr(t[3]))
    for side in ('l','r'):
        if p[side] is not None:p[side]['p']=p
    return p
def rp(t):return None if t is None else [t['k'],rp(t['l']),rp(t['r'])]
def vine(lo,hi):
    t=S.LEAF
    for k in range(hi,lo-1,-1):t=S.node(k,S.LEAF,t)
    return t
def ints(t):
    if t==S.LEAF:return set()
    ks=S.inorder(t)
    return {(ks[0],ks[-1])}|ints(t[2])|ints(t[3])
def proper(t):
    ks=S.inorder(t);ss=ints(t)
    if ks:ss.remove((ks[0],ks[-1]))
    return sorted(ss)
def mirror(t,n):return S.LEAF if t==S.LEAF else S.node(n+1-t[1],mirror(t[3],n),mirror(t[2],n))
def mi(I,n):return (n+1-I[1],n+1-I[0])

def graph(label,a,b,pairs,cover):
    aa=proper(a);bb=proper(b);r=a[1];common=sorted(set(aa)&set(bb));cs=set(common)
    left=[I for I in aa if I not in cs];right=[J for J in bb if J not in cs and not (J[0]<=r<=J[1])]
    adj=[[j for j,J in enumerate(right) if I[0]==J[0] or I[1]==J[1]] for I in left]
    matching=sorted([[left.index(I),right.index(J)] for I,J in pairs]);cr=sorted(right.index(J) for J in cover)
    ck(len({i for i,j in matching})==len({j for i,j in matching})==len(matching),'distinct matching endpoints')
    ck(all(j in adj[i] for i,j in matching),'genuine hand matching')
    ck(all(j in cr for row in adj for j in row) and len(cr)==len(matching),'hand matching equals right cover')
    f=len(aa)-len(common)
    return {'label':label,'A':raw(a),'B':raw(b),'root_A':r,'all_A_intervals':[list(I) for I in aa],'all_B_intervals':[list(J) for J in bb],
      'forced_exact_pairs':[list(I) for I in common],'left_residual':[list(I) for I in left],'eligible_right_residual':[list(J) for J in right],
      'ineligible_B_intervals':[list(J) for J in bb if J[0]<=r<=J[1]],'adjacency':adj,'matching':matching,
      'cover_left':[],'cover_right':cr,'mu_root':len(matching),'F':f,'P':f-len(matching)}

def edge(label,a,b,mode,x):
    aa,ea=S.trace(a,x)
    if mode=='K':bb,eb=S.trace(b,x)
    else:bb,eb=b,[]
    pa,pea=P.splay_trace(ptr(a),x)
    if mode=='K':pb,peb=P.splay_trace(ptr(b),x)
    else:pb,peb=ptr(b),[]
    ev=lambda es:[[e['case'],e['lo'],e['hi'],e['orient']] for e in es]
    ck(raw(aa)==rp(pa) and raw(bb)==rp(pb),'full source endpoints agree')
    ck([list(e) for e in ea]==ev(pea) and [list(e) for e in eb]==ev(peb),'all oriented events agree')
    da=S.lookup(a,x)[1];db=S.lookup(b,x)[1] if mode=='K' else None;ac=len(ea);q=sum(e[0]!='ZIG' for e in eb);z=sum(e[0]=='ZIG' for e in eb)
    ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'source cost convention')
    return aa,bb,{'label':label,'source_A':raw(a),'source_B':raw(b),'mode':mode,'key':x,'destination_A':raw(aa),'destination_B':raw(bb),
      'dA':da,'dB':db,'a':ac,'q':q,'z':z,'events_A':ev(pea),'events_B':ev(peb),'budget':2*ac-q}

def main():
    ck((OUT/'PE00_FOUR_RULE_GATE.md').is_file(),'written gate precedes audit')
    prior=OUT.parent/'route_c_root_safe_matching_20261031_v001'
    entry=json.loads((prior/'entry_source_pins.json').read_text(encoding='utf-8'));paths=set(entry['files'])
    paths.update(prior.relative_to(ROOT).as_posix()+'/'+p for p in ['RS01_DEFINITION_AND_TRANSPORT_LAWS.md','RS02_NAMED_REPAYMENT_CLASSES.md','RS03_UNBOUNDED_DELETE_OBSTRUCTION.md','RS04_STRATEGY_REVIEW.md','RS05_FINAL_REPORT.md','root_matching_certificate.json','independent_audit.json','final_integrity.json'])
    paths.update((OUT.parent/d/p).relative_to(ROOT).as_posix() for d,p in [
      ('route_c_potential_20261031_v001','SP03_ENVELOPE_LAW_AND_ALL_SIZE_REFUTATION.md'),('route_c_alignment_20261031_v001','AL05_STRATEGY_REVIEW.md')])
    pins={p:sha(ROOT/p) for p in sorted(paths)}
    ck(all(pins[p]==h for p,h in entry['files'].items()),'inherited pins unchanged')
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    ck(not git('status','--porcelain=v1','--untracked-files=no'),'tracked entry clean')
    save('entry_source_pins.json',{'date':'2026-10-31','head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),
      'files':pins,'stage11g_all_files':entry['stage11g_all_files'],'gate_sha256':sha(OUT/'PE00_FOUR_RULE_GATE.md')})
    n=6;leaf=lambda k:S.node(k,S.LEAF,S.LEAF)
    a=S.node(1,S.LEAF,S.node(n,vine(2,n-1),S.LEAF));t=S.node(n,S.node(1,S.LEAF,vine(2,n-1)),S.LEAF)
    b=S.node(2,leaf(1),vine(3,n));c=vine(1,n)
    pairs0=[((k,n-1),(k,n)) for k in range(3,n)]+[((2,n),(n,n))]
    cover0=[(k,n) for k in range(3,n+1)]
    pairs1=[((1,n-1),(1,1))];cover1=[(1,1)]
    pairs2=[((k,n-1),(k,n)) for k in range(3,n)];cover2=[(k,n) for k in range(3,n)]
    specs=[('A_B',a,b,pairs0,cover0),('Tstar_B',t,b,pairs1,cover1),('A_C',a,c,pairs2,cover2),('Tstar_C',t,c,[],[])]
    graphs=[graph(*s) for s in specs]
    graphs += [graph('reflection_'+label,mirror(aa,n),mirror(bb,n),[(mi(I,n),mi(J,n)) for I,J in pairs],[mi(J,n) for J in cover]) for label,aa,bb,pairs,cover in specs]
    ck([g['P'] for g in graphs]==[1,4,1,5]*2,'four analytic P identities and reflections')
    controls=[]
    for label,aa,bb,mode,x,src,dst in [('DELETE_n',a,b,'D',n,0,1),('zero_double_KEEP_1',a,b,'K',1,0,2)]:
        aa1,bb1,r=edge(label,aa,bb,mode,x)
        r.update({'source_graph':src,'destination_graph':dst,'lambda':1,'J_source':3,'J_destination':4,
          'R_source':3-graphs[src]['P'],'R_destination':4-graphs[dst]['P'],'delta_J':1,'whole_law_holds':1<=r['budget']})
        ck((raw(aa1),raw(bb1))==(graphs[dst]['A'],graphs[dst]['B']),'analytic node matches physical endpoint');controls.append(r)
        _,_,m=edge('reflection_'+label,mirror(aa,n),mirror(bb,n),mode,n+1-x)
        m.update({'source_graph':src+4,'destination_graph':dst+4,'lambda':1,'J_source':3,'J_destination':4,
          'R_source':3-graphs[src+4]['P'],'R_destination':4-graphs[dst+4]['P'],'delta_J':1,'whole_law_holds':1<=m['budget']})
        controls.append(m)
    # A->Tstar is the displayed single root zig, hence rho=1 exactly.
    metric={'source_A':raw(a),'auxiliary_Tstar':raw(t),'rho':1,'distance_upper_witness_control':0,
      'distance_lower_reason':'distinct trees have strictly positive integer rotation distance'}
    old=json.loads((prior/'root_matching_certificate.json').read_text(encoding='utf-8'))
    prefix=old['closed_witness']['word'][:old['closed_witness']['failed_edge_index']]
    ck(prefix==[['D',4],['D',6],['D',3],['D',6],['D',1]],'reuse existing explicit connector; no BFS')
    word=prefix+[['K',1]]+[['K',x] for x in range(1,n+1)]+[['K',x] for x in range(n-1,0,-1)]+[['K',2]]
    ca=cb=b;replay=[]
    for i,(mode,x) in enumerate(word):ca,cb,r=edge('closed_'+str(i),ca,cb,mode,x);replay.append(r)
    ck(ca==cb==b,'actual diagonal pair closure')
    ck(replay[5]['source_A']==raw(a) and replay[5]['source_B']==raw(b) and replay[5]['destination_B']==raw(c),'B safeguard reached')
    At=sum(r['a'] for r in replay);Qt=sum(r['q'] for r in replay);Zt=sum(r['z'] for r in replay)
    ck(Qt<=2*At,'not a CD counterexample')
    save('p_envelope_certificate.json',{'date':'2026-10-31','n':n,'matching_graphs':graphs,'controls':controls,'one_rotation_distance':metric,
      'analytic_global_maxima':{'over_B':'n-2','over_C':'n-1','n_min':3,'proof':'PE02_EXACT_EXTREMA_AND_B_OBSTRUCTION.md'},
      'coefficient_formulas':{'Jlambda(A,B)':'max(1,n-2-lambda)','Jlambda(Tstar,B)':'n-2','Jlambda(A,C)':'max(1,n-1-lambda)',
        'lambda_domain':'nonnegative real, allowed to depend on n','same_n6_DELETE_necessary_upper':2,'same_n6_KEEP_necessary_lower':4},
      'closed_witness':{'initial_A':raw(b),'initial_B':raw(b),'word':word,'failed_edge_index':5,'full_replay':replay,'A':At,'Q_B':Qt,'Z_B':Zt},
      'no_J_labels_claimed_on_other_replay_states':True,'finite_potential_fits':0,'new_pair_graphs':0,'new_metric_graphs':0,'new_BFS_calls':0})
    print(json.dumps({'P_values':[g['P'] for g in graphs],'correction_controls':[{k:r[k] for k in ['label','a','q','z','J_source','J_destination','R_source','R_destination','budget','whole_law_holds']} for r in controls],
      'closed_word':word,'totals':[At,Qt,Zt],'matching_duals':len(graphs),'source_pins':len(pins),'new_BFS_calls':0},indent=2))

if __name__=='__main__':main()
