# CRA earliest-residual evidence builder (fresh re-derivation for the record).
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay, totals, core_of
from CRA_strict_msink_membership import strict_msink, intervals
from CRA_segment_memberships import full_banked, keep_support, genuine_keys
from CRA_cyclic_coverage_engine import fresh_segment, classify_segment

CANON = ("D5,D4,D3,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D1,D9,"
         "D5,D4,K3,K7,D5,K1,D9,D8,K9,K5,K7,K1,K9,D8,D2,D6,D1,D9")
W = [(t[0], int(t[1:])) for t in CANON.split(",")]
R = replay(W)
n = len(W)
ev = {"canon": CANON,
      "sha": __import__("hashlib").sha256(CANON.encode("ascii")).hexdigest(),
      "provenance": {"seed": "concat35", "layer": "L0L1", "idx": 191,
                     "op": "insert D3 at gap 2 (L1 insertion order g=2,k=3)"},
      "tot": totals(R["legs"]), "closed": R["S1"] == R["S0"],
      "agree": R["agree"],
      "gkeys": genuine_keys(R["legs"]),
      "cores9": all((lambda c: c is not None and len(c) == 9)(core_of(p[1])) for p in R["pairs"])}
sm = strict_msink(R["legs"])
ev["strict_msink"] = sm
fb = full_banked(R["legs"], R["pairs"], R["snaps"])
ev["direct20"] = {k: bool(v) for k, v in fb.items()}
pre = R["pairs"][:-1]
reps = sorted([(a, b) for a in range(n) for b in range(a + 1, n) if pre[a] == pre[b]])
# BOTH cyclic directions per repeat pair (each direction is a closed segment)
segs = []
seen = set()
for (a, b) in reps:
    for (x, y) in ((a, b), (b, a)):
        if (x, y) in seen:
            continue
        seen.add((x, y))
        c = classify_segment(W, R, x, y)
        segs.append({"a": x, "b": y, "len": (y - x) % n, "covered": c["covered"],
                     "why": c["why"], "A": c.get("A"), "Q": c.get("Q"),
                     "xcheck": c.get("xcheck")})
ev["repeats"] = reps
ev["segments"] = segs
ev["nsegments"] = len(segs)
# anchored split at 18 detail
ev["split18"] = [s for s in segs if (s["a"], s["b"]) in ((0, 18), (18, 0), (18, 36 % n))]
open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT/CRA_potential_new_coverage_candidates.json', 'w').write(
    json.dumps({"earliest": ev}, indent=1, default=str))
print("member:", sm["member"], "sinks:", sm["sinks"], "E:", sm["E"], "t:", sm["t"], flush=True)
print("direct20 any:", any(ev["direct20"].values()), flush=True)
print("segments tested:", len(segs), "covered:", [s for s in segs if s["covered"]], flush=True)
print("Q<=2A:", ev["tot"]["Q"] <= 2 * ev["tot"]["A"], flush=True)
