# Route 02 — Step 4 linear-gap audit

Date: 2026-11-08.

**Requested result: close the linear gap for always-A-absent frames.**
**Actual result: NOT CLOSED.** The source argument needed for that conclusion has not been obtained.

**Outcome F for the direct certificate-to-unit payment rule.** A pinned, original paired-closed CCR source refutes that rule even for g1-residual always-absent producer-silent histories. This does not refute a general linear theorem or Universal CD.

No new weaker cost bound is offered as closure. No new numbered step is introduced.

## 1. Exact target and retained source

Continue from STEP03_ALWAYS_ABSENT_FRAME_BOUND.md and SIX_STEP_SEQUENCE.md. Preserve the original paired-closed source W, full-B KEEP-only semantics, ordinary A accesses, original support S, SET labels, physical event IDs, lambda, g1, owners, periods and costs.

For a neutral demand d the always-absent condition is

    W_d not in J_S(A) throughout Pi_d=(kappa_d,t_d^A].

Step 3 provided an injection into ORIGINAL EVENT PAIRS

    d -> (beta(d),tau(d)),

or into an A-entry/B-decrease pair plus one of three roles. It did not give distinct available A units. The exact new obligation is a source-derived linear restriction with original event multiplicities, rather than another product count or a relabelled residual inequality.

STEP04_SCOPE_BEFORE.md fixes the bounded linearization attempt before this audit. No source query, replay, experiment, solver/state search or new potential is used. All concrete evidence below is a static read of existing saved annotations, with symbolic rotation reasoning.

## 2. Timing fact checked: a shared LAST entry has one B consumer

The Step 3 selector beta(d) is the LAST A global-root entry into the physical span of W_d after Gamma_d and before its producer's post-A snapshot.

Suppose two histories share beta. Their current B frame labels contain the new A root, or the same adjacent carrier key for a private new root, so the labels are nested. Write W_1 contained in W_2.

After its last entry beta, A's global root cannot leave span(W_1) before its consuming A snapshot: an exit followed by the necessary return would make a later entry. The first B hit of W_2 occurs no later than that of W_1. If it occurred strictly earlier, its target would have to be outside W_1; otherwise it would also first-hit W_1. Its A-root snapshot would then be outside span(W_1), contradicting last-entry persistence.

Therefore both frames have the SAME actual first B-consumer access. The argument uses their current runs and the first future consumers after the shared event, so it also respects a cyclic seam.

This removes a possible ambiguity in the entry groups. It does not prove a linear supply of available units: one consumer access can still contain several neutral doubles, and source tokens can recur at different entry groups.

## 3. Proposed graph linearization and the missing source implication

Define the bipartite graph G from the fixed Step 3 association:

    left vertex:  a distinct original entry rotation beta;
    right vertex: a tagged original root/branch event tau;
    edge:         an original always-absent demand d.

Pair injectivity makes this a SIMPLE graph. Its number of edges is |U|. There are E left vertices and at most r+K right vertices.

If this graph were an UNDIRECTED FOREST, the forest edge bound would give

    |U| <= E+r+K
         <= 7A(W),

using the earlier E<=2A, r<=4A and K<=A. This would be a linear counted-work estimate. It would still need availability/owner analysis before becoming a payment theorem.

No proof that the actual source forces this undirected-forest property has been obtained.

In particular, acyclicity of the separate N8 CREATOR FOREST does not imply acyclicity after histories are identified by repeated entry and token coordinates. Chronological direction of edges does not prove undirected acyclicity either.

### 3.1 Exact logical failure of the forest-only inference

The following is an abstract graph argument, NOT a newly generated source or a CD counterexample.

Take n disjoint directed paths, each with n nodes d_(i,1),...,d_(i,n). Give every node on path i the inherited root token tau_i, and give its j-th node entry name beta_j.

Each beta group is an antichain in this creator forest. Each (beta,tau) pair is unique. There are no branching nodes, so the at-most-one-branch-per-access statement is automatically satisfied. Entries may be labelled with one consumer access per beta group.

The resulting incidence graph is the complete bipartite graph K_(n,n). It has n^2 edges and 2n vertices. Already n=2 gives an undirected four-cycle.

Thus the listed combinatorial facts from Step 3 do not imply incidence-graph acyclicity or a universal constant edge/vertex ratio. Additional ORIGINAL SOURCE GEOMETRY would have to exclude or pay such patterns.

This construction is not asserted to satisfy all BST rotation/source constraints. It only rejects the inference from the named abstract facts. It cannot refute a source-specific acyclicity theorem; that theorem remains unproved. Treating this countermodel as an actual source would be invalid.

## 4. Exact original-source refutation of the direct payment rule

There is a stronger, source-valid obstruction to simply choosing a certificate coordinate as the new payment.

Use the existing CCR source in

    C/CONTINUATION_04/cluster_collateral_closed_source.json,

with original period [51,68], one actual word copy. Here C is SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35 under DO_RESEARCH_REBOOT.

The carrier is S=[13]. A's period targets are all odd keys. The nonaccessed even keys remain physical leaves, and are not private or erased. The source has original A=23, Q_B=22; its scalar slack is 24. It is a solvent, reachable paired-closed control, not a counterexample to Universal CD.

### 4.1 Two actual always-A-absent frames

Let

    d1=(68,1), W_1=[1,3], I_1=[2,3];
    d2=(68,2), W_2=[1,7], I_2=[2,7].

Both doubles are neutral. Their original producer is 1. Their whole frames and designated outputs follow directly from the saved B path for KEEP1 at 68.

At the source boundary A, 3 is an ancestor of leaf 4, and 7 is an ancestor of leaf 8. A never accesses 4 or 8 in the period. A leaf is never an ordinary splay-path operand unless accessed, so these leaves never rotate.

For adjacent physical keys 3,4, removing ancestor 3 from the path to 4 would require promoting 4 across 3; there is no intervening physical key. That cannot happen here. The same reasoning applies to 7,8. Hence A keeps

    3 ancestor of 4,   7 ancestor of 8

throughout all intermediate A rotations of the period.

Any A subtree containing 3 contains 4; any A subtree containing 7 contains 8. Therefore [1,3] and [1,7] are NEVER A labels in this period. In particular both satisfy the full Pi-window always-absent condition. Their outputs [2,3] and [2,7] are also never A-acquired.

The saved histories have producer-silent output attachment intervals: the producer flags are false during their initial birth attachments in the K1 B phase, and true from their later reverse attachments through their first hits. No producer-child A transition supplies a zero event in these intervals.

### 4.2 Original creation/removal IDs

| History | Last B frame creator Gamma | Previous B frame removal kappa | Consuming access |
|---|---|---|---|
| d1 | B(57,2,0), neutral half of B1 double (57,2) | Previous cyclic occurrence of B(68,2,1) | K1 at 68 |
| d2 | B(67,3,0), neutral half of B1 double (67,3) | B(57,3,1) | K1 at 68 |

The later first removal of W_1 in the consuming B phase is B(68,2,1). The later removal of W_2 is B(68,3,1). These are original slots; wrapping kappa_1 across the display seam adds no source copy or work.

The saved PC35 annotation for access 68 explicitly gives

    B0=2, B1=1, B2=0, Z=0,
    residual_demands=[(68,1),(68,2)].

Thus d1 and d2 are genuinely in the original g1-residual F. They are not merely examples of neutral demands already paid by g1.

No assertion is made that these two demands remain unpaid after every later alternative comparison, including the inherited FAR results. The counterexample below is exactly to vacancy under g1 and to the proposed certificate-coordinate rule.

### 4.3 Their A entries are already occupied

The single A LL double at access 68 is

    A(68,1,0): right 11 -> 7, positive;
    A(68,1,1): right 7 -> 1, positive.

The first rotation enters span([1,7]); the second enters span([1,3]). The original last-entry selectors are therefore

    beta(d1)=A(68,1,1),
    beta(d2)=A(68,1,0).

The preserved raw g1 map in release_completion_controls.json records

    g1(68,3)=A(68,1,1),
    g1(58,3)=A(68,1,0).

Both proposed entry units are already occupied by existing full claims. Both are outside R1=C_A minus im(g1).

The exact false source implication is therefore

    d in F, I_d unacquired and producer-silent,
    W_d A-absent throughout Pi_d
       ==> own(beta(d)) in R1.                        FALSE.

Both d1 and d2 refute this implication in the original source.

There is no extra virtual unit at this A StepEv: it is a double with two real rotation bits, not a terminal zig.

### 4.4 The root companion decreases are occupied too

Each of d1 and d2 is a root of the N8 forest: its Gamma is the neutral half of a NONNEUTRAL B1 double. The Step 3 token is that root creator, so the associated companion decreases are

    delta_1=B(57,2,1),
    delta_2=B(67,3,1).

The original positive heads and owners are:

| Proposed coordinate | Original A unit | Preserved g1 owner |
|---|---|---|
| Entry for d1 | A(68,1,1) | (68,3) |
| Companion decrease head for d1 | A(57,1,0) | (57,2) |
| Entry for d2 | A(68,1,0) | (58,3) |
| Companion decrease head for d2 | A(62,2,0) | (67,3) |

The two companion slots are the first/only decreases of their B1 doubles. Their lambda heads pay those doubles. Calling the neutral half a root token does not release its companion payment.

Consequently the candidate relation

    d -> one available unit in
         { own(beta(d)), lambda(delta_root(d)) }

has NO R1 neighbour for either of these two g1-residual demands while preserving g1. This is an exact original-source refutation of that restricted payment mechanism.

It does not show that the source has no other unused units. The whole source is solvent. Other original negative, zero, virtual or unselected-release contributions remain in the original account.

### 4.5 Why the control does not settle the unrestricted gap

The source refutes a specified direct payment rule, not every possible source-derived linear restriction. A later FAR comparison may already cover these histories by another certificate. Any universal Step 4 proof must retain that coverage and all its actual costs/owners.

No critical access is extracted as closed. The negative local price at 68 is not a CD counterexample; all original DELETE accesses, earlier KEEPs, reachability and resets remain present.

No A event is counted twice. The four occupied A units in the table keep their original g1 owners.

## 5. What can and cannot be concluded

Established in this audit:

* A shared last-entry group has one first B consumer.
* The incidence-forest criterion would imply a linear counted-work bound, but it has not been proved from the source.
* The N8 forest/antichain/pair-injection facts alone do not imply that criterion.
* The direct projection to the entry unit or root companion head is refuted on original g1-residual always-absent histories, with exact physical IDs.

Not established:

* an unrestricted source-derived linear bound closing the always-absent case;
* a globally injective map of that class into available original A units;
* a proof that all remaining always-absent histories are already covered elsewhere;
* Universal CD.

The residual equation |R_H|-|U_H|=2A-Q_B is not used to assert its own sign. No new matching premise, source potential, cap increase or hypothetical donor is introduced.

## 6. Outcome and obligation status

**BEFORE:** Step 4 required a source theorem converting event-pair certificates into linear non-overcounting work/payments.

**RESULT:** the proposed direct payment conversion fails exactly. The graph alternative needs an independent source sparsity theorem that is not supplied by the current facts.

**AFTER:** the requested mathematical closure has not been achieved. This is a failure of the attempted proof, not a proof of insolvency or impossibility of a future linear theorem.

**NET ADVANCEMENT:** an exact rejection of this closure mechanism and a precise identification of its missing premise. This is not reported as completion of Step 4 or as another successful weaker bound.

**Outcome F applies to the mechanism, not Universal CD. Step 4 is NOT CLOSED.**

The requested closure has not been achieved. No mathematical status, fixed owner or step number has been changed to suggest otherwise.

No further open mechanism is launched within this audit. The original mathematical obligation retains the number 4.

## 7. Planned steps 5 and 6

5. Handle near-side endpoints jointly: attached epsilon_C and unattached P_free, with persistent-blocker and always-absent histories included.
6. Establish global composition: preserve one coherent base comparison and resolve all physical-event intersections and fixed owners before counting.

Neither is executed here. They remain the next named stages, but the Step 4 linear gap cannot be assumed solved when proving them or claiming Universal CD.

## 8. Read-only provenance and preservation

Repository branch: coarse-double-branch.
HEAD observed at final inspection: ca8e9456e1508afb15641f7e1684f1d00f1a3f6c. Earlier reports record 8c378d49283b3738b18e7175886772a98025e4e9; no commit or checkout operation was performed by this work.

The three pinned CCR inputs below are historical artifacts, read statically without executing their engines:

| Input under C | SHA256 |
|---|---|
| CONTINUATION_04/cluster_collateral_closed_source.json | 9bdacf3235d8fa3a47c27e814ee587713daf09d6823651c87f0f425f81afee7a |
| ND35_COMPLEMENT_08/lifetime_controls.json | 3b1b603a02a64ef41688f079a646702e7f815da099bad76e52e10386348dac3f |
| PC35_RELEASE_COMPLETION_09/release_completion_controls.json | 67884ea4bfc83ac6dd27fc4c1a3d97560d96b5b293027f8d27c74e77fd1cf27c |

Authoritative preceding report:
PARALLEL_ROUTE02_ALWAYS_ABSENT_20261108/STEP03_ALWAYS_ABSENT_FRAME_BOUND.md
SHA256 a06eff982f350aff51d4004b6ea1739e62e254b13455d3f872c66c2d5ec2c837.

All new deductions have symbolic self-review only; independent/formal audit is pending. Cached owner values and fine-step IDs are quoted at their existing recorded scope. No historical status is upgraded.

Only this new isolated audit folder is written by this work. No writes to earlier reports, original sources, owner maps, Routes 01/03, resource records or Git are performed. The pinned mathematical input hashes match their inspected originals; the current HEAD is recorded above without attributing the separate repository update. No mathematical/source query, source replay, experiment, solver/state search, new potential or verification phase is run.

The inherited resource checkpoint remains global CPU 6394.71875/7200; symbolic 2452.375/2640; independent 740.96875/750; source queries 3050330/3100000; batch 50000; Bank25 25. No allowance is reset/increased, no exhaustion is claimed, and no new semantic phase is charged under the inherited metadata convention.

This is repository-recoverable research and is not duplicated into Notion.

