"""Exact public union produced by the provisional one-credit proof construction."""
import json,z3
from pathlib import Path
from seven_anchor import seven_one
SAVED=json.loads((Path(__file__).resolve().parent/'audit_seven_closure.json').read_text())
assert SAVED['status']=='UNIVERSAL_ONE_CREDIT_CLOSURE_PASS_PENDING_INDEPENDENT_AUDIT'
BYCORE={}
for c in SAVED['clauses']:BYCORE.setdefault(c['core'],[]).append(c)
def closure_one(i,t,a,m):
    terms=[]
    for c in BYCORE.get(i,[]):
        guard=seven_one(t,a) if c['kind'].startswith('initial') else z3.And(*(a[p]==v for p,v in c['score_equalities']))
        terms.append(z3.And(guard,*(m[k] for k in c['marks'])))
    return z3.Or(*terms)
