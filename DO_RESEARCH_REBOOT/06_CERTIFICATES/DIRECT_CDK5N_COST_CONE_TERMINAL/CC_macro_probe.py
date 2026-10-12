# Macro-cost probe: completions-to-R(2) + effective words per observed shadow.
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'python/independent')
from CRA_pointer_tuple_replay import replay, idepths, from_serial, core_of
from CRA_segment_memberships import genuine_keys
import splay as S

def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]

def shapes(keys):
    if not keys:
        return [S.LEAF]
    out = []
    for i, k in enumerate(keys):
        for l in shapes(keys[:i]):
            for r in shapes(keys[i + 1:]):
                out.append(S.node(k, l, r))
    return out

# For one concrete boundary (A tree + S + M + u), count:
# (a) R-prefix completions are trivially 1 (concrete tree) — instead count EFFECTIVE words H<=2
# (b) effective nontrivial access patterns with total cost <=2
WORDS = ["D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"]
R = replay(parse(WORDS[0]))
legs = R["legs"]
# collect H<=2 intervals: effective patterns
from CRA_strict_msink_membership import intervals as miv
iv = miv(legs)
import collections
pats = collections.Counter()
for j, v in enumerate(iv):
    if v["H"] <= 2:
        acc = tuple((legs[k]["m"], legs[k]["x"], legs[k]["a"]) for k in v["segi"])
        pats[(v["H"], v["c"], v["q"], acc)] += 1
print("H<=2 interval patterns in SELR-OUT:", len(pats), flush=True)
for p, c in list(pats.items())[:12]:
    print("  H=%d c=%d q=%d %s (x%d)" % (p[0], p[1], p[2], p[3], c), flush=True)
# completions probe: take a deep-vine-ish A state, count BST completions of holes to depth 6
# worst case: single hole at depth 3 containing s S-keys + f fringe placeholders
import math
for s, f in ((3, 2), (5, 3), (7, 5)):
    n = s + f
    # Catalan-ish upper bound: number of BST shapes over n distinct keys = Catalan(n)
    from functools import lru_cache
    def cat(n):
        if n <= 1:
            return 1
        return sum(cat(i) * cat(n - 1 - i) for i in range(n))
    print("hole keys=%d shapes=%d" % (n, cat(n)), flush=True)
