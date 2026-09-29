# B StepEv count lemma (MSTL-14P supporting lemma D2)

Domain: PresentLegalPairInstance, ordinary bottom-up Splay.

## D2 statement

For a present key at B-depth d = y-1 with B StepEv count e_B:

    ceil(d/2) <= e_B <= d,   i.e.   2*e_B >= d = y-1.

Proof: total B-rotations telescoping to splay a depth-d node to root equal d
exactly (ZIG reduces depth by 1; LL/RR/LR/RL reduce it by 2). Each StepEv
covers 1 rotation (ZIG) or 2 (doubles). Hence e_B events cover d rotations
with 1-2 each: e_B >= d/2, i.e. e_B >= ceil(d/2); and e_B <= d. Cases
ROOT (d=0, e=0), ZIG, LL, RR, LR, RL all satisfy this counting; no symmetry
is assumed beyond the verified per-case rotation counts (1 vs 2). QED.

## Raw bandwidth corollary (rho=2 role, partial)

need = max(y-2a,0) <= y-1 (a>=1) <= 2*e_B. Under FLAT(2) each eligible B
StepEv activates up to 2 LATENT credits, so raw current-access B service
bandwidth 2*e_B >= need. THIS IS RAW CAPACITY, NOT USABLE LIQUIDITY:
eligibility/support may restrict which LATENT credits each B event can
activate (see service-lemma gap). The absent witness breaks exactly this
relation (need>0 with e_B=0); present access restores it structurally.

Status: PROVED (counting + property tests below). Raw bandwidth only;
eligible-bandwidth theorem still open (service lemma).
