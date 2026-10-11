# DLSS L1–L7 universal payment proof (Gate C — reconstructed)

Domain H1–H6 frozen. Claim Q≤2A for every member. Relay lengths play NO
payment role (audit §C9); the proof below never queries short-vs-long.

## C1 — Interval identities

Cyclic KEEP intervals partition accesses exactly once (seam by closure):
ΣH=A, Σq=Q_B, Σc=C_K, Σw=Q−2C_K, ΣR=2(A−C_K) (verified on IN: 55/36/16).

## C2 — Baseline

H≥c: c=0 trivial; c=1 by A-root-change (a=0 ⟺ current A-root; root splays
are no-ops; if H=0 the terminal KEEP would repeat the previous key,
contradicting c=1). R≥0. No-ops/DELETEs unrestricted.

## C3 — Nine-core bound (arbitrary ambient trees)

Marked B-ancestor core: union of root-to-marked-KEEP-key paths (authoritative
definition: ancestor-closed marked set; every such path lies inside the core
by construction). H1 gives |core|=9. A genuine KEEP key is marked, so its
root path has ≤8 edges ⇒ d_B≤8 ⇒ q≤4. Ambient size unrestricted (paths stay
in core). c=0 ⇒ B still rooted (DELETEs freeze; single KEEP per interval) ⇒
q=0 ⇒ w=0. Hence w>0 ⇒ c=1, q∈{3,4}, w∈{1,2}.

## C4 — Exceptions

|E|=2, each (1,0). Strict K needs d_A≥3 ⇒ a≥2 ⇒ H≥2 ≠1; strict P needs two
a≥1 accesses ⇒ H≥2 ≠1. Neither holds; E complete by definition.

## C5 — Joint sink (full q_p table)

∃p∉E (c=1,H≥3, enumerated existentially). R_p≥4; w_p=q_p−2≤2:
q=0→−2, 1→−1, 2→0, 3→1, 4→2 — each with 2+w_p≤R_p given R_p≥4 (tight 4≤4 at
q=4,H=3, included). So 1+1+w_p ≤ 4 ≤ R_p. IN: p=0, H=18, q=3, w=1, R=34
(3≤34). ∎

## C6 — Others

j∉E∪{p}: w≤0 ⇒ w≤R; w>0 ⇒ strict-K (d_A≥3 ⇒ a≥2 ⇒ H≥2) or strict-P
(a≥1 both ⇒ H≥2) ⇒ c=1 ⇒ R=2(H−1)≥2≥w. IN other-positive iv8 (H=4):
strict-K (dA=3) and strict-P both hold.

## C7 — Disjointness

{e1,e2,p} distinct; triple + singletons partition intervals; sink spent
once; exceptions never recharged; accesses counted once.

## C8 — Telescoping

Σw≤ΣR ⇒ Q−2C_K≤2(A−C_K) ⇒ Q≤2A (IN: 4≤78 ⇒ 36≤110).

## C9 — Relay-independence audit

Steps C1–C8 reference relay lengths NOWHERE except H3 domain membership:
bridges are ordinary w≤R singletons (L5/C6); the mixed-vs-dual-long
distinction classifies but never pays. Substituting MSINK's mixed H3 with
DLSS's dual-long H3 changes no payment step (verified by textual audit of
C1–C8 above: no short-relay assumption, no strengthening, no removal).
Rule 2 holds for the dual-long domain as written. ∎
