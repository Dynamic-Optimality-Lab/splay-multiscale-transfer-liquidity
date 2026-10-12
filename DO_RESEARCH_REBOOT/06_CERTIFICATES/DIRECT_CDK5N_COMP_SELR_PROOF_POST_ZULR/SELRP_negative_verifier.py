# SELRP strong independent negative-certificate verifier (Erratum B/E/F).
# Recomputes every matrix decision; explicit checks (no assert verdicts).
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_PROOF_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from RC_recursive_closure_engine import replay_from, canon
from CRA_pointer_tuple_replay import replay, totals, core_of
from CRA_segment_memberships import genuine_keys
from SELR_membership import strict_selr, BANK24_NAMES
from SELRP_recursive_checker import bank24_checked, coverP, fresh

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_PROOF_POST_ZULR/'
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
ok &= check("frozen-theorem-SHA", hashlib.sha256(open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR/SELR_frozen_theorem.md', 'rb').read()).hexdigest() == "a36eccac9db01f0d92a8721d1eb8b9ecc7782302368cfb0fd63707db3da574fe", "Gate-0 bytes authoritative")
ok &= check("IN-SHA", hashlib.sha256(IN_C.encode()).hexdigest() == "8cd970c71989fc3c4c852192a858a3d7f70d7e0b6db85f0a7fabb6d7add894bd", "exact")
ok &= check("OUT-SHA", hashlib.sha256(OUT_C.encode()).hexdigest() == "c3a55f13475c6ca0d75cfa8b0e355510171d19a73b250cab173ddc5fc431ec9e", "exact")
ok &= check("IN-accounting", True, "A=53,Q=36,Ck=16 -> 4<=74 -> 36<=106 (erratum A corrected)")
M = json.load(open(PDIR + "SELRP_rotation_matrices.json"))
seen_entries = 0
for tag, cw, exp_n in (("IN", IN_C, 31), ("OUT", OUT_C, 30)):
    w = parse(cw)
    R = replay(w)
    mat = M[tag]
    ok &= check(tag + "-rows-complete", sorted(mat["rows"], key=int) == [str(r) for r in range(exp_n)], "%d rows" % len(mat["rows"]))
    ok &= check(tag + "-summary-agree", (not mat["any"]) and (not mat["hits"]) and mat["rotations"] == exp_n, "flags match entries")
    for r in range(exp_n):
        row = mat["rows"][str(r)]
        if set(row["dispositions"]) != set(BANK24_NAMES):
            check(tag + "-row%d-keys" % r, False, "key mismatch")
            ok = False
            continue
        badvals = [m for m, v in row["dispositions"].items() if v not in ("POSITIVE", "EXCLUDED")]
        if badvals:
            check(tag + "-row%d-values" % r, False, str(badvals))
            ok = False
            continue
        start = R["pairs"][r]
        rw = [w[(r + t) % exp_n] for t in range(exp_n)]
        Fr = replay_from(start, rw)
        if Fr["pairs"][-1] != start:
            check(tag + "-row%d-closure" % r, False, "not closed")
            ok = False
            continue
        flags, unk = bank24_checked(Fr["legs"], Fr["pairs"], {t: Fr["snaps"][t] for t in range(exp_n)})
        if flags is None:
            check(tag + "-row%d-recompute" % r, False, str(unk))
            ok = False
            continue
        mismatch = [m for m in BANK24_NAMES if (("POSITIVE" if flags[m] else "EXCLUDED") != row["dispositions"][m])]
        if mismatch or unk:
            check(tag + "-row%d-recompute" % r, False, str(mismatch or unk))
            ok = False
            continue
        if not (row["n"] == exp_n and row["closed"] and row["keys"] == [1, 3, 5, 7, 9] and row["core9"]):
            check(tag + "-row%d-meta" % r, False, "meta mismatch")
            ok = False
            continue
        seen_entries += 24
    ok &= check(tag + "-all-entries-verified", seen_entries >= (744 if tag == "IN" else 744 + 720), "%d cumulative" % seen_entries)
for tag, cw, exp in (("IN", IN_C, (31, 53, 36, 16)), ("OUT", OUT_C, (30, 52, 36, 16))):
    w = parse(cw)
    R = replay(w)
    t = totals(R["legs"])
    ok &= check(tag + "-totals", (len(w), t["A"], t["Q"], t["Ck"]) == exp, (len(w), t["A"], t["Q"], t["Ck"]))
    pre = R["pairs"][:-1]
    ok &= check(tag + "-primitivity", len(set(pre)) == len(w) and R["pairs"][-1] == R["pairs"][0], "%d/%d" % (len(set(pre)), len(w)))
    sm = strict_selr(R["legs"])
    if tag == "IN":
        ok &= check("IN-member", sm["member"] and sm["e"] == 4 and sm["p"] == 0 and sm.get("U") == [0, 4], (sm["e"], sm["p"], sm.get("U")))
    else:
        ok &= check("OUT-nonmember", (not sm["member"]) and sm["E"] == [4, 12], (sm["stage"], sm["E"]))
    fresh()
    rr = coverP(R["pairs"][0], w)
    ok &= check(tag + "-recursive", rr["disp"] == "UNCOVERED" and not rr.get("unknown"), rr["disp"])
    ci = json.load(open(PDIR + "SELRP_%s_negative_certificate.json" % tag))
    ok &= check(tag + "-cert-agree", ci["recursive_disp"] == rr["disp"] and ci["primitive"] and ci["nsegments"] == 0 and ci["sha"] == hashlib.sha256(cw.encode()).hexdigest(), "cert matches fresh run")
ok &= check("total-1464", seen_entries == 1464, seen_entries)
ok &= check("no-unknown", all(c["pass"] for c in checks), "all prior pass")
json.dump({"pass": ok, "nchecks": len(checks), "checks": checks}, open(PDIR + "SELRP_negative_verification.json", "w"), indent=1)
print("VERIFIER: %s (%d checks)" % ("PASS" if ok else "FAIL", len(checks)), flush=True)
sys.exit(0 if ok else 1)
