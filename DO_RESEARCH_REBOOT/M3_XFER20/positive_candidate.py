"""Public new correction over sealed Step4, with exact record-defined clauses."""
import json,z3
from support import BASE,trees,N,cheap_floor,full_floor
REPORT=json.loads((BASE/'audit_completion_v2.json').read_text())
assert REPORT['status']=='COMPLETE_SIGNED_POSITIVE_ANCHOR_CLOSURE'
ANCHORS={int(i):set(v) for i,v in REPORT['anchors'].items()}
BYCORE={}
for c in REPORT['clauses']:BYCORE.setdefault(c['core'],[]).append(c)
def new_correction(i,a,m,k):
    terms=[]
    for c in BYCORE.get(i,[]):
        if c['level']<k:continue
        if c['kind']=='positive_anchor':
            terms.append(z3.Or(*(z3.And(m[r],z3.Or(*(a[p]==r for p in ((1,3) if r<trees[i][0] else (2,6))))) for r in ANCHORS[i])))
        else:terms.append(z3.And(*(a[p]==v for p,v in c['score_equalities']),*(m[r] for r in c['marks'])))
    return z3.And(N(a,trees[i][0]),z3.Or(*terms))
def candidate_floor(i,a,m,k,allfloors=False):
    assert allfloors or k==1,'the lazy capacity tier is used only at level1'
    return z3.Or((full_floor if allfloors else cheap_floor)(i,a,m,k),new_correction(i,a,m,k))
