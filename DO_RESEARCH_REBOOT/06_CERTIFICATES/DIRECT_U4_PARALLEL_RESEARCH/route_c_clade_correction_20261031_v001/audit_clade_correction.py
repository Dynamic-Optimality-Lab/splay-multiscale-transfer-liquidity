"""Fixed exact controls for the subtree-set correction; no graph or fit.

All universal statements are proved analytically in the accompanying reports.
The only key sizes evaluated are the pre-registered fixed n=6,7 controls.
"""
from pathlib import Path
from fractions import Fraction as Q
import sys,json,hashlib,subprocess

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/'python'))
from independent import splay as S
from liquidity import legacy_embedding as P

def ck(b,msg):
    if not b:raise AssertionError(msg)
def put(name,value):
    with (OUT/name).open('x',encoding='utf-8') as f:json.dump(value,f,indent=2)
def raw(t):return None if t==S.LEAF else [t[1],raw(t[2]),raw(t[3])]
def dec(t):return S.LEAF if t is None else S.node(t[0],dec(t[1]),dec(t[2]))
def ptr(t):
    if t==S.LEAF:return None
    p=P.mknode(t[1],ptr(t[2]),ptr(t[3]))
    for k in ('l','r'):
        if p[k] is not None:p[k]['p']=p
    return p
def pr(t):return None if t is None else [t['k'],pr(t['l']),pr(t['r'])]
def clades(t):
    if t==S.LEAF:return frozenset()
    return frozenset([frozenset(S.inorder(t))])|clades(t[2])|clades(t[3])
def serial_sets(c):return sorted([sorted(v) for v in c])
def F(a,b):return len(S.inorder(a))-len(clades(a)&clades(b))
def G(a,b):return sum(Q(S.lookup(b,k)[1],8**S.lookup(a,k)[1]) for k in S.inorder(a))
def mirror(t,n):return S.LEAF if t==S.LEAF else S.node(n+1-t[1],mirror(t[3],n),mirror(t[2],n))

def pointer_trace(t,x):
    """Instrument original rotations only in this local Python process."""
    records=[];left=P._rot_left;right=P._rot_right
    def wrapper(original,child):
        def call(p):
            top=p
            while top['p'] is not None:top=top['p']
            before=pr(top);oldset=frozenset(P.keys_inorder(p[child]))
            result=original(p)
            top=result
            while top['p'] is not None:top=top['p']
            after=pr(top);newset=frozenset(P.keys_inorder(p))
            cb=clades(dec(before));ca=clades(dec(after))
            ck(cb-ca==frozenset([oldset]) and ca-cb==frozenset([newset]),'exact one-set primitive identity')
            ck(x in oldset and x not in newset,'source splay removes target-containing proper set')
            records.append({'rotation':'L' if child=='r' else 'R','before':before,'after':after,
                'removed':sorted(oldset),'added':sorted(newset)})
            return result
        return call
    try:
        P._rot_left=wrapper(left,'r');P._rot_right=wrapper(right,'l')
        result,events=P.splay_trace(ptr(t),x)
    finally:P._rot_left=left;P._rot_right=right
    return pr(result),[[e['case'],e['lo'],e['hi'],e['orient']] for e in events],records

def edge(label,a,b,mode,x):
    ap,ea=S.trace(a,x)
    if mode=='K':bp,eb=S.trace(b,x)
    else:bp=b;eb=[]
    pa,pea,ra=pointer_trace(a,x)
    if mode=='K':pb,peb,rb=pointer_trace(b,x)
    else:pb=raw(b);peb=[];rb=[]
    ck(pa==raw(ap) and pb==raw(bp),'complete pointer/frame state agreement')
    ck(pea==[list(e) for e in ea] and peb==[list(e) for e in eb],'every oriented grouped event agrees')
    da=S.lookup(a,x)[1];db=S.lookup(b,x)[1] if mode=='K' else None
    ac=len(ea);q=sum(e[0]!='ZIG' for e in eb);z=sum(e[0]=='ZIG' for e in eb)
    ck(len(ra)==da and len(rb)==(db or 0),'source primitive rotation counts')
    ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'exact source cost definitions')
    for r in ra:
        ck(abs(F(dec(r['after']),b)-F(dec(r['before']),b))<=1,'A primitive Lipschitz bound')
    if mode=='K':
        ck(ap[1]==x,'B phase has accessed root in A')
        for r in rb:
            old=clades(dec(r['before']));new=clades(dec(r['after']));fixed=clades(ap)
            ck(not (fixed&old)-new,'no common set lost in B phase')
            ck(F(ap,dec(r['after']))<=F(ap,dec(r['before'])),'root-conditioned B monotonicity')
    f0=F(a,b);f1=F(ap,bp);g0=G(a,b);g1=G(ap,bp)
    row={'label':label,'mode':mode,'key':x,'source_A':raw(a),'source_B':raw(b),
       'destination_A':raw(ap),'destination_B':raw(bp),'dA':da,'dB':db,'a':ac,'q':q,'z':z,
       'events_A':pea,'events_B':peb,'primitive_A':ra,'primitive_B':rb,
       'source_clades_A':serial_sets(clades(a)),'source_clades_B':serial_sets(clades(b)),
       'destination_clades_A':serial_sets(clades(ap)),'destination_clades_B':serial_sets(clades(bp)),
       'F_source':f0,'F_destination':f1,'delta_F':f1-f0,
       'G_source':str(g0),'G_destination':str(g1),'delta_G':str(g1-g0),
       'R_source':str(Q(f0)-g0),'R_destination':str(Q(f1)-g1),'delta_R':str(Q(f1-f0)-(g1-g0)),
       'required_upper_bound':2*ac-q,'inequality_holds':f1-f0<=2*ac-q}
    return ap,bp,row

def main():
    prev=OUT.parent/'route_c_alignment_20261031_v001'
    deps=[ROOT/'python/independent/splay.py',ROOT/'python/liquidity/legacy_embedding.py',
      ROOT/'DO_RESEARCH_REBOOT/RESEARCH_RULES.md',
      prev/'AL02_DELETE_BAND_OBSTRUCTION.md',prev/'AL03_SIZE_DEPENDENT_BLEND_NO_GO.md',prev/'AL05_STRATEGY_REVIEW.md',
      prev/'root_aligned_countercertificate.json',prev/'final_integrity.json',
      ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/11G_FOUR_RULE_FREEZE.md',
      ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py',
      ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/STRICT_HIGH_COMPILER.py']
    git=lambda *a:subprocess.check_output(['git','-C',str(ROOT),*a]).decode().strip()
    ck(not git('status','--porcelain=v1','--untracked-files=no'),'tracked tree clean at entry')
    pins={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in deps}
    entry={'date':'2026-10-31','head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),'files':pins}
    put('entry_source_pins.json',entry)
    cases=[];scales=[]
    for n in (6,7):
        rv=S.vine(n);lv=S.vine_left(n)
        _,_,dd=edge('diagonal_DELETE_'+str(n),rv,rv,'D',n)
        _,_,kk=edge('opposite_vines_KEEP_'+str(n),lv,rv,'K',n)
        cases.extend([dd,kk])
        gain=1 if n%2==0 else 2
        ck(dd['delta_F']==n-1 and kk['delta_F']==-gain,'analytic parity control')
        ck(not kk['inequality_holds'] and dd['inequality_holds'],'full B repayment refuted')
        upper=Q(2*dd['a'],dd['delta_F']);lower=Q(kk['q'],gain)
        ck(lower>upper,'size-fixed scalar rescaling impossible')
        scales.append({'n':n,'necessary_c_upper_from_DELETE':str(upper),'necessary_c_lower_from_KEEP':str(lower),'overlap':False})
    n=6;rv=S.vine(n);lv=S.vine_left(n);mid=S.balanced(list(range(2,n)))
    oldA=S.node(1,S.LEAF,S.node(n,mid,S.LEAF));oldB=S.node(2,S.node(1,S.LEAF,S.LEAF),S.LEAF)
    right=S.LEAF
    for k in range(n,2,-1):right=S.node(k,S.LEAF,right)
    oldB=S.node(2,S.node(1,S.LEAF,S.LEAF),right)
    for is_mirror in (False,True):
        aa=mirror(oldA,n) if is_mirror else oldA;bb=mirror(oldB,n) if is_mirror else oldB
        for mode,x,tag in [('D',n,'old_DELETE'),('K',1,'old_KEEP')]:
            if is_mirror:x=n+1-x
            _,_,row=edge(tag+('_mirror' if is_mirror else ''),aa,bb,mode,x)
            cases.append(row)
            ck(row['delta_F']==(0 if mode=='D' else -1),'old obstruction repaired exactly')
            if mode=='D':ck(Q(row['delta_G'])==Q(21,8) and Q(row['delta_R'])==Q(-21,8),'unbounded drift cancellation control')
    _,_,row=edge('opposite_vines_KEEP_6_mirror',rv,lv,'K',1);cases.append(row)
    ck(row['delta_F']==-1 and not row['inequality_holds'],'mirror repayment failure')
    # Deterministic source-only connectors; no BFS, state corpus or fitting.
    word=[('K',k) for k in range(n-1,0,-1)]+[('D',k) for k in range(2,n+1)]+[('K',n)]+[('K',k) for k in range(1,n+1)]
    failed=2*(n-1);a=b=lv;rows=[]
    for j,(mode,x) in enumerate(word):
        a,b,row=edge('closed_'+str(j),a,b,mode,x);rows.append(row)
    ck(a==b==lv,'exact diagonal paired closure')
    bad=rows[failed]
    ck(bad['source_A']==raw(lv) and bad['source_B']==raw(rv) and bad['key']==6 and bad['delta_F']==-1 and bad['q']==2,'counteredge reached exactly')
    At=sum(r['a'] for r in rows);Qt=sum(r['q'] for r in rows);Zt=sum(r['z'] for r in rows)
    ck(Qt<=2*At,'closed walk is not a Coarse-Double counterexample')
    result={'status':'EXPLICIT_UNBOUNDED_CORRECTION_HAS_DELETE_AND_B_MONOTONICITY_BUT_FULL_REPAYMENT_IS_REFUTED',
       'definition':'C(T)=exact key sets of nonempty node-rooted subtrees; F=n-|C(A) intersection C(B)|; R=F-G; Psi=F',
       'r':'1/8','controls':cases,'rescaling_controls':scales,
       'closed_witness':{'n':n,'initial_A':raw(lv),'initial_B':raw(lv),'word':word,'failed_edge_index':failed,
          'full_replay':rows,'paired_closure':True,'A':At,'Q_B':Qt,'Z_B':Zt},
       'analytic_claims':{'DELETE':'universal Delta F<=d_A<=2a',
          'B_monotonicity':'universal Delta_B F<=0 when root(A)=access key',
          'old_DELETE_drift':'Delta F=0 and Delta R=-7(n-3)/8 for all n>=3 and arbitrary middle M',
          'old_zero_demand_KEEP':'Delta F=-1 for all n>=3 and arbitrary middle M',
          'full_B_repayment':'opposite-vine counterexample at every n>=6',
          'rescaling':'no coefficient c_n, even size-dependent, satisfies both laws for any n>=6'},
       'finite_control_sizes':[6,7],'new_pair_graphs':0,'finite_fits':0,'fitted_coefficients':0,
       'source_rotation_identity_checks':sum(len(r['primitive_A'])+len(r['primitive_B']) for r in cases+rows),
       'CoarseDouble_refuted':False}
    put('clade_correction_countercertificate.json',result)
    changed=[p for p,h in pins.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
    ck(not changed and not git('status','--porcelain=v1','--untracked-files=no'),'preservation check')
    put('integrity.json',{'status':'PASS','source_changes':changed,'head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),'Stage11G_writes_performed':False})
    print(json.dumps({'status':result['status'],'rescaling_controls':scales,
      'old_DELETE_control':'delta G=21/8, delta R=-21/8, delta Psi=0',
      'closed_word_accesses':len(word),'closed_totals':{'A':At,'Q_B':Qt,'Z_B':Zt},
      'rotation_identity_checks':result['source_rotation_identity_checks'],'finite_fits':0},indent=2))

if __name__=='__main__':main()
