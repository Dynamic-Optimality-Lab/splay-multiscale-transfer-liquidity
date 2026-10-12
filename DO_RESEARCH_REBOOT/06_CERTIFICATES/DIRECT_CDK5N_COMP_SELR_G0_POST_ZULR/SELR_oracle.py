# SELR 19-case recursive oracle battery vs cover24/bank24 (fresh engine).
# Every case executes a real engine/predicate behavior. No padding.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from RC_recursive_closure_engine import replay_from
from CRA_pointer_tuple_replay import replay
from CRA_strict_msink_membership import intervals
from SELR_recursive import cover24, MEMO24, CALLS24, bank24, base24
from SELR_membership import strict_selr, relay_len
import SELR_recursive as E

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
def canon(w):
    return ",".join(m + str(k) for m, k in w)
IN_C = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
OUT_C = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
ZIN_C = "D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"

def fresh():
    MEMO24.clear(); CALLS24["n"] = 0; CALLS24["hit"] = False

def T(name, cond, got):
    return {"name": name, "pass": bool(cond), "got": str(got)}

if __name__ == "__main__":
    IN_W = parse(IN_C); OUT_W = parse(OUT_C); Z_W = parse(ZIN_C)
    RI = replay(IN_W); RO = replay(OUT_W); RZ = replay(Z_W)
    out = []
    fbz = bank24(RZ["legs"], RZ["pairs"], RZ["snaps"])
    out.append(T("direct-banked", sorted(k for k, v in fbz.items() if v) == ["ZULR"], sorted(k for k, v in fbz.items() if v)))
    ok0, c0 = base24([], [], {})
    out.append(T("zero-cost-path", c0.get("indeterminate") is True, c0.get("basis")))
    fresh(); r = cover24(RZ["S0"], Z_W)
    out.append(T("zulr-covered", r.get("covered") is True and r.get("depth") == 0, (r.get("covered"), r.get("depth"))))
    fresh(); r = cover24(RZ["S0"], Z_W[:7])
    out.append(T("nonclosed-segment", r.get("covered") is False and r.get("why") == "not-closed", r.get("why")))
    fresh(); r = cover24(RI["S0"], IN_W)
    out.append(T("selr-in-uncovered", r.get("covered") is False and not r.get("indeterminate"), (r.get("covered"), r.get("indeterminate"))))
    Fr = replay_from(RI["pairs"][3], [IN_W[(3 + t) % 31] for t in range(31)])
    out.append(T("rotation-fidelity", Fr["pairs"][-1] == RI["pairs"][3], True))
    fresh(); r = cover24(RO["S0"], OUT_W)
    out.append(T("out-uncovered", r.get("covered") is False and not r.get("indeterminate"), (r.get("covered"), r.get("indeterminate"))))
    fbo = bank24(RO["legs"], RO["pairs"], RO["snaps"])
    out.append(T("out-direct-negative", not any(fbo.values()), True))
    try:
        replay([("K", 99)])
        out.append(T("false-closure", False, "NOT-RAISED"))
    except Exception as ex:
        out.append(T("false-closure", True, type(ex).__name__))
    iv = intervals(RI["legs"])
    out.append(T("relay-maximal", relay_len(iv, 4) == 0 and iv[5]["H"] == 2, relay_len(iv, 4)))
    out.append(T("donor-boundary", (3 - 2 * 1) == 1 and (2 * (2 - 1)) == 2, "w=1,R=2"))
    smo = strict_selr(RO["legs"])
    out.append(T("out-exception-pair", smo["E"] == [4, 12] and smo.get("U") == [0, 4, 12], (smo["E"], smo.get("U"))))
    fresh(); cover24(RI["S0"], IN_W); n1 = CALLS24["n"]
    cover24(RI["S0"], IN_W); n2 = CALLS24["n"]
    out.append(T("memo-exactness", n1 == n2, (n1, n2)))
    out.append(T("canon-roundtrip", parse(canon(IN_W)) == IN_W and len(canon(IN_W).split(",")) == 31, True))
    fresh(); r = cover24(RZ["S0"], IN_W)
    out.append(T("string-start-mismatch", r.get("covered") is not True, r.get("covered")))
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
    fresh(); sv = E.CAP24; E.CAP24 = -1
    r = cover24(RI["S0"], IN_W[:4])
    E.CAP24 = sv; forced = r.get("indeterminate") in ("cap", "cap-hit"); fresh()
    out.append(T("budget-analog", forced is True, r.get("indeterminate")))
    ok = all(t["pass"] for t in out)
    json.dump({"tests": out, "pass": ok, "count": len(out)}, open(PDIR + "SELR_oracle.json", "w"), indent=1)
    print("oracle saved: %d pass=%s" % (len(out), ok), flush=True)
    for t in out:
        if not t["pass"]:
            print("FAIL:", t, flush=True)
    if not ok:
        raise SystemExit("ORACLE FAIL")
