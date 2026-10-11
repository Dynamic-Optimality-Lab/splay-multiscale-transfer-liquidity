# MSINK finalization four-rule verdict (task J) — CDK5NCMS-A GATE 0 APPROVED

Independent re-evaluation on finalization evidence (63-check verifier PASS,
predecessor audit, additive analysis, 41-attack rerun PASS, battery rerun PASS).

## R1 — Strictly Smaller: PASS

W_IN (`19ff110a…78df`, 61/36/16) ∈ MSINK ∩ R5: closed, engines agree,
5 genuine keys, core9 ×35, E=[4,12], t=(0,2), joint sink p=0 (H=13, 1+1+1≤24),
others narrow-H5 (strict-P), 17/17 banked negatives, no S0-splits.
W_OUT (`b8b02be7…bedab3`, 55/36/16) ∈ R5 ∖ MSINK: same validity backbone;
MSINK-false at the mixed-relay gate (t=(2,2)); MR-H6 fails at iv0
(dA=0/KEEP-a=0); 17/17 banked negatives; no S0-splits.
Neither is an old control (both n=34 campaign mutants, full SHAs pinned,
constructions verified). ∅ ≠ (MSINK ∩ R5) ⊊ R5 certified both sides.

## R2 — Solvability Mechanism: PASS

Unchanged L1–L7 (`MSINK_universal_payment_proof.md` in this directory;
frozen H1–H6 in `MSINK_frozen_theorem.md` sibling record, hashes below):
baseline/identities, nine-core debt bounds, exception arithmetic,
joint sink (worst-case q_p=4 ⇒ w_p≤2 ≤ R_p−2 with H_p≥3; H4/H5 JOINT
existential eligibility, min-first certificate — ∃-equivalence verified:
8 eligible sinks, min selected), others (explicit w≤R + K/P cases;
frozen-narrow-H5 holds on IN via strict-P), disjoint triple+singletons,
telescoping to Q_B≤2A. No witness-specific substitution, no aggregate
premise, no new hypothesis. Finite replays certify instances only; the
universal argument stands on its own derivations.

## R3 — One-Prompt Scope: PASS

One frozen theorem, one mechanism, original bounded campaign preserved
(956 words, fixed order verified byte-equal, caps met, L2 correctly unrun),
no aperiodicity filter (aperiodicity audit PASS), no replacement witnesses
(constructions pinned to census indices), no new campaign, no promotion
(`02_PROVED/` untouched; ledger/deps reconciled — R1HARD appends removed,
content preserved in this directory).

## R4 — Upward Progress: PASS

Genuine new IN coverage: source-valid, closed, independently reproduced
(pointer + tuple), outside the complete 17-mechanism union and certified
additive closure (first-eligible in campaign order among 8 predecessors with
proved dispositions; 45-member IN-tractable landscape, all clean).

## Final condition

All four rules PASS; finalization audits green (verify 63/63, order audit,
additive regression, attacks 41/41 with 0 hard fails, battery, controls).

**CDK5NCMS-A — FOUR-RULE GATE 0 APPROVED (Gate-0 approval only; no PROVED
theorem; MSINK-PROOF remains separately authorized work).**

## Appendix — frozen theorem record (verbatim copy, E-task)

Source: `DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_MSINK_G0_R1HARD/MSINK_frozen_theorem.md`
SHA-256 of source file: recorded in terminal status.
“Domain: admissible reachable exactly-closed pair-walks. H1: five genuine
KEEP keys + nine-node marked B-core at every cyclic state. H2: exception set
E={j:c=1,q=3,H=1} (w=1,R=0 each), |E|=2 exactly, E={e1,e2}, all listed (VR
singletons excluded; MR multi-relays admitted as raw members pending
novelty). H3: per exception maximal creditless run (c=1,H=1,q≤2), lengths
exactly one short t∈{0,1} + one long t≥2 (rotation-invariant classification;
distinguishes from MR). H4+H5 JOINT existential eligibility: ∃ single index
p∉E with c_p=1,H_p≥3 AND ∀j∉E∪{p}: w_j>0 ⇒ (K_j∨P_j). Enumerate every
H4-eligible sink; accept iff at least one also satisfies H5; canonical-first
(rotation-invariant) choice for certificates. Never reject merely because the
first H4-only sink fails H5. Type K (d_A≥3) / Type P (preceding DELETE y≠x,
a≥1 both) banked unchanged. Claim Q_B≤2A. Arbitrary n/length/DELETEs/order/
prefixes/divergence/seams. No packet/E-S/Q≤2C_K/potential/aggregate premises.
Frozen.”
Note: executed membership uses min-first among JOINT-eligible sinks;
∃-equivalence verified on IN (8 eligible, min taken) and globally on census
survivors by construction audit; rotation-dependence of the index label does
not affect payment soundness (any valid p satisfies the joint inequality).
