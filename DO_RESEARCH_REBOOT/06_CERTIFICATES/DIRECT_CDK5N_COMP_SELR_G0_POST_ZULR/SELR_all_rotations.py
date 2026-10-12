# Exhaustive whole-cycle rotation audit: every rotation replayed from its
# TRUE start state against all 24 banked domains. Fresh enumeration code.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from RC_recursive_closure_engine import replay_from
from SELR_recursive import bank24
from SELR_membership import BANK24_NAMES
from CRA_pointer_tuple_replay import replay

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR/'
MECHS = BANK24_NAMES
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
IN_C = ("D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,"
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
        fb = bank24(Fr["legs"], Fr["pairs"], snaps)
        assert fb is not None, (name, r)
        row = dict(fb)
        mat[str(r)] = {m: ("POSITIVE" if row.get(m) else "EXCLUDED") for m in MECHS}
    hits = {m: [r for r in range(n) if mat[str(r)][m] == "POSITIVE"] for m in MECHS}
    return {"n": n, "rotations": n, "matrix": mat,
            "hits": {m: v for m, v in hits.items() if v},
            "any": any(hits.values())}

if __name__ == "__main__":
    words = {"IN": IN_C}
    if len(sys.argv) > 1:
        words = {"OUT": sys.argv[1]}
    out = {}
    for name, cw in words.items():
        out[name] = audit(name, cw)
        print("%s: rotations=%d hits=%s" % (name, out[name]["rotations"], out[name]["hits"]), flush=True)
    if "IN" in out:
        json.dump(out, open(PDIR + "SELR_rotation_matrices.json", "w"), indent=1, default=str)
        assert not out["IN"]["any"]
        print("ROTATIONS: PASS (31x24 = 744 decisions, all EXCLUDED)", flush=True)
    else:
        json.dump(out["OUT"], open(PDIR + "SELR_OUT_rotation_matrix.json", "w"), indent=1, default=str)
        assert not out["OUT"]["any"]
        print("OUT-ROTATIONS: PASS", flush=True)
