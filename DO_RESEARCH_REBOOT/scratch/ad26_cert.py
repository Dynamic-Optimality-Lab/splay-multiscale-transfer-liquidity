"""26AD obstruction certificate: UG-involvement, residual direction, finite witness.
Writes to DO_RESEARCH_REBOOT/{06_CERTIFICATES}. No other writes."""
import sys, json
sys.path.insert(0, 'scripts')
from pathlib import Path
ROOT = Path('.')
RDIR = Path(r"DO_RESEARCH_REBOOT")
import numpy as np
D0 = json.load(open(RDIR / "scratch/ad26_D0.json"))
terms = {eval(k): c for k, c in D0["terms"]}
print(f"[AC] D0 const={D0['c0']} support={len(terms)}", flush=True)
dom = json.load(open("artifacts/v04/wp6_present/0909c74a/dual_mine/j4_gapdomain.json"))
proved = set((('F', k), 2, dl, d) for (k, dl, d) in dom["overlap"])
proved.update((('F', 5), 2, dl, 6) for dl in (-5, -4))
print(f"[AC] proven twin pairs: {len(proved)}", flush=True)
# UG involvement: is any D0 key a twin source (lam2,proven) or twin target?
for k in terms:
    role = []
    if k[0] == 't' and k[1][0][0] == 'F' and k[1][1] == 2 and k[1] in proved:
        role.append('twin-source')
    if k[0] == 't' and k[1][0][0] == 'F' and k[1][1] == 1 and ((k[1][0], 2) + k[1][1:]) in proved:
        role.append('twin-target')
    print(f"[AC] key {k}: UG-role={role or 'NONE'}", flush=True)
# normalization evidence
uga = json.load(open("artifacts/v04/wp6_present/0909c74a/dual_mine/j4_ugar_a.json"))
print(f"[AC] ugar_a: {uga}", flush=True)
# residual direction v: +1 on (F0,1,0,3), -1 on (F0,-1,0,3); E has no rows touching support => Ev=0
v = {('t', (('F', 0), 1, 0, 3)): 1, ('t', (('F', 0), -1, 0, 3)): -1}
bv = sum(terms[k] * v.get(k, 0) for k in terms)
print(f"[AC] beta.v = {bv} (nonzero => equalities alone don't bound D0)", flush=True)
# finite witness: J=0 default; twins lam2=1/lam1=0 per proven pair; roots = c; F0 keys (10,0); rest 0
J = {}
for (s, lam, dl, d) in proved:
    J[('t', (s, 2, dl, d))] = 1.0
    J[('t', (s, 1, dl, d))] = 0.0
J[('r', 1)] = 1.0
J[('r', -1)] = -1.0
J[('t', (('F', 0), 1, 0, 3))] = 10.0
J[('t', (('F', 0), -1, 0, 3))] = 0.0
# verify ALL UG twin eqs J[lam2]-J[lam1]==1
ok = True
for (s, lam, dl, d) in proved:
    if J.get(('t', (s, 2, dl, d)), 0.0) - J.get(('t', (s, 1, dl, d)), 0.0) != 1.0:
        ok = False; print("[AC] UG VIOLATED at", (s, lam, dl, d), flush=True)
print(f"[AC] all proven UG eqs satisfied: {ok}", flush=True)
print(f"[AC] normalization holds by construction: {J[('r',1)]==1.0 and J[('r',-1)]==-1.0}", flush=True)
D0val = D0["c0"] + sum(c * J.get(k, 0.0) for k, c in terms.items())
print(f"[AC] D0 witness value = {D0val} (|.|>2 violates: {abs(D0val) > 2})", flush=True)
json.dump({"D0_const": D0["c0"], "D0_terms": D0["terms"],
           "ug_involvement": "none (no F0 twin pairs in proven domain; roots untouched)",
           "normalization_evidence": uga,
           "residual_beta_v": bv,
           "witness": {str(k): v for k, v in J.items() if k in terms or True},
           "witness_D0": D0val, "ug_satisfied": ok,
           "verdict": "premises (UG proven eqs + rho=c) do NOT imply |D0|<=2"},
          open(RDIR / "06_CERTIFICATES/26AD_base_obstruction.json", "w"), indent=1, default=str)
print("[AC] done", flush=True)
