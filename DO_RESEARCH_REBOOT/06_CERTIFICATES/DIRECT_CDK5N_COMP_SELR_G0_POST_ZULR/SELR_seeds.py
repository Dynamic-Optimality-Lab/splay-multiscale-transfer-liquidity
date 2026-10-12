# SELR seven-seed distance-zero audit (§11): fixed order, full classification.
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_CYCLIC_RC')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from RC_recursive_closure_engine import replay_from
from CRA_pointer_tuple_replay import replay, totals, core_of
from CRA_segment_memberships import genuine_keys
from SELR_membership import strict_selr, bank24, BANK24_NAMES
from SELR_recursive import cover24, MEMO24, CALLS24

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_SELR_G0_POST_ZULR/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
def canon(w):
    return ",".join(m + str(k) for m, k in w)

S1W = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 4),
       ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 2), ('D', 5),
       ('D', 6), ('D', 1), ('D', 9)]
VRW = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 9),
       ('D', 8), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8),
       ('D', 2), ('D', 6), ('D', 1), ('D', 9)]
MRW = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 9),
       ('D', 8), ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 5),
       ('D', 4), ('K', 3), ('K', 7), ('D', 5), ('K', 1), ('D', 9), ('D', 8),
       ('K', 9), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8), ('D', 4),
       ('D', 2), ('D', 5), ('D', 6), ('D', 1), ('D', 9)]
SEEDS = [
    ("selr-in", "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
     "8cd970c71989fc3c4c852192a858a3d7f70d7e0b6db85f0a7fabb6d7add894bd"),
    ("zulr-in", "D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
     "593b3f3ac56101755ea8995a8c87fd35ed73ba54cec8b5ef16f296d2d44945b9"),
    ("uesink-in", "D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
     "a7c6504c27817236123fcf9a8d58ae51bbb4583205e8171dd95983493629fda8"),
    ("dlss-in", "D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
     "b8b02be76c04033741d5f8534d286bbd14f571d3cd995961ac3d3cacb4bedab3"),
    ("dlss-ctl", "D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D5,D4,D3,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9",
     "6b242e23dbcdd11f1bef4a7c9101a6a26b3df44f5bb4452c60b38cc30c7c76cc"),
    ("mr33", None, "f647667922643558a8f8eed34d58293fc7bda27d053fd56fec35354cdcb2521d"),
    ("concat35", None, "7b00897fab01764d14f0c98e6d07daf415839edff31b6f5e90eef93211418bfd"),
]
WORDMAP = {"mr33": MRW, "concat35": S1W + VRW}

rows = []
for pri, (name, cw, h) in enumerate(SEEDS, start=1):
    w = parse(cw) if cw else WORDMAP[name]
    cc = canon(w)
    sha_ok = hashlib.sha256(cc.encode("ascii")).hexdigest() == h
    try:
        R = replay(w)
        closed = (R["S1"] == R["S0"]) and R["agree"]
    except Exception as e:
        rows.append({"pri": pri, "name": name, "sha_ok": sha_ok, "disp": "invalid-%s" % type(e).__name__})
        print(pri, name, "sha_ok=%s" % sha_ok, "INVALID", flush=True)
        continue
    gk = sorted(genuine_keys(R["legs"]))
    core_ok = all(core_of(p[1]) is not None and len(core_of(p[1])) == 9 for p in R["pairs"])
    backbone = closed and len(gk) == 5 and core_ok
    sm = strict_selr(R["legs"])
    fb = bank24(R["legs"], R["pairs"], R["snaps"])
    flags = sorted(k for k, v in fb.items() if v) if fb is not None else None
    t = totals(R["legs"])
    # rotations all-negative?
    n = len(w)
    allneg = True
    for r in range(n):
        st = R["pairs"][r]
        rw = [w[(r + tt) % n] for tt in range(n)]
        Fr = replay_from(st, rw)
        assert Fr["pairs"][-1] == st, (name, r)
        f2 = bank24(Fr["legs"], Fr["pairs"], {tt: Fr["snaps"][tt] for tt in range(n)})
        if f2 is None or any(f2.values()):
            allneg = False
            break
    if not backbone:
        disp = "non-backbone"
    elif sm["member"]:
        disp = "SELR-member" if (not flags) else "SELR-member+BANKED?"
    elif flags:
        disp = "banked"
    else:
        MEMO24.clear(); CALLS24["n"] = 0; CALLS24["hit"] = False
        cov = cover24(R["S0"], w)
        if cov.get("indeterminate"):
            disp = "INDETERMINATE"
        elif cov.get("covered"):
            disp = "recursive-covered"
        else:
            disp = "OUT-HOPEFUL"
    row = {"pri": pri, "name": name, "sha_ok": sha_ok, "n": n,
           "A": t["A"], "Q": t["Q"], "keys": gk, "core9": core_ok,
           "closed": closed, "selr": sm["member"], "E": sm["E"],
           "U": sm.get("U"), "t": sm.get("t"), "e": sm.get("e"), "p": sm.get("p"),
           "stage": sm["stage"], "banked": flags, "allrot_neg": allneg, "disp": disp}
    rows.append(row)
    print(pri, name, "sha=%s" % sha_ok, "n=%d A=%d Q=%d" % (n, t["A"], t["Q"]),
          "selr=%s E=%s U=%s" % (sm["member"], sm["E"], sm.get("U")),
          "banked=%s allneg=%s => %s" % (flags, allneg, disp), flush=True)

json.dump(rows, open(PDIR + "SELR_distance_zero.json", "w"), indent=1, default=str)
outs = [r for r in rows if r.get("disp") == "OUT-HOPEFUL"]
indets = [r for r in rows if r.get("disp") == "INDETERMINATE"]
print("SEEDS: %d classified, OUT-HOPEFUL=%d INDET=%d" % (len(rows), len(outs), len(indets)), flush=True)
if indets:
    raise SystemExit("INDETERMINATE seed: %s" % indets[0]["name"])
if outs:
    print("FIRST-OUT-CANDIDATE: %s" % outs[0]["name"], flush=True)
