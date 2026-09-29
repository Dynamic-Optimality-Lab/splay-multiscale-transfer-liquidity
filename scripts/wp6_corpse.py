"""WP-6 STEP CB-00: TSRC-corpse probe (what future badness disappears?).

Corpse (SM2 n7): A=(1,(2,(7,(3,(4,(5,(6))))))), B=left-vine 7..1, x=1,
e_A=0, e_B=3, Delta 6->11. Reward r=+3. Any valid potential needs
V_before >= 3+V_after. Print best bounded-horizon continuations (DFS,
depth<=9, top-4 branches by immediate reward, exact StepEv costs) BEFORE
(state (A,B)) and AFTER (state (A',B')=(A,S_1(B))) the KEEP.
Question: what future badness exists before that disappears after?
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_splaymetric import splay_cost_events


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def main() -> int:
    # WP-6 STEP CB-00.
    step("CB-00", "TSRC-corpse probe")
    import json
    n = 7
    import ast
    A = ast.literal_eval("(1, None, (2, None, (7, (3, None, (4, None, (5, None, (6, None, None)))), None)))")
    B = ast.literal_eval("(7, (6, (5, (4, (3, (2, (1, None, None), None), None), None), None), None), None)")

    def keys(t):
        out = set()

        def rec(u):
            if u is None:
                return
            out.add(u[0])
            rec(u[1])
            rec(u[2])

        rec(t)
        return out

    assert keys(A) == set(range(1, 8)) and keys(B) == set(range(1, 8)), (keys(A), keys(B))
    x = 1
    Ap, eA = splay_cost_events(A, x)
    Bp, eB = splay_cost_events(B, x)
    step("CB-01", "e_A=%d e_B=%d reward=%d" % (eA, eB, eB - 3 * eA))

    def best_conts(a, b, depth, width=4):
        """Top-width continuations by immediate reward, DFS depth-first."""
        # returns list of (total_reward, word) best-first (bounded approx)
        cands = []
        for xx in range(1, n + 1):
            a2, ca = splay_cost_events(a, xx)
            b2, cb = splay_cost_events(b, xx)
            cands.append(("K", xx, ca, cb, cb - 3 * ca, a2, b2))
            cands.append(("D", xx, ca, 0, -3 * ca, a2, b))
        cands.sort(key=lambda z: -z[4])
        out = []
        for (m, xx, ca, cb, r, a2, b2) in cands[:width]:
            if depth <= 1:
                out.append((r, [(m, xx, ca, cb, r)]))
            else:
                sub = best_conts(a2, b2, depth - 1, width)
                br, bw = sub[0]
                out.append((r + br, [(m, xx, ca, cb, r)] + bw))
        out.sort(key=lambda z: -z[0])
        return out

    pre = best_conts(A, B, 5)
    post = best_conts(Ap, Bp, 5)
    step("CB-02", "BEFORE top-3 (total, word):")
    for tot, w in pre[:3]:
        step("CB-02", "  %d %s" % (tot, w))
    step("CB-03", "AFTER top-3 (total, word):")
    for tot, w in post[:3]:
        step("CB-03", "  %d %s" % (tot, w))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "corpse.json").write_text(
        json.dumps({"eA": eA, "eB": eB, "reward": eB - 3 * eA,
                    "before": pre[:3], "after": post[:3]},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
