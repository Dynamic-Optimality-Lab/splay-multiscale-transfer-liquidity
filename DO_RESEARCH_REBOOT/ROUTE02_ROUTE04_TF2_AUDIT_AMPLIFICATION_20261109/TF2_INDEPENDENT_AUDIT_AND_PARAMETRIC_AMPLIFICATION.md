# TF2 independent audit and parametric source amplification

Date: 2026-11-09, Asia/Karachi. Route 02 / Route 04.

**Decision I: AUDIT PASS at the fresh symbolic-reconstruction level.** The 97-key, 293-operation source and its frozen-selector K_{3,5} witness survive the checks below. This reconstruction is by the same agent that wrote the certificate; it is NOT an independent person/agent audit, external computational verification, or a proof-assistant certificate.

**Decision II: parametric amplification is established.** For every positive integers p,q, an explicit ordinary reachable paired-closed source W_{p,q} has

    K_{p,q} subset of G_int(W_{p,q}),
    N=2^(p+1)(q+1)+1.

The parametric word is a controlled variant of the original 97-key word: B stops at dyadic backbone roots, while intervening adjacent A descents are original DELETEs. The original certificate is audited separately, not silently replaced.

**Decision III: this amplified family does NOT have an unbounded cost ratio.** On the complete original period,

    A_prep=N-1,  A_critical=2^p-1,  A_restore=N-1,
    A_forward=Theta(N),
    U_int=Theta(N),
    U_int/A=Theta(1),

with absolute uniform constants. The upper bounds for the forward scans use the established classical sequential-access theorem, identified precisely in Section 8. No new potential is introduced.

Arbitrary complete-bipartite SUBGRAPH density and unbounded arboricity are therefore compatible with linear complete-period A cost. No unrestricted all-source U_int<=cA theorem, cost counterexample, or Dynamic Optimality conclusion is proved.

## 1. Frozen model, audit scope and status

The current source model is unchanged: A processes KEEP and DELETE by ordinary bottom-up splay; B processes KEEP and freezes on DELETE; no key is physically removed. Costs are the original sum of ceil(depth_A/2) and Q_B=sum_KEEP floor(depth_B/2).

Every source below has the allowed common diagonal A=B=V+(1,N), an empty reaching prefix, all physical keys S=M=X=[N], and exact closure in both COMPLETE labelled trees. V+ and V- are the full right and left vines on their displayed ordered interval. All physical keys are KEEP-visited by the full sweeps.

The inherited source results retain their symbolic/self-review or audit-pending qualifications. In particular, the Route 02/04 bound Q_B<=6A+U_int is not re-proved or promoted to externally certified status.

Use the FIXED Step 3 selector. For a neutral double d, F_d is its WHOLE grandparent frame, Gamma_d its actual B creation, kappa_d the B removal preceding Gamma_d, and Pi_d=(kappa_d,t_d^A]. Beta(d) is the LAST real A global-root entry into the CLOSED PHYSICAL SPAN of F_d after Gamma_d and through its post-A snapshot.

The FULL neutral creator forest includes every neutral double, including exposed nodes and nodes outside the selected graph. Roots carry their original Gamma token; unary children in T_q inherit; the first child by creation bit inherits at a binary node and the second receives the branch-access token. No convenient replacement of this rule is permitted or made.

A pass here means that the explicit mathematical checks have been reconstructed. It does not manufacture another independent auditor. The precise verification limit is carried into the final conclusions.

## 2. Fresh primitive checks

### 2.1 Ordinary rotations and the RR identity

An ordinary left rotation changes

    g(L,p(H,U)) -> p(g(L,H),U).

Substituting U=z(C,R), then performing the second actual left rotation, gives

    g(L,p(H,z(C,R)))
      -> p(g(L,H),z(C,R))
      -> z(p(g(L,H),C),R).                         (2.1)

These are actual full subtree transformations. The first output is g(L,H); the second is p(g(L,H),C). Both exclude actual target z.

The WHOLE old grandparent frame is transported to z; it is NOT removed by its own double. It is removed at a subsequent promotion of z above that frame. This is important for the exact sigma bit.

All bottom-up path operands are retained. Reflection derives LL. If the path turns, the target is promoted in both rotations, giving LR or RL in their literal order.

### 2.2 Extremal-ancestor test at EVERY rotation

If u is an ancestor of the maximum key N, a splay with actual target z<=u cannot destroy this relation. Only a left rotation at old pivot u that promotes its right child could take N outside u. That child is on the actual target path, which would require z>u. If u is promoted it keeps its old descendants; all other rotations transport the relevant subtrees.

Reflection: if u is an ancestor of minimum 1, a splay to z>=u preserves that relation at every rotation.

Thus, starting with a pivot c that is an ancestor of N, an increasing scan 1,...,N preserves c->N through KEEP c; after that access c is global root, and all later larger targets preserve c->1. Any label containing c and excluding both 1 and N stays absent throughout the entire scan.

This statement applies separately to physical A and physical B. It is not a snapshot-only or label-potential argument.

### 2.3 Sweep endpoint and orientation checks

After accessing 1,...,k, the visited prefix is a left vine rooted at k. The next target k+1 is the minimum of k's right subtree. Its search path is one RIGHT edge followed by zero or more LEFT edges. The old visited prefix moves rigidly and is attached under k+1 without any intervening key.

The internal doubles are LL. The final operation is RL if one left edge remains with the initial right edge, or a left zig if only the initial right edge remains. For the initial minimum access the path is entirely left: LL doubles and possibly a final right zig.

Induction yields V-(1,N) from ANY initial complete BST after the entire increasing scan. From that left vine the reverse targets N-1,...,1 are each a single right zig and produce V+(1,N).

These deductions verify legality and orientation throughout the reset without pretending that every reset access has cost one.

## 3. Stage 1: reconstruct the original 97-key source

### 3.1 The whole period

The word is exactly

    t=1,...,96:    DELETE 2,...,97;
    t=97,...,100:  KEEP 97,96,95,94;
    t=101,...,197: KEEP 1,...,97;
    t=198,...,293: KEEP 96,...,1.

There are 96+4+97+96=293 operations, all legal on the full key set [97]. The initial common right vine is itself an allowed diagonal; the prefix is legitimately empty.

After each preparation DELETE k,

    A=k(V-(1,k-1),V+(k+1,97)).

Each is one left zig. B remains the right vine. After KEEP 97 A is the left vine and has cost zero at that KEEP. Each of KEEP 96,95,94 is one right A zig, giving the same displayed form with k=96,95,94.

Define perfect trees P_h(c) by

    P_1(c)=c,
    P_(h+1)(c)=c(P_h(c-2^(h-1)),P_h(c+2^(h-1))).

The primitive identity (2.1), applied along the literal B paths, reconstructs these COMPLETE B states:

    after 97:
       97(C_1,-);
       C_i=(2i)((2i-1),C_(i+1)), i=1,...,48;
       C_49=-.

    after 96:
       96(D_0,97);
       D_i=(4i+2)(T_i,D_(i+1)), i=0,...,23;
       T_0=1; T_i=P_2(4i) for i>=1; D_24=95.

    after 95:
       95(E_0,96(-,97));
       E_i=(8i+6)(L_i,E_(i+1)), i=0,...,11;
       L_0=2(1,4(3,5));
       L_i=P_3(8i+2) for i>=1; E_12=-.

    after 94:
       94(Q_0,95(-,96(-,97)));
       Q_i=(16i+6)(R_i,Q_(i+1)), i=0,...,5;
       R_0=2(1,4(3,5));
       R_i=P_4(16i-2) for i>=1; Q_6=P_3(90).

The corresponding B paths are

    1,2,...,97:              48 RR doubles;
    97,2,4,...,96:           23 RR then one LR;
    96,2,6,...,94,95:        12 RR then one right zig;
    95,6,14,...,94:           5 RR then one LR.

The left-tree key counts are respectively 96,95,94,93; the displayed root and right tails supply exactly the remaining keys. The shortened outer block and final right remainder are included, not approximated by an infinite repeating pattern.

By Section 2.3, both trees become the full left vine at t=197 and then the full right vine at t=293. All 97 physical labels and both complete endpoints therefore agree exactly with the start.

### 3.2 Fifteen frames, creators and removals

For i=1,...,5 set a_i=87-16i, giving 71,55,39,23,7. The reconstructed table is

| i | Initial neutral ancestor p_i | d_1i | d_2i | d_3i |
|---|---|---|---|---|
| 1 | (97,13) | (98,6) | (99,3) | (100,1) |
| 2 | (97,21) | (98,10) | (99,5) | (100,2) |
| 3 | (97,29) | (98,14) | (99,7) | (100,3) |
| 4 | (97,37) | (98,18) | (99,9) | (100,4) |
| 5 | (97,45) | (98,22) | (99,11) | (100,5) |

Before those RR doubles the grandparent roots and frames are respectively

    p_i:  root a_i,    frame [a_i,97];
    d_1i: root a_i+1,  frame [a_i,96];
    d_2i: root a_i+3,  frame [a_i,95];
    d_3i: root a_i+7,  frame [a_i,94].

Their first outputs have intervals {a_i},[a_i,a_i+2],[a_i,a_i+6],[a_i,a_i+14]. Their second outputs end at 96,95,94,93 respectively. At the original post-A snapshots every proper A label starts at 1 or ends at 97. Both outputs of all twenty displayed doubles exclude both extremes. The old removed labels contain the actual A root, so both producing rotations have Psi change zero. This independently establishes neutrality.

The selected creators are

    Gamma(d_1i)=B(97,8i+5,1);
    Gamma(d_2i)=B(98,4i+2,1);
    Gamma(d_3i)=B(99,2i+1,1).

The actual first B consumers are the next KEEPs 96,95,94. No intervening B access occurs. A creator excludes its target and its output persists to access end.

Current-run removals are

    sigma(d_1i)=B(98,4i+3,1);
    sigma(d_2i)=B(99,2i+2,1);
    sigma(d_3i)=B(100,i+1,1), i<=4;
    sigma(d_35)=B(100,6,0).

The last bit is 0 because the next double is LR and already promotes actual target 94 in its FIRST rotation.

Before the packet the selected labels are absent from the right vine. Other first-SS outputs in the packet have at most 15 keys, whereas these frames have at least 24. Target outputs have the exact distinct end labels listed above. Final boundary outputs include 1 or 97. After the packet all selected frames contain pivot 94; Section 2.2 excludes their B presence during the entire increasing reset. The decreasing reset has only prefix/suffix labels.

Thus each selected frame has exactly ONE B creation/removal run per period. Its preceding kappa is the previous cyclic occurrence of the displayed sigma. Its FULL original window is

    Pi(d_ji)=(previous-cycle sigma(d_ji),t_(97+j)^A].

### 3.3 Full-window A absence and exact event pairs

During preparation, the critical A descents and reverse restoration, A has only prefix/suffix proper labels at every real rotation. During the increasing reset A begins rooted at 94. Every selected frame contains 94 and excludes 1 and 97. Section 2.2 excludes it at EVERY reset rotation as well.

Consequently all fifteen selected frames are A-absent on the ENTIRE cyclic period, hence on their complete Pi windows. Their lower endpoints exceed 1 and upper endpoints are below 97: all are interior.

There is exactly one A root entry after each immediate creator:

    beta_1=A(98,1,0), q=96;
    beta_2=A(99,1,0), q=95;
    beta_3=A(100,1,0), q=94.

For p_i, its preceding whole-frame creator is the reverse KEEP a_i-1. The original physical IDs are

    tau_i=(ROOT,B(295-a_i,1,0))
       = (ROOT,B(224,1,0)), (ROOT,B(240,1,0)),
         (ROOT,B(256,1,0)), (ROOT,B(272,1,0)),
         (ROOT,B(288,1,0)).

At those reverse operations A and B are synchronized, and both perform one right zig creating the suffix [a_i,97]. The B zig is decreasing, so p_i is genuinely a ROOT of the full neutral forest.

For every required q in {94,95,96}, the first-output labels {a_i},[a_i,a_i+2],[a_i,a_i+6] end below q. Thus every required link

    p_i -> d_1i -> d_2i -> d_3i

is unary in its actual T_q; the original root token inherits. Other full-forest children are not deleted; their labels simply exclude q. Each selected d has actual producer q and hence no child containing q. The fixed first-child descent returns its incoming token.

The original selector therefore gives d_ji -> (beta_j,tau_i). The three real A-entry bits and five unsplit original root tokens form K_{3,5}; 15>2(8-1)=14 refutes TF2.

**Stage 1 verdict: AUDIT PASS for this symbolic reconstruction; no mathematical defect found.** The complete neutral forest is used, not a forest rebuilt on the selected subset. No enumeration of irrelevant reset branches is needed: Gamma fixes each selected parent, and the only alternative child labels are explicitly excluded for the required q. External/different-agent verification is still pending.

### 3.4 Base-source A costs and all-demand clarification

Directly from the actual A zigs,

    A_prep=96, A_critical=3, A_restore=96,
    A_total=195+A_forward.

Before the forward sweep A has root 94, the left vine on [1,93] and right vine on [95,97]. The first access to 1 has depth 93 and cost 47. The remaining 96 distinct consecutive targets each cost at least one, so A_forward>=143.

For the first 94 targets, greater keys are a rigid right hanger and cannot enter the search path. After target k-1, the next k has at most 94-k+1 unvisited local nodes on its path. Hence

    A_forward
       <=47+sum_(r=1)^93 ceil(r/2)+3
       =47+2209+3=2259.

Therefore 338<=A_total<=2454, without a replay or an invented exact total. Section 8 also supplies a uniform linear scan bound.

There are 23+11+5=39 interior RR neutral demands in the three later critical accesses, not merely the fifteen selected edges. Each is globally A-absent by the same endpoint/pivot argument. Initial critical frames ending at 97 are boundary frames, not U_int. Consequently

    39 <= U_int(W_TF2) <= 39+Q_B(forward reset).

The old certificate did not claim fifteen was the full U_int count; no correction to its graph witness is needed.


## 4. Stage 2: an exact parametric ordinary source

### 4.1 Parameters, word and occurrence times

Let p,q be ANY positive integers. Set

    N=2^(p+1)(q+1)+1,
    b_j=N+1-2^j,             j=0,...,p+1;
    m=b_p=N+1-2^p.

Start at A=B=V+(1,N), with empty prefix and X=S=M=[N].

The exact full word W_{p,q} is:

1. DELETE 2,...,N.
2. Access k=N,N-1,...,m in that order. Tag it KEEP exactly when k=b_j for some j=0,...,p; tag every other access DELETE.
3. KEEP 1,...,N.
4. KEEP N-1,...,1.

All intervening DELETEs in item 2 are original positive A work. They preserve the actual A vine-state invariant; they are neither erased nor assigned cost zero.

The period length is

    L=(N-1)+2^p+N+(N-1)=3N+2^p-2.

Original operation indices are fully specified:

    preparation DELETE k: t=k-1;
    descending access k:  t=2N-k;
    critical KEEP b_j:    t_j=N-1+2^j;
    forward KEEP k:       t=N+2^p-1+k;
    reverse KEEP k:       t=3N+2^p-1-k.              (4.1)

The parametric word is NOT claimed to equal the original word when p=3,q=5. At those parameters N=97, but the B targets are 97,96,94,90 and the complete period has 297 operations. The literal original 293-operation word was checked separately in Section 3.

### 4.2 Exact complete B recurrence

Write

    s_j=2^(j+1),
    n_j=(N-1)/s_j=2^(p-j)(q+1).

Define the ordered left chain C^(j)_i for i=0,...,n_j-1 by

    r_i=2+s_j i;
    C^(j)_i=r_i(T_i,C^(j)_(i+1));
    T_0=1;
    T_i=P_(j+1)(r_i-2^j),     i>=1.

Its final right remainder and the root's right subtree are

    C^(j)_(n_j)=R_j;

    R_0=H_0=-;
    R_j=P_j(N+1-3*2^(j-1)),   j>=1;
    H_j=P_j(N+1-2^(j-1)),     j>=1.

The exact full B tree after critical KEEP b_j is

    B_j=b_j(C^(j)_0,H_j).                          (4.2)

Its left chain's last root is b_(j+1)=N+1-2^(j+1); its right remainder R_j runs from that root plus one through b_j-1. No remainder or outer block is omitted.

Base j=0: ordinary splaying N in the right vine gives n_0 RR doubles, and the two-rotation transformation (2.1) gives the even-root chain with odd left leaves. This is precisely (4.2), including R_0=H_0=empty.

Inductive step j->j+1: the next target b_(j+1) is the LAST root on the current left chain. Its literal path begins with a LEFT edge from b_j, then follows the chain RIGHT. The chain length n_j is even because j<p.

There are n_j/2=n_(j+1) doubles: n_(j+1)-1 RR doubles, then a final LR. Each interior RR right-spine pair g,p separated by s_j has perfect left blocks of size s_j-1. Its first RR output is the perfect tree P_(j+2)(g), obtained from the two actual side blocks and g. The second output has root p and the previous target-left subtree as its right hanger. The new chain therefore has spacing 2s_j and the displayed T_i.

The actual target's old left subtree is R_(j+1). The final LR leaves old root b_j on the new root's right:

    H_(j+1)=b_j(R_j,H_j)=P_(j+1)(b_j).

The outer root 2 and its left leaf 1 remain explicit. These facts prove (4.2) for every j, without a finite-state extrapolation.

For a full label/count check, C^(j)_0 contains exactly keys 1,...,b_j-1:

    n_j roots
    +1 outer left leaf
    +(n_j-1)(s_j-1) perfect-block keys
    +(2^j-1) remainder keys
    =N-2^j=b_j-1.

H_j has exactly keys b_j+1,...,N, and the single root b_j completes the full labelled key set.

### 4.3 Closure and legality in both trees

Preparation makes A=V-(1,N), while B stays V+(1,N). During item 2, every A target decreases by exactly one, including DELETE targets. Every such step after KEEP N is one right zig. Thus at EACH critical access

    A=b_j(V-(1,b_j-1),V+(b_j+1,N)).                 (4.3)

All B transitions are the actual ordinary accesses proved in (4.2); DELETEs freeze B. Then the full increasing sweep makes both trees V-(1,N), and the complete decreasing sweep makes both V+(1,N).

This proves legality, genuine all-key support, empty-prefix reachability and exact COMPLETE labelled paired closure for every p,q. It does not impose a vine-only restriction on the unrestricted theorem; it constructs an allowed family within its domain.

## 5. The parametric frozen event pairs

### 5.1 Column intervals and row occurrences

For i=1,...,q set

    a_i=N+2-2^(p+1)(i+1)
       =2^(p+1)(q-i)+3.                            (5.1)

For j=0,...,p let

    k_ji=2^(p-j)(i+1)-1.

Use p_i=(t_0,k_0i) for the initial neutral ancestor. For j=1,...,p define

    d_ji=(t_j,k_ji);
    u_j=b_(j-1)-1=N-2^(j-1);
    F_ji=[a_i,u_j].                                (5.2)

The genuine index recurrence is

    k_(j-1),i=2 k_ji+1.                            (5.3)

It follows from actual alternate ancestor positions on the right spine, not from extrapolating 8i+5 -> 4i+2 -> 2i+1 -> i.

For row j>=1, the RR double k has actual grandparent

    g=b_j-2^(j+1)k,
    min whole frame =g-(2^j-1)
                    =N+2-2^(j+1)(k+1),
    max whole frame =u_j.

Substituting k_ji gives exactly F_ji. Its outputs are

    first:  [a_i,a_i+2^(j+1)-2];
    second: [a_i,b_j-1], rooted at a_i+2^(j+1)-1.    (5.4)

For j=0 the initial double at root a_i has whole frame [a_i,N], first output {a_i} and second [a_i,N-1].

Every selected k_ji lies in 1,...,n_j-1, the actual interior RR range. Its maximum at i=q is exactly n_j-1. The selected ancestor p_i also precedes the last initial RR double. Thus no selected occurrence is a boundary LR or an invented event.

All a_i>=3 and all u_j<N; further,

    a_i < m=b_p <= b_j <= u_j.

Both outputs in (5.4) exclude 1,N. At (4.3) the old removed labels contain actual target b_j and are A-absent, while the new outputs are neither A prefix nor A suffix. Both producing rotations are neutral.

### 5.2 Original creators, first hits and current-run removals

For j>=1,

    Gamma(d_ji)=B(t_(j-1),2 k_ji+1,1).              (5.5)

This is exactly the bit-1 rotation of the preceding row's original double, whose index is k_((j-1)i)=2 k_ji+1.

That second output is [a_i,b_(j-1)-1]=F_ji. It excludes its creating target b_(j-1). Between this creator and the next KEEP b_j there are only the explicit A-only DELETEs. Since b_j is in F_ji, the actual first B hit is exactly that next KEEP.

To avoid ambiguous multi-index typography, the same formula in words is: the creator of row j, column i is rotation bit 1 of the preceding row's double indexed by 2 k_ji+1.

The current frame is removed at the NEXT double of its consumer:

    sigma_ji=B(t_j,k_ji+1,1),   i<q;
    sigma_jq=B(t_j,n_j,0).                         (5.6)

For i<q that next double is RR; for i=q it is the final LR, whose first rotation already promotes the actual target. No virtual bit is used.

Each selected frame has just one B run per period. In the descending packet, any first-SS output has at most 2^(p+1)-1 keys, whereas a selected frame has at least 7*2^(p-1)-1 keys, strictly more. Target-created output upper endpoints are the distinct u_j; boundary outputs contain 1 or N. Thus only the specified Gamma creates the selected label.

After its first consumer all later critical targets remain inside that label, so they cannot recreate it. After the final critical access all selected frames contain global pivot m. The extremal-ancestor argument of Section 2.2 excludes them throughout B's increasing scan; reverse vine states exclude them as well.

Hence kappa_ji is exactly the previous cyclic occurrence of sigma_ji, and

    Pi_ji=(previous-cycle sigma_ji,t_j^A].           (5.7)

### 5.3 Full-window A absence

During preparation, the ENTIRE descending packet including all DELETEs, and reverse restoration, every A state has only prefix/suffix proper labels.

At the start of the forward sweep, A's right side is the full right vine. For each u_j>=m, u_j is an ancestor of N. Targets <=u_j preserve that relation through KEEP u_j; larger later targets preserve u_j->1 after u_j becomes root.

Every F_ji contains u_j and excludes both extremes. Therefore it is A-absent at EVERY A rotation of the full period, in particular throughout (5.7).

This also covers all the OTHER interior RR frames in the critical packet, not just the q selected columns: their upper endpoint is the same u_j. No full-window exposure is hidden by the A-only descents or reset.

### 5.4 Beta entries and original ROOT tokens

After the creating access b_(j-1), A is rooted strictly above F_ji. Its first next adjacent descent enters that interval at u_j. All subsequent descending A roots through b_j remain inside it. Thus the selected LAST entry is

    beta_j=A(N+2^(j-1),1,0),  q_beta=u_j.            (5.8)

For j=1 this operation is KEEP b_1. For j>=2 it is the explicit DELETE u_j. In those rows q_beta is NOT the eventual KEEP target b_j; the distinction is required by the original selector.

The root p_i's whole-frame creator is the synchronized reverse KEEP a_i-1. Its original token is

    tau_i=(ROOT,B(3N+2^p-a_i,1,0)).                 (5.9)

This is one real decreasing B zig; the five-token computation of Stage 1 has become a genuine formula. Each p_i is a root of the FULL neutral forest.

The actual forest path is

    p_i -> d_1i -> ... -> d_pi.

For the required q=u_j, all earlier second outputs contain q. At every earlier parent row ell<j the competing first output ends at most at

    a_i+2^j-2
       <= N-2^(p+2)+2^j
       < N-2^(j-1)=q.

Thus the path is unary in T_q even if every possible other full-forest child exists. The original root token inherits. At d_ji both its outputs lie below b_j<=q, so it is a leaf of T_q and the fixed first-child descent preserves its incoming token.

Consequently the FIXED original association is exactly

    d_ji -> (beta_j,tau_i),   1<=j<=p, 1<=i<=q.      (5.10)

There are p distinct real A-entry bits, q distinct unsplit original ROOT tokens and pq distinct original double edges. All other graph edges and all reset forest branches remain in the full graph; they do not change these identities.

## 6. Exact amplification result and its scope

Equations (4.1)–(5.10) prove for EVERY positive p,q that the full admissible source contains K_{p,q}, with exactly pq selected edges and p+q selected vertices. Thus p=q=t gives subgraph density t/2, unbounded.

The exponential spacing is a genuine requirement of THIS propagation construction. The initial output chain has (N-1)/2 roots. Each next selected backbone access consumes alternating positions and halves that count. At the last generation n_p=(N-1)/2^(p+1) must supply q interior RR events plus its one boundary event, so

    N-1 >= 2^(p+1)(q+1).

Our choice attains equality. This is not a lower bound on N for ALL conceivable ways of realizing K_{p,q}; no such universal geometric necessity is claimed.

The literal adjacent-descending word in the old 97-key certificate is therefore not blindly extrapolated. The dyadic-target variant has a complete all-parameter recurrence, including the real A-only work needed between B targets.


## 7. Stage 3: COMPLETE-period A costs

Let m=N+1-2^p, the final critical A/B root.

### 7.1 Exact non-forward components

The actual A operations give

    A_prep=N-1;
    A_critical=2^p-1;
    A_restore=N-1.                                (7.1)

Preparation is N-1 adjacent left zigs. KEEP N has A cost zero; every one of the following 2^p-1 adjacent descents is one right zig, including all DELETEs. Restoration is N-1 actual right zigs after the full forward scan.

Thus, with F_A denoting the TRUE cost of the increasing reset,

    A(W_{p,q})=2N+2^p-3+F_A.                       (7.2)

There is no preparation in the excluded reaching prefix. The prefix is empty.

### 7.2 Forward-cost formula and direct finite bounds

Let S_A(m) be the actual A StepEv cost of accessing 1,...,m starting at V-(1,m). It is a definite ordinary-splay cost, not an assumed closed form.

Keys greater than m remain in a rigid right hanger during the first m accesses, so their actual depths and events agree with that m-key history. At its end the remaining N-m successors are each a single left zig. Therefore

    F_A=S_A(m)+(N-m).                              (7.3)

The first access has cost c_m=ceil((m-1)/2). All other N-1 targets differ from their preceding roots. The next unvisited local target k has depth at most m-k+1. Consequently the direct finite bounds are

    N-1+c_m <= F_A
       <= c_m+floor(m^2/4)+(N-m).                  (7.4)

The upper sum uses sum_(r=1)^(m-1) ceil(r/2)=floor(m^2/4). No replay or computational recurrence evaluation is hidden in this estimate.

For the original 97-key word m=94, (7.4) reproduces 143<=A_forward<=2259 and 338<=A_total<=2454. An exact numerical A_forward is NOT claimed.

## 8. Established linear scan bound and its precise dependency

The classical sequential-access theorem gives an absolute constant C_seq>=1 such that, for every ordinary initial N-key BST, accessing all keys once in increasing order has both StepEv cost and double cost at most C_seq N. One may take a larger common constant to cover both conventions: ceil(d/2) and floor(d/2) are bounded by the standard access-plus-rotation cost.

This is Tarjan's published sequential-access theorem, not the unproved Dynamic Optimality theorem. Its identity was already present as reference [65] in the local Levy–Tarjan material. The [primary publisher statement](https://link.springer.com/article/10.1007/BF02579253) was checked. The complete subscription-paper proof and a numerical optimal constant were not newly audited here. It is an explicit standard mathematical dependency; no new potential is introduced.

Apply it separately to the two actual initial reset trees:

    F_A <= C_seq N,
    Q_B(forward reset) <= C_seq N.                 (8.1)

A and B need not agree at reset start. The theorem allows arbitrary initial complete trees, exactly as required. The forward scan and all its costs remain INSIDE the source.

From (7.2), (8.1), and 2^p< N/4,

    2N+2^p-3+(N-1+c_m)
       <= A(W_{p,q})
       <= (C_seq+9/4)N.                            (8.2)

In particular A=Theta(N), with constants independent of p,q. This conclusion is proved using the stated classical scan theorem; it is not attributed to a new independent verification of that theorem.

## 9. Count ALL interior demands and determine the ratio

### 9.1 Exact critical count; all other classes retained

The initial KEEP N has n_0-1 neutral RR doubles whose whole frames end at N. They are boundary frames, not U_int.

For each later critical row j=1,...,p, exactly n_j-1 doubles are RR with whole frames

    [N+2-2^(j+1)(k+1),u_j],
       k=1,...,n_j-1.

Every lower endpoint is at least 3. All are neutral by (4.3) and (5.4), and all are globally A-absent by the upper-endpoint argument of Section 5.3. The final LR double is nonneutral: it creates the common full left and right A-root sides.

Thus the COMPLETE critical interior count is exactly

    C_crit=sum_(j=1)^p (n_j-1)
          =((N-1)/2)(1-2^(-p))-p
          =(2^p-1)(q+1)-p.                        (9.1)

This includes many edges outside the displayed K_{p,q}. Indeed C_crit-pq=(2^p-1-p)(q+1)>=0.

Preparation has no B events. Reverse restoration has only B zigs and no doubles. Every further interior demand, of ANY provenance or payment status, lies in the full increasing reset. Bound it by ALL its B doubles, rather than discard it:

    C_crit <= U_int(W_{p,q})
            <= C_crit+Q_B(forward reset)
            <= (C_seq+1/2)N.                      (9.2)

The exact number of exposed versus unexposed reset frames is not enumerated. Equations (9.1)–(9.2) are full-scope bounds sufficient for the required asymptotic decision. They do not redefine U as only the selected, silent, residual, or g1-unpaid set.

### 9.2 Uniform lower and upper bounds

Because N-1>=2^(p+2) and p<=2^(p-1),

    C_crit >=(N-1)/4-p
            >=(N-1)/8
            >=N/9,               N>=9.

Combine this with (8.2) and (9.2). Since A>=N,

    1/[9(C_seq+9/4)]
       <= U_int(W_{p,q})/A(W_{p,q})
       <= C_seq+1.                                (9.3)

The upper constant is deliberately coarse and absolute. Thus the FULL actual ratio is uniformly bounded AND bounded away from zero in this parametric family. The family proves neither divergence nor convergence to a particular numerical limit.

In particular it is cost-solvent in the requested sense:

    U_int(W_{p,q}) <= c_0 A(W_{p,q}),
    c_0=C_seq+1<infinity.                          (9.4)

This is a restricted-family theorem, not the unrestricted all-source assertion.

### 9.3 Selected incidence versus actual work

For the selected pq edges alone,

    pq/A <= pq/[2(N-1)]
          =pq/[2^(p+2)(q+1)]
          <p/2^(p+2).                              (9.5)

As p grows this selected-edge-to-cost ratio tends to zero, uniformly in q. Meanwhile the FULL U_int remains Theta(N), owing to all the additional critical frames and whatever reset demands occur. It would be wrong to replace U_int by pq and announce that the full ratio tends to zero.

Answers to the four cost questions:

1. Unbounded SUBGRAPH incidence density is achievable: p=q=t gives t/2.
2. This family does NOT establish an unbounded full U_int/A; (9.3) rules it out.
3. Its carrier and preparation/restoration costs grow exponentially with row count p. The exact spacing recurrence forces N-1=2^(p+1)(q+1) in this construction.
4. The whole family satisfies the uniform bound (9.4), using every original operation.

## 10. A physical source-work association for the critical class

There is a sharper source explanation than total-cost asymptotics alone.

For an arbitrary critical interior RR demand indexed by row j and double k, where 1<=j<=p and 1<=k<=n_j-1, put

    ell(j,k)=2^(j-1)(2k+1).                         (10.1)

Its range lies in 1,...,n_0-1 because

    ell(j,k)<=n_0-2^(j-1)<=n_0-1.

Distinct pairs (j,k) give distinct ell: the exact exponent of 2 dividing ell is j-1; its remaining odd factor recovers k. These ell are ORIGINAL initial neutral-root double indices, not newly introduced tokens.

The root at initial double ell has whole frame [a_ell,N], where

    a_ell=N-2ell>=3.

Its actual original B creator is reverse KEEP a_ell-1. Associate the critical demand to the REAL A restoration zig at that operation:

    f(j,k)=A(3N+2^p-a_ell,1,0).                    (10.2)

Every f(j,k) is one actual cost-one A StepEv. The map is injective across ALL critical rows and all their RR demands.

At this reverse operation, before A moves, the two trees are equal with root a_ell. A loses the B-common proper prefix [1,a_ell-1] and creates the right suffix [a_ell,N] not yet proper in B. This is a positive original A rotation. The later original B zig creates that suffix A-common and decreases. Thus (10.2) identifies actual physical restoration work and an actual decrease/positive-head pair, with maximum fiber ONE.

This is a cost-counting association, not a new historical owner map. The A rotation may already be g1-owned. No payment is reallocated, no virtual bit becomes real, and no Bank25 receipt is created.

The associated root need not be the demand's own endpoint token. Higher generations use real spacer roots omitted from the selected K_{p,q}. This explains how bounded physical work counting can survive the failure of every bounded endpoint-only assignment.

The association proves, within this literal source family,

    all critical U_int <= distinct restoring A zigs.

It remains compatible with the separate forward-reset bound (8.1). No same physical event is duplicated within the critical work class. Repetitions of the full period use their distinct original occurrence IDs.

For composition, U_critical<=A_restore<=A and U_forward<=C_seq N<=C_seq A give U_int<=(1+C_seq)A. These are two independently bounded cost classes; the added coefficient explicitly permits reuse of the same physical inventory between classes. No claim is made that every full-source demand has a distinct unit under one historical payment matching.

## 11. What the graph amplification does and does not refute

For any constant L, a rule assigning EVERY edge to one of its OWN two original endpoint vertices, with load at most L, would require pq<=L(p+q) on the selected K_{p,q}. Taking p=q arbitrarily large contradicts this. Historical vacancy is irrelevant.

The same subgraphs rule out uniform arboricity, bounded degeneracy and every-subgraph constant edge/vertex density. For two forests the original K_{3,5} already suffices.

They do NOT by themselves refute a bound

    |E(G_int(W))| <= c |V(G_int(W))|

ONLY for each complete full graph G_int(W). Restricting to H deletes potentially many other vertices, so a full-graph-only density assertion is logically different from an all-subgraph/arboricity assertion. No full-graph unbounded density is established here.

They also do not refute assignments to OTHER original A events: (10.2) explicitly uses restoration work outside the chosen endpoint subset. No conclusion against U_int<=cA or Dynamic Optimality follows from graph density alone.

## 12. The exact remaining universal obligation

The restricted source mechanism is now concrete:

* Repeated target-output compression consumes alternating positions.
* Many original spacer roots are required for surviving columns.
* The complete word has N-1 actual A preparation zigs and N-1 actual A restoration zigs.
* Formula (10.2) selects distinct physical restoration events for ALL critical interior demands.
* The complete reset contributes at most a uniform linear scan cost.

The imported global root bound r<=4A also recognizes the large initial root population: this family has n_0-1=(N-3)/2 genuine neutral roots with distinct decreasing creators. That inherited fact does not need a vacant owner.

The first unsupported universal extension would be:

    Every reused interior-history collection admits the same
    fresh spacer-root/restoration-event accounting, with
    globally bounded overlap across all original cohorts.

This does NOT follow from existing Route 02/04 facts. In a general source, a spacer may itself descend from an older neutral creation; different birth accesses and first-consumer cohorts can share root and A events; the local parity bound has an endpoint allowance per cohort; root/branch tokens can persist and branch at different key regions. The arithmetic indexing (10.1) belongs to this literal recurrence and is not an invariant of arbitrary splay histories.

Complete closure alone does not specify a globally disjoint collection of A restoration events. Private A ancestors, persistent blockers, arbitrary helpers and multiple branch-token birth sites remain allowed. The existing event-pair theorem controls pairs, not a bounded physical-event load on those general cases.

Thus no universal cost theorem is inferred. What remains is the original all-source U_int<=cA statement with a source-derived bounded-overlap work argument that does not restrict counting to the two endpoints. This report does not replace it by a new conjecture, ownership system, or TF2 repair.


## 13. Decisions, independent-verification status and limits

| Question | Mathematical result | Verification qualification |
|---|---|---|
| Original 97-key source and fifteen event pairs | AUDIT PASS under fresh symbolic reconstruction; K_{3,5} remains valid | Same agent as the producer; no separate-agent or external computational/formal certificate |
| Arbitrary p,q amplification | Proved by the full subtree induction and fixed-selector check in Sections 4–6 | New symbolic proof with self-review; independent review pending |
| Full-period A cost | Exact preparation, critical and restoration costs; rigorous forward bounds | Uniform scan upper bound imports the classical sequential-access theorem explicitly |
| All interior demands | Critical count exact; full count bounded between C_crit and C_crit+Q_forward | No claim to an exact reset U count or a generated event enumeration |
| Cost ratio | Uniformly Theta(1) on this family; no divergence | Family-specific, with the stated standard theorem dependency |
| Universal interior bound / Dynamic Optimality | Still OPEN | No special-family calculation is promoted to an all-source proof |

### 13.1 Separate check proposed, NOT executed

A fresh independent computational audit would materially strengthen the verification status of Stage 1, but is not authorized or run here. A concrete bounded check would:

* Construct two complete labelled 97-key BSTs at the specified right-vine diagonal and execute EXACTLY the 293 literal operations, using an independently written ordinary bottom-up rotation implementation.
* Log original operation/StepEv/bit IDs, complete subtree labels, both A/B endpoint trees and actual depths/costs.
* Reconstruct the FULL neutral creator forest, Pi windows, last A entries, original T_q routing and the fifteen selected event pairs; then verify the graph density.
* Check A absence at every actual intermediate snapshot, including the entire cyclic window, rather than only post-A states.

There are 293 A accesses and 197 B KEEP accesses. Each has at most 96 real rotations, so at most 47,040 real rotations need checking in this finite audit. Only two 97-key trees and finite label/event records are needed. This is a defined finite replay workload, not a claimed CPU-time measurement. It would still require separate authorization as a computational/source verification run; saying it can use an independent implementation does not exempt it from the restriction.

No source-engine queries, code execution of this proposed checker, experimental parameter enumeration, solver, or resource-cap change has occurred. A finite replay of Stage 1 would not itself verify the arbitrary-parameter induction.

### 13.2 Advancement record

**Before:** the TF2 report gave a symbolic 97-key refutation; its finite audit, parametric survival mechanism and complete A-cost implications had not been separated.

**Result:** the finite witness survives fresh derivation; an all-p,q dyadic variant produces genuine K_{p,q}; the full family has U_int=Theta(N) and A=Theta(N); critical demands have the explicit injective physical restoration-event map (10.2).

**After:** uniform arboricity and own-endpoint bounded-load approaches cannot be universal. This source mechanism supplies enough complete-period A work and gives no unbounded U_int/A family. The unrestricted cost theorem remains open at the global cohort-sharing obligation in Section 12.

**New assumptions:** none on the original admissible source domain. The restricted family deliberately has explicit shapes and operations. Its uniform scan-cost estimate uses the established sequential-access theorem; it does not assume the desired unrestricted U_int<=cA theorem.

**Net advancement:** graph density and physical work are now separated by a proved source family and explicit original work events. No new speculative closure premise is accepted.

## 14. Current inputs, preservation and resource record

Repository:
C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2.

Branch coarse-double-branch.
Current HEAD inspected: 6d532b2c795c0778f57d8023b23b5fedfc48b010.

This differs from the previous certificate's internal HEAD description. Current verified file bytes are authoritative. The old certificate SHA256 remains 1a56e2f4eb3023642979fae4ca93f73e9ad794bb1d982c9de5a018fef8cdf0a7.

The mandatory Route 02/04, C02–C09 and downstream reports retain their earlier full-read scopes and status qualifications; current byte pins below identify the actual versions used. Nothing in this report upgrades a symbolic inherited result to a proof-assistant or external certification.

Paths are relative to DO_RESEARCH_REBOOT.

| Input | SHA256 |
|---|---|
| PARALLEL_ROUTE02_STEP04_TF2_20261109/STEP04_TF2_BINARY_CERTIFICATION.md | 1a56e2f4eb3023642979fae4ca93f73e9ad794bb1d982c9de5a018fef8cdf0a7 |
| PARALLEL_ROUTE02_STEP04_LINEAR_INCIDENCE_20261108/STEP04_LINEAR_INCIDENCE_SOURCE_GEOMETRY.md | 77702f3cb914d36a62adb5ba7511c141d92068b52680138997aefc845349e11a |
| PARALLEL_ROUTE02_ALWAYS_ABSENT_20261108/STEP03_ALWAYS_ABSENT_FRAME_BOUND.md | a06eff982f350aff51d4004b6ea1739e62e254b13455d3f872c66c2d5ec2c837 |
| PARALLEL_ROUTE02_REUSE_RESTRICTION_20261108/STEP02_REUSE_RESTRICTION.md | d81f9abb7bf841c0661d55b8df7f2f6b2170b134287ccefb01e7682f28bc5e3f |
| PARALLEL_ROUTE02_ATTACHMENT_TRACE_20261108/STEP01_ATTACHMENT_TRACE.md | fc07769642f6b08f35f6d6cfdd45290f740772556d7ad754757eb94a3a9949b4 |
| ROUTE04_RELAXED_UNIVERSAL_CD_20261108/RELAXED_UNIVERSAL_CD_DISCOVERY_STEP01.md | f85354f04eed727e3bdc4c0ddca72c1a6f706885c35721ced525ee52fa26e712 |
| SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/STEP3_1B_NECESSITY_CONTINUATION_02.md | 9b784193b5d68bc0fc358ca09204ff4ebacb69ba1db0fabce422cf97ff98a1e3 |
| SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/STEP3_1B_NECESSITY_CONTINUATION_03.md | 00a004ec6f55fbe3e4e7bc8c4866782f428edbcbc40f1eb7c4903e46769e2059 |
| SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/STEP3_1B_NECESSITY_CONTINUATION_04.md | e247f175606d377ee359d89fce487e4985ab885726ef126abb35ccfde5c6e08d |
| SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/STEP3_1B_NECESSITY_CONTINUATION_05.md | 57261c7bc9e45579acd42c90862baf985bda6c3a4eb726d6773e03c8d0ad43e4 |
| SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/STEP3_1B_NECESSITY_CONTINUATION_06.md | 5899bf71ef7840589a5bf568ef56f0dec0267de1503a9dca2290a94a418a643f |
| SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/STEP3_1B_NECESSITY_CONTINUATION_07.md | f55e33760afefd41e1f69a62d3d1e8779dfbea361db76129f9d8a2dc2777cf50 |
| SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/STEP3_1B_NECESSITY_CONTINUATION_08.md | 454b4a2bcd61b1046edbc6962abff160841dc1983ea6ebc52924836c6021ed71 |
| SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/STEP3_1B_NECESSITY_CONTINUATION_09.md | 9ea0af9b61d08259ffd41a3e7c041e64a0bef36aa75ed34285bf89122d59a709 |
| 02_PROVED/C_ZIG_RECONSTRUCTED.md | dc1294a4d6bbef3db0aad2583323ea6e542cd18c192f0046309c1c8fe3c9aa56 |
| 01_MAIN_PIPELINE/stage_01_levy_tarjan.md | 07b4d66e672a83802684c4b4cced1af19f1acdb583906d5cedf138ac8a3843c6 |
| 01_MAIN_PIPELINE/stage_02_lt_bound.md | 2a38456b118878c8cf3977de5774ed179c39f943b743289ff2e59ca6ac5a7a93 |
| 11_REPRODUCIBILITY/L3_local_extracted.txt | 2981e5017d68d358e8e4a3591bc703172e4177ea048252f6accc8862a6af5bfd |
| SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/UNIVERSAL_GLOBAL_FUNDING_11/resources_checkpoint.json | 76c8be7af7b580a06f659c3147b6090968aac7e5cc9e7c77001afb46654dce10 |

One primary-paper metadata/abstract read confirmed the classical sequential-access theorem already identified in the local bibliography: R. E. Tarjan, Combinatorica 5 (1985), 367–378, DOI 10.1007/BF02579253. It is recorded separately from source-engine activity. No fresh literature claim of Dynamic Optimality is made, and the subscription proof was not newly reconstructed in full.

All newly written files are confined to this isolated continuation folder. Historical reports, original sources, certificates, owners, resource files and Routes 01/03/04 are unchanged. No Git mutation is performed.

No unauthorized source-engine query, semantic replay job, computational proof run, solver/state search, enumeration, generated-source experiment or new potential is used. The family is proved symbolically from literal rotations, as authorized; it is not an experimentally sampled source family.

The inherited resource checkpoint remains unchanged: global CPU 6394.71875/7200; symbolic 2452.375/2640; independent 740.96875/750; source queries 3050330/3100000; batch 50000; Bank25 25. Those are historical checkpoint values, not a new concurrent aggregate. No allowance is reset or increased.

The explicitly requested repository report contains the durable derivations. Repository-recoverable proof content is not duplicated into Notion.
