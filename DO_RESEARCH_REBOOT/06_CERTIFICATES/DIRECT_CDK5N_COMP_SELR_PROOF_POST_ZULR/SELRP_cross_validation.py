# SELRP checker cross-validation: DP(coverP) vs DFS(coverA) agreement.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_PROOF_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay
from SELRP_recursive_checker import coverP, fresh as freshP
from SELRP_alt_checker import coverA, fresh as freshA

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_PROOF_POST_ZULR/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]

IN = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
OUT = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
ZIN = "D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
UESIN = "D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
DLSSIN = "D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
CTL = "D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
CY1 = "D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D1,D9,D5,D4,K3,K7,D5,K1,D9,D1,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9"
CY2 = "D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D1,D9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,D8,K7,K1,K9,D8,D2,D6,D1,D9"
_log = [json.loads(l) for l in open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR/SELR_screened_log.jsonl')]
RM2 = [e["canon"] for e in _log if e["op"] == "rm2"][0]
RM5 = [e["canon"] for e in _log if e["op"] == "rm5"][0]
RM12 = [e["canon"] for e in _log if e["op"] == "rm12"][0]
CONCAT = ZIN + "," + UESIN

FIX = [("IN", IN), ("OUT", OUT), ("ZULR-IN", ZIN), ("UESINK-IN", UESIN),
       ("DLSS-IN", DLSSIN), ("CTL", CTL), ("rm2", RM2), ("rm5", RM5),
       ("rm12", RM12), ("concat65", CONCAT), ("cyclic35", CY1), ("cyclic36", CY2)]
# rotated queries: (start-offset, word) pairs exercising rotation frames
ROTQ = [("IN-rot3", IN, 3), ("OUT-rot7", OUT, 7), ("ZIN-rot11", ZIN, 11)]

rows = []
for name, cw in FIX:
    w = parse(cw)
    R = replay(w)
    freshP(); p = coverP(R["pairs"][0], w)
    freshA(); a = coverA(R["pairs"][0], w)
    ag = (p["disp"] == a["disp"])
    rows.append({"name": name, "n": len(w), "dp": p["disp"], "dfs": a["disp"],
                 "agree": ag, "dp_why": p.get("why"), "dp_basis": p.get("basis")})
    print("%s n=%d dp=%s dfs=%s %s" % (name, len(w), p["disp"], a["disp"], "AGREE" if ag else "DISAGREE"), flush=True)
for name, cw, off in ROTQ:
    w = parse(cw)
    R = replay(w)
    n = len(w)
    wq = [w[(off + t) % n] for t in range(n)]
    from RC_recursive_closure_engine import replay_from
    Fq = replay_from(R["pairs"][off], wq)
    assert Fq["pairs"][-1] == R["pairs"][off]
    freshP(); p = coverP(R["pairs"][off], wq)
    freshA(); a = coverA(R["pairs"][off], wq)
    ag = (p["disp"] == a["disp"])
    rows.append({"name": name, "n": n, "dp": p["disp"], "dfs": a["disp"],
                 "agree": ag, "dp_why": p.get("why"), "dp_basis": p.get("basis")})
    print("%s n=%d dp=%s dfs=%s %s" % (name, n, p["disp"], a["disp"], "AGREE" if ag else "DISAGREE"), flush=True)
nag = sum(1 for r in rows if r["agree"])
json.dump({"rows": rows, "agree": nag, "total": len(rows)}, open(PDIR + "SELRP_cross_validation.json", "w"), indent=1)
print("XVAL: %d/%d agree" % (nag, len(rows)), flush=True)
if nag != len(rows):
    raise SystemExit("XVAL DISAGREEMENT")
print("XVAL: PASS", flush=True)
