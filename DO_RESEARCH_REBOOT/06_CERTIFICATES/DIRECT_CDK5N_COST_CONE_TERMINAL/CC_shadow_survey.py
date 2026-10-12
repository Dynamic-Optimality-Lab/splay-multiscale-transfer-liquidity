# Rank-canonical A-shadow canonicalizer + corpus survey (prototype sizing).
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import replay, idepths, from_serial, core_of
from CRA_segment_memberships import genuine_keys

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COST_CONE_TERMINAL/'

def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]

def shadow_of(A_tree, S_sorted, M_set):
    # rank map S -> 1..9
    rk = {k: i + 1 for i, k in enumerate(S_sorted)}
    # BFS levels through depth 2; anonymous fringe by inorder
    # collect visible fringe nodes left-to-right for canonical naming
    nodes = {}  # (level, pos) -> ('S', rank) | ('F', key) | None
    fringe_keys = []
    def walk(t, lv, pos):
        if t == '.' or (isinstance(t, tuple) and t and t[0] == "leaf"):
            nodes[(lv, pos)] = None
            return
        _, k, l, r = t
        if lv <= 2:
            if k in rk:
                nodes[(lv, pos)] = ('S', rk[k])
            else:
                nodes[(lv, pos)] = ('F', k)
                fringe_keys.append(k)
            walk(l, lv + 1, pos * 2)
            walk(r, lv + 1, pos * 2 + 1)
        else:
            # opaque hole root: record S-subset + interval below in holes
            pass
    walk(A_tree, 0, 0)
    # canonical anonymous renaming by inorder appearance
    order = []
    def ino(t, lv):
        if t == '.' or (isinstance(t, tuple) and t and t[0] == "leaf"):
            return
        _, k, l, r = t
        ino(l, lv + 1)
        if lv <= 2 and k not in rk:
            order.append(k)
        ino(r, lv + 1)
    ino(A_tree, 0)
    beta = {k: 'b%d' % (i + 1) for i, k in enumerate(order)}
    # holes at depth 3: for each node at depth 2, its children
    holes = []
    def holewalk(t, lv, lo, hi):
        if t == '.' or (isinstance(t, tuple) and t and t[0] == "leaf"):
            if lv == 3:
                holes.append((frozenset(), lo, hi, True))
            return
        _, k, l, r = t
        if lv == 2:
            # children are hole roots (depth 3)
            for side, ch, (nlo, nhi) in (('L', l, (lo, k)), ('R', r, (k, hi))):
                sub = set()
                stack = [ch]
                while stack:
                    u = stack.pop()
                    if u == '.' or (isinstance(u, tuple) and u and u[0] == "leaf"):
                        continue
                    _, kk, ll, rr = u
                    if kk in rk:
                        sub.add(rk[kk])
                    stack.append(ll); stack.append(rr)
                holes.append((frozenset(sub), nlo, nhi, ch == '.' or (isinstance(ch, tuple) and ch and ch[0] == "leaf")))
            return
        holewalk(l, lv + 1, lo, k)
        holewalk(r, lv + 1, k, hi)
    holewalk(A_tree, 0, 0, 10)
    # inventory per S rank-gap (10 gaps over ranks 1..9)
    inv = [0] * 10
    d = idepths(A_tree)
    Sset = set(S_sorted)
    for k, dd in d.items():
        if k in Sset:
            continue
        # rank gap: number of S keys less than k
        g = sum(1 for s in S_sorted if s < k)
        inv[g] += 1
    # canonical visible tuple
    vis = tuple(sorted(nodes.items(), key=str))
    return {"vis": str([(str(k), v if v is None or v[0] == 'S' else ('F', beta[v[1]])) for k, v in nodes.items()]),
            "holes": str(sorted(holes, key=str)), "inv": tuple(inv),
            "mask": tuple(sorted(rk[k] for k in M_set))}

if __name__ == "__main__":
    WORDS = ["D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"]
    RDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD/'
    rows = []
    for seed in ("concat35", "mr33"):
        for l in open(RDIR + "state_" + seed + "/survivors.jsonl"):
            rows.append(json.loads(l))
    bycanon = {}
    for r in rows:
        bycanon.setdefault(r["canon"], []).append(r)
    for i, cs in enumerate(sorted(bycanon)):
        WORDS.append(cs)
        if i >= 120:
            break
    sh = set()
    nb = 0
    for cw in WORDS:
        w = parse(cw)
        try:
            R = replay(w)
        except Exception:
            continue
        if not (R["S1"] == R["S0"] and R["agree"]):
            continue
        M = set(sorted({l["x"] for l in R["legs"] if l["m"] == "K" and l["chg"]}))
        if len(M) != 5:
            continue
        for k, l in enumerate(R["legs"]):
            if l["m"] != "K":
                continue
            A = from_serial(R["pairs"][k + 1][0])
            Sset = sorted(core_of(R["pairs"][k + 1][1]))
            if len(Sset) != 9:
                continue
            s = shadow_of(A, Sset, M)
            sh.add((s["vis"], s["holes"], s["inv"], s["mask"]))
            nb += 1
    print("boundaries=%d distinct rank-canonical shadows=%d" % (nb, len(sh)), flush=True)
    masks = {}
    for v, h, i, m in sh:
        masks[m] = masks.get(m, 0) + 1
    print("masks seen:", masks, flush=True)
