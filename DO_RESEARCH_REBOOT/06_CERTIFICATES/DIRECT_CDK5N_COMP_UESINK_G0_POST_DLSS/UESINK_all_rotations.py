# UESINK exhaustive whole-cycle rotations: every rotation replayed from its
# TRUE start state against all 22 banked domains. Fresh enumeration code.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_UESINK_G0_POST_DLSS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from RC_recursive_closure_engine import replay_from
from UESINK_recursive import bank22
from CRA_pointer_tuple_replay import replay

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
    hits = {}
    for r in range(n):
        start = R["pairs"][r]
        rw = [w[(r + t) % n] for t in range(n)]
        Fr = replay_from(start, rw)
        assert Fr["pairs"][-1] == start, (name, r)
        snaps = {t: Fr["snaps"][t] for t in range(len(rw))}
        fb = bank22(Fr["legs"], Fr["pairs"], snaps)
        assert fb is not None, (name, r)
        for m, v in fb.items():
            if v:
                hits.setdefault(m, []).append(r)
    print("%s: rotations=%d hits=%s" % (name, n, hits), flush=True)
    return hits

if __name__ == "__main__":
    hi = audit("IN", IN_C)
    ho = audit("OUT", OUT_C)
    assert not hi and not ho
    print("ROTATIONS: PASS (33+32 frames all-negative)", flush=True)
