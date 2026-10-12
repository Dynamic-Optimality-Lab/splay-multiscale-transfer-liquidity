# MIG forensic control replay: A/B/C + SELR regressions (frozen inputs).
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay, idepths, from_serial, core_of, pdepths
from CRA_segment_memberships import genuine_keys

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_DISPARITY_MIGRATION_G0_POST_SELR/'.replace('SELR', 'GLOBAL_OPEN')
PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_DISPARITY_MIGRATION_G0_POST_GLOBAL_OPEN/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
def canon(w):
    return ",".join(m + str(k) for m, k in w)

T0STD = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]], [8, [7, None, None], None]], None]
TC = [1, None, [2, None, [3, None, [4, None, [5, None, [8, [6, None, [7, None, None]], [9, None, None]]]]]]]
M = {1, 3, 5, 7, 9}

CTRL = {
    "A": ("D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,D3,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
          "c805670d61bdf8a95f481570de67d562a87570fd3c45d13aa5fdd17a0a71f3d2", T0STD, 31, 53, 36),
    "B": ("D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D1,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
          "86cb71faddf69918ec2886717111850301c40406d67b6fe21878a4139bcfdaec", T0STD, 29, 50, 36),
    "C": ("D7,D9,D5,D6,D9,D1,K1,K9,K1,K3,K5,K9,K7,K9,K5,K3,K1,D2,D6,D4,D8,D5,D3,D1",
          "4274383229549cadc8b723fbbb9ab0a5024a58c6de3134ac1b5ad214ffcc23f0", TC, 24, 37, 16),
}
SELR = {
    "SELR-OUT": ("D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
                 "c3a55f13475c6ca0d75cfa8b0e355510171d19a73b250cab173ddc5fc431ec9e", T0STD, 30, 52, 36),
    "SELR-IN": ("D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
                "8cd970c71989fc3c4c852192a858a3d7f70d7e0b6db85f0a7fabb6d7add894bd", T0STD, 31, 53, 36),
}

def gaps(ps):
    A = from_serial(ps[0]); B = from_serial(ps[1])
    dA = idepths(A); dB = idepths(B)
    return {x: dB.get(x, 0) - dA.get(x, 0) for x in sorted(M)}

def work(tag, cw, sha, T0, en, eA, eQ):
    assert hashlib.sha256(cw.encode()).hexdigest() == sha, tag + " SHA"
    w = parse(cw)
    R = replay(w, A0=T0, B0=T0)
    assert R["S1"] == R["S0"] and R["agree"], tag + " closure"
    A = sum(l["a"] for l in R["legs"]); Q = sum(l["q"] for l in R["legs"])
    assert (len(w), A, Q) == (en, eA, eQ), (tag, len(w), A, Q)
    assert sorted(genuine_keys(R["legs"])) == [1, 3, 5, 7, 9], tag + " keys"
    assert all(core_of(p[1]) is not None and len(core_of(p[1])) == 9 for p in R["pairs"]), tag + " core"
    rec = {"tag": tag, "sha": sha, "n": len(w), "A": A, "Q": Q, "exc": Q - 2 * A,
           "closed": True, "boundaries": []}
    for k in range(len(w)):
        g = gaps(R["pairs"][k])
        Gam = sum(max(0, v) for v in g.values())
        rec["boundaries"].append({"k": k, "op": canon([w[k]]), "a": R["legs"][k]["a"],
                                  "q": R["legs"][k]["q"], "dA": R["legs"][k]["dA"],
                                  "dB": R["legs"][k]["dB"], "gaps": g, "Gamma": Gam})
    json.dump(rec, open(PDIR + "MIG_replay_%s.json" % tag, "w"), indent=1, default=str)
    print("%s: n=%d A=%d Q=%d exc=%d keys/core/closure OK" % (tag, len(w), A, Q, Q - 2 * A), flush=True)
    return R, rec

if __name__ == "__main__":
    for tag, (cw, sha, T0, en, eA, eQ) in list(CTRL.items()) + list(SELR.items()):
        work(tag, cw, sha, T0, en, eA, eQ)
    print("REPLAY: PASS (3 controls + 2 regressions)", flush=True)
