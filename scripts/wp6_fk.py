"""WP-6 FK: F_2/F_3 liability ladder on minimized witness (C182).

F_k(s) = max deficit (E_B - 3*S_A) over continuations of length <= k from s.
Covered at s iff F_k(s) <= pool(s) for all k. Ladder: F_1=31, F_2=42 here;
F_3 decides whether liability stabilizes (bounded => closure plausible)
or exceeds pool (=> REFUTED via argmax continuation).
F_3(s) = max(F_2(s), max over 128 successors [reward + F_2(succ)]).
Cost O((2n)^2 * n^2) per F_3 eval; file-logged progress.
Artifact: bellman/fk.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_pushledger import gen
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_adv import depths_of
from wp6_bellman import H1f
from solver import encode as E


def step(sid, msg):
    line = "[WP-6][FK %s] %s" % (sid, msg)
    print(line, flush=True)
    try:
        bd = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "bellman"
        bd.mkdir(parents=True, exist_ok=True)
        with open(bd / "fk_progress.log", "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def F1_of(A, B, keys):
    dA = depths_of(A)
    dB = depths_of(B)
    v, _ = H1f(dA, dB, keys)
    return v


def F2_of(A, B, keys):
    dA = depths_of(A)
    dB = depths_of(B)
    best = 0
    arg = None
    for x in keys:
        da = dA.get(x, 0)
        a = (da + 1) // 2
        A2 = copy.deepcopy(A)
        A2, _ = splay_A(A2, x)
        fd, _ = H1f(depths_of(A2), dB, keys)
        v = fd - 3 * a
        if v > best:
            best = v
            arg = ("DEL", x)
        B2 = copy.deepcopy(B)
        B2, _ = splay_B_push(B2, x)
        db = dB.get(x, 0)
        b = (db + 1) // 2
        fk, _ = H1f(depths_of(A2), depths_of(B2), keys)
        v = b + fk - 3 * a
        if v > best:
            best = v
            arg = ("KEEP", x, a, b, fk)
    return best, arg


def F3_of(A, B, keys, pool):
    dA = depths_of(A)
    dB = depths_of(B)
    f2, _ = F2_of(A, B, keys)
    best = [f2, ("F2",)]
    done = 0
    for x in keys:
        da = dA.get(x, 0)
        a = (da + 1) // 2
        A2 = copy.deepcopy(A)
        A2, _ = splay_A(A2, x)
        f, _ = F2_of(A2, copy.deepcopy(B), keys)
        v = f - 3 * a
        if v > best[0]:
            best = [v, ("DEL", x)]
            if v > pool:
                return best, True
        B2 = copy.deepcopy(B)
        B2, _ = splay_B_push(B2, x)
        db = dB.get(x, 0)
        b = (db + 1) // 2
        f, _ = F2_of(A2, B2, keys)
        v = b + f - 3 * a
        if v > best[0]:
            best = [v, ("KEEP", x)]
            if v > pool:
                return best, True
        done += 1
        if done % 16 == 0:
            step("FK-P", "succ %d best=%s pool=%s" % (done, best[0], pool))
    return best, False


def main() -> int:
    step("FK-00", "F_2/F_3 liability ladder on witness")
    n, T0, H = gen(6, b"bl")
    pre = E.precompute(n, T0, H)
    A, B = to_ptr(T0), to_ptr(T0)
    keys = sorted(depths_of(A).keys())
    SA = EB = 0
    for i in range(5):
        acc = pre[i]
        A, invs = splay_A(A, acc["x"])
        SA += len(invs)
        if acc["mode"] == "KEEP":
            B, pushes = splay_B_push(B, acc["x"])
            EB += len(pushes)
    pool = 3 * SA - EB
    step("FK-01", "witness state pool=%d" % pool)
    f2, arg2 = F2_of(A, B, keys)
    step("FK-02", "F2=%s arg=%s" % (f2, arg2))
    (f3, arg3), kill = F3_of(A, B, keys, pool)
    step("FK-03", "F3=%s arg=%s kill=%s" % (f3, arg3, kill))
    out = {"pool": pool, "F1": 31, "F2": f2, "F2arg": arg2, "F3": f3,
           "F3arg": arg3, "kill": kill}
    bd = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "bellman"
    bd.mkdir(parents=True, exist_ok=True)
    (bd / "fk.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str),
        encoding="utf-8")
    step("FK-04", "done kill=%s" % kill)
    return 2 if kill else 0


if __name__ == "__main__":
    sys.exit(main())
