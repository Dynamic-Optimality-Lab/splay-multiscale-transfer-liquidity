"""PIVOT-2 periodic-word hunt: replay periodic W, Floyd/hash cycle detect,
exact closed-cycle ratios to n=256. Seeds: random + killer prefixes.
Artifacts: pivot_cycle/periodic_hunt.json
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
from wp6_adv import vine, balanced

BD = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "pivot_cycle"


def step(sid, msg):
    line = "[PERIOD %s] %s" % (sid, msg)
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


def enc(P):
    if P is None:
        return None
    return (P["k"], enc(P["l"]), enc(P["r"]))


def key_enc(P):
    # canonical hashable (drop parents)
    return json.dumps(enc(P), sort_keys=True)


def run_word(A0, B0, W, cap=4000):
    A, B = copy.deepcopy(A0), copy.deepcopy(B0)
    seen = {}
    SA = EB = 0
    # per-visit cumulative (SA,EB) to compute cycle sums
    hist = []

    def h():
        return (key_enc(A), key_enc(B))

    seen[h()] = (0, 0)
    i = 0
    while i < cap:
        for (mode, x) in W:
            A, iv = splay_A(A, x)
            eB = 0
            if mode == "KEEP":
                B, p = splay_B_push(B, x)
                eB = len(p)
            SA += len(iv)
            EB += eB
            i += 1
            hh = h()
            if hh in seen:
                sa0, eb0 = seen[hh]
                return {"cycle": True, "A": SA - sa0, "B": EB - eb0,
                        "tail": i}
            seen[hh] = (SA, EB)
    return {"cycle": False}


def main():
    step("PH-00", "periodic hunt")
    best = []
    ntests = 0
    for n in (16, 32, 64, 128, 256):
        keys = list(range(1, n + 1))
        rng = random.Random(1000 + n)
        starts = []
        T0 = vine(n)
        starts.append(("vine", to_ptr(T0), to_ptr(T0)))
        T1 = balanced(keys)
        starts.append(("bal", to_ptr(T1), to_ptr(T1)))
        # diverged start: churn then use state
        A, B = to_ptr(T0), to_ptr(T0)
        for _ in range(15):
            m = rng.choice(["KEEP", "DELETE"])
            x = rng.randint(1, n)
            A, _ = splay_A(A, x)
            if m == "KEEP":
                B, _ = splay_B_push(B, x)
        starts.append(("div", A, B))
        for trial in range(12):
            L = rng.choice([2, 3, 4, 6, 8, 12, 16])
            pat = rng.choice(["alt", "kdd", "kkd", "sweep", "rand"])
            W = []
            for j in range(L):
                if pat == "alt":
                    W.append(("KEEP" if j % 2 == 0 else "DELETE",
                              rng.randint(1, n)))
                elif pat == "kdd":
                    W.append(("KEEP" if j % 3 == 0 else "DELETE",
                              rng.randint(1, n)))
                elif pat == "kkd":
                    W.append(("DELETE" if j % 3 == 2 else "KEEP",
                              rng.randint(1, n)))
                elif pat == "sweep":
                    W.append(("KEEP", (j % n) + 1))
                else:
                    W.append((rng.choice(["KEEP", "DELETE"]),
                              rng.randint(1, n)))
            for sname, A0, B0 in starts:
                ntests += 1
                r = run_word(A0, B0, W)
                if r["cycle"] and r["A"] > 0:
                    ratio = r["B"] / r["A"]
                    if not best or ratio > best[0][0]:
                        best = [(ratio, n, sname, pat, W, r)]
                    elif len(best) < 8:
                        best.append((ratio, n, sname, pat, W, r))
                elif r["cycle"] and r["A"] == 0 and r["B"] > 0:
                    step("PH-ZA", "ZERO-A POSITIVE-B CYCLE n=%d %s %s"
                         % (n, sname, W))
                    save("zeroA_kill.json",
                         {"n": n, "start": sname, "W": W, "r": r})
                    return 2
        step("PH-01", "n=%d done best=%s" %
             (n, best[0][0] if best else None))
    best.sort(key=lambda t: -t[0])
    save("periodic_hunt.json", {"ntests": ntests, "best": best[:10]})
    for b in best[:10]:
        step("PH-02", "ratio=%.4f n=%s start=%s pat=%s W=%s cyc=%s" %
             (b[0], b[1], b[2], b[3], b[4], b[5]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
