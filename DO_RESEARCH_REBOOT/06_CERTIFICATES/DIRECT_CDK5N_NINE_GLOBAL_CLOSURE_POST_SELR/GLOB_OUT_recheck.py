# SELR OUT Bank25 recheck: 30x25=750 rotation decisions + 30/30 primitivity.
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_NINE_GLOBAL_CLOSURE_POST_SELR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
from RC_recursive_closure_engine import replay_from
from CRA_pointer_tuple_replay import replay, totals, core_of
from CRA_segment_memberships import genuine_keys
from GLOB_recursive_checker import bank25_checked, coverC, fresh
from GLOB_bank25 import BANK25_NAMES

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_NINE_GLOBAL_CLOSURE_POST_SELR/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
OUT_C = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
OUT_SHA = "c3a55f13475c6ca0d75cfa8b0e355510171d19a73b250cab173ddc5fc431ec9e"

if hashlib.sha256(OUT_C.encode()).hexdigest() != OUT_SHA:
    raise SystemExit("OUT SHA MISMATCH")
w = parse(OUT_C)
R = replay(w)
if not (R["S1"] == R["S0"] and R["agree"]):
    raise SystemExit("OUT not closed")
t = totals(R["legs"])
print("OUT totals: n=%d A=%d Q=%d Ck=%d Q-2A=%d" % (len(w), t["A"], t["Q"], t["Ck"], t["Q"] - 2 * t["A"]), flush=True)
if (len(w), t["A"], t["Q"], t["Ck"]) != (30, 52, 36, 16):
    raise SystemExit("OUT totals mismatch")
pre = R["pairs"][:-1]
print("primitivity: %d/%d" % (len(set(pre)), len(w)), flush=True)
if len(set(pre)) != len(w):
    raise SystemExit("OUT not primitive")
if sorted(genuine_keys(R["legs"])) != [1, 3, 5, 7, 9]:
    raise SystemExit("OUT keys mismatch")
if not all(core_of(p[1]) is not None and len(core_of(p[1])) == 9 for p in R["pairs"]):
    raise SystemExit("OUT core mismatch")
n = len(w)
rows = {}
for r in range(n):
    start = R["pairs"][r]
    rw = [w[(r + x) % n] for x in range(n)]
    Fr = replay_from(start, rw)
    if Fr["pairs"][-1] != start:
        raise SystemExit("rotation %d not closed" % r)
    flags, unk = bank25_checked(Fr["legs"], Fr["pairs"], {x: Fr["snaps"][x] for x in range(n)})
    if flags is None or unk:
        raise SystemExit("rotation %d unknown %s" % (r, unk))
    if set(flags) != set(BANK25_NAMES):
        raise SystemExit("rotation %d key mismatch" % r)
    rows[str(r)] = {m: ("POSITIVE" if flags[m] else "EXCLUDED") for m in BANK25_NAMES}
hits = {m: [r for r in range(n) if rows[str(r)][m] == "POSITIVE"] for m in BANK25_NAMES}
hits = {m: v for m, v in hits.items() if v}
print("rotation hits: %s" % (hits or "none"), flush=True)
if hits:
    raise SystemExit("BANK25 PROOF FOUND: %s" % hits)
json.dump({"n": n, "rotations": n, "rows": rows, "hits": hits, "any": False, "ndecisions": n * 25},
          open(PDIR + "GLOB_OUT_rotation_matrix.json", "w"), indent=1, default=str)
print("ROTATIONS: 750 EXCLUDED", flush=True)
fresh()
rc = coverC(R["pairs"][0], w)
print("coverC: %s %s calls=%d" % (rc["disp"], rc.get("why"), __import__("GLOB_recursive_checker", fromlist=["x"]).CALLSC["n"]), flush=True)
json.dump({"disp": rc["disp"], "why": rc.get("why"), "n": n}, open(PDIR + "GLOB_OUT_negative_certificate.json", "w"), indent=1)
if rc["disp"] != "UNCOVERED":
    raise SystemExit("OUT recursive status: %s" % rc["disp"])
print("OUT-RECHECK: PASS (genuine residual witness)", flush=True)
