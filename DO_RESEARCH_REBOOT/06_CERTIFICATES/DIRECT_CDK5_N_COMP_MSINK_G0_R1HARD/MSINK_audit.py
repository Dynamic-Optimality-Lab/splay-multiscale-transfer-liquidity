# MSINK finalist audit: pointer replay + full worksheet (AS, splits, msink re-check).
import sys, copy, json
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD')
from pathlib import Path
from wp6_eventflow import to_ptr, splay_A, splay_B_push
import splay as S
import MSINK_bounded_search as B

T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]],
          [8, [7, None, None], None]], None]

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

def audit(word):
    A = to_ptr(copy.deepcopy(T0)); Bp = to_ptr(copy.deepcopy(T0))
    IA = B.totup(copy.deepcopy(T0)); IB = B.totup(copy.deepcopy(T0))
    S0 = (pserial(A), pserial(Bp))
    legs, snaps, pairs = [], {}, [S0]
    agree = True
    for i, (md, x) in enumerate(word):
        dA = pdepths(A).get(x, -1); assert dA >= 0
        a = (dA + 1) // 2
        ra, rb = proot(A), proot(Bp)
        sb = pserial(Bp)
        if md == 'K':
            dB = pdepths(Bp).get(x, -1); assert dB >= 0
            q = dB // 2
        else:
            dB = None; q = 0
        eA = B.dep(IA).get(x)
        eB = B.dep(IB).get(x) if md == 'K' else None
        A, _ = splay_A(A, x)
        push = []
        if md == 'K':
            Bp, outB = splay_B_push(Bp, x)
            for s in outB:
                push += list(s)
        IA = S.trace(IA, x)[0]
        if md == 'K':
            IB = S.trace(IB, x)[0]
        chg = (pserial(Bp) != sb) if md == 'K' else False
        agree = agree and (dA, dB) == (eA, eB) and pserial(A) == B.ser(IA) \
            and pserial(Bp) == B.ser(IB)
        snaps[i] = pdepths(Bp)
        pairs.append((pserial(A), pserial(Bp)))
        legs.append({"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                     "delta": q - 2 * a, "ra": ra, "rb": rb, "chg": chg,
                     "push": sorted(set(push))})
    S1 = pairs[-1]
    lb = B.perleg_blocks(legs)
    mb = B.merged_blocks(legs)
    u = B.union_exec(lb, mb)
    rAS = B.ASm.recognize(mb, snaps)
    u["AS"] = bool(rAS.get("accepted", False))
    iv = B.intervals_of(legs)
    # msink with fail-stage tracing
    stages = {}
    s = len(iv)
    E = [j for j in range(s) if iv[j]["c"] == 1 and iv[j]["q"] == 3 and iv[j]["H"] == 1]
    stages["E"] = E
    ms = B.msink(iv, legs)
    pos = [{"gi": v["gi"], "x": v["x"], "H": v["H"], "c": v["c"],
            "q": v["q"], "w": v["w"], "R": v["R"]} for v in iv if v["w"] > 0]
    gk = sorted({l["x"] for l in legs if l["m"] == "K" and l["chg"]})
    cores = []
    for ps in pairs:
        c = B.core(ps[1], B.MSET)
        cores.append(None if c is None else len(c))
    out = {"n": len(word), "closed": S1 == S0, "engines_agree": agree,
           "tot": B.totals_of(legs), "gkeys": gk, "cores": cores,
           "union": u, "msink": ms, "E": E, "positives": pos,
           "np": B.np_covered(iv, legs),
           "splits": [i for i in range(1, len(word)) if pairs[i] == S0],
           "iv": [(v["x"], v["H"], v["c"], v["q"], v["w"], v["R"]) for v in iv]}
    return out

if __name__ == "__main__":
    sha_want = sys.argv[1]
    rows = []
    for seed in ("concat35", "mr33"):
        f = B.RDIR / ("state_" + seed) / "survivors.jsonl"
        if f.exists():
            rows += [json.loads(l) for l in open(f)]
    hit = [r for r in rows if r["sha"].startswith(sha_want)]
    assert len(hit) == 1, len(hit)
    word = B.parse(hit[0]["canon"])
    out = audit(word)
    out["meta"] = hit[0]["meta"]
    out["sha"] = hit[0]["sha"]
    fn = B.RDIR / ("MSINK_audit_" + hit[0]["sha"][:12] + ".json")
    json.dump(out, open(fn, "w"), indent=1, default=str)
    print("audit %s: closed=%s engines=%s union=%s msink=%s splits=%s gkeys=%s cores9=%s" % (
        hit[0]["sha"][:12], out["closed"], out["engines_agree"], out["union"],
        out["msink"] is not None, out["splits"], out["gkeys"],
        all(c == 9 for c in out["cores"])), flush=True)
    print("wrote", fn, flush=True)
