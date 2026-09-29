# Local present mechanics (MSTL-14P supporting lemmas D0-D1)

Domain: PresentLegalPairInstance (every access key in keys(T0); FIXED_KEY
closure gives presence in both trees at every occurrence).

## D0 (closure restatement)

keys(S_x(T)) = keys(T) for present x (rotations permute nodes); hence
keys(A_i) = keys(B_i) = K for all i. Proved in tests/test_present_domain.py.

## D1 PRESENT_POSITIVE_DEBT_IMPLIES_B_WORK

Claim: for present x at a KEEP with need > 0, the B splay trace is nonempty.
Proof: need = max(y-2a,0) > 0 gives y > 2a >= 2 (a>=1, present costs defined),
so y >= 3 and d_B(x) = y-1 >= 2. Bottom-up splay of a present node at depth
>= 1 performs >= 1 rotation, emitting >= 1 StepEv. Hence Bev nonempty. QED.

Stronger easy branch: A trace empty at a KEEP implies x is A-root (a=1).
With need > 0 this forces y > 2, i.e. d_B(x) >= 2, so B performs nontrivial
structural work. Corollary: Aev empty AND Bev empty implies need = 0 for
present accesses (a=y=1). The absent battery violates exactly this relation
(empty traces with need = 1); that family is excluded by domain here.

Status: PROVED (mechanics + property tests below). Used by: service lemma.
