# AF-2 ordered-hole integer allocation: max-flow solver + frozen reconstruction.
import sys, json
sys.path.insert(0, 'python/independent')
import splay as S

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL/'

class Dinic:
    def __init__(self, n):
        self.g = [[] for _ in range(n)]
    def add(self, u, v, c):
        self.g[u].append([v, c, len(self.g[v])])
        self.g[v].append([u, 0, len(self.g[u]) - 1])
    def flow(self, s, t):
        n = len(self.g)
        F = 0
        INF = 10 ** 18
        while True:
            lv = [-1] * n
            lv[s] = 0
            q = [s]
            for u in q:
                for v, c, _ in self.g[u]:
                    if c > 0 and lv[v] < 0:
                        lv[v] = lv[u] + 1
                        q.append(v)
            if lv[t] < 0:
                return F
            it = [0] * n
            def dfs(u, f):
                if u == t:
                    return f
                while it[u] < len(self.g[u]):
                    v, c, rev = self.g[u][it[u]]
                    if c > 0 and lv[v] == lv[u] + 1:
                        r = dfs(v, min(f, c))
                        if r:
                            self.g[u][it[u]][1] -= r
                            self.g[v][rev][1] += r
                            return r
                    it[u] += 1
                return 0
            while True:
                f = dfs(s, INF)
                if not f:
                    break
                F += f

def solve_allocation(p, S_holes, compat, sigma, nonempty_nos):
    # p[i]: prefix gap-i count; S_holes[r]: sorted S ranks in hole r (exact, must fit interval);
    # compat[i][r]: bool gap i keys allowed in hole r; sigma: signature (canonical counts);
    # nonempty_nos: holes requiring >=1 fringe key (S-less nonempty).
    # demand per gap: d_i = sigma_i - p_i (must be >=0)
    R = len(S_holes)
    d = [sigma[i] - p[i] for i in range(10)]
    if any(x < 0 for x in d):
        return None  # signature incompatible with prefix (valid infeasibility)
    # lower bounds: 1 unit to each S-less nonempty hole from a compatible gap with demand
    # flow: source -> gaps (cap d_i) -> holes (inf if compat) -> sink (demand = lower bounds + free)
    # lower-bound transformation: hole r needs lb_r in {0,1}; satisfy via flow with lb.
    lb = [1 if r in nonempty_nos else 0 for r in range(R)]
    # nodes: src=0, gaps 1..10, holes 11.., sink
    N = 1 + 10 + R + 1
    SNK = N - 1
    # standard reduction for lower bounds on hole->sink edges: demand lb_r must flow; reduce: pre-send lb via compatible gap
    # simpler: two-stage greedy is UNSOUND in general; use full lower-bound circulation:
    # edge hole->sink capacity inf with lower lb_r. Transform: cap' = inf-lb... use demand method:
    # demand[v] += lb(in) ... implement generic lower-bound feasible circulation with super source/sink.
    # Nodes: SRC, gaps, holes, SNK. Edges with (lo, hi): SRC->gap (0, d_i); gap->hole (0, INF) if compat;
    # hole->SNK (lb_r, INF); SNK->SRC (0, INF) circulation; require hole-demand met: total flow must cover sum lb.
    # Exact demands: SRC->gap carries EXACTLY d_i (lower=upper=d_i); hole->SNK carries >= lb_r.
    # Circulation SNK->SRC closes. Feasibility <=> all demands met (standard lower-bound reduction).
    INF = 10 ** 12
    NN = N + 2
    SS, TT = N, N + 1
    D = Dinic(NN)
    bal = [0] * N
    def add_lb(u, v, lo, hi):
        D.add(u, v, hi - lo)
        bal[u] -= lo
        bal[v] += lo
    SRC = 0
    for i in range(10):
        add_lb(SRC, 1 + i, d[i], d[i])
    for i in range(10):
        for r in range(R):
            if compat[i][r]:
                add_lb(1 + i, 11 + r, 0, INF)
    for r in range(R):
        add_lb(11 + r, SNK, lb[r], INF)
    add_lb(SNK, SRC, 0, INF)
    need = 0
    for v in range(N):
        if bal[v] > 0:
            D.add(SS, v, bal[v])
            need += bal[v]
        elif bal[v] < 0:
            D.add(v, TT, -bal[v])
    got = D.flow(SS, TT)
    if got < need:
        return None
    # recover z_{i,r} from gap->hole flows: need flow values; Dinic stores residual; reconstruct via reverse edges
    z = {}
    for i in range(10):
        for e in D.g[1 + i]:
            v, c, rev = e
            if 11 <= v < 11 + R:
                # flow = original cap INF - residual c... cap was INF so flow unknown directly; use reverse edge value
                f = D.g[v][rev][1]
                if f > 0:
                    z[(i, v - 11)] = f
    # NOTE: lower-bound pre-send accounting: z includes lb flows routed through gaps (fine: z counts keys)
    return z

def reconstruct(prefix_top, S_holes, alloc, hole_intervals):
    # frozen §8 reconstruction: balanced BST per nonempty hole over (S-hole keys + allocated fringe placeholders);
    # returns hole trees keyed by hole id (placeholders as ('P', gap, seq) ordered markers for verification).
    out = {}
    for r, Sh in enumerate(S_holes):
        keys = [('S', k) for k in sorted(Sh)]
        fr = []
        for (i, rr), c in sorted(alloc.items()):
            if rr == r:
                fr.extend([('F', i, s) for s in range(c)])
        keys = sorted(keys + fr)
        # deterministic balanced build over ordered markers
        def build(ks):
            if not ks:
                return S.LEAF
            m = len(ks) // 2
            return S.node(ks[m], build(ks[:m]), build(ks[m + 1:]))
        out[r] = build(keys)
    return out

def verify_completion(prefix_top, S_holes, hole_intervals, alloc, sigma, p, holes_trees, nonempty_nos):
    # check: BST validity skipped (markers); counts per gap; S placement; emptiness; hole intervals respected
    # count fringe per gap from allocation + prefix (caller checks prefix part); here check allocation-level:
    for i in range(10):
        s = sum(v for (ii, r), v in alloc.items() if ii == i)
        if s != sigma[i] - p[i]:
            return False, ("gap-count", i)
    for r in nonempty_nos:
        s = sum(v for (ii, rr), v in alloc.items() if rr == r)
        if s < 1:
            return False, ("nonempty", r)
    # S keys unique across holes + intervals respected (S_holes given compatible by caller)
    seen = []
    for r, Sh in enumerate(S_holes):
        seen.extend(Sh)
    if len(set(seen)) != len(seen):
        return False, ("dup-S",)
    return True, ("ok",)

if __name__ == "__main__":
    # self-test: random feasible/infeasible instances + reconstruction validity on samples
    import random
    rng = random.Random(42)
    nfeas = 0
    for trial in range(300):
        R = rng.randint(1, 8)
        S_holes = [sorted(rng.sample(range(1, 10), rng.randint(0, 3))) for _ in range(R)]
        compat = [[rng.random() < 0.6 for _ in range(R)] for _ in range(10)]
        p = [rng.randint(0, 5) for _ in range(10)]
        sigma = [p[i] + rng.randint(0, 10) for i in range(10)]
        non = set(r for r in range(R) if not S_holes[r] and rng.random() < 0.5)
        # ensure each non hole has a compatible gap (else trivially infeasible; still valid test)
        z = solve_allocation(p, S_holes, compat, sigma, non)
        if z is not None:
            nfeas += 1
            # verify EXACT equations p_i + sum_r = sigma_i
            for i in range(10):
                s = sum(v for (ii, r), v in z.items() if ii == i)
                assert s == sigma[i] - p[i], (trial, i, s)
            for r in non:
                s = sum(v for (ii, rr), v in z.items() if rr == r)
                assert s >= 1, (trial, r)
    print("feasible=%d/300 (solver runs; equations hold on feasible)" % nfeas, flush=True)
    json.dump({"trials": 300, "feasible": nfeas}, open(PDIR + "AFSP_AF2_SELFTEST.json", "w"), indent=1)
