# SELRP rotation-domain audit: recompute every decision with per-entry evidence.
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_PROOF_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from RC_recursive_closure_engine import replay_from, canon
from CRA_pointer_tuple_replay import replay, totals, core_of
from CRA_segment_memberships import genuine_keys
from SELRP_recursive_checker import bank24_checked
from SELR_membership import BANK24_NAMES

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_PROOF_POST_ZULR/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
IN_C = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
OUT_C = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"

def audit(tag, cw):
    w = parse(cw)
    R = replay(w)
    if not (R["S1"] == R["S0"] and R["agree"]):
        raise SystemExit(tag + " root not closed")
    n = len(w)
    rows = {}
    for r in range(n):
        start = R["pairs"][r]
        rw = [w[(r + t) % n] for t in range(n)]
        Fr = replay_from(start, rw)
        if Fr["pairs"][-1] != start:
            raise SystemExit("%s rotation %d not closed" % (tag, r))
        legs = Fr["legs"]
        t = totals(legs)
        snaps = {tt: Fr["snaps"][tt] for tt in range(n)}
        flags, unk = bank24_checked(legs, Fr["pairs"], snaps)
        if flags is None:
            raise SystemExit("%s rotation %d battery unknown: %s" % (tag, r, unk))
        if set(flags) != set(BANK24_NAMES):
            raise SystemExit("%s rotation %d key mismatch" % (tag, r))
        for k, v in flags.items():
            if not isinstance(v, bool):
                raise SystemExit("%s rotation %d non-bool %s" % (tag, r, k))
        rows[str(r)] = {"start_sha": hashlib.sha256(repr(start).encode()).hexdigest()[:16],
                         "closed": True, "n": n, "A": t["A"], "Q": t["Q"], "Ck": t["Ck"],
                         "keys": sorted(genuine_keys(legs)),
                         "core9": bool(all(core_of(p[1]) is not None and len(core_of(p[1])) == 9 for p in Fr["pairs"])),
                         "dispositions": {m: ("POSITIVE" if flags[m] else "EXCLUDED") for m in BANK24_NAMES},
                         "unknown": unk}
    hits = {m: [r for r in range(n) if rows[str(r)]["dispositions"][m] == "POSITIVE"] for m in BANK24_NAMES}
    hits = {m: v for m, v in hits.items() if v}
    return {"n": n, "rotations": n, "rows": rows,
            "hits": hits, "any": bool(hits),
            "ndecisions": n * len(BANK24_NAMES)}

if __name__ == "__main__":
    out = {}
    for tag, cw in (("IN", IN_C), ("OUT", OUT_C)):
        out[tag] = audit(tag, cw)
        print("%s: %d rotations x 24 = %d decisions, hits=%s" % (tag, out[tag]["rotations"], out[tag]["ndecisions"], out[tag]["hits"] or "none"), flush=True)
    json.dump(out, open(PDIR + "SELRP_rotation_matrices.json", "w"), indent=1, default=str)
    if out["IN"]["ndecisions"] != 744 or out["OUT"]["ndecisions"] != 720:
        raise SystemExit("decision count mismatch")
    if out["IN"]["any"] or out["OUT"]["any"]:
        raise SystemExit("POSITIVE rotation found")
    print("ROTATIONS: PASS (744 + 720 = 1464 EXCLUDED)", flush=True)
