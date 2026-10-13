# 55-type verification: source-derived hole gap-sets are contiguous intervals; count distinct types.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'python/independent')
from CRA_pointer_tuple_replay import replay, from_serial, core_of
import splay as S

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_STAGE11F_CLOSURE_CERTIFIED/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]

def holes_of(A, Sset):
    # returns list of (frozenset(Ssub), lo_key_or_None, hi_key_or_None) for depth<=3 holes
    # lo/hi as raw bounds for overlap computation (canonicalized later)
    out = []
    Ss = sorted(Sset)
    def subkeys(t):
        if t[0] == 'leaf':
            return set()
        _, k, l, r = t
        s = ({k} if k in Sset else set()) | subkeys(l) | subkeys(r)
        return s
    def walk(t, lv, lo, hi):
        if t[0] == 'leaf':
            return
        _, k, l, r = t
        if lv == 2:
            for ch, (nlo, nhi) in ((l, (lo, k)), (r, (k, hi))):
                out.append((subkeys(ch), nlo, nhi, ch[0] == 'leaf'))
            return
        walk(l, lv + 1, lo, k)
        walk(r, lv + 1, k, hi)
    walk(A, 0, None, None)
    return out

def gapset(nlo, nhi, Ss):
    # gaps g (0..9) with interval (S_{g-1}, S_g) overlapping (nlo,nhi); None = unbounded
    G = set()
    for g in range(10):
        a = Ss[g - 1] if g > 0 else float('-inf')
        b = Ss[g] if g < 9 else float('inf')
        if max(nlo if nlo is not None else float('-inf'), a) < min(nhi if nhi is not None else float('inf'), b):
            G.add(g)
    return G

if __name__ == "__main__":
    RDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_MSINK_G0_R1HARD/'
    rows = []
    for seed in ("concat35", "mr33"):
        for l in open(RDIR + "state_" + seed + "/survivors.jsonl"):
            rows.append(json.loads(l))
    bycanon = {}
    for r in rows:
        bycanon.setdefault(r["canon"], []).append(r)
    types = set()
    nbad = tot = 0
    for cs in sorted(bycanon):
        w = parse(cs)
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
            Ss = sorted(Sset)
            for (sub, nlo, nhi, isempty) in holes_of(A, set(Sset)):
                G = gapset(nlo, nhi, Ss)
                tot += 1
                srt = sorted(G)
                if srt != list(range(min(srt), max(srt) + 1)) if srt else False:
                    nbad += 1
                    print("NONCONTIG", cs[:30], srt, flush=True)
                types.add(tuple(srt))
    print("holes=%d noncontiguous=%d distinct-types=%d (cap 55)" % (tot, nbad, len(types)), flush=True)
    json.dump({"holes": tot, "noncontiguous": nbad, "distinct_types": len(types),
               "pass": nbad == 0 and len(types) <= 55}, open(PDIR + "AFSP_HOLE_TYPES.json", "w"), indent=1)
    sys.exit(0 if (nbad == 0 and len(types) <= 55) else 1)
