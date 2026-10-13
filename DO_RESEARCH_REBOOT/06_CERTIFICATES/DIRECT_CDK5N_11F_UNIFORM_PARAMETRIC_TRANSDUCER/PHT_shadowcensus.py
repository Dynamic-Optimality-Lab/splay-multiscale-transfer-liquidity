# Symbolic variety census: canonicalize concrete post-KEEP boundaries (corpus + validation fringe) to shadows.
import sys, json, random
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'python/independent')
from CRA_pointer_tuple_replay import replay, core_of, from_serial
from CRA_segment_memberships import genuine_keys
from AFSP_canonical import canonical_shadow
import splay as S

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_UNIFORM_PARAMETRIC_TRANSDUCER/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]

def rank_canon(A, Sset):
    # map S ranks to 1..9 by order; fringe anonymous by inorder; return canonical shadow key
    Ss = sorted(Sset)
    rk = {k: i + 1 for i, k in enumerate(Ss)}
    # relabel tree: S->rank, fringe->order-preserving anonymous symbols F1.. (need concrete distinct labels for canonicalizer)
    # canonicalizer takes (tree, Sset): relabel S keys to ranks, fringe keys to 1000+i by inorder (canonical)
    order = []
    def ino(t):
        if t[0] == 'leaf':
            return
        _, k, l, r = t
        ino(l)
        if k not in Sset:
            order.append(k)
        ino(r)
    ino(A)
    beta = {k: 1000 + i for i, k in enumerate(order)}
    def rel(t):
        if t[0] == 'leaf':
            return t
        _, k, l, r = t
        kk = rk[k] if k in Sset else beta[k]
        return S.node(kk, rel(l), rel(r))
    A2 = rel(A)
    S2 = set(range(1, 10))
    return canonical_shadow(A2, S2)

if __name__ == "__main__":
    SH = set()
    nb = 0
    # corpus words (9-key) + validation-scale fringe universes
    RDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD/'
    rows = []
    for seed in ("concat35", "mr33"):
        for l in open(RDIR + "state_" + seed + "/survivors.jsonl"):
            rows.append(json.loads(l))
    bycanon = {}
    for r in rows:
        bycanon.setdefault(r["canon"], []).append(r)
    WORDS = sorted(bycanon)[:150]
    WORDS.append("D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
    for cw in WORDS:
        w = parse(cw)
        try:
            R = replay(w)
        except Exception:
            continue
        if not (R["S1"] == R["S0"] and R["agree"]):
            continue
        for k, l in enumerate(R["legs"]):
            if l["m"] != "K":
                continue
            A = from_serial(R["pairs"][k + 1][0])
            Sset = core_of(R["pairs"][k + 1][1])
            if Sset is None or len(Sset) != 9:
                continue
            M = tuple(sorted({ll["x"] for ll in R["legs"] if ll["m"] == "K" and ll["chg"]}))
            if len(M) != 5:
                continue
            rk = {kk: i + 1 for i, kk in enumerate(sorted(Sset))}
            mask = tuple(sorted(rk[kk] for kk in M))
            try:
                sh = rank_canon(A, set(Sset))
            except Exception:
                continue
            SH.add((mask, sh["vis"], sh["holes"]))
            nb += 1
    # fringe universes: random n=10..20 words, closed ones only
    random.seed(9)
    for trial in range(300):
        n = random.randint(10, 20)
        keys = list(range(1, n + 1))
        t = S.LEAF
        ks = sorted(keys)
        random.shuffle(ks)
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
        marked = random.sample(keys, 5)
        word = [("K" if random.random() < 0.5 else "D", random.choice(marked if random.random() < 0.6 else keys)) for _ in range(random.randint(6, 24))]
        try:
            R = replay(word, A0=T, B0=T)
        except Exception:
            continue
        if not (R["S1"] == R["S0"] and R["agree"]):
            continue
        M = {l["x"] for l in R["legs"] if l["m"] == "K" and l["chg"]}
        if len(M) != 5:
            continue
        for k, l in enumerate(R["legs"]):
            if l["m"] != "K":
                continue
            A = from_serial(R["pairs"][k + 1][0])
            Sset = core_of(R["pairs"][k + 1][1])
            if Sset is None or len(Sset) != 9:
                continue
            if not M <= set(Sset):
                continue
            rk = {kk: i + 1 for i, kk in enumerate(sorted(Sset))}
            mask = tuple(sorted(rk[kk] for kk in M))
            try:
                sh = rank_canon(A, set(Sset))
            except Exception:
                continue
            SH.add((mask, sh["vis"], sh["holes"]))
            nb += 1
    print("boundaries=%d distinct (mask,shadow)=%d" % (nb, len(SH)), flush=True)
    json.dump({"boundaries": nb, "distinct": len(SH)}, open(PDIR + "PHT_SHADOW_CENSUS.json", "w"), indent=1)
