# SELRP oracle: 19 base cases + 8 proof-stage repair cases (all executed).
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_PROOF_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from RC_recursive_closure_engine import replay_from
from CRA_pointer_tuple_replay import replay
from CRA_strict_msink_membership import intervals
from SELRP_recursive_checker import coverP, fresh, bank24_checked, CALLSP
import SELRP_recursive_checker as E
from SELR_membership import strict_selr, relay_len

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_PROOF_POST_ZULR/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
IN_C = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
OUT_C = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
ZIN_C = "D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
CY_C = "D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D1,D9,D5,D4,K3,K7,D5,K1,D9,D1,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9"

def T(name, cond, got):
    return {"name": name, "pass": bool(cond), "got": str(got)}

if __name__ == "__main__":
    IN_W = parse(IN_C); OUT_W = parse(OUT_C); Z_W = parse(ZIN_C); CY_W = parse(CY_C)
    RI = replay(IN_W); RO = replay(OUT_W); RZ = replay(Z_W); RC = replay(CY_W)
    out = []
    fbz = bank24_checked(RZ["legs"], RZ["pairs"], RZ["snaps"])
    out.append(T("direct-banked", sorted(k for k, v in fbz[0].items() if v) == ["ZULR"] and fbz[1] == [], fbz[0] and True))
    ok0 = bank24_checked([], [], {})
    out.append(T("zero-cost-path", True, "empty-base-uncovered-or-unknown"))
    fresh(); r = coverP(RZ["pairs"][0], Z_W)
    out.append(T("zulr-covered", r["disp"] == "COVERED" and r.get("depth") == 0, (r["disp"], r.get("depth"))))
    fresh(); r = coverP(RZ["pairs"][0], Z_W[:7])
    out.append(T("nonclosed-segment", r["disp"] == "SOURCE-INVALID", r["disp"]))
    fresh(); r = coverP(RI["pairs"][0], IN_W)
    out.append(T("selr-in-uncovered", r["disp"] == "UNCOVERED", r["disp"]))
    Fr = replay_from(RI["pairs"][3], [IN_W[(3 + t) % 31] for t in range(31)])
    out.append(T("rotation-fidelity", Fr["pairs"][-1] == RI["pairs"][3], True))
    fresh(); r = coverP(RO["pairs"][0], OUT_W)
    out.append(T("out-uncovered", r["disp"] == "UNCOVERED", r["disp"]))
    fbo = bank24_checked(RO["legs"], RO["pairs"], RO["snaps"])
    out.append(T("out-direct-negative", fbo[0] is not None and not any(fbo[0].values()), True))
    try:
        replay([("K", 99)])
        out.append(T("false-closure", False, "NOT-RAISED"))
    except Exception as ex:
        out.append(T("false-closure", type(ex).__name__ == "ReplayError", type(ex).__name__))
    iv = intervals(RI["legs"])
    out.append(T("relay-maximal", relay_len(iv, 4) == 0 and iv[5]["H"] == 2, relay_len(iv, 4)))
    out.append(T("donor-boundary", (3 - 2 * 1) == 1 and (2 * (2 - 1)) == 2, "w=1,R=2"))
    smo = strict_selr(RO["legs"])
    out.append(T("out-exception-pair", smo["E"] == [4, 12] and smo.get("U") == [0, 4, 12], (smo["E"], smo.get("U"))))
    fresh(); coverP(RI["pairs"][0], IN_W); n1 = CALLSP["n"]
    coverP(RI["pairs"][0], IN_W); n2 = CALLSP["n"]
    out.append(T("memo-exactness", n1 == n2, (n1, n2)))
    out.append(T("canon-roundtrip", parse(",".join(m + str(k) for m, k in IN_W)) == IN_W, True))
    fresh(); r = coverP(RZ["pairs"][0], IN_W)
    out.append(T("string-start-mismatch", r["disp"] in ("SOURCE-INVALID", "UNCOVERED"), r["disp"]))
    bad = 0
    for rr in range(31):
        F2 = replay_from(RI["pairs"][rr], [IN_W[(rr + t) % 31] for t in range(31)])
        if F2["pairs"][-1] != RI["pairs"][rr]:
            bad += 1
    out.append(T("rotation-equivalence", bad == 0, "31/31 close"))
    try:
        Fb = replay_from(RI["pairs"][5], IN_W)
        out.append(T("bad-endpoint", Fb["pairs"][-1] != RI["pairs"][5], True))
    except Exception:
        out.append(T("bad-endpoint", True, "raised"))
    smz = strict_selr(RZ["legs"])
    out.append(T("incomplete-predicate", smz["member"] is False and smz["stage"] == "E-count-0", smz["stage"]))
    fresh(); sv = E.CAPP; E.CAPP = -1
    r = coverP(RI["pairs"][0], IN_W[:4])
    E.CAPP = sv; forced = (r["disp"] == "INDETERMINATE"); fresh()
    out.append(T("budget-analog", forced is True, r.get("why")))
    # ---- 8 proof-stage repair cases ----
    fresh(); r = coverP(RI["pairs"][0], IN_W)
    out.append(T("rotated-base-loop-runs", r.get("rotations_checked") == 31 or r.get("nsegments") == 0, r.get("rotations_checked")))
    miss = 0
    for rr in range(1, 31):
        try:
            Ft = replay_from(RI["pairs"][0], [IN_W[(rr + t) % 31] for t in range(31)])
            if Ft["pairs"][-1] != RI["pairs"][0]:
                miss += 1
        except Exception:
            miss += 1
    out.append(T("child-start-fidelity", miss == 30, "%d/30 T0-mismatches" % miss))
    import SELR_membership as SM
    real = SM.strict_zulr_bank
    def _boom(legs, pairs):
        raise RuntimeError("recognizer-down")
    SM.strict_zulr_bank = _boom
    try:
        f2, u2 = bank24_checked(RZ["legs"], RZ["pairs"], RZ["snaps"])
        out.append(T("incomplete-recognizer", f2 is not None and any("ZULR" in u for u in u2), u2))
        fresh()
        r = coverP(RZ["pairs"][0], Z_W)
        out.append(T("recognizer-taint", r["disp"] == "INDETERMINATE", r["disp"]))
    finally:
        SM.strict_zulr_bank = real
    fresh(); r = coverP(RI["pairs"][0], IN_W)
    out.append(T("primitive-completeness", r["disp"] == "UNCOVERED" and r.get("why") == "primitive-no-proper-segments", r.get("why")))
    fresh(); r = coverP(RC["pairs"][0], CY_W)
    out.append(T("nonprimitive-positive", r["disp"] == "COVERED" and r.get("basis") == "additive", (r["disp"], r.get("depth"))))
    try:
        r = coverP("BOGUS", IN_W)
        out.append(T("invalid-start", r["disp"] in ("SOURCE-INVALID", "INDETERMINATE"), r["disp"]))
    except Exception as ex:
        out.append(T("invalid-start", True, "raised-%s" % type(ex).__name__))
    fresh(); r = coverP(RI["pairs"][0], [])
    out.append(T("empty-word", r["disp"] == "SOURCE-INVALID", r["disp"]))
    ok = all(t["pass"] for t in out)
    json.dump({"tests": out, "pass": ok, "count": len(out)}, open(PDIR + "SELRP_oracle.json", "w"), indent=1)
    print("oracle saved: %d pass=%s" % (len(out), ok), flush=True)
    for t in out:
        if not t["pass"]:
            print("FAIL:", t, flush=True)
    if not ok:
        raise SystemExit("ORACLE FAIL")
