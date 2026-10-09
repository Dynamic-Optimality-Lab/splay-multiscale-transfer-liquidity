"""Exact, isolated verification of source-defined rows (no source module imports).

Only selected function ASTs are executed; source entry points and import-time
code are excluded. All files written by this script remain under this folder.
The universal proof is in 02_PROVED/; this finite check is supplementary.
"""
import ast, copy, json, hashlib, itertools, sys
from pathlib import Path
from collections import Counter
from fractions import Fraction
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
WS = HERE.parent
ROOT = WS.parent
provenance = {}
def pure_functions(rel, names, environment=None):
    path = ROOT/rel
    data = path.read_bytes()
    tree = ast.parse(data.decode('utf-8-sig'),filename=str(path))
    selected = [n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert {n.name for n in selected} == set(names)
    namespace = dict(environment or {})
    module = ast.Module(body=selected,type_ignores=[])
    exec(compile(ast.fix_missing_locations(module),str(path),'exec'),namespace)
    provenance[rel] = {'sha256':hashlib.sha256(data).hexdigest(),
                       'functions':{n.name:[n.lineno,n.end_lineno] for n in selected}}
    return namespace
sr = pure_functions('scripts/wp6_staticR.py',['path_nodes','sz','depths_list','Tmap','R_static'])
lc = pure_functions('scripts/wp6_lambda.py',['subkeys_list','R_coeffs'],sr)
j4 = pure_functions('scripts/wp6_j4shared.py',['subkeys_list','slot_of','subsize','H0','tau4_of'],dict(sr,KAPPA=4))
depths, path_nodes, R_static, R_coeffs = sr['depths_list'], sr['path_nodes'], sr['R_static'], lc['R_coeffs']
def canonical(d): return {k:v for k,v in d.items() if v}
def add(a,b,scale=1):
    out = dict(a)
    for k,v in b.items(): out[k] = out.get(k,0)+scale*v
    return canonical(out)
def form(B,y):
    dd=depths(B); c,lam=R_coeffs(B,y)
    out={('constant',):j4['H0'](B,y,len(dd)),('r',c):1}
    for z in dd:
        if z != y:
            key=('t',j4['tau4_of'](B,y,z,lam.get(z,0)))
            out[key]=out.get(key,0)+1
    assert all(isinstance(v,int) for v in out.values())
    assert R_static(B,y)==c+sum(lam.values())
    return canonical(out)
def difference(B,u,v): return add(form(B,u),form(B,v),-1)
def shapes(ks):
    if not ks: return [None]
    return [[k,L,R] for i,k in enumerate(ks) for L in shapes(ks[:i]) for R in shapes(ks[i+1:])]
def valid(t,lo=None,hi=None):
    if t is None: return True
    k,L,R=t
    assert (lo is None or lo<k) and (hi is None or k<hi),t
    return valid(L,lo,k) and valid(R,k,hi)
def reflect(t,axis=200):
    return None if t is None else [axis-t[0],reflect(t[2],axis),reflect(t[1],axis)]
def empty_sibling(B,side):
    out=copy.deepcopy(B); out[2 if side=='L' else 1]=None; return out
def ftop(B,y):
    P=path_nodes(B,y); d=len(P)-1
    assert d>=1
    # Read the top fringe coefficient directly from the source fold, even
    # when the sibling is empty and its per-key lambda dictionary omits it.
    if d%2==0: st=(0,0,[],0)
    else: st=(-1,0,[1],0) if y<B[0] else (0,-1,[1],0)
    pats=[]
    for i in range(d,1,-2):
        g,p,x=P[i-2],P[i-1],P[i]
        a=0 if g[1] is p else 1; b=0 if p[1] is x else 1
        pats.append({(0,0):'LL',(1,1):'RR',(0,1):'LR',(1,0):'RL'}[a,b])
    for pat in reversed(pats): st=sr['Tmap'](pat,st)
    assert len(st[2])==d
    return st[2][-1]
def row_sibling_increment(B,y,side):
    dd=depths(B); d=dd[y]; f=ftop(B,y)
    S=B[2 if side=='L' else 1]; ds=depths(S) if S else {}
    out={('constant',):(4-f)*len(ds)}
    for z in ds:
        atom=('t',(('F',d-1),f,dd[z]-d,d))
        out[atom]=out.get(atom,0)+1
    return canonical(out)
stats=Counter()
for t in range(1,7):
    for T in shapes([10*k for k in range(1,t+1)]):
        p=10*(t+1)
        for s in range(4):
            for S in shapes([p+10*k for k in range(1,s+1)]):
                original=[p,copy.deepcopy(T),copy.deepcopy(S)]
                for side,B in [('L',original),('R',reflect(original))]:
                    valid(B); B0=empty_sibling(B,side)
                    target=B[1 if side=='L' else 2]
                    dd=depths(B); ys=list(depths(target))
                    row_cache={}
                    base_cache={}
                    for y in ys:
                        fy=form(B,y); fy0=form(B0,y)
                        row_cache[y]=fy; base_cache[y]=fy0
                        assert add(fy,fy0,-1)==row_sibling_increment(B,y,side),(B,y,side)
                        stats['full_row_sibling_formula_checks']+=1
                        if dd[y]%2: assert ftop(B,y)==1
                    for u,v in itertools.combinations(ys,2):
                        if dd[u]==dd[v] and ftop(B,u)==ftop(B,v):
                            assert add(row_cache[u],row_cache[v],-1)==add(base_cache[u],base_cache[v],-1)
                            stats['eligible_pair_erasure_checks']+=1
                            stats['mirror_pairs' if side=='R' else 'left_pairs']+=1
                        stats['all_pair_contexts_inspected']+=1
                    stats['valid_contexts']+=1

# Leaf insertion at every empty pointer of each sibling with <=3 nodes.
def gaps(S,lo,hi,loc=()):
    if S is None: return [(loc,(lo+hi)/2)]
    return gaps(S[1],lo,S[0],loc+(1,))+gaps(S[2],S[0],hi,loc+(2,))
def insert_at(S,loc,key):
    if not loc:
        assert S is None
        return [key,None,None]
    out=copy.deepcopy(S); node=out
    for i in loc[:-1]: node=node[i]
    assert node[loc[-1]] is None
    node[loc[-1]]=[key,None,None]; return out
for T in shapes([10,20,30,40]):
    for s in range(4):
        for S in shapes([60+10*k for k in range(s)]):
            for loc,e in gaps(S,Fraction(50),Fraction(100)):
                B=[50,copy.deepcopy(T),copy.deepcopy(S)]
                Bp=[50,copy.deepcopy(T),insert_at(S,loc,e)]
                for side,A,Ap in [('L',B,Bp),('R',reflect(B),reflect(Bp))]:
                    valid(A);valid(Ap)
                    ee=e if side=='L' else 200-e
                    da=depths(A);dap=depths(Ap)
                    ys=list(depths(A[1 if side=='L' else 2]))
                    for u,v in itertools.combinations(ys,2):
                        du,dv=da[u],da[v];fu,fv=ftop(A,u),ftop(A,v)
                        predicted={('constant',):fv-fu}
                        predicted=add(predicted,{('t',(('F',du-1),fu,dap[ee]-du,du)):1})
                        predicted=add(predicted,{('t',(('F',dv-1),fv,dap[ee]-dv,dv)):1},-1)
                        actual=add(difference(Ap,u,v),difference(A,u,v),-1)
                        assert actual==canonical(predicted),(A,u,v,e,actual,predicted)
                        stats['all_pair_leaf_insertion_checks']+=1

T=[40,[20,[10,None,None],[30,None,None]],[60,[50,None,None],[70,None,None]]]
B=[80,T,[100,[90,None,None],[110,None,None]]]
assert depths(B)[10]==depths(B)[30]==3
assert ftop(B,10)==ftop(B,30)==1
assert difference(B,10,30)==difference([80,T,None],10,30)
nonvacuity={'B':B,'u':10,'v':30,'depth':3,'f_top':1,
            'difference_coefficients':[[repr(k),v] for k,v in sorted(difference(B,10,30).items(),key=lambda kv:repr(kv[0]))]}
# Arbitrarily deep family illustrations. Each new ancestor remains below p
# by increasing p too; old target keys and subtree remain fixed.
for height in range(0,31):
    ext=copy.deepcopy(T)
    for k in range(height): ext=[100+10*k,ext,None]
    p=110+10*height
    deep=[p,ext,[p+20,None,[p+30,None,None]]]
    for side,A in [('L',deep),('R',reflect(deep,axis=10000))]:
        u,v=(10,30) if side=='L' else (9990,9970)
        assert depths(A)[u]==depths(A)[v]
        assert ftop(A,u)==ftop(A,v)
        assert difference(A,u,v)==difference(empty_sibling(A,side),u,v)
        stats['deep_family_checks']+=1

# Rank-nullity correction is arithmetic; source matrices for the reported
# T01+/T12+/T23+ dimensions are absent and not manufactured here.
rank_nullity=[{'map':'T01+','source_dim':52,'target_dim':44,'rank':33},
              {'map':'T12+','source_dim':49,'target_dim':55,'rank':44},
              {'map':'T23+','source_dim':70,'target_dim':47,'rank':38}]
for r in rank_nullity:
    r['kernel_dim']=r['source_dim']-r['rank']
    r['cokernel_dim']=r['target_dim']-r['rank']
output={'status':'PASS','arithmetic':'integer symbolic coefficient dictionaries; rational keys for insertions',
        'corpus':{'T_sizes':[1,2,3,4,5,6],'S_sizes':[0,1,2,3],
                  'orientations':['left','right'], 'deep_family_heights':[0,30]},
        'counts':dict(stats),'source_provenance':provenance,'nonvacuity':nonvacuity,
        'rank_nullity_arithmetic_only':rank_nullity,
        'claim_supported':'finite verification supporting REBOOT-01; universal proof is separate'}
(HERE/'verification_results.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
print(json.dumps({'status':output['status'],'counts':dict(stats),'nonvacuity':nonvacuity},indent=2))
