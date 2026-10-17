# S03_INDEPENDENT_FINITE_GRAPH_ORACLE.py — brute-force reference (Gate I).
# Explicit states/edges per sort; direct finite enumeration. Shares NO code with the
# production quantified implementation (no DAG, no Z3). Results compared state-by-state.
# States: O-sort ints, M-sort ints (disjoint namespaces by sort, not value).

SAT, UNSAT, UNKNOWN = 'SAT', 'UNSAT', 'UNKNOWN'


class FiniteGraph:
    def __init__(self, O, M, edges):
        # edges: {(i,j,w): set((x,y))} with i,j in {0(O),1(M)}
        self.O = list(O)
        self.M = list(M)
        self.edges = {k: set(v) for k, v in edges.items()}

    def E(self, i, j, w):
        return self.edges.get((i, j, w), set())

    def pre(self, XO, XM, w):
        XO, XM = set(XO), set(XM)
        rO = set(s for (s, t) in self.E(0, 0, w) if t in XO)
        rO |= set(s for (s, m) in self.E(0, 1, w) if m in XM)
        rM = set(m for (m, t) in self.E(1, 0, 0) if t in XO) if w == 0 else set()
        return (rO, rM)

    def post(self, XO, XM, w):
        XO, XM = set(XO), set(XM)
        rO = set(t for (s, t) in self.E(0, 0, w) if s in XO)
        if w == 0:
            rO |= set(t for (m, t) in self.E(1, 0, 0) if m in XM)
        rM = set(m for (s, m) in self.E(0, 1, w) if s in XO)
        return (rO, rM)

    def minpre(self, XO, XM, w, alphabet):
        bO, bM = self.pre(XO, XM, w)
        lowsO, lowsM = set(), set()
        for a in alphabet:
            if a < w:
                lO, lM = self.pre(XO, XM, a)
                lowsO |= lO
                lowsM |= lM
        return (set(bO) - lowsO, set(bM) - lowsM)

    @staticmethod
    def union(A, B):
        return (set(A[0]) | set(B[0]), set(A[1]) | set(B[1]))

    @staticmethod
    def inter(A, B):
        return (set(A[0]) & set(B[0]), set(A[1]) & set(B[1]))

    def compl(self, A):
        return (set(self.O) - set(A[0]), set(self.M) - set(A[1]))

    def isempty(self, A):
        return not A[0] and not A[1]

    def equiv(self, A, B):
        return set(A[0]) == set(B[0]) and set(A[1]) == set(B[1])
