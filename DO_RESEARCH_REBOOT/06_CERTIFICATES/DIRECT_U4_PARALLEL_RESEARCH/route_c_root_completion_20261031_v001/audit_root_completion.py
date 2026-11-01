"""Explicit one-root completion potential; no fitted potential values."""
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
def save(n,v):
    with (OUT/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
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
def vine(lo,hi,left=False):
    t=S.LEAF
    if left:
        for k in range(lo,hi+1):t=S.node(k,t,S.LEAF)
    else:
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
def key(a,b):return json.dumps([raw(a),raw(b)],separators=(',',':'))
def ev(es):return [[e['case'],e['lo'],e['hi'],e['orient']] for e in es]
GRAPHS=[];CACHE={};INHERITED={}
def pval(a,b,empty=False):
    k=key(a,b)
    if k not in CACHE:
        if k in INHERITED:g=INHERITED[k]
        else:
            ck(empty,'only explicitly empty new residual graphs allowed')
            aa=proper(a);bb=proper(b);r=a[1];common=sorted(set(aa)&set(bb));cs=set(common)
            left=[I for I in aa if I not in cs];right=[J for J in bb if J not in cs and not (J[0]<=r<=J[1])]
            adj=[[j for j,J in enumerate(right) if I[0]==J[0] or I[1]==J[1]] for I in left]
            ck(not any(adj),'new graphs have no edges, no matching solver')
            f=len(aa)-len(common)
            g={'A':raw(a),'B':raw(b),'root_A':r,'all_A_intervals':[list(I) for I in aa],'all_B_intervals':[list(J) for J in bb],
              'forced_exact_pairs':[list(I) for I in common],'left_residual':[list(I) for I in left],'eligible_right_residual':[list(J) for J in right],
              'ineligible_B_intervals':[list(J) for J in bb if J[0]<=r<=J[1]],'adjacency':adj,'matching':[],'cover_left':[],'cover_right':[],
              'mu_root':0,'F':f,'P':f,'origin':'new empty residual graph from analytic seven-key family'}
        CACHE[k]=len(GRAPHS);GRAPHS.append(g)
    i=CACHE[k];g=GRAPHS[i]
    return {'P':g['P'],'graph_id':i}

def completion(a,b):
    r=a[1];c,es=S.trace(b,r);pc,pes=P.splay_trace(ptr(b),r)
    ck(raw(c)==rp(pc) and [list(e) for e in es]==ev(pes),'completion uses exact source operation')
    n=len(S.inorder(a));ck(S.inorder(a)==S.inorder(b),'same source keys')
    common=sorted(set(proper(a))&set(proper(c)));f=n-1-len(common);q=sum(e[0]!='ZIG' for e in es);z=sum(e[0]=='ZIG' for e in es);d=S.lookup(b,r)[1]
    ck(q==d//2 and z==d%2 and c[1]==r,'completion depth and root')
    return {'root_A':r,'completed_B':raw(c),'completion_depth':d,'completion_q':q,'completion_z':z,
      'completion_events':ev(pes),'common_terminal_intervals':[list(I) for I in common],'F_terminal':f,'Phi':f+q}

def edge(label,a,b,mode,x,local_p=False,empty=False):
    aa,ea=S.trace(a,x)
    if mode=='K':bb,eb=S.trace(b,x)
    else:bb,eb=b,[]
    pa,pea=P.splay_trace(ptr(a),x)
    if mode=='K':pb,peb=P.splay_trace(ptr(b),x)
    else:pb,peb=ptr(b),[]
    ck(raw(aa)==rp(pa) and raw(bb)==rp(pb) and [list(e) for e in ea]==ev(pea) and [list(e) for e in eb]==ev(peb),'actual full source engines agree')
    da=S.lookup(a,x)[1];db=S.lookup(b,x)[1] if mode=='K' else None;ac=len(ea);q=sum(e[0]!='ZIG' for e in eb);z=sum(e[0]=='ZIG' for e in eb)
    ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'actual source units')
    v0,vm,v1=completion(a,b),completion(aa,b),completion(aa,bb)
    if mode=='K':ck(v1['Phi']-vm['Phi']==-q,'full B identity exactly')
    delta=v1['Phi']-v0['Phi'];budget=2*ac-q
    row={'label':label,'source_A':raw(a),'source_B':raw(b),'mode':mode,'key':x,'destination_A':raw(aa),'destination_B':raw(bb),
      'dA':da,'dB':db,'a':ac,'q':q,'z':z,'events_A':ev(pea),'events_B':ev(peb),
      'source_completion':v0,'after_A_completion':vm,'destination_completion':v1,'delta_Phi':delta,'budget':budget,'whole_law_holds':delta<=budget}
    if local_p:
        ps,pd=pval(a,b,empty),pval(aa,bb,empty)
        row.update({'source_P':ps,'destination_P':pd,'R_source':v0['Phi']-ps['P'],'R_destination':v1['Phi']-pd['P']})
    return aa,bb,row

def main():
    ck((OUT/'CP00_FOUR_RULE_GATE.md').is_file(),'written gate exists before audit')
    prior=OUT.parent/'route_c_joint_alignment_correction_20261031_v001'
    old=json.loads((prior/'joint_alignment_certificate.json').read_text(encoding='utf-8'))
    for i,g in enumerate(old['matching_graphs']):INHERITED[key(dec(g['A']),dec(g['B']))]={**g,'inherited_from_JA_graph':i}
    entry=json.loads((prior/'entry_source_pins.json').read_text(encoding='utf-8'));paths=set(entry['files'])
    paths.update(prior.relative_to(ROOT).as_posix()+'/'+p for p in ['JA00_FOUR_RULE_GATE.md','JA01_JOINT_CONSTRUCTION_AND_PARTIAL_LAWS.md','JA02_EQUAL_ROOT_DELETE_AND_CLASS_OBSTRUCTION.md','JA03_STRATEGY_REVIEW.md','JA04_FINAL_REPORT.md','joint_alignment_certificate.json','independent_audit.json','final_integrity.json'])
    paths.add((OUT.parent/'route_c_clade_correction_20261031_v001/CC02_UNBOUNDED_CORRECTION_AND_PARTIAL_LAWS.md').relative_to(ROOT).as_posix())
    pins={p:sha(ROOT/p) for p in sorted(paths)}
    ck(all(pins[p]==h for p,h in entry['files'].items()),'all inherited pins unchanged')
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    ck(not git('status','--porcelain=v1','--untracked-files=no'),'tracked entry clean')
    save('entry_source_pins.json',{'date':'2026-10-31','head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),
      'files':pins,'stage11g_all_files':entry['stage11g_all_files'],'gate_sha256':sha(OUT/'CP00_FOUR_RULE_GATE.md')})
    controls=[]
    for label,row in [('previous_equal_root_DELETE6',old['controls'][-1]),('starved_helper_KEEP2',old['controls'][5])]:
        _,_,r=edge(label,dec(row['source_A']),dec(row['source_B']),row['mode'],row['key'],True);ck(r['whole_law_holds'],'earlier required control paid');controls.append(r)
    n=7;a=S.node(1,S.LEAF,S.node(n,vine(2,n-1,True),S.LEAF));b=vine(1,n)
    aa,_,bad=edge('odd_vine_middle_DELETE7',a,b,'D',7,True,True);controls.append(bad)
    ck((bad['source_completion']['F_terminal'],bad['destination_completion']['F_terminal'],bad['source_completion']['completion_q'],bad['destination_completion']['completion_q'],bad['delta_Phi'],bad['budget'])==(5,5,0,3,3,2),'registered analytic odd-family failure')
    reflections=[]
    for row in controls:
        nn=len(S.inorder(dec(row['source_A'])))
        _,_,r=edge('reflection_'+row['label'],mirror(dec(row['source_A']),nn),mirror(dec(row['source_B']),nn),row['mode'],nn+1-row['key'],True,nn==7)
        ck((r['source_completion']['Phi'],r['destination_completion']['Phi'],r['a'],r['q'],r['z'])==(row['source_completion']['Phi'],row['destination_completion']['Phi'],row['a'],row['q'],row['z']),'reflected values/costs');reflections.append(r)
    # One fixed n7 single-tree connector only. Phi is not evaluated here.
    queue=deque([b]);prev={b:None};expanded=requests=0
    while queue:
        t=queue.popleft()
        if t==a:break
        expanded+=1
        for x in range(1,n+1):
            u,_=S.trace(t,x);requests+=1
            if u not in prev:prev[u]=(t,x);queue.append(u)
    ck(a in prev and len(prev)<=429,'bounded fixed-witness source connector found')
    prefix=[];cur=a
    while prev[cur] is not None:
        parent,x=prev[cur];prefix.append(['D',x]);cur=parent
    prefix.reverse();failed=len(prefix)
    word=prefix+[['D',7]]+[['K',x] for x in range(1,8)]+[['K',x] for x in range(6,0,-1)]
    ca=cb=b;replay=[]
    for i,(mode,x) in enumerate(word):ca,cb,row=edge('closed_'+str(i),ca,cb,mode,x);replay.append(row)
    ck(ca==cb==b,'actual paired diagonal closure')
    ck(replay[failed]['source_A']==raw(a) and replay[failed]['source_B']==raw(b),'analytic failure reached')
    At=sum(r['a'] for r in replay);Qt=sum(r['q'] for r in replay);Zt=sum(r['z'] for r in replay)
    ck(Qt==0 and Zt==12 and sum(r['delta_Phi'] for r in replay)==0,'actual totals and explicit potential telescope')
    save('root_completion_certificate.json',{'date':'2026-10-31','controls':controls,'reflections':reflections,'matching_graphs':GRAPHS,
      'closed_witness':{'initial_A':raw(b),'initial_B':raw(b),'word':word,'failed_edge_index':failed,'full_replay':replay,'A':At,'Q_B':Qt,'Z_B':Zt},
      'connector':{'single_tree_BFS_calls':1,'n':7,'states_visited':len(prev),'states_expanded':expanded,'source_requests':requests,'potential_evaluations_during_BFS':0},
      'all_odd_family':{'n':'odd n>=7','source_F_terminal':'n-2','destination_F_terminal':'n-2','source_completion_q':0,'destination_completion_q':'(n-1)/2','actual_a':1,'actual_q':0,'delta_Phi':'(n-1)/2','budget':2},
      'terminal_scalar_class':'arbitrary f_n(F(A,S_root(A) B))+floor(d_B(root(A))/2); f_n cancels on equal F terminal values',
      'finite_potential_fits':0,'new_pair_graphs':0,'new_metric_graphs':0,'matching_solver_calls':0})
    print(json.dumps({'controls':[{ 'label':r['label'],'Phi_source':r['source_completion']['Phi'],'Phi_destination':r['destination_completion']['Phi'],
      'R_source':r['R_source'],'R_destination':r['R_destination'],'a':r['a'],'q_actual':r['q'],'q_completion_source':r['source_completion']['completion_q'],
      'q_completion_destination':r['destination_completion']['completion_q'],'budget':r['budget'],'holds':r['whole_law_holds']} for r in controls],
      'local_duals':len(GRAPHS),'closed_word':word,'totals':[At,Qt,Zt],'connector_states':len(prev),'source_pins':len(pins)},indent=2))

if __name__=='__main__':main()
