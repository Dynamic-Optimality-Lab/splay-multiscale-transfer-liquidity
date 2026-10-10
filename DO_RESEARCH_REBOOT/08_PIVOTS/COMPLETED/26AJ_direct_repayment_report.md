# PIVOT-26AJ REPORT — UNIVERSAL FORMER-ROOT REPAYMENT THEOREM

## Verdict

```text
PROVED:
UNIVERSAL FORMER-ROOT SUCCESSOR
COARSE-DOUBLE THEOREM;
GENUINE POSITIVE-DEFICIT CLASS COVERED
```

## A. Safety
Branch `coarse-double-branch`, HEAD `88d3007` (+ clean tree at session start; this
session wrote only inside `DO_RESEARCH_REBOOT/`). No reset/clean/stash/commit,
no source/test/config edits. (Note: prompt expected `wp5x-k6c2-specialized`/
`88f344d`; per standing rules the pushed checkpoint branch/HEAD won and the
prompt itself anticipated `coarse-double-branch`/`88d3007`.)

## B. Source definitions
a=ceil(d_A/2) all accesses; KEEP q=floor(d_B/2); DELETE q=0; A=Σa, Q_B=Σq;
KEEP splays both, DELETE A-only with B frozen, fixed key set
(`wp6_coarse_double.py:28-53`, `wp6_eventflow.py:84-182`).

## C. Block decomposition
Universal proof (Lemma 1): zero-A ⇒ banked zero-A; else cyclic A-root blocks,
single-key followers, ≤1 nontrivial B splay each, `Σδ_i = Q−2A`.

## D. Former-root depth lemma
Universal rotation-case proof (`d ≤ 2`, both engines) + 2952-trial
falsification probe (0 violations). Full derivation in audit companion.

## E–F. Repayment theorems
26AJ-A (δ_i=1 + former-root successor) and stronger 26AJ-B
(`δ_i ≤ 2a_{i+1}−1`) via disjoint cyclic pairing; m=1 degenerate case closed
by contradiction. Exact statements + proofs in `02_PROVED` doc.

## G. Non-overlapping matching
Successor map injective mod m; successors (≤−1) never positive; leftovers
nonpositive; wraparound covered. Proved, not assumed.

## H. Seven-key replay
Diagonal vine-7 start; prefix D7,D6; closed 8-word verified leg-by-leg
(costs, closure of BOTH trees by serial equality, leaders, blocks, deficits,
former root 1, successor KEEP 1, B-depth 6, totals 14/9/−19, `replay()`
identical). Repetition ⇒ arbitrarily long covered walks.

## I. Restricted Coarse-Double result
`Q_B ≤ 2A` for all closed walks whose positive blocks have former-root
successors within capacity — including a genuine δ=+1 overflow at n=7,
B-depth 6, outside zero-A/n≤6/bounded-depth coverage. No J4 anywhere.

## J. Four-rule audit
RULE 1 — STRICTLY SMALLER: PASS (successor-conditioned closed walks only).
RULE 2 — CONCRETE SOURCE MECHANISM: PASS (run structure + splay mechanics).
RULE 3 — COMPLETE ONE-SESSION PROOF: PASS (lemmas + theorems + witness).
RULE 4 — NEW ORIGINAL COARSE-DOUBLE OBLIGATION DISCHARGED: YES (positive-deficit
closed class with validated witness).

## K. Pipeline advancement
PAIR ACCESS → C.ZIG RUN DECOMPOSITION → BOUNDED-DEPTH CHARGING [banked] →
FORMER-ROOT OVERFLOW REPAYMENT [26AJ proved: Theorems A+B + witness] →
UNRESTRICTED COARSE-DOUBLE [OPEN] (+ C.ZIG ≤ A banked → B ≤ 3A conditional →
PIVOT-2 conditional → LT conditional → DO open). Restricted charging is progress
inside Coarse-Double; unrestricted CD does not follow.

## L. Final decision
PROVED verdict recorded. No 26AK launched (not auto-authorized; next step would
need its own four-rule gate — natural continuation: indirect/multi-step repayment
or larger-deficit capacity, unscoped here).
