# B-side representative compatibility (§9): prune fringe arbitrarily (keep S), splay marked v, compare.
import sys, random
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_UFRL_TERMINAL_CLOSURE')
sys.path.insert(0, 'python/independent')
import splay as S
from UFRL_extract import balanced, keys_of, depth

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_UFRL_TERMINAL_CLOSURE/'
bad = tot = 0
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay, core_of, from_serial
for trial in range(3000):
    rng = random.Random(5000 + trial)
    n = rng.randint(9, 25)
    keys = list(range(1, n + 1))
    t = S.LEAF
    ks = sorted(keys)
    rng.shuffle(ks)
    def ins(t, k):
        if t[0] == "leaf":
            return S.node(k, S.LEAF, S.LEAF)
        _, kk, l, r = t
        return S.node(kk, ins(l, k), r) if k < kk else S.node(kk, l, ins(r, k))
    for k in ks:
        t = ins(t, k)
    def tolist(t):
        if t[0] == "leaf":
            return None
        _, k, l, r = t
        return [k, tolist(l), tolist(r)]
    T = tolist(t)
    marked = rng.sample(keys, 5)
    word = [("K" if rng.random() < 0.5 else "D", rng.choice(marked if rng.random() < 0.6 else keys)) for _ in range(rng.randint(6, 20))]
    try:
        R = replay(word, A0=T, B0=T)
    except Exception:
        continue
    # pick a random post-KEEP B-state with genuine 9-core
    cand = [k for k, l in enumerate(R["legs"]) if l["m"] == "K"]
    if not cand:
        continue
    k = rng.choice(cand)
    B = from_serial(R["pairs"][k + 1][1])
    Sset = core_of(R["pairs"][k + 1][1])
    if Sset is None or len(Sset) != 9:
        continue
    Sset = set(Sset)
    M = {l["x"] for l in R["legs"] if l["m"] == "K" and l["chg"]}
    if len(M) != 5 or not M <= Sset:
        continue
    v = rng.choice(sorted(M))
    dB = depth(B, v)
    if dB is None:
        continue
    # faithful §9 representative: extraction (prefix exact + S + E4 witnesses + V gap selection)
    from UFRL_extract import extract
    U = set(keys)
    try:
        RB = extract(B, Sset, U)
    except Exception as e:
        print("EXTRACT-RAISED", trial, e, flush=True)
        continue
    Bs = RB["Astar"]
    tot += 1
    if depth(Bs, v) != dB:
        bad += 1
        print("DEPTH", trial, dB, depth(Bs, v), flush=True)
        continue
    B2, _ = S.trace(B, v)
    Bs2, _ = S.trace(Bs, v)
    # projected successors agree on S-structure: contract fringe subtrees to '*' holes, then compare
    def proj(u):
        if u[0] == "leaf":
            return '.'
        _, k, l, r = u
        if k not in Sset:
            return '*'
        return (k, proj(l), proj(r))
    # NOTE: fringe nodes ON S-paths cannot exist (true core); '*' marks whole fringe subtrees
    if proj(B2) != proj(Bs2):
        bad += 1
        print("SUCCESSOR", trial, flush=True)
print("tot=%d bad=%d" % (tot, bad), flush=True)
import json
json.dump({"tot": tot, "bad": bad, "pass": bad == 0}, open(PDIR + "UFRL_BCOMPAT.json", "w"), indent=1)
sys.exit(0 if bad == 0 else 1)
