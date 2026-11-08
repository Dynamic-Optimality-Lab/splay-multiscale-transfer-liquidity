"""Frozen inputs and public Step4 lower floors; no original compiler imports."""
import json,sys
from pathlib import Path
import z3
BASE=Path(__file__).resolve().parent;OLD=BASE.parent/'M3_XFER19'
sys.path.insert(0,str(OLD))
from target_floor import opp,opposite_alpha
from baseline19 import floor as baseline
from universal_grammar_v2 import build
from symbolic_prefix_v2 import prefix,PATHS
def freeze(t):return None if t is None else (t[0],freeze(t[1]),freeze(t[2]))
bank=json.loads((BASE.parent/'M3_LDR01/negative_run_census.json').read_text())
tab=json.loads((BASE.parent/'M3_H1F01/cheap_census.json').read_text())
kernel=json.loads((BASE.parent/'M3_H2R01/fringe_kernel_certificate.json').read_text())
certificate=json.loads((OLD/'STEP4_CERTIFICATE.json').read_text())
trees=[freeze(q['tree']) for q in bank['nodes']];ids={t:i for i,t in enumerate(trees)}
psi=[q['psi'] for q in bank['nodes']];depth=tab['B_depth'];destination=tab['B_destination']
anchors={int(i):{int(r):v for r,v in d.items()} for i,d in certificate['anchor_coefficients'].items()}
bycore={}
for c in certificate['clauses']:bycore.setdefault(c['core'],[]).append(c)
def N(a,r):return z3.And(*(a[j]!=r for j in range(1,7)))
def correction(i,a,m,k):
    q=[];root=trees[i][0]
    for c in bycore.get(i,[]):
        if c['level']<k:continue
        if c['kind']=='anchor':
            q.append(z3.Or(*(z3.And(m[r],z3.Or(*(a[j]==r for j in ((1,3) if r<root else (2,6)))))
              for r,v in anchors[i].items() if v>=c['level'])))
        else:q.append(z3.And(*(a[p]==v for p,v in c['score_equalities']),*(m[r] for r in c['marks'])))
    return z3.And(N(a,root),z3.Or(*q))
def capacity(i,a,m,k):
    r=trees[i][0]
    bad=[x for x in range(9) if x!=r and 2-depth[i][x]//2+psi[destination[i][x]]<k]
    return z3.And(*(z3.Implies(m[x],z3.And(*(a[p]!=x for p in range(1,7)))) for x in bad))
def seed_two(i,a,m):return z3.Or(z3.BoolVal(psi[i]==2),capacity(i,a,m,2))
def necessary_two(i,a,m):
    r=trees[i][0]
    return z3.And(*(z3.Implies(m[x],z3.And(*(a[p]!=x for p in range(1,7))))
      for x in range(9) if x!=r and depth[i][x]>=6))
def cheap_floor(i,a,m,k):
    return z3.Or(z3.BoolVal(psi[i]>=k),capacity(i,a,m,k),correction(i,a,m,k))
def full_floor(i,a,m,k):
    margins=[2-depth[i][x]//2+psi[destination[i][x]] for x in range(9)]
    return z3.Or(baseline(i,trees[i],a,m,psi[i],margins,k),correction(i,a,m,k))
def gamma_words(root,x,h):
    # Actual min orientation; the max reverses every primitive direction.
    r=root if h==0 else 8-root;y=x if h==0 else 8-x
    pairs=(((0,),(1,0)),((0,0),(1,)),((0,0),(1,0)),((0,1),(1,0))) if y<r else (((0,),(1,1)),((0,1),(1,1)))
    return pairs if h==0 else tuple(tuple(tuple(1-v for v in p) for p in w) for w in pairs)
