# SELRP rich negative certificates: auditable records per witness (Erratum F).
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_PROOF_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay, totals
from SELRP_recursive_checker import coverP, fresh, CALLSP

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_PROOF_POST_ZULR/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
IN_C = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
OUT_C = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"

def build(tag, cw, sha):
    w = parse(cw)
    R = replay(w)
    n = len(w)
    t = totals(R["legs"])
    states = R["pairs"]
    pre = states[:-1]
    classes = {}
    for i, s in enumerate(pre):
        classes.setdefault(repr(s), []).append(i)
    segs = []
    for i in range(n):
        for j in range(i + 1, n + 1):
            if j - i == n:
                continue
            if states[i] == states[j % n]:
                segs.append([i, j])
    fresh()
    r = coverP(states[0], w)
    cert = {"canon": cw, "sha": sha, "n": n, "A": t["A"], "Q": t["Q"], "Ck": t["Ck"],
            "closed": bool(states[-1] == states[0]),
            "nboundaries": len(states), "distinct": len(set(pre)),
            "primitive": bool(len(set(pre)) == n),
            "equality_classes": len(classes),
            "repeated_states": [v for v in classes.values() if len(v) > 1],
            "proper_closed_segments": segs, "nsegments": len(segs),
            "recursive_disp": r["disp"], "recursive_why": r.get("why"),
            "recursive_basis": r.get("basis"), "rotations_checked": r.get("rotations_checked"),
            "calls": CALLSP["n"], "cap_hit": CALLSP["hit"],
            "unresolved": r.get("unknown")}
    json.dump(cert, open(PDIR + "SELRP_%s_negative_certificate.json" % tag, "w"), indent=1, default=str)
    print("%s: prim=%s segs=%d disp=%s calls=%d" % (tag, cert["primitive"], len(segs), r["disp"], CALLSP["n"]), flush=True)
    return cert

if __name__ == "__main__":
    ci = build("IN", IN_C, "8cd970c71989fc3c4c852192a858a3d7f70d7e0b6db85f0a7fabb6d7add894bd")
    co = build("OUT", OUT_C, "c3a55f13475c6ca0d75cfa8b0e355510171d19a73b250cab173ddc5fc431ec9e")
    if not (ci["primitive"] and co["primitive"]):
        raise SystemExit("primitivity failed")
    if not (ci["recursive_disp"] == "UNCOVERED" and co["recursive_disp"] == "UNCOVERED"):
        raise SystemExit("recursive negative failed")
    if ci["nsegments"] != 0 or co["nsegments"] != 0:
        raise SystemExit("primitive segment census nonzero")
    print("NEGCERTS: PASS", flush=True)
