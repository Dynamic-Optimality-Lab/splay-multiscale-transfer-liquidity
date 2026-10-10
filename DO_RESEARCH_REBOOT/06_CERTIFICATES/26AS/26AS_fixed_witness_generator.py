"""26AS bounded witness hunt: PRECOMMITTED manifest + deterministic generator.

Seeds: banked 26AQ / 26AR vine-16 constructions (prefix + cycle). Family:
head = first 6 KEEPs of seed cycle; tail = rest. Mutations: (a) substitute
<=1 head KEEP key; (b) insert <=2 KEEPs at slots 0..6. Budget <= 40000.
Screen staged cheap-first; qualifiers need full 15-gate pass + engines."""
import sys, copy, json, itertools
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AS')
from wp6_eventflow import to_ptr, splay_A, splay_B_push
import splay as S
import legacy_embedding as PE

def vine_right(n):
    t = None
    for k in range(n, 0, -1):
        t = [k, None, t]
    return t
T0 = vine_right(16)

SEEDS = {
    "26AQ": {"prefix": [('D', 9), ('D', 8), ('D', 6), ('D', 6), ('D', 11),
                        ('D', 9), ('D', 16), ('D', 16), ('D', 5)],
             "cycle": None},  # filled below
    "26AR": {"prefix": [('K', 3), ('K', 6), ('K', 15), ('K', 9), ('K', 1),
                        ('K', 14), ('K', 13), ('K', 16), ('D', 3), ('D', 11),
                        ('D', 4), ('D', 13), ('D', 3), ('D', 15), ('D', 4),
                        ('D', 7)],
             "cycle": None},
}
AQ_CYCLE = [('K', 11), ('K', 9), ('K', 16), ('K', 1), ('K', 16), ('K', 15),
            ('K', 14), ('K', 13), ('K', 12), ('K', 11), ('K', 10), ('K', 9),
            ('K', 8), ('K', 7), ('K', 6), ('K', 5), ('K', 4), ('K', 3),
            ('K', 2), ('K', 1), ('D', 9), ('D', 8), ('D', 6), ('D', 6),
            ('D', 11), ('D', 9), ('D', 16), ('D', 16), ('D', 5)]
AR_CYCLE = [('K', 11), ('K', 4), ('K', 7), ('K', 16), ('K', 4), ('K', 16),
            ('K', 15), ('K', 14), ('K', 13), ('K', 12), ('K', 11), ('K', 10),
            ('K', 9), ('K', 8), ('K', 7), ('K', 6), ('K', 5), ('K', 4),
            ('K', 3), ('K', 2), ('K', 1), ('K', 3), ('K', 6), ('K', 15),
            ('K', 9), ('K', 1), ('K', 14), ('K', 13), ('K', 16), ('D', 3),
            ('D', 11), ('D', 4), ('D', 13), ('D', 3), ('D', 15), ('D', 4),
            ('D', 7)]
SEEDS["26AQ"]["cycle"] = AQ_CYCLE
SEEDS["26AR"]["cycle"] = AR_CYCLE
KEYS = list(range(1, 17))

MANIFEST = {"seeds": ["26AQ", "26AR"], "head_len": 6, "slots": [0, 1, 2, 3, 4, 5, 6],
            "max_insertions": 2, "max_substitutions": 1, "max_keys": 16,
            "budget_cap": 40000,
            "counts_per_seed": {"substitutions": 6 * 15, "insert1": 7 * 16,
                                "insert2": 28 * 16 * 16, "base": 1},
            "note": "insert2 slot pairs ordered i<=j; deterministic key order"}
MANIFEST["total"] = 2 * (90 + 112 + 28 * 256 + 1)
assert MANIFEST["total"] <= 40000, MANIFEST["total"]
(RDIR / '26AS_search_manifest.json').write_text(json.dumps(MANIFEST, indent=1))
print("manifest written; total candidates:", MANIFEST["total"], flush=True)

def pdepths(t):
    out = {}
    def go(nd, d):
        if nd is None:
            return
        out[nd["k"]] = d
        go(nd["l"], d + 1); go(nd["r"], d + 1)
    while t["p"] is not None:
        t = t["p"]
    go(t, 0)
    return out
def pserial(t):
    while t["p"] is not None:
        t = t["p"]
    def go(nd):
        if nd is None:
            return '.'
        return (nd["k"], go(nd["l"]), go(nd["r"]))
    return go(t)
def proot(t):
    while t["p"] is not None:
        t = t["p"]
    return t["k"]

def gen_heads(head0):
    yield ("base", list(head0))
    for i in range(6):
        for k in KEYS:
            if k == head0[i][1]:
                continue
            h = list(head0); h[i] = ('K', k)
            yield ("sub-%d-%d" % (i, k), h)
    for i in range(7):
        for k in KEYS:
            h = list(head0); h.insert(i, ('K', k))
            yield ("ins1-%d-%d" % (i, k), h)
    for i in range(7):
        for j in range(i, 7):
            for k1 in KEYS:
                for k2 in KEYS:
                    h = list(head0)
                    h.insert(i, ('K', k1))
                    h.insert(j + 1, ('K', k2))
                    yield ("ins2-%d-%d-%d-%d" % (i, j, k1, k2), h)

def replay(A0, B0, word, gi0=0):
    A = to_ptr(copy.deepcopy(A0)); B = to_ptr(copy.deepcopy(B0))
    legs, snaps = [], {}
    gi = gi0
    for (md, x) in word:
        dA = pdepths(A).get(x, -1)
        if dA < 0:
            return None
        a = (dA + 1) // 2
        ra, rb = proot(A), proot(B)
        if md == 'K':
            dB = pdepths(B).get(x, -1)
            if dB < 0:
                return None
            q = dB // 2
        else:
            dB = None; q = 0
        A, _ = splay_A(A, x)
        push = []
        if md == 'K':
            B, outB = splay_B_push(B, x)
            for s in outB:
                push += list(s)
        legs.append({"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                     "delta": q - 2 * a, "ra": ra, "rb": rb,
                     "bchanged": None, "push": sorted(set(push)), "gi": gi})
        snaps[gi] = pdepths(B)
        gi += 1
    return legs, snaps, A, B

# cache seed prefix-end states + cycle-start serials
SEEDSTATE = {}
for name, sd in SEEDS.items():
    A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
    r = replay(T0, T0, sd["prefix"])
    legs, snaps, A, B = r
    SEEDSTATE[name] = {"A0": A, "B0": B, "S0": (pserial(A), pserial(B)),
                       "npre": len(sd["prefix"])}

def build_blocks(legs):
    blocks, leading = [], []
    for lg in legs:
        if lg["a"] >= 1:
            blocks.append({"leader": lg["x"], "legs": [lg]})
        else:
            if not blocks:
                leading.append(lg)  # cyclically belongs to last block
                continue
            if lg["x"] != blocks[-1]["leader"]:
                return None
            blocks[-1]["legs"].append(lg)
    if leading:
        if not blocks:
            return None
        for lg in leading:
            if lg["x"] != blocks[-1]["leader"]:
                return None  # model violation given closure; reject walk
            blocks[-1]["legs"].append(lg)
    out = []
    for b in blocks:
        L = b["legs"][0]
        a = sum(l["a"] for l in b["legs"]); q = sum(l["q"] for l in b["legs"])
        push = set()
        for l in b["legs"]:
            push |= set(l["push"])
        out.append({"key": L["x"], "keys": sorted({l["x"] for l in b["legs"]}),
                    "a": a, "q": q, "delta": q - 2 * a,
                    "genuine": any(pserial_check(l) for l in b["legs"]),
                    "dB": L["dB"], "rb": L["rb"],
                    "keeps": sorted({l["x"] for l in b["legs"] if l["m"] == "K"}),
                    "dA": L["dA"], "push": sorted(push),
                    "l0": b["legs"][0]["gi"], "l1": b["legs"][-1]["gi"] + 1,
                    "nleg": len(b["legs"])})
    return out

def pserial_check(lg):
    return lg.get("_chg", False)

CLOSED = [0]

def screen_candidate(name, tag, head, tail, S0, npre):
    st = SEEDSTATE[name]
    A = copy.deepcopy(st["A0"]); B = copy.deepcopy(st["B0"])
    r1 = replay_pair(A, B, head, npre)
    if r1 is None:
        return None
    legs1, snaps1, A, B = r1
    r2 = replay_pair(A, B, tail, npre + len(head))
    if r2 is None:
        return None
    legs2, snaps2, A, B = r2
    if (pserial(A), pserial(B)) != S0:
        return None
    CLOSED[0] += 1
    legs = legs1 + legs2
    snaps = dict(snaps1); snaps.update(snaps2)
    # genuine flags via serial compare per KEEP
    words = head + tail
    Btmp = copy.deepcopy(st["B0"])
    for lg, (md, x) in zip(legs, words):
        if md == 'K':
            sb = pserial(Btmp)
            Btmp, _ = splay_B_push(Btmp, x)
            lg["_chg"] = (pserial(Btmp) != sb)
        else:
            lg["_chg"] = False
    blocks = build_blocks(legs)
    if blocks is None:
        return None
    m = len(blocks)
    pos = [i for i, b in enumerate(blocks) if b["delta"] > 0]
    if not pos:
        return None
    # structural screen: every positive belongs to one of exactly two maximal +1 runs
    runs = []
    i = 0
    while i < m:
        if blocks[i]["delta"] == 1:
            j = i
            while j < m and blocks[j]["delta"] == 1:
                j += 1
            runs.append((i, j - 1))
            i = j
        else:
            if blocks[i]["delta"] > 1:
                return None
            i += 1
    if len(runs) != 2:
        return None
    if any(blocks[i]["delta"] != 1 for (a, b) in runs for i in range(a, b + 1)):
        return None
    (a1, b1), (a2, b2) = runs
    mr, ms = b1 - a1 + 1, b2 - a2 + 1
    # cyclic order: run1, sepA>=1, run2, sepB>=1, R, S, rest(nonpos)
    # try both run orders (cyclic rotations of assignment)
    for (R1, S1) in [((a1, b1), (a2, b2)), ((a2, b2), (a1, b1))]:
        res = try_layout(blocks, snaps, m, R1, S1)
        if res is not None:
            res.update({"seed": name, "tag": tag, "runs": runs,
                        "head": head, "tail": tail, "npre": npre})
            return res
    return None

def replay_pair(A, B, word, gi0):
    legs, snaps = [], {}
    gi = gi0
    for (md, x) in word:
        dA = pdepths(A).get(x, -1)
        if dA < 0:
            return None
        a = (dA + 1) // 2
        ra, rb = proot(A), proot(B)
        if md == 'K':
            dB = pdepths(B).get(x, -1)
            if dB < 0:
                return None
            q = dB // 2
        else:
            dB = None; q = 0
        A, _ = splay_A(A, x)
        push = []
        if md == 'K':
            B, outB = splay_B_push(B, x)
            for s in outB:
                push += list(s)
        legs.append({"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                     "delta": q - 2 * a, "ra": ra, "rb": rb,
                     "push": sorted(set(push)), "gi": gi})
        snaps[gi] = pdepths(B)
        gi += 1
    return legs, snaps, A, B

def try_layout(blocks, snaps, m, R1, S1):
    (a1, b1), (a2, b2) = R1, S1
    mr, ms = b1 - a1 + 1, b2 - a2 + 1
    # cyclic successor helper
    def nxt(i):
        return (i + 1) % m
    # sepA: from b1+1 to a2-1 cyclic, >=1 block, all nonpositive
    sepA = []
    i = nxt(b1)
    while i != a2:
        if blocks[i]["delta"] > 0:
            return None
        sepA.append(i); i = nxt(i)
    if not sepA:
        return None
    # sepB: from b2+1 while nonpositive and not R-pattern; then R,S consecutive
    r = blocks[a1]["rb"]; s = blocks[a2]["rb"]
    if r == s:
        return None
    sepB = []
    i = nxt(b2)
    while True:
        if blocks[i]["delta"] > 0:
            return None
        if blocks[i]["key"] == r and r in blocks[i]["keeps"]:
            break
        sepB.append(i); i = nxt(i)
        if len(sepB) > m:
            return None
    if not sepB:
        return None
    Ro, So = i, nxt(i)
    R, Sb = blocks[Ro], blocks[So]
    if R["delta"] > 0 or Sb["delta"] > 0:
        return None
    if not (R["key"] == r and r in R["keeps"]):
        return None
    if not (Sb["key"] == s and s in Sb["keeps"]):
        return None
    if s in R["keeps"] or r in Sb["keeps"]:
        return None
    # rest after S back to a1: all nonpositive
    rest = []
    i = nxt(So)
    while i != a1:
        if blocks[i]["delta"] > 0:
            return None
        rest.append(i); i = nxt(i)
    # lifetimes
    for o in list(range(a1 + 1, b1 + 1)) + sepA + list(range(a2, b2 + 1)) + sepB:
        oo = o % m
        if r in blocks[oo]["keeps"]:
            return None
    for o in list(range(a2 + 1, b2 + 1)) + sepB:
        oo = o % m
        if s in blocks[oo]["keeps"]:
            return None
    # W candidates in sepB
    for Wo in sepB:
        W = blocks[Wo]
        if not (W["genuine"] and W["dB"] is not None and 1 <= W["dB"] <= 3
                and W["a"] >= 1 and min(r, s) < W["key"] < max(r, s)):
            continue
        if not (r in W["push"] and s in W["push"]):
            continue
        t0acc = blocks[b2 % m]["l1"] - 1
        snap = snaps.get(t0acc)
        if snap is None or r not in snap or s not in snap:
            continue
        dr0, ds0 = snap[r], snap[s]
        h = sum(1 for o in sepB if blocks[o]["genuine"])
        g = sum(1 for o in sepB if blocks[o]["genuine"]
                and min(r, s) < blocks[o]["key"] < max(r, s))
        eps = 1 if (dr0 % 2 == 1 and ds0 % 2 == 1) else 0
        kap = g - eps
        if kap < 1:
            continue
        Ur = (dr0 + 2 * h) // 2
        Us = (ds0 + 2 * h + 2) // 2
        Urs = (dr0 + ds0 + 4 * h - 2 * g + 2) // 2
        if Ur + Us - Urs != kap:
            return None
        Tr = max(1, -(-(Ur + mr - 1) // 2))
        Ts = max(1, -(-(Us + ms - 1) // 2))
        if not (R["dA"] >= 2 * Tr - 1 and Sb["dA"] >= 2 * Ts - 1):
            continue
        CR, CS = 2 * R["a"] - R["q"], 2 * Sb["a"] - Sb["q"]
        CW = 2 * W["a"] - W["q"]
        if CW != 1:
            continue
        if not (CR >= mr - 1 and CS >= ms - 1):
            continue
        if not (CR + CW >= mr and CS + CW >= ms and CR + CW + CS >= mr + ms):
            continue
        cR, cS = 2 * R["a"] - Ur, 2 * Sb["a"] - Us
        if not (cR + cS + 1 < mr + ms and cR + cS + kap + 1 >= mr + ms):
            continue
        return {"layout": "AS", "r": r, "s": s, "mr": mr, "ms": ms, "W": Wo,
                "R": Ro, "S": So, "run1": [a1, b1], "run2": [a2, b2],
                "h": h, "g": g, "kap": kap, "CW": CW, "CR": CR, "CS": CS,
                "cR": cR, "cS": cS}
    return None

if __name__ == "__main__":
    stat = {"tested": 0, "closed": 0, "qualifiers": []}
    LOG = open(RDIR / '26AS_bounded_search_log.json', 'w')
    for name, sd in SEEDS.items():
        head0 = sd["cycle"][:6]
        tail = sd["cycle"][6:]
        S0 = SEEDSTATE[name]["S0"]
        npre = SEEDSTATE[name]["npre"]
        for tag, head in gen_heads(head0):
            stat["tested"] += 1
            res = screen_candidate(name, tag, head, tail, S0, npre)
            if isinstance(res, dict):
                stat["qualifiers"].append(res)
                LOG.write(json.dumps(res) + "\n"); LOG.flush()
                print("QUALIFIER:", name, tag, {k: res[k] for k in (
                    "r", "s", "mr", "ms", "h", "g", "kap", "CW")}, flush=True)
    stat["closed"] = CLOSED[0]
    LOG.close()
    json.dump(stat, open(RDIR / '26AS_bounded_search_summary.json', 'w'), indent=1)
    print("tested=%d qualifiers=%d" % (stat["tested"], len(stat["qualifiers"])), flush=True)
