# DIRECT-CWC frozen ECT specification (v1.1 — hash before testing)

Charter §18 items 1–10 implemented exactly as follows. No redesign after testing.
v1.1 amendment (indexing convention only, per §18 local-audit allowance):
source `_depth_to` paths list nodes from ROOT, so with path P (P[-1]=x_t,
n=len(P)) the consecutive parent-toward-root pairs are
({P[n-2j],P[n-2j-1]}), j=1..q_t, verified equal-as-sets to the j-th source
B-double pushed set in execution order. Unordered pairs and both tracked
relations are unchanged from v1.0; eligibility relation mathematically
identical. v1.0 hash preserved in the hash file for transparency.

## S1. B-demand tokens

Per KEEP access t with pre-B-depth d and pre-access B path keys
[y=x_t, p_1, ..., p_d] (parent toward root): q_t=⌊d/2⌋ tokens
b_{t,j}=(t,j,x_t,p_{2j−1},p_{2j}) for j=1..q_t. The pair MUST equal the j-th
source B-double pushed set (execution order); odd-zig pushes nothing.
DELETE: zero tokens. |B|=Q_B asserted and checked.

## S2. Pair order

First element = nearer parent (p_{2j−1} above p_{2j}... precisely: p_{2j−1}
is the shallower of the two? NO — frozen: listed parent-toward-root, so
p_{2j−1} is DEEPER (nearer x) than p_{2j}. Kept as listed; epochs use both
relations symmetrically.)

## S3. A supply

Per access t (KEEP or DELETE) with a_t source A StepEvs in bottom-up order
e_{t,1..a_t}: exactly two slots (e,0),(e,1) each. 2|E|=2A asserted. No-op: zero.

## S4. Epochs

Whole-access B-boundary serials B_0..B_m (B_m=B_0). For token pair (u,x) dying
at access t (0-indexed; pre H(B_t)=1, post H(B_{t+1})=0): birth b = first index
scanning t−1,t−2,... (mod m) with H(B_b)=0 (terminates since H(B_t)... scan
covers all m; H(B_{t})... precisely: scan j from t−1 downward while H(B_j)=1;
b = first 0 found; H(B_{b+1})=1 by construction). Window I = {b+1,...,t} mod m
(access indices; birth excluded, death included).

## S5. Contacts

RotA(e) = source StepEv rotated-key set (zig 2 keys, double 3 keys).
Intermediate A states S_0..S_k per access captured from an instrumented mirror
splay cross-checked serial-equal against authoritative splay_A on every access
(any mismatch aborts). OwnerA_t(u,v): net=H(S_k)−H(S_0); None if 0, else last e
with H(S_e)=final and H(S_{e−1})≠final. ContactA(e;u,v)=1 iff u∈RotA(e) (C1)
or OwnerA_t(u,v)=e (C2). No other channel.

## S6. Eligibility

Edge b=(t,j,x,p,q) ∼ (s,e) iff [s∈I(p,x;t) ∧ ContactA(e;p,x)] ∨
[s∈I(q,x;t) ∧ ContactA(e;q,x)]. No other edges, no post-hoc additions.

## S7. Capacities

Demand 1 per token; supply 2 per StepEv; integers; bipartite as specified.

## S8. Graph indices

Canonical cyclic rotation (lex-least record rotation) for deterministic
indexing; flow value rotation-invariant (isomorphic graphs).

## S9. Theorem target

Universal cut inequality ∀S⊆B: |S|≤2|N(S)| (UNPROVED — the candidate claim).

## S10. Deterministic flow

Dinic with canonical node order (tokens by (t,j), events by (s,e-index));
augmenting order fixed; accept iff flow value = |B|.
