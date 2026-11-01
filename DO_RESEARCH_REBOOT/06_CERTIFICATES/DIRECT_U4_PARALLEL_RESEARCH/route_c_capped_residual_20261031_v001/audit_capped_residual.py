"""One explicit capped residual repair, inherited controls and one safeguard.

All matching values are exact current-pair evaluations. No potential fitting,
larger corpus, parameter search or source-state pair graph is involved.
"""
from pathlib import Path
from collections import deque
import hashlib,json,subprocess,sys

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
PRIOR=OUT.parent/'route_c_fixed_exact_pairs_20261031_v001'
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
    ks=S.inorder(t)
    return {(ks[0],ks[-1])}|clades(t[2])|clades(t[3])
def proper(t):
    ks=S.inorder(t);c=clades(t)
    if ks:c.remove((ks[0],ks[-1]))
    return sorted(c)

def residual(left,right):
    n=len(left);ck(n==len(right),'equal residual sides')
    adj=[[j for j,J in enumerate(right) if I[0]==J[0] or I[1]==J[1]] for I in left];mr=[None]*n
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
    ck(mu==len(covl)+len(covr) and all(i in covl or j in covr for i,row in enumerate(adj) for j in row),'exact matching-cover certificate')
    return {'left_residual':[list(i) for i in left],'right_residual':[list(j) for j in right],
      'adjacency':adj,'matching':mat,'cover_left':covl,'cover_right':covr,'mu':mu}

GRAPHS=[];CACHE={};INHERITED={}
def values(a,b):
    key=(a,b)
    if key not in CACHE:
        if key in INHERITED:
            oldid,oldg=INHERITED[key];g={**oldg,'origin':'inherited fixed_exact_pair_certificate graph '+str(oldid)}
        else:
            l=proper(a);r=proper(b);common=sorted(set(l)&set(r));cs=set(common)
            g={'A':raw(a),'B':raw(b),'all_left':[list(i) for i in l],'all_right':[list(j) for j in r],
              'forced_exact_intervals':[list(i) for i in common],**residual([i for i in l if i not in cs],[j for j in r if j not in cs]),
              'origin':'new fixed current-pair evaluation'}
            g['protected_rank']=len(common)+g['mu'];g['Ehat']=len(l)-g['protected_rank']
        CACHE[key]=len(GRAPHS);GRAPHS.append(g)
    idx=CACHE[key];g=GRAPHS[idx];n=len(S.inorder(a));f=n-1-len(g['forced_exact_intervals'])
    eh=g['Ehat'];cap=max(0,n//2-2);j=max(eh,f-cap)
    ck(j==f-min(g['mu'],cap) and eh<=j<=f,'explicit cap formula and bounds')
    return {'F':f,'Ehat':eh,'J':j,'cap':cap,'graph_id':idx}

def edge(label,a,b,mode,x,meta=None):
    ap,ea=S.trace(a,x)
    if mode=='K':bp,eb=S.trace(b,x)
    else:bp=b;eb=[]
    pa,pea=P.splay_trace(ptr(a),x)
    if mode=='K':pb,peb=P.splay_trace(ptr(b),x)
    else:pb,peb=ptr(b),[]
    ck(pr(pa)==raw(ap) and pr(pb)==raw(bp),'full source engine agreement')
    ev=lambda es:[[e['case'],e['lo'],e['hi'],e['orient']] for e in es]
    ck(ev(pea)==[list(e) for e in ea] and ev(peb)==[list(e) for e in eb],'all oriented events agree')
    da=S.lookup(a,x)[1];db=S.lookup(b,x)[1] if mode=='K' else None
    ac=len(ea);q=sum(e[0]!='ZIG' for e in eb);z=sum(e[0]=='ZIG' for e in eb)
    ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'source costs')
    v0=values(a,b);vm=values(ap,b);v1=values(ap,bp)
    ck(abs(vm['J']-v0['J'])<=da,'concrete A bound')
    row={'label':label,'mode':mode,'key':x,'source_A':raw(a),'source_B':raw(b),'destination_A':raw(ap),'destination_B':raw(bp),
       'dA':da,'dB':db,'a':ac,'q':q,'z':z,'events_A':ev(pea),'events_B':ev(peb),
       'source_values':v0,'after_A_values':vm,'destination_values':v1,
       'delta_J':v1['J']-v0['J'],'budget':2*ac-q,'inequality_holds':v1['J']-v0['J']<=2*ac-q}
    if meta is not None:row['meta']=meta
    return ap,bp,row

def word_to(start,goal):
    queue=deque([start]);parent={start:None};expanded=requests=0
    while queue and goal not in parent:
        t=queue.popleft();expanded+=1
        for x in range(1,7):
            u=S.trace(t,x)[0];requests+=1
            if u not in parent:parent[u]=(t,x);queue.append(u)
    ck(goal in parent,'six-key prefix exists');v=goal;word=[]
    while v!=start:
        u,x=parent[v];word.append(x);v=u
    return word[::-1],{'visited_single_trees':len(parent),'expanded_single_trees':expanded,'requests_examined':requests}

def main():
    cc=OUT.parent/'route_c_clade_correction_20261031_v001'
    dep=[ROOT/'python/independent/splay.py',ROOT/'python/liquidity/legacy_embedding.py',ROOT/'DO_RESEARCH_REBOOT/RESEARCH_RULES.md',
      cc/'CC01_SOURCE_ROTATION_IDENTITY.md',PRIOR/'FX01_DEFINITION_AND_DELETE.md',PRIOR/'FX02_OPPOSITE_VINE_PROOF.md',
      PRIOR/'FX03_ARBITRARY_FRINGE_HELPER_PROOF.md',PRIOR/'FX04_FULL_LAW_COUNTEREXAMPLE_AND_REPLAY.md',PRIOR/'FX05_UPDATED_STRATEGY_REVIEW.md',
      PRIOR/'fixed_exact_pair_certificate.json',PRIOR/'helper_boundary_certificate.json',PRIOR/'independent_audit.json',
      ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/11G_FOUR_RULE_FREEZE.md',
      ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py',
      ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/STRICT_HIGH_COMPILER.py']
    git=lambda *a:subprocess.check_output(['git','-C',str(ROOT),*a]).decode().strip()
    ck(not git('status','--porcelain=v1','--untracked-files=no'),'tracked tree clean')
    pins={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in dep}
    save('entry_source_pins.json',{'date':'2026-10-31','head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),'files':pins})
    old=json.loads((PRIOR/'fixed_exact_pair_certificate.json').read_text(encoding='utf-8'))
    ck(json.loads((PRIOR/'independent_audit.json').read_text(encoding='utf-8'))['status']=='PASS','inherited verification')
    for i,g in enumerate(old['protected_matching_graphs']):INHERITED[(dec(g['A']),dec(g['B']))]=(i,g)
    controls=[]
    for r in old['controls']:
        _,_,row=edge('reused_'+r['label'],dec(r['source_A']),dec(r['source_B']),r['mode'],r['key'],r.get('meta'))
        ck(row['inequality_holds'],'all prior named/source controls repaired');controls.append(row)
    hook=controls[-1]
    ck((hook['source_values']['J'],hook['destination_values']['J'],hook['a'],hook['q'])==(4,2,0,2),'old starved six-key KEEP now paid')
    oldL=next(r for r in old['controls'] if r['label']=='helper_L_m0')
    _,_,derived=edge('derived_starved_L_helper_B',dec(oldL['destination_A']),dec(oldL['source_B']),'K',oldL['key'])
    ck((derived['source_values']['J'],derived['destination_values']['J'],derived['a'],derived['q'])==(4,2,0,2),'known starved B phase also paid');controls.append(derived)
    N=lambda k,l=S.LEAF,r=S.LEAF:S.node(k,l,r)
    a=N(1,S.LEAF,N(5,N(4,N(3,N(2))),N(6)))
    b=N(5,N(4,N(3,N(2,N(1)))),N(6))
    _,_,bad=edge('padded_five_core_hook_safeguard',a,b,'K',1);controls.append(bad)
    ck((bad['source_values']['F'],bad['source_values']['Ehat'],bad['destination_values']['F'],bad['destination_values']['Ehat'])==(4,1,2,2),'aggregation obstruction coordinates')
    ck((bad['a'],bad['q'],bad['z'],bad['delta_J'],bad['budget'])==(0,2,0,-1,-2),'new full-law failure')
    prefix,search=word_to(b,a)
    word=[('D',x) for x in prefix]+[('K',1)]+[('K',x) for x in range(1,7)]+[('K',5)]
    aa=bb=b;rows=[]
    for j,(mode,x) in enumerate(word):aa,bb,r=edge('closed_'+str(j),aa,bb,mode,x);rows.append(r)
    ck(aa==bb==b,'actual full pair closure')
    failed=len(prefix);ck(rows[failed]['source_A']==raw(a) and rows[failed]['source_B']==raw(b) and rows[failed]['delta_J']==-1,'new counteredge reached')
    At=sum(r['a'] for r in rows);Qt=sum(r['q'] for r in rows);Zt=sum(r['z'] for r in rows)
    ck(Qt<=2*At,'no Coarse-Double counterexample')
    opp=controls[0]
    ck((opp['source_values']['F'],opp['source_values']['Ehat'],opp['destination_values']['F'],opp['destination_values']['Ehat'])==(5,5,4,2),'opposite-vine aggregation coordinates')
    obstruction={'n':6,'class':'J=phi_n(F,Ehat), coordinatewise nondecreasing and Ehat<=J<=F',
      'opposite_source':[5,5],'opposite_destination':[4,2],'opposite_budget':-2,
      'padded_source':[4,1],'padded_destination':[2,2],'padded_budget':-2,
      'forced_diagonal_values':{'phi(5,5)':5,'phi(2,2)':2},
      'necessary_inequalities':['phi(4,2)<=3','phi(4,1)>=4','phi(4,1)<=phi(4,2)'],
      'contradiction':'4<=phi(4,1)<=phi(4,2)<=3',
      'cap_corollary':'At n=6 opposite vines require cap>=1, padded hook requires cap=0; no nonnegative size-dependent cap solves full B repayment',
      'scope':'This excludes the stated monotone scalar aggregation class, not all structural corrections.'}
    result={'status':'FOUR_NAMED_LAWS_ACHIEVED_BUT_FULL_POTENTIAL_AND_MONOTONE_AGGREGATION_CLASS_REFUTED',
       'candidate':'J=max(Ehat,F-t_n)=F-min(mu,t_n), t_n=max(0,floor(n/2)-2)',
       'controls':controls,'protected_matching_graphs':GRAPHS,'monotone_obstruction':obstruction,
       'closed_witness':{'initial_A':raw(b),'initial_B':raw(b),'word':word,'failed_edge_index':failed,'full_replay':rows,
          'A':At,'Q_B':Qt,'Z_B':Zt,'actual_pair_closure':True},'single_tree_connector_search':search,
       'four_named_requirements_achieved':True,'global_candidate_refuted':True,
       'finite_potential_fits':0,'new_pair_state_graphs':0,'larger_helper_samples':0,'connector_BFS_calls':1,
       'CoarseDouble_refuted':False,'next_automatic_campaign':None}
    save('capped_residual_certificate.json',result)
    changed=[p for p,h in pins.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
    ck(not changed and not git('status','--porcelain=v1','--untracked-files=no'),'preservation')
    save('integrity.json',{'status':'PASS','inherited_pins_changed':changed,'head':git('rev-parse','HEAD'),
       'branch':git('branch','--show-current'),'Stage11G_writes_performed':False})
    print(json.dumps({'status':result['status'],'old_starved_KEEP':{'J_source':4,'J_destination':2,'q':2},
      'opposite_vines':{'J_source':opp['source_values']['J'],'J_destination':opp['destination_values']['J'],'q':opp['q']},
      'new_safeguard':{k:bad[k] for k in ['a','q','z','delta_J','budget']},'new_safeguard_values':[bad['source_values']['J'],bad['destination_values']['J']],
      'matching_graphs':len(GRAPHS),'closed_word_accesses':len(rows),'closed_totals':{'A':At,'Q_B':Qt,'Z_B':Zt},
      'connector_search':search,'monotone_class_obstruction':obstruction['contradiction'],'finite_fits':0},indent=2))

if __name__=='__main__':main()
