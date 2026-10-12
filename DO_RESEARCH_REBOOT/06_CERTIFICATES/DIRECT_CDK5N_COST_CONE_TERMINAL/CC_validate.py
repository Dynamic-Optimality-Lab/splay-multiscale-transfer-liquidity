# Frozen randomized diagnostic validation (§17): 40k words + 10k mutants.
import sys, json, random
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'python/independent')
from CRA_pointer_tuple_replay import replay, core_of
from CRA_segment_memberships import genuine_keys
import splay as S

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COST_CONE_TERMINAL/'

def rand_tree(rng, keys):
    # permutation-insertion BST (diagonal init family)
    ks = sorted(keys)
    rng.shuffle(ks)
    t = S.LEAF
    for k in ks:
        t = S.trace(t, k)[0] if False else _ins(t, k)
    return t

def _ins(t, k):
    if t[0] == "leaf":
        return S.node(k, S.LEAF, S.LEAF)
    _, kk, l, r = t
    if k < kk:
        return S.node(kk, _ins(l, k), r)
    return S.node(kk, l, _ins(r, k))

def tolist(t):
    if t[0] == "leaf":
        return None
    _, k, l, r = t
    return [k, tolist(l), tolist(r)]

def gen_word(rng, keys, marked, ln):
    w = []
    for _ in range(ln):
        if rng.random() < 0.5:
            w.append(("K", rng.choice(marked)))
        else:
            w.append(("D", rng.choice(keys)))
    return w

cats = {"invalid": 0, "nonclosed": 0, "outside": 0, "holds": 0, "counterexample": 0}
ces = []
tot = 0
for seed in (9, 25, 126, 20261012):
    rng = random.Random(seed)
    for i in range(10000):
        n = rng.randint(9, 20)
        keys = list(range(1, n + 1))
        T = tolist(rand_tree(rng, keys))
        marked = rng.sample(keys, 5)
        w = gen_word(rng, keys, marked, rng.randint(1, 80))
        tot += 1
        try:
            R = replay(w, A0=T, B0=T)
        except Exception:
            cats["invalid"] += 1
            continue
        if not (R["S1"] == R["S0"] and R["agree"]):
            cats["nonclosed"] += 1
            continue
        if sorted({l["x"] for l in R["legs"] if l["m"] == "K" and l["chg"]}) != sorted(marked) and len({l["x"] for l in R["legs"] if l["m"] == "K" and l["chg"]}) != 5:
            cats["outside"] += 1
            continue
        if any(core_of(p[1]) is None or len(core_of(p[1])) != 9 for p in R["pairs"]):
            cats["outside"] += 1
            continue
        A = sum(l["a"] for l in R["legs"])
        Q = sum(l["q"] for l in R["legs"])
        if Q > 2 * A:
            cats["counterexample"] += 1
            ces.append({"seed": seed, "i": i, "A": A, "Q": Q})
        else:
            cats["holds"] += 1
    print("seed %d done: %s" % (seed, cats), flush=True)
# mutations (10k): insert/remove/replace DELETE, swap adjacent DELETEs, rotate closed, concat closed
mut_cats = {"invalid": 0, "nonclosed": 0, "outside": 0, "holds": 0, "counterexample": 0}
rng = random.Random(20261012)
made = 0
while made < 10000:
    n = rng.randint(9, 20)
    keys = list(range(1, n + 1))
    T = tolist(rand_tree(rng, keys))
    marked = rng.sample(keys, 5)
    w = gen_word(rng, keys, marked, rng.randint(5, 40))
    op = rng.randint(0, 5)
    dpos = [i for i, (m, _) in enumerate(w) if m == "D"]
    if op == 0 and dpos:
        w2 = w[:rng.choice(dpos)] + w[rng.choice(dpos) + 1:]
    elif op == 1:
        g = rng.randint(0, len(w))
        w2 = w[:g] + [("D", rng.choice(keys))] + w[g:]
    elif op == 2 and dpos:
        i = rng.choice(dpos)
        w2 = list(w)
        w2[i] = ("D", rng.choice(keys))
    elif op == 3 and len(dpos) >= 2:
        i, j = rng.sample(dpos, 2)
        w2 = list(w)
        w2[i], w2[j] = w2[j], w2[i]
    elif op == 4:
        k = rng.randrange(len(w)) if w else 0
        w2 = [w[(k + t) % len(w)] for t in range(len(w))] if w else w
    elif op == 5:
        wB = gen_word(rng, keys, marked, rng.randint(5, 40))
        w2 = w + wB
    else:
        continue
    made += 1
    try:
        R = replay(w2, A0=T, B0=T)
    except Exception:
        mut_cats["invalid"] += 1
        continue
    if not (R["S1"] == R["S0"] and R["agree"]):
        mut_cats["nonclosed"] += 1
        continue
    if len({l["x"] for l in R["legs"] if l["m"] == "K" and l["chg"]}) != 5:
        mut_cats["outside"] += 1
        continue
    if any(core_of(p[1]) is None or len(core_of(p[1])) != 9 for p in R["pairs"]):
        mut_cats["outside"] += 1
        continue
    A = sum(l["a"] for l in R["legs"])
    Q = sum(l["q"] for l in R["legs"])
    if Q > 2 * A:
        mut_cats["counterexample"] += 1
    else:
        mut_cats["holds"] += 1
print("mutants:", mut_cats, flush=True)
json.dump({"words": tot, "cats": cats, "counterexamples": ces, "mutants": mut_cats}, open(PDIR + "CC_VALIDATION.json", "w"), indent=1)
print("VALIDATION DONE", flush=True)
sys.exit(0 if (cats["counterexample"] == 0 and mut_cats["counterexample"] == 0) else 2)
