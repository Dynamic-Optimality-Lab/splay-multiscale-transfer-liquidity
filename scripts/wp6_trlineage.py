"""PIVOT-25R-T §7-8: interval lineage traces.

From a post-hard-double pair-state, tag moved key-intervals by range and
follow them through a short word. Per access log: tagged ranges' B-depth
min/mean, A-cover counts, and every B-double's (twinDrop, DbDrop, pay).
Answers: does debt persist/migrate/split/merge? what A event fixes it?
"""
from __future__ import annotations
import sys
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
from wp6_transport import find, keyset, depth_of, cover_A


def step(sid, msg):
    print("[TRL %s] %s" % (sid, msg), flush=True)


def reroot(P):
    r = P
    while r["p"] is not None:
        r = r["p"]
    return r


def depths_all(P):
    return V.depths_of(reroot(P))


def main():
    import wp6_cycle_ratio as O
    Sh8 = O.shapes_of(list(range(1, 9)))
    Sh6 = O.shapes_of(list(range(1, 7)))
    traces = []

    def run(tag, A0, B0, first, word, tagranges):
        A = V.to_ptr(copy.deepcopy(A0))
        B = V.to_ptr(copy.deepcopy(B0))
        A, _ = V.splay_cap(A, first, 0, [])
        # replay first access's B phase stepwise to reach post-double state?
        # Simpler: full first access, then tag, then word.
        rep = V.replay(A0, B0, [("K", first)])
        A = V.to_ptr(copy.deepcopy(rep["endA"]))
        B = V.to_ptr(copy.deepcopy(rep["endB"]))
        rec = {"tag": tag, "ranges": tagranges, "steps": []}
        for (mo, x) in word:
            # canonical KEEP order: A-phase first, then stepwise B.
            A, _ = V.splay_cap(A, x, 0, [])
            da = depths_all(A)
            db = depths_all(B)
            cov = {}
            for name, (lo, hi) in tagranges.items():
                cov[name] = {"bmin": min(db[y] for y in range(lo, hi + 1)),
                             "bmean": sum(db[y] for y in range(lo, hi + 1)) /
                             (hi - lo + 1),
                             "acover": len(cover_A(A, (lo, hi)))}
            st = {"acc": [mo, x], "dA_x": da[x],
                  "dB_x": db.get(x, None), "cov": cov, "doubles": []}
            # stepwise B with per-double pay
            if mo == "K":
                import liquidity.legacy_embedding as PE
                Bw = B
                while True:
                    nd = find(reroot(Bw), x)
                    if nd["p"] is None:
                        break
                    p = nd["p"]
                    g = p["p"]
                    rA = [k for k, v in depths_all(A).items() if v == 0][0]
                    tw0 = 1 if rA == reroot(Bw)["k"] else 0
                    D0 = sum(depths_all(Bw).values())
                    if g is None:
                        if p["l"] is nd:
                            PE._rot_right(p)
                        else:
                            PE._rot_left(p)
                        kind = "zig"
                    else:
                        if p["l"] is nd and g["l"] is p:
                            PE._rot_right(g)
                            PE._rot_right(p)
                            kind = "LL"
                        elif p["r"] is nd and g["r"] is p:
                            PE._rot_left(g)
                            PE._rot_left(p)
                            kind = "RR"
                        elif p["r"] is nd and g["l"] is p:
                            PE._rot_left(p)
                            PE._rot_right(g)
                            kind = "LR"
                        else:
                            PE._rot_right(p)
                            PE._rot_left(g)
                            kind = "RL"
                    Bw = reroot(Bw)
                    tw1 = 1 if rA == Bw["k"] else 0
                    D1 = sum(depths_all(Bw).values())
                    if kind != "zig":
                        st["doubles"].append(
                            {"kind": kind, "tw": 2 * (tw1 - tw0),
                             "db": D0 - D1})
                B = Bw
            rec["steps"].append(st)
        traces.append(rec)
        step("T", "%s: %d accesses traced" % (tag, len(word)))

    # Trace A: L4c aftermath. Post (255,2,x8): tag descended outer blocks.
    # The last double pushed outer mass down; follow keys 1..4 (low) + re-hit 8.
    run("A-L4c", Sh8[255], Sh8[2], 8, [("K", 2), ("K", 8), ("K", 1)],
        {"low": (1, 4), "mid": (5, 7)})
    # Trace B: D2-trade aftermath (0,74,x1 @n6 in 1..6; embed at n=8? use n=6 pair + word in 1..6)
    Sh6b = Sh6
    run("B-D2trade", Sh6b[0], Sh6b[74], 1, [("K", 2), ("K", 1), ("K", 3)],
        {"chain": (1, 3), "rest": (4, 6)})
    # Trace C: twin-pair contrast states from bank RR ambiguous pair:
    # reconstruct: need the two PAIR states (pre-access pairs). Approximate
    # with fresh L4a-like accesses? Instead trace post states of two
    # same-geometry accesses differing in twin: use (A vine, B) pairs:
    run("C-twinkept", Sh8[0], Sh8[89], 3, [("K", 3), ("K", 5)],
        {"deep": (1, 3)})
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / "lineage_bank.json").write_text(
        json.dumps(traces, indent=1, default=str), encoding="utf-8")
    for rec in traces:
        print("[TRL %s]" % rec["tag"])
        for st in rec["steps"]:
            print("  acc=%s dAx=%s dBx=%s cov=%s dbl=%s" %
                  (st["acc"], st["dA_x"], st["dB_x"], st["cov"],
                   st["doubles"]))
    step("S", "saved lineage_bank.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
