# Exclusion reasons: first-failing hypothesis per class per finalist.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD')
import MSINK_bounded_search as B
import MSINK_memberships as M

def reasons(canon):
    word = B.parse(canon)
    r = B.replay(word)
    legs = r["legs"]
    mb, bdep = B.merged_blocks(legs), r["bdep"]
    iv = B.intervals_of(legs)
    out = {}
    E = M.E_slots(iv)
    out["E"] = E
    # NP
    bad = []
    for j in range(len(iv)):
        if iv[j]["w"] > 0 and not (M.isK(iv[j], legs) or M.isP(iv[j], legs)):
            bad.append((j, iv[j]["x"], legs[iv[j]["gi"]]["dA"]))
    out["NP"] = bad
    # relays
    out["t"] = {e: M.relay(iv, e) for e in E}
    # AJ
    out["AJ"] = [(i, b["key"], mb[(i + 1) % len(mb)]["key"], b["rb"])
                 for i, b in enumerate(mb)
                 if b["delta"] > 0 and mb[(i + 1) % len(mb)]["key"] != b["rb"]]
    # AK/AL-G H4
    out["AK_H4"] = [(i, b["key"], mb[(i + 2) % len(mb)]["key"], b["rb"])
                    for i, b in enumerate(mb)
                    if b["delta"] > 0 and mb[(i + 2) % len(mb)]["key"] != b["rb"]]
    # AM G4
    out["AM_G4"] = [(i, b["key"], mb[(i + 3) % len(mb)]["key"], b["rb"])
                    for i, b in enumerate(mb)
                    if b["delta"] > 0 and mb[(i + 3) % len(mb)]["key"] != b["rb"]]
    # AN uncovered positives
    m = len(mb)
    pos = M.positives(mb)
    valid = [j for j in range(m) if M.valid_AN_packet(mb, j) is not None]
    unc = [i for i in pos if not any(i in ((j, (j + 2) % m)) for j in valid)]
    out["AN_valid_anchors"] = valid
    out["AN_uncovered"] = unc
    # MSINK stage
    out["msink"] = M.msink(iv, legs) if False else B.msink(iv, legs)
    # S1 successor / S2 shape / VR relay+payer / MR payers (for docs)
    if len(E) == 1:
        e = E[0]
        out["succ1"] = {k: iv[(e + 1) % len(iv)][k] for k in ("x", "H", "c", "q")}
    # joint-sink candidates
    out["Psink"] = [(j, iv[j]["H"], iv[j]["q"]) for j in range(len(iv))
                    if j not in E and iv[j]["c"] == 1 and iv[j]["H"] >= 3]
    return out

if __name__ == "__main__":
    for h in sys.argv[1:]:
        rows = []
        for seed in ("concat35", "mr33"):
            f = B.RDIR / ("state_" + seed) / "survivors.jsonl"
            if f.exists():
                rows += [json.loads(l) for l in open(f)]
        hit = [x for x in rows if x["sha"].startswith(h)][0]
        print("=" * 20, h[:12], "=" * 20, flush=True)
        print(json.dumps(reasons(hit["canon"]), indent=1, default=str), flush=True)
