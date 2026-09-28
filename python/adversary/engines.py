"""WP-4 STEP 114: nine budgeted adversarial engines (propose; exact evaluator disposes).

Budgets frozen in prereg/liquidity_search_space.yaml; episode counts operationalized
in planning/WP4_CONTRACT.md REQ-018. Deterministic (own DRBG + seeds). Engines never
touch H4L/OOD/clean-room bytes. Each engine yields (episodes, record).
"""
from __future__ import annotations
import hashlib

from solver import legality as LG

ENGINE_SEEDS = {"uniform": 101, "structured": 102, "hillclimb": 103, "anneal": 104,
                "genetic": 105, "rotneigh": 106, "splice": 107, "motif": 108,
                "generalize": 109}


class DRBG:
    """WP-4 STEP 114: engine-local exact-uniform DRBG."""

    def __init__(self, engine: str):
        self.seed = b"wp4-adversary-v1"
        self.stream = engine.encode()
        self.ctr = 0

    def _block(self) -> bytes:
        self.ctr += 1
        return hashlib.sha256(self.seed + b"|" + self.stream + b"|"
                              + self.ctr.to_bytes(8, "big")).digest()

    def below(self, n: int) -> int:
        assert n > 0
        bound = (1 << 256) - ((1 << 256) % n)
        while True:
            v = int.from_bytes(self._block(), "big")
            if v < bound:
                return v % n

    def irange(self, lo: int, hi: int) -> int:
        return lo + self.below(hi - lo + 1)

    def choice(self, seq):
        return seq[self.below(len(seq))]


def _balanced(keys):
    if not keys:
        return None
    m = len(keys) // 2
    return [keys[m], _balanced(keys[:m]), _balanced(keys[m + 1:])]


def _vine_right(n):
    t = None
    for k in range(n, 0, -1):
        t = [k, None, t]
    return t


def _vine_left(n):
    t = None
    for k in range(1, n + 1):
        t = [k, t, None]
    return t


def _insert(t, k):
    if t is None:
        return [k, None, None]
    if k < t[0]:
        return [t[0], _insert(t[1], k), t[2]]
    return [t[0], t[1], _insert(t[2], k)]


def _rtree(n, rng):
    keys = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = rng.below(i + 1)
        keys[i], keys[j] = keys[j], keys[i]
    t = None
    for k in keys:
        t = _insert(t, k)
    return t


def _tree(shape, n, rng):
    return {"balanced": _balanced(list(range(1, n + 1))), "vine-right": _vine_right(n),
            "vine-left": _vine_left(n), "random-bst": _rtree(n, rng)}[shape]


def _mk(n, T0, H, engine):
    LG.check(n, T0, H)
    return {"n": n, "T0": T0, "H": H, "battery": "adversarial-" + engine,
            "id": LG.episode_id(n, T0, H)}


def _rand_history(n, rng, lo=2, hi=8):
    L = rng.irange(lo, hi)
    return [[rng.choice(["KEEP", "DELETE"]), rng.irange(1, n)] for _ in range(L)]


def uniform(draws=50000):
    """WP-4 STEP 114: uniform random episodes (sizes 8..64)."""
    print("[WP-4][STEP 114] engine uniform: %d draws" % draws, flush=True)
    rng = DRBG("uniform")
    eps = []
    for _ in range(draws):
        n = rng.choice([8, 16, 32, 64])
        T0 = _tree(rng.choice(["balanced", "vine-right", "vine-left", "random-bst"]), n, rng)
        eps.append(_mk(n, T0, _rand_history(n, rng), "uniform"))
    return eps, {"engine": "uniform", "draws": draws, "seed": 101, "episodes": len(eps)}


STRUCT_FAMS = [("vine-right", "DDKK"), ("vine-right", "BURST"), ("vine-left", "DDKK"),
               ("vine-left", "DRAIN"), ("balanced", "DDKK"), ("balanced", "ALT"),
               ("random-bst", "DDKK"), ("random-bst", "BOUND"), ("vine-right", "NEST"),
               ("vine-left", "MIRROR"), ("balanced", "RDEL"), ("random-bst", "ALT")]


def _fam_history(fam, n, rng):
    a = rng.irange(1, n - 1)
    L = rng.irange(2, 8)
    if fam == "DDKK":
        return [["DELETE", a], ["DELETE", a + 1], ["KEEP", a + 1], ["KEEP", a]]
    if fam == "BURST":
        d = rng.irange(2, 5)
        return [["DELETE", rng.irange(1, n)] for _ in range(d)] + \
               [["KEEP", rng.irange(1, n)] for _ in range(max(1, L - d))]
    if fam == "DRAIN":
        x = rng.irange(1, n)
        return [["KEEP", x]] * rng.irange(3, 5) + [["KEEP", min(n, x + 1)]]
    if fam == "ALT":
        return [[["KEEP", "DELETE"][i % 2], rng.irange(1, n)] for i in range(max(4, L))]
    if fam == "BOUND":
        return [[rng.choice(["KEEP", "DELETE"]), rng.choice([1, n])] for _ in range(L)]
    if fam == "NEST":
        c = rng.irange(3, n - 2)
        return [["KEEP" if i % 2 == 0 else "DELETE", x]
                for i, x in enumerate([c, c - 1, c + 1, c - 2, c + 2][:L])]
    if fam == "MIRROR":
        H = [[rng.choice(["KEEP", "DELETE"]), rng.irange(1, n)] for _ in range(L)]
        return [[m, n + 1 - x] for m, x in H] + [[m, x] for m, x in H]
    if fam == "RDEL":
        x = rng.irange(1, n)
        return [["DELETE", x]] * rng.irange(2, 6) + [["KEEP", x]]
    return _rand_history(n, rng)


def structured(per=250):
    """WP-4 STEP 114: 12 families x 4 sizes x 250 = 12000 episodes."""
    print("[WP-4][STEP 114] engine structured", flush=True)
    rng = DRBG("structured")
    eps = []
    for shape, fam in STRUCT_FAMS:
        for n in (8, 16, 32, 64):
            for _ in range(per):
                eps.append(_mk(n, _tree(shape, n, rng), _fam_history(fam, n, rng), "structured"))
    return eps, {"engine": "structured", "families": 12, "sizes": [8, 16, 32, 64],
                 "per": per, "seed": 102, "episodes": len(eps)}


def _mutate_ep(rng, ep):
    import copy
    n, T0, H = ep["n"], copy.deepcopy(ep["T0"]), [list(s) for s in ep["H"]]
    op = rng.below(5)
    if op == 0 and H:
        i = rng.below(len(H))
        H[i][1] = min(n, max(1, H[i][1] + rng.choice([-2, -1, 1, 2])))
    elif op == 1 and H:
        i = rng.below(len(H))
        H[i][0] = "DELETE" if H[i][0] == "KEEP" else "KEEP"
    elif op == 2 and len(H) < 8:
        H.append([rng.choice(["KEEP", "DELETE"]), rng.irange(1, n)])
    elif op == 3 and len(H) > 2:
        H.pop(rng.below(len(H)))
    else:
        n = rng.choice([8, 16, 32, 64])
        T0 = _tree(rng.choice(["balanced", "vine-right", "vine-left", "random-bst"]), n, rng)
        H = _rand_history(n, rng)
    try:
        return _mk(n, T0, H, "search")
    except ValueError:
        return ep


def _seed_episodes(rng, count=20):
    out = []
    a = 14
    out.append(_mk(28, _vine_right(28),
                   [["DELETE", 27], ["DELETE", 28], ["KEEP", 28], ["KEEP", 27]], "search"))
    out.append(_mk(16, _vine_right(16),
                   [["DELETE", a], ["DELETE", a + 1], ["KEEP", a + 1], ["KEEP", a]], "search"))
    while len(out) < count:
        n = rng.choice([8, 16, 32])
        out.append(_mk(n, _tree(rng.choice(["balanced", "vine-right"]), n, rng),
                        _rand_history(n, rng), "search"))
    return out


def _shortfall(evaluate, ep) -> int:
    try:
        res = evaluate(ep["n"], ep["T0"], ep["H"])
    except ValueError:
        return -1
    return max([kp["need"] - kp["paid"] for kp in res["keeps"]] + [0])


def hillclimb(evaluate, steps=20000, restarts=5):
    """WP-4 STEP 114: hillclimb residual-hunt (fitness = max KEEP shortfall)."""
    print("[WP-4][STEP 114] engine hillclimb", flush=True)
    rng = DRBG("hillclimb")
    eps, best, viol = [], 0, 0
    for _ in range(restarts):
        cur = rng.choice(_seed_episodes(rng))
        cur_f = _shortfall(evaluate, cur)
        for _ in range(steps // restarts):
            nxt = _mutate_ep(rng, cur)
            f = _shortfall(evaluate, nxt)
            if f >= cur_f:
                cur, cur_f = nxt, f
        eps.append(_mk(cur["n"], cur["T0"], cur["H"], "hillclimb"))
        best = max(best, cur_f)
        viol += sum(1 for kp in evaluate(cur["n"], cur["T0"], cur["H"])["keeps"]
                    if kp["paid"] < kp["need"])
    return eps, {"engine": "hillclimb", "steps": steps, "restarts": restarts,
                 "seed": 103, "best_shortfall": best, "final_violations": viol}


def anneal(evaluate, steps=20000, restarts=5):
    """WP-4 STEP 114: simulated-annealing residual-hunt (deterministic schedule)."""
    print("[WP-4][STEP 114] engine anneal", flush=True)
    rng = DRBG("anneal")
    eps, best, viol = [], 0, 0
    for _ in range(restarts):
        cur = rng.choice(_seed_episodes(rng))
        cur_f = _shortfall(evaluate, cur)
        total = steps // restarts
        for t in range(total):
            nxt = _mutate_ep(rng, cur)
            f = _shortfall(evaluate, nxt)
            temp = 1.0 - t / total
            if f >= cur_f or rng.below(1000) < int(1000 * temp * 0.05):
                cur, cur_f = nxt, f
        eps.append(_mk(cur["n"], cur["T0"], cur["H"], "anneal"))
        best = max(best, cur_f)
        viol += sum(1 for kp in evaluate(cur["n"], cur["T0"], cur["H"])["keeps"]
                    if kp["paid"] < kp["need"])
    return eps, {"engine": "anneal", "steps": steps, "restarts": restarts,
                 "seed": 104, "best_shortfall": best, "final_violations": viol}


def genetic(evaluate, pop=100, gens=200, restarts=3):
    """WP-4 STEP 114: genetic residual-hunt (splice crossover + mutation)."""
    print("[WP-4][STEP 114] engine genetic", flush=True)
    rng = DRBG("genetic")
    eps, best, viol = [], 0, 0
    for _ in range(restarts):
        pool = _seed_episodes(rng, count=pop)
        for _ in range(gens):
            scored = [(_shortfall(evaluate, e), e) for e in pool]
            scored.sort(key=lambda t: -t[0])
            best = max(best, scored[0][0])
            elite = [e for _, e in scored[:10]]
            nxt = list(elite)
            while len(nxt) < pop:
                a, b = rng.choice(elite), rng.choice(elite)
                cut = rng.below(len(a["H"]))
                H = [list(s) for s in a["H"][:cut]] + [list(s) for s in b["H"][cut:cut + 8]]
                H = H[:8] or [list(s) for s in a["H"]]
                try:
                    child = _mk(a["n"], a["T0"], H, "search")
                except ValueError:
                    child = rng.choice(elite)
                nxt.append(_mutate_ep(rng, child) if rng.below(2) else child)
            pool = nxt
        top = max(pool, key=lambda e: _shortfall(evaluate, e))
        eps.append(_mk(top["n"], top["T0"], top["H"], "genetic"))
        viol += sum(1 for kp in evaluate(top["n"], top["T0"], top["H"])["keeps"]
                    if kp["paid"] < kp["need"])
    return eps, {"engine": "genetic", "pop": pop, "gens": gens, "restarts": restarts,
                 "seed": 105, "best_shortfall": best, "final_violations": viol}


def rotneigh(count=10000):
    """WP-4 STEP 114: rotation-neighborhood (single-step key/mode perturbations)."""
    print("[WP-4][STEP 114] engine rotneigh", flush=True)
    rng = DRBG("rotneigh")
    eps = []
    bases = _seed_episodes(rng)
    for i in range(count):
        m = _mutate_ep(rng, rng.choice(bases))
        eps.append(_mk(m["n"], m["T0"], m["H"], "rotneigh"))
    return eps, {"engine": "rotneigh", "neighborhoods": count, "seed": 106,
                 "episodes": len(eps)}


def splice(count=5000):
    """WP-4 STEP 114: history splicing across episodes."""
    print("[WP-4][STEP 114] engine splice", flush=True)
    rng = DRBG("splice")
    eps, made = [], 0
    bases = _seed_episodes(rng, count=40)
    while made < count:
        a, b = rng.choice(bases), rng.choice(bases)
        if a["n"] != b["n"]:
            continue
        cut = rng.below(len(a["H"]) + 1)
        H = [list(s) for s in a["H"][:cut] + b["H"][:8 - cut]]
        if not (2 <= len(H) <= 16):
            continue
        try:
            eps.append(_mk(a["n"], a["T0"], H, "splice"))
            made += 1
        except ValueError:
            continue
    return eps, {"engine": "splice", "splices": count, "seed": 107, "episodes": len(eps)}


def motif(per_scale=1000):
    """WP-4 STEP 114: motif episodes at 4 size scales."""
    print("[WP-4][STEP 114] engine motif", flush=True)
    rng = DRBG("motif")
    eps = []
    for n in (8, 16, 32, 64):
        for _ in range(per_scale):
            fam = rng.choice(["DDKK", "BURST", "DRAIN", "ALT"])
            eps.append(_mk(n, _tree("vine-right" if rng.below(2) else "balanced", n, rng),
                            _fam_history(fam, n, rng), "motif"))
    return eps, {"engine": "motif", "scales": 4, "per_scale": per_scale,
                 "seed": 108, "episodes": len(eps)}


def generalize(witnesses, per_witness=8):
    """WP-4 STEP 114: generalize each witness 8 ways (size/key/history variants)."""
    print("[WP-4][STEP 114] engine generalize", flush=True)
    rng = DRBG("generalize")
    eps = []
    for w in witnesses:
        n, H = w["n"], [list(s) for s in w["H"]]
        for _ in range(per_witness):
            op = rng.below(4)
            if op == 0:
                nn = rng.choice([8, 16, 32, 64])
                HH = [[m, min(nn, max(1, x))] for m, x in H]
                eps.append(_mk(nn, _tree("balanced", nn, rng), HH, "generalize"))
            elif op == 1:
                HH = [[m, min(n, max(1, x + rng.choice([-2, 2])))] for m, x in H]
                eps.append(_mk(n, w["T0"], HH, "generalize"))
            elif op == 2 and len(H) < 12:
                HH = H + [[rng.choice(["KEEP", "DELETE"]), rng.irange(1, n)]]
                eps.append(_mk(n, w["T0"], HH, "generalize"))
            else:
                eps.append(_mk(n, _tree(rng.choice(["vine-right", "vine-left"]), n, rng),
                                H, "generalize"))
    return eps, {"engine": "generalize", "witnesses": len(witnesses),
                 "per_witness": per_witness, "seed": 109, "episodes": len(eps)}
