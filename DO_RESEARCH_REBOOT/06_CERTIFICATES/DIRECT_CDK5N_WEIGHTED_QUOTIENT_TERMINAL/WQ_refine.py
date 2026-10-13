# Weighted refinement implementation + Gate-D validation (STEP 09 + Gate D).
import sys, json, random
sys.path.insert(0, 'python/independent')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_WEIGHTED_QUOTIENT_TERMINAL/'

def refine(n, edges, init, max_rounds=256, cap_blocks=2000000):
    # edges: list of (u,v,w). init: list of block ids. Returns (part, rounds, stable).
    # Bisimulation signatures (stronger than WQ-1 min-weight; sound for it): sig(x)=sorted((part[dst],w)).
    # Split within current blocks only (never merge).
    import collections
    part = list(init)
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    rounds = 0
    for _ in range(max_rounds):
        sig_of = {}
        new_id = {}
        nxt = []
        changed = False
        for x in range(n):
            s = tuple(sorted((part[v], w) for v, w in adj[x]))
            key = (part[x], s)
            if key not in new_id:
                new_id[key] = len(new_id)
            nxt.append(new_id[key])
        # check stability under WQ-1 min-criterion too (report both)
        if nxt == part:
            return nxt, rounds + 1, True
        part = nxt
        rounds += 1
        if len(set(part)) > cap_blocks:
            return part, rounds, False
    return part, rounds, False

def check_stable(n, edges, part):
    # WQ-1 min-weight stability: m_C equal within blocks
    from collections import defaultdict
    bysrc = defaultdict(list)
    for u, v, w in edges:
        bysrc[u].append((part[v], w))
    minw = {}
    for x in range(n):
        d = {}
        for c, w in bysrc.get(x, []):
            d[c] = min(d.get(c, float('inf')), w)
        minw[x] = d
    blocks = defaultdict(list)
    for x in range(n):
        blocks[part[x]].append(x)
    for b, xs in blocks.items():
        ds = [minw[x] for x in xs]
        if any(d != ds[0] for d in ds[1:]):
            return False
    return True

def check_reverse(n, edges, part):
    # uniform reverse lifting: quotient edge B->C (weight m) realizable from every x in B at m
    from collections import defaultdict
    qedges = {}
    for u, v, w in edges:
        key = (part[u], part[v])
        qedges[key] = min(qedges.get(key, float('inf')), w)
    bysrc = defaultdict(list)
    for u, v, w in edges:
        bysrc[u].append((part[v], w))
    blocks = defaultdict(list)
    for x in range(n):
        blocks[part[x]].append(x)
    for (b, c), m in qedges.items():
        for x in blocks[b]:
            if not any(cc == c and w == m for cc, w in bysrc.get(x, [])):
                return False
    return True

def neg_cycle(n, edges):
    dist = [0] * n
    for _ in range(n):
        upd = False
        for u, v, w in edges:
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                upd = True
        if not upd:
            return False
    return True

if __name__ == "__main__":
    rng = random.Random(11)
    R = {"pass": [], "fail": []}
    # valid small graphs: refinement must stabilize + forward/reverse/cycle-reflection hold
    for trial in range(120):
        n = rng.randint(2, 10)
        edges = []
        for _ in range(rng.randint(1, 3 * n)):
            edges.append((rng.randrange(n), rng.randrange(n), rng.randint(-2, 4)))
        init = [rng.randint(0, 2) for _ in range(n)]
        part, rounds, stable = refine(n, edges, init, max_rounds=64)
        if not stable:
            R["fail"].append(("no-stable", trial))
            continue
        if not check_stable(n, edges, part):
            R["fail"].append(("unstable", trial))
            continue
        if not check_reverse(n, edges, part):
            R["fail"].append(("no-reverse", trial))
            continue
        # reflection: quotient negative cycle <=> detailed negative cycle (build quotient, compare)
        from collections import defaultdict
        qe = {}
        for u, v, w in edges:
            key = (part[u], part[v])
            qe[key] = min(qe.get(key, float('inf')), w)
        blocks = sorted(set(part))
        bi = {b: i for i, b in enumerate(blocks)}
        qedges = [(bi[b], bi[c], w) for (b, c), w in qe.items()]
        if neg_cycle(n, edges) != neg_cycle(len(blocks), qedges):
            R["fail"].append(("reflection", trial))
            continue
        R["pass"].append(trial)
    # invalid partitions must be REJECTED (stability or reverse fails)
    rej = 0
    for trial in range(60):
        n = rng.randint(2, 8)
        edges = []
        for _ in range(rng.randint(2, 2 * n)):
            edges.append((rng.randrange(n), rng.randrange(n), rng.randint(-2, 4)))
        # deliberately coarse invalid partition: all in one block (usually unstable/non-uniform)
        part = [0] * n
        if not check_stable(n, edges, part) or not check_reverse(n, edges, part):
            rej += 1
    print("valid=%d/120 invalid-rejected-or-trivial=%d/60" % (len(R["pass"]), rej), flush=True)
    # note: all-in-one may occasionally BE stable (then it's valid, not a rejection case); report only
    json.dump({"valid_pass": len(R["pass"]), "invalid_rej": rej, "fail": R["fail"][:5]},
              open(PDIR + "WQ_REFINEMENT_TEST.json", "w"), indent=1)
    sys.exit(0 if not R["fail"] else 1)
