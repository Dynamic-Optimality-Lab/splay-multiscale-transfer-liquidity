# SELRP independent replay: frozen IN/OUT from canonical words (fresh code).
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_PROOF_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay, totals, core_of
from CRA_segment_memberships import genuine_keys
from CRA_strict_msink_membership import intervals, strict_K, strict_P
from SELR_membership import strict_selr, relay_len

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_PROOF_POST_ZULR/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]

IN_C = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
OUT_C = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"

def work(tag, cw, exp_sha):
    if hashlib.sha256(cw.encode()).hexdigest() != exp_sha:
        raise SystemExit(tag + " SHA MISMATCH")
    w = parse(cw)
    R = replay(w)
    t = totals(R["legs"])
    iv = intervals(R["legs"])
    n = len(w)
    pre = R["pairs"][:-1]
    E = [j for j in range(len(iv)) if iv[j]["c"] == 1 and iv[j]["q"] == 3 and iv[j]["H"] == 1]
    U = [j for j in range(len(iv)) if iv[j]["w"] > 0 and not strict_K(iv[j], R["legs"]) and not strict_P(iv[j], R["legs"])]
    sm = strict_selr(R["legs"])
    rec = {"canon": cw, "sha": exp_sha, "n": n, "A": t["A"], "Q": t["Q"], "Ck": t["Ck"],
           "W": sum(v["w"] for v in iv), "R": sum(v["R"] for v in iv),
           "closed": bool(R["S1"] == R["S0"] and R["agree"]),
           "keys": sorted(genuine_keys(R["legs"])),
           "core9": bool(all(core_of(p[1]) is not None and len(core_of(p[1])) == 9 for p in R["pairs"])),
           "nboundaries": len(R["pairs"]),
           "distinct": len(set(pre)), "primitive": bool(len(set(pre)) == n),
           "E": E, "U": U,
           "relay": (relay_len(iv, E[0]) if len(E) == 1 else None),
           "member": sm["member"], "stage": sm["stage"], "e": sm.get("e"), "p": sm.get("p"),
           "positives": [{"j": j, "x": iv[j]["x"], "H": iv[j]["H"], "c": iv[j]["c"],
                          "q": iv[j]["q"], "w": iv[j]["w"], "R": iv[j]["R"],
                          "dA": R["legs"][iv[j]["gi"]]["dA"],
                          "K": strict_K(iv[j], R["legs"]), "P": strict_P(iv[j], R["legs"])}
                         for j in range(len(iv)) if iv[j]["w"] > 0]}
    json.dump(rec, open(PDIR + "SELRP_%s_replay.json" % tag, "w"), indent=1, default=str)
    print("%s: n=%d A=%d Q=%d Ck=%d W=%d R=%d closed=%s prim=%s E=%s U=%s member=%s" % (
        tag, n, t["A"], t["Q"], t["Ck"], rec["W"], rec["R"], rec["closed"],
        rec["primitive"], E, U, sm["member"]), flush=True)
    return rec

if __name__ == "__main__":
    ri = work("IN", IN_C, "8cd970c71989fc3c4c852192a858a3d7f70d7e0b6db85f0a7fabb6d7add894bd")
    ro = work("OUT", OUT_C, "c3a55f13475c6ca0d75cfa8b0e355510171d19a73b250cab173ddc5fc431ec9e")
    if (ri["n"], ri["A"], ri["Q"], ri["Ck"]) != (31, 53, 36, 16):
        raise SystemExit("IN totals mismatch")
    if (ro["n"], ro["A"], ro["Q"], ro["Ck"]) != (30, 52, 36, 16):
        raise SystemExit("OUT totals mismatch")
    if not (ri["closed"] and ri["primitive"] and ro["closed"] and ro["primitive"]):
        raise SystemExit("closure/primitivity mismatch")
    if not (ri["member"] and ri["E"] == [4] and ri["U"] == [0, 4]):
        raise SystemExit("IN membership mismatch")
    if not ((not ro["member"]) and ro["E"] == [4, 12]):
        raise SystemExit("OUT nonmembership mismatch")
    print("REPLAY: PASS", flush=True)
