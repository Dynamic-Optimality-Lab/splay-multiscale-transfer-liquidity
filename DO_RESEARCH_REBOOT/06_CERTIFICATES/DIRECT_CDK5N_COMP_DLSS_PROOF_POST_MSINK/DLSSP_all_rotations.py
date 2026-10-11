# Gate D exhaustive whole-cycle rotations: every rotation of IN (34) and OUT
# (33) replayed from its TRUE start state, tested against all 21 banked
# domains. Fresh enumeration code; audited engines/predicates reused.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_PROOF_POST_MSINK')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from RC_recursive_closure_engine import replay_from
from CRA_segment_memberships import full_banked
from CRA_pointer_tuple_replay import replay

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_PROOF_POST_MSINK/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
IN_CANON = ("D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,"
            "D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
OUT_CANON = ("D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,"
             "K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")

MECHS21 = ["RT2", "CDK4", "CDK5L", "NP", "S1", "S2", "VR", "MR", "MSINK",
           "AJ", "AK", "ALG", "ALS", "AMG", "AMS", "AN",
           "AO", "AP", "AQ", "AR", "AS"]

def audit_rotations(name, cw):
    w = parse(cw)
    R = replay(w)
    assert R["S1"] == R["S0"] and R["agree"]
    n = len(w)
    sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_G0_POST_MSINK')
    from DLSS_membership import strict_msink_bank
    hits = {}
    for r in range(n):
        start = R["pairs"][r]
        rw = [w[(r + t) % n] for t in range(n)]
        Fr = replay_from(start, rw)
        assert Fr["pairs"][-1] == start, (name, r)
        n2 = len(rw)
        snaps = {t: Fr["snaps"][t] for t in range(n2)}
        fb = full_banked(Fr["legs"], Fr["pairs"], snaps)
        assert fb is not None
        got = sorted(k for k, v in fb.items() if v)
        if strict_msink_bank(Fr["legs"], Fr["pairs"]):
            got = sorted(set(got) | {"MSINK"})
        for m in got:
            hits.setdefault(m, []).append(r)
    return {"n": n, "rotations": n, "hits": hits,
            "any": any(hits.values())}

if __name__ == "__main__":
    out = {}
    for name, cw in (("IN", IN_CANON), ("OUT", OUT_CANON)):
        r = audit_rotations(name, cw)
        out[name] = r
        print("%s: rotations=%d hits=%s" % (name, r["rotations"], r["hits"]), flush=True)
    json.dump(out, open(PDIR + "DLSSP_all_rotations_direct_membership.json", "w"), indent=1, default=str)
    assert not out["IN"]["any"] and not out["OUT"]["any"], out
    print("ROTATIONS: PASS (no banked rotation for IN/OUT)", flush=True)
