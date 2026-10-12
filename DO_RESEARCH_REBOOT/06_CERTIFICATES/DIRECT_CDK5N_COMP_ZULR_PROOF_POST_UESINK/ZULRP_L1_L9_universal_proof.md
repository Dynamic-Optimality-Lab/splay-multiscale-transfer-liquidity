# ZULRP L1–L9 universal proof (Gate C — reconstructed, fixture-free)

For arbitrary W satisfying frozen H1–H5 (any ambient size, length, DELETEs,
order, prefixes, divergence, seams). No Q≤2C_K premise anywhere below.
Mechanism (exactly one): a single positive-debt interval outside strict K/P
pays its own debt from intrinsic local A-credit; every other positive debt
is paid locally by strict K/P. No sink. No transfer. No packet.

L1 (partition): cyclic KEEP intervals cut at KEEPs (seam by closure); each
access in exactly one I_j. ΣH=A, Σq=Q, Σc=C_K (hence Σw=Q−2C_K,
ΣR=2(A−C_K)).

L2 (baseline + debt): H≥c (c=0 trivial; c=1 with H=0 would freeze the root
at the previous key — all accesses A-root no-ops — contradicting a
different-key KEEP); so R≥0. Marked core (ancestor-closed root→marked-key
paths, nine nodes by H1) contains every genuine KEEP root path: ≤8 edges,
d_B≤8, q≤4 (ambient size unrestricted). c=0 ⇒ B rooted + frozen ⇒ q=0 ⇒
w=0. Hence w>0 ⇒ c=1, q∈{3,4}, w∈{1,2}.

L3 (zero-exception classification): E=∅ excludes (c,q,H)=(1,3,1) slots.
It does NOT exclude (1,4,1) with w=2,R=0 — such a slot would need H≥2
reserve via H3/H5, never via H2. E=∅ alone implies no per-interval
solvency (the invalid inference is explicitly rejected here).

L4 (unique self-payer + sharp case): U={w>0,¬K,¬P}={p} (H3); H_p≥2 for
that same p (H4). With c_p=1, q_p∈{3,4}: R_p=2(H_p−1)≥2 and w_p=q_p−2≤2,
so w_p≤R_p intrinsically — no borrowed credit. Sharp case q_p=4,H_p=2:
w=2,R=2, equality 2=2 (included). q_p=3,H_p=2: 1≤2. No H≥3 requirement
(IN H_p=18 is corroboration, not a threshold).

L5 (others, predicates first): j≠p. w≤0 ⇒ w≤R. w>0 ⇒ strict-K (d_A≥3 ⇒
a≥2 ⇒ H≥2) or strict-P (a≥1 both ⇒ H≥2) by H5; with c=1, R=2(H−1)≥2≥w.
IN: iv4 K (dA=4); iv8 K (dA=3) + P (prev-D4 distinct, a≥1 both); iv12 K
(dA=4). H≥2 is a CONSEQUENCE, never the definition.

L6 (no double spending): every interval pays only its own debt (p from
R_p; others from R_j; nonpositives need nothing). No sink is introduced;
no credit transfers; no reserve reused; no A-cost double-counted; K/P
overlap never duplicates credit; seam wraps exactly once.

L7 (telescoping): Σw≤ΣR ⇒ Q−2C_K≤2(A−C_K) ⇒ Q≤2A (IN: 4≤80 ⇒ 36≤112).

L8 (classification independence): E=∅/uniqueness/H≥2 classify only
(verified textually: no sink/relay/transfer in any payment step). No
H2/H3/H4 change; no multi-payer variant claimed.

L9 (hypothesis audit): keys/core feed only the debt bound; H2 is redundant
under H3+H4 (documented, retained, checked); H3/H4 load-bearing for the
unique payer; H5 classifies the rest. No generalization claimed. ∎
