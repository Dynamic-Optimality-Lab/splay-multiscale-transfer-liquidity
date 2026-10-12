# Cross-validation DP vs DFS + origin-shift additive case.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_NINE_GLOBAL_CLOSURE_POST_SELR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay
from GLOB_recursive_checker import coverC, fresh as freshC
from GLOB_alt_checker import coverD, fresh as freshD

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_NINE_GLOBAL_CLOSURE_POST_SELR/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
OUT = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
ZIN = "D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
SIN = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
CY = "D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D1,D9,D5,D4,K3,K7,D5,K1,D9,D1,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9"
CONCAT = ZIN + "," + "D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
FIX = [("OUT", OUT), ("SELR-IN", SIN), ("ZULR-IN", ZIN), ("CYCLIC", CY), ("CONCAT", CONCAT)]
rows = []
for name, cw in FIX:
    w = parse(cw)
    R = replay(w)
    freshC(); p = coverC(R["pairs"][0], w)
    freshD(); d = coverD(R["pairs"][0], w)
    ag = p["disp"] == d["disp"]
    rows.append({"name": name, "n": len(w), "dp": p["disp"], "dfs": d["disp"], "agree": ag})
    print("%s n=%d dp=%s dfs=%s %s" % (name, len(w), p["disp"], d["disp"], "AGREE" if ag else "DISAGREE"), flush=True)
# origin-shift: rotated CONCAT frame as input (additive proof visible only off-origin)
w = parse(CONCAT)
R = replay(w)
n = len(w)
off = 33
wq = [w[(off + t) % n] for t in range(n)]
from RC_recursive_closure_engine import replay_from
import sys as _s
_s.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
Fq = replay_from(R["pairs"][off], wq)
assert Fq["pairs"][-1] == R["pairs"][off]
freshC(); p = coverC(R["pairs"][off], wq)
freshD(); d = coverD(R["pairs"][off], wq)
ag = p["disp"] == d["disp"]
rows.append({"name": "CONCAT-shift33", "n": n, "dp": p["disp"], "dfs": d["disp"], "agree": ag})
print("CONCAT-shift33 dp=%s dfs=%s %s" % (p["disp"], d["disp"], "AGREE" if ag else "DISAGREE"), flush=True)
nag = sum(1 for r in rows if r["agree"])
json.dump({"rows": rows, "agree": nag, "total": len(rows)}, open(PDIR + "GLOB_cross_validation.json", "w"), indent=1)
print("XVAL %d/%d" % (nag, len(rows)), flush=True)
if nag != len(rows):
    raise SystemExit("DISAGREEMENT")
print("XVAL: PASS", flush=True)
