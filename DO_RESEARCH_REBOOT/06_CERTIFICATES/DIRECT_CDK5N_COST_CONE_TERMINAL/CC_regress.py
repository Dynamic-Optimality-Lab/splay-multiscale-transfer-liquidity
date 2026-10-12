# Regressions A-F (§16) + abstract-correspondence coverage on random words.
import sys, json, random
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'python/independent')
from CRA_pointer_tuple_replay import replay, core_of
from CRA_segment_memberships import genuine_keys
from CRA_strict_msink_membership import intervals as miv
import splay as S

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COST_CONE_TERMINAL/'
R = []
ok = True
def check(name, cond, obs):
    global ok
    R.append({"check": name, "pass": bool(cond), "observed": obs})
    print(("PASS" if cond else "FAIL") + " " + name + ": " + str(obs), flush=True)
    if not cond:
        ok = False
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
T0 = [9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]], [8, [7, None, None], None]], None]

A = "D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
r = replay(parse(A))
t = (len(parse(A)), sum(l["a"] for l in r["legs"]), sum(l["q"] for l in r["legs"]))
check("A-SELR-OUT", t == (30, 52, 36) and R_ if False else t == (30, 52, 36), t)
check("A-closed-core", r["S1"] == r["S0"] and all(core_of(p[1]) is not None and len(core_of(p[1])) == 9 for p in r["pairs"]), "closure+core9")
B = "D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,D3,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
r = replay(parse(B))
legs = r["legs"]
check("B-E3", (len(parse(B)), sum(l["a"] for l in legs), sum(l["q"] for l in legs)) == (31, 53, 36), "A=53 Q=36")
iv = miv(legs)
e3 = [j for j in range(len(iv)) if iv[j]["H"] == 1 and iv[j]["q"] == 3 and iv[j]["c"] == 1]
found = any(legs[iv[j]["gi"]]["a"] == 1 and legs[iv[j]["gi"]]["q"] == 3 for j in e3)
check("B-zeroGamma-E3", found, "E3 a=1/q=3 present")
C = "D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D1,K1,K9,K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9"
r = replay(parse(C))
legs = r["legs"]
hit = [k for k, l in enumerate(legs) if l["m"] == "K" and l["a"] == 0 and l["q"] == 2]
check("C-zeroA-migration", (len(parse(C)), sum(l["a"] for l in legs), sum(l["q"] for l in legs)) == (29, 50, 36) and len(hit) > 0, "A=50 Q=36, a=0/q=2@%s" % hit)
# D: B-only vine K9,K1,K3,K5,K7,K5,K3,K1 depths 8,2,4,4,4,2,2,2 Q=14
# D: B-only right vine (root 1 ... 9 deep): K9,K1,K3,K5,K7,K5,K3,K1
V = [1, None, [2, None, [3, None, [4, None, [5, None, [6, None, [7, None, [8, None, [9, None, None]]]]]]]]]
Dw = [("K", x) for x in (9, 1, 3, 5, 7, 5, 3, 1)]
r = replay(Dw, A0=V, B0=V)
ds = [l["dB"] for l in r["legs"]]
check("D-vine-depths", ds == [8, 2, 4, 4, 4, 2, 2, 2] and sum(l["q"] for l in r["legs"]) == 14, ds)
# E: root-switch K9,K3,K5,K1,K9,K3,K7,K1 costs 2,2,3,2,2,2,3,2 Q=18.
# Compatible start is UNIQUE among 4862 nine-key shapes (exhaustive search):
# ambient fringe required (q=3 needs depth 6-7, impossible on 5 nodes).
Ew = [("K", x) for x in (9, 3, 5, 1, 9, 3, 7, 1)]
ESTART = [1, None, [4, [2, None, [3, None, None]], [7, [6, [5, None, None], None], [8, None, [9, None, None]]]]]
r = replay(Ew, A0=ESTART, B0=ESTART)
qs = [l["q"] for l in r["legs"]]
check("E-rootswitch", qs == [2, 2, 3, 2, 2, 2, 3, 2] and sum(qs) == 18, qs)
# F: naive A-projection failure (4-key right vine demo)
def conv(t):
    if t is None:
        return S.LEAF
    k, l, r = t
    return S.node(k, conv(l), conv(r))
Avail = conv([4, [3, [2, [1, None, None], None], None], None])
# prune off-core ancestor (key 4, suppose core={1,2,3}) then splay 1, vs splay-then-project
pruned = S.trace(Avail, 4)[0]  # bring 4 up? use projection: remove key 4 (BST delete=root removal)
# BST delete root 4 with left subtree: predecessor 3 up
def proj_delmax(t):
    # project out key 4 by standard BST deletion
    return S.trace(t, 4)[0]  # splay 4 to root first
P = proj_delmax(Avail)  # 4 at root
# contracted: merge (drop 4, join left): take left subtree as projection
Pproj = P[2]  # left subtree of root 4
s1 = S.trace(Pproj, 1)[0]
s2full = S.trace(Avail, 1)[0]
def drop4(t):
    # remove key 4 from tree by BST deletion (splay 4 up then drop with join)
    tt = S.trace(t, 4)[0]
    _, _, l, r = tt
    if l[0] == "leaf":
        return r
    # join: max of l up
    def mx(t):
        while t[0] != "leaf" and t[3][0] != "leaf":
            t = t[3]
        return t[1]
    m = mx(l)
    l2 = S.trace(l, m)[0]
    _, _, ll, _ = l2
    return S.node(m, ll, r)
s2p = drop4(s2full)
check("F-projection-fails", s1 != s2p, "prune-then-splay != splay-then-prune")
json.dump({"pass": ok, "checks": R}, open(PDIR + "CC_REGRESSIONS.json", "w"), indent=1)
print("REGRESSIONS: %s" % ("PASS" if ok else "FAIL"), flush=True)
sys.exit(0 if ok else 1)
