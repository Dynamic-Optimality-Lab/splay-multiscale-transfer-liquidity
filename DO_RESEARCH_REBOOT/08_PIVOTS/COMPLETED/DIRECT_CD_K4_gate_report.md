# DIRECT-CD-K4 gate report — CDK4-A (PROVED)

## A. Repository status

Branch `coarse-double-branch`, HEAD `23392fc` verified at start (= banked
commit); sources unchanged; all writes under `DO_RESEARCH_REBOOT/`.

## B. Gate 0 + four rules

PASS — CD-K4 AUTHORIZED (witness 19/10/−28 exact; all recognizers REJECT;
frozen constants: +2 growth, 7 nodes, η depth-6 bit, 56/840/7920/60060).

## C. Strict-gap witness replay

Authoritative + independent 15/15; closure PASS/PASS; sole positive K7
(a=1,q=3,δ=+1,dB=6,r=1; successors D-keys 2,4,6) outside AJ–AS (analytic +
executable). W<0: gap example, not counterexample.

## D–F. Rotation geometry, growth, pruning, reduction

Single-rotation lemma (+1 max; 0 if pivot marked); marked accesses
nonincreasing; unmarked ≤+2 (first mark-acquiring StepEv budget); pruning
commutes for marked x (path/rotation/marked-depth agreement); growing-set
induction + closure rotation gives core ≤7 at every cyclic B-state.

## G–H. Finite certificate + one-bit potential

68,876/68,876 verified, 0 violations, 0 engine mismatches, 1,280 positives
covered; potential unmodified post-freeze.

## I–K. Conservation, theorem, obligation removed

Q_B≤2C_K (η telescoping, exact seam) ≤2C_X≤2A (contraction + StepEv charging);
|supp(KEEP)|=4 proved; with RT2-A, ≤4. Removed: the complete four-KEY-key
cardinality layer from the original pipeline. Controls A (q=3 real), B
(Q=10=C_K·2−2 tight-ish, B-closed), D/E (no idempotence/E/S assumptions) pass.

## L. Terminal, files, publication

```text
CDK4-A — PROVED; four-key obligation eliminated; 5+ keys OPEN; DO OPEN.
```

Files: 12 under 06_CERTIFICATES/DIRECT_CD_K4/ + 02_PROVED doc + this report;
ledger + dependency graph updated. Committed + pushed (SHA verified).
No new gate launched. STOP.
