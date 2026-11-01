"""One frozen root-eligible global matching audit, exact dual certificates."""
from pathlib import Path
from collections import deque
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
def dec(t):return S.LEAF if t is None else S.node(t[0],dec(t[1]),dec(t[2]))
def raw(t):return None if t==S.LEAF else [t[1],raw(t[2]),raw(t[3])]
def ptr(t):
    if t==S.LEAF:return None
    p=P.mknode(t[1],ptr(t[2]),ptr(t[3]))
    for side in ('l','r'):
        if p[side] is not None:p[side]['p']=p
    return p
def rp(t):return None if t is None else [t['k'],rp(t['l']),rp(t['r'])]
def intervals(t):
    if t==S.LEAF:return set()
    ks=S.inorder(t)
    return {(ks[0],ks[-1])}|intervals(t[2])|intervals(t[3])
def proper(t):
    keys=S.inorder(t);ss=intervals(t)
    if keys:ss.remove((keys[0],keys[-1]))
    return sorted(ss)
def mirror(t,n):return S.LEAF if t==S.LEAF else S.node(n+1-t[1],mirror(t[3],n),mirror(t[2],n))
def vine(lo,hi):
    t=S.LEAF
    for k in range(hi,lo-1,-1):t=S.node(k,S.LEAF,t)
    return t

GRAPHS=[];CACHE={}
def val(a,b):
    if (a,b) not in CACHE:
        keys=S.inorder(a);ck(keys==S.inorder(b),'same source key set')
        r=a[1] if keys else None;ai=proper(a);bi=proper(b);common=sorted(set(ai)&set(bi));cs=set(common)
        ck(all(not (I[0]<=r<=I[1]) for I in common),'exact pairs are root-eligible')
        left=[I for I in ai if I not in cs];right=[J for J in bi if J not in cs and not (J[0]<=r<=J[1])]
        adj=[[j for j,J in enumerate(right) if I[0]==J[0] or I[1]==J[1]] for I in left]
        mr=[None]*len(right)
        def aug(i,seen):
            for j in adj[i]:
                if j in seen:continue
                seen.add(j)
                if mr[j] is None or aug(mr[j],seen):mr[j]=i;return True
            return False
        for i in range(len(left)):aug(i,set())
        ml={i:j for j,i in enumerate(mr) if i is not None};zl={i for i in range(len(left)) if i not in ml};zr=set();queue=list(zl)
        while queue:
            i=queue.pop()
            for j in adj[i]:
                if ml.get(i)==j or j in zr:continue
                zr.add(j)
                if mr[j] is not None and mr[j] not in zl:zl.add(mr[j]);queue.append(mr[j])
        cl=sorted(set(range(len(left)))-zl);cr=sorted(zr);matching=sorted([[i,j] for i,j in ml.items()]);mu=len(matching)
        ck(len(cl)+len(cr)==mu and all(i in cl or j in cr for i,row in enumerate(adj) for j in row),'matching-cover equality')
        f=len(ai)-len(common);value=f-mu;d=S.lookup(b,r)[1] if r is not None else 0
        ck(value>=d,'root depth lower bound')
        g={'A':raw(a),'B':raw(b),'root_A':r,'all_A_intervals':[list(I) for I in ai],'all_B_intervals':[list(J) for J in bi],
          'forced_exact_pairs':[list(I) for I in common],'left_residual':[list(I) for I in left],'eligible_right_residual':[list(J) for J in right],
          'ineligible_B_intervals':[list(J) for J in bi if J[0]<=r<=J[1]],'adjacency':adj,'matching':matching,
          'cover_left':cl,'cover_right':cr,'mu_root':mu,'F':f,'P':value,'d_B_root_A':d}
        CACHE[(a,b)]=len(GRAPHS);GRAPHS.append(g)
    i=CACHE[(a,b)];g=GRAPHS[i]
    return {'F':g['F'],'mu_root':g['mu_root'],'P':g['P'],'root_A':g['root_A'],'d_B_root_A':g['d_B_root_A'],'graph_id':i}

def edge(label,a,b,mode,x):
    ap,ea=S.trace(a,x)
    if mode=='K':bp,eb=S.trace(b,x)
    else:bp,eb=b,[]
    pa,pea=P.splay_trace(ptr(a),x)
    if mode=='K':pb,peb=P.splay_trace(ptr(b),x)
    else:pb,peb=ptr(b),[]
    ev=lambda es:[[e['case'],e['lo'],e['hi'],e['orient']] for e in es]
    ck(raw(ap)==rp(pa) and raw(bp)==rp(pb),'source engine endpoints agree')
    ck([list(e) for e in ea]==ev(pea) and [list(e) for e in eb]==ev(peb),'oriented events agree')
    da=S.lookup(a,x)[1];db=S.lookup(b,x)[1] if mode=='K' else None;ac=len(ea);q=sum(e[0]!='ZIG' for e in eb);z=sum(e[0]=='ZIG' for e in eb)
    ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'source costs')
    v0,vm,v1=val(a,b),val(ap,b),val(ap,bp)
    if mode=='K':ck(v1['P']<=vm['P'],'root-conditioned B nonincrease')
    delta=v1['P']-v0['P'];budget=2*ac-q
    return ap,bp,{'label':label,'source_A':raw(a),'source_B':raw(b),'mode':mode,'key':x,
      'destination_A':raw(ap),'destination_B':raw(bp),'dA':da,'dB':db,'a':ac,'q':q,'z':z,
      'events_A':ev(pea),'events_B':ev(peb),'source_values':v0,'after_A_values':vm,'destination_values':v1,
      'delta_P':delta,'budget':budget,'whole_law_holds':delta<=budget,'B_full_q_holds':v1['P']-vm['P']<=-q}

def main():
    ck((OUT/'RS00_FOUR_RULE_GATE.md').is_file(),'written gate exists before audit')
    prior=OUT.parent/'route_c_crossing_threshold_20261031_v001'
    inherited=json.loads((prior/'entry_source_pins.json').read_text(encoding='utf-8'));paths=set(inherited['files'])
    paths.update(prior.relative_to(ROOT).as_posix()+'/'+p for p in ['CT01_STRUCTURAL_DEFINITION_AND_DELETE_v002.md','CT02_EXACT_REPAYMENT_OBSTRUCTION.md','CT03_STRATEGY_REVIEW.md','CT04_FINAL_REPORT_v002.md','crossing_certificate.json','independent_audit.json','final_integrity.json'])
    for p in ['FX03_ARBITRARY_FRINGE_HELPER_PROOF.md']:
        paths.add((OUT.parent/'route_c_fixed_exact_pairs_20261031_v001'/p).relative_to(ROOT).as_posix())
    pins={p:sha(ROOT/p) for p in sorted(paths)}
    ck(all(pins[p]==h for p,h in inherited['files'].items()),'all inherited pins unchanged')
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    ck(not git('status','--porcelain=v1','--untracked-files=no'),'tracked entry clean')
    save('entry_source_pins.json',{'date':'2026-10-31','head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),
      'files':pins,'stage11g_all_files':inherited['stage11g_all_files'],'gate_sha256':sha(OUT/'RS00_FOUR_RULE_GATE.md')})
    capped=json.loads((OUT.parent/'route_c_capped_residual_20261031_v001/capped_residual_certificate.json').read_text(encoding='utf-8'))
    cross=json.loads((prior/'crossing_certificate.json').read_text(encoding='utf-8'))
    oldhook=next(r for r in capped['controls'] if r['label']=='reused_hook_vine_full_law_safeguard')
    padded=capped['controls'][-1];opposite=capped['controls'][0];transfer=cross['controls'][0]
    controls=[]
    for label,r in [('old_six_key_hook',oldhook),('padded_six_key_hook',padded),('four_key_conflict_transfer',transfer),('six_key_opposite_vines',opposite)]:
        _,_,new=edge(label,dec(r['source_A']),dec(r['source_B']),r['mode'],r['key']);ck(new['whole_law_holds'],'registered starved consumer is paid');controls.append(new)
    n=6;leaf=lambda k:S.node(k,S.LEAF,S.LEAF)
    a=S.node(1,S.LEAF,S.node(n,vine(2,n-1),S.LEAF));b=S.node(2,leaf(1),vine(3,n))
    _,_,bad=edge('root_change_DELETE_family_n6',a,b,'D',n);controls.append(bad)
    ck((bad['source_values']['P'],bad['destination_values']['P'],bad['a'],bad['delta_P'],bad['budget'])==(1,4,1,3,2),'registered one-zig DELETE failure')
    reflections=[]
    for r in controls:
        nn=len(S.inorder(dec(r['source_A'])))
        _,_,m=edge('reflection_'+r['label'],mirror(dec(r['source_A']),nn),mirror(dec(r['source_B']),nn),r['mode'],nn+1-r['key'])
        ck((m['source_values']['P'],m['destination_values']['P'],m['a'],m['q'],m['z'])==(r['source_values']['P'],r['destination_values']['P'],r['a'],r['q'],r['z']),'reflection symmetry')
        reflections.append(m)
    queue=deque([b]);previous={b:None};expanded=requests=0
    while queue:
        t=queue.popleft()
        if t==a:break
        expanded+=1
        for x in range(1,n+1):
            u,_=S.trace(t,x);requests+=1
            if u not in previous:previous[u]=(t,x);queue.append(u)
    ck(a in previous and len(previous)<=132,'fixed six-key single-tree connector found')
    word=[];cur=a
    while previous[cur] is not None:
        parent,x=previous[cur];word.append(['D',x]);cur=parent
    word.reverse();failed=len(word)
    word+=[['D',n]]+[['K',x] for x in range(1,n+1)]+[['K',x] for x in range(n-1,0,-1)]+[['K',2]]
    ca=cb=b;replay=[]
    for i,(mode,x) in enumerate(word):ca,cb,r=edge('closed_'+str(i),ca,cb,mode,x);replay.append(r)
    ck(ca==cb==b,'exact actual pair closure')
    ck(replay[failed]['source_A']==raw(a) and replay[failed]['source_B']==raw(b),'counteredge reached')
    At=sum(r['a'] for r in replay);Qt=sum(r['q'] for r in replay);Zt=sum(r['z'] for r in replay)
    ck(Qt<=2*At,'not a CD counterexample')
    save('root_matching_certificate.json',{'date':'2026-10-31','controls':controls,'reflections':reflections,'matching_graphs':GRAPHS,
      'closed_witness':{'initial_A':raw(b),'initial_B':raw(b),'word':word,'failed_edge_index':failed,'full_replay':replay,'A':At,'Q_B':Qt,'Z_B':Zt},
      'connector':{'single_tree_BFS_calls':1,'n':6,'states_visited':len(previous),'states_expanded':expanded,'source_requests':requests},
      'all_size_DELETE_family':{'n_min':3,'source_F':'n-1','destination_F':'n-1','source_mu':'n-2','destination_mu':1,'source_P':1,'destination_P':'n-2','delta_P':'n-3','a':1,'violates_for':'n>=6'},
      'finite_potential_fits':0,'new_pair_graphs':0})
    print(json.dumps({'controls':[{ 'label':r['label'],'P_source':r['source_values']['P'],'P_destination':r['destination_values']['P'],'a':r['a'],'q':r['q'],'z':r['z'],'budget':r['budget'],'holds':r['whole_law_holds']} for r in controls],
      'closed_word':word,'totals':[At,Qt,Zt],'matching_graphs':len(GRAPHS),'connector_states':len(previous),'source_pins':len(pins)},indent=2))

if __name__=='__main__':main()
