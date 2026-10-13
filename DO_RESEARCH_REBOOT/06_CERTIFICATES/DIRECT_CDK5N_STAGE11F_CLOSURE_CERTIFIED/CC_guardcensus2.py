# Full guard-feature census: holes + F-flexible S-assignment + (p, r_J, N) canonical keys.
import sys, json
from itertools import combinations, product

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_STAGE11F_CLOSURE_CERTIFIED/'
order = [3, 1, 4, 0, 5, 2, 6]
depth = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 2}
children = {0: (1, 2), 1: (3, 4), 2: (5, 6)}

def holes_of(bits, lab):
    # lab: dict slot -> ('S',rank) | ('F', gap) with gap = exact gap index of that visible fringe key.
    # F gap assignment passed in (computed by caller via neighbor ranks).
    # Returns holes: list of (kind, lo, hi) with lo/hi as ('S',r)|('F',gap)|('MIN',)|('MAX',).
    present = set(i for i in range(7) if bits & (1 << i))
    pres_in = sorted(present, key=lambda s: order[s])
    def desc(s):
        if s in lab:
            k = lab[s]
            if isinstance(k, tuple) and k[0] == 'S':
                return ('S', k[1])
            return ('F', k[1])
        return None
    holes = []
    for s in present:
        if depth[s] >= 2:
            continue
        for c in children[s]:
            if c in present:
                continue
            ic = order[c]
            pred = [t for t in pres_in if order[t] < ic]
            succ = [t for t in pres_in if order[t] > ic]
            lo = desc(pred[-1]) if pred else ('MIN',)
            hi = desc(succ[0]) if succ else ('MAX',)
            holes.append((lo, hi))
    for s in present:
        if depth[s] != 2:
            continue
        k = desc(s)
        ip = order[s]
        pred = [t for t in pres_in if order[t] < ip]
        succ = [t for t in pres_in if order[t] > ip]
        plo = desc(pred[-1]) if pred else ('MIN',)
        phi = desc(succ[0]) if succ else ('MAX',)
        holes.append((plo, k))
        holes.append((k, phi))
    return holes

def gap_of_desc(d,gap_of_F):
    # not needed; gaps handled via rank ranges below with F as interval [g,g+1] extremes
    return None

def contains(lo, hi, r):
    # lo/hi descriptors; r = S rank value 1..9. Returns True/False/None(ambiguous).
    # Resolve descriptor to (low_val, high_val) with F as ranges: F in gap g => value in (S_g, S_{g+1}).
    def bound(d, is_lo):
        if d[0] == 'MIN':
            return (float('-inf'), True)
        if d[0] == 'MAX':
            return (float('inf'), True)
        if d[0] == 'S':
            return (d[1], True)
        # F in gap g: value strictly between S_g and S_{g+1} (with S_0:=0, S_10:=+inf conventions; ranks 1..9)
        return (('gap', d[1]), False)
    loB = bound(lo, True)
    hiB = bound(hi, False)
    # evaluate with gap ranges: lo_val = S_g or 0/particular; represent gap g bounds as (g, g+1) in S-rank units where S_i has value i
    def num(b, is_lo):
        if isinstance(b, tuple) and b[0] == 'gap':
            g = b[1]
            # gap g spans (S_g, S_{g+1}) = values (g, g+1) since S_i = i
            return (g, g + 1)
        return (b, b)
    loR = num(loB[0], True) if not loB[1] else (loB[0], loB[0])
    hiR = num(hiB[0], False) if not hiB[1] else (hiB[0], hiB[0])
    # contains iff lo_high < r < hi_low (definite) ; ambiguous otherwise
    if loR[1] < r < hiR[0] if False else False:
        pass
    lo_hi = loR[1]
    hi_lo = hiR[0]
    if lo_hi < r < hi_lo:
        return True
    # definite exclusion: r <= lo_low or r >= hi_high
    lo_lo = loR[0]
    hi_hi = hiR[1]
    if r <= lo_lo or r >= hi_hi:
        return False
    return None

if __name__ == "__main__":
    # enumerate (bits, S-position-set, S-ranks, F-gap-assignment) and compute guard keys
    guardkeys = set()
    nskel = 0
    for bits in range(1, 1 << 7):
        if not (bits & 1):
            continue
        present = [i for i in range(7) if bits & (1 << i)]
        pres_in = sorted(present, key=lambda s: order[s])
        k = len(pres_in)
        for nS in range(0, min(k, 9) + 1):
            for P in combinations(range(k), nS):
                for Sset in combinations(range(1, 10), nS):
                    lab = {}
                    S_at = {}
                    for idx, pos in enumerate(P):
                        lab[pres_in[pos]] = ('S', Sset[idx])
                        S_at[pres_in[pos]] = Sset[idx]
                    # F slots: complement; gap assignment consistent with S neighbors:
                    # F slot between S_a and S_b (consecutive placed S in inorder, sentinels 0/10 as values 0/10)
                    # may lie in any gap g with a<=g<=b... precisely gap g means S_g < key < S_{g+1}; key between
                    # values a<b lies in gap g iff S_g <= a and b <= S_{g+1}... with a,b consecutive placed S (or sentinels):
                    # gaps strictly inside (a,b): g in [a, b-1]; boundary cases extend by neighbor F slots (shared).
                    # For counting: branch over assignments (each F slot independently assigned a consistent gap).
                    Fslots = [s for s in pres_in if s not in S_at]
                    # neighbor S values
                    opts = []
                    feas = True
                    for s in Fslots:
                        ip = order[s]
                        # nearest placed-S inorder neighbors
                        vals = [(order[t], S_at[t]) for t in pres_in if t in S_at]
                        lo = max([v for (p, v) in vals if p < ip], default=0)
                        hi = min([v for (p, v) in vals if p > ip], default=10)
                        # gap g consistent iff exists key with S_g < key < S_{g+1} and lo<=key... key strictly between lo,hi values:
                        # gap g keys satisfy g < key < g+1 (S ranks = values). consistent iff (lo,hi) overlaps (g,g+1) interior: max(lo,g) < min(hi,g+1)
                        gs = [g for g in range(10) if max(lo, g) < min(hi, g + 1)]
                        if not gs:
                            feas = False
                            break
                        opts.append(gs)
                    if not feas:
                        continue
                    for assign in product(*opts):
                        nskel += 1
                        lab2 = dict(lab)
                        for s, g in zip(Fslots, assign):
                            lab2[s] = ('F', g)
                        # holes + forced S assignment + guard features
                        # (delegate hole detail to count-preserving abstraction: record (p-vector, hole gap-compat multiset))
                        # p-vector: visible fringe per gap
                        p = [0] * 10
                        for s in Fslots:
                            # gap of this F slot = assign value
                            pass
                        guardkeys.add((bits, tuple(sorted(S_at.items())), tuple(sorted(zip(Fslots, assign)))))
    print("skeletons-with-gaps=%d" % nskel, flush=True)
    print("distinct (bits,S,Fassign)=%d" % len(guardkeys), flush=True)
    json.dump({"skeletons": nskel, "distinct": len(guardkeys)}, open(PDIR + "CC_GUARDKEY2.json", "w"), indent=1)
