# SELR independent negative-certificate verifier (fresh code path, cleared memo).
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay, totals, core_of
from CRA_segment_memberships import genuine_keys
from SELR_membership import strict_selr, bank24
from SELR_recursive import cover24, MEMO24, CALLS24

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
IN_C = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
OUT_C = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"

checks = []
def check(name, cond, obs):
    checks.append({"check": name, "pass": bool(cond), "observed": obs})
    print(("PASS" if cond else "FAIL") + " check: %s (%s)" % (name, obs), flush=True)
    return bool(cond)

ok = True
ok &= check("IN-SHA", hashlib.sha256(IN_C.encode()).hexdigest() == "8cd970c71989fc3c4c852192a858a3d7f70d7e0b6db85f0a7fabb6d7add894bd", "exact")
ok &= check("OUT-SHA", hashlib.sha256(OUT_C.encode()).hexdigest() == "c3a55f13475c6ca0d75cfa8b0e355510171d19a73b250cab173ddc5fc431ec9e", "exact")
for tag, cw, exp in (("IN", IN_C, (31, 53, 36, 16)), ("OUT", OUT_C, (30, 52, 36, 16))):
    w = parse(cw)
    R = replay(w)
    t = totals(R["legs"])
    got = (len(w), t["A"], t["Q"], t["Ck"])
    ok &= check(tag + "-totals", got == exp, got)
    ok &= check(tag + "-closed", R["S1"] == R["S0"] and R["agree"], "full pair closure")
    pre = R["pairs"][:-1]
    ok &= check(tag + "-primitivity", len(pre) == len(w) and len(set(pre)) == len(w), "%d/%d" % (len(set(pre)), len(w)))
    ok &= check(tag + "-keys-core", sorted(genuine_keys(R["legs"])) == [1, 3, 5, 7, 9] and all(core_of(p[1]) is not None and len(core_of(p[1])) == 9 for p in R["pairs"]), "5 keys, core9")
    sm = strict_selr(R["legs"])
    if tag == "IN":
        ok &= check("IN-SELR-member", sm["member"] and sm["e"] == 4 and sm["p"] == 0 and sm["t"] == 0 and sm.get("U") == [0, 4], (sm["e"], sm["p"], sm["t"], sm.get("U")))
    else:
        ok &= check("OUT-nonmember", (not sm["member"]) and sm["E"] == [4, 12], (sm["stage"], sm["E"]))
    fb = bank24(R["legs"], R["pairs"], R["snaps"])
    ok &= check(tag + "-direct-negative", fb is not None and not any(fb.values()), "24/24 negative")
    MEMO24.clear(); CALLS24["n"] = 0; CALLS24["hit"] = False
    r = cover24(R["S0"], w)
    ok &= check(tag + "-recursive-negative", r.get("covered") is False and not r.get("indeterminate"), "calls=%d hit=%s" % (CALLS24["n"], CALLS24["hit"]))
m = json.load(open(PDIR + "SELR_rotation_matrices.json"))["IN"]
mo = json.load(open(PDIR + "SELR_OUT_rotation_matrix.json"))
ni = sum(1 for row in m["matrix"].values() for v in row.values())
no = sum(1 for row in mo["matrix"].values() for v in row.values())
ok &= check("IN-744-EXCLUDED", ni == 744 and not m["any"] and m["rotations"] == 31, ni)
ok &= check("OUT-720-EXCLUDED", no == 720 and not mo["any"] and mo["rotations"] == 30, no)
ok &= check("total-1464", ni + no == 1464, ni + no)
json.dump({"pass": ok, "checks": checks}, open(PDIR + "SELR_negative_verification.json", "w"), indent=1)
print("VERIFIER: %s" % ("PASS" if ok else "FAIL"), flush=True)
sys.exit(0 if ok else 1)
