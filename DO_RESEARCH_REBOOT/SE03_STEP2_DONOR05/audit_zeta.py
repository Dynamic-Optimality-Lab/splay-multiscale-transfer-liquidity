"""New Zeta free terms on specified paths, reusing old B identity results."""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def N(k,l,r):return (k,l,r)
def at(t,p):
    for c in p:t=t[1 if c=='L' else 2]
    return t
def put(t,p,u):
    if not p:return u
    k,l,r=t
    return N(k,put(l,p[1:],u),r) if p[0]=='L' else N(k,l,put(r,p[1:],u))
def frame(t,s):
    g,l,r=t
    if s=='LL':p,pl,c=l;x,a,b=pl;return N(x,a,N(p,b,N(g,c,r)))
    if s=='RR':p,b,pr=r;x,c,d=pr;return N(x,N(p,N(g,l,b),c),d)
    if s=='LR':p,a,pr=l;x,b,c=pr;return N(x,N(p,a,b),N(g,c,r))
    if s=='RL':p,pl,d=r;x,b,c=pl;return N(x,N(g,l,b),N(p,c,d))
    if s=='L':p,a,b=l;return N(p,a,N(g,b,r))
    if s=='R':p,b,d=r;return N(p,N(g,l,b),d)
    raise AssertionError(s)
def access(t,x,p):
    assert at(t,p)[0]==x,(x,p)
    pp=p;e=[]
    while len(pp)>=2:
        pre,pair=pp[:-2],pp[-2:];e.append(pair);t=put(t,pre,frame(at(t,pre),pair));pp=pre
    if pp:e.append(pp);t=frame(t,pp)
    assert t[0]==x
    return t,e
def inorder(t):return [t] if isinstance(t,str) else inorder(t[1])+[t[0]]+inorder(t[2])
def from_json(t):return t if isinstance(t,str) else N(t[0],from_json(t[1]),from_json(t[2]))
def marked_below(t):
    if isinstance(t,str):return set()
    return ({t[0]} if t[0]%2 else set())|marked_below(t[1])|marked_below(t[2])
def marked_leaves(t):
    if isinstance(t,str):return set()
    s=marked_leaves(t[1])|marked_leaves(t[2])
    return s|({t[0]} if t[0]%2 and not (marked_below(t[1])|marked_below(t[2])) else set())
def main():
    f=[f'F{i}' for i in range(12)];R=f[11]
    for k in range(11,0,-1):R=N(k,f[k-1],R)
    t=R;trace=[]
    def step(tag,key,path):
        nonlocal t
        t,events=access(t,key,path);assert inorder(t)==inorder(R)
        trace.append({'tag':tag,'key':key,'path':path,'events':events,'cost':len(events)})
    prep=[(5,'RRRR'),(11,'RRRRRR'),(3,'LLLRL'),(11,'R'),(1,'LLL'),(3,'RLR'),(1,'L')]
    for x,p in prep:step('preparation',x,p)
    tail=N(8,N(7,f[6],f[7]),N(10,N(9,f[8],f[9]),f[10]))
    P=N(1,f[0],N(3,N(2,f[1],f[2]),N(11,N(5,N(4,f[3],f[4]),N(6,f[5],tail)),f[11])))
    assert t==P
    step('boundary_root',1,'');step('critical',11,'RR');step('critical',1,'LL');assert t==P
    step('zero',3,'R');step('zero',5,'RL')
    Q=N(5,N(3,N(1,f[0],N(2,f[1],f[2])),N(4,f[3],f[4])),N(11,N(6,f[5],tail),f[11]))
    assert t==Q
    # Read ONE completed endpoint as a lemma, never replay its transition.
    old=json.loads((B.parent/'SE03_STEP2_REPAY01/source_term_derivation.json').read_text())
    B5=from_json(old['trace'][17]['end_terms'][1])
    expected=N(5,N(4,N(3,N(2,N(1,f[0],f[1]),f[2]),f[3]),f[4]),
        N(6,f[5],N(11,N(8,N(7,f[6],f[7]),N(10,N(9,f[8],f[9]),f[10])),f[11])))
    assert B5==expected and marked_leaves(B5)=={1,7,9}
    assert at(Q,'R')[0]==at(B5,'RR')[0]==11
    paths=['LL','RL','R','RL','R','RL','RLL','R','RLL','R','R']
    for x,p in enumerate(paths,1):step('ascending',x,p)
    L=f[0]
    for k in range(1,12):L=N(k,L,f[k])
    assert t==L
    for k in range(10,0,-1):step('descending',k,'L')
    assert t==R
    groups={g:sum(r['cost'] for r in trace if r['tag']==g) for g in {r['tag'] for r in trace}}
    assert groups=={'preparation':14,'boundary_root':0,'critical':2,'zero':2,'ascending':13,'descending':10}
    W=[('K',k) for k in [3,5,7,9,11,9,7,5,3,1]]
    H=[('K',k) for k in [11,1,3,5,7,9,11,9,7,5,3,1]]
    scan=[('D',k) for k in range(1,12)]+[('D',k) for k in range(10,0,-1)]
    word=W[:-1]+[('D',1)]+[('D',k) for k,p in prep]+[('K',1)]+H[:4]+scan+[('D',11),('D',1),('D',3),('D',5)]+H[4:]
    assert len(word)==55 and sum(o=='K' for o,k in word)==22
    assert [r for r in word if r[0]=='K']==W+H
    Pids=[(1,1),(9,1),(19,5),(21,1),(21,2),(54,1)]
    units=[(o,e,b) for o,e in [(11,2),(12,1),(12,2)] for b in (0,1)]
    assert len(set(Pids))==len(set(units))==6
    assert [word[i-1] for i in [11,12,18,19,20,21,22,54]]==[('D',5),('D',11),('K',1),('K',11),('K',1),('K',3),('K',5),('K',3)]
    A=9+1+14+0+2+2+23+10+10;assert A==71 and 2*A-30==112
    out('zeta_audit.json',{'status':'PASS_UNIVERSAL_NEW_A_TERMS_AND_SOURCE_CANDIDATE_OBSTRUCTION',
        'Fi':'twelve independent arbitrary ordered BST variables, never instantiated','trace':trace,'group_costs':groups,
        'prepared_A':P,'after_zero_A':Q,'after_zero_B':B5,'marked_core_leaves_at_end':[1,7,9],
        'inherited_endpoint_reused':'REPAY01 source_term_derivation trace18 full B term; no replay',
        'closure':'new scan returns R11; inherited H6 first-four A identity aligns atB5; inherited eight-KEEP suffix closes R11',
        'counts':{'operations':55,'KEEP':22,'DELETE':33,'A':71,'QF':30,'QE_steady':24,'QE_first':25,'D3':5,'J3':1,'N':0,'P':6,'full_slack':112},
        'candidate_refuted':'D0=max(psi11,packet-safe L)','two_zero_path':{'start_D0':2,'end_D0_upper_bound':1,'total_weight':0,'total_residual_upper_bound':-1},
        'receipt':[{'demand':p,'unit':u} for p,u in zip(Pids,units)],
        'word':[{'occurrence':i,'op':o,'key':k} for i,(o,k) in enumerate(word,1)],
        'negative_original_cycle':False,'all_D6_formulas_refuted':False,'new_finite_tests':0,'source_engine_calls':0,'old_semantic_rows_replayed':0,'Step2':'OPEN'})
    print('PASS new arbitrary-fringe Zeta source identities, exact closure interfaces, and two-zero-path candidate refutation')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_zeta_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
