# G01_POTENTIAL_DUALITY_THEOREM.md — Phase G (G01-20)

For finite directed weighted G, TFAE: (1) no negative closed walk; (2) no
negative directed cycle; (3) exists Phi: V->R with Phi(v)-Phi(u) <= w on all
edges. Proof. (3)=>(1): sum around a closed walk telescopes the left side to
0 <= total weight. (2)=>(1): a closed walk decomposes into directed simple
cycles; if every directed simple cycle is nonnegative, every closed walk (sum
of its cycle decomposition) is nonnegative. Contrapositive gives (1)=>(2).
(2)=>(3): add a zero-weight super-source s* and run Bellman-Ford (|V|-1 relaxations); absence
of negative cycles makes distances d finite and satisfying
d[v] <= d[u]+w for all edges (standard relaxation invariant); set Phi = d.
Finiteness of G: the symbolic state space is finite (bounded Int domains,
audited widths: 9544 low vars) — enormous but finite, so the duality applies
mathematically. Decidability/termination within budget is NOT claimed (Step-02
scope). Only the certificate condition (edge inequalities) is frozen here;
no Phi is exhibited (Step-03 task). Verified on 175/175 two-node graphs + all
K-families (necessity and sufficiency both directions).
