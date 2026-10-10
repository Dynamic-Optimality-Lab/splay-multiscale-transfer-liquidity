"""26AS Test A: exhaustive L1 falsification (all shapes n<=7, all r<y<s).

L1: d_{S_y(B)}(r)+d_{S_y(B)}(s) <= d_B(r)+d_B(s)+2. Both engines; extremals kept.
"""
import sys, copy, json, itertools
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python')
sys.path.insert(0, 'python/independent')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AS')
RDIR.mkdir(parents=True, exist_ok=True)
from wp6_eventflow import to_ptr, splay_B_push
import splay as S
import wp6_cycle_ratio as O

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
def to_tup(t):
    if t is None:
        return S.LEAF
    return S.node(t[0], to_tup(t[1]), to_tup(t[2]))
def idepths(t):
    out = {}
    def go(nd, d):
        if nd[0] == "leaf":
            return
        _, k, l, r = nd
        out[k] = d; go(l, d + 1); go(r, d + 1)
    go(t, 0)
    return out

CACHE = {}
def shapes(n):
    if n not in CACHE:
        CACHE[n] = O.shapes_of(list(range(1, n + 1)))
    return CACHE[n]

worst = -10**9
worst_cases = []
count = 0
violations = []
eng_mismatch = 0
for n in range(1, 8):
    for T0 in shapes(n):
        keys = list(range(1, n + 1))
        for y in keys:
            others = [k for k in keys if k != y]
            for r, s in itertools.combinations(others, 2):
                if not (r < y < s):
                    continue
                count += 1
                # ptr engine
                B = to_ptr(copy.deepcopy(T0))
                d0 = pdepths(B)
                B2, _ = splay_B_push(B, y)
                d1 = pdepths(B2)
                g_ptr = (d1[r] + d1[s]) - (d0[r] + d0[s])
                # tuple engine
                T = to_tup(copy.deepcopy(T0))
                e0 = idepths(T)
                T2, _ = S.trace(T, y)
                e1 = idepths(T2)
                g_tup = (e1[r] + e1[s]) - (e0[r] + e0[s])
                if g_ptr != g_tup:
                    eng_mismatch += 1
                    if eng_mismatch <= 3:
                        print("ENGINE MISMATCH n=%d y=%d r=%d s=%d: %d vs %d" % (
                            n, y, r, s, g_ptr, g_tup))
                g = g_ptr
                if g > worst:
                    worst = g
                    worst_cases = [(n, y, r, s)]
                elif g == worst and len(worst_cases) < 5:
                    worst_cases.append((n, y, r, s))
                if g > 2:
                    violations.append({"n": n, "y": y, "r": r, "s": s,
                                       "gain": g})
                    if len(violations) <= 5:
                        print("VIOLATION: n=%d y=%d r=%d s=%d gain=%d" % (
                            n, y, r, s, g))
print("triples tested:", count)
print("engine mismatches:", eng_mismatch)
print("max pair-gain:", worst)
print("extremals:", worst_cases)
print("violations of +2:", len(violations))
json.dump({"triples": count, "mismatches": eng_mismatch, "worst": worst,
           "extremals": worst_cases, "n_violations": len(violations),
           "violations": violations[:20]},
          open(RDIR / '26AS_coupled_root_exhaustive.json', 'w'), indent=1)
