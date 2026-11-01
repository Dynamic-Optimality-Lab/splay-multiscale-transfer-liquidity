# A full form obstruction lifts to an actual source cycle

Allowing arbitrary Theta and nonnegative H removes the extra architecture restriction. On the original reachable source domain, existence of a potential in this full form satisfying DELETE is equivalent to Coarse-Double. A finite valid contradiction to the full form produces an actual negative source cycle, rather than merely a conflict between terminal summaries.

This is a universal correspondence theorem and a burden audit. It proves neither CD nor its negation. No potential is constructed without assuming nonnegative source cycles.

## Source domain and exact two-phase identity

Fix a finite nonempty ordered key set K. Let P_K contain all pairs of BSTs on K. Let R_K be the forward closure of all diagonal pairs (T0,T0) under the original present-key DELETE and KEEP requests. Both sets are finite. R_K is forward closed by definition. These are mathematical source domains, not modifications to Stage 11G's separate frozen graphs or predicates.

For a physical state v=(A,B), put

    r=root(A), pi(v)=(A,S_r B), Q(v)=floor(d_B(r)/2).

A DELETE x has edge weight 2a, where a=ceil(d_A(x)/2). A root-aligned KEEP r has A cost zero, B-double count Q(v), and edge v->pi(v) of weight -Q(v). It is an actual source request; pi(v) is reachable whenever v is. A terminal state has equal roots, pi(v)=v and Q(v)=0. The converse Q(v)=0 does not imply equal roots: a final zig may remain.

Every original KEEP x factors exactly as

    (A,B) --DELETE x--> (S_x A,B)
          --root-aligned KEEP x--> (S_x A,S_x B).

The second A splay is a no-op. Thus endpoints, A StepEvs, B doubles, B zigs, and total weight 2a-q are unchanged. This uses the actual source splay on each tree, including parent-first same-side doubles. It is not a replacement by move-to-root rotations.

Let the split graph contain all DELETE edges and all root-aligned KEEP edges on the chosen forward-closed domain. Every split edge is an original legal operation; every original KEEP has the displayed split. Original and split cycles therefore have the same possible signed weights, after replacing edges as necessary. A cycle is negative exactly when Q_B>2A. Stuttering no-ops add zero and cause no difficulty.

## The full normal form is exhaustive

Let Theta be arbitrary finite real values on terminal states, and H(v)>=0 with H(t)=0 at terminal states. Set

    Phi(v)=Theta(pi(v))+Q(v)+H(v).                 (1)

The root-aligned B edge changes Phi by -Q(v)-H(v), which is at most -Q(v). Conversely, every potential obeying this B inequality has (1): take Theta(t)=Phi(t) and H(v)=Phi(v)-Phi(pi(v))-Q(v). The B inequality makes H nonnegative, and terminal idempotence makes it zero there.

No matching rule, scalar statistic, symmetry, diagonal normalization, or bounded-range restriction remains in (1). This is the same normal-form identity proved in EB01, now used on the actual source domain.

## Exact finite contradiction criterion

For a DELETE edge e:u->v, (1) turns its required bound into

    Theta(pi(v))-Theta(pi(u))+H(v)-H(u)
       <=2a_e-Q(v)+Q(u).                          (2)

Take any finitely supported nonnegative multipliers lambda_e on DELETE rows. Define physical incidence

    c(s)=sum_{e entering s} lambda_e
          -sum_{e leaving s} lambda_e.

The Theta coefficients cancel exactly when, for each terminal state t,

    sum_{s:pi(s)=t} c(s)=0.                       (3)

After this cancellation, the weighted left side is sum_s c(s)H(s). Since terminal H values are zero, a conic contradiction using only H>=0 requires

    c(s)>=0 for every nonterminal s.              (4)

Indeed the constraints -H(s)<=0 can cancel that coefficient only with nonnegative multiplier c(s). Negative c(s) cannot be silently discarded; arbitrary nonnegative reserve at that physical source may absorb the alleged deficit.

With (3)-(4), a negative right side

    W=sum_e 2a_e lambda_e-sum_s c(s)Q(s)<0         (5)

would be a valid contradiction. Every H variable must retain its complete physical-state identity, even when two states have the same pi image or Q=0.

## Constructive lift of that contradiction

Retain each DELETE edge with flow lambda_e. For each nonterminal s, add flow c(s) on the actual root-aligned KEEP edge s->pi(s). These added flows are nonnegative by (4), and their source weights are -Q(s).

At a nonterminal s the DELETE incidence is c(s); the added outgoing KEEP flow subtracts exactly c(s), so the total incidence is zero. At a terminal t the total incidence is

    c(t)+sum_{s nonterminal:pi(s)=t} c(s),

which is zero by (3). Therefore the lifted edge flow is a nonnegative physical circulation. Its weight is precisely (5), because Q(t)=0 at terminals and sum_e lambda_e(Q(v_e)-Q(u_e))=sum_s c(s)Q(s).

There are no free changes of B preimage in this lift. Every added edge is an actual present-key KEEP with A already at its root. Zero-double zig edges still belong to the lift when their positive flow is needed for physical balance; weight zero does not erase their state transition.

Any finite nonnegative circulation decomposes into directed cycles: follow positive-flow outgoing edges until a vertex repeats, subtract the smallest flow on that cycle, and repeat. Conservation guarantees an outgoing edge whenever positive incoming flow has reached a vertex. Each subtraction removes at least one positive edge, so finitely many steps suffice. The circulation's weight is a nonnegative weighted sum of cycle weights. If (5) is negative, at least one cycle has negative weight.

All lifted vertices belong to the chosen source domain. On R_K the negative cycle is reachable from a diagonal start and consists of actual DELETE/root-aligned KEEP requests. It therefore has Q_B>2A and is a genuine counterexample to the original CD statement. On P_K the same construction yields an actual closed pair walk, but its diagonal reachability must be proved separately.

This proves the certificate-lifting theorem for every finite K and every finite exact conic certificate of the stated full constraints. It is not an assumption of a future matching or charging witness.

## Finite-graph converse and precise existence burden

On R_K the following statements are equivalent:

1. Every reachable original closed pair walk satisfies Q_B<=2A.
2. The finite split source graph has no negative directed cycle.
3. A finite real pair function obeys every DELETE and root-aligned B inequality.
4. Some arbitrary Theta and nonnegative H in (1) obey every DELETE inequality.

The source factorization proves 1 iff 2. If 3 holds, summing its edge inequalities around a split cycle gives 0<=its weight, proving 2. To prove 2 implies 3, add an auxiliary vertex with zero-weight edges to every source state and define d(v) as the minimum weight of a path from it to v. Remove repeated closed subwalks from any path: without negative cycles this cannot increase its weight. A minimum therefore exists among finitely many simple paths. For every source edge u->v of weight w, d(v)<=d(u)+w, as required. These auxiliary edges are only a proof device, not physical source operations or reachability assertions. The normal-form identity proves 3 iff 4.

For P_K the identical proof gives equivalence with nonnegativity of all closed pair walks in P_K. That is a stronger cycle domain unless equality of the reachable and relevant all-pairs cycle domains is independently established. No such equality is assumed here.

The empty-key case has no present-key operations; the one-key case has only zero-weight operations. Both satisfy the equivalence with zero potential. Rank relabeling changes none of the source costs. Applying the finite statement to each size yields the all-size logical correspondence; it does not establish its open nonnegative-cycle premise.

## Consequence for the requested campaign

On the original reachable domain, the full Theta+Q+H form has no separate architecture-only obstruction. A refutation of the unrestricted full form would refute CD itself. An all-pairs obstruction could instead lie outside that original reachable domain and would need separate interpretation.

The optional exact-B architecture H=0 differs: it removes the physical slack constraints, so a terminal-projected negative cycle can refute it without yielding an actual negative CD cycle. That earlier class-elimination method cannot simply be promoted to unrestricted H.

This result corrects the scope of the previous strategic recommendation. A class-wide obstruction is a smaller architecture audit only while genuine additional restrictions remain. With arbitrary Theta and H, the proposed target has returned to the original source-cycle burden.
