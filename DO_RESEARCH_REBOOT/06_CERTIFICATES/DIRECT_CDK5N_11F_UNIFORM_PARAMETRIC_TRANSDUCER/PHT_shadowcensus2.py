# Joint symbolic variety census v2: proper S9 handling + multimask sample + fringe.
import sys, json, gzip, random, ast
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL')
sys.path.insert(0, 'python/independent')
from CRA_pointer_tuple_replay import replay, core_of, from_serial
from AFSP_canonical import canonical_shadow
import splay as S

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_UNIFORM_PARAMETRIC_TRANSDUCER/'

def canon_tree(A, S9):
    Ss = sorted(S9)
    rk = {k: i + 1 for i, k in enumerate(Ss)}
    order = []
    def ino(t):
        if t[0] == 'leaf':
            return
        _, k, l, r = t
        ino(l)
        if k not in S9:
            order.append(k)
        ino(r)
    ino(A)
    beta = {k: 1000 + i for i, k in enumerate(order)}
    def rel(t):
        if t[0] == 'leaf':
            return t
        _, k, l, r = t
        kk = rk[k] if k in S9 else beta[k]
        return S.node(kk, rel(l), rel(r))
    A2 = rel(A)
    return canonical_shadow(A2, set(range(1, 10)))

def parse_serial_str(s):
    ps = ast.literal_eval(s)
    return from_serial(ps)

if __name__ == "__main__":
    SH = set()
    nb = 0
    # 1) multimask sample (9-key, all masks)
    f = gzip.open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_UFRL_TERMINAL_CLOSURE/UFRL_MM_STATES.json.gz', 'rt')
    d = json.load(f)
    states = d['states']
    random.seed(4)
    idx = random.sample(range(len(states)), min(20000, len(states)))
    S9 = set(range(1, 10))
    for i in idx:
        mi, sa, sb = states[i]
        try:
            A = parse_serial_str(sa)
            B = parse_serial_str(sb)
            shA = canon_tree(A, S9)
            shB = canon_tree(B, S9)
            SH.add((tuple(sorted(d['masks'][mi])), shA["vis"], shA["holes"], shB["vis"], shB["holes"]))
            nb += 1
        except Exception:
            continue
    print("multimask sample: boundaries=%d distinct=%d" % (nb, len(SH)), flush=True)
    # 2) fringe universes with explicit S9 = M5 + 4 extra
    nadd = 0
    for trial in range(500):
        n = random.randint(10, 24)
        keys = list(range(1, n + 1))
        M5 = random.sample(keys, 5)
        rest = [k for k in keys if k not in M5]
        S9x = set(M5) | set(random.sample(rest, 4))
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
        Sall = list(S9x) + random.sample([k for k in keys if k not in S9x], min(3, n - 9))
        word = [("K" if random.random() < 0.5 else "D", random.choice(Sall)) for _ in range(random.randint(6, 24))]
        try:
            R = replay(word, A0=T, B0=T)
        except Exception:
            continue
        if not (R["S1"] == R["S0"] and R["agree"]):
            continue
        Mchg = {l["x"] for l in R["legs"] if l["m"] == "K" and l["chg"]}
        if len(Mchg) != 5 or not Mchg <= S9x:
            continue
        for k, l in enumerate(R["legs"]):
            if l["m"] != "K":
                continue
            A = from_serial(R["pairs"][k + 1][0])
            B = from_serial(R["pairs"][k + 1][1])
            rk = {kk: i + 1 for i, kk in enumerate(sorted(S9x))}
            mask = tuple(sorted(rk[kk] for kk in Mchg))
            try:
                shA = canon_tree(A, S9x)
                shB = canon_tree(B, S9x)
            except Exception:
                continue
            SH.add((mask, shA["vis"], shA["holes"], shB["vis"], shB["holes"]))
            nadd += 1
    nb += nadd
    print("total: boundaries~%d distinct joint=%d" % (nb, len(SH)), flush=True)
    json.dump({"boundaries": nb, "distinct_joint": len(SH)}, open(PDIR + "PHT_SHADOW_CENSUS2.json", "w"), indent=1)
