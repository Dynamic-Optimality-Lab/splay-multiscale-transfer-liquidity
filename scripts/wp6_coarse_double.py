"""PIVOT-12 regressions: q/z/epsilon/W_Q accounting on all hard corpora."""
from __future__ import annotations
import sys
import json
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_adv import depths_of
import wp6_cycle_ratio as O

BD = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "coarse_double"


def save(name, obj):
    BD.mkdir(parents=True, exist_ok=True)
    (BD / name).write_text(json.dumps(obj, indent=1, sort_keys=True,
                                      default=str), encoding="utf-8")


def step(sid, msg):
    print("[CDR %s] %s" % (sid, msg), flush=True)


def replay(T0, word):
    """word = list of (mode, x). Returns per-access + totals with q/z."""
    A = to_ptr(copy.deepcopy(T0))
    B = to_ptr(copy.deepcopy(T0))
    legs = []
    Aacc = Qacc = Zacc = 0
    for (md, x) in word:
        dA = depths_of(copy.deepcopy(A)).get(x, 0)
        a = (dA + 1) // 2
        if md == "K":
            dB = depths_of(copy.deepcopy(B)).get(x, 0)
            q, z = dB // 2, dB % 2
        else:
            q = z = 0
        A, _ = splay_A(A, x)
        if md == "K":
            B, _ = splay_B_push(B, x)
        Aacc += a
        Qacc += q
        Zacc += z
        legs.append({"m": md, "x": x, "dA": dA,
                     "dB": dB if md == "K" else None,
                     "a": a, "q": q, "z": z, "eps": q - 2 * a})
    return {"legs": legs, "A": Aacc, "Q": Qacc, "Z": Zacc,
            "B": Qacc + Zacc, "WQ": Qacc - 2 * Aacc,
            "W2": (Qacc + Zacc) - 2 * Aacc}


def vine(n, left=False):
    t = None
    for k in (range(n, 0, -1) if not left else range(1, n + 1)):
        t = [k, None, t] if not left else [k, t, None]
    return t


def main():
    out = {}
    # A. n=5 B.DOUBLE killer [(K,5),(K,1),(K,5),(K,3)] -- need T0: use vine? The
    # original witness was on some T0; replay from vine-pair diagonal + report.
    # (Exact original T0 unknown here; use right-vine T0 and also search diagnostics.)
    T5 = vine(5)
    r = replay(T5, [("K", 5), ("K", 1), ("K", 5), ("K", 3)])
    step("R-A", "n=5 killer from vine T0: A=%d Q=%d Z=%d WQ=%d" %
         (r["A"], r["Q"], r["Z"], r["WQ"]))
    out["n5_killer_vineT0"] = {k: v for k, v in r.items() if k != "legs"}
    # B. n=6 5/3 cycle from achiever start u0=137 (shapes idx 1 and 5)
    G = O.build(6)
    nS, adj, Sh = G["nS"], G["adj"], G["Sh"]
    T0 = Sh[1]
    r = replay(T0, [("K", 3), ("K", 6), ("K", 3), ("K", 4), ("K", 2), ("K", 1)])
    step("R-B", "5/3 word: A=%d Q=%d Z=%d WQ=%d rhoQ=%.3f" %
         (r["A"], r["Q"], r["Z"], r["WQ"],
          (r["Q"] / r["A"]) if r["A"] else -1))
    out["n6_53"] = {k: v for k, v in r.items() if k != "legs"}
    out["n6_53"]["legs"] = r["legs"]
    # D. n=32 excursion K1+K1..K32 from (inc,dec)
    def vinci(n):
        t = None
        for k in range(n, 0, -1):
            t = [k, None, t]
        return t

    def vind(n):
        t = None
        for k in range(1, n + 1):
            t = [k, t, None]
        return t

    # NOTE replay() uses single T0 for both; need pair start -> inline it
    n = 32
    A = to_ptr(vinci(n))
    B = to_ptr(vind(n))
    word = [("K", 1)] + [("K", x) for x in range(1, n + 1)]
    legs = []
    Aacc = Qacc = Zacc = 0
    for (md, x) in word:
        dA = depths_of(copy.deepcopy(A)).get(x, 0)
        a = (dA + 1) // 2
        dB = depths_of(copy.deepcopy(B)).get(x, 0)
        q, z = dB // 2, dB % 2
        A, _ = splay_A(A, x)
        B, _ = splay_B_push(B, x)
        Aacc += a
        Qacc += q
        Zacc += z
        legs.append({"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                     "z": z, "eps": q - 2 * a, "A": Aacc, "Q": Qacc,
                     "Z": Zacc, "WQ": Qacc - 2 * Aacc})
    step("R-D", "n=32: A=%d Q=%d Z=%d WQ=%d (old W2=+9)" %
         (Aacc, Qacc, Zacc, Qacc - 2 * Aacc))
    print("  WQ trajectory:", [l["WQ"] for l in legs], flush=True)
    print("  eps trajectory:", [l["eps"] for l in legs], flush=True)
    out["n32"] = {"A": Aacc, "Q": Qacc, "Z": Zacc, "WQ": Qacc - 2 * Aacc,
                  "W2": (Qacc + Zacc) - 2 * Aacc, "legs": legs}
    save("regressions.json", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
