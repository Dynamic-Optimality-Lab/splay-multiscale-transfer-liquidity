"""C-PIVOT epoch potential: LT heap-violation diff with X-clock recency.

Psi(A,B) = V(B) - V(A), V(T) = #edges parent->child with prio(parent)
< prio(child), prio(x) = last X-access time (0 if never).
Epochs: [KEEP x][DELETEs][KEEP y]; checkpoints post-KEEP (common root).
V(epoch) = BCost + dPsi - C*ACost for C in grid. Kill on max>0.
Corpus: micro seeds, steered divergence, walks, BK1/vine shapes.
Artifacts: artifacts/v04/wp6_present/0909c74a/pivot_epoch/
"""
from __future__ import annotations
import sys
import json
import copy
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_adv import vine, balanced, depths_of

BD = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" \
    / "pivot_epoch"


def step(sid, msg):
    line = "[PIVOT %s] %s" % (sid, msg)
    print(line, flush=True)
    try:
        BD.mkdir(parents=True, exist_ok=True)
        with open(BD / "progress.log", "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def save(name, obj):
    BD.mkdir(parents=True, exist_ok=True)
    (BD / name).write_text(json.dumps(obj, indent=1, sort_keys=True,
                                      default=str), encoding="utf-8")


def viols(T, prio):
    """Count heap-violating edges (parent.prio < child.prio)."""
    n = [0]

    def rec(t):
        if t is None:
            return
        for c in (t.get("l"), t.get("r")):
            if c is not None and c.get("k") is not None:
                if prio.get(t["k"], 0) < prio.get(c["k"], 0):
                    n[0] += 1
                rec(c)

    rec(T)
    return n[0]


def run_epoch_histories():
    import wp6_micro as M
    hists = []
    for s in range(10):
        n, T0, H = M.gen(s, b"bl")
        if n > 64:
            continue
        hists.append(("micro%d" % s, n, T0, H))
    for n in (16, 32):
        keys = list(range(1, n + 1))
        for t in range(3):
            T0 = vine(n) if t % 2 == 0 else balanced(keys)
            rng = random.Random(6000 + t)
            H = [[rng.choice(["KEEP", "DELETE"]), rng.randint(1, n)]
                 for _ in range(30)]
            hists.append(("walk%d_%d" % (n, t), n, T0, H))
    # steered divergence: churn + DELETE-reroot + KEEP (BK1-style)
    for n in (24,):
        keys = list(range(1, n + 1))
        T0 = vine(n)
        rng = random.Random(42)
        deep = sorted(keys, reverse=True)[:8]
        churn = [[rng.choice(["KEEP", "DELETE"]), rng.choice(deep)]
                 for _ in range(15)]
        churn += [["DELETE", 2], ["KEEP", 2]]
        hists.append(("steer%d" % n, n, T0, churn))
    return hists


def epochs_of(H):
    eps = []
    cur = None
    for mode, x in H:
        if mode == "KEEP":
            if cur is not None:
                cur["y"] = x
                eps.append(cur)
            cur = {"x": x, "dels": [], "y": None}
        else:
            if cur is not None:
                cur["dels"].append(x)
    return eps


def main():
    step("PV-00", "epoch heap-violation scan")
    CS = [1, 2, 3, 4, 6, 8, 12, 16]
    worst = {c: None for c in CS}
    nepoch = 0
    prz = None
    for name, n, T0, H in run_epoch_histories():
        A, B = to_ptr(T0), to_ptr(T0)
        prio = {}
        t = 0
        # state BEFORE first KEEP = virtual checkpoint (T0,T0)
        PA, PB = copy.deepcopy(A), copy.deepcopy(B)
        snap = dict(prio)  # frozen prio snapshot at previous checkpoint
        for ep in epochs_of(H):
            # run dels
            acost = 0
            for d in ep["dels"]:
                t += 1
                prio[d] = t
                A, iv = splay_A(A, d)
                acost += len(iv)
            # terminal keep
            y = ep["y"]
            t += 1
            prio[y] = t
            A, iv = splay_A(A, y)
            acost += len(iv)
            B, p = splay_B_push(B, y)
            bcost = len(p)
            psi0 = viols(PB, snap) - viols(PA, snap)
            snap = dict(prio)  # freeze post-epoch snapshot
            psi1 = viols(B, snap) - viols(A, snap)
            nepoch += 1
            for c in CS:
                v = bcost + (psi1 - psi0) - c * acost
                if worst[c] is None or v > worst[c][0]:
                    worst[c] = (v, name, ep, bcost, psi0, psi1,
                                acost)
            PA, PB = copy.deepcopy(A), copy.deepcopy(B)
        step("PV-01", "%s epochs done" % name)
    out = {"nepoch": nepoch,
           "worst": {str(c): worst[c] for c in CS}}
    save("heapviol.json", out)
    for c in CS:
        step("PV-02", "C=%d worst=%s" % (c, worst[c]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
