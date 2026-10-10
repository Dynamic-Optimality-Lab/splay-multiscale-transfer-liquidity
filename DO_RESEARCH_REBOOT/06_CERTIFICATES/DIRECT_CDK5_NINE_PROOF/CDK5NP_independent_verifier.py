"""CDK5NP independent verifier (§15): fresh code path, tuple-engine-first.

Replays witness + excluded control; checks depths/costs/closure/cores/keys;
reconstructs KEEP intervals (H/c/w/R); verifies baseline, local charging,
Type K/P per debt, control predicate failure; cross-checks pointer engine.
Exact ints only. This is a finite source-fidelity check, NOT the universal
proof (which lives in CDK5NP_*_lemma/proof.md).
"""
import sys, copy, json, hashlib
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_NINE_PROOF')
import splay as S
from wp6_eventflow import to_ptr, splay_A, splay_B_push
import legacy_embedding as PE

H = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:12]
hashes = {"eventflow": H('scripts/wp6_eventflow.py'),
          "splay": H('python/independent/splay.py'),
          "legacy": H('python/liquidity/legacy_embedding.py')}

def T(t, x):
    return S.trace(t, x)[0]
def dep(t):
    out = {}
    def go(nd, d):
        if nd[0] == "leaf":
            return
        _, k, l, r = nd
        out[k] = d; go(l, d + 1); go(r, d + 1)
    go(t, 0)
    return out
def ser(t):
    if t[0] == "leaf":
        return '.'
    _, k, l, r = t
    return (k, ser(l), ser(r))
def pser(t):
    while t["p"] is not None:
        t = t["p"]
    def go(nd):
        if nd is None:
            return '.'
        return (nd["k"], go(nd["l"]), go(nd["r"]))
    return go(t)
def totup(t):
    if t is None:
        return S.LEAF
    return S.node(t[0], totup(t[1]), totup(t[2]))
def core(s, M):
    c = set()
    def path(nd, x, p):
        if nd == '.':
            return None
        k, l, r = nd
        p = p + [k]
        if k == x:
            return p
        return path(l, x, p) or path(r, x, p)
    for m in M:
        c.update(path(s, m, []))
    return c

T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]],
          [8, [7, None, None], None]], None]

def run(word):
    """Tuple-engine-first replay; pointer engine cross-check per access."""
    A = totup(copy.deepcopy(T0)); B = totup(copy.deepcopy(T0))
    P = to_ptr(copy.deepcopy(T0)); Q = to_ptr(copy.deepcopy(T0))
    assert ser(A) == ser(B)
    S0 = (ser(A), ser(B))
    legs, ok = [], True
    for (md, x) in word:
        da = dep(A).get(x, -1); assert da >= 0
        a = (da + 1) // 2
        db = dep(B).get(x, -1) if md == 'K' else None
        assert (db is None) or db >= 0
        q = db // 2 if md == 'K' else 0
        # pointer-engine cross-check (depths via serials compared post-splay)
        A = T(A, x)
        P, _ = splay_A(P, x)
        push = []
        if md == 'K':
            # independent pushed-set check via legacy trace events
            B = T(B, x)
            Q, out = splay_B_push(Q, x)
            for s in out:
                push += list(s)
        ok = ok and ser(A) == pser(P) and ser(B) == pser(Q)
        legs.append({"m": md, "x": x, "dA": da, "dB": db, "a": a, "q": q,
                     "push": sorted(set(push))})
    return legs, ok, S0, (ser(A), ser(B))

def intervals(legs):
    """KEEP intervals with H/c/w/R."""
    ki = [i for i, l in enumerate(legs) if l["m"] == "K"]
    out = []
    for n, i in enumerate(ki):
        prev = ki[n - 1]
        seg = (legs[prev + 1:i + 1] if prev < i
               else legs[prev + 1:] + legs[:i + 1])
        H = sum(l["a"] for l in seg)
        x = legs[i]["x"]
        xp = legs[prev]["x"]
        c = 1 if x != xp else 0
        q = legs[i]["q"]
        out.append({"j": n, "x": x, "H": H, "c": c, "q": q,
                    "w": q - 2 * c, "R": 2 * (H - c), "prev": legs[i - 1]})
    return out

res = {"hashes": hashes}
# witness
WIT = [('D', 5), ('D', 4), ('K', 3), ('K', 7), ('K', 1), ('D', 4), ('K', 9),
       ('D', 6), ('K', 5), ('K', 7), ('K', 1), ('K', 9), ('D', 8), ('D', 2),
       ('D', 1), ('D', 6), ('D', 9)]
legs, ok, S0, S1 = run(WIT)
M = {1, 3, 5, 7, 9}
A = totup(copy.deepcopy(T0)); B = totup(copy.deepcopy(T0))
cores = [len(core(ser(B), M))]
for (md, x) in WIT:
    A = T(A, x)
    if md == 'K':
        B = T(B, x)
    cores.append(len(core(ser(B), M)))
Atot = sum(l["a"] for l in legs); Qtot = sum(l["q"] for l in legs)
ks = [l["x"] for l in legs if l["m"] == "K"]
Ck = sum(1 for i in range(len(ks)) if ks[i] != ks[(i - 1) % len(ks)])
IV = intervals(legs)
base_ok = all(iv["H"] >= iv["c"] for iv in IV)
loc_ok = all(iv["w"] <= iv["R"] for iv in IV)
debts = []
for iv in IV:
    if iv["w"] > 0:
        l = legs[[i for i, l in enumerate(legs) if l["m"] == "K"][iv["j"]]]
        p = iv["prev"]
        tk = l["dA"] >= 3
        tp = (p["m"] == "D" and p["x"] != l["x"] and p["a"] >= 1 and l["a"] >= 1)
        debts.append({"x": l["x"], "w": iv["w"], "TypeK": tk, "TypeP": tp})
        assert tk or tp, iv
tel = (sum(iv["w"] for iv in IV) == Qtot - 2 * Ck
       and sum(iv["R"] for iv in IV) == 2 * (Atot - Ck))
res["witness"] = {"A": Atot, "Q": Qtot, "Ck": Ck, "closure": [S0[0] == S1[0], S0[1] == S1[1]],
                  "engines": ok, "cores": cores, "baseline": base_ok,
                  "local": loc_ok, "debts": debts, "telescoping": tel,
                  "Qle2A": Qtot <= 2 * Atot}
print("WITNESS:", res["witness"], flush=True)
assert Atot == 29 and Qtot == 18 and Ck == 8 and ok and base_ok and loc_ok and tel
assert all(c == 9 for c in cores) and S0[0] == S1[0] and S0[1] == S1[1]
assert Qtot <= 2 * Atot

# control
CTL = [('D', 3), ('D', 3), ('K', 3), ('K', 7), ('K', 1), ('K', 9), ('K', 5),
       ('K', 7), ('K', 1), ('K', 9)]
legs, ok, S0, S1 = run(CTL)
k3 = [l for l in legs if l["m"] == "K"][0]
gi = legs.index(k3)
prev = legs[gi - 1]
excluded = not (k3["dA"] >= 3) and not (
    prev["m"] == "D" and prev["x"] != k3["x"] and prev["a"] >= 1 and k3["a"] >= 1)
res["control"] = {"A": sum(l["a"] for l in legs), "Q": sum(l["q"] for l in legs),
                  "closure": [S0[0] == S1[0], S0[1] == S1[1]], "engines": ok,
                  "K3": {"q": k3["q"], "a": k3["a"], "prev_a": prev["a"]},
                  "excluded": excluded}
print("CONTROL:", res["control"], flush=True)
assert res["control"]["A"] == 18 and res["control"]["Q"] == 18 and ok and excluded
json.dump(res, open(RDIR / 'CDK5NP_verification_results.json', 'w'), indent=1)
print("INDEPENDENT VERIFIER: PASS", flush=True)
