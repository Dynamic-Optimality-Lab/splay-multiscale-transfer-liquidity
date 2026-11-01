"""Exact fixed-candidate audit, stopping at the first helper obstruction.

No fitted potentials or source-state graphs. Each intra-state matching value
has a matching and an equal-cardinality vertex cover as an exact certificate.
"""
from pathlib import Path
import hashlib,json,sys,subprocess

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
    c=clades(t)
    if c:
        keys=S.inorder(t);c.remove((keys[0],keys[-1]))
    return sorted(c)
def f(a,b):return len(S.inorder(a))-len(clades(a)&clades(b))

def graph_certificate(a,b):
    left=proper(a);right=proper(b);n=len(left)
    ck(n==len(right),'same-key proper graph dimensions')
    adj=[[j for j,J in enumerate(right) if I[0]==J[0] or I[1]==J[1]] for I in left]
    mr=[None]*n
    def augment(i,seen):
        for j in adj[i]:
            if j in seen:continue
            seen.add(j)
            if mr[j] is None or augment(mr[j],seen):mr[j]=i;return True
        return False
    for i in range(n):augment(i,set())
    ml={i:j for j,i in enumerate(mr) if i is not None}
    zl={i for i in range(n) if i not in ml};zr=set();queue=list(zl)
    while queue:
        i=queue.pop()
        for j in adj[i]:
            if ml.get(i)==j or j in zr:continue
            zr.add(j)
            if mr[j] is not None and mr[j] not in zl:zl.add(mr[j]);queue.append(mr[j])
    coverL=sorted(set(range(n))-zl);coverR=sorted(zr)
    matching=sorted([[i,j] for i,j in ml.items()]);nu=len(matching)
    ck(len(coverL)+len(coverR)==nu,'exact matching-cover equality')
    ck(all(i in coverL or j in coverR for i,row in enumerate(adj) for j in row),'all graph edges covered')
    return {'left_intervals':[list(i) for i in left],'right_intervals':[list(j) for j in right],
        'adjacency':adj,'matching':matching,'cover_left':coverL,'cover_right':coverR,'nu':nu,'E':n-nu}

GRAPHS=[];CACHE={}
def evaluate(a,b):
    key=(a,b)
    if key not in CACHE:
        CACHE[key]=len(GRAPHS);GRAPHS.append({'A':raw(a),'B':raw(b),**graph_certificate(a,b)})
    k=CACHE[key];return GRAPHS[k]['E'],k

def edge(label,a,b,mode,x):
    ap,ea=S.trace(a,x)
    if mode=='K':bp,eb=S.trace(b,x)
    else:bp=b;eb=[]
    pa,pea=P.splay_trace(ptr(a),x)
    if mode=='K':pb,peb=P.splay_trace(ptr(b),x)
    else:pb,peb=ptr(b),[]
    ck(pr(pa)==raw(ap) and pr(pb)==raw(bp),'full pointer/frame source agreement')
    pea=[[e['case'],e['lo'],e['hi'],e['orient']] for e in pea]
    peb=[[e['case'],e['lo'],e['hi'],e['orient']] for e in peb]
    ck(pea==[list(e) for e in ea] and peb==[list(e) for e in eb],'all oriented events agree')
    da=S.lookup(a,x)[1];db=S.lookup(b,x)[1] if mode=='K' else None
    ac=len(ea);q=sum(e[0]!='ZIG' for e in eb);z=sum(e[0]=='ZIG' for e in eb)
    ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'exact costs')
    e0,i0=evaluate(a,b);em,im=evaluate(ap,b);e1,i1=evaluate(ap,bp)
    ck(abs(em-e0)<=da,'concrete A-motion bound')
    row={'label':label,'mode':mode,'key':x,'source_A':raw(a),'source_B':raw(b),
      'destination_A':raw(ap),'destination_B':raw(bp),'dA':da,'dB':db,'a':ac,'q':q,'z':z,
      'events_A':pea,'events_B':peb,'matching_source_id':i0,'matching_after_A_id':im,'matching_destination_id':i1,
      'E_source':e0,'E_after_A':em,'E_destination':e1,'delta_E':e1-e0,
      'F_source':f(a,b),'F_after_A':f(ap,b),'F_destination':f(ap,bp),
      'repair_source':e0-f(a,b),'repair_destination':e1-f(ap,bp),
      'required_upper_bound':2*ac-q,'inequality_holds':e1-e0<=2*ac-q}
    return ap,bp,row

def main():
    prev=OUT.parent/'route_c_clade_correction_20261031_v001'
    analytic=OUT.parent/'route_c_analytic_20261030_v001'
    deps=[ROOT/'python/independent/splay.py',ROOT/'python/liquidity/legacy_embedding.py',ROOT/'DO_RESEARCH_REBOOT/RESEARCH_RULES.md',
       prev/'CC01_SOURCE_ROTATION_IDENTITY.md',prev/'CC02_UNBOUNDED_CORRECTION_AND_PARTIAL_LAWS.md',
       prev/'CC03_ALL_SIZE_REPAYMENT_OBSTRUCTION.md',prev/'CC05_STRATEGY_AND_PROOF_STATUS.md',
       prev/'clade_correction_countercertificate.json',prev/'independent_audit.json',
       analytic/'RA02_ZERO_HELPER_ARBITRARY_FRINGE_PROOF.md',analytic/'six_key_closed_controls.json',
       ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/11G_FOUR_RULE_FREEZE.md',
       ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py',
       ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/STRICT_HIGH_COMPILER.py']
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    ck(not git('status','--porcelain=v1','--untracked-files=no'),'tracked tree clean')
    pins={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in deps}
    entry={'date':'2026-10-31','head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),'files':pins}
    save('entry_source_pins.json',entry)
    controls=[]
    for n in (6,7):
        _,_,row=edge('opposite_vine_'+str(n),S.vine_left(n),S.vine(n),'K',n)
        ck(row['E_source']==n-1 and row['E_destination']==n//2-2,'opposite-vine analytic values')
        ck(row['delta_E']==-(row['q']+2),'opposite-vine margin')
        controls.append(row)
    # FIRST registered helper: branch L, empty fringe, six keys.
    N=lambda k,l=S.LEAF,r=S.LEAF:S.node(k,l,r)
    a=N(6,N(2,N(1),N(3,S.LEAF,N(4,S.LEAF,N(5)))))
    b=N(6,N(5,N(4,N(1,S.LEAF,N(2,S.LEAF,N(3))))))
    ap,bp,bad=edge('helper_L_empty_first',a,b,'K',2);controls.append(bad)
    ck((bad['a'],bad['q'],bad['z'])==(1,2,0),'old helper source costs')
    ck((bad['E_source'],bad['E_after_A'],bad['E_destination'])==(1,2,2),'exact endpoint-matching helper values')
    ck(not bad['inequality_holds'],'first helper is an exact obstruction; stop candidate tests')
    old=json.loads((analytic/'six_key_closed_controls.json').read_text(encoding='utf-8'))['controls'][0]
    oldbad=old['full_replay'][old['zero_helper_index']]
    ck(oldbad['source_A']==raw(a) and oldbad['source_B']==raw(b),'reuse correct old closed source certificate')
    aa=dec(old['initial_A']);bb=dec(old['initial_B']);rows=[]
    for j,(mode,x) in enumerate(old['word']):aa,bb,row=edge('closed_'+str(j),aa,bb,mode,x);rows.append(row)
    ck(raw(aa)==old['initial_A'] and raw(bb)==old['initial_B'] and aa==bb,'actual diagonal paired closure')
    At=sum(r['a'] for r in rows);Qt=sum(r['q'] for r in rows);Zt=sum(r['z'] for r in rows)
    ck((At,Qt)==(old['A'],old['Q_B'])==(16,4),'inherited closed totals')
    ck(rows[old['zero_helper_index']]['delta_E']==1,'same failed whole operation in exact cycle')
    result={'status':'ENDPOINT_MATCHING_REPAIR_REFUTED_BY_FIRST_EMPTY_FRINGE_HELPER',
      'candidate':'proper subtree endpoint maximum matching deficit E=(n-1)-nu; min=min OR max=max; full sets fixed together',
      'controls':controls,'matching_graphs':GRAPHS,
      'closed_witness':{'initial_A':old['initial_A'],'initial_B':old['initial_B'],'word':old['word'],
        'failed_edge_index':old['zero_helper_index'],'full_replay':rows,'A':At,'Q_B':Qt,'Z_B':Zt,
        'actual_pair_closure':True,'source_word_reused_from':'route_c_analytic_20261030_v001/six_key_closed_controls.json, control 0'},
      'stop':{'first_failed_test':'six-key L helper, m=0','further_helper_variants_run':False,
         'singleton_fringe_controls_run':False,'port_embedding_search_run':False,'hook_vine_control_run':False},
      'new_source_state_graphs':0,'new_tree_corpora':0,'finite_potential_fits':0,'coefficient_fits':0,'connector_BFS_calls':0,
      'CoarseDouble_refuted':False}
    save('endpoint_matching_countercertificate.json',result)
    changes=[p for p,h in pins.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
    ck(not changes and not git('status','--porcelain=v1','--untracked-files=no'),'source and tracked state preserved')
    save('integrity.json',{'status':'PASS','pinned_inputs_changed':changes,'head':git('rev-parse','HEAD'),
      'branch':git('branch','--show-current'),'Stage11G_writes_performed':False})
    print(json.dumps({'status':result['status'],'opposite_vine_values':[(r['E_source'],r['E_destination'],r['q']) for r in controls[:2]],
      'helper':{k:bad[k] for k in ['E_source','E_after_A','E_destination','F_source','F_destination','a','q','delta_E','required_upper_bound']},
      'matching_graphs_certified':len(GRAPHS),'closed_totals':{'A':At,'Q_B':Qt,'Z_B':Zt},'closed_word_accesses':len(rows),
      'further_candidate_tests_stopped':True,'finite_fits':0},indent=2))

if __name__=='__main__':main()
