"""PIVOT-25R-U §2: independent repository replay of the 42-transition
joint-depth countercertificate (keys 0..7 translated +1 to 1..8).
Checks BST validity, legality, pre-depths, post-trees, StepEv costs,
q, twin bits, raw/corrected rewards, histogram cancellation (64 cells),
positive-integer multiplicities, and surplus == 10971177."""
from __future__ import annotations
import sys
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V

CERT = Path("C:/Users/SAIFMA~1/AppData/Local/Temp/opencode/jointcert/"
            "joint_depth_template_countercertificate.json")


def step(sid, msg):
    print("[JCR %s] %s" % (sid, msg), flush=True)


def shift(t):
    if t is None:
        return None
    return [t[0] + 1, shift(t[1]), shift(t[2])]


def inorder_list(t):
    if t is None:
        return []
    return inorder_list(t[1]) + [t[0]] + inorder_list(t[2])


def depths_list(t):
    out = {}

    def go(nd, d):
        if nd is None:
            return
        out[nd[0]] = d
        go(nd[1], d + 1)
        go(nd[2], d + 1)
    go(t, 0)
    return out


def main():
    D = json.loads(CERT.read_text())
    n = D["n"]
    assert n == 8, n
    items = D["items"]
    cancel = [0] * (n * n)
    surplus = 0
    for k, it in enumerate(items):
        m = it["multiplicity"]
        assert type(m) is int and m > 0, (k, m)
        A, B = shift(it["A"]), shift(it["B"])
        assert inorder_list(A) == list(range(1, n + 1)), k
        assert inorder_list(B) == list(range(1, n + 1)), k
        x = it["key"] + 1
        mo = it["mode"]
        rep = V.replay(A, B, [(mo[0], x)])
        acc = rep["accesses"][0]
        a, q = acc["a"], acc["q"]
        assert a == it["a"] == len(acc["asteps"]), (k, a, it["a"])
        if mo == "KEEP":
            ndb = sum(1 for s in acc["bsteps"] if s["kind"] == "double")
            assert ndb == q, (k, ndb, q)
            w = q - 2 * a
        else:
            assert mo == "DELETE" and q == 0, (k, mo, q)
            w = -2 * a
        assert w == it["raw_reward"], (k, w)
        assert rep["endA"] == shift(it["A_after"]), (k, "Apost")
        assert rep["endB"] == shift(it["B_after"]), (k, "Bpost")
        t0 = 1 if A[0] == B[0] else 0
        t1 = 1 if rep["endA"][0] == rep["endB"][0] else 0
        assert t0 == it["twin_before"] and t1 == it["twin_after"], (k,)
        r = w - 2 * (t1 - t0)
        assert r == it["corrected_reward"], (k, r)
        da, db = depths_list(A), depths_list(B)
        ea = rep["endA"]
        eb = rep["endB"]
        pa = V.to_ptr(copy.deepcopy(ea))
        pb = V.to_ptr(copy.deepcopy(eb))
        da2, db2 = V.depths_of(pa), V.depths_of(pb)
        for y in range(1, n + 1):
            cancel[n * da[y] + db[y]] += m
            cancel[n * da2[y] + db2[y]] -= m
        surplus += m * r
        if (k + 1) % 14 == 0:
            step("G", "%d/%d surplus=%d" % (k + 1, len(items), surplus))
    assert len(items) == D["support"] == 42, len(items)
    assert all(v == 0 for v in cancel), [v for v in cancel if v != 0]
    assert surplus == D["positive_corrected_reward_sum"] == 10971177, surplus
    step("S", "42/42 replayed via canonical engine; 64/64 cells cancel; "
              "surplus=%d>0" % surplus)
    step("S", "ADDITIVE JOINT-DEPTH TEMPLATE REFUTED (banked, scoped §3)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
