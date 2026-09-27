# SPLAY-AM-DECIDE v0.4: Universal Pair-Access Closure and Dynamic-Optimality Decision Program

**Document type:** Frozen mathematical implementation specification / preregistration blueprint  
**Authoring status:** `PRE_FREEZE_PARENT_PIN_REQUIRED` — the scientific design is complete, but the normative v0.4 freeze occurs only after Phase 00 pins the final sealed v0.3 commit, FINAL_RESULT, manifest, archive, theorem-status ledger, survivor record, and normative hashes. No Phase 01+ theorem-facing execution is permitted before that pin.  
**Target problem:** Sleator–Tarjan Dynamic Optimality Conjecture for ordinary bottom-up Splay  
**Primary positive route:** frozen Pair-Access survivor `MSTC-0002 = (P_all,k=6,C=2)` → universal locality / preservation / boundary / injection / KEEP repayment / integrability / constant-independence → Pair Access → approximate monotonicity → audited Levy–Tarjan bridge → Dynamic Optimality  
**Primary negative route:** exact obstruction to the positive route → obstruction lifting → explicit legal real-Splay family + explicit competing BST execution → unbounded `Splay/OPT` ratio → Dynamic Optimality disproof  
**Experiment short name:** `SPLAY-AM-DECIDE-v0.4`  
**Primary parent experiment:** `SPLAY-AM-MST-v0.3`  
**Parent navigation commit:** `353ee92` — Phase 00 must replace this navigation hash by the exact full 40-character sealed commit read from the cloned parent repository and verify all final-seal artifacts by hash.  
**Parent terminal claim:** `TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS`  
**Immutable imported positive object:** `MSTC-0002`, frozen tuple `(P_all,k=6,C=2)`, the unique v0.3 fresh-H3T + clean-room + large-n survivor  
**Primary scientific mutation:** stop searching for transfer calculi; freeze the surviving calculus and attack the complete mapped theorem blocker set from both proof and refutation directions until either the positive theorem chain closes, a genuine negative Dynamic-Optimality certificate closes, or the experiment ends with an explicit no-claim obstruction/resource status  
**Primary implementation languages:** Python for exact executable semantics, falsification, certificate generation, audits, and reproduction; Lean 4 for theorem-critical formalization; Rust permitted only for acceleration behind exact-agreement gates  
**Experimental style:** deterministic, exact, theorem-led, certificate-first, dual prove/refute, formal-kernel checked, hostile-review gated, obstruction-preserving, fail-closed, no finite-premise theorem upgrades  
**Number of implementation phases:** 20 (`PHASE 00` through `PHASE 19`)  
**Core rule:** YES or NO are the only *successful* terminal outcomes. The implementation may still terminate honestly at `RESOURCE_LIMIT_NO_CLAIM`, `POSITIVE_ROUTE_REFUTED_NO_DOC_NEGATIVE`, `BRIDGE_BLOCKED_NO_CLAIM`, or another explicitly preregistered no-claim level. The system is forbidden to manufacture a binary theorem result merely because the experiment was designed as a decision assault.

---

# 0. Executive purpose

`SPLAY-AM-MST-v0.3` changed the state of the problem.

It did not prove Dynamic Optimality. It did something narrower and operationally decisive: it searched a frozen local transfer language, froze three development survivors, spent a genuinely fresh transfer holdout exactly once, killed two of the three candidates with exact fresh counterexamples, and left one calculus standing:

```text
MSTC-0001 = (P_all,  k=2, C=2)  -> FRESH_H3T_FAIL, max residual 8
MSTC-0002 = (P_all,  k=6, C=2)  -> FRESH_H3T_PASS, max residual 0
MSTC-0003 = (P_keep, k=1, C=6)  -> FRESH_H3T_FAIL, max residual 23
```

The survivor then passed independent replay, clean-room reconstruction, mutation controls, and large-`n` adversarial falsification through the v0.3 ceiling `TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS`. The sealed parent execution record further produced an arbitrary-`n` author proof claim for bounded DELETE injection (`MST0-13`) while leaving the universal KEEP / integrability / Pair-Access chain honestly open.

The battlefield is therefore no longer an unspecified search over potentials or transfer calculi.

The exact positive blockers of `UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED` are mapped:

```text
MST0-08U  universal reference locality                 universal form open
MST0-09   raw boundary law                             UNPROVED
MST0-11   transfer preservation                        UNPROVED
MST0-13   bounded DELETE injection                     PROVED author claim, human review pending
MST0-14   synchronous KEEP repayment                   UNPROVED
MST0-15   global integrability                         UNPROVED
MST0-22   constant independence                        UNPROVED
MST0-17   Pair-Access composition                      BLOCKED on 13/14/15 (+ required guards)
MST0-18   telescoping / approximate monotonicity       BLOCKED on 17
MST0-19   Levy-Tarjan bridge                           BLOCKED on 18 + exact L2/L3 premise bytes
```

The decisive v0.4 mutation is therefore:

> **Freeze MSTC-0002 and the mapped blocker DAG. For each unresolved theorem, simultaneously build the proof and attack its negation. Do not search for a replacement calculus inside the experiment. If the positive route dies, immediately attempt to lift the exact obstruction into a genuine Splay-vs-OPT negative theorem.**

The end-to-end positive chain is frozen as:

```math
\boxed{
\text{sealed v0.3 survivor MSTC-0002}
\to
\text{MST0-08U/09/11/13/14/15/22 REVIEWED}
\to
\text{MST0-17 REVIEWED}
\to
\text{MST0-18 REVIEWED}
\to
\text{MST0-19 REVIEWED}
\to
\text{UNIVERSAL PAIR ACCESS}
\to
\text{APPROXIMATE MONOTONICITY}
\to
\text{DYNAMIC OPTIMALITY}
}
```

The negative chain is frozen as:

```math
\boxed{
\text{exact universal obstruction to MSTC-0002 or positive bridge}
\to
\text{closed-form obstruction family}
\to
\text{legal real Splay sequences }(T_m,X_m)
\to
\operatorname{Splay}(X_m,T_m)\ge g(m)
\to
\text{explicit BST competitor cost}\le f(m)
\to
\frac{g(m)}{f(m)}\to\infty
\to
\text{DYNAMIC OPTIMALITY DISPROVED}
}
```

No weaker negative signal is enough.

The experiment is allowed to end with a precisely localized mathematical obstruction. Such an ending is scientifically valid but is not labeled a successful YES/NO resolution.

---

# 1. Scientific scope and central question

## 1.1 Primary scientific question

The central question is now literal:

```math
\boxed{\textbf{Is ordinary bottom-up Splay dynamically optimal?}}
```

The primary positive subquestion is:

```math
\boxed{
\text{Does the exact frozen calculus }MSTC\text{-}0002=(P_{all},k=6,C=2)
\text{ satisfy the complete arbitrary-}n\text{ theorem chain needed for Pair Access?}
}
```

The primary negative subquestion is:

```math
\boxed{
\text{If that chain fails, can the exact obstruction be lifted to a closed-form real-Splay family with unbounded }Splay/OPT?
}
```

## 1.2 No more calculus discovery

v0.4 is not permitted to search the old grammar for a different `P`, different `k`, different `C`, different credit type, or different active predicate.

Hard rule:

```text
MSTC-0002 is immutable experimental input.
```

Any modification of its theorem-facing fields is a new experiment ID and cannot be used to claim v0.4 closed the mapped route.

This includes:

```text
P_all -> another predicate
k=6 -> any other k
C=2 -> any other C
support semantics
injection sites
transfer/cancellation semantics
scale semantics
mapping semantics
ledger energy semantics
```

## 1.3 Why this experiment is theorem-first

Finite falsification has already done its job.

v0.4 may generate arbitrarily vicious finite stress families, but those families have only two permitted logical roles:

```text
1. REFUTATION: one exact legal witness can falsify a universal candidate lemma.
2. THEOREM MINING: repeated obstruction patterns may suggest a proof lemma.
```

They may never play the role:

```text
3. PROOF: no finite survival count proves a universal statement.
```

## 1.4 Positive theorem target

The desired exact Pair-Access form is:

```math
\boxed{
\operatorname{Splay}(Y,T)
\le
2\operatorname{Splay}(X,T)+A(n)
\qquad
\forall T,\forall X,\forall Y\preceq X
}
```

where `A(n)=0` is preferred. A nonzero additive term is permitted only if:

```text
- its exact formula is proved;
- it is independent of sequence length;
- its dependence on n is explicit;
- the exact frozen Levy-Tarjan bridge accepts it;
- no terminal-energy deficit is hidden inside it.
```

## 1.5 Constant policy

Unlike v0.3, v0.4 does **not** run a diagnostic constant ladder for the positive route.

The imported primary theorem candidate is bound to:

```text
C = 2
k = 6
P = P_all
```

`MST0-22` must prove that these constants are independent of:

```text
n
sequence length
initial tree
subsequence choice
proof decomposition
finite corpus
holdout bank
search generator
solver state
```

If the exact frozen calculus cannot be proved at these constants, the positive route is refuted for MSTC-0002. v0.4 may not silently relax `C` or `k` and continue under the same scientific claim.

## 1.6 Only YES / NO count as successful terminal outcomes

Successful positive terminal claim:

```text
DYNAMIC_OPTIMALITY_PROVED
```

Successful negative terminal claim:

```text
DYNAMIC_OPTIMALITY_DISPROVED
```

Allowed honest non-success terminal levels include:

```text
BOUNDED_DELETE_INJECTION_PROVED
UNIVERSAL_LOCALITY_PROVED
TRANSFER_PRESERVATION_PROVED
RAW_BOUNDARY_LAW_PROVED
SYNCHRONOUS_KEEP_TRANSFER_PROVED
GLOBAL_INTEGRABILITY_PROVED
UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED
APPROXIMATE_MONOTONICITY_PROVED
MSTC0002_UNIVERSAL_COUNTEREXAMPLE
POSITIVE_ROUTE_REFUTED_NO_DOC_NEGATIVE
BRIDGE_BLOCKED_NO_CLAIM
RESOURCE_LIMIT_NO_CLAIM
```

These are scientifically meaningful but are not counted as v0.4 success.

## 1.7 Non-goals

v0.4 does not claim:

```text
- that MSTC-0002 is already an invariant theorem because it survived v0.3;
- that k=6 is minimal;
- that failure of k=2 proves a six-way combinatorial bound;
- that a K6 saturation search proves a six-way bound merely by failing to find seven claims;
- that a local repayment proof implies global integrability;
- that a Pair-Access failure implies Dynamic Optimality is false;
- that an obstruction to one proof route is an OPT lower bound;
- that a proof assistant replaces mathematical review;
- that human review replaces formal checking;
- that formal checking validates an incorrectly stated theorem;
- that the Levy-Tarjan bridge can be consumed before exact source identity and convention match are frozen;
- that external current literature can silently modify the preregistered theorem DAG;
- that resource exhaustion is evidence for either YES or NO.
```

---

# 2. Parent lineage and immutable inherited evidence

## 2.1 Primary parent

```text
experiment_id: SPLAY-AM-MST-v0.3
repository: Dynamic-Optimality-Lab/splay-multiscale-transfer
navigation_commit: 353ee92
sealed_commit: TO_BE_PINNED_FULL_SHA_FROM_PARENT_PHASE19
terminal_claim: TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS
```

Phase 00 must read the authoritative final seal and replace every navigation identity by the exact sealed artifact identity.

## 2.2 Earlier ancestors

The v0.4 parent importer must verify the complete inherited chain, including at minimum:

```text
SPLAY-AM-BD-v0.2
  sealed commit from v0.3 parent import record
  terminal FINITE_DEBT_LAW_MINING_RESULTS

SPLAY-AM-PD-v0.1
  sealed commit 6de1ca2a595e8895f54794f3a211fe6ee1a95a80
  terminal FINITE_EXACT_BN_RESULTS
```

## 2.3 Certified v0.3 facts expected for import

Expected but not trusted until hash-verified from the parent seal:

```text
- WP-0..WP-6 all completed and sealed.
- FINAL_RESULT terminal claim TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS.
- MSTC-0002 is the standing frozen primary survivor.
- MSTC-0002 = (P_all,k=6,C=2).
- MSTC-0001 fresh H3T fail: max residual 8; first witness n=32 idx=4406.
- MSTC-0003 fresh H3T fail: max residual 23; first witness n=16 idx=3610.
- MSTC-0002 fresh H3T pass: 70,000/70,000, max residual 0.
- clean-room and independent replay agreed.
- large-n v0.3 falsification reported 0 exact-replayed kills on MSTC-0002.
- v0.3 lifecycle at seal: REVIEWED 10 / PROVED 4 / NOT_APPLICABLE 3 / BLOCKED 3 / UNPROVED 6.
- MST0-13 carries an arbitrary-n author proof claim and pending human review package.
- MST0-14 and MST0-15 have no universal proof in the parent.
- MST0-17/18/19 are blocked.
- MST0-08 is reviewed only in scoped-finite form; the universal form remains gapped.
- MST0-09, MST0-11, MST0-22 remain unproved on the positive path.
```

## 2.4 Parent facts are evidence, never editable inputs

v0.4 may:

```text
verify hashes
vendor/copy exact sealed theorem statements by hash
import the exact MSTC-0002 record read-only
import counterexamples read-only
import review packages read-only
replay exact parent evidence
construct new v0.4 proof/refutation artifacts with explicit parent provenance
```

v0.4 may not:

```text
rewrite a v0.3 artifact
change an inherited status in the parent repository
repair a v0.3 proof in place
replace MSTC-0002 with a recomputed equivalent without preserving the sealed record
change the parent FINAL_RESULT
remove the two fresh sibling failures
reinterpret a finite parent pass as a universal theorem
```

Any mismatch emits:

```text
PARENT_SEAL_MISMATCH
```

and blocks theorem-facing execution.

## 2.5 Parent Path.md is part of the audit inheritance

The final parent `Path.md` is imported read-only by hash because it records implementation reality, including repaired bugs, lifecycle decisions, fresh-bank one-unlock history, seal determinism, and the explicit universal-proof frontier.

It is historical evidence, not a theorem premise.

---

# 3. Frozen literature and theorem-premise sources

v0.4 freezes the exact literature actually used as a theorem premise before any bridge theorem is consumed.

Required source set:

```text
L0  SPLAY-AM-MST-v0.3 final sealed release
L1  Sleator & Tarjan, Self-Adjusting Binary Search Trees, JACM 1985
L2  Levy & Tarjan, A New Path from Splay to Dynamic Optimality, SODA 2019
L3  Levy & Tarjan, A Foundation for Proving Splay is Dynamically Optimal, exact frozen version
L4  Chmel et al. 2026, exact v0.3-frozen version, context/translation only unless separately promoted
```

Hard mutation relative to v0.3:

```text
MST0-19 may not leave PENDING because the source bytes are unavailable locally.
```

Phase 02 must either:

```text
A. acquire lawful exact bytes for the precise L2/L3 versions and hash-freeze them; or
B. freeze an authoritative publisher/arXiv artifact representation accepted by the spec, with exact theorem text captured and hash-bound; or
C. emit BRIDGE_SOURCE_UNAVAILABLE and block the positive final theorem branch.
```

No “bibliographic identity is probably enough” shortcut is permitted for a theorem-facing bridge premise in v0.4.

For each premise source store:

```text
source_id
canonical citation
exact theorem/lemma identifiers
exact version/date
retrieval method
retrieval UTC timestamp
SHA-256 or immutable authoritative artifact identity
verbatim theorem statement within copyright-safe internal research storage
hypotheses actually used
logical role
```

---

# 4. Frozen Splay / Pair-Access / survivor contract

All ordinary Splay and Pair-Access semantics are inherited by hash from v0.3.

Key universe:

```math
[n]=\{1,\dots,n\}.
```

Cost:

```math
c(T,x)=\operatorname{depth}_T(x)+1.
```

KEEP:

```math
(A,B)\mapsto(S_xA,S_xB),\qquad a=c(A,x),\quad y=c(B,x).
```

DELETE:

```math
(A,B)\mapsto(S_xA,B),\qquad a=c(A,x),\quad y=0.
```

For MSTC-0002:

```math
w(e)=y(e)-2a(e).
```

The imported calculus record, not prose, defines:

```text
P_all
k=6
injection sites
support semantics
credit lifecycle
transfer/cancellation/payment operations
scale semantics
energy/flow statement
```

v0.4 code may wrap or formalize those definitions but may not semantically mutate them.

---

# 5. Formal proof kernel contract

## 5.1 Proof assistant

v0.4 uses one frozen Lean 4 toolchain.

Phase 00 records:

```text
Lean version
elan/toolchain identity
mathlib commit/hash if used
lake-manifest hash
all custom axiom declarations
```

No theorem-critical declaration may depend on an untracked `axiom`, `sorry`, `admit`, unsafe theorem escape, generated proof hole, or external oracle result without a separately checked certificate.

## 5.2 Formalized core objects

The Lean core must contain or faithfully import definitions for:

```text
finite totally ordered key sets
BST validity
ordinary bottom-up Splay
ROOT/ZIG/LL/RR/LR/RL
cost depth+1
Pair-Access KEEP/DELETE
subsequence relation
rotation trace refinement
MSTC-0002 ledger state
credit support and mass
T5/T6/T7 semantics actually used by MSTC-0002
energy/flow quantities
block partition
all positive-path theorem statements
```

## 5.3 Three-layer theorem certificate

For each theorem-critical positive node:

```text
Layer A: human-readable mathematical proof
Layer B: Lean theorem or kernel-checkable exact certificate
Layer C: hostile refutation attack against the theorem's exact negation
```

A theorem may become `PROVED` only if A and B are complete and C has no exact counterexample.

A theorem becomes `REVIEWED` only after a human ACCEPT record audits the statement, dependencies, cases, formal binding, and objections.

## 5.4 Formalization is not semantic authority by itself

If the Lean statement differs from the frozen mathematical statement, the result is:

```text
FORMALIZATION_MISMATCH
```

not a proof.

---

# 6. Frozen positive theorem battlefield

Exactly the following unresolved theorem nodes are on the v0.4 positive critical path.

```text
MST0-08U  universal reference locality
MST0-09   raw boundary law
MST0-11   transfer preservation
MST0-13   bounded DELETE injection
MST0-14   synchronous KEEP repayment
MST0-15   integrability / decomposition independence
MST0-22   constant independence
MST0-17   universal Pair-Access composition
MST0-18   telescope / approximate monotonicity
MST0-19   Levy-Tarjan bridge
```

No new mathematical prerequisite may be silently inserted into the critical path after Phase 00.

A newly discovered intermediate lemma is allowed only if:

```text
- it is explicitly registered as a child lemma of one of these frozen nodes;
- its statement is versioned;
- it does not relax the parent theorem;
- its proof/refutation artifacts are retained;
- its introduction does not alter MSTC-0002.
```

The downstream target remains Phase 18 theorem activation.

---

# 7. Dual theorem obligation contract

Every unresolved node `L` maintains two simultaneous research objects:

```text
PROVE(L)
REFUTE(L)
```

`PROVE(L)` may use only reviewed upstream theorems and frozen definitions.

`REFUTE(L)` searches for a legal witness satisfying the exact negation of `L`.

Status namespace:

```text
UNPROVED
PROVED
REVIEWED
REFUTED
BLOCKED
NOT_APPLICABLE
```

Allowed lifecycle:

```text
UNPROVED -> PROVED -> REVIEWED
UNPROVED -> REFUTED
PROVED   -> REFUTED   only if the alleged proof is broken before REVIEWED
```

A `REVIEWED` theorem may be overturned only by a versioned erratum process that preserves the old review and exact counterexample/proof defect. Downstream results are then invalidated by dependency hash.

No theorem status may be changed merely because a test suite is green.

---

# 8. Proof Stress Corpus (PSC)

## 8.1 Purpose

The PSC is not a holdout and never proves a theorem.

It is a preregistered adversarial battery generated from theorem negations to force proof discovery toward the hardest known configurations.

## 8.2 Frozen PSC families

```text
PSC-L   LOCALITY_EXPLOSION
PSC-P   PRIMITIVE_PRESERVATION_EXHAUSTION
PSC-B   BOUNDARY_TORTURE
PSC-K6  K6_SATURATION
PSC-I   DOUBLE_SPEND_APOCALYPSE
PSC-T   TELESCOPE_ENDPOINT_TORTURE
PSC-N   NEGATIVE_OBSTRUCTION_LIFTING
```

## 8.3 No theorem by survival

Allowed:

> The proposed theorem survived the declared PSC attacks.

Forbidden:

> The PSC proves the theorem.

## 8.4 Attack records

Each PSC attack stores:

```text
theorem_id
negation predicate
generator version
seed / symbolic parameter family
input hash
exact witness if found
objective vector
best finite obstruction metrics
replay certificate
independent checker result
scientific interpretation
```

---

# 9. MST0-08U universal locality: Locality Explosion Engine

The finite v0.3 locality result is already reviewed only in scoped form. v0.4 must prove or refute the exact arbitrary-`n` locality statement required by MSTC-0002.

## 9.1 Frozen stress objectives

The Locality Explosion Engine maximizes, independently and lexicographically where applicable:

```text
reference-support radius
number of changed translated primitives after one A rotation
provenance descendant count
number of simultaneously touched scales
number of boundary objects whose ownership changes
heap/lazy dependency depth
support descriptor span
```

## 9.2 Required theorem form

The exact theorem statement is imported from the v0.3 MST0-08 universal gap and then frozen in v0.4 Phase 00.

The proof must establish a universal constant bound on exactly the primitive modifications consumed by MST0-14/15.

It may not prove a weaker neighborhood statement and silently substitute it.

## 9.3 Refutation form

An exact legal family showing any required locality quantity grows unboundedly with `n` refutes MST0-08U as stated.

Such a refutation kills the current positive proof route unless the theorem statement consumed by MST0-14/15 is proven under a versioned logically sufficient replacement that was preregistered as an allowed child lemma family.

---

# 10. MST0-11 transfer preservation: symbolic primitive exhaustion

## 10.1 Objective

Prove that every legal primitive update of MSTC-0002 maps a well-formed ledger to a well-formed ledger and preserves all invariants required downstream.

## 10.2 Symbolic cases

At minimum:

```text
ROOT
ZIG-left
ZIG-right
LL
RR
LR
RL
```

Each case is parameterized by arbitrary legal subtree intervals/sizes/ranks/supports rather than finite concrete trees.

## 10.3 Preservation obligations

For every primitive:

```text
BST legality
ledger support legality
mass domain legality
credit type legality
scale legality
ownership uniqueness where required
source/provenance validity
no spent-credit resurrection
no forbidden future/history lookup
energy/flow identity required by the rule
```

## 10.4 Refutation

One symbolic or concrete legal primitive violating a required invariant refutes MST0-11.

Finite exhaustive enumeration may falsify or mutation-test the proof; it is not the proof itself.

---

# 11. MST0-09 raw boundary law: Boundary Torture Chamber

## 11.1 Objective

Prove or refute the exact arbitrary-`n` boundary law actually used by MSTC-0002.

## 11.2 Adversarial families

Generate legal executions maximizing:

```text
active boundary count
nested boundaries
alternating orientation
boundary creation/destruction rate
rank gap
interval span
simultaneous positive KEEP burden
DELETE burst length before KEEP
credit lifetime before activation
boundary reactivation
mirror asymmetry
```

## 11.3 Proof requirement

The final law must identify the exact cost-bearing source for every harmful boundary contribution.

No statement of the form “all observed boundary damage was bounded” is theorem-facing.

## 11.4 Failure preservation

The smallest exact counterexample and an inflation attempt are append-only artifacts.

A failure refutes this positive route statement but does not by itself imply Dynamic Optimality is false.

---

# 12. MST0-13 bounded DELETE injection: hostile review and formal transport

v0.3 contains an author proof claim of the form:

```math
E_{after}-E_{before}\le 6\,\operatorname{cost}_A(D).
```

v0.4 must not rubber-stamp it.

## 12.1 Review attacks

Audit:

```text
rotation count <= access cost under the exact cost convention
T7 bounded creation in every legal primitive
T5 conservation
T6 inapplicability on DELETE
ROOT/ZIG/LL/RR/LR/RL completeness
block versus access granularity
initial/final ledger terms
hidden dependence on n
hidden dependence on finite evidence
all imported definitions bound to exact parent hashes
```

## 12.2 Formalization

The exact proof statement is formalized in Lean and linked to the imported MSTC-0002 semantics by hash/version.

## 12.3 Human action

Only a human may record:

```text
ACCEPT
REJECT
BLOCKED
```

If ACCEPT and formal checks are green:

```text
MST0-13 -> REVIEWED
BOUNDED_DELETE_INJECTION_PROVED becomes a legal intermediate terminal claim.
```

---

# 13. MST0-22 constant independence

The theorem must literally quantify the frozen constants before arbitrary inputs:

```math
\exists C=2,\;k=6\quad
\forall n,T,X,Y\preceq X:\;\cdots
```

No proof object may reference:

```text
n-specific coefficient
sequence length
holdout identifier
corpus identifier
finite state ID
cycle ID
search seed
solver-selected panel
proof decomposition choice
```

The static scanner is supporting evidence only; the mathematical proof must show the definitions themselves are uniform.

A hidden dependence on any forbidden parameter refutes MST0-22.

---

# 14. MST0-14 synchronous KEEP repayment: K6 Saturation War

This is the central local theorem attack.

## 14.1 Exact target

For every legal KEEP event/block under the frozen calculus, prove the exact repayment inequality required by MST0-17 at `C=2`.

In edge-regret notation:

```math
w=y-2a.
```

Whenever `w>0`, the calculus must expose sufficient legal payment without double use of credit and without future information.

## 14.2 Why `k=6` is attacked directly

The fresh parent experiment established only:

```text
k=2 failed on fresh H3T
k=6 survived fresh H3T
```

This does not prove a six-way combinatorial theorem.

v0.4 therefore treats “why six?” as an explicit theorem-mining target.

## 14.3 `K6_SATURATION_ATTACK`

Construct legal executions maximizing the demand placed on the exact frozen `k=6` injection/credit semantics.

The attack attempts to create a legal configuration whose exact repayment certificate would require strictly more resource than the frozen six-unit rule permits.

Search dimensions include:

```text
scale combinations
rotation roles
provenance classes
left/right/mixed orientation
nested causal intervals
zig-zig / zig-zag alternation
boundary crossings
DELETE bursts then KEEP
long-lived latent packets
simultaneous activation
mirror families
rank-gap extremes
recurrent KEEP motifs
```

The implementation must derive “independent demand” from the actual calculus semantics. It may not assume that `k=6` literally means six abstract slots unless that equivalence is proved.

## 14.4 Desired structural theorem shape

Preferred discoveries include an exact universal statement such as:

```text
- bounded overlap of causal supports;
- bounded multiplicity of simultaneously active obligations;
- forced merge/cancellation of an attempted seventh independent demand;
- bend destruction closing one claim class;
- laminar boundary ownership preventing independent coexistence;
- a stronger injection-to-payment matching theorem.
```

The final theorem is whatever exact statement suffices to prove MST0-14; it is not required to use the English phrase “at most six claims.”

## 14.5 Refutation

One exact legal KEEP witness with positive residual under the *frozen theorem semantics* refutes MST0-14 and MSTC-0002 as a universal Pair-Access proof mechanism.

The witness must be independently replayed and minimized under the preregistered canonical order.

---

# 15. MST0-15 integrability: Double-Spend Apocalypse

Local repayment is insufficient.

v0.4 must prove that all local payments coexist globally without decomposition dependence, duplicate consumption, or hidden negative terminal energy.

## 15.1 Credit-use graph

Construct an exact directed acyclic/possibly cyclic accounting graph whose nodes/edges encode, as applicable:

```text
credit creation
ownership
transfer
split/merge
activation
consumption
cancellation
support migration
scale migration
```

Every unit of theorem-facing mass must have a unique auditable lifecycle under the frozen calculus semantics.

## 15.2 `DOUBLE_SPEND_APOCALYPSE`

Generate histories attempting:

```text
same causal mass pays two KEEP debts
nested intervals claim the same source
crossing intervals create incompatible ownership
credits survive and reactivate repeatedly
cyclic transfer returns mass to a reusable state
decomposition choice changes total paid amount
terminal stored energy grows with sequence length
terminal energy can become arbitrarily negative
local legal payments cannot be simultaneously realized
```

## 15.3 Positive theorem targets

Any sufficient exact structure is permitted, including:

```text
laminar ownership
unique causal ownership
monotone credit lifetime
acyclic use graph
conservation with single consumption
canonical decomposition independence
explicit scalar energy with universal lower bound
exact flow theorem that telescopes without scalar energy
```

## 15.4 Refutation

An exact legal family showing unavoidable double spending, path dependence, or unbounded endpoint defect refutes MST0-15 as stated.

Again: this refutes the MSTC-0002 Pair-Access proof route, not Dynamic Optimality itself.

---

# 16. Negative obstruction lifting contract

The negative branch is dormant while the positive path remains logically viable.

It activates immediately when any theorem-critical positive node is `REFUTED`, or when the exact Pair-Access/bridge theorem is proved false under the frozen conventions.

## 16.1 Local obstruction is not a DOC disproof

Forbidden implication:

```text
MSTC-0002 fails -> Dynamic Optimality false
```

## 16.2 Genuine negative target

A negative success requires a closed-form family `(T_m,X_m)` with a proof that:

```math
\operatorname{Splay}(X_m,T_m)\ge g(m)
```

and an explicit legal BST execution/algorithm with:

```math
\operatorname{OPT}(X_m,T_m)\le f(m),
```

such that:

```math
\frac{g(m)}{f(m)}\to\infty.
```

It is sufficient to upper-bound OPT by an explicit valid BST execution; exact OPT computation is not required.

## 16.3 Obstruction lifting

The exact positive-route counterexample may seed the family construction, but the final family may not be solver-defined one instance at a time.

Required:

```text
closed-form tree family
closed-form access family
legality proof
Splay lower bound
competitor upper bound
ratio divergence
independent replay on finite prefixes
formal theorem
human review
```

## 16.4 Negative branch independence

A negative theorem must be checkable without trusting the failed transfer calculus.

---

# 17. Outcome taxonomy

Core statuses:

```text
PARENT_CHAIN_VERIFIED
PARENT_SEAL_MISMATCH
SURVIVOR_IDENTITY_VERIFIED
SURVIVOR_IDENTITY_MISMATCH
BRIDGE_SOURCES_FROZEN
BRIDGE_SOURCE_UNAVAILABLE
FORMAL_KERNEL_FROZEN
FORMALIZATION_MISMATCH
PSC_FROZEN
MST0_08U_PROVED / MST0_08U_REFUTED
MST0_09_PROVED / MST0_09_REFUTED
MST0_11_PROVED / MST0_11_REFUTED
MST0_13_REVIEWED / MST0_13_REJECTED
MST0_22_PROVED / MST0_22_REFUTED
MST0_14_PROVED / MST0_14_REFUTED
MST0_15_PROVED / MST0_15_REFUTED
UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED
APPROXIMATE_MONOTONICITY_PROVED
DYNAMIC_OPTIMALITY_PROVED
MSTC0002_UNIVERSAL_COUNTEREXAMPLE
NEGATIVE_FAMILY_CANDIDATE
NEGATIVE_REAL_SPLAY_FAMILY_PROVED
DYNAMIC_OPTIMALITY_DISPROVED
POSITIVE_ROUTE_REFUTED_NO_DOC_NEGATIVE
BRIDGE_BLOCKED_NO_CLAIM
RESOURCE_LIMIT_NO_CLAIM
```

YES and NO theorem claims are mutually exclusive under one sealed run.

---

# 18. Repository layout

Recommended root:

```text
splay-decide-v04/
|-- README.md
|-- IMPLEMENTATION_SPEC_v0.4.md
|-- WorkPlan.md
|-- Path.md
|-- CHANGELOG.md
|-- CITATIONS.md
|-- AI_USE.md
|-- LICENSE
|-- pyproject.toml
|-- requirements-lock.txt
|-- lean-toolchain
|-- lakefile.lean
|-- lake-manifest.json
|
|-- parent/
|   |-- V03_SEAL.json
|   |-- V03_FINAL_RESULT.json
|   |-- V03_MANIFEST.sha256
|   |-- V03_ARCHIVE.sha256
|   |-- V03_PATH_FINAL.md
|   |-- V03_WORKPLAN_FINAL.md
|   |-- V03_MSTC_0002.json
|   |-- V03_THEOREM_STATUS.json
|   |-- V03_COUNTEREXAMPLE_INDEX.json
|   `-- BOOTSTRAP_MANIFEST.sha256
|
|-- prereg/
|   |-- experiment_v0.4.yaml
|   |-- parent_contract.yaml
|   |-- theorem_battlefield.yaml
|   |-- theorem_gate_matrix.yaml
|   |-- dual_obligation_policy.yaml
|   |-- proof_kernel_policy.yaml
|   |-- proof_stress_corpus.yaml
|   |-- negative_lifting_policy.yaml
|   |-- bridge_sources.yaml
|   |-- threat_control_matrix.yaml
|   |-- stop_control_matrix.yaml
|   |-- allowed_claims.md
|   |-- forbidden_claims.md
|   `-- prereg_sha256.txt
|
|-- math/
|   |-- definitions_v0.4.md
|   |-- theorem_MST08U_locality.md
|   |-- theorem_MST09_raw_boundary.md
|   |-- theorem_MST11_preservation.md
|   |-- theorem_MST13_delete_injection.md
|   |-- theorem_MST14_keep_repayment.md
|   |-- theorem_MST15_integrability.md
|   |-- theorem_MST22_constant_independence.md
|   |-- theorem_MST17_pair_access.md
|   |-- theorem_MST18_telescoping.md
|   |-- theorem_MST19_bridge.md
|   |-- negative/
|   |-- reviews/
|   `-- proof_status.json
|
|-- lean/
|   |-- Splay/Core.lean
|   |-- Splay/PairAccess.lean
|   |-- MSTC0002/Ledger.lean
|   |-- MSTC0002/Locality.lean
|   |-- MSTC0002/Preservation.lean
|   |-- MSTC0002/Boundary.lean
|   |-- MSTC0002/Injection.lean
|   |-- MSTC0002/Repayment.lean
|   |-- MSTC0002/Integrability.lean
|   |-- MSTC0002/Constants.lean
|   |-- PairAccess/Composition.lean
|   |-- PairAccess/Telescope.lean
|   `-- Negative/Family.lean
|
|-- python/
|   |-- inherited/
|   |-- formal_bridge/
|   |-- proof_attack/
|   |   |-- locality_explosion.py
|   |   |-- primitive_exhaust.py
|   |   |-- boundary_torture.py
|   |   |-- k6_saturation.py
|   |   |-- double_spend.py
|   |   `-- telescope_torture.py
|   |-- negative/
|   |   |-- lift_obstruction.py
|   |   |-- splay_lower.py
|   |   |-- competitor_upper.py
|   |   `-- family_replay.py
|   |-- audit/
|   |-- seal/
|   `-- cleanroom/
|
|-- schemas/
|-- tests/
|   |-- parent/
|   |-- formal/
|   |-- locality/
|   |-- preservation/
|   |-- boundary/
|   |-- injection/
|   |-- repayment/
|   |-- integrability/
|   |-- constants/
|   |-- pair_access/
|   |-- bridge/
|   |-- negative/
|   |-- mutation/
|   `-- seal/
|
|-- artifacts/v04/
|   |-- freeze/
|   |-- formal/
|   |-- proof_attacks/
|   |-- counterexamples/
|   |-- proofs/
|   |-- negative/
|   |-- audits/
|   |-- logs/
|   `-- seal/
|
`-- scripts/
    |-- run_phase00.py
    |-- ...
    |-- run_phase19.py
    `-- reproduce_all_v0.4.py
```

---

# 19. Preregistration files

## 19.1 `experiment_v0.4.yaml`

Minimum:

```yaml
experiment_id: SPLAY-AM-DECIDE-v0.4
parent:
  experiment_id: SPLAY-AM-MST-v0.3
  sealed_commit: TO_BE_PINNED_FULL_SHA
  expected_terminal_claim: TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS
primary_candidate:
  calculus_id: MSTC-0002
  predicate: P_all
  k: 6
  C: 2
  mutation_allowed: false
target_problem: Sleator-Tarjan Dynamic Optimality Conjecture
success_outcomes:
  - DYNAMIC_OPTIMALITY_PROVED
  - DYNAMIC_OPTIMALITY_DISPROVED
no_claim_outcomes_allowed: true
```

## 19.2 `theorem_battlefield.yaml`

Must enumerate exactly:

```text
MST0-08U
MST0-09
MST0-11
MST0-13
MST0-14
MST0-15
MST0-22
MST0-17
MST0-18
MST0-19
```

For each:

```text
exact statement hash
exact negation
parent status
v0.4 owner phase
first consumer
required status
prerequisites
allowed child-lemma namespace
forbidden premises
proof artifact
formal artifact
review artifact
refutation artifact
whether falsity refutes MSTC-0002 only or can feed DOC-negative lifting
```

## 19.3 `dual_obligation_policy.yaml`

Freeze:

```text
prove/refute simultaneous policy
canonical counterexample order
proof mutation policy
proof review package schema
erratum policy
no downstream consumption before REVIEWED
```

## 19.4 `proof_stress_corpus.yaml`

Freeze all PSC families, generators, parameter ranges, seeds, symbolic objectives, minimization orders, and exact replay policies before theorem-specific attack execution.

## 19.5 `negative_lifting_policy.yaml`

Freeze the rules for activating the negative branch and the exact certificate requirements for `DYNAMIC_OPTIMALITY_DISPROVED`.

## 19.6 `bridge_sources.yaml`

Freeze exact L2/L3 theorem premise artifacts before Phase 16.

## 19.7 `theorem_gate_matrix.yaml`

For every critical node:

```text
owner phase
first consumer
required status REVIEWED
proof artifact
formal artifact
review artifact
refutation artifact
controls
```

---

# 20. Canonical data schemas

All sealed JSON:

```text
UTF-8, no BOM
sorted keys
canonical separators
newline termination
integer strings for arbitrary-precision fields
rational {num,den}
explicit schema_version
SHA-256 references for every dependency
```

Required schemas include at minimum:

```text
parent_import.schema.json
survivor_binding.schema.json
theorem_obligation.schema.json
proof_certificate.schema.json
formal_certificate.schema.json
review_record.schema.json
proof_attack.schema.json
locality_witness.schema.json
preservation_case.schema.json
boundary_witness.schema.json
repayment_witness.schema.json
credit_use_graph.schema.json
integrability_witness.schema.json
pair_access_certificate.schema.json
bridge_audit.schema.json
negative_family.schema.json
final_result_v0.4.schema.json
```

Example theorem obligation:

```json
{
  "schema_version": "DECIDE-THEOREM-v0.4",
  "theorem_id": "MST0-14",
  "statement_sha256": "...",
  "negation_sha256": "...",
  "dependencies": ["MST0-08U","MST0-09","MST0-11","MST0-13","MST0-22"],
  "status": "UNPROVED",
  "formal_status": "PENDING",
  "review_status": "PENDING",
  "critical_path": true
}
```

---

# 21. Deterministic implementation order within every phase

Every phase follows:

```text
VERIFY PARENT / INPUT HASHES
  -> LOAD FROZEN v0.4 CONTRACT
    -> ASSERT THEOREM GATES
      -> ASSERT SURVIVOR BINDING
        -> ASSERT FORMAL KERNEL VERSION
          -> LOAD EXACT THEOREM + NEGATION
            -> RUN REFUTATION ATTACK FIRST OR IN PARALLEL
              -> DEVELOP / CHECK PROOF
                -> SAVE RAW APPEND-ONLY OUTPUT
                  -> BUILD FORMAL CERTIFICATE
                    -> INDEPENDENT CHECK
                      -> RUN PROOF MUTANTS
                        -> BUILD HUMAN REVIEW PACKAGE
                          -> UPDATE DERIVED STATUS ONLY AFTER HUMAN VERDICT
                            -> APPEND Path.md
```

No phase rewrites prereg files after `FOUNDATION_FROZEN`.

---

# 22. Twenty-phase implementation plan

# PHASE 00 - Clone, pin, freeze the v0.4 decision contract

## Goal

Create an immutable theorem battlefield before any new proof search or refutation attack.

## 00.1 Pin v0.3 final seal

Verify full parent commit and exact hashes for:

```text
FINAL_RESULT
MANIFEST
archive
Path.md
WorkPlan.md
MSTC-0002
candidate-set commitment
h3t reveal/state
lifecycle audit
counterexample atlas
all parent theorem docs/reviews used downstream
```

## 00.2 Freeze v0.4 spec/prereg

Freeze this specification, theorem battlefield, dual-obligation rules, PSC, proof kernel policy, negative-lifting policy, bridge-source policy, threats/stops/tests/invariants.

## 00.3 Initialize v0.4 theorem ledger

Imported reviewed parent lemmas retain imported status only after hash verification.

Critical v0.4 nodes initialize from the mapped frontier, not by copying parent prose blindly.

## Phase-00 gate

```text
FOUNDATION_FROZEN
```

---

# PHASE 01 - Reverify survivor identity and blocker DAG

## Goal

Prove that v0.4 is attacking exactly the sealed MSTC-0002 and exactly the mapped positive blockers.

## 01.1 Survivor binding

Verify every theorem-facing field of MSTC-0002 against the parent record and candidate-set commitment.

## 01.2 Fresh history integrity

Verify the parent one-unlock H3T trajectory and exact sibling kill records without re-unlocking any bank.

## 01.3 Blocker DAG re-derivation

Independently derive from the gate matrix and parent theorem statuses that the positive critical set is exactly:

```text
08U,09,11,13,14,15,22,17,18,19
```

## Phase-01 gate

```text
SURVIVOR_IDENTITY_VERIFIED
BATTLEFIELD_VERIFIED
```

---

# PHASE 02 - Freeze exact bridge premise sources

## Goal

Remove the independent L2/L3 source-byte blocker before the endgame.

## 02.1 Acquire exact authorized artifacts

Freeze exact source versions/theorem statements.

## 02.2 Convention extraction

Extract the exact bridge theorem hypotheses into a machine-readable checklist.

## 02.3 Independent extraction

A second implementation reproduces the statement/hypothesis record.

## Phase-02 gate

```text
BRIDGE_SOURCES_FROZEN
```

or fail closed:

```text
BRIDGE_SOURCE_UNAVAILABLE
```

---

# PHASE 03 - Freeze the formal kernel and semantic equivalence layer

## Goal

Establish Lean definitions corresponding exactly to the inherited executable semantics.

## 03.1 Splay equivalence

Prove/verify ROOT/ZIG/LL/RR/LR/RL and final-tree/cost agreement against the exact Python semantics on generated finite canaries, while the theorem proof itself is symbolic.

## 03.2 Pair-Access equivalence

Bind KEEP/DELETE/subsequence/cost definitions.

## 03.3 MSTC-0002 binding

Bind ledger/rule semantics field-by-field to the sealed survivor JSON.

## Phase-03 gate

```text
FORMAL_KERNEL_FROZEN
```

---

# PHASE 04 - Freeze dual obligations and Proof Stress Corpus

## Goal

Freeze every theorem's exact statement, exact negation, attack interfaces, and proof mutants before the theorem campaign.

## 04.1 Generate PSC

Commit PSC-L/P/B/K6/I/T/N without using future proof failures to alter definitions.

## 04.2 Freeze proof mutants

Preregister mutation operators for every critical theorem.

## Phase-04 gate

```text
PSC_FROZEN
DUAL_OBLIGATIONS_FROZEN
```

---

# PHASE 05 - Hostile review / formalize MST0-13 DELETE injection

## Goal

Turn the parent author proof claim into a legitimately REVIEWED theorem or preserve the exact defect.

## 05.1 Formal proof

Formalize the exact imported statement.

## 05.2 Refutation attack

Attack all Splay cases, T5/T6/T7 boundaries, block granularities, and hidden-dependence possibilities.

## 05.3 Human review package

Produce proof + formal output + attack results + mutants + objections.

## Phase-05 gate

One of:

```text
MST0_13_REVIEWED
MST0_13_REJECTED
```

A rejection activates the positive-route-failure record and Phase-17 negative lifting, but does not itself imply DOC is false.

---

# PHASE 06 - Prove or refute MST0-08U universal locality

## Goal

Close the parent SPLIT theorem's arbitrary-`n` gap.

## 06.1 Locality Explosion Engine

Run PSC-L and symbolic family attacks.

## 06.2 Proof

Prove exactly the bounded modifications required by the downstream calculus.

## 06.3 Formal check + hostile review

No finite maximum is a premise.

## Phase-06 gate

```text
MST0_08U_REVIEWED
```

or:

```text
MST0_08U_REFUTED
```

---

# PHASE 07 - Prove or refute MST0-11 transfer preservation

## Goal

Symbolically exhaust every primitive calculus update.

## 07.1 Primitive symbolic cases

ROOT/ZIG/LL/RR/LR/RL plus every ledger rule applicable to MSTC-0002.

## 07.2 Proof mutants

Delete one case, mutate one rule result, alter one support relation: the suite must reject.

## Phase-07 gate

```text
MST0_11_REVIEWED
```

or:

```text
MST0_11_REFUTED
```

---

# PHASE 08 - Prove or refute MST0-09 raw boundary law

## Goal

Resolve the arbitrary-`n` boundary theorem actually consumed by repayment/integrability.

## 08.1 Boundary Torture Chamber

Run PSC-B.

## 08.2 Exact theorem

Prove the frozen law or preserve the smallest legal counterexample and an inflation analysis.

## Phase-08 gate

```text
MST0_09_REVIEWED
```

or:

```text
MST0_09_REFUTED
```

---

# PHASE 09 - Prove or refute MST0-22 constant independence

## Goal

Prove that `C=2`, `k=6`, and every theorem-facing rule constant are uniform.

## 09.1 Quantifier audit

Check the exact order of quantifiers and all definitions.

## 09.2 Static + formal proof

Static scans support but never replace the proof.

## Phase-09 gate

```text
MST0_22_REVIEWED
```

or:

```text
MST0_22_REFUTED
```

---

# PHASE 10 - K6 Saturation War: pre-proof attack on KEEP repayment

## Goal

Attempt to destroy MST0-14 before writing the final proof, while mining exact structural lemmas from failed attacks.

## 10.1 Attack families

Run PSC-K6 across generated, symbolic, spliced, nested-scale, recurrent, and mirror families.

## 10.2 Counterexample minimization

Any exact positive residual under frozen theorem semantics is independently replayed and minimized.

## 10.3 Lemma mining

If attacks fail, preserve candidate structural explanations but do not promote them automatically.

## Phase-10 gate

One of:

```text
KEEP_REPAYMENT_EXACT_COUNTEREXAMPLE
KEEP_REPAYMENT_ATTACK_SURVIVED
```

Survival is not a theorem.

---

# PHASE 11 - Prove or refute MST0-14 synchronous KEEP repayment

## Goal

Close the central local theorem for every legal KEEP.

## 11.1 Case-complete proof

Cover all rotation classes, support classes, activation/payment rules, and local structural configurations required by the calculus.

## 11.2 Matching/accounting theorem

Prove the exact mapping from positive regret to legally available payment.

## 11.3 Formal proof + hostile review

All child lemmas are versioned and dependency-linked.

## Phase-11 gate

```text
MST0_14_REVIEWED
SYNCHRONOUS_KEEP_TRANSFER_PROVED
```

or:

```text
MST0_14_REFUTED
MSTC0002_UNIVERSAL_COUNTEREXAMPLE
```

---

# PHASE 12 - Double-Spend Apocalypse: pre-proof attack on integrability

## Goal

Attempt to construct a globally inconsistent accounting even if every local KEEP looks payable.

## 12.1 Credit-use graph

Build exact lifecycle graphs for all attacked executions.

## 12.2 Attack objectives

Maximize reuse multiplicity, ownership ambiguity, cycle formation, endpoint defect, and decomposition disagreement.

## 12.3 Independent checker

A clean-room implementation receives only the frozen calculus and history.

## Phase-12 gate

```text
INTEGRABILITY_EXACT_COUNTEREXAMPLE
```

or:

```text
INTEGRABILITY_ATTACK_SURVIVED
```

---

# PHASE 13 - Prove or refute MST0-15 integrability

## Goal

Prove decomposition-independent global accounting or exact direct telescoping.

## 13.1 Global theorem

Prove every unit of credit has a legal lifecycle and cannot be spent twice.

## 13.2 Endpoint theorem

Prove initial and terminal energy/flow terms are controlled exactly.

## 13.3 Formal proof + hostile review

No finite path enumeration as premise.

## Phase-13 gate

```text
MST0_15_REVIEWED
GLOBAL_INTEGRABILITY_PROVED
```

or:

```text
MST0_15_REFUTED
```

---

# PHASE 14 - Prove MST0-17 universal Pair-Access composition

## Goal

Once all direct prerequisites are REVIEWED, reconstruct the Pair-Access theorem from scratch.

Required reviewed inputs:

```text
MST0-08U
MST0-09
MST0-11
MST0-13
MST0-14
MST0-15
MST0-22
plus already-reviewed inherited structural prerequisites
```

## 14.1 No status toggling shortcut

The theorem must be written and proved independently; upstream review does not mechanically imply MST0-17.

## 14.2 Exact theorem

Prove the frozen block/local inequalities imply:

```math
\operatorname{Splay}(Y,T)+E_m-E_0
\le
2\operatorname{Splay}(X,T)+A(n).
```

## Phase-14 gate

```text
MST0_17_REVIEWED
UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED
```

---

# PHASE 15 - Prove MST0-18 telescope / approximate monotonicity

## Goal

Control endpoint energy and obtain the exact approximate-monotonicity statement consumed by the bridge.

## 15.1 Telescope Torture

PSC-T attempts:

```text
E_m unbounded below
E_0 improperly positive
A(n) sequence-dependent
block overlap
missing access
hidden reset between blocks
```

## 15.2 Formal theorem

Prove the exact additive term and direction.

## Phase-15 gate

```text
MST0_18_REVIEWED
APPROXIMATE_MONOTONICITY_PROVED
```

---

# PHASE 16 - Prove MST0-19 bridge under exact frozen source conventions

## Goal

Audit the exact Levy-Tarjan premise and map the v0.4 approximate-monotonicity theorem into the Dynamic Optimality theorem.

## 16.1 Convention checklist

Must check:

```text
ordinary bottom-up Splay variant
cost convention
initial-tree convention
subsequence definition
additive term
universal constant independence
direction of implication
exact theorem/version
quantifier order
any normalization or root assumptions
```

## 16.2 Independent bridge reconstruction

A second reviewer/implementation reconstructs the mapping from source theorem text and frozen v0.4 statement without using the first audit's conclusion.

## Phase-16 gate

```text
MST0_19_REVIEWED
BRIDGE_READY_FOR_DECISION
```

or:

```text
BRIDGE_BLOCKED_NO_CLAIM
```

---

# PHASE 17 - Negative obstruction lifting if the positive route was refuted

## Goal

If any theorem-critical positive node is REFUTED, attempt a genuine Dynamic-Optimality disproof rather than stopping at a representation failure.

## 17.1 Activation

Activated by an exact preserved obstruction from Phase 05–16.

If the positive chain is intact and `BRIDGE_READY_FOR_DECISION`, Phase 17 records:

```text
NEGATIVE_BRANCH_NOT_ACTIVATED
```

and performs no speculative negative mining.

## 17.2 Closed-form family

If activated, derive a parameterized legal family.

## 17.3 Real Splay lower bound

Formal symbolic lower bound.

## 17.4 Explicit competitor upper bound

Construct a legal BST execution and bound its cost.

## 17.5 Divergence

Prove ratio divergence.

## Phase-17 gate

One of:

```text
NEGATIVE_BRANCH_NOT_ACTIVATED
NEGATIVE_REAL_SPLAY_FAMILY_PROVED
POSITIVE_ROUTE_REFUTED_NO_DOC_NEGATIVE
RESOURCE_LIMIT_NO_CLAIM
```

---

# PHASE 18 - DECISION GATE: actual theorem result

## Goal

Emit the strongest mathematically justified theorem result and nothing stronger.

## 18.1 Positive activation

The positive branch may activate only if all of:

```text
MST0-08U REVIEWED
MST0-09  REVIEWED
MST0-11  REVIEWED
MST0-13  REVIEWED
MST0-14  REVIEWED
MST0-15  REVIEWED
MST0-22  REVIEWED
MST0-17  REVIEWED
MST0-18  REVIEWED
MST0-19  REVIEWED
```

and all formal/review dependency hashes match.

Then Phase 18 may emit:

```text
DYNAMIC_OPTIMALITY_PROVED
```

only after regenerating the complete proof DAG from frozen artifacts.

## 18.2 Negative activation

The negative branch may emit:

```text
DYNAMIC_OPTIMALITY_DISPROVED
```

only if Phase 17 has a REVIEWED closed-form real-Splay/competitor divergence theorem.

## 18.3 No forced binary claim

If neither branch closes, Phase 18 must emit an exact no-claim level explaining the first unresolved/refuted gate.

## 18.4 Mutual exclusivity

Exactly one terminal theorem-facing branch may be active.

## Phase-18 gate

Exactly one of:

```text
DYNAMIC_OPTIMALITY_PROVED
DYNAMIC_OPTIMALITY_DISPROVED
POSITIVE_ROUTE_REFUTED_NO_DOC_NEGATIVE
BRIDGE_BLOCKED_NO_CLAIM
RESOURCE_LIMIT_NO_CLAIM
```

No finite-survival status is sufficient at this stage.

---

# PHASE 19 - Seal, reproduce, package, and release

## Goal

Seal the decision experiment from artifacts only.

## 19.1 FINAL_RESULT

Regenerate the Phase-18 terminal level solely from theorem statuses, formal certificates, review records, negative-family certificates, and bridge audit.

## 19.2 Fresh-checkout reproduction

Must verify:

```text
parent seal and MSTC-0002 binding
prereg freeze
Lean toolchain and proof hashes
all theorem dependency hashes
all human review records
all exact counterexamples
PSC commitments
bridge source hashes
negative family if present
Phase-18 branch recomputation
```

No consumed v0.3 holdout is re-unlocked.

## 19.3 Deterministic archive

Create:

```text
SPLAY-AM-DECIDE-v0.4.tar.zst
```

with canonical ordering and rebuild byte identity.

## 19.4 Reports

Produce:

```text
DECISION_REPORT.md
THEOREM_BATTLEFIELD_REPORT.md
MSTC0002_PROOF_LEDGER.md
LOCALITY_REPORT.md
KEEP_REPAYMENT_REPORT.md
INTEGRABILITY_REPORT.md
PAIR_ACCESS_REPORT.md
BRIDGE_AUDIT.md
NEGATIVE_OBSTRUCTION_REPORT.md
COUNTEREXAMPLE_ATLAS.md
REPRODUCIBILITY.md
AI_USE.md
```

---

# 23. Threat model

The v0.4 seal audits at least the following threats.

```text
T001 parent v0.3 navigation hash mistaken for full sealed identity
T002 parent FINAL_RESULT not verified from artifact
T003 parent Path.md ignored despite implementation-reality dependence
T004 MSTC-0002 reconstructed rather than imported by exact hash
T005 MSTC-0002 field mutated under same calculus ID
T006 sibling fresh failures omitted from lineage
T007 consumed H3T re-unlocked or regenerated
T008 finite H3T survival used as theorem premise
T009 large-n survival used as theorem premise
T010 parent author proof status treated as human REVIEWED
T011 parent scoped-finite MST0-08 treated as universal REVIEWED
T012 blocker DAG hand-edited to remove a difficult theorem
T013 new critical-path theorem silently invented after failure
T014 theorem statement weakened after refutation under same ID
T015 theorem negation incorrectly encoded
T016 proof attack tests an easier negation than the theorem requires
T017 counterexample generator shares proof implementation logic
T018 clean-room checker shares a theorem-critical helper
T019 exact witness minimized incorrectly
T020 smallest-witness claim based on noncanonical order
T021 Lean theorem differs from markdown theorem
T022 Lean proof contains sorry/admit/axiom escape
T023 imported axiom not declared in kernel manifest
T024 code generator inserts unchecked theorem
T025 formal proof binds wrong MSTC-0002 version
T026 ROOT case omitted
T027 ZIG-left or ZIG-right omitted
T028 LL/RR omitted
T029 LR/RL omitted
T030 primitive transfer rule case omitted
T031 preservation theorem proves only finite supports
T032 locality theorem hides interval-size dependence
T033 locality proof uses empirical max radius
T034 locality attack fails to generate legal BSTs
T035 boundary theorem redefines damage after counterexample
T036 boundary source cost not identified
T037 boundary proof assumes no reactivation
T038 constant theorem quantifiers ordered incorrectly
T039 C=2 depends on n through a helper definition
T040 k=6 depends on finite panel
T041 theorem-facing support uses cycle/state ID
T042 theorem-facing proof uses holdout membership
T043 K6 saturation interprets k as six slots without proof
T044 K6 attack fails to target actual frozen injection semantics
T045 repayment proof uses future access
T046 repayment proof spends latent credit illegally
T047 repayment proof resurrects spent credit
T048 repayment proof uses same credit twice within one KEEP
T049 repayment proof uses same credit across multiple KEEP events
T050 local paid amount exceeds injected mass without theorem source
T051 proof ignores a positive-regret KEEP class
T052 finite no-counterexample result called repayment theorem
T053 integrability inferred from local repayment
T054 credit-use graph drops a transfer edge
T055 credit-use graph conflates merge with duplication
T056 credit split violates mass conservation
T057 decomposition choice changes total payment
T058 transfer cycle permits credit reuse
T059 terminal energy can drift negative
T060 initial energy normalization silently reset mid-execution
T061 endpoint additive term absorbs unproved deficit
T062 block partition double-counts an access
T063 block partition omits an access
T064 MST0-17 toggled REVIEWED automatically from prerequisites
T065 Pair-Access theorem cites v0.3 finite survival
T066 telescope assumes E_m>=0 without proof
T067 telescope additive term depends on sequence length
T068 telescope direction reversed
T069 bridge source bytes not exact
T070 bridge theorem version wrong
T071 bridge Splay variant mismatch
T072 bridge cost convention mismatch
T073 bridge initial-tree convention mismatch
T074 bridge subsequence definition mismatch
T075 bridge additive term mismatch
T076 bridge implication direction mismatch
T077 bridge quantifier mismatch
T078 external current literature silently replaces frozen source
T079 a failed positive lemma is called DOC disproof
T080 transfer residual used as Splay lower bound
T081 Pair-Access counterexample used as Splay-vs-OPT counterexample without reduction
T082 negative family defined instance-by-instance by solver
T083 negative family legality unproved
T084 Splay lower bound empirical only
T085 competitor execution illegal under BST model
T086 OPT upper bound inferred without explicit competitor
T087 ratio grows finitely but divergence unproved
T088 negative family relies on candidate ledger semantics
T089 negative proof reuses failed positive theorem
T090 NO claim from resource exhaustion
T091 YES claim from proof search timeout absence
T092 human review generated by agent
T093 human ACCEPT lacks theorem SHA binding
T094 review ignores formal statement mismatch
T095 review record lacks objections/dependency audit
T096 theorem lifecycle jump UNPROVED->REVIEWED
T097 REFUTED theorem consumed downstream
T098 erratum overwrites prior REVIEWED artifact
T099 proof mutant not caught
T100 mutation suite lacks a known-killed control
T101 proof attack seed changed after seeing failure
T102 PSC definition adapted after theorem proof
T103 PSC survival called fresh evidence
T104 random generator nondeterminism changes best witness
T105 parallel reduction changes canonical witness
T106 floating-point sign determines theorem status
T107 symbolic inequality delegated to approximate solver only
T108 solver SAT accepted without exact replay
T109 solver UNSAT accepted without certificate/independent proof
T110 source quote/hypothesis extracted incorrectly
T111 report omits a failed theorem attempt
T112 counterexample deleted after proof repair
T113 manifest omits Lean source or compiled proof artifact
T114 archive excludes negative evidence
T115 FINAL_RESULT hardcoded rather than derived
T116 both YES and NO branches accidentally active
T117 no-claim state mislabeled success
T118 resource record incomplete
T119 AI-assisted theorem edit not disclosed
T120 Phase 18 run before all required gates are resolved
```

At seal:

```text
set(threat_ids)=={T001,...,T120}
every threat has >=1 valid control
every referenced control exists
```

---

# 24. Test matrix

Minimum named tests.

## Parent / foundation

```text
PARENT-01 full v0.3 sealed commit exact
PARENT-02 FINAL_RESULT exact
PARENT-03 manifest/archive exact
PARENT-04 Path.md/WorkPlan.md exact
PARENT-05 MSTC-0002 record exact
PARENT-06 candidate-set commitment binds MSTC-0002
PARENT-07 sibling H3T failures preserved
PARENT-08 H3T state remains UNLOCKED_ONCE/1 without reread
PARENT-09 blocker DAG matches sealed gate matrix
PARENT-10 no pre-prereg v0.4 science
```

## Formal kernel

```text
FORM-01 Lean toolchain exact
FORM-02 no sorry/admit
FORM-03 undeclared axiom scan clean
FORM-04 Splay case semantics agreement
FORM-05 cost depth+1 binding
FORM-06 Pair-Access KEEP binding
FORM-07 Pair-Access DELETE binding
FORM-08 MSTC-0002 field-by-field binding
FORM-09 theorem statement hash binding
FORM-10 dependency hash binding
FORM-11 formal mutant rejected
FORM-12 markdown/formal statement equivalence audit
```

## Locality

```text
LOC-01 legal Locality Explosion families
LOC-02 finite v0.3 witnesses replay
LOC-03 arbitrary-n statement exact
LOC-04 support-radius mutant caught
LOC-05 interval-span mutant caught
LOC-06 all primitive A rotations covered
LOC-07 no finite maximum used as premise
LOC-08 exact refutation replay if found
```

## Preservation

```text
PRES-01 ROOT
PRES-02 ZIG-left
PRES-03 ZIG-right
PRES-04 LL
PRES-05 RR
PRES-06 LR
PRES-07 RL
PRES-08 every MSTC-0002 rule case
PRES-09 support legality
PRES-10 mass conservation where required
PRES-11 spent-credit nonresurrection
PRES-12 missing-case mutant caught
```

## Boundary

```text
BND-01 boundary definition exact
BND-02 source cost explicit
BND-03 nested boundaries
BND-04 alternating orientation
BND-05 reactivation
BND-06 mirror covariance
BND-07 scale extremes
BND-08 exact counterexample minimization
```

## Injection

```text
INJ-01 parent theorem SHA exact
INJ-02 rotations<=cost proof
INJ-03 T7 bound
INJ-04 T5 conservation
INJ-05 T6 inapplicability
INJ-06 all Splay cases
INJ-07 no finite premise
INJ-08 human review binding
```

## Repayment

```text
REP-01 all positive-regret KEEP classes
REP-02 K6 attack legal
REP-03 actual k semantics used
REP-04 latent cannot pay unless activated
REP-05 spent cannot repay again
REP-06 no future access
REP-07 payment <= legally available mass
REP-08 exact residual arithmetic
REP-09 k=2 fresh kill replays as sensitivity control
REP-10 k=6 theorem proof independent of H3T
REP-11 C=1/k=5 proof mutants caught where meaningful
REP-12 universal formal proof
REP-13 clean-room theorem evaluator
REP-14 human hostile review
```

## Integrability

```text
INT-01 credit-use graph complete
INT-02 unique lifecycle identity
INT-03 split/merge conservation
INT-04 no double spend
INT-05 no transfer reuse cycle
INT-06 decomposition independence
INT-07 endpoint lower bound
INT-08 initial normalization
INT-09 long-history torture
INT-10 recurrent KEEP cycles
INT-11 nested/crossing intervals
INT-12 decomposition mutant caught
INT-13 formal proof
INT-14 human hostile review
```

## Constant independence

```text
CONST-01 C=2 frozen
CONST-02 k=6 frozen
CONST-03 no n dependence
CONST-04 no sequence-length dependence
CONST-05 no tree dependence
CONST-06 no corpus/holdout dependence
CONST-07 no decomposition dependence
CONST-08 quantifier-order formal check
```

## Pair Access / telescope / bridge

```text
PA-01 all prerequisites REVIEWED
PA-02 no finite premise import
PA-03 exact block coverage
PA-04 exact Pair-Access inequality
PA-05 formal composition
TEL-01 endpoint theorem
TEL-02 additive term explicit
TEL-03 additive term bridge-compatible
TEL-04 telescope symbolic check
BR-01 exact source bytes/identity
BR-02 source theorem statement exact
BR-03 Splay variant match
BR-04 cost match
BR-05 initial-tree match
BR-06 subsequence match
BR-07 additive-term match
BR-08 direction/quantifier match
BR-09 independent bridge reconstruction
```

## Negative branch

```text
NEG-01 activation only after exact positive obstruction
NEG-02 local obstruction not mislabeled DOC disproof
NEG-03 closed-form tree family
NEG-04 closed-form access family
NEG-05 legality proof
NEG-06 Splay lower bound symbolic
NEG-07 explicit BST competitor legal
NEG-08 competitor upper bound symbolic
NEG-09 ratio divergence
NEG-10 independent finite-prefix replay
NEG-11 formal negative theorem
NEG-12 human hostile review
```

## Decision / seal

```text
DEC-01 exactly one Phase-18 branch
DEC-02 YES requires all ten positive nodes REVIEWED
DEC-03 NO requires reviewed real-Splay/competitor divergence theorem
DEC-04 no-claim level derived correctly
SEAL-01 fresh checkout
SEAL-02 prereg exact
SEAL-03 threat set exact T001..T120
SEAL-04 stop set exact
SEAL-05 theorem lifecycle exact
SEAL-06 formal certificates complete
SEAL-07 review packages complete
SEAL-08 counterexamples retained
SEAL-09 manifest complete
SEAL-10 archive deterministic
SEAL-11 FINAL_RESULT regenerated
SEAL-12 AI use disclosed
```

---

# 25. Permanent invariants

At minimum:

```text
INV-001 parent is final sealed v0.3
INV-002 full parent commit, not short navigation hash, is authoritative
INV-003 parent artifacts read-only
INV-004 MSTC-0002 imported by exact hash
INV-005 MSTC-0002 predicate remains P_all
INV-006 MSTC-0002 k remains 6
INV-007 MSTC-0002 C remains 2
INV-008 candidate mutation requires new experiment ID
INV-009 ordinary bottom-up Splay unchanged
INV-010 cost remains depth+1
INV-011 Pair-Access KEEP/DELETE unchanged
INV-012 v0.3 H3T never re-unlocked
INV-013 sibling fresh failures retained
INV-014 finite survival never theorem premise
INV-015 blocker set exactly 08U/09/11/13/14/15/22/17/18/19
INV-016 newly discovered child lemmas versioned
INV-017 child lemma may not weaken parent theorem silently
INV-018 exact theorem negation frozen
INV-019 prove/refute tracks both retained
INV-020 exact refutation beats finite survival
INV-021 formal toolchain frozen
INV-022 no sorry/admit in theorem-critical proofs
INV-023 every axiom declared
INV-024 formal statement hash-bound to math statement
INV-025 executable/formal survivor semantics audited
INV-026 human proof and formal proof both required for PROVED
INV-027 human ACCEPT required for REVIEWED
INV-028 AI cannot author human ACCEPT
INV-029 theorem SHA bound in review
INV-030 objections retained
INV-031 REVIEWED dependencies required before consumption
INV-032 REFUTED theorem cannot be consumed
INV-033 errata preserve old artifacts
INV-034 PSC frozen before theorem attack
INV-035 PSC never called proof
INV-036 attack generator knows negation, not proof internals
INV-037 clean-room checker shares no theorem-critical helpers
INV-038 exact arithmetic controls signs
INV-039 canonical witness order frozen
INV-040 counterexamples append-only
INV-041 MST0-08U proof arbitrary n
INV-042 MST0-08U cannot cite finite maxima
INV-043 MST0-11 covers all primitive cases
INV-044 MST0-11 preserves all downstream-required invariants
INV-045 MST0-09 damage definition immutable
INV-046 boundary damage has explicit source cost
INV-047 MST0-13 parent proof not pre-reviewed
INV-048 MST0-13 review hostile, not ceremonial
INV-049 MST0-22 quantifiers place constants before arbitrary inputs
INV-050 C independent of n and length
INV-051 k independent of n and length
INV-052 K6 attack uses actual calculus semantics
INV-053 no assumption that k equals literal slot count
INV-054 every positive-regret KEEP included
INV-055 latent credit cannot pay illegally
INV-056 spent credit never reused
INV-057 payment source causal and legal
INV-058 local repayment not integrability
INV-059 credit-use graph complete
INV-060 no double spend
INV-061 split/merge conservation explicit
INV-062 transfer cycles audited
INV-063 decomposition independence proved
INV-064 terminal energy lower bound proved
INV-065 initial normalization explicit
INV-066 block partition exact once
INV-067 MST0-17 independently proved after prerequisites
INV-068 MST0-17 cannot cite v0.3 holdout pass
INV-069 telescope endpoints controlled
INV-070 additive term explicit
INV-071 additive term sequence-length independent
INV-072 L2/L3 premise identity frozen
INV-073 bridge convention match exact
INV-074 bridge direction exact
INV-075 bridge theorem version exact
INV-076 positive Phase-18 requires all ten critical nodes REVIEWED
INV-077 positive theorem branch regenerated from artifacts
INV-078 local positive-route failure not DOC disproof
INV-079 negative branch requires actual Splay costs
INV-080 negative branch requires explicit competitor
INV-081 OPT upper bound may use competitor, never unexplained oracle
INV-082 negative family closed form
INV-083 negative legality proved
INV-084 ratio divergence symbolic
INV-085 negative formal proof independent of failed ledger
INV-086 resource limit no claim
INV-087 no forced binary theorem
INV-088 YES/NO mutually exclusive
INV-089 failed proof attempts retained
INV-090 proof mutants retained
INV-091 all deterministic reductions sorted
INV-092 parallelism cannot change canonical witness
INV-093 no float decides theorem result
INV-094 manifest covers scientific and formal artifacts
INV-095 archive rebuild byte-identical
INV-096 FINAL_RESULT artifact-derived
INV-097 Path.md updated contemporaneously
INV-098 AI assistance disclosed
INV-099 current web context cannot override frozen premise sources
INV-100 Dynamic Optimality claim only at Phase-18 decision gate
```

---

# 26. Scaling and resource policy

## 26.1 Proof attacks may scale aggressively

Unlike v0.3, v0.4 is not restricted to a single fixed large-`n` panel for theorem attacks.

Permitted generated sizes include any deterministic schedule within resources, for example:

```text
16,24,32,48,64,96,128,192,256,384,512,768,1024,...
```

but no absence of a counterexample at any finite maximum is proof.

## 26.2 Symbolic before brute-force where possible

For preservation/locality/repayment/integrability, prefer symbolic parameter families and exact constraint solving that can expose an unbounded obstruction.

## 26.3 Large artifact hygiene

Use deterministic sharding/compression with logical-stream hashes.

## 26.4 Parallelism

Safe parallel tasks:

```text
independent theorem-negation searches
symbolic case generation
finite witness replay
proof mutation checking
formal compilation of independent modules
negative-family finite-prefix replay
```

All canonical selections are deterministically post-sorted.

## 26.5 Resource failure record

Must include:

```text
phase
theorem_id
prove/refute track
last valid artifact
wall time
peak memory
formal compiler state
solver/certificate state
search bounds attempted
unattempted regions
claims still valid
```

---

# 27. Logging requirements

Every run record contains:

```text
experiment_id
phase
UTC timestamp
local commit
parent v0.3 commit
spec SHA
prereg SHA
theorem battlefield SHA
Lean toolchain hash
bridge source manifest SHA
MSTC-0002 SHA
current theorem ID
prove/refute track
statement SHA
negation SHA
dependency SHAs
command
input hashes
output hashes
stdout/stderr hashes
wall time
peak memory
exit code
scientific status
```

Logs are append-only.

---

# 28. Dependencies and environment

Freeze exact versions.

Required baseline:

```text
Python 3.12+ or exact parent-compatible interpreter chosen at Phase 00
sympy
zstandard
jsonschema
z3-solver if symbolic counterexample search uses SMT
Lean 4 exact pinned toolchain
mathlib exact pinned commit if used
Rust stable optional acceleration only
```

Discovery solvers may propose witnesses. The theorem authority is exact replay, symbolic proof, formal kernel, and human review.

---

# 29. AI assistance policy

AI may assist:

```text
code generation
formalization scaffolding
proof search
counterexample generation
proof mutation design
literature theorem extraction under human/source audit
lemma brainstorming
review checklist generation
prose
audit
```

AI may not silently:

```text
change MSTC-0002
change a theorem statement after failure under same ID
record human ACCEPT
weaken a negation tested by the refutation engine
suppress a counterexample
use finite survival as proof
claim Pair Access failure disproves DOC
invent OPT bounds
replace exact bridge source versions
hide proof-assistant axioms/sorries
activate Phase 18 before gates
```

`AI_USE.md` is mandatory.

---

# 30. Stop conditions

Create `prereg/stop_control_matrix.yaml` with exact IDs `STOP-01..STOP-70`.

```text
STOP-01 parent v0.3 not finally sealed
STOP-02 parent full commit/hash mismatch
STOP-03 parent scientific artifact mutated
STOP-04 MSTC-0002 hash mismatch
STOP-05 MSTC-0002 field mutation
STOP-06 prereg hash mismatch
STOP-07 blocker DAG mismatch
STOP-08 v0.3 H3T re-unlock attempted
STOP-09 consumed holdout regenerated
STOP-10 finite parent survival used as theorem premise
STOP-11 bridge premise source unavailable but consumed
STOP-12 bridge source version mismatch
STOP-13 Lean toolchain drift
STOP-14 undeclared axiom/sorry/admit
STOP-15 formal statement mismatch
STOP-16 theorem negation mismatch
STOP-17 PSC changed after attack starts
STOP-18 proof attack reads proof internals improperly
STOP-19 clean-room checker shares critical implementation
STOP-20 float-dependent theorem sign
STOP-21 solver witness fails exact replay
STOP-22 solver UNSAT unverified
STOP-23 canonical witness nondeterministic
STOP-24 counterexample deleted
STOP-25 theorem weakened under same ID
STOP-26 child lemma silently inserted into critical path
STOP-27 downstream theorem consumed before REVIEWED prerequisite
STOP-28 ROOT/ZIG/LL/RR/LR/RL coverage incomplete
STOP-29 primitive ledger rule case omitted
STOP-30 locality proof uses finite maximum
STOP-31 locality support bound hides n dependence
STOP-32 boundary definition mutated
STOP-33 boundary source cost absent
STOP-34 MST0-13 review package SHA mismatch
STOP-35 human review generated by agent
STOP-36 constant quantifier order wrong
STOP-37 C or k depends on n/length/tree/corpus
STOP-38 K6 attack uses incorrect k semantics
STOP-39 repayment omits positive-regret KEEP class
STOP-40 repayment uses future information
STOP-41 latent credit pays illegally
STOP-42 spent credit reused
STOP-43 payment exceeds legal source without proof
STOP-44 local repayment treated as integrability
STOP-45 credit-use graph incomplete
STOP-46 double spend detected
STOP-47 split/merge mass inconsistency
STOP-48 decomposition dependence detected
STOP-49 terminal energy lower bound unproved
STOP-50 block partition incomplete
STOP-51 Pair-Access theorem cites finite evidence
STOP-52 telescope endpoint uncontrolled
STOP-53 additive term sequence-dependent
STOP-54 additive term bridge-incompatible
STOP-55 bridge Splay variant mismatch
STOP-56 bridge cost mismatch
STOP-57 bridge initial-tree mismatch
STOP-58 bridge subsequence mismatch
STOP-59 bridge direction/quantifier mismatch
STOP-60 local obstruction called DOC disproof
STOP-61 negative family not closed form
STOP-62 negative Splay lower bound empirical only
STOP-63 negative competitor illegal/unproved
STOP-64 negative ratio divergence unproved
STOP-65 positive and negative terminal branches both active
STOP-66 Phase 18 before all positive gates or negative certificate
STOP-67 failed proof artifact removed
STOP-68 manifest incomplete
STOP-69 nondeterministic archive/reproduction
STOP-70 resource exhaustion interpreted as YES/NO
```

At seal:

```text
set(stop_ids)=={STOP-01,...,STOP-70}
every stop has an owner and executable/manual control
```

---

# 31. Decision-theorem ladder

The positive route advances only in order compatible with dependencies:

```text
DEC-GATE-00 parent + survivor exact
DEC-GATE-01 bridge sources frozen
DEC-GATE-02 formal kernel frozen
DEC-GATE-03 dual obligations + PSC frozen
DEC-GATE-04 MST0-13 REVIEWED
DEC-GATE-05 MST0-08U REVIEWED
DEC-GATE-06 MST0-11 REVIEWED
DEC-GATE-07 MST0-09 REVIEWED
DEC-GATE-08 MST0-22 REVIEWED
DEC-GATE-09 MST0-14 REVIEWED
DEC-GATE-10 MST0-15 REVIEWED
DEC-GATE-11 MST0-17 REVIEWED / universal Pair Access
DEC-GATE-12 MST0-18 REVIEWED / approximate monotonicity
DEC-GATE-13 MST0-19 REVIEWED / bridge ready
DEC-GATE-14 Phase-18 positive decision
```

Negative route:

```text
NEG-GATE-00 exact positive obstruction preserved
NEG-GATE-01 closed-form legal family
NEG-GATE-02 symbolic Splay lower bound
NEG-GATE-03 explicit competitor upper bound
NEG-GATE-04 ratio divergence
NEG-GATE-05 formal proof + human review
NEG-GATE-06 Phase-18 negative decision
```

First exact refutation freezes the positive route at that theorem ID. It cannot be erased by later evidence.

---

# 32. Interpretation rules

## 32.1 MSTC-0002 finite survival

Means:

> The exact frozen calculus survived the v0.3 finite/fresh/adversarial program.

Does not mean:

> It is universally valid.

## 32.2 Locality attack survival

Means no witness was found under the declared attack.

Does not prove MST0-08U.

## 32.3 K6 saturation attack survival

Means no tested legal construction exceeded the frozen repayment capacity.

Does not prove that “six is universally enough.”

## 32.4 Repayment theorem

`MST0-14 REVIEWED` means every legal KEEP in the theorem domain is covered by the proved payment argument.

It does not imply integrability.

## 32.5 Integrability theorem

`MST0-15 REVIEWED` means local transfer/payment rules coexist in a globally valid accounting with controlled endpoints/decomposition.

It does not automatically imply Pair Access until MST0-17 composes the whole execution.

## 32.6 Pair Access

`UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED` is not yet Dynamic Optimality.

## 32.7 Positive-route refutation

Refuting MSTC-0002 or one of its required lemmas refutes this proof mechanism as stated.

It does not refute Dynamic Optimality.

## 32.8 Negative theorem

Only a real Splay-vs-OPT divergence family can support `DYNAMIC_OPTIMALITY_DISPROVED`.

---

# 33. Allowed and forbidden claims by result level

## 33.1 `BOUNDED_DELETE_INJECTION_PROVED`

Allowed:

> Under the exact frozen MSTC-0002 semantics, DELETE-side injection is universally bounded by the proved constant times A-side cost.

No Pair-Access claim.

## 33.2 `UNIVERSAL_LOCALITY_PROVED`

Allowed:

> The exact reference modifications required downstream satisfy the proved arbitrary-`n` bound.

No repayment claim.

## 33.3 `SYNCHRONOUS_KEEP_TRANSFER_PROVED`

Allowed:

> Every legal KEEP satisfies the frozen repayment theorem.

No global Pair-Access claim until integrability/composition.

## 33.4 `GLOBAL_INTEGRABILITY_PROVED`

Allowed:

> The frozen local calculus admits the proved global accounting.

Still requires composition/telescope.

## 33.5 `UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED`

Allowed:

> The exact universal Pair-Access inequality has been proved for all legal paired executions under the frozen conventions.

No DOC claim before MST0-18/19.

## 33.6 `APPROXIMATE_MONOTONICITY_PROVED`

Allowed only after the telescope theorem and endpoint/additive-term audit.

## 33.7 `DYNAMIC_OPTIMALITY_PROVED`

Allowed only after all ten positive critical nodes are REVIEWED and Phase 18 regenerates the bridge result from frozen artifacts.

## 33.8 `MSTC0002_UNIVERSAL_COUNTEREXAMPLE`

Allowed:

> MSTC-0002 is false as a universal Pair-Access calculus, with this exact legal witness/family.

Forbidden:

> Dynamic Optimality is false.

## 33.9 `DYNAMIC_OPTIMALITY_DISPROVED`

Allowed only after the negative real-Splay/competitor divergence theorem is formally checked and human reviewed.

---

# 34. Final seal checklist

Before Phase 19:

```text
FOUNDATION
[ ] exact full parent v0.3 seal pinned
[ ] MSTC-0002 exact
[ ] sibling kills preserved
[ ] blocker DAG exact
[ ] spec/prereg frozen

BRIDGE SOURCES
[ ] L2/L3 exact premise artifacts frozen
[ ] theorem statements/hypotheses extracted independently

FORMAL KERNEL
[ ] Lean toolchain exact
[ ] no sorry/admit/undeclared axioms
[ ] executable/formal semantics bound

THEOREM CAMPAIGN
[ ] every critical theorem has exact statement + negation
[ ] every critical proof has formal artifact
[ ] every REVIEWED node has human ACCEPT bound to theorem SHA
[ ] every refutation retained
[ ] proof mutants caught
[ ] PSC definitions remained frozen

LOCALITY / PRESERVATION / BOUNDARY
[ ] MST0-08U disposition exact
[ ] MST0-11 disposition exact
[ ] MST0-09 disposition exact

INJECTION / CONSTANTS
[ ] MST0-13 disposition exact
[ ] MST0-22 disposition exact

KEEP
[ ] K6 attack record complete
[ ] MST0-14 disposition exact

INTEGRABILITY
[ ] double-spend attack complete
[ ] credit-use graph checks complete
[ ] MST0-15 disposition exact

PAIR ACCESS / BRIDGE
[ ] MST0-17 disposition exact
[ ] MST0-18 disposition exact
[ ] MST0-19 disposition exact

NEGATIVE
[ ] no local failure mislabeled DOC disproof
[ ] if NO claimed, real Splay lower bound proved
[ ] explicit competitor upper bound proved
[ ] ratio divergence proved
[ ] negative theorem formal + reviewed

DECISION
[ ] Phase 18 regenerated from artifacts
[ ] exactly one terminal branch
[ ] YES only if all ten positive nodes REVIEWED
[ ] NO only if negative divergence theorem REVIEWED
[ ] otherwise exact no-claim level

REPRODUCIBILITY
[ ] threats T001..T120 exact
[ ] stops STOP-01..70 exact
[ ] invariants INV-001..100 exact
[ ] all tests/mutants pass
[ ] counterexamples retained
[ ] manifest complete
[ ] archive rebuild byte-identical
[ ] fresh checkout reproduces FINAL_RESULT
[ ] AI use disclosed
```

---

# 35. Success criteria

v0.4 counts as scientifically **successful** only if one of two outcomes is sealed:

```text
S1  DYNAMIC_OPTIMALITY_PROVED
S2  DYNAMIC_OPTIMALITY_DISPROVED
```

Every other exact result is scientifically valuable but is classified as a non-success terminal outcome for this decision program.

The experiment must prefer an honest no-claim result over an invalid binary conclusion.

---

# 36. Purpose questions the final report must answer

`DECISION_REPORT.md` must answer at least:

```text
Q01 What exact v0.3 seal and MSTC-0002 bytes were imported?
Q02 Was the v0.3 survivor mutated anywhere in v0.4?
Q03 Were the two fresh-killed siblings preserved?
Q04 What exact positive blocker DAG was frozen?
Q05 What exact L2/L3 bridge sources were frozen?
Q06 Does the Lean kernel match executable Splay semantics?
Q07 Are there any theorem-critical axioms/sorries?
Q08 What exact universal MST0-08U statement was attacked?
Q09 Did Locality Explosion find a counterexample?
Q10 What proves or refutes universal locality?
Q11 What exact preservation invariants does MST0-11 require?
Q12 Were all ROOT/ZIG/LL/RR/LR/RL and ledger cases covered?
Q13 What proves or refutes transfer preservation?
Q14 What exact raw-boundary law does MST0-09 state?
Q15 What was the strongest Boundary Torture witness?
Q16 What proves or refutes the boundary law?
Q17 Did the parent MST0-13 proof survive formalization and hostile review?
Q18 What exact injection constant was proved?
Q19 What proves C=2 and k=6 are universal constants rather than fitted parameters?
Q20 What is the exact mathematical meaning of k in MSTC-0002?
Q21 What did K6_SATURATION_ATTACK maximize?
Q22 Did it find an exact repayment counterexample?
Q23 If not, what structural lemma explains the obstruction to higher demand?
Q24 What is the complete MST0-14 theorem statement?
Q25 Is every positive-regret KEEP covered?
Q26 What is the formal repayment proof or exact refutation?
Q27 What did the Double-Spend Apocalypse attempt?
Q28 Was any credit consumed twice?
Q29 Can transfer cycles reactivate spent mass?
Q30 Is accounting decomposition-independent?
Q31 What controls terminal energy/flow?
Q32 What is the exact MST0-15 theorem or obstruction?
Q33 Were MST0-08U/09/11/13/14/15/22 all REVIEWED before MST0-17?
Q34 What exact Pair-Access inequality was proved?
Q35 What is A(n), if nonzero?
Q36 Are endpoint terms controlled independently of sequence length?
Q37 What exact approximate-monotonicity theorem follows?
Q38 Does the bridge source theorem match the Splay variant?
Q39 Does the cost convention match?
Q40 Does the initial-tree convention match?
Q41 Does the subsequence convention match?
Q42 Is the additive term compatible?
Q43 Is the implication direction exact?
Q44 Were all ten positive critical nodes REVIEWED at Phase 18?
Q45 If yes, what exact Dynamic Optimality theorem was emitted?
Q46 If the positive route failed, which theorem failed first?
Q47 What exact counterexample/proof defect caused failure?
Q48 Was obstruction lifting activated?
Q49 Is the negative family closed form?
Q50 What is the symbolic Splay lower bound?
Q51 What explicit BST competitor gives the OPT upper bound?
Q52 What proves ratio divergence?
Q53 Is the negative proof independent of MSTC-0002?
Q54 Did Phase 18 emit YES, NO, or a no-claim status?
Q55 Why was no stronger claim permitted?
Q56 Which proof mutants were caught?
Q57 Which human reviews were recorded and against which theorem SHAs?
Q58 Were any reviewed theorems later invalidated by erratum?
Q59 Does fresh checkout regenerate the exact terminal claim?
Q60 What may a paper claim, and what must it explicitly not claim?
```

---

# 37. Frozen reference notes

The final repository `CITATIONS.md` uses exact metadata from the frozen source manifest.

Logical roles:

```text
Sleator & Tarjan 1985:
  ordinary bottom-up Splay semantics/context.

Levy & Tarjan SODA 2019 / arXiv foundation:
  exact positive bridge premise only after Phase-02 source freeze and Phase-16 convention audit.

Chmel et al. 2026:
  inherited ontology/context through v0.3; not a new logical premise unless explicitly promoted and audited.

SPLAY-AM-MST-v0.3:
  sealed source of MSTC-0002, fresh sibling kills, finite survivor evidence, theorem frontier, and imported reviewed structural lemmas.
```

No current-web summary may override the frozen theorem source used in the final proof.

---

# 38. Final frozen statement of intent

`SPLAY-AM-DECIDE-v0.4` begins where v0.3 deliberately stopped.

v0.3 answered:

> **Is there a concrete constant-factor transfer calculus worth taking seriously?**

Its sealed answer was one exact survivor:

```text
MSTC-0002 = (P_all,k=6,C=2)
```

v0.4 does not search for a prettier replacement.

It freezes that survivor and the complete mapped theorem frontier.

The positive assault is:

```text
universal locality
+ transfer preservation
+ raw boundary theorem
+ reviewed DELETE injection
+ constant independence
+ universal KEEP repayment
+ global integrability
+ Pair-Access composition
+ telescope / approximate monotonicity
+ exact Levy-Tarjan bridge
```

The negative assault is activated only by exact obstruction and requires a real Splay-vs-OPT divergence theorem.

The experiment is intentionally hostile to both sides:

```text
- every theorem has an exact negation;
- every proof has a formal kernel artifact;
- every proof has a counterexample attack;
- every theorem-critical status has human review;
- every failed attempt is preserved;
- every local obstruction is forbidden from masquerading as a DOC disproof;
- every finite survival result is forbidden from masquerading as a theorem.
```

The strongest positive endpoint is:

```text
DYNAMIC_OPTIMALITY_PROVED
```

The strongest negative endpoint is:

```text
DYNAMIC_OPTIMALITY_DISPROVED
```

Those are the only successful outcomes.

If neither theorem closes, v0.4 seals the exact first unresolved or refuted mathematical wall and says no more.

The experiment's governing question is therefore no longer “what should we try next?”

It is:

```math
\boxed{\textbf{IS ORDINARY BOTTOM-UP SPLAY DYNAMICALLY OPTIMAL OR NOT?}}
```

and every implementation choice in this specification exists to make the answer, if obtained, survive hostile scrutiny.

**End of frozen implementation specification.**
