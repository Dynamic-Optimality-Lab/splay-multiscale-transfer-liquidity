# PP_SYMBOLIC_OPERATORS.py — exact weighted operators over the explicit diagnostic product.
# Implements the full §11 API on the ACTUAL edge relation (decide + fibers, not a reimplementation);
# tested against an independent brute-force oracle at small scope. Full-scope symbolic compilation OPEN.
import sys, json, random, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PERSISTENT_PORT_FULL_CLOSURE')
import splay as S
from PP_LOW_RELATION import S_to_list, all_bsts
from PP_SYMBOLIC_PRODUCT import build_product

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PERSISTENT_PORT_FULL_CLOSURE/'


class Graph:
    def __init__(self, nodes, edges, prov=None):
        self.V = set(nodes)
        self.E = dict(edges)  # (s,w,t) -> mult
        self.prov = dict(prov) if prov else {}
        self.succ = {}
        self.pred = {}
        for (s, w, t) in self.E:
            self.succ.setdefault(s, []).append((w, t))
            self.pred.setdefault(t, []).append((w, s))

    # §11 API (exact Boolean semantics over the stored relation)
    def valid_state(self, v):
        return v in self.V

    def low_edge(self, s, t, w):
        return (s, w, t) in self.E

    def high_source(self, s):
        return any(self.prov.get((s, ww, tt)) == 'high' for (ww, tt) in self.succ.get(s, []))

    def high_destination(self, t):
        return any(self.prov.get((ss, ww, t)) == 'high' for (ww, ss) in self.pred.get(t, []))

    def pre(self, X, w):
        X = set(X)
        return {s for s in self.V if any(tt in X and ww == w for (ww, tt) in self.succ.get(s, []))}

    def post(self, X, w):
        X = set(X)
        return {t for t in self.V if any(ss in X and ww == w for (ww, ss) in self.pred.get(t, []))}

    def minpre(self, X, w):
        X = set(X)
        lower = set()
        for a in self.weights_below(w):
            lower |= self.pre(X, a)
        return self.pre(X, w) - lower

    def weights_below(self, w):
        return sorted({ww for (ss, ww, tt) in self.E if ww < w})

    def union(self, X, Y):
        return set(X) | set(Y)

    def intersection(self, X, Y):
        return set(X) & set(Y)

    def complement(self, X):
        return self.V - set(X)

    def equivalent(self, X, Y):
        return set(X) == set(Y)

    def is_empty(self, X):
        return len(set(X)) == 0

    def extract_witness(self, X):
        X = set(X)
        return None if not X else sorted(X)[0]


def make_oracle(V, E):
    by_src = {}
    by_dst = {}
    for (ss, ww, tt) in E:
        by_src.setdefault(ss, []).append((ww, tt))
        by_dst.setdefault(tt, []).append((ww, ss))
    def brute_pre(X, w):
        X = set(X)
        return {s for s in V if any(tt in X and ww == w for (ww, tt) in by_src.get(s, []))}
    def brute_post(X, w):
        X = set(X)
        return {t for t in V if any(ss in X and ww == w for (ww, ss) in by_dst.get(t, []))}
    return brute_pre, brute_post


if __name__ == '__main__':
    t0 = time.time()
    rng = random.Random(53)
    keys = [1, 2, 3, 4, 5, 6, 7]
    Sset = set(keys)
    M = {1, 2}
    trees = list(all_bsts(keys))
    seeds = [(A, A) for A in trees]
    nodes, edges, prov = build_product(keys, Sset, M, seeds, [0, 1, 2, 3])
    G = Graph(nodes, edges, prov)
    E = list(edges)
    W = sorted({w for (s, w, t) in E})
    V = list(nodes)
    brute_pre, brute_post = make_oracle(V, E)
    ntest = 0
    for trial in range(400):
        X = set(rng.sample(V, rng.randint(0, len(V))))
        w = rng.choice(W)
        assert G.equivalent(G.pre(X, w), brute_pre(X, w)), ('pre', trial)
        assert G.equivalent(G.post(X, w), brute_post(X, w)), ('post', trial)
        # minpre: brute force
        lower = set()
        for a in W:
            if a < w:
                lower |= brute_pre(X, a)
        assert G.equivalent(G.minpre(X, w), brute_pre(X, w) - lower), ('minpre', trial)
        # boolean algebra
        Y = set(rng.sample(V, rng.randint(0, len(V))))
        assert G.equivalent(G.union(X, Y), set(X) | set(Y)), ('union', trial)
        assert G.equivalent(G.intersection(X, Y), set(X) & set(Y)), ('inter', trial)
        assert G.equivalent(G.complement(X), set(V) - set(X)), ('compl', trial)
        assert G.is_empty(set()) and not G.is_empty(V), ('empty', trial)
        assert (G.extract_witness(set()) is None) and (G.extract_witness(V) in V), ('wit', trial)
        # valid_state / edge spot
        v = rng.choice(V)
        assert G.valid_state(v) and not G.valid_state(('nope', 'nope')), ('valid', trial)
        ntest += 1
    # quantifier hygiene: nested pre = two-step paths (exact binding, no leakage);
    # high_source/high_destination agree with provenance on every node
    for trial in range(100):
        X = set(rng.sample(V, rng.randint(0, len(V))))
        a, b = rng.choice(W), rng.choice(W)
        two = set()
        for s in V:
            for (w1, m) in G.succ.get(s, []):
                if w1 == b:
                    for (w2, t) in G.succ.get(m, []):
                        if w2 == a and t in X:
                            two.add(s)
                            break
        assert G.equivalent(G.pre(G.pre(X, a), b), two), ('hygiene', trial)
    for v in V:
        assert G.high_source(v) == any(prov.get((v, ww, tt)) == 'high' for (s2, ww, tt) in E if s2 == v), ('hs', v)
        assert G.high_destination(v) == any(prov.get((ss, ww, v)) == 'high' for (ss, ww, tt) in E if tt == v), ('hd', v)
    print('operators: trials=%d weights=%d ok time=%.1fs' % (ntest, len(W), time.time() - t0), flush=True)
    json.dump({'trials': ntest, 'weights': len(W), 'scope': '7-key diagnostic product'}, open(PDIR + 'PP_OPERATOR_TEST.json', 'w'), indent=1)
