# GAP anti-padding + Rule 1/2 re-certification

## Interventions are genuine

D4 (idx 5, K1→K9): a=1≥1, B frozen (DELETE), A changed. D6 (idx 7, K9→K5):
a=2≥1, B frozen, A changed. No a=0 no-ops; legal DELETEs; costs exact.

## Removing them changes the walk (no padding invariance)

17-access K5: dA=2/a=1; 15-access K5: dA=5/a=3. K3's fourth block: D4 here vs
K9 there. A-depth sequences, block decomposition (17 vs 15 blocks), packet
structure, and AM-G membership all differ. No banked theorem states
DELETE-removal preserves coverage in either direction (ledger/domains
checked); none is assumed. The walk is not reducible to the failed 15-access
control or to any banked domain by deletion.

## Structural delta vs G0-C control

+ D4 after K1 (idx 4): makes D4 (not K9) K3's fourth block ⇒ AM-G G4 fails.
+ D6 after K9 (idx 6): re-routes A so K5 pays via Type P at dA=2 and the later
  K9 returns with a=1 ⇒ AM-G G5 fails. Tail D8,D2,D1,D6,D9 closes the pair
  exactly (verified serials). Formal coverage is new; mathematical-significance
  claims beyond that are not made.

## Rule 1 (re-certified)

Unchanged Type K/P nine-core subclass: nonempty (this witness: 5 genuine keys,
core 9 throughout, both debts Type P) and proper (banked D3,D3,K3… control:
K3 a=0/prev-a=0, both types fail — revalidated byte-identical this run).

## Rule 2 (re-certified)

Eight-step charging proof unchanged and valid under current sources (G0-C
audit stands; definitions identical; this witness's debt intervals satisfy
H≥2 with w=1≤R=2 each — K3: H(idx2-interval)≥a(D4)+a(K3)=2; K5 likewise).
Independent of AM-G packets (no packet premise used). No alternative proof
constructed.
