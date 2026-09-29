# E1-CAPACITY LEMMA (Stage-B Zone Lemma, author-level PROVED)

Status: PROVED (pure pigeonhole over banked U=0 + E-eligibility structure; no geometry).
Date: 2026-09-30. Step: ST/LS-00. Artifact: `loadstruct.json` (finite check).

## Statement

Let t be a present-key legal access with key x, e_A = #(sited A-StepEvs of t),
e_B = #(B-StepEvs of t). Run chronological deterministic least-loaded
(capacity 3, canonical oldest-first tie-break; proof uses no tie-break property).

(a) If e_B <= 3*e_A, every B-StepEv b of access t satisfies
    min_{a in N(b)} load_before_b(a) <= 2 (via E1 sources alone).
(b) If e_B <= 2*e_A, every B-StepEv b of access t satisfies min <= 1 (via E1).

## Proof

E1(t) = sited A-StepEvs of access t; |E1(t)| = e_A; slots 3*e_A.
E1(t) ⊆ N(b) for every B-StepEv b of t (E1 edges, build_tagged/wp6_eventflow2).
Loads on E1(t) come ONLY from access-t B-events: E2/E4 reference A-StepEvs of
strictly earlier accesses (windows (prevkeep,idx), setup != idx); E3 same-access
eligibility is exactly access-t B-events. (E1 sources are created during t's
A-part, before t's B-part; U=0 gives sitedness.)
Before the j-th B-event of t (1 <= j <= e_B), at most j-1 <= e_B-1 assignments
have landed on E1(t).
(a): E1-load-total <= e_B-1 <= 3*e_A-1 < 3*e_A = slots. If all E1 >= 3,
total >= 3*e_A. Contradiction. Some E1 member has load <= 2. It lies in N(b).
(b): total <= 2*e_A-1 < 2*e_A. All >= 2 impossible. Some member has load <= 1.

## Consequence

Stage-B danger zone is EXACTLY B-heavy accesses (e_B > 3*e_A); minload-1 zone
exactly e_B > 2*e_A. Non-heavy accesses are CLOSED without any geometry.

## Finite check (loadstruct.json, 120 histories, B=7075)

e_B <= 2*e_A events: 5554/5554 minload <= 1 (0 viol).
e_B <= 3*e_A events: 5893/5893 minload <= 2 (0 viol).

## Dependencies

U=0 (sitedness), E1/E2/E3/E4 eligibility structure (build2/build_tagged),
chronological allocator definition. GC-independent. Lean-pending.
