# Credit model, correct Hall normal form and exact all-starved factorization

[charge](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/scripts/wp6_overflow.py:329>) allocates credits C=(i,j,b),
j an A StepEv at access i and b in{0,1}. There are exactly 2A distinguishable units.
Demands D=(t,B-double sequence index), one per individual double, total Q_B.
For each demand, Gamma(D)=C_t union C_creator(D) union C_setup(t), omitting absent pools.
Every named pool is joined completely; duplicate pool IDs are counted once. Creator's setup
is NOT present. setup(t) is read before access t updates the root-arrival map, including
at nonstarved accesses. Adjacency order local-first changes a search order, not graph feasibility.

Hall: for every demand subset X, |X|<=|Gamma(X)|. Because access pools are disjoint,
|Gamma(X)|=2 sum_(i in N_access(X)) a_i. This exactly equates the unit and capacity versions.
Kuhn maximum matching and Konig alternating reachability are in the same file at277/299.

Correct minimal-deficiency proof: let X be inclusion-minimal deficient, k=|X|. For any d in X,
minimality gives |Gamma(X\{d})|>=k-1, while it is contained in Gamma(X), whose size<k.
Thus |Gamma(X)|=k-1 and Gamma(X\{d})=Gamma(X). No neighbor credit is private to a single
demand. Full pools have even capacities, so k is odd. This says nothing about different
ACCESSES sharing a pool: three demands of ONE access can provide all the required sharing.

Exact factorization theorem (all sizes): if every KEEP has a=0, every creator pool is empty,
and every positive-demand access t has only its own DELETE-setup pool. Distinct such
accesses have distinct setups by L2. Consequently the graph is a disjoint union of
complete bipartite graphs K_(q_t,2a_setup(t)), plus unused credits. Its maximum matching is
sum_t min(q_t,2a_setup(t)); its unmatched count is sum_t(q_t-2a_setup(t))^+.
Proof: the stated pools are the entire source adjacency; match independently inside each
disjoint complete component. This is a closed-form structural calculation, not a new Hall premise.

Scalar identity: R=sum(q-2a)^+, S=sum(2a-q)^+, R-S=Q_B-2A. Thus U4-S iff CD-U;
U4-M implies CD-U, while CD-U does NOT imply U4-M, as our physical witnesses prove.
Canonical local-first residualization need not preserve all possible matchings: other
demands can name an access's local pool as creator/setup. The historical 'locals exclusive'
phrase in PIVOT_RESIDUAL_JOINT.md is not valid for this full graph.
