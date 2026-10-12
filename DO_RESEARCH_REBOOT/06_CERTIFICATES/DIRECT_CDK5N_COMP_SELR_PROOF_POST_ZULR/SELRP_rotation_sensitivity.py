# SELRP rotation-sensitivity diagnostics: per-word rotation census + old-vs-new.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_PROOF_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from RC_recursive_closure_engine import replay_from
from CRA_pointer_tuple_replay import replay
from SELRP_recursive_checker import coverP, fresh, bank24_checked

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_PROOF_POST_ZULR/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]

WORDS = {
    "IN": "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
    "OUT": "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
    "ZULR-IN": "D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
    "UESINK-IN": "D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
}
CY = ["D5,D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D1,D9,D5,D4,K3,K7,D5,K1,D9,D1,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9"]

rec = {}
for name, cw in list(WORDS.items()) + [("CYCLIC-%d" % i, c) for i, c in enumerate(CY)]:
    w = parse(cw)
    R = replay(w)
    n = len(w)
    npos = 0
    for rr in range(n):
        Fr = replay_from(R["pairs"][rr], [w[(rr + t) % n] for t in range(n)])
        fb, unk = bank24_checked(Fr["legs"], Fr["pairs"], {t: Fr["snaps"][t] for t in range(n)})
        if fb is not None and any(fb.values()):
            npos += 1
    fresh()
    r = coverP(R["pairs"][0], w)
    rec[name] = {"n": n, "npos_rotations": npos, "mixed": bool(0 < npos < n),
                 "coverP": r["disp"], "rotations_checked": r.get("rotations_checked")}
    print("%s n=%d npos=%d mixed=%s coverP=%s" % (name, n, npos, rec[name]["mixed"], r["disp"]), flush=True)
# old-behavior simulation (input-orientation-only base) on witnesses
old_same = {}
for name in ("IN", "OUT"):
    w = parse(WORDS[name])
    R = replay(w)
    Fr0 = replay_from(R["pairs"][0], w)
    fb0, _ = bank24_checked(Fr0["legs"], Fr0["pairs"], Fr0["snaps"])
    old_same[name] = not any(fb0.values())
    print("old-base-only %s negative: %s" % (name, old_same[name]), flush=True)
rec["old_behavior_agrees"] = old_same
json.dump(rec, open(PDIR + "SELRP_rotation_sensitivity.json", "w"), indent=1)
print("SENSITIVITY SAVED", flush=True)
