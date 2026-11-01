"""Fixed exact-pair matching repair: exact source controls and one safeguard.

No potential fit or source-state pair graph. Residual maxima carry equal-size
matching/vertex-cover certificates. Uniform helper proofs use a separate
symbolic core/port certificate, not expanded finite samples.
"""
from pathlib import Path
from collections import deque
import sys,json,hashlib,subprocess

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/'python'))
from independent import splay as S
from liquidity import legacy_embedding as P

def ck(ok,msg):
    if not ok:raise AssertionError(msg)
def save(name,value):
    with (OUT/name).open('x',encoding='utf-8') as f:json.dump(value,f,indent=2)
def dec(t):return S.LEAF if t is None else S.node(t[0],dec(t[1]),dec(t[2]))
def raw(t):return None if t==S.LEAF else [t[1],raw(t[2]),raw(t[3])]
def ptr(t):
    if t==S.LEAF:return None
    p=P.mknode(t[1],ptr(t[2]),ptr(t[3]))
    for k in ('l','r'):
        if p[k] is not None:p[k]['p']=p
    return p
def pr(t):return None if t is None else [t['k'],pr(t['l']),pr(t['r'])]
def clades(t):
    if t==S.LEAF:return set()
    keys=S.inorder(t)
    return {(keys[0],keys[-1])}|clades(t[2])|clades(t[3])
def proper(t):
    keys=S.inorder(t);c=clades(t)
    if keys:c.remove((keys[0],keys[-1]))
    return sorted(c)
def F(a,b):return len(S.inorder(a))-len(clades(a)&clades(b))
def mirror(t,n):return S.LEAF if t==S.LEAF else S.node(n+1-t[1],mirror(t[3],n),mirror(t[2],n))

def residual_certificate(left,right):
    adj=[[j for j,J in enumerate(right) if I[0]==J[0] or I[1]==J[1]] for I in left]
    n=len(left);ck(n==len(right),'equal residual sides');mr=[None]*n
    def aug(i,seen):
        for j in adj[i]:
            if j in seen:continue
            seen.add(j)
            if mr[j] is None or aug(mr[j],seen):mr[j]=i;return True
        return False
    for i in range(n):aug(i,set())
    ml={i:j for j,i in enumerate(mr) if i is not None};zl={i for i in range(n) if i not in ml};zr=set();queue=list(zl)
    while queue:
        i=queue.pop()
        for j in adj[i]:
            if ml.get(i)==j or j in zr:continue
            zr.add(j)
            if mr[j] is not None and mr[j] not in zl:zl.add(mr[j]);queue.append(mr[j])
    covl=sorted(set(range(n))-zl);covr=sorted(zr);mat=sorted([[i,j] for i,j in ml.items()]);mu=len(mat)
    ck(mu==len(covl)+len(covr),'matching-cover exact equality')
    ck(all(i in covl or j in covr for i,row in enumerate(adj) for j in row),'all residual edges covered')
    return {'left_residual':[list(i) for i in left],'right_residual':[list(j) for j in right],
       'adjacency':adj,'matching':mat,'cover_left':covl,'cover_right':covr,'mu':mu}

GRAPHS=[];CACHE={}
def evaluate(a,b):
    key=(a,b)
    if key not in CACHE:
        left=proper(a);right=proper(b);common=sorted(set(left)&set(right));sl=set(common)
        residual=residual_certificate([i for i in left if i not in sl],[j for j in right if j not in sl])
        rank=len(common)+residual['mu'];value=len(left)-rank
        ck(0<=value<=F(a,b),'protected deficit lies below F')
        CACHE[key]=len(GRAPHS);GRAPHS.append({'A':raw(a),'B':raw(b),'all_left':[list(i) for i in left],
          'all_right':[list(j) for j in right],'forced_exact_intervals':[list(i) for i in common],
          **residual,'protected_rank':rank,'Ehat':value})
    i=CACHE[key];return GRAPHS[i]['Ehat'],i

def edge(label,a,b,mode,x,meta=None):
    ap,ea=S.trace(a,x)
    if mode=='K':bp,eb=S.trace(b,x)
    else:bp=b;eb=[]
    pa,pea=P.splay_trace(ptr(a),x)
    if mode=='K':pb,peb=P.splay_trace(ptr(b),x)
    else:pb,peb=ptr(b),[]
    ck(pr(pa)==raw(ap) and pr(pb)==raw(bp),'full pointer/frame source states')
    pe=lambda ev:[[e['case'],e['lo'],e['hi'],e['orient']] for e in ev]
    ck(pe(pea)==[list(e) for e in ea] and pe(peb)==[list(e) for e in eb],'oriented source events')
    da=S.lookup(a,x)[1];db=S.lookup(b,x)[1] if mode=='K' else None
    ac=len(ea);q=sum(e[0]!='ZIG' for e in eb);z=sum(e[0]=='ZIG' for e in eb)
    ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'source cost conventions')
    v0,i0=evaluate(a,b);vm,im=evaluate(ap,b);v1,i1=evaluate(ap,bp)
    ck(abs(vm-v0)<=da,'concrete A-motion bound')
    r={'label':label,'mode':mode,'key':x,'source_A':raw(a),'source_B':raw(b),'destination_A':raw(ap),'destination_B':raw(bp),
       'dA':da,'dB':db,'a':ac,'q':q,'z':z,'events_A':pe(pea),'events_B':pe(peb),
       'graph_source_id':i0,'graph_after_A_id':im,'graph_destination_id':i1,
       'Ehat_source':v0,'Ehat_after_A':vm,'Ehat_destination':v1,'delta_Ehat':v1-v0,
       'F_source':F(a,b),'F_destination':F(ap,bp),'budget':2*ac-q,'inequality_holds':v1-v0<=2*ac-q}
    if meta is not None:r['meta']=meta
    return ap,bp,r

N=lambda k,l=S.LEAF,r=S.LEAF:S.node(k,l,r)
def helper(branch,m):
    ck(m in (0,1),'registered fixed helper controls only')
    core=[1,2,3,4,5+m,6+m];c1,c2,c3,c4,c5,c6=core
    fringe=S.LEAF if m==0 else N(5)
    a=N(c6,N(c2,N(c1),N(c3,S.LEAF,N(c4,S.LEAF,N(c5,fringe)))))
    head=N(c1,S.LEAF,N(c2,S.LEAF,N(c3))) if branch=='L' else N(c3,N(c2,N(c1)))
    b=N(c6,N(c5,N(c4,head,fringe)))
    return a,b,c2,{'family':branch,'m':m,'core':core,'fringe_keys':([] if m==0 else [5]),'mirror':False}

def source_word(start,goal):
    queue=deque([start]);parent={start:None};expanded=0;requests=0
    while queue and goal not in parent:
        t=queue.popleft();expanded+=1
        for x in range(1,7):
            u=S.trace(t,x)[0];requests+=1
            if u not in parent:parent[u]=(t,x);queue.append(u)
    ck(goal in parent,'fixed six-key DELETE connector exists');word=[];v=goal
    while v!=start:
        old,x=parent[v];word.append(x);v=old
    return word[::-1],{'visited_single_trees':len(parent),'expanded_single_trees':expanded,'source_requests_examined':requests}

def main():
    prev=OUT.parent/'route_c_endpoint_matching_20261031_v001';ra=OUT.parent/'route_c_analytic_20261030_v001';cc=OUT.parent/'route_c_clade_correction_20261031_v001'
    deps=[ROOT/'python/independent/splay.py',ROOT/'python/liquidity/legacy_embedding.py',ROOT/'DO_RESEARCH_REBOOT/RESEARCH_RULES.md',
      prev/'EM01_DEFINITION_AND_DELETE.md',prev/'EM02_OPPOSITE_VINE_PROOF.md',prev/'EM03_EXACT_HELPER_OBSTRUCTION.md',
      prev/'EM05_MANDATORY_STRATEGY_REVIEW.md',prev/'endpoint_matching_countercertificate.json',prev/'independent_audit.json',
      ra/'RA02_ZERO_HELPER_ARBITRARY_FRINGE_PROOF.md',cc/'CC03_ALL_SIZE_REPAYMENT_OBSTRUCTION.md',
      ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/11G_FOUR_RULE_FREEZE.md',
      ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py',
      ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/STRICT_HIGH_COMPILER.py']
    git=lambda *a:subprocess.check_output(['git','-C',str(ROOT),*a]).decode().strip()
    ck(not git('status','--porcelain=v1','--untracked-files=no'),'tracked tree clean at entry')
    pins={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in deps}
    save('entry_source_pins.json',{'date':'2026-10-31','head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),'files':pins})
    controls=[]
    _,_,v=edge('opposite_vines_6',S.vine_left(6),S.vine(6),'K',6)
    ck((v['Ehat_source'],v['Ehat_destination'],v['delta_Ehat'])==(5,2,-3),'opposite-vine protected count')
    controls.append(v)
    for m in (0,1):
        for branch in ('L','R'):
            a,b,x,meta=helper(branch,m);_,_,r=edge('helper_'+branch+'_m'+str(m),a,b,'K',x,meta)
            ck((r['a'],r['q'])==(1,2),'helper costs')
            ck((r['Ehat_source'],r['Ehat_destination'])==((2,2) if branch=='L' else (3,1)),'fixed helper boundary values')
            ck(r['inequality_holds'],'helper compensation preserved');controls.append(r)
    for branch in ('L','R'):
        a,b,x,meta=helper(branch,0);meta['mirror']=True
        _,_,r=edge('helper_'+branch+'_m0_mirror',mirror(a,6),mirror(b,6),'K',7-x,meta)
        ck((r['Ehat_source'],r['Ehat_destination'])==((2,2) if branch=='L' else (3,1)),'helper reflection');controls.append(r)
    # The independently registered full-law safeguard, after the named tests.
    chain=S.LEAF
    for k in range(2,7):chain=N(k,chain)
    a=N(1,S.LEAF,chain);b=S.vine_left(6)
    _,_,bad=edge('hook_vine_full_law_safeguard',a,b,'K',1);controls.append(bad)
    ck((bad['a'],bad['q'],bad['z'],bad['Ehat_source'],bad['Ehat_destination'])==(0,2,1,1,2),'full B-law counterexample')
    prefix,search=source_word(b,a);word=[('D',x) for x in prefix]+[('K',1)]+[('K',x) for x in range(1,7)]
    aa=bb=b;rows=[]
    for j,(mode,x) in enumerate(word):aa,bb,r=edge('closed_'+str(j),aa,bb,mode,x);rows.append(r)
    ck(aa==bb==b,'actual diagonal paired closure')
    failed=len(prefix);ck(rows[failed]['source_A']==raw(a) and rows[failed]['source_B']==raw(b) and rows[failed]['delta_Ehat']==1,'counteredge reached inside source cycle')
    At=sum(r['a'] for r in rows);Qt=sum(r['q'] for r in rows);Zt=sum(r['z'] for r in rows)
    ck(Qt<=2*At,'no Coarse-Double counterexample')
    result={'status':'THREE_NAMED_LAWS_PROVED_BUT_UNIVERSAL_B_REPAYMENT_REFUTED',
      'candidate':'Ehat=(n-1)-c-mu: all exact common proper pairs fixed, mu maximum residual endpoint matching',
      'controls':controls,'protected_matching_graphs':GRAPHS,
      'closed_witness':{'initial_A':raw(b),'initial_B':raw(b),'word':word,'failed_edge_index':failed,'full_replay':rows,
         'A':At,'Q_B':Qt,'Z_B':Zt,'actual_pair_closure':True},'single_tree_connector_search':search,
      'named_partial_results':['universal DELETE','full q on opposite vines at every size','both arbitrary-fringe helper branches'],
      'full_universal_potential':False,'finite_potential_fits':0,'new_source_state_graphs':0,'connector_BFS_calls':1,
      'larger_helper_controls':False,'CoarseDouble_refuted':False,'next_automatic_campaign':None}
    save('fixed_exact_pair_certificate.json',result)
    changes=[p for p,h in pins.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
    ck(not changes and not git('status','--porcelain=v1','--untracked-files=no'),'source preservation')
    save('integrity.json',{'status':'PASS','pinned_inputs_changed':changes,'head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),'Stage11G_writes_performed':False})
    print(json.dumps({'status':result['status'],'positive_controls':[{k:r[k] for k in ['label','Ehat_source','Ehat_destination','a','q']} for r in controls[:-1]],
      'full_law_counterexample':{k:bad[k] for k in ['Ehat_source','Ehat_destination','a','q','z','delta_Ehat','budget']},
      'closed_word_accesses':len(rows),'closed_totals':{'A':At,'Q_B':Qt,'Z_B':Zt},'matching_graphs':len(GRAPHS),
      'connector_search':search,'finite_fits':0},indent=2))

if __name__=='__main__':main()
