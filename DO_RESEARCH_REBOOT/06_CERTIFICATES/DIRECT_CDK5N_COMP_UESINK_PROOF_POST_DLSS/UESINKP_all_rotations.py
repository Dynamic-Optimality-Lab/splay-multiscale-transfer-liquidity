# Exhaustive whole-cycle rotation matrices (Gate D hardening): every rotation
# replayed from its TRUE start state; all 22 domains decided per rotation.
# Dispositions: POSITIVE / EXCLUDED(reason). No INDETERMINATE expected.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_UESINK_PROOF_POST_DLSS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_UESINK_G0_POST_DLSS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_DLSS_G0_POST_MSINK')
from RC_recursive_closure_engine import replay_from
from CRA_segment_memberships import full_banked, keep_support, genuine_keys
from CRA_pointer_tuple_replay import replay
from UESINK_membership import strict_dlss_bank
from DLSS_membership import strict_msink_bank

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_UESINK_PROOF_POST_DLSS/'
MECHS = ["RT2", "CDK4", "CDK5L", "NP", "S1", "S2", "VR", "MR", "MSINK",
         "DLSS", "AJ", "AK", "ALG", "ALS", "AMG", "AMS", "AN",
         "AO", "AP", "AQ", "AR", "AS"]
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
IN_C = ("D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,"
        "K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
OUT_C = ("D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,"
         "K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")

def audit(name, cw):
    w = parse(cw)
    R = replay(w)
    assert R["S1"] == R["S0"] and R["agree"]
    n = len(w)
    mat = {}
    for r in range(n):
        start = R["pairs"][r]
        rw = [w[(r + t) % n] for t in range(n)]
        Fr = replay_from(start, rw)
        assert Fr["pairs"][-1] == start, (name, r)
        snaps = {t: Fr["snaps"][t] for t in range(len(rw))}
        fb = full_banked(Fr["legs"], Fr["pairs"], snaps)
        assert fb is not None, (name, r)
        row = dict(fb)
        row["MSINK"] = strict_msink_bank(Fr["legs"], Fr["pairs"])
        row["DLSS"] = strict_dlss_bank(Fr["legs"], Fr["pairs"])
        mat[str(r)] = {m: ("POSITIVE" if row.get(m) else "EXCLUDED") for m in MECHS}
    hits = {m: [r for r in range(n) if mat[str(r)][m] == "POSITIVE"] for m in MECHS}
    return {"n": n, "rotations": n, "matrix": mat,
            "hits": {m: v for m, v in hits.items() if v},
            "any": any(hits.values())}

if __name__ == "__main__":
    out = {}
    for name, cw in (("IN", IN_C), ("OUT", OUT_C)):
        out[name] = audit(name, cw)
        print("%s: %d rotations, hits=%s" % (name, out[name]["rotations"], out[name]["hits"]), flush=True)
    json.dump(out, open(PDIR + "UESINKP_rotation_matrices.json", "w"), indent=1, default=str)
    assert not out["IN"]["any"] and not out["OUT"]["any"]
    print("ROTATIONS: PASS (33x22 + 32x22 = 1430 decisions, all EXCLUDED)", flush=True)
